"""
02_score_collapse.py — build the STAT6/GATA3 anchor signature and score every well-powered
perturbation for how well it phenocopies the type-2 collapse.

Reproduces outputs/th2_collapse_scores.csv from the streamed DE matrix + th2_collapse_scorer.py.
Rationale: a naive "Th2 down & Th1 flat" residual is dominated by low-power noise (FDR ~ 1 in the
sibling projects). Anchoring instead on the STAT6/GATA3 collapse is a POSITIVE signal that calibrates.
"""
import numpy as np, pandas as pd, importlib.util
from pathlib import Path
HERE = Path(__file__).resolve().parent; DATA = HERE.parent/"data"; OUT = HERE.parent/"outputs"

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
stream = _load("stream", HERE/"01_stream_matrix.py")
scorer = _load("scorer", HERE/"th2_collapse_scorer.py")

obs, var, off, rb = stream.open_structure()
obs_pos = {k:i for i,k in enumerate(obs)}; g2c = {g:i for i,g in enumerate(var)}
de = pd.read_csv(DATA/"DE_stats.suppl_table.csv"); de["mrow"] = de["index"].map(obs_pos)
gene2ens = (de.dropna(subset=["target_contrast"]).drop_duplicates("target_contrast_gene_name")
              .set_index("target_contrast_gene_name")["target_contrast"].to_dict())
CONDS = ["Rest","Stim8hr","Stim48hr"]

anchors = {(g,c): obs_pos[f"{gene2ens.get(g)}_{c}"] for g in ("GATA3","STAT6") for c in CONDS
           if f"{gene2ens.get(g)}_{c}" in obs_pos}
Za = stream.fetch_rows(sorted(set(anchors.values())), off, rb)
sig = scorer.build_signature({k: Za[v] for k,v in anchors.items()}, g2c)

wp = de[(de.ontarget_significant)&(de.n_total_de_genes>=50)].dropna(subset=["mrow"]).copy()
Z = stream.fetch_rows(sorted({int(r) for r in wp.mrow}), off, rb, workers=32)
rows = [dict(gene=r.target_contrast_gene_name, condition=r.culture_condition, index=r["index"],
             collapse_score=scorer.collapse_score(Z[int(r.mrow)], r.culture_condition, sig, g2c, r.target_contrast_gene_name),
             n_de=r.n_total_de_genes, n_cells=r.n_cells_target) for _,r in wp.iterrows()]
sc = pd.DataFrame(rows)
sc["rank_in_cond"] = sc.groupby("condition").collapse_score.rank(ascending=False)
sc["pctile_in_cond"] = sc.groupby("condition").collapse_score.rank(pct=True)*100
sc.sort_values(["condition","collapse_score"], ascending=[True,False]).to_csv(OUT/"th2_collapse_scores.csv", index=False)
for g in ("GATA3","STAT6","IL4R"):
    s = sc[sc.gene==g]
    if len(s): print(g, [(r.condition, round(r.collapse_score,3), f"#{int(r.rank_in_cond)}") for _,r in s.iterrows()])
print("wrote outputs/th2_collapse_scores.csv", sc.shape)
