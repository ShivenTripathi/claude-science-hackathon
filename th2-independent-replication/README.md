# Th2 selective-suppressor — independent replication

An **independent, from-scratch re-analysis** of the same question as
[`../th2-selective-suppressors/`](../th2-selective-suppressors): in the Zhu & Dann et al. 2025
genome-scale CRISPRi Perturb-seq screen (primary human CD4+ T cells), are there **selective Th2
suppressors** — knockdowns that lower the Th2 program while leaving Th1 flat (the allergy-relevant
target the paper's single bidirectional Th2−Th1 axis can't isolate)?

> **Same honest bottom line: a calibrated negative result.** Built with a different pipeline and
> tooling, this replication independently reaches the same conclusion — under a clean **matched
> Th1-vs-Th0 arm, GATA3 (the apparent top hit) is a Th1-skewer, not a selective suppressor** (its
> knockdown *induces* Th1, ≈ +2.8 SD). Single-gene selective suppression is not established by this
> screen + metric, because Th1/Th2 are genuinely reciprocal. Agreement between two independent
> pipelines is the point.

## What's here
- **`index.html`** — an interactive **primer + write-up**: the biology from zero, the "wedge" idea,
  the results (corrected to the negative finding), a worked mechanism-card format, and what actually
  holds up. (Also published as a Claude artifact.)
- **`src/`** — the pipeline:
  - `common/remote_h5.py` — read the 16.8 GB public-S3 `.h5ad` over **HTTP byte-ranges** (no download).
  - `stage_a/a1*` — ingest the arm scores, **GATA3 alignment guardrail** (caught a silent
    arm↔annotation row-order scramble — 0.9% overlap — and fixed it with a 2.5 MB remote read),
    reproduce the 172 selective set.
  - `stage_a/a2_rigor.py` — QC gates, donor reproducibility, threshold sweep, known-regulator recall,
    diff vs the published atlas.
  - `stage_b/b1–b4` — remote structure inspection, arm cross-check, co-perturbation coherence, triage.
  - `stage_b/b5–b6_verify*` — **the decisive verification**: matched Th1-vs-Th0 arm (GATA3 → Th1-skewer),
    competitive rank scoring, permutation null.
  - `results/shortlist/mechanism_cards/AMBRA1.json` — the mechanism-card format (illustrative; did **not**
    survive hardening).
- **`results/`** — tables, the (superseded) shortlist, the mechanism card.
- **`data/haltavey/`** — the arm-score inputs. **`data/s3/` (the 16.8 GB matrix) is intentionally
  excluded** — it is streamed, not stored.

## What this replication adds
1. **A pure streaming approach** — never downloads the matrix; reads only the ~50 MB of rows it needs.
2. **A concrete QC catch** — the arm arrays were in the h5ad `obs` order, not the annotation-table
   order; the GATA3 guardrail caught the resulting gene-scramble before it poisoned everything.
3. **A pedagogical primer** (`index.html`) — the biology and the full reasoning for a non-specialist.

## Honest limitations
Selectivity ≠ efficacy/safety; Th2 has protective roles (anti-helminth, barrier); this is transcriptomic
screen evidence, not in vivo. Before any target claim: a functional IL-4/5/13 readout + a control-guide FDR.

Data: Zhu & Dann et al. 2025 (Marson lab); signature: Ota et al. 2021. Full provenance in the
[top-level README](../README.md).
