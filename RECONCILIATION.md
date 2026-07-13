# Reconciled view — selective Th2 suppressors and their AD-target translation

*This document reconciles three analyses of the same question against the Zhu & Dann et al. 2025
genome-scale CRISPRi Perturb-seq screen (primary human CD4⁺ T cells): the two re-analysis tracks
already in this repo, and a third **therapeutic-translation** track (`th2-ad-translation/`) added
here. It is the single place to understand what agrees, what was corrected, and what actually
survives.*

## The question

Can single-gene knockdowns **selectively suppress the Th2 program** (lower GATA3/IL-4/IL-5/IL-13)
**without flipping cells toward Th1** — the allergy/atopic-dermatitis-relevant target the paper's
single bidirectional Th2−Th1 axis cannot isolate on its own?

## Bottom line (read this first)

**On the core scientific claim, the calibrated *negative* result is the honest answer, and it
supersedes the optimistic atlas framing.** Under proper statistics — competitive rank scoring, a
matched Th1-vs-Th0 arm, and a permutation null — single-gene selective Th2 suppression is **not
established** by this screen:

- Competitive scoring collapses the two-arm correlation **+0.54 → +0.18** (`th2-selective-suppressors`,
  `th2-independent-replication`): most of the "global-magnitude confound" was a scoring artifact of
  mean-of-z, not biology.
- A permutation null shows the "selective" set is **not enriched over random gene sets** of the same
  size (empirical FDR ≈ 1.25 for the 2-arm set; ≈ 5.5 for the multi-lineage set) — genuine selective
  suppressors are no more common than chance, because Th1 and Th2 are genuinely reciprocal.
- With a **matched Th1-vs-Th0 arm**, **GATA3** — the apparent top hit in every optimistic pass —
  reads as a **Th1-skewer** (Th1-vs-Th0 ≈ +2.8): its knockdown *induces* Th1, exactly as canonical
  biology predicts (GATA3 loss de-represses T-bet). It is not a selective suppressor.

**What is real and worth keeping** is (a) the reproducible streaming pipeline over the 16.8 GB remote
AnnData, (b) the agentic investigate→adversarial-verify mechanism layer, (c) the multi-agent
literature/methods self-audit that caught the over-claim, and — added in the translation track —
(d) an **AD patient-expression validation**, (e) a **druggability/off-axis annotation** that
separates Dupixent-competitive nodes from novel-mechanism ones. These translation layers are useful
*conditioned on* the negative: they describe what one would check *if* a candidate ever cleared a
functional selectivity test — they do not, and cannot, rescue the negative.

## The three tracks

| Track | What it did | Verdict |
|---|---|---|
| **`th2-selective-suppressors/`** | Full pipeline: arm reconstruction → credibility tiering → magnitude-controlled composite → agentic dossiers → 6-agent audit → **hardened re-analysis** | Calibrated negative; 7 genes pass the strict multi-arm gate, none credible at FDR≥1 |
| **`th2-independent-replication/`** | From-scratch second pipeline; streaming, GATA3 alignment guardrail, matched Th1-vs-Th0 verification, permutation null | **Independently reaches the same negative** — agreement between two pipelines is the point |
| **`th2-ad-translation/`** (new) | Therapeutic translation *conditioned on the negative*: AD patient-skin validation (GSE147424), Open Targets + HPA druggability, off-axis (Dupixent) classification, integrated dossier | No candidate rescued; contributes the disease-relevance + druggability filters a target would additionally have to pass |

## Where the analyses converge (cross-pipeline agreement)

1. **The negative itself.** Two independently-built pipelines, different tooling and scoring, reach
   the same conclusion: the naive selective set is a threshold-soft artifact once Th1/Th2 reciprocity
   is scored correctly.
2. **GATA3 is a skewer, not selective.** Both the hardened re-analysis and the independent
   replication show GATA3 KD induces Th1 under the matched Th1-vs-Th0 arm. Calibration (GATA3 recovers
   as the strongest Th2-*lowering* gene) is real, but "lowers Th2" ≠ "selective."
3. **The same least-artifactual gene surfaces across pipelines.** The hardened 7-gene survivor set
   (BRPF1, DALRD3, GLIS2, RABEPK, RELL2, SLC30A5, UQCR11) and the translation track's top-lead set
   both surface **BRPF1** — the one gene common to the rigorous survivor list and the 16-candidate
   translation set. (Separately, **RELL2** appears both in the hardened survivors and in this
   session's broader residual-leaders ranking over all 33,983 rows — a weaker, different overlap, not
   part of the 16-gene translation candidate set.) Convergence on BRPF1 across independent scoring
   schemes is the most positive signal — and *even it does not clear the permutation FDR.*
4. **ARNT is the most mechanistically legible lead in every track, and "uncertain" in every track.**
   The HIF-2α→GATA3 circuit is real (Immunity 2024), but ARNT is a pleiotropic hub (obligate for
   HIF-1α, HIF-2α, and AHR), no source shows ARNT KD selectively lowering Th2, and the AHR arm
   predicts the opposite direction. Both the repo's ARNT dossier and the translation track land on the
   same downgraded "uncertain."

## The one sharp correction between the session and the repo

The therapeutic-translation work was built on an **Ota Th2-vs-Th1 arm split** (correlation +0.485),
under which GATA3 scored as a *selective* hit (genome rank 6, Th1 arm near-flat) and served as the
positive control anchoring the atlas. **That control was the wrong one.** The Th2-vs-Th1 contrast
entangles the Th1 reference with the Th2 axis, so a gene that skews toward Th1 can still read as
"Th1-flat." The repo's **matched Th1-vs-Th0 arm** — the correct, orthogonal control (and the original
project plan's "STEP 0") — dissolves the illusion: GATA3 KD drives Th1 to +2.8.

The session's own data hinted at this (GATA3's Th1 arm drifted to −0.17/−0.26 under stimulation, so
it was classed "rest-only selective"), but it never ran the matched-Th0 arm that settles it. **The
repo's result is correct and the translation track now carries this correction at the top of its
report.** This is the textbook value of running two independent pipelines: the second caught a control
the first got wrong.

## What the translation track adds (and its honest limits)

Conditioned on the negative, the translation track answers "*if* any candidate were real, would it be
a good AD drug target?" — three filters neither re-analysis track applied:

- **AD patient validation (GSE147424, AD lesional-skin scRNA-seq, 45,332 cells).** 15/16 candidates
  are significantly upregulated in AD lesional-skin T cells (FDR<0.05); GATA3/STAT6 controls behave;
  the signal is T-cell-specific. **This is necessary but not sufficient** — NDFIP2 has the *strongest*
  patient upregulation (log₂FC +1.88) yet the mechanism layer flags it a likely artifact (its Nedd4
  substrates are Th2-*positive*). Patient expression confirms disease-site presence; it does not
  establish causal selectivity. Note also the compartment mismatch: the screen was in *circulating*
  CD4, validation is in *skin* T cells.
- **Druggability (Open Targets + Human Protein Atlas).** All 16 candidates are intracellular →
  small-molecule programs; **0 antibody-tractable** (the surface-accessible axis is the one Dupixent
  already owns); 7 hard-to-drug (TF/chromatin/scaffold/E3); 2 already drugged (P4HB, SRD5A3). This
  annotation is track-independent and holds regardless of the negative.
- **Off-axis classification.** Separates Dupixent-competitive nodes (ARL1/RAB21/P4HB route through the
  autocrine IL-4→STAT6→GATA3 loop) from genuinely novel-mechanism candidates (ARNT/RBCK1/BRPF1). The
  commercially valuable targets, *were any real*, would be the off-axis ones.

## What would actually settle it (shared next step)

Every track converges on the same experiment, which no computational analysis can substitute for:
**CRISPRi-knock down the candidate in primary human CD4⁺ T cells under explicit Th2- vs
Th1-polarizing conditions**, read Th2 (GATA3/IL-4/IL-5/IL-13) vs Th1 (T-bet/IFNγ) by intracellular
flow + qPCR, **with a proliferation/viability control** to exclude the global-dampening artifact and a
**candidate + GATA3 epistasis** arm. Selectivity is a functional claim; this screen (single-perturbation,
non-polarized, transcriptomic) can nominate and triage, but cannot demonstrate it.

## Provenance

Data: Zhu R., Dann E. et al. (2025) bioRxiv 2025.12.23.696273; reference signature Ota M. et al.
(2021); AD patient data GSE147424 (He et al. 2020, *J Allergy Clin Immunol*). Full citations in the
top-level [`README.md`](./README.md) and each track's README.
