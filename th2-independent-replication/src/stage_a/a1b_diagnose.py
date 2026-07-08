"""A1b — is the arm array MIS-ALIGNED to suppl_table order, or is GATA3 just weak under the arm metric?
Decisive test: are the 12 known Th2 regulators enriched near the top of th2_z? If random -> misaligned."""
import numpy as np, pandas as pd, yaml

REPO = "/Users/shiventripathi/dev/GWT_perturbseq_analysis_2025"
T = "/Users/shiventripathi/dev/science/th2_suppressor_hardening/results/tables"

de = pd.read_parquet(f"{T}/de_stats_with_arms.parquet")
known = yaml.safe_load(open(f"{REPO}/metadata/th1_th2_known_regulators.yaml"))
th2_known, th1_known = known["th2"], known["th1"]

# per-gene best (most negative) th2_z and its percentile (0=top/most suppressive)
g = de.groupby("target_contrast_gene_name").agg(best_th2_z=("th2_arm_z", "min")).reset_index()
g["pct"] = g.best_th2_z.rank(pct=True) * 100  # low pct = strong suppressor

print("[1] Top-25 genes by strongest th2_arm suppression (my suppl_table ordering):")
top = g.sort_values("best_th2_z").head(25)
print("   ", ", ".join(f"{r.target_contrast_gene_name}({r.best_th2_z:.1f})" for _, r in top.iterrows()))

print("\n[2] Where do the 12 KNOWN Th2 regulators land? (low pct = near top = good alignment)")
kn = g[g.target_contrast_gene_name.isin(th2_known)].sort_values("pct")
print(kn.to_string(index=False))
print(f"   median percentile of known Th2 regs: {kn.pct.median():.1f}%  (random=50%, aligned<<50%)")
print(f"   how many known Th2 regs in top 5%%: {(kn.pct<=5).sum()}/{len(kn)}")

print("\n[3] Known Th1 regs th2_z (should NOT be strongly negative):")
kt1 = g[g.target_contrast_gene_name.isin([x.replace('IKFZ1','IKZF1') for x in th1_known])]
print("   median pct of known Th1 regs:", f"{kt1.pct.median():.1f}%")

print("\n[4] GATA3 on-target knockdown quality in this screen:")
gata = de[de.target_contrast_gene_name == "GATA3"][
    ["culture_condition", "ontarget_significant", "ontarget_effect_size",
     "target_baseMean", "n_cells_target", "n_total_de_genes"]]
print(gata.to_string(index=False))

print("\n[5] GATA3 in the PAPER's published atlas (elastic-net model, signature=ota):")
atlas = pd.read_csv(f"{REPO}/metadata/suppl_tables/polarization_prediction_condition_comparison_regulator_coefficients.csv", index_col=0)
gz = atlas[(atlas.regulator == "GATA3") & (atlas.signature == "ota")][
    ["celltype", "coef_mean", "coef_rank", "known_regulators"]]
print(gz.to_string(index=False))
print("   -> if GATA3 coef_rank ~1.0 here but ~0.79 under my arm metric, 'GATA3 is #1' referred to the PAPER model.")
