# Provenance

## Data (`data/`)
- `DE_stats.suppl_table.csv` — per-perturbation QC/DE summary (33,983 rows) from the Zhu & Dann
  et al. 2025 GWCD4i.DE_stats.h5ad supplementary object. Selects well-powered perturbations and
  maps gene names to matrix rows.
- `th2_arm.npy`, `th1_arm.npy`, `Th2_Th1_signature.csv` — the Ota-2021 Th2/Th1 arm inputs
  (shared with the sibling strands).

## The 16.8 GB DE matrix (not committed)
Notebooks 01/02 stream specific rows of the `zscore` layer of
`s3://genome-scale-tcell-perturb-seq/marson2025_data/GWCD4i.DE_stats.h5ad`
(public) by HTTP byte-range. The layer is a contiguous dense float64 array (33,983 × 10,282), so
row i is at `data_offset + i*row_bytes` (~82 KB/row) — no full download.

## Annotation layers (`outputs/`, produced via external services)
- `druggability_genetics.csv` — Open Targets Platform GraphQL (Target.tractability) + GWAS Catalog,
  queried per Ensembl id via the Claude Science clinical-genomics + human-genetics MCP connectors.
- `AD_patient_validation.csv` — GEO **GSE147424** (atopic dermatitis skin scRNA-seq); per-candidate
  lesional-vs-control DE in the T-cell (CD3+) compartment.
`03_annotate_network.py` documents both and reassembles `druggable_type2_network.csv` from them.

## Scorer
`th2_collapse_scorer.py` (in `notebooks/` and mirrored in `outputs/`) is standalone and documented.
`anchor_signature.npz` bundles the per-condition program genes + consensus weights it builds.
