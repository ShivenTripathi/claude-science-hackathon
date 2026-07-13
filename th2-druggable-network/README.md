# The druggable intracellular type-2 network beyond STAT6

A **third, complementary strand** of the [Zhu & Dann et al. 2025 genome-scale CRISPRi Perturb-seq](../th2-selective-suppressors/)
re-analysis (primary human CD4+ T cells). The two sibling strands
([`th2-selective-suppressors/`](../th2-selective-suppressors) and the independent
[`th2-independent-replication/`](../th2-independent-replication)) both reach the **same calibrated
negative**: a naive "Th2 down & Th1 flat" selectivity residual is not enriched over random (FDR ≈ 1),
and GATA3 — the apparent top hit — is a Th1-skewer, not a selective suppressor. Two independent
pipelines agreeing is the honest result.

> **Read [`../RECONCILIATION.md`](../RECONCILIATION.md) first.** The other tracks establish a
> **calibrated negative** on *selective* Th2 suppression (FDR ≈ 1; GATA3 is a Th1-skewer). This track
> does **not** overturn that. It scores a *different* phenotype — **collapse phenocopy**, the bar an
> oral STAT6 degrader clears — which calibrates as a classifier and yields a druggable off-axis
> nomination map. It is conditioned on the same negative and caveats.

This strand asks what to do *next*, motivated by a "next-degrader" thesis: STAT6 was recently
**orally degraded with biologic-like efficacy in atopic dermatitis (AD)**, proving an intracellular
master regulator of the type-2 program is druggable. So instead of the noisy selectivity residual,
we **anchor on a positive signal** — score every perturbation for how well it phenocopies the
STAT6/GATA3 collapse — then fuse that with chemical tractability, stimulation-specificity, AD human
genetics, and AD patient skin.

> **Result, in one line.** Positive anchoring *calibrates where the residual did not*: GATA3/STAT6
> self-recover as #1/#2, held-out IL4R recovers out-of-sample, permutation p < 0.001, known
> regulators concentrate at the 87th percentile (vs recall@250 = 0 for the naive atlas). Layering
> Open Targets tractability + GWAS + AD patient scRNA-seq onto the ranking surfaces **ITK** and
> **INPP5D/SHIP1** as the most actionable off-axis nodes (existing chemical matter + AD/allergy GWAS +
> activation-gated), and **KDM8, UBA5, DOHH** as under-explored enzyme handles up in AD lesional skin.
> All transcriptional-footprint evidence in **un-polarized** CD4s — not a functional assay.

## How the three strands fit together
| strand | question | result |
|---|---|---|
| `th2-selective-suppressors/` | selective Th2 suppressors (naive residual) | calibrated negative, FDR ≈ 1 |
| `th2-independent-replication/` | same, independent pipeline | **same** negative; GATA3 = Th1-skewer (+2.8 SD) |
| **`th2-druggable-network/`** (this) | reframe to STAT6/GATA3 collapse phenocopy + druggability | positive, calibrated (p < 0.001); a druggable off-axis target map |

Three independent readouts converge on the negative; the positive reframe is what turns it into an
actionable target list.

## Start here
- **`deck.html`** — self-contained slide deck (open in a browser; also a Claude artifact).
- **`outputs/next_degrader_report.md`** — the consolidated written report.
- **`outputs/druggable_type2_network.csv`** — the ranked map (collapse + tractability + stim + GWAS + patient).
- **`outputs/th2_collapse_scorer.py`** — the reusable, documented scorer.

## Pipeline (`notebooks/`, run in order)
| step | script | what it does |
|---|---|---|
| 01 | `01_stream_matrix.py` | streaming primitive: fetch DE-matrix rows by HTTP byte-range (no 16.8 GB download) |
| 02 | `02_score_collapse.py` | build the STAT6/GATA3 anchor signature; score every well-powered perturbation |
| 03 | `03_annotate_network.py` | reassemble the composite from the annotation layers (documents the MCP/patient provenance) |

Reproduced on a clean run: GATA3 #1 in all three conditions (0.948 Rest), STAT6 #2, IL4R #3;
permutation p < 0.001; 63-node map, ITK 0.695 / INPP5D 0.660 top the off-axis ranking.

## The two annotation layers that use external services
`druggability_genetics.csv` (Open Targets tractability + GWAS Catalog) and `AD_patient_validation.csv`
(GEO GSE147424 AD skin scRNA-seq, T-cell compartment) were produced via the Claude Science MCP
connectors and a public patient download; `03_annotate_network.py` documents exactly how and
reassembles the composite, so the final map is fully reproducible from the committed CSVs.

## Honest caveats
Un-polarized cells (transcriptional footprint, not a Th2 assay); the collapse score is activation-
coupled (broader than cytokine-specific); patient log-fold-changes are directionally positive but
mostly not multiple-testing-significant in this small cohort; tractability flags mean *a handle
exists*, not that a degrader is feasible; mechanism ordering is inferred, not measured. See the report.

Data: Zhu & Dann et al. 2025 (Marson lab); signature: Ota et al. 2021; patient: GEO GSE147424.
