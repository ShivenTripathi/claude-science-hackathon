"""Independent QC audit: pull the RICHER h5ad obs QC columns (not in the suppl table) and
check them against our high-confidence set. Also test robustness of counts to thresholds
and to using the combined (Ota+Hollbacher+Diff043) signature instead of Ota alone.
"""
import h5py, numpy as np, pandas as pd, fsspec
from pathlib import Path
ROOT = Path("/Users/shiventripathi/dev/science/th2_selective"); DATA, OUT = ROOT/"data", ROOT/"outputs"
URL = "https://genome-scale-tcell-perturb-seq.s3.amazonaws.com/marson2025_data/GWCD4i.DE_stats.h5ad"

def sarr(node):
    if isinstance(node, h5py.Dataset):
        v=node[:]; return np.array([x.decode() if isinstance(x,bytes) else x for x in v])
    cats=node["categories"][:]; codes=node["codes"][:]
    cats=np.array([c.decode() if isinstance(c,bytes) else c for c in cats]); return cats[codes]

fo = fsspec.filesystem("https").open(URL, block_size=8*2**20)
with h5py.File(fo,"r") as f:
    obs=f["obs"]; cols={}
    want=["index","culture_condition","target_contrast_gene_name","neighboring_gene_KD","low_target_gex",
          "distal_offtarget_flag","single_guide_estimate","guide_n_signif_ontarget","n_guides",
          "donor_correlation_all_mean","donor_correlation_all_min","donor_correlation_hits_mean",
          "guide_correlation_all","guide_correlation_signif","ontarget_significant","ontarget_effect_size",
          "n_total_de_genes"]
    for k in want:
        if k in obs:
            try: cols[k]=sarr(obs[k])
            except Exception as e: print("skip",k,e)
o = pd.DataFrame(cols).rename(columns={"target_contrast_gene_name":"target_gene","index":"obs_index"})
for b in ["neighboring_gene_KD","low_target_gex","distal_offtarget_flag","single_guide_estimate"]:
    if b in o: o[b] = o[b].isin([True,1,"True","true"])
for nc in ["donor_correlation_all_mean","donor_correlation_hits_mean","guide_correlation_signif","guide_n_signif_ontarget","n_guides"]:
    if nc in o: o[nc] = pd.to_numeric(o[nc], errors="coerce")
o.to_parquet(OUT/"obs_qc.parquet")
print("[obs] rows", len(o), "cols", list(o.columns), "-> saved obs_qc.parquet")

short = pd.read_csv(OUT/"real_vs_fp_shortlist.csv")
hc = set(short.target_gene)
sub = o[o.target_gene.isin(hc)].copy()

print("\n=== richer QC flags on high-confidence genes (best row per gene) ===")
for c in ["neighboring_gene_KD","low_target_gex","distal_offtarget_flag","single_guide_estimate"]:
    if c in sub:
        vc = sub.groupby("target_gene")[c].max(numeric_only=False)
        flagged = [g for g,v in vc.items() if v in (True,1,"True")]
        print(f"  {c:24s}: flagged genes = {flagged}")

print("\n=== donor coverage: all_mean vs suppl crossdonor (NaN rate on HC) ===")
for c in ["donor_correlation_all_mean","donor_correlation_hits_mean"]:
    if c in sub:
        v=pd.to_numeric(sub[c],errors="coerce")
        print(f"  {c:28s} NaN%={v.isna().mean():.2f}  median={v.median():.2f}")

# per-gene table for review
det = (o[o.target_gene.isin(hc)]
       .assign(**{k:pd.to_numeric(o[k],errors='coerce') for k in ['donor_correlation_all_mean','guide_n_signif_ontarget','n_guides','n_total_de_genes'] if k in o})
       .sort_values('target_gene'))
keep=[c for c in ["target_gene","culture_condition","neighboring_gene_KD","low_target_gex","distal_offtarget_flag",
      "single_guide_estimate","guide_n_signif_ontarget","n_guides","donor_correlation_all_mean","n_total_de_genes"] if c in det]
det[keep].to_csv(OUT/"qc_audit_highconf.csv", index=False)
print("\n[wrote] outputs/qc_audit_highconf.csv")

# threshold robustness of selective count
arms = pd.read_parquet(OUT/"arms.parquet")
print("\n=== selective-count robustness to gate thresholds ===")
for tx in [-1.5,-2.0,-2.5]:
    row=[]
    for ty in [0.5,1.0,1.5]:
        n=int(((arms.th2_arm<tx)&(arms.th1_arm.abs()<ty)).sum()); row.append(f"|th1|<{ty}:{n}")
    print(f"  th2<{tx}: "+"  ".join(row))
