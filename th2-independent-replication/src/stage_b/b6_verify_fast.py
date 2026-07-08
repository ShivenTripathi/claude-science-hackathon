"""B6 — fast unbuffered verification. T3 (GATA3 matched arm) first with minimal reads, then T1/T2 on a small sample."""
import sys; sys.path.insert(0, "/Users/shiventripathi/dev/science/th2_suppressor_hardening/src")
from common.remote_h5 import open_remote
import numpy as np, pandas as pd, yaml
def p(*a): print(*a, flush=True)
rng = np.random.default_rng(0)
REPO = "/Users/shiventripathi/dev/GWT_perturbseq_analysis_2025"
T = "/Users/shiventripathi/dev/science/th2_suppressor_hardening/results/tables"

m = pd.read_parquet(f"{T}/arms_aligned.parquet").reset_index(drop=True)
known = yaml.safe_load(open(f"{REPO}/metadata/th1_th2_known_regulators.yaml"))
th2_known = set(known["th2"]); th1_known = {x.replace("IKFZ1","IKZF1") for x in known["th1"]}
h5, f = open_remote()
def readcol(g,n):
    d=g[n]
    if hasattr(d,"keys") and "categories" in d:
        c=np.array([x.decode() if isinstance(x,bytes) else x for x in d["categories"][:]]); return c[d["codes"][:]]
    return np.array([x.decode() if isinstance(x,bytes) else x for x in d[:]])
genes=readcol(h5["var"],"gene_name"); gidx={g:i for i,g in enumerate(genes)}
Z=h5["layers"]["zscore"]
def sig_up(path,thr=2.0):
    df=pd.read_csv(path); gcol="variable" if "variable" in df else df.columns[0]
    if "zscore" not in df: df["zscore"]=df["log_fc"]/df["lfcSE"]
    s=df.groupby(gcol)["zscore"].mean()
    return [gidx[g] for g in s[s>thr].index if g in gidx]
ota=pd.read_csv(f"{REPO}/metadata/suppl_tables/Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv")
ota=ota[ota.contrast.str.contains("Ota")].groupby("variable").zscore.mean()
C={"ota_th2":[gidx[g] for g in ota[ota>0].index if g in gidx],
   "ota_th1":[gidx[g] for g in ota[ota<0].index if g in gidx],
   "th2vth0":sig_up(f"{REPO}/src/4_polarization_signatures/results/Th2_vs_Th0_DE_results.csv"),
   "th1vth0":sig_up(f"{REPO}/src/4_polarization_signatures/results/Th1_vs_Th0_DE_results.csv")}
p(f"arm sizes: Ota-Th2={len(C['ota_th2'])} Ota-Th1={len(C['ota_th1'])} Th2vTh0={len(C['th2vth0'])} Th1vTh0={len(C['th1vth0'])}")

# ---- T3: decisive, minimal reads ----
probe=["GATA3","STAT6","RARA","IL4R","AMBRA1","ARNT","RAB21","UBA6","DPP4","TBX21","STAT1"]
ppos=[i for g in probe for i in m.index[m.gene==g]]
p(f"\n[T3] reading {len(ppos)} probe rows ...")
Zp={}
for j,i in enumerate(ppos): Zp[i]=Z[i,:]
def arm(z,k): return float(np.nanmean(z[C[k]]))
p(f"{'gene':8s}{'cond':10s}{'Th2vTh0':>9s}{'Th1vTh0':>9s}  verdict")
for g in probe:
    for i in m.index[m.gene==g]:
        z=Zp[i]; a2=arm(z,'th2vth0'); a1=arm(z,'th1vth0')
        v="Th1-SKEWER" if (a1>1 and a2<0.5) else ("selective" if (a2<-1 and abs(a1)<1) else "")
        p(f"{g:8s}{m.loc[i,'condition']:10s}{a2:9.2f}{a1:9.2f}  {v}")

# ---- T1/T2 on a 400-row sample ----
p(f"\n[T1/T2] reading 400-row sample ...")
samp=sorted(set(m.index[m.selective].tolist()) | set(rng.choice(m.index,350,replace=False).tolist()))
Zs={}
for j,i in enumerate(samp):
    Zs[i]=Zr=Z[i,:]
    if (j+1)%150==0: p(f"  {j+1}/{len(samp)} ({f.n_bytes/1e6:.0f}MB)")
h5.close(); p(f"read {f.n_bytes/1e6:.0f}MB / {f.n_reqs} reqs")
pos=list(Zs.keys())
def a_naive(k): return np.array([np.nanmean(Zs[i][C[k]]) for i in pos])
def a_comp(k):  return np.array([ (lambda z:(np.nanmean(((z-np.nanmean(z))/np.nanstd(z))[C[k]])))(Zs[i]) for i in pos])
n2,n1=a_naive("ota_th2"),a_naive("ota_th1"); c2,c1=a_comp("ota_th2"),a_comp("ota_th1")
p(f"\n[T1] arm correlation: naive(mean-of-z)={np.corrcoef(n2,n1)[0,1]:+.2f}  competitive={np.corrcoef(c2,c1)[0,1]:+.2f}")
def nsel(a2,a1):
    z2=(a2-a2.mean())/a2.std(); z1=(a1-a1.mean())/a1.std(); return int(((z2<=-2)&(np.abs(z1)<=1)).sum())
obs=nsel(n2,n1); allc=np.arange(len(genes)); null=[]
for _ in range(150):
    r2=rng.choice(allc,len(C['ota_th2']),replace=False); r1=rng.choice(allc,len(C['ota_th1']),replace=False)
    null.append(nsel(np.array([np.nanmean(Zs[i][r2]) for i in pos]),np.array([np.nanmean(Zs[i][r1]) for i in pos])))
null=np.array(null)
p(f"[T2] selective count: observed={obs}  null random-gene-sets mean={null.mean():.0f}±{null.std():.0f}  emp_p={(null>=obs).mean():.2f}  enrichment={obs/max(null.mean(),1):.2f}x")
