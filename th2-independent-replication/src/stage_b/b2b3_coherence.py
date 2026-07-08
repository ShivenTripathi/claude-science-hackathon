"""B2-light (arm cross-check) + B3 (co-perturbation coherence) via remote byte-range reads of the zscore layer."""
import sys; sys.path.insert(0, "/Users/shiventripathi/dev/science/th2_suppressor_hardening/src")
from common.remote_h5 import open_remote
import numpy as np, pandas as pd

REPO = "/Users/shiventripathi/dev/GWT_perturbseq_analysis_2025"
T = "/Users/shiventripathi/dev/science/th2_suppressor_hardening/results/tables"
rng = np.random.default_rng(0)

m = pd.read_parquet(f"{T}/arms_aligned.parquet").reset_index(drop=True)  # row i == h5ad obs row i
h5, f = open_remote()
def readcol(grp, name):
    d = grp[name]
    if hasattr(d, "keys") and "categories" in d:
        cats = np.array([x.decode() if isinstance(x, bytes) else x for x in d["categories"][:]]); return cats[d["codes"][:]]
    return np.array([x.decode() if isinstance(x, bytes) else x for x in d[:]])
genes = readcol(h5["var"], "gene_name"); gidx = {g: i for i, g in enumerate(genes)}
Z = h5["layers"]["zscore"]

# --- rows we need: selective hits + anchors (GATA3/STAT6/IL4R) + random null ---
sel_pos = m.index[m.selective].tolist()
anchors = ["GATA3", "STAT6", "IL4R"]
anch_pos = {g: m.index[(m.gene == g)].tolist() for g in anchors}
null_pos = rng.choice(m.index[~m.selective], size=400, replace=False).tolist()
need = sorted(set(sel_pos) | {p for v in anch_pos.values() for p in v} | set(null_pos))
print(f"reading {len(need)} rows x {len(genes)} genes over HTTPS byte-range ...")
Zrows = {}
for j, p in enumerate(need):
    Zrows[p] = Z[p, :]
    if (j+1) % 150 == 0: print(f"  {j+1}/{len(need)} rows ({f.n_bytes/1e6:.0f} MB)")
h5.close()
print(f"done: {f.n_bytes/1e6:.0f} MB in {f.n_reqs} requests (NOT 16.8GB)")

# ---------- B2-light: recompute arm on selective rows, cross-check Haltavey ----------
sig = pd.read_csv(f"{REPO}/metadata/suppl_tables/Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv")
ota = sig[sig.contrast.str.contains("Ota")].groupby("variable").zscore.mean()
th2_arm_genes = [g for g in ota[ota > 0].index if g in gidx]
th1_arm_genes = [g for g in ota[ota < 0].index if g in gidx]
th2_cols = [gidx[g] for g in th2_arm_genes]; th1_cols = [gidx[g] for g in th1_arm_genes]
print(f"\narm gene sets: Th2-up={len(th2_cols)}  Th1-up={len(th1_cols)} (in matrix)")
rec_th2 = np.array([np.nanmean(Zrows[p][th2_cols]) for p in sel_pos])
rec_th1 = np.array([np.nanmean(Zrows[p][th1_cols]) for p in sel_pos])
hal_th2 = m.loc[sel_pos, "th2_arm_raw"].values; hal_th1 = m.loc[sel_pos, "th1_arm_raw"].values
print(f"B2 cross-check on 172 hits: pearson(recomputed th2, Haltavey th2) = {np.corrcoef(rec_th2, hal_th2)[0,1]:.3f}")
print(f"                            pearson(recomputed th1, Haltavey th1) = {np.corrcoef(rec_th1, hal_th1)[0,1]:.3f}")

# ---------- B3: co-perturbation coherence ----------
def coherence(hit_pos, hit_gene, cond):
    zh = Zrows[hit_pos].copy()
    best = -2; best_anchor = None; rs = {}
    for a in anchors:
        aps = [p for p in anch_pos[a] if m.loc[p, "condition"] == cond]
        if not aps: continue
        za = Zrows[aps[0]].copy()
        # mask cis (own target cols) + keep informative genes (|z|>=1 in either)
        mask = np.ones(len(zh), bool)
        for g in (hit_gene, a):
            if g in gidx: mask[gidx[g]] = False
        keep = mask & ((np.abs(zh) >= 1) | (np.abs(za) >= 1)) & ~np.isnan(zh) & ~np.isnan(za)
        if keep.sum() < 20: continue
        r = np.corrcoef(zh[keep], za[keep])[0, 1]
        rs[a] = round(float(r), 3)
        if r > best: best, best_anchor = r, a
    return best, best_anchor, rs

# null distribution of coherence (random non-selective rows vs GATA3 same condition)
null_scores = []
for p in null_pos[:200]:
    c = m.loc[p, "condition"]; b, _, _ = coherence(p, m.loc[p, "gene"], c)
    if b > -2: null_scores.append(b)
null_scores = np.array(null_scores); nmean, nstd = null_scores.mean(), null_scores.std()
print(f"\nnull coherence: mean={nmean:.3f} std={nstd:.3f} (n={len(null_scores)})")

rows = []
for p in sel_pos:
    g, c = m.loc[p, "gene"], m.loc[p, "condition"]
    b, anch, rs = coherence(p, g, c)
    rows.append({"gene": g, "condition": c, "coherence": round(b,3), "best_anchor": anch,
                 "coh_z_vs_null": round((b - nmean)/nstd, 2) if nstd else np.nan, **{f"r_{a}": rs.get(a) for a in anchors}})
coh = pd.DataFrame(rows).sort_values("coherence", ascending=False)
coh.to_csv(f"{T}/coherence_scores.csv", index=False)

# anchor self/cross coherence sanity
print("\nSanity — GATA3 vs STAT6/IL4R (same cond) should be high:")
for c in ["Stim48hr", "Stim8hr", "Rest"]:
    gp = [p for p in anch_pos["GATA3"] if m.loc[p,"condition"]==c]
    if gp:
        _, _, rs = coherence(gp[0], "GATA3", c); print(f"  {c}: GATA3 vs anchors {rs}")

print("\nTop 12 hits by co-perturbation coherence with the Th2 axis:")
print(coh.head(12).to_string(index=False))
print(f"\nhits with coherence z>2 vs null: {(coh.coh_z_vs_null>2).sum()}/{len(coh)}")
print("saved -> results/tables/coherence_scores.csv")
