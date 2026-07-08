"""
Hardened re-analysis addressing the methods red-team:
 (1) COMPETITIVE rank-based scoring (singscore-style) instead of mean-of-z -> removes the
     global-magnitude confound at the scoring step (test: does the +0.54 arm corr collapse?).
 (2) PERMUTATION NULL -> empirical FDR on the selective count (random same-size gene sets).
 (3) MULTI-LINEAGE + PROLIFERATION control arms (Th1/Th17/Treg/cell-cycle, from the dataset's
     own vs-Th0 signatures) -> 'selective' = Th2 down while ALL other arms flat (kills lineage
     diversion + sick-cell artifacts).
 (4) TWO-SIGNATURE CONCORDANCE (Ota Th2-vs-Th1 AND matched Th2-vs-Th0).
Streams the zscore matrix once via parallel HTTP range reads.
"""
import json, numpy as np, pandas as pd, h5py, fsspec, requests
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT=Path("/Users/shiventripathi/dev/science/th2_selective"); DATA,OUT=ROOT/"data",ROOT/"outputs"
URL="https://genome-scale-tcell-perturb-seq.s3.amazonaws.com/marson2025_data/GWCD4i.DE_stats.h5ad"

# ---------- gene sets ----------
def upset(csv, lfc=0.5, adjp=0.05, sign=+1, topn=None):
    d=pd.read_csv(DATA/csv)
    m=(d.adj_p_value<adjp)&((d.log_fc>lfc) if sign>0 else (d.log_fc<-lfc))
    s=d[m].reindex(d[m].log_fc.abs().sort_values(ascending=False).index)
    genes=list(dict.fromkeys(s.variable)); return set(genes[:topn] if topn else genes)
ota=pd.read_csv(DATA/"Ota_Th2vsTh1_DE_results.csv")
SETS={
 "th2":  set(ota.loc[(ota.adj_p_value<.05)&(ota.log_fc> .5),"variable"]),   # Ota Th2-up
 "th1":  set(ota.loc[(ota.adj_p_value<.05)&(ota.log_fc<-.5),"variable"]),   # Ota Th1-up
 "th2_v0": upset("Th2_vs_Th0_DE_results.csv"),   # matched, dataset's own
 "th1_v0": upset("Th1_vs_Th0_DE_results.csv"),
 "th17_v0":upset("Th17_vs_Th0_DE_results.csv"),
 "treg_v0":upset("Treg_vs_Th0_DE_results.csv"),
}
CELLCYCLE={"MCM5","PCNA","TYMS","MCM2","MCM4","RRM1","UNG","MCM6","DTL","UHRF1","HELLS","RPA2","GMNN","RRM2",
 "CDC45","CDC6","EXO1","USP1","CLSPN","HMGB2","CDK1","NUSAP1","UBE2C","BIRC5","TPX2","TOP2A","NDC80","CKS2",
 "MKI67","CENPF","SMC4","CCNB2","AURKB","BUB1","KIF11","CDC20","TTK","KIF2C","DLGAP5","AURKA","ANLN","NEK2","CENPA"}
SETS["prolif"]=CELLCYCLE

# ---------- align obs + var ----------
arms=pd.read_parquet(OUT/"arms.parquet")  # row order == obs order
fo=fsspec.filesystem("https").open(URL, block_size=8*2**20)
with h5py.File(fo,"r") as f:
    genes=np.array([x.decode() if isinstance(x,bytes) else x for x in f["var"]["gene_name"][:]])
    dset=f["layers"]["zscore"]; shape,dtype=dset.shape,dset.dtype; offset=dset.id.get_offset()
g2i={g:i for i,g in enumerate(genes)}
idx={k:np.array(sorted(g2i[g] for g in s if g in g2i)) for k,s in SETS.items()}
for k in idx: print(f"[set] {k:8s} measured {len(idx[k])}/{len(SETS[k])}")
N=shape[1]; ncol=N; isz=dtype.itemsize; B=2000
# random null sets (Th2-sized) drawn from measured genes
rng=np.random.default_rng(0); M=100; th2n=len(idx["th2"])
null_idx=[rng.choice(N, size=th2n, replace=False) for _ in range(M)]

# ---------- competitive rank scoring in row-blocks ----------
keys=list(idx.keys())
comp={k:np.empty(shape[0]) for k in keys}
nullscore=np.empty((M, shape[0]))
def fetch(i0):
    i1=min(i0+B, shape[0]); b0=offset+i0*ncol*isz; b1=offset+i1*ncol*isz
    for a in range(4):
        try: r=requests.get(URL, headers={"Range":f"bytes={b0}-{b1-1}"}, timeout=180); r.raise_for_status(); break
        except Exception:
            if a==3: raise
    Z=np.frombuffer(r.content, dtype=dtype).reshape(i1-i0, ncol)
    Z=np.nan_to_num(np.asarray(Z, np.float32))
    ranks=Z.argsort(1).argsort(1).astype(np.float32)          # 0 = most suppressed
    ranks=(ranks/(ncol-1))-0.5                                 # competitive, genome-normalized, [-.5,.5]
    out={k: ranks[:,idx[k]].mean(1) for k in keys}
    nl=np.stack([ranks[:,ni].mean(1) for ni in null_idx])      # (M, block)
    return i0, out, nl
starts=list(range(0,shape[0],B))
print(f"[stream] {len(starts)} blocks, competitive rank scoring + {M} null sets")
with ThreadPoolExecutor(max_workers=12) as ex:
    for k,(i0,out,nl) in enumerate(ex.map(fetch,starts)):
        for key in keys: comp[key][i0:i0+len(out[key])]=out[key]
        nullscore[:, i0:i0+nl.shape[1]]=nl
        if k%4==0: print(f"  block {k+1}/{len(starts)}", flush=True)

df=arms[["obs_index","target_gene","culture_condition"]].copy()
def zc(x): x=np.asarray(x,float); return (x-x.mean())/x.std()
for k in keys: df[f"c_{k}"]=zc(comp[k])
nullz=(nullscore - nullscore.mean(1,keepdims=True))/nullscore.std(1,keepdims=True)

# ---------- (1) does the arm correlation collapse under competitive scoring? ----------
old_corr=np.corrcoef(arms.th2_arm, arms.th1_arm)[0,1]
new_corr=np.corrcoef(df.c_th2, df.c_th1)[0,1]
print(f"\n[1) SCORING] arm corr: mean-of-z={old_corr:+.3f}  ->  competitive rank={new_corr:+.3f}")

# ---------- (3) multi-arm selective + (4) concordance ----------
GATE_DOWN=-2.0; FLAT=1.0
th1_flat=df.c_th1.abs()<FLAT; th17_flat=df.c_th17_v0.abs()<FLAT; treg_flat=df.c_treg_v0.abs()<FLAT
prolif_flat=df.c_prolif.abs()<FLAT; th1v0_flat=df.c_th1_v0.abs()<FLAT
df["sel_th2_only"]=(df.c_th2<GATE_DOWN)&th1_flat                                   # original-style (2 arm)
df["sel_multi"]=(df.c_th2<GATE_DOWN)&th1_flat&th17_flat&treg_flat&prolif_flat&th1v0_flat
df["concordant"]=(df.c_th2<GATE_DOWN)&(df.c_th2_v0<GATE_DOWN)                       # Ota AND vs-Th0 agree
df["sel_hardened"]=df.sel_multi&df.concordant
n2=int(df.sel_th2_only.sum()); nm=int(df.sel_multi.sum()); nh=int(df.sel_hardened.sum())
print(f"[3) MULTI-ARM] selective (Th2 down, Th1 flat) = {n2}")
print(f"               + Th17/Treg/prolif/Th1v0 flat  = {nm}")
print(f"[4) CONCORDANCE] + Ota&vs-Th0 agree (hardened) = {nh}")

# ---------- (2) permutation FDR ----------
# expected 'selective' calls if the Th2 set were random (same size), same Th1-flat gate
null_counts=[int(((nullz[m]<GATE_DOWN)&th1_flat.to_numpy()).sum()) for m in range(M)]
exp_fp=float(np.mean(null_counts)); fdr=exp_fp/max(n2,1)
print(f"\n[2) FDR] observed selective(2-arm)={n2}  expected under random Th2 set={exp_fp:.1f}  ->  empirical FDR={fdr:.2f}")
null_multi=[int(((nullz[m]<GATE_DOWN)&th1_flat.to_numpy()&th17_flat.to_numpy()&treg_flat.to_numpy()&prolif_flat.to_numpy()).sum()) for m in range(M)]
fdr_m=float(np.mean(null_multi))/max(nm,1)
print(f"         multi-arm selective={nm}  expected null={np.mean(null_multi):.1f}  ->  FDR={fdr_m:.2f}")

# ---------- overlap with the old high-confidence set ----------
old=set(pd.read_csv(OUT/"real_vs_fp_shortlist.csv").target_gene)
hard_genes=set(df[df.sel_hardened].target_gene)
print(f"\n[survivors] hardened selective genes = {len(hard_genes)}")
print("  hardened set:", sorted(hard_genes))
print(f"  of old high-confidence ({len(old)}), survive hardening:", sorted(old & hard_genes))
gata=df[df.target_gene=='GATA3'][["culture_condition","c_th2","c_th1","c_th1_v0","c_th17_v0","c_treg_v0","c_prolif","sel_multi"]]
print("\n[GATA3 under competitive multi-arm scoring]\n", gata.to_string(index=False))

df.to_parquet(OUT/"hardened_scores.parquet")
short=df[df.sel_multi].merge(pd.read_csv(OUT/"real_vs_fp_shortlist.csv")[["target_gene","real_score","target_class","druggable"]],on="target_gene",how="left")
short.sort_values("c_th2").to_csv(OUT/"hardened_shortlist.csv",index=False)
json.dump({"old_corr":round(old_corr,3),"new_corr":round(new_corr,3),"sel_2arm":n2,"sel_multi":nm,
 "sel_hardened":nh,"fdr_2arm":round(fdr,3),"fdr_multi":round(fdr_m,3),
 "hardened_genes":sorted(hard_genes),"survivors_from_old":sorted(old&hard_genes)}, open(OUT/"hardened_stats.json","w"), indent=2)
print("\n[done] hardened_scores.parquet, hardened_shortlist.csv, hardened_stats.json")
