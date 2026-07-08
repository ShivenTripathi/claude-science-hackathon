"""Stage A rigor: A3 QC gates, A4 donor, A5 threshold sweep, A6 recall@k, A7 Hollbacher, A8 atlas diff.
Produces results/shortlist/hardened_shortlist.csv."""
import numpy as np, pandas as pd, yaml
pd.set_option("display.width", 160)

REPO = "/Users/shiventripathi/dev/GWT_perturbseq_analysis_2025"
S = "/Users/shiventripathi/dev/science/th2_suppressor_hardening"
T, SL = f"{S}/results/tables", f"{S}/results/shortlist"

m = pd.read_parquet(f"{T}/arms_aligned.parquet")
de = pd.read_csv(f"{REPO}/metadata/suppl_tables/DE_stats.suppl_table.csv", index_col=0)
ens_map = de.set_index("target_contrast_gene_name")["target_contrast"].to_dict()  # symbol->ensembl
known = yaml.safe_load(open(f"{REPO}/metadata/th1_th2_known_regulators.yaml"))
th2_known = set(known["th2"]); th1_known = {x.replace("IKFZ1","IKZF1") for x in known["th1"]}

# ---------- A3 QC GATES ----------
ess = set(pd.read_csv(f"{REPO}/metadata/gene_lists/core_essentials_hart.tsv", header=None)[0])
kd = pd.read_csv(f"{REPO}/metadata/suppl_tables/guide_kd_efficiency.suppl_table.csv")
kd_ok = (kd[kd.signif_knockdown].groupby(["perturbed_gene_id","culture_condition"]).size()
         .rename("n_signif_guides").reset_index())
m["ensembl"] = m.gene.map(ens_map)
m = m.merge(kd_ok, left_on=["ensembl","condition"], right_on=["perturbed_gene_id","culture_condition"], how="left")
m["n_signif_guides"] = m["n_signif_guides"].fillna(0)
m["pass_kd"]        = (m.ontarget_significant == True) & (m.n_signif_guides >= 1)
m["not_essential"]  = ~m.gene.isin(ess)
m["no_offtarget"]   = m.offtarget_flag != True
m["well_powered"]   = (m.n_cells_target >= 50) & (m.target_baseMean.fillna(0) > 0.1)
m["hardened_pass"]  = m.pass_kd & m.not_essential & m.no_offtarget & m.well_powered

# ---------- A4 DONOR REPRODUCIBILITY ----------
def donor_tag(r):
    if pd.isna(r.crossdonor_correlation_mean): return "untested"
    if r.crossdonor_correlation_mean >= 0.2 and r.crossdonor_correlation_min > 0: return "robust"
    return "weak"
m["donor_evidence"] = m.apply(donor_tag, axis=1)

# ---------- A5 THRESHOLD SWEEP + stability ----------
grid = [(t2, t1) for t2 in [-1.5,-2,-2.5,-3] for t1 in [0.5,1,1.5,2]]
canonical = set(m.loc[m.selective, "obs_index"])
stab = pd.Series(0.0, index=m.obs_index)
sweep_rows = []
for t2, t1 in grid:
    s = (m.th2_z <= t2) & (m.th1_z.abs() <= t1)
    ids = set(m.loc[s, "obs_index"])
    jac = len(ids & canonical) / len(ids | canonical) if (ids | canonical) else 0
    sweep_rows.append({"th2_thr": t2, "th1_flat": t1, "n": int(s.sum()),
                       "n_genes": m.loc[s,"gene"].nunique(), "jaccard_vs_172": round(jac,3)})
    stab[m.loc[s, "obs_index"].values] += 1
stab /= len(grid)
m["stability_score"] = m.obs_index.map(stab)
pd.DataFrame(sweep_rows).to_csv(f"{T}/threshold_sweep.csv", index=False)

# ---------- A6 RECALL@K of known Th2 regulators ----------
gene_best = m.groupby("gene").th2_z.min()
gene_rank = gene_best.rank(method="min")            # 1 = strongest suppressor
n_genes = gene_best.size
def recall_at(k, gset): return sum(gene_rank.get(g, 1e9) <= k for g in gset) / len(gset)
recall = {k: round(recall_at(k, th2_known), 3) for k in [10,25,50,100,172,250,500]}
th1_ctrl_median_pct = float(np.median([100*gene_rank.get(g,n_genes)/n_genes for g in th1_known if g in gene_rank.index]))
pd.DataFrame([recall]).to_csv(f"{T}/recall_at_k.csv", index=False)

# ---------- A7 Ota vs Hollbacher signature overlap (local, signature-level) ----------
sig = pd.read_csv(f"{REPO}/metadata/suppl_tables/Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv")
ota = sig[sig.contrast.str.contains("Ota")].set_index("variable").zscore
hol = sig[sig.contrast.str.contains("Hollbacker")].set_index("variable").zscore
common = ota.index.intersection(hol.index)
sign_agree = (np.sign(ota[common]) == np.sign(hol[common])).mean()
hol_overlap = {"n_common_genes": int(len(common)),
               "sign_agreement": round(float(sign_agree),3),
               "zscore_pearson": round(float(np.corrcoef(ota[common], hol[common])[0,1]),3)}

# ---------- A8 DIFF vs published atlas ----------
atlas = pd.read_csv(f"{REPO}/metadata/suppl_tables/polarization_prediction_condition_comparison_regulator_coefficients.csv", index_col=0)
ota_atlas = atlas[atlas.signature == "ota"][["regulator","celltype","coef_mean","coef_rank","known_regulators"]]
m = m.merge(ota_atlas.rename(columns={"regulator":"gene","celltype":"condition",
            "coef_mean":"atlas_coef","coef_rank":"atlas_rank","known_regulators":"atlas_known"}),
            on=["gene","condition"], how="left")
def atlas_class(r):
    if pd.isna(r.atlas_rank): return "not_in_atlas"
    if r.atlas_rank >= 0.9: return "concordant"
    if r.atlas_rank < 0.5: return "novel_selective"
    return "moderate"
m["atlas_class"] = m.apply(atlas_class, axis=1)

# ---------- COMPOSE hardened shortlist (the 172) ----------
sh = m[m.selective].copy()
sh["stageA_score"] = (sh.hardened_pass.astype(int)*2 + (sh.donor_evidence=="robust").astype(int)
                      + sh.stability_score - sh.th2_z/10)  # higher = better
sh = sh.sort_values("stageA_score", ascending=False)
cols = ["gene","condition","th2_z","th1_z","hardened_pass","pass_kd","not_essential","no_offtarget",
        "well_powered","donor_evidence","stability_score","atlas_class","atlas_rank","stageA_score"]
sh[cols].to_csv(f"{SL}/hardened_shortlist.csv", index=False)
m.to_parquet(f"{T}/arms_hardened.parquet")

# ---------- SUMMARY ----------
print("="*70, "\nSTAGE A SUMMARY  (172 selective hits, 161 genes)")
print("-"*70)
print("A3 QC gates (of 172 selective rows):")
for c in ["pass_kd","not_essential","no_offtarget","well_powered","hardened_pass"]:
    print(f"    {c:14s}: {int(sh[c].sum()):3d}/172 pass")
print(f"\nA4 donor evidence: {sh.donor_evidence.value_counts().to_dict()}")
print(f"\nA5 threshold sweep (N selective at each cutoff):")
print(pd.DataFrame(sweep_rows).to_string(index=False))
print(f"    median stability of the 172: {sh.stability_score.median():.2f}")
print(f"\nA6 recall@k of 12 known Th2 regs: {recall}")
print(f"    GATA3 gene_rank={int(gene_rank['GATA3'])}, STAT6={int(gene_rank['STAT6'])} (of {n_genes})")
print(f"    neg-control: known Th1 regs median percentile = {th1_ctrl_median_pct:.0f}% (want high/mid, not top)")
print(f"\nA7 Ota vs Hollbacher signature: {hol_overlap}")
print(f"\nA8 atlas class of the 172: {sh.atlas_class.value_counts().to_dict()}")
print("-"*70)
print("HARDENED (pass all QC gates):", int(sh.hardened_pass.sum()), "of 172")
print("HARDENED + novel_selective + robust/weak donor:",
      int(((sh.hardened_pass) & (sh.atlas_class=='novel_selective') & (sh.donor_evidence!='untested')).sum()))
print("\nTop 15 hardened, novel-selective hits:")
top = sh[(sh.hardened_pass) & (sh.atlas_class.isin(['novel_selective','moderate','not_in_atlas']))].head(15)
print(top[["gene","condition","th2_z","th1_z","donor_evidence","stability_score","atlas_class"]].to_string(index=False))
print("\nsaved -> results/shortlist/hardened_shortlist.csv")
