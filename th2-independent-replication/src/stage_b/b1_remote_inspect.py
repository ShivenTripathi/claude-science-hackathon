"""B1 — inspect the remote h5ad structure (layers, var, chunking) to plan coherence reads."""
import sys; sys.path.insert(0, "/Users/shiventripathi/dev/science/th2_suppressor_hardening/src")
from common.remote_h5 import open_remote
import numpy as np

h5, f = open_remote()
print("top-level keys:", list(h5.keys()))
print("\nlayers:", list(h5["layers"].keys()) if "layers" in h5 else "NONE")
for ln in (h5["layers"].keys() if "layers" in h5 else []):
    d = h5["layers"][ln]
    print(f"  layer {ln}: shape={d.shape} dtype={d.dtype} chunks={d.chunks} compression={d.compression}")
if "X" in h5:
    X = h5["X"]
    if hasattr(X, "shape"):
        print(f"\nX: shape={X.shape} dtype={X.dtype} chunks={getattr(X,'chunks',None)}")
    else:
        print("\nX is a group (sparse):", list(X.keys()))

# var (gene) names
var = h5["var"]
vidx = var.attrs.get("_index", "_index")
if isinstance(vidx, bytes): vidx = vidx.decode()
print("\nvar index name:", vidx, "| var keys:", list(var.keys())[:15])
def readcol(grp, name):
    d = grp[name]
    if hasattr(d, "keys") and "categories" in d:
        cats = np.array([x.decode() if isinstance(x, bytes) else x for x in d["categories"][:]])
        return cats[d["codes"][:]]
    return np.array([x.decode() if isinstance(x, bytes) else x for x in d[:]])
var_index = readcol(var, vidx)
gene_name = readcol(var, "gene_name") if "gene_name" in var else var_index
print("n_var:", len(var_index), "| first genes:", list(gene_name[:8]))
print("GATA3 in var gene_name?", "GATA3" in set(gene_name), "| STAT6?", "STAT6" in set(gene_name),
      "| IL4R?", "IL4R" in set(gene_name))
print(f"\nbytes transferred so far: {f.n_bytes/1e6:.1f} MB in {f.n_reqs} requests")
h5.close()
