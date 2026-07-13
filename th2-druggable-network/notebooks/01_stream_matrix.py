"""
01_stream_matrix.py — streaming primitive: fetch specific rows of the 16.8 GB DE matrix by
HTTP byte-range, no full download.

The public-S3 GWCD4i.DE_stats.h5ad zscore layer is a contiguous dense float64 array
(33,983 perturbations x 10,282 genes). Row i lives at data_offset + i*row_bytes, so any row
is one ~82 KB range request. open_structure() returns obs/var/offset/row_bytes; fetch_rows()
pulls an arbitrary set of rows in parallel.
"""
import numpy as np, h5py, fsspec, requests, os, time
from concurrent.futures import ThreadPoolExecutor
URL = "https://genome-scale-tcell-perturb-seq.s3.amazonaws.com/marson2025_data/GWCD4i.DE_stats.h5ad"

def open_structure(url=URL):
    fs = fsspec.filesystem("https", client_kwargs={"trust_env": True})
    with fs.open(url, "rb") as fh, h5py.File(fh, "r") as f:
        obs = f["obs"]["_index"][:].astype(str) if "_index" in f["obs"] else f["obs"]["index"][:].astype(str)
        var = f["var"]["gene_name"][:].astype(str)
        ds = f["layers"]["zscore"]
        off = ds.id.get_offset(); row_bytes = ds.shape[1] * 8
    return obs, var, off, row_bytes

def _one(args):
    url, i, off, rb, sess, tries = args
    lo = off + i * rb
    for a in range(tries):
        try:
            r = sess.get(url, headers={"Range": f"bytes={lo}-{lo+rb-1}"}, timeout=60)
            r.raise_for_status()
            return i, np.frombuffer(r.content, dtype="<f8")
        except Exception:
            if a == tries - 1:
                raise
            time.sleep(1.5 * (a + 1))  # backoff on transient proxy/connection drops

def fetch_rows(rows, off, row_bytes, url=URL, workers=12, tries=4):
    """rows: iterable of int matrix-row indices. Returns dict{row_index: 1D float64 array}.
    Modest concurrency + retry/backoff to tolerate transient proxy/connection drops."""
    rows = sorted(set(int(r) for r in rows))
    sess = requests.Session()
    out = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        for i, v in ex.map(_one, [(url, i, off, row_bytes, sess, tries) for i in rows]):
            out[i] = v
    return out

if __name__ == "__main__":
    obs, var, off, rb = open_structure()
    print(f"obs={len(obs)} var={len(var)} row_bytes={rb}")
    demo = fetch_rows([0, 1, 2], off, rb)
    print("fetched demo rows:", {k: v.shape for k, v in demo.items()})
