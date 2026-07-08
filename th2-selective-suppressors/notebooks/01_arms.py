"""
Phase 1: Reconstruct Th2/Th1 arm scores per perturbation x condition from DE_stats.h5ad
and the Ota-2021 Th2-vs-Th1 signature. Reproduce the ~172 / ~4 / +0.49 checkpoint.

Run: python notebooks/01_arms.py
Outputs: outputs/arms.parquet, outputs/arm_gene_sets.json, prints checkpoint stats.
"""
import json, sys, h5py, numpy as np, pandas as pd, yaml
from pathlib import Path
from contextlib import contextmanager

ROOT = Path("/Users/shiventripathi/dev/science/th2_selective")
DATA = ROOT / "data"; OUT = ROOT / "outputs"; OUT.mkdir(exist_ok=True)
H5 = DATA / "GWCD4i.DE_stats.h5ad"
URL = "https://genome-scale-tcell-perturb-seq.s3.amazonaws.com/marson2025_data/GWCD4i.DE_stats.h5ad"

@contextmanager
def open_h5():
    """Open the DE_stats h5ad locally if present, else stream via HTTP range reads."""
    if H5.exists() and H5.stat().st_size > 16e9:
        with h5py.File(H5, "r") as f:
            yield f
    else:
        import fsspec
        print("[h5ad] streaming remotely via fsspec (reads only needed datasets)")
        fo = fsspec.filesystem("https").open(URL, block_size=16*2**20)
        with h5py.File(fo, "r") as f:
            yield f

# ---- arm gene sets from Ota signature (positive z = Th2-program, negative = Th1-program) ----
ADJP = 0.05; LFC = 0.5   # signature membership thresholds (tunable to reproduce teammate counts)
ota = pd.read_csv(DATA / "Ota_Th2vsTh1_DE_results.csv")
th2_set = set(ota.loc[(ota.adj_p_value < ADJP) & (ota.log_fc >  LFC), "variable"])
th1_set = set(ota.loc[(ota.adj_p_value < ADJP) & (ota.log_fc < -LFC), "variable"])
print(f"[arms] Th2-arm genes={len(th2_set)}  Th1-arm genes={len(th1_set)}  (adj_p<{ADJP}, |lfc|>{LFC})")

# ---- introspect h5ad structure ----
def h5_str_array(node):
    """Read an anndata string-index/categorical column from an open h5py node."""
    if isinstance(node, h5py.Dataset):
        v = node[:]
        return np.array([x.decode() if isinstance(x, bytes) else x for x in v])
    # categorical group: categories + codes
    cats = node["categories"][:]; codes = node["codes"][:]
    cats = np.array([c.decode() if isinstance(c, bytes) else c for c in cats])
    return cats[codes]

with open_h5() as f:
    print("[h5ad] top-level keys:", list(f.keys()))
    print("[h5ad] layers:", list(f["layers"].keys()) if "layers" in f else "NONE")
    print("[h5ad] obs keys:", list(f["obs"].keys()))
    print("[h5ad] var keys:", list(f["var"].keys()))
    # gene names (var)
    var_grp = f["var"]
    gene_col = "gene_name" if "gene_name" in var_grp else "_index"
    genes = h5_str_array(var_grp[gene_col])
    n_var = len(genes)
    # obs: index + condition + target gene name
    obs_grp = f["obs"]
    _idx_key = "index" if "index" in obs_grp else "_index"
    obs_index = h5_str_array(obs_grp[_idx_key])
    cond = h5_str_array(obs_grp["culture_condition"]) if "culture_condition" in obs_grp else None
    tgt_col = next((c for c in ["target_contrast_gene_name","perturbed_gene_name","gene_name"] if c in obs_grp), None)
    tgt = h5_str_array(obs_grp[tgt_col]) if tgt_col else None
    n_obs = len(obs_index)
    print(f"[h5ad] n_obs={n_obs} n_var={n_var}  target_col={tgt_col}")

    # choose perturbation metric layer
    layer_name = "zscore" if ("layers" in f and "zscore" in f["layers"]) else None
    assert layer_name, "expected 'zscore' layer"
    # gene column masks
    g2i = {g: i for i, g in enumerate(genes)}
    th2_idx = np.array(sorted(g2i[g] for g in th2_set if g in g2i))
    th1_idx = np.array(sorted(g2i[g] for g in th1_set if g in g2i))
    print(f"[arms] measured overlap: Th2={len(th2_idx)}/{len(th2_set)}  Th1={len(th1_idx)}/{len(th1_set)}")

    dset = f["layers"][layer_name]
    shape, dtype = dset.shape, dset.dtype
    chunks, comp = dset.chunks, dset.compression
    offset = dset.id.get_offset()  # byte offset if contiguous & uncompressed, else None
    print(f"[h5ad] {layer_name} shape={shape} dtype={dtype} chunks={chunks} comp={comp} offset={offset}")
    if offset is None:
        # fallback: h5py block reads (handles chunk/compression) — slower
        print("[read] non-contiguous -> h5py block reads")
        raw_th2 = np.empty(shape[0]); raw_th1 = np.empty(shape[0]); B = 2000
        for i in range(0, shape[0], B):
            Zb = np.nan_to_num(np.asarray(dset[i:i+B, :], np.float64))
            raw_th2[i:i+Zb.shape[0]] = Zb[:, th2_idx].mean(1)
            raw_th1[i:i+Zb.shape[0]] = Zb[:, th1_idx].mean(1)
        offset = "handled"

if offset != "handled":
    # fast path: parallel HTTP range reads of the contiguous float64 matrix
    import requests
    from concurrent.futures import ThreadPoolExecutor
    ncol = shape[1]; isz = dtype.itemsize; B = 2000
    raw_th2 = np.empty(shape[0]); raw_th1 = np.empty(shape[0])
    def fetch(i0):
        i1 = min(i0 + B, shape[0])
        b0 = offset + i0*ncol*isz; b1 = offset + i1*ncol*isz
        for attempt in range(4):
            try:
                r = requests.get(URL, headers={"Range": f"bytes={b0}-{b1-1}"}, timeout=180)
                r.raise_for_status(); break
            except Exception as e:
                if attempt == 3: raise
        arr = np.frombuffer(r.content, dtype=dtype).reshape(i1-i0, ncol)
        arr = np.nan_to_num(np.asarray(arr, np.float64))
        return i0, arr[:, th2_idx].mean(1), arr[:, th1_idx].mean(1)
    starts = list(range(0, shape[0], B))
    print(f"[read] parallel range reads: {len(starts)} blocks x {B} rows (~2.8GB, 12 workers)")
    with ThreadPoolExecutor(max_workers=12) as ex:
        for k,(i0,a2,a1) in enumerate(ex.map(fetch, starts)):
            raw_th2[i0:i0+len(a2)] = a2; raw_th1[i0:i0+len(a1)] = a1
            if k % 3 == 0: print(f"  block {k+1}/{len(starts)}", flush=True)

def zsc(x):
    x = np.asarray(x, float); return (x - x.mean()) / x.std()

th2_arm = zsc(raw_th2)   # negative = Th2 suppressed
th1_arm = zsc(raw_th1)   # positive = Th1 induced

arms = pd.DataFrame({
    "obs_index": obs_index, "target_gene": tgt, "culture_condition": cond,
    "th2_arm_raw": raw_th2, "th1_arm_raw": raw_th1,
    "th2_arm": th2_arm, "th1_arm": th1_arm,
})

# ---- gates + checkpoint ----
TX, TY = -2.0, 1.0
selective = (arms.th2_arm < TX) & (arms.th1_arm.abs() < TY)
skewer = (arms.th2_arm < TX) & (arms.th1_arm > TY)
corr = np.corrcoef(arms.th2_arm, arms.th1_arm)[0, 1]
print(f"\n[CHECKPOINT] arm corr = {corr:+.3f}   (target ~ +0.49)")
print(f"[CHECKPOINT] selective (th2<{TX}, |th1|<{TY}) = {int(selective.sum())}   (target ~172)")
print(f"[CHECKPOINT] skewer    (th2<{TX}, th1>{TY})  = {int(skewer.sum())}   (target ~4)")

arms["is_selective"] = selective; arms["is_skewer"] = skewer
# top selective by depth of Th2 suppression
top = arms[selective].sort_values("th2_arm").head(15)
print("\n[top selective by Th2 suppression]")
print(top[["target_gene","culture_condition","th2_arm","th1_arm"]].to_string(index=False))
print("\nGATA3 rows:")
print(arms[arms.target_gene=="GATA3"][["culture_condition","th2_arm","th1_arm","is_selective"]].to_string(index=False))

arms.to_parquet(OUT / "arms.parquet")
json.dump({"th2_genes": sorted(th2_set), "th1_genes": sorted(th1_set),
           "adjp": ADJP, "lfc": LFC, "gate": [TX, TY]}, open(OUT/"arm_gene_sets.json","w"))
print(f"\n[done] wrote {OUT/'arms.parquet'} ({len(arms)} rows)")
