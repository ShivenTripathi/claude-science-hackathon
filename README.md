# claude-science-hackathon

Work from the **Built with Claude: Life Sciences** hackathon (Researcher track).

> **Start with [`RECONCILIATION.md`](./RECONCILIATION.md)** — the single reconciled view across all
> three tracks: what agrees, the one sharp correction (GATA3), the cross-pipeline convergence, and
> what actually survives. Short version: the core scientific claim is a **calibrated negative** —
> single-gene selective Th2 suppression is not established by this screen — and the durable
> deliverables are the reproducible pipeline, the agentic review infrastructure, and the AD
> translational-filter layer.

## Projects

### [`th2-selective-suppressors/`](./th2-selective-suppressors) — Selective Th2 suppressor re-analysis

A re-analysis of the **Zhu & Dann et al. 2025** genome-scale CRISPRi Perturb-seq screen in primary
human CD4+ T cells, asking: *which gene knockdowns selectively suppress the Th2 program (GATA3 / IL4 /
IL5 / IL13) without flipping cells toward Th1?* — the allergy-relevant distinction the paper's single
bidirectional Th2−Th1 axis can't make on its own.

**Honest bottom line (read this first).** After a rigorous re-analysis, the naive
selective-suppressor atlas **does not survive proper statistics** — this repo documents a *calibrated
negative result*, not a target list:

- Competitive rank-based scoring collapses the "global-magnitude" arm correlation **+0.54 → +0.18**,
  showing most of that confound was an artifact of the initial mean-of-z scoring.
- A permutation null shows the "selective" set is **not enriched over random gene sets** of the same
  size (empirical FDR ≈ 1) — a consequence of genuine Th1/Th2 reciprocity.
- **GATA3**, the apparent top hit, reads as a **Th1-skewer** under proper scoring with a matched
  Th1-vs-Th0 arm (+2.8) — exactly as canonical biology predicts (GATA3 loss de-represses T-bet).

What *did* hold up and is the real contribution: a reproducible streaming pipeline over a 16.8 GB
remote AnnData (reading only what's needed), an **agentic investigate→verify mechanism-dossier layer**,
and a **6-agent literature + methods self-audit** that caught the over-claim before it went out.

**Interactive dashboard (self-contained):**
https://claude.ai/code/artifact/65051cc2-afc8-44ec-b5f8-b72349fafb54

### [`th2-independent-replication/`](./th2-independent-replication) — Independent from-scratch replication

A second, independently-built pipeline for the same question. Different tooling, different code — same
honest bottom line: under a clean matched Th1-vs-Th0 arm, GATA3 (the apparent top hit) is a
**Th1-skewer**, not a selective suppressor. Agreement between two independent pipelines is the point.

### [`th2-ad-translation/`](./th2-ad-translation) — Atopic-dermatitis target translation

The therapeutic-translation layer, following a pharma researcher's brief: **AD patient-skin validation**
(GSE147424), **Open Targets + HPA druggability**, and **off-axis (non-Dupixent) classification** of the
candidates. Conditioned on the calibrated negative — these are the filters a target would additionally
have to pass *if* it ever cleared a functional selectivity test; the druggability and off-axis
annotations hold independently of the negative.

## Data provenance & citation

Input data under `th2-selective-suppressors/data/` are **public supplementary tables** from the
source study and an external reference signature, redistributed here for reproducibility with
attribution:

- Zhu R., Dann E. et al. (2025) *Genome-scale perturb-seq in primary human CD4+ T cells maps
  context-specific regulators of T cell programs and human immune traits.* bioRxiv 2025.12.23.696273.
  Code/metadata: https://github.com/emdann/GWT_perturbseq_analysis_2025 · Data (public, no-sign):
  `s3://genome-scale-tcell-perturb-seq/marson2025_data/`
- Ota M. et al. (2021) Th2-vs-Th1 reference signature.
- He H. et al. (2020) *Single-cell transcriptome analysis of human skin identifies novel fibroblast
  subpopulation and enrichment of immune subsets in atopic dermatitis.* J Allergy Clin Immunol; data
  GEO **GSE147424** (used in `th2-ad-translation/` for AD lesional-skin validation).
- AD peripheral-blood PBMC scRNA-seq, GEO **GSE189188** (used in `th2-ad-translation/` for the
  screen-matched blood-CD4 secondary validation).
- Human Protein Atlas (proteinatlas.org) and Open Targets Platform — target druggability annotation
  (`th2-ad-translation/`).

The large DE matrix (`GWCD4i.DE_stats.h5ad`, 16.8 GB) is **not** vendored — the code streams it
directly from the public S3 bucket.

🤖 Analysis and tooling generated with [Claude Code](https://claude.com/claude-code).
