"""A1c — read ONLY the obs index of the remote 15.6GB h5ad over S3 byte-ranges (no full download),
to recover Haltavey's true row order and re-test the GATA3 guardrail."""
import numpy as np, pandas as pd, sys

BUCKET = "genome-scale-tcell-perturb-seq"
KEY = "marson2025_data/GWCD4i.DE_stats.h5ad"
HAL = "/Users/shiventripathi/dev/science/th2_suppressor_hardening/data/haltavey"
REPO = "/Users/shiventripathi/dev/GWT_perturbseq_analysis_2025"

# check backends
try:
    import s3fs, h5py
except Exception as e:
    print("MISSING backend:", e); print("packages:")
    import importlib
    for p in ["s3fs", "fsspec", "h5py", "aiobotocore"]:
        try: importlib.import_module(p); print("  have", p)
        except Exception: print("  NO", p)
    sys.exit(1)

fs = s3fs.S3FileSystem(anon=True)
print("opening remote h5ad (lazy)...")
with fs.open(f"{BUCKET}/{KEY}", "rb") as fo:
    h5 = h5py.File(fo, "r")
    obs = h5["obs"]
    print("obs keys:", list(obs.keys())[:20])
    idx_name = obs.attrs.get("_index", "_index")
    if isinstance(idx_name, bytes): idx_name = idx_name.decode()
    print("index dataset name:", idx_name)
    idx = obs[idx_name][:]
    idx = np.array([x.decode() if isinstance(x, bytes) else x for x in idx])
    print("n obs:", len(idx), "| first 5:", list(idx[:5]))
    # also try to grab a gene-name column if present
    cols = {}
    for c in ["target_contrast_gene_name", "culture_condition", "target_contrast"]:
        if c in obs:
            d = obs[c]
            # categorical stored as group with 'codes'+'categories'
            if isinstance(d, h5py.Group) and "categories" in d:
                cats = np.array([x.decode() if isinstance(x, bytes) else x for x in d["categories"][:]])
                cols[c] = cats[d["codes"][:]]
            else:
                v = d[:]
                cols[c] = np.array([x.decode() if isinstance(x, bytes) else x for x in v])
    h5.close()

obs_df = pd.DataFrame({"obs_index": idx})
for c, v in cols.items(): obs_df[c] = v
print("recovered obs columns:", list(obs_df.columns))
obs_df.to_parquet("/Users/shiventripathi/dev/science/th2_suppressor_hardening/results/tables/remote_obs_order.parquet")

# align Haltavey's arms to THIS order and retest GATA3
th2 = np.load(f"{HAL}/th2_arm.npy"); th1 = np.load(f"{HAL}/th1_arm.npy")
assert len(obs_df) == len(th2), f"len mismatch {len(obs_df)} vs {len(th2)}"
obs_df["th2_z"] = (th2 - th2.mean())/th2.std()
obs_df["th1_z"] = (th1 - th1.mean())/th1.std()

gene_col = "target_contrast_gene_name" if "target_contrast_gene_name" in obs_df else None
if gene_col:
    g = obs_df.groupby(gene_col).th2_z.min().rank(pct=True)*100
    import yaml
    th2_known = yaml.safe_load(open(f"{REPO}/metadata/th1_th2_known_regulators.yaml"))["th2"]
    print("\n=== RE-TEST after remote-order alignment ===")
    kn = g[g.index.isin(th2_known)].sort_values()
    print(kn.to_string())
    print(f"median pct of known Th2 regs: {kn.median():.1f}%  (aligned -> should be LOW)")
    print(f"GATA3 percentile: {g.get('GATA3', float('nan')):.2f}%")
else:
    print("\nNo gene-name column in remote obs; index only. Will map via obs_index parse.")
