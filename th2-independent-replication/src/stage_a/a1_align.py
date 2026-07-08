"""A1 — attach arms to DE_stats, GATA3 guardrail, find the rule that reproduces 172."""
import numpy as np, pandas as pd

REPO = "/Users/shiventripathi/dev/GWT_perturbseq_analysis_2025"
HAL = "/Users/shiventripathi/dev/science/th2_suppressor_hardening/data/haltavey"
OUT = "/Users/shiventripathi/dev/science/th2_suppressor_hardening/results"

de = pd.read_csv(f"{REPO}/metadata/suppl_tables/DE_stats.suppl_table.csv", index_col=0)
de["th2_arm_raw"] = np.load(f"{HAL}/th2_arm.npy")
de["th1_arm_raw"] = np.load(f"{HAL}/th1_arm.npy")

# standardize each arm across all perturbation x condition rows (plot axis is "(z)")
for a in ["th2_arm", "th1_arm"]:
    r = de[f"{a}_raw"]
    de[f"{a}_z"] = (r - r.mean()) / r.std()

def diag(gene):
    g = de[de.target_contrast_gene_name == gene]
    for _, row in g.iterrows():
        print(f"    {gene:8s} {row.culture_condition:9s} "
              f"th2_raw={row.th2_arm_raw:+.3f} th2_z={row.th2_arm_z:+.2f} | "
              f"th1_raw={row.th1_arm_raw:+.3f} th1_z={row.th1_arm_z:+.2f}")

print("[GATA3] (master Th2 reg — must be strongly NEGATIVE th2, flat th1):")
diag("GATA3")
print("[A1BG] (no on-target KD — must be ~0 on both):")
diag("A1BG")
print("[STAT6, IL4R] (other known Th2 regs):")
diag("STAT6"); diag("IL4R")

# rank of GATA3 by th2_arm (most suppressive first)
de["th2_rank"] = de.th2_arm_z.rank(method="min")  # 1 = most negative
gata3_best = de[de.target_contrast_gene_name == "GATA3"].th2_rank.min()
print(f"\nGATA3 best th2_arm rank = {int(gata3_best)} / {len(de)} "
      f"(top {100*gata3_best/len(de):.2f}%)")

print("\n=== reproduce the 172 : try thresholds ===")
for th2_thr, th1_flat, unit in [(-2, 1, "z"), (-2.5, 1, "z"), (-1.5, 1, "z"),
                                 (-2, 1.5, "z"), (-2, 1, "raw")]:
    t2 = de.th2_arm_z if unit == "z" else de.th2_arm_raw
    t1 = de.th1_arm_z if unit == "z" else de.th1_arm_raw
    sel = (t2 <= th2_thr) & (t1.abs() <= th1_flat)
    ngenes = de.loc[sel, "target_contrast_gene_name"].nunique()
    skew = (t2 <= th2_thr) & (t1 > th1_flat)  # Th1-skewers
    print(f"  th2{unit}<={th2_thr}, |th1{unit}|<={th1_flat}:  "
          f"rows={sel.sum():4d}  unique_genes={ngenes:4d}  skewers={skew.sum():3d}")

de.to_parquet(f"{OUT}/tables/de_stats_with_arms.parquet")
print(f"\nsaved -> results/tables/de_stats_with_arms.parquet  ({de.shape})")
