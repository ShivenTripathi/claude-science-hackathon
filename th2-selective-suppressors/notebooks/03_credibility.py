"""
Phase 2: Credibility pack. Joins reconstructed arms + local annotations and emits:
  1) cutoff-tiered selective list (confident core vs borderline)
  2) donor stability flags   3) KD self-silencing flags
  4) known-regulator recall overlay figure + metric
  5) per-condition (Rest/Stim8hr/Stim48hr) selectivity split
Run after 01_arms.py and 02_annotations.py.
"""
import json, yaml, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path
ROOT = Path("/Users/shiventripathi/dev/science/th2_selective")
DATA, OUT = ROOT/"data", ROOT/"outputs"

arms = pd.read_parquet(OUT/"arms.parquet")
ann  = pd.read_parquet(OUT/"annotations.parquet")
known = yaml.safe_load(open(DATA/"th1_th2_known_regulators.yaml"))
th2_known, th1_known = set(known["th2"]), set(known["th1"])

df = arms.merge(ann, on=["target_gene","culture_condition"], how="left")
# merge richer h5ad QC (neighboring-gene KD, single-guide, proper donor reproducibility)
qc_path = OUT/"obs_qc.parquet"
if qc_path.exists():
    qc = pd.read_parquet(qc_path)[["obs_index","neighboring_gene_KD","single_guide_estimate",
         "distal_offtarget_flag","low_target_gex","donor_correlation_hits_mean","donor_correlation_all_mean"]]
    df = df.merge(qc, on="obs_index", how="left")
else:
    for c in ["neighboring_gene_KD","single_guide_estimate","donor_correlation_hits_mean"]: df[c]=np.nan

# ---------- 1) cutoff sensitivity / tiering ----------
TXS, TYS = [-1.5,-2.0,-2.5], [0.5,1.0,1.5]
def sel_mask(d, tx, ty): return (d.th2_arm < tx) & (d.th2_arm.notna()) & (d.th1_arm.abs() < ty)
robust = np.zeros(len(df), int)
for tx in TXS:
    for ty in TYS:
        robust += sel_mask(df, tx, ty).to_numpy().astype(int)
df["gate_robustness"] = robust                      # 0..9
df["sel_strict"]  = sel_mask(df, -2.5, 0.5)
df["sel_lenient"] = sel_mask(df, -1.5, 1.5)
df["sel_default"] = sel_mask(df, -2.0, 1.0)
def tier(r):
    if r.sel_strict: return "core"
    if r.sel_default: return "confident"
    if r.sel_lenient: return "borderline"
    return "not_selective"
df["tier"] = df.apply(tier, axis=1)

# ---------- 2) donor stability ----------
# use donor_correlation_hits_mean from the h5ad (reproducibility across donors among DE hits;
# median ~0.81 on our set) — far better coverage than the sparse suppl-table crossdonor column.
DONOR_MIN = 0.3
df["donor_hits"] = df.get("donor_correlation_hits_mean", pd.Series(np.nan,index=df.index))
df["donor_stable"] = df.donor_hits.fillna(df.crossdonor_correlation_mean).fillna(-1) >= DONOR_MIN
# richer QC flags
df["neighbor_kd_flag"] = df.get("neighboring_gene_KD", pd.Series(False,index=df.index)).fillna(False)
df["single_guide_flag"] = df.get("single_guide_estimate", pd.Series(False,index=df.index)).fillna(False)
# ---------- 3) KD self-silencing ----------
df["kd_ok"] = df.ontarget_significant.fillna(False) & (df.ontarget_effect_size.fillna(0) < 0) \
              & (df.frac_signif_guides.fillna(0) >= 0.5)
# combined pass = selective(default) + donor stable + kd ok + not artifact class + not off-target
df["passes_all"] = df.sel_default & df.donor_stable & df.kd_ok \
                   & ~df.is_artifact_class.fillna(False) & ~df.offtarget_flag.fillna(False)

selective_rows = df[df.sel_default].copy()
print(f"[selective default gate] rows={len(selective_rows)}  unique genes={selective_rows.target_gene.nunique()}")
print("[tier counts]\n", df[df.tier!='not_selective'].tier.value_counts())
print(f"[of default-selective] donor_stable={selective_rows.donor_stable.mean():.2f} "
      f"kd_ok={selective_rows.kd_ok.mean():.2f} passes_all={selective_rows.passes_all.mean():.2f}")

cols = ["target_gene","culture_condition","th2_arm","th1_arm","tier","gate_robustness",
        "ontarget_significant","ontarget_effect_size","frac_signif_guides",
        "crossdonor_correlation_mean","crossguide_correlation","offtarget_flag",
        "n_total_de_genes","broad_effect_flag","target_class","donor_stable","kd_ok","passes_all"]
selective_rows.sort_values("th2_arm")[cols].to_csv(OUT/"selective_tiered.csv", index=False)

# ---------- headline plane plot (reproduction) ----------
fig, ax = plt.subplots(figsize=(7,7))
bg = df.dropna(subset=["th2_arm","th1_arm"])
ax.scatter(bg.th2_arm, bg.th1_arm, s=3, c="0.78", alpha=.35, label="all perturbations", rasterized=True)
sd = df[df.sel_default]; sk = df[(df.th2_arm<-2)&(df.th1_arm>1)]
ax.scatter(sd.th2_arm, sd.th1_arm, s=11, c="#0f9c82", label=f"selective Th2 suppressor (n={len(sd)})")
ax.scatter(sk.th2_arm, sk.th1_arm, s=30, c="#c0392b", label=f"Th1-skewer (n={len(sk)})", zorder=5)
lim = np.array([-6,4]); ax.plot(lim, lim, c="0.5", lw=1, label="single Th2-vs-Th1 axis (1D)")
ax.axvline(-2, ls="--", c="k", lw=.8); ax.axhline(1, ls=":", c="k", lw=.8); ax.axhline(-1, ls=":", c="k", lw=.8)
corr = np.corrcoef(bg.th2_arm, bg.th1_arm)[0,1]
ax.set_xlim(-6,4); ax.set_ylim(-5,5)
ax.set_xlabel("Th2-arm response (z)   <- suppression"); ax.set_ylabel("Th1-arm response (z)   induction ->")
ax.set_title(f"Selective Th2 suppression resolvable in the 2D arm plane\n(dominant confound = global magnitude, corr={corr:+.2f})")
ax.legend(loc="lower right", fontsize=8, framealpha=.9)
fig.tight_layout(); fig.savefig(OUT/"plane_plot.svg"); fig.savefig(OUT/"plane_plot.png", dpi=140)
print("[fig] wrote plane_plot.svg/.png")

# ---------- 4) known-regulator recall overlay ----------
df["known"] = np.where(df.target_gene.isin(th2_known),"Th2-known",
              np.where(df.target_gene.isin(th1_known),"Th1-known","other"))
# The known-Th2 list is directionally mixed: activators (KD -> Th2 down, should be selective)
# vs repressor-complex members (NuRD/H3K9: KD -> Th1 up, should NOT be selective suppressors).
TH2_ACTIVATORS = {"GATA3","STAT6","IL4R","IL4","RARA","ICOS"}   # KD expected to lower Th2
def best_row(g):
    r = df[df.target_gene==g]
    return None if len(r)==0 else r.loc[r.th2_arm.idxmin()]
print("\n[known Th2 regulators — position on the arm plane]")
for g in sorted(th2_known):
    b = best_row(g)
    if b is None: print(f"  {g:8s} not perturbed/measured"); continue
    tag = "activator" if g in TH2_ACTIVATORS else "repressor/neg-reg"
    print(f"  {g:8s} th2={b.th2_arm:+.2f} th1={b.th1_arm:+.2f} sel={bool(b.sel_default)} "
          f"trend={bool(b.sel_lenient)} [{tag}]")
# recall computed over ACTIVATORS that produced a detectable KD (the ones that *should* be selective)
detect = [g for g in TH2_ACTIVATORS if (best_row(g) is not None and best_row(g).n_total_de_genes>=10)]
recovered = [g for g in detect if df[df.target_gene==g].sel_lenient.any()]
recall = len(recovered)/max(len(detect),1)
th1_in_box = sorted(g for g in th1_known if df[df.target_gene==g].sel_default.any())
print(f"[recall] Th2 activators w/ detectable KD recovered (Th2 down, Th1 flat): "
      f"{len(recovered)}/{len(detect)} = {recall:.2f}  -> {recovered}")
print(f"[specificity] Th1-known landing in selective box (should be ~0): {th1_in_box}")

fig, ax = plt.subplots(figsize=(7,7))
bg = df[df.known=="other"]
ax.scatter(bg.th2_arm, bg.th1_arm, s=3, c="0.8", alpha=.4, label="all perturbations", rasterized=True)
sd = df[df.sel_default & (df.known=="other")]
ax.scatter(sd.th2_arm, sd.th1_arm, s=10, c="#2ca089", label="selective Th2 suppressor")
for g in th2_known:
    r = df[(df.target_gene==g)].sort_values("th2_arm").head(1)
    if len(r): ax.scatter(r.th2_arm, r.th1_arm, s=60, c="#c0392b", edgecolor="k", zorder=5)
    if len(r): ax.annotate(g, (r.th2_arm.iloc[0], r.th1_arm.iloc[0]), fontsize=7)
ax.axvline(-2, ls="--", c="k", lw=.8); ax.axhline(1, ls=":", c="k", lw=.8); ax.axhline(-1, ls=":", c="k", lw=.8)
ax.set_xlabel("Th2-arm response (z)   <- suppression"); ax.set_ylabel("Th1-arm response (z)   induction ->")
ax.set_title(f"Known Th2 regulators (red) recall into selective box\nrecall={recall:.0%}")
ax.legend(loc="upper right", fontsize=8)
fig.tight_layout(); fig.savefig(OUT/"recall_overlay.svg"); fig.savefig(OUT/"recall_overlay.png", dpi=140)
print("[fig] wrote recall_overlay.svg/.png")

# ---------- 5) per-condition selectivity split ----------
piv = (df.assign(sel=df.sel_default.astype(int))
         .pivot_table(index="target_gene", columns="culture_condition", values="sel",
                      aggfunc="max", fill_value=0))
for c in ["Rest","Stim8hr","Stim48hr"]:
    if c not in piv: piv[c]=0
piv = piv[["Rest","Stim8hr","Stim48hr"]]
piv["n_cond"] = piv.sum(1)
def ctx(r):
    if r.n_cond==0: return "none"
    if r.n_cond==3: return "constitutive"
    if r.Rest and not (r.Stim8hr or r.Stim48hr): return "rest_only"
    if (r.Stim8hr or r.Stim48hr) and not r.Rest: return "stim_induced"
    return "mixed"
piv["context"] = piv.apply(ctx, axis=1)
piv_sel = piv[piv.n_cond>0].copy()
piv_sel.to_csv(OUT/"condition_selectivity_matrix.csv")
print("\n[per-condition context of selective genes]\n", piv_sel.context.value_counts())

df.to_parquet(OUT/"candidates_full.parquet")
print("\n[done] selective_tiered.csv, recall_overlay.svg, condition_selectivity_matrix.csv, candidates_full.parquet")
