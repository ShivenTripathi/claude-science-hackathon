# `ad-offaxis-druggability/` — AD patient-validation + druggability layer, and a three-way reconciliation

The third analysis in this repo, and the one that **reconciles all three**. It takes the selective
Th2-suppressor candidates and asks a drug-discovery question — *for atopic dermatitis, off the
IL-4Rα–STAT6 axis, is any candidate upregulated in patient skin and druggable?* — then honestly
positions the answer against the two statistical-hardening pipelines
([`../th2-selective-suppressors/`](../th2-selective-suppressors),
[`../th2-independent-replication/`](../th2-independent-replication)).

## Read this first — the honest bottom line

> The naive selective-suppressor atlas **does not survive rigorous statistics** (Analyses 1 & 2), and
> a patient-validation + druggability layer on top of it **does not rescue it**. Three independent
> analyses produce **almost-disjoint candidate lists**; of 102 statistically-hardened survivors, only
> one has atopic-dermatitis genetic support — GATA3, the gene both pipelines re-classified as a
> Th1-skewer. Non-convergence *is* the evidence. → **[`reconciled_view.md`](./reconciled_view.md)**

## What's here

- **[`reconciled_view.md`](./reconciled_view.md)** — the comprehensive three-way reconciliation (start here).
- **[`SUBMISSION.md`](./SUBMISSION.md)** — 168-word summary, rubric mapping, 3-minute demo script.
- **[`ad_target_report.md`](./ad_target_report.md)** — the AD off-axis analysis on its own terms.
- **`tables/`**
  - `reconciliation_sets.csv`, `reconciliation_overlaps.csv` — the 8 candidate sets and their overlaps.
  - `their_survivors_common_footing.csv` — Analyses 1 & 2 survivors (102) annotated with druggability,
    AD genetics, and (partial) patient T-cell expression.
  - `ad_offaxis_target_atlas.csv` — all 626 candidates × 37 columns (off-axis flag, AD genetics,
    druggability, patient expression, AD-target score).
  - `ad_offaxis_lead_shortlist.csv` — 72 off-axis, patient-upregulated, tractable, selective leads.
  - `ad_patient_validation.csv` — per-gene T-cell / all-cell expression across Healthy / Non-lesional
    / Lesional.
- **`figures/`** — overlap matrix, patient dotplot, druggability×patient map, shortlist ranking.

## How it was built (Claude Science)

- **MCP connectors:** Open Targets GraphQL (tractability, AD-specific genetic associations, existing
  drugs) and STRING v12 (IL-4R/STAT6 axis classification).
- **Patient data:** CELLxGENE Atopic Dermatitis Atlas (280,518 skin cells; Nat Commun 2026; DOI
  10.1038/s41467-026-69587-7), T-cell-resolved lesional-vs-healthy expression.
- **Reconciliation:** overlap analysis against the two hardening pipelines' survivor sets.
- **Adversarial QC:** a continuous auditor loop caught and forced fixes to a colormap inversion, a
  fabricated citation, and a mislabeled axis during the build.

## Honest limitations

Selectivity ≠ efficacy/safety; Th2 is protective (anti-helminth, barrier). This is transcriptomic
screen + patient-expression evidence, not in vivo. Patient upregulation corroborates but does not
prove direction of effect. The patient-expression column on the 102 survivors is partial (CDN
throttling); druggability + genetics are complete. The decisive missing experiment — shared by all
three analyses — is a functional IL-4/5/13 readout with a control-guide FDR.

Data: Zhu & Dann et al. 2025 (Marson lab); Ota et al. 2021 signature; CELLxGENE AD atlas. Full
provenance in the [top-level README](../README.md).
