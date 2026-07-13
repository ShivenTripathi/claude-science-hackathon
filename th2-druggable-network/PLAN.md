# Plan: the druggable intracellular type-2 network beyond STAT6

## Context
Third companion to `../th2-selective-suppressors/` and `../th2-independent-replication/`. Those two
strands independently scored the screen for selective Th2 suppressors and both reached a calibrated
negative (FDR ≈ 1; GATA3 is a Th1-skewer). Motivated by a "next-degrader" thesis: STAT6 was recently
degraded orally with biologic-like efficacy in atopic dermatitis (AD), proving an intracellular
master regulator of the type-2 program can be drugged. Most Perturb-seq target work stops at "which
knockout shifts the phenotype." Here we fuse functional genomics with chemical tractability in one
ranking, and anchor it to AD patients.

Dataset: Zhu & Dann et al. 2025 Marson-lab genome-scale CRISPRi Perturb-seq, primary human CD4+
T cells; public S3 `s3://genome-scale-tcell-perturb-seq/marson2025_data/`.

## Why anchor on STAT6/GATA3
The naive "Th2 down & Th1 flat" residual is dominated by low-power noise. The fix is a positive
anchor: GATA3/STAT6 have a measurable trans footprint, so scoring who else reproduces their collapse
calibrates (anchors self-recover, permutation p < 0.001, known regulators enriched).

## Steps
1. **Scorer.** Build the per-condition STAT6/GATA3 consensus collapse signature on the informative
   "program genes"; score every well-powered perturbation by Pearson correlation to it. Validate:
   anchor self-recovery, held-out IL4R recovery, permutation null, known-regulator recall. Package
   as a reusable module.
2. **Annotate the top nodes** (two parallel tracks + a specificity layer):
   - Druggability + genetics: Open Targets Target.tractability (small-molecule / antibody / PROTAC)
     + GWAS Catalog AD/atopy/allergy associations; flag off-IL4R/STAT6-axis.
   - Patient anchoring: find a public AD skin scRNA-seq dataset; test candidate upregulation in the
     lesional T-cell compartment.
   - Stimulation-specificity: classify each node constitutive / activation-gated / stim-only.
3. **Assemble** the ranked map with a transparent additive confidence, write the report + figures,
   wire into the repo and the GitHub Pages landing page.

## Deliverables
`th2_collapse_scorer.py`, `th2_collapse_scores.csv`, `candidate_nodes.csv`, `druggability_genetics.csv`,
`AD_patient_validation.csv`, `druggable_type2_network.csv`, `next_degrader_report.md`,
`next_degrader_network.png`, `AD_validation_volcano.png`, `deck.html`.
