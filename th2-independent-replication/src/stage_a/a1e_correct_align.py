"""A1e — CORRECT alignment: arms are in h5ad obs order. Join QC by (gene,condition). Reproduce 172."""
import numpy as np, pandas as pd, yaml

REPO = "/Users/shiventripathi/dev/GWT_perturbseq_analysis_2025"
HAL = "/Users/shiventripathi/dev/science/th2_suppressor_hardening/data/haltavey"
T = "/Users/shiventripathi/dev/science/th2_suppressor_hardening/results/tables"

# 1) arms aligned POSITIONALLY to remote OBS ORDER (the order Haltavey computed them in)
arms = pd.read_parquet(f"{T}/remote_obs_order.parquet").rename(columns={"gene": "gene", "condition": "condition"})
th2 = np.load(f"{HAL}/th2_arm.npy"); th1 = np.load(f"{HAL}/th1_arm.npy")
arms["th2_arm_raw"], arms["th1_arm_raw"] = th2, th1
arms["th2_z"] = (th2 - th2.mean())/th2.std()
arms["th1_z"] = (th1 - th1.mean())/th1.std()

# 2) join QC by (gene, condition) — robust to the symbol/Ensembl key inconsistency
de = pd.read_csv(f"{REPO}/metadata/suppl_tables/DE_stats.suppl_table.csv", index_col=0)
print(f"suppl_table order == obs order? {(de['index'].values==arms['obs_index'].values).mean():.1%} (confirms DIFFERENT orders)")
qc = de.rename(columns={"target_contrast_gene_name": "gene", "culture_condition": "condition"})[
    ["gene","condition","ontarget_significant","ontarget_effect_size","target_baseMean",
     "offtarget_flag","n_cells_target","n_total_de_genes","n_downstream",
     "crossdonor_correlation_mean","crossdonor_correlation_min","crossguide_correlation","ontarget_effect_category"]]
m = arms.merge(qc, on=["gene","condition"], how="left")
print("unmatched QC rows after (gene,condition) join:", m["ontarget_significant"].isna().sum(), "of", len(m))

# 3) recall of known Th2 regulators (correct labels)
th2_known = yaml.safe_load(open(f"{REPO}/metadata/th1_th2_known_regulators.yaml"))["th2"]
per_gene = m.groupby("gene").th2_z.min().sort_values()
rank = per_gene.rank(method="min")
print("\nTop-20 selective genes by th2_z (should be Th2/immune-plausible now):")
print("   ", ", ".join(f"{g}({v:.1f})" for g, v in per_gene.head(20).items()))
print(f"\nKnown Th2 regulator ranks (of {per_gene.nunique()} genes tested):")
for g in sorted(th2_known, key=lambda x: per_gene.get(x, 1e9)):
    if g in per_gene.index:
        print(f"    {g:8s} best th2_z={per_gene[g]:+.2f}  gene_rank={int(rank[g]):5d}  (top {100*rank[g]/per_gene.nunique():.1f}%)")

# 4) reproduce the 172 with CORRECT labels
sel = (m.th2_z <= -2) & (m.th1_z.abs() <= 1)
skew = (m.th2_z <= -2) & (m.th1_z > 1)
m["selective"] = sel
print(f"\n=== 172 reproduction (correct labels) ===")
print(f"selective rows={sel.sum()}  unique_genes={m.loc[sel,'gene'].nunique()}  skewers={skew.sum()}")
print(f"GATA3 in selective set? {'GATA3' in set(m.loc[sel,'gene'])}")
print("known Th2 regs that are selective:", sorted(set(m.loc[sel,'gene']) & set(th2_known)))
m.to_parquet(f"{T}/arms_aligned.parquet")
print(f"\nsaved -> results/tables/arms_aligned.parquet  {m.shape}")
