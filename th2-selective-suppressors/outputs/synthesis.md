# Selective Th2 Suppressor Atlas — synthesis

> **UPDATE (hardened re-analysis, supersedes the optimistic read below).** Running the review's
> recommended fixes changed the conclusion. (1) Competitive rank-based scoring collapses the arm
> correlation **+0.54 → +0.18** — most of the "global-magnitude confound" was a scoring artifact.
> (2) A permutation null shows the 2-arm selective set (420 under competitive scoring) is **not
> enriched over random gene sets** of the same size (expected ~526; empirical FDR ≈ 1.25) — genuine
> selective suppressors are no more common than chance, because Th1/Th2 are genuinely reciprocal.
> (3) **GATA3 fails**: with the matched Th1-vs-Th0 arm, GATA3 KD drives Th1 to +2.8 (a Th1-*skewer*,
> as canonical biology predicts); the earlier "top selective hit" was a mean-of-z + noisy-Ota-arm
> artifact. Only 7 genes pass the strict multi-arm + concordance gate and none are credible at FDR≥1.
> **Honest conclusion: the naive selective-suppressor atlas does not survive rigorous statistics.**
> The real deliverables are the calibrated negative result, the reproducible pipeline, and the
> agentic review/QC infrastructure. Next step before any claim: a functional IL-4/5/13 readout and a
> control-guide-based FDR. See `hardened_stats.json` / `notebooks/10_hardened.py`.



**Data:** Zhu & Dann et al. 2025 genome-scale CRISPRi Perturb-seq, primary human CD4+ T cells
(`GWCD4i.DE_stats.h5ad`, 33,983 perturbation×condition, streamed from the public Virtual Cells S3).
**Signature:** Ota et al. 2021 Th2-vs-Th1, split into a Th2-up arm (505 measured genes) and Th1-up arm (802).

## What we set out to do
Separate *selective Th2 suppressors* (KD lowers Th2, leaves Th1 flat — the allergy target) from
*Th1-skewers* (KD just flips the cell toward Th1). The paper's single bidirectional Th2−Th1 axis
cannot make this distinction; a two-arm 2D decomposition can.

## Results
1. **Reproduced the teammate's result from the authoritative matrix.** Arm correlation **+0.54** (their +0.49);
   the arms move *together*, so the dominant confound is global magnitude (sick-cell dampening), not skewing.
   The Th1 arm therefore doubles as a built-in control. Selective ≈127, true skewers ≈10 at the default gate.
2. **Calibration holds.** GATA3 (Th2 master regulator) is the #1 selective hit and #1 in the scored shortlist; RARA #2.
3. **The known-regulator list is directionally mixed — and the 2D method resolves it.** Th2 *activators*
   (GATA3, RARA, STAT6-trending) recover as suppressors; NuRD/chromatin *repressors* (MTA2, CHD4, SETDB1) and ICOS
   correctly appear as **Th1-inducers** (Th1 arm up), not suppressors. IL4/IL4R produce ~no transcriptional footprint.
   This is exactly the direction the 1D axis conflates.
4. **Context-dependence is the novel cut.** Of selective hits, ~60 act only at Rest and ~49 only under stimulation;
   even GATA3 is selective at Rest/Stim8hr but not Stim48hr. The paper's per-condition 1D coefficients cannot
   express this as *selectivity*.
5. **Two false-positive sources handled honestly.** A hard KD-confirmed + real-footprint (≥10 DE genes) gate
   (Haltavey's "did it actually knock down?" concern) plus magnitude-controlled selectivity (regress Th2 arm on the
   Th1 arm) collapsed 127 noisy hits to **21 high-confidence genes**.

## The agentic mechanism layer is the differentiator
For the top 10 novel candidates, an investigator agent (web research) proposed a mechanistic route to the Th2
program bypassing T-bet + a confirming experiment; a skeptic agent adversarially verified citations and logic.
**Outcome:** after review, 0/10 survived as "plausible" — 4 uncertain, 2 unlikely, 4 likely-artifact. The only
non-artifact leads worth following up were **ARNT** and **ELAVL1** (real, still-unverified Th2 links). The rest of
the top-scored list (AHSA1, RAB21, SSR1, KDM2A, MPG…) are global-effect / housekeeping false positives that the
numeric score under-penalized. **The mechanism layer performs the triage the score cannot** — separating real Th2
biology from sick-cell artifacts, with every claim adversarially checked.

## Honest limitations
- Arm construction (unweighted signature mean) differs slightly from the teammate's; cross-check against their `.npy`.
- 21 high-confidence genes still contain artifacts; mechanistic triage narrows the real leads to ~2 of the top 10.
- Selectivity ≠ efficacy/safety; Th2 has protective roles (anti-helminth, barrier). This is transcriptomic screen
  evidence, not in-vivo.

## Artifacts produced
`arms.parquet` · `selective_tiered.csv` · `plane_plot.svg` · `recall_overlay.svg` ·
`condition_selectivity_matrix.csv` · `real_vs_fp_shortlist.csv` · `mechanism_dossiers/*.md` · live dashboard.
