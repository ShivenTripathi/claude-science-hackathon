"""A1d — recover the remote h5ad obs order via HTTPS byte-range reads (stdlib only), align arms, retest GATA3."""
import numpy as np, pandas as pd, urllib.request, yaml, io

URL = "https://genome-scale-tcell-perturb-seq.s3.amazonaws.com/marson2025_data/GWCD4i.DE_stats.h5ad"
HAL = "/Users/shiventripathi/dev/science/th2_suppressor_hardening/data/haltavey"
REPO = "/Users/shiventripathi/dev/GWT_perturbseq_analysis_2025"
OUT = "/Users/shiventripathi/dev/science/th2_suppressor_hardening/results/tables"

class HTTPRangeFile(io.RawIOBase):
    def __init__(self, url):
        self.url = url
        r = urllib.request.urlopen(urllib.request.Request(url, method="HEAD"))
        self.size = int(r.headers["Content-Length"]); self.pos = 0
        self.n_reqs = 0; self.n_bytes = 0
    def seek(self, off, whence=0):
        self.pos = off if whence==0 else self.pos+off if whence==1 else self.size+off
        return self.pos
    def tell(self): return self.pos
    def readable(self): return True
    def seekable(self): return True
    def readinto(self, b):
        n = len(b)
        end = min(self.pos+n-1, self.size-1)
        if self.pos > end: return 0
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={self.pos}-{end}"})
        data = urllib.request.urlopen(req).read()
        self.n_reqs += 1; self.n_bytes += len(data)
        b[:len(data)] = data; self.pos += len(data)
        return len(data)

import h5py
f = HTTPRangeFile(URL)
print(f"remote size = {f.size/1e9:.2f} GB")
h5 = h5py.File(f, "r")
obs = h5["obs"]
idx_name = obs.attrs.get("_index", "_index")
if isinstance(idx_name, bytes): idx_name = idx_name.decode()

def read_col(grp, name):
    d = grp[name]
    if isinstance(d, h5py.Group) and "categories" in d:
        cats = np.array([x.decode() if isinstance(x, bytes) else x for x in d["categories"][:]])
        return cats[d["codes"][:]]
    v = d[:]
    return np.array([x.decode() if isinstance(x, bytes) else x for x in v])

idx = read_col(obs, idx_name)
gene = read_col(obs, "target_contrast_gene_name") if "target_contrast_gene_name" in obs else None
cond = read_col(obs, "culture_condition") if "culture_condition" in obs else None
h5.close()
print(f"read obs in {f.n_reqs} range requests, {f.n_bytes/1e6:.1f} MB transferred (NOT 15.6GB)")
print("n obs:", len(idx), "| first 3 index:", list(idx[:3]))

order = pd.DataFrame({"obs_index": idx})
if gene is not None: order["gene"] = gene
if cond is not None: order["condition"] = cond
order.to_parquet(f"{OUT}/remote_obs_order.parquet")

th2 = np.load(f"{HAL}/th2_arm.npy"); th1 = np.load(f"{HAL}/th1_arm.npy")
assert len(order) == len(th2)
order["th2_z"] = (th2 - th2.mean())/th2.std()
order["th1_z"] = (th1 - th1.mean())/th1.std()

if gene is not None:
    th2_known = yaml.safe_load(open(f"{REPO}/metadata/th1_th2_known_regulators.yaml"))["th2"]
    pct = order.groupby("gene").th2_z.min().rank(pct=True)*100
    kn = pct[pct.index.isin(th2_known)].sort_values()
    print("\n=== GATA3 GUARDRAIL, RE-TESTED IN REMOTE OBS ORDER ===")
    print(kn.to_string())
    print(f"median pct known Th2 regs: {kn.median():.1f}%  (ALIGNED if << 50%)")
    print(f"GATA3 percentile: {pct.get('GATA3', float('nan')):.2f}%   (want ~top few %)")
    print(f"known Th2 regs in top 5%: {(kn<=5).sum()}/{len(kn)}")
