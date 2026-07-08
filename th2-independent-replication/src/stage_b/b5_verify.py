"""B5 — INDEPENDENT verification of the hardened negative result:
 (T3) GATA3 under a MATCHED Th1-vs-Th0 arm -> Th1-skewer?
 (T1) competitive (per-perturbation-standardized) scoring collapses the arm correlation?
 (T2) permutation null -> is the selective set enriched over random gene sets?"""
import sys; sys.path.insert(0, "/Users/shiventripathi/dev/science/th2_suppressor_hardening/src")
from common.remote_h5 import open_remote
import numpy as np, pandas as pd, yaml
rng = np.random.default_rng(0)
REPO = "/Users/shiventripathi/dev/GWT_perturbseq_analysis_2025"
T = "/Users/shiventripathi/dev/science/th2_suppressor_hardening/results/tables"

m = pd.read_parquet(f"{T}/arms_aligned.parquet").reset_index(drop=True)   # row i == obs row i
known = yaml.safe_load(open(f"{REPO}/metadata/th1_th2_known_regulators.yaml"))
th2_known, th1_known = set(known["th2"]), {x.replace("IKFZ1","IKZF1") for x in known["th1"]}

h5, f = open_remote()
def readcol(g, n):
    d = g[n]
    if hasattr(d, "keys") and "categories" in d:
        c = np.array([x.decode() if isinstance(x, bytes) else x for x in d["categories"][:]]); return c[d["codes"][:]]
    return np.array([x.decode() if isinstance(x, bytes) else x for x in d[:]])
genes = readcol(h5["var"], "gene_name"); gidx = {g:i for i,g in enumerate(genes)}
Z = h5["layers"]["zscore"]

# ---- signatures ----
def sig_up(path, contrast=None, thr=2.0):
    df = pd.read_csv(path)
    if contrast: df = df[df.contrast.str.contains(contrast, case=False)]
    gcol = "variable" if "variable" in df else df.columns[0]
    zc = "zscore" if "zscore" in df else None
    if zc is None: df["zscore"] = df["log_fc"]/df["lfcSE"]; zc="zscore"
    s = df.groupby(gcol)[zc].mean()
    up = [g for g in s[s>thr].index if g in gidx]
    dn = [g for g in s[s<-thr].index if g in gidx]
    return up, dn
ota = pd.read_csv(f"{REPO}/metadata/suppl_tables/Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv")
ota = ota[ota.contrast.str.contains("Ota")].groupby("variable").zscore.mean()
ota_th2 = [g for g in ota[ota>0].index if g in gidx]; ota_th1 = [g for g in ota[ota<0].index if g in gidx]
th2vth0_up,_ = sig_up(f"{REPO}/src/4_polarization_signatures/results/Th2_vs_Th0_DE_results.csv")
th1vth0_up,_ = sig_up(f"{REPO}/src/4_polarization_signatures/results/Th1_vs_Th0_DE_results.csv")
print(f"arm sizes: Ota-Th2={len(ota_th2)} Ota-Th1={len(ota_th1)} | Th2vTh0up={len(th2vth0_up)} Th1vTh0up={len(th1vth0_up)}")
C = {k:[gidx[g] for g in v] for k,v in dict(ota_th2=ota_th2, ota_th1=ota_th1, th2vth0=th2vth0_up, th1vth0=th1vth0_up).items()}

# ---- rows to read: selective + known regs + random sample ----
sel_pos = m.index[m.selective].tolist()
reg_pos = m.index[m.gene.isin(th2_known|th1_known)].tolist()
rand_pos = rng.choice(m.index, size=1100, replace=False).tolist()
need = sorted(set(sel_pos)|set(reg_pos)|set(rand_pos))
print(f"streaming {len(need)} rows ...")
Zr = {}
for j,p in enumerate(need):
    Zr[p] = Z[p,:]
    if (j+1)%300==0: print(f"  {j+1}/{len(need)} ({f.n_bytes/1e6:.0f}MB)")
h5.close(); print(f"read {f.n_bytes/1e6:.0f}MB in {f.n_reqs} reqs")

def arm(z, cols): return np.nanmean(z[cols])
def arm_comp(z, cols):  # competitive: standardize the perturbation's whole z-vector first
    zz=(z-np.nanmean(z))/np.nanstd(z); return np.nanmean(zz[cols])

# ===== T3: GATA3 (+ top hits + known regs) under MATCHED arms =====
print("\n===== T3: matched Th1-vs-Th0 arm (is GATA3 a Th1-skewer?) =====")
probe = ["GATA3","STAT6","RARA","AMBRA1","ARNT","RAB21","UBA6","TBX21","IL4"]
print(f"{'gene':8s} {'cond':9s} {'Th2vTh0':>8s} {'Th1vTh0':>8s}  verdict")
for g in probe:
    for p in m.index[m.gene==g]:
        z=Zr.get(p);
        if z is None: continue
        a2=arm(z,C['th2vth0']); a1=arm(z,C['th1vth0'])
        verdict = "Th1-SKEWER" if a1>1 and a2<0 else ("selective?" if a2<-1 and abs(a1)<1 else "")
        print(f"{g:8s} {m.loc[p,'condition']:9s} {a2:8.2f} {a1:8.2f}  {verdict}")

# ===== T1: competitive scoring collapses arm correlation =====
pos = list(Zr.keys())
naive2=np.array([arm(Zr[p],C['ota_th2']) for p in pos]); naive1=np.array([arm(Zr[p],C['ota_th1']) for p in pos])
comp2 =np.array([arm_comp(Zr[p],C['ota_th2']) for p in pos]); comp1=np.array([arm_comp(Zr[p],C['ota_th1']) for p in pos])
print(f"\n===== T1: arm correlation  naive(mean-of-z)={np.corrcoef(naive2,naive1)[0,1]:+.2f}  competitive={np.corrcoef(comp2,comp1)[0,1]:+.2f} =====")

# ===== T2: permutation null — is the selective set enriched over random gene sets? =====
def n_selective(a2col, a1col):
    z2=(a2col-a2col.mean())/a2col.std(); z1=(a1col-a1col.mean())/a1col.std()
    return int(((z2<=-2)&(np.abs(z1)<=1)).sum())
obs = n_selective(naive2, naive1)
null=[]
allcols=np.arange(len(genes))
for _ in range(200):
    r2=rng.choice(allcols,len(C['ota_th2']),replace=False); r1=rng.choice(allcols,len(C['ota_th1']),replace=False)
    a2=np.array([np.nanmean(Zr[p][r2]) for p in pos]); a1=np.array([np.nanmean(Zr[p][r1]) for p in pos])
    null.append(n_selective(a2,a1))
null=np.array(null)
print(f"===== T2: selective count observed={obs}  null(random gene sets) mean={null.mean():.0f} sd={null.std():.0f}  "
      f"emp_p={(null>=obs).mean():.2f}  enrichment={obs/max(null.mean(),1):.2f}x =====")
print("(enrichment ~1x and emp_p~1 => NOT enriched over chance => negative result confirmed)")
