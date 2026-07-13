"""
03_annotate_network.py — reassemble the druggable type-2 network from the annotation layers.

The three layers were produced via external services (not re-run here):
  * druggability_genetics.csv — Open Targets Platform (Target.tractability: small-molecule /
    antibody / PROTAC buckets) + GWAS Catalog (atopic dermatitis / atopy / allergy / asthma),
    queried per Ensembl id via the Claude Science clinical-genomics + human-genetics MCP connectors.
  * AD_patient_validation.csv — GEO GSE147424 (atopic dermatitis skin scRNA-seq); per-candidate
    lesional-vs-control DE in the T-cell (CD3+) compartment.
  * candidate_nodes.csv — top collapse-scored nodes + stimulation-specificity class (from 02).
This script documents that provenance and reassembles druggable_type2_network.csv from the layer
CSVs so the composite is fully reproducible.

Composite network_confidence (transparent, additive; see next_degrader_report.md):
  0.30*collapse + 0.25*druggability + 0.15*stim-specificity + 0.15*patient + 0.10*GWAS + 0.05*off-axis
"""
import numpy as np, pandas as pd
from pathlib import Path
OUT = Path(__file__).resolve().parent.parent/"outputs"
cand = pd.read_csv(OUT/"candidate_nodes.csv"); dg = pd.read_csv(OUT/"druggability_genetics.csv"); av = pd.read_csv(OUT/"AD_patient_validation.csv")
BUCKET = {"approved/clinical small-molecule":1.0,"degrader handle (PROTAC)":0.9,
          "ligandable pocket (SM discovery)":0.7,"antibody/surface":0.4,"hard/undrugged":0.1,"unknown":0.2}
net = (cand.merge(dg[["gene","tractability_bucket","has_protac_bucket","sm_bucket_detail",
                      "ad_association_score","gwas_ad_support","gwas_trait_hits","off_axis"]], on="gene", how="left")
           .merge(av[["gene","dataset_accession","compartment","log2FC_lesional_vs_control",
                      "pvalue","padj","upregulated_in_lesion"]], on="gene", how="left"))
net["c_collapse"] = (net.collapse_score.clip(lower=0)/net.collapse_score.max()).round(3)
net["c_drug"]     = net.tractability_bucket.map(BUCKET)
net["c_stim"]     = net.stim_class.map(lambda s: 1.0 if s in ("activation-gated","stim-only(detected)") else 0.3)
net["c_gwas"]     = net.gwas_ad_support.map({True:1.0, False:0.0}).fillna(0.0)
net["c_patient"]  = np.where(net.upregulated_in_lesion==True, np.clip(net.log2FC_lesional_vs_control.fillna(0),0,1), 0.0)
net["c_offaxis"]  = net.off_axis.map({True:1.0, False:0.0}).fillna(1.0)
net["network_confidence"] = (0.30*net.c_collapse + 0.25*net.c_drug + 0.15*net.c_stim
                             + 0.15*net.c_patient + 0.10*net.c_gwas + 0.05*net.c_offaxis).round(3)
net.sort_values("network_confidence", ascending=False).to_csv(OUT/"druggable_type2_network.csv", index=False)
print("reassembled outputs/druggable_type2_network.csv", net.shape)
print(net[~net.is_anchor].sort_values("network_confidence",ascending=False)
        .head(8)[["gene","collapse_score","tractability_bucket","gwas_ad_support","network_confidence"]].to_string(index=False))
