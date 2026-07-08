"""
Phase 2/3 groundwork (no h5ad needed): build a per (target_gene x condition) annotation
table from local supplementary tables — donor stability, KD self-silencing, guide
concordance, artifact flags, and druggability/target class.

Run: python notebooks/02_annotations.py  ->  outputs/annotations.parquet
"""
import re, numpy as np, pandas as pd
from pathlib import Path
ROOT = Path("/Users/shiventripathi/dev/science/th2_selective")
DATA = ROOT/"data"; OUT = ROOT/"outputs"; OUT.mkdir(exist_ok=True)

de = pd.read_csv(DATA/"DE_stats.suppl_table.csv")
de = de.rename(columns={"target_contrast_gene_name":"target_gene","target_contrast":"target_ensembl"})
keep = ["target_gene","target_ensembl","culture_condition","n_cells_target","n_up_genes",
        "n_down_genes","n_total_de_genes","ontarget_effect_size","ontarget_significant",
        "target_baseMean","offtarget_flag","n_downstream","crossdonor_correlation_mean",
        "crossdonor_correlation_min","crossguide_correlation"]
ann = de[keep].copy()

# ---- guide KD self-silencing: fraction of guides with significant knockdown per gene x condition ----
kd = pd.read_csv(DATA/"guide_kd_efficiency.suppl_table.csv")
kd_frac = (kd.groupby(["perturbed_gene_id","culture_condition"])
             .agg(n_guides=("signif_knockdown","size"),
                  n_signif_guides=("signif_knockdown","sum")).reset_index())
kd_frac["frac_signif_guides"] = kd_frac.n_signif_guides / kd_frac.n_guides
ann = ann.merge(kd_frac.rename(columns={"perturbed_gene_id":"target_ensembl"}),
                on=["target_ensembl","culture_condition"], how="left")

# ---- target-class / artifact annotation ----
# Lambert file cols: ID(ENSG), Name(symbol), DBD, is_TF(Yes/No)
_lam = pd.read_csv(DATA/"Lambert_2018_HumanTF.csv")
tf = set(_lam.loc[_lam.is_TF.astype(str).str.strip().eq("Yes"), "Name"].astype(str))

E3_PREFIX = ("RNF","TRIM","HERC","MARCHF","MARCH","ZNRF","PELI","WWP","SIAH","DTX","UBR",
             "UBE3","UBE4","RC3H","MDM","CUL","FBXW","FBXO","FBXL","FBXL","KLHL","KLHDC","ASB",
             "RBX","ZYG11","FEM1","DCAF","BTBD","SPSB","KCTD","SOCS","LNX","MKRN","MGRN","RCHY",
             "PJA","TRAIP","TRIP","BIRC","NEURL","TOPORS","ZBTB")
E3_EXACT = {"ITCH","CBLB","CBL","CBLC","CBLL1","NEDD4","NEDD4L","STUB1","VHL","MDM2","MDM4",
            "PELI1","PELI2","RNF128","HUWE1","SMURF1","SMURF2","GRAIL","AMFR","RNF41","PJA1",
            "PJA2","TRAF6","TRAF3","TRAF2","KEAP1","SPOP","FBXW7","DDB1","DDB2","VPS11","WSB1",
            "WSB2","ELOB","ELOC","GAN","HACE1","UHRF1","MYLIP","MARCHF7","RLIM","AREL1"}
KIN_EXACT = {"MAP2K1","MAP2K2","MAP2K3","MAP2K4","MAP2K6","MAP2K7","MAPK1","MAPK3","MAPK8","MAPK9",
             "MAPK14","LCK","FYN","ZAP70","ITK","TXK","LAT","PDPK1","AKT1","AKT2","PIK3CD","PIK3CA",
             "PRKCQ","PRKCA","PRKD2","MAP3K7","MAP3K8","MAP4K1","MAP4K3","IKBKB","IKBKE","CHUK",
             "JAK1","JAK2","JAK3","TYK2","STK11","STK17B","STK35","STK39","STK4","STK25","GSK3B",
             "MTOR","RPS6KB1","RPS6KA1","CAMK2D","CAMK4","CDK1","CDK4","CDK6","CDK7","CDK9","DGKA",
             "DGKZ","PIM1","PIM2","NEK6","TBK1","RIPK1","RIPK2","RIPK3","TAOK1","TAOK3","WNK1","SGK1"}

def classify(g):
    g = str(g)
    if g.startswith(("RPL","RPS","MRPL","MRPS")): return "ribosomal_artifact"
    if g.startswith("MT-") or g in {"MT-CO1","MT-ND1"}: return "mito_artifact"
    return None

CELLCYCLE = {"MKI67","TOP2A","CCNB1","CCNB2","CCNA2","CDK1","CDC20","AURKB","BUB1","PLK1",
             "PCNA","MCM2","MCM3","MCM4","MCM5","MCM6","CDT1","CDC6","E2F1","CCNE1","CCND3"}

def target_class(g):
    g = str(g)
    art = classify(g)
    if art: return art
    if g in CELLCYCLE: return "cellcycle_artifact"
    if g in E3_EXACT or g.startswith(E3_PREFIX): return "E3_ligase"
    if g in KIN_EXACT: return "kinase"
    if g in tf: return "TF"
    return "other"

ann["target_class"] = ann.target_gene.map(target_class)
ann["is_artifact_class"] = ann.target_class.str.endswith("artifact")

# global-magnitude / broad-effect proxy (sick-cell dampening): high total DE burden
thr_broad = ann.n_total_de_genes.quantile(0.95)
ann["broad_effect_flag"] = ann.n_total_de_genes > thr_broad

ann.to_parquet(OUT/"annotations.parquet")
print("[annotations] rows:", len(ann), " unique target genes:", ann.target_gene.nunique())
print("[target_class counts]\n", ann.drop_duplicates("target_gene").target_class.value_counts())
print("[KD] frac with ontarget_significant:", round(ann.ontarget_significant.mean(),3))
print("[broad-effect 95pct cutoff] n_total_de_genes >", int(thr_broad))
print("\nGATA3:\n", ann[ann.target_gene=="GATA3"][["culture_condition","ontarget_significant",
      "ontarget_effect_size","frac_signif_guides","crossdonor_correlation_mean","target_class"]].to_string(index=False))
print("\nsample E3 ligases found:", sorted(ann[ann.target_class=="E3_ligase"].target_gene.unique())[:20])
