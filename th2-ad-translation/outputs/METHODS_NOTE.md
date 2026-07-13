# Selective Th2-suppressor atlas — methods note for the team

*Companion to the artifact set. Data: Zhu & Dann et al. 2025 genome-scale CRISPRi Perturb-seq
in primary human CD4⁺ T cells (Marson lab). Analysis object:
`GWCD4i.DE_stats.h5ad` (33,983 perturbation×condition rows × 10,282 genes).*

## The question, and why it isn't the paper's

The paper ranks regulators on a single bidirectional **Th2-vs-Th1** axis. On that axis a
knockdown that *deletes the Th2 program* and one that *drives cells toward Th1* both project
negative and are indistinguishable. We reframed the target as **selective Th2 suppression** —
Th2 program down **while Th1 stays flat** — which the 1-D axis structurally cannot express.
This is a genuinely different phenotype, not the same atlas with names filtered.

**Standing caveat (state it in any writeup):** these are Rest/Stim CD4⁺ T cells, *not*
polarized Th1/Th2. "Selective Th2 suppression" is a statement about a knockdown's
*transcriptional footprint* resembling selective loss of the Th2 program — a phenotypic
inference from a single-perturbation screen, not a functional polarization assay.

## Pipeline

1. **Two arms from the Ota-2021 Th2-vs-Th1 signature.** We reconstructed the teammate's
   `th2_arm` (Th2-up genes) and `th1_arm` (Th1-up genes) as a **log_fc-weighted mean z** over
   arm genes at adj-p < 0.05, recovering the reference arms at r = 0.942 (th2) / 0.967 (th1).
   `th2_arm` ≪ 0 = Th2 program down; `th1_arm` ≈ 0 = Th1 flat (positive = Th1 up).
2. **Separability gate (go/no-go).** corr(th2_arm, th1_arm) = **+0.485** across all
   perturbations — *positively* correlated, not the ≈ −0.9 mirror the bidirectional axis would
   imply. Interpretation: the dominant confound is **global magnitude / dampening**, not
   Th1-skewing; genuine Th1-skewers are rare (5 at the strict gate). Off-diagonal structure
   exists → the selective question is well-posed. (Figure: `separability_plane.png`.)
3. **Selective gate.** `th2_arm < −0.35 & |th1_arm| < 0.15` → **132 selective / 5 skewer**
   rows. A 3×3 threshold sweep tiers hits into core / confident / borderline
   (`selective_tiered.csv`).
4. **QC filters** (`selective_tiered.csv`): cross-donor reproducibility (donor_correlation ≥
   0.30), valid on-target knockdown (**ontarget_significant & effect_size < 0** — CRISPRi
   drives the target's *own* transcript down; using > 0 was a bug we caught and fixed),
   guide concordance, and exclusion of distal-off-target / neighboring-gene-KD rows.
   **45 QC-passing rows, 16 unique genes** (incl. GATA3, STAT6).
5. **Calibration (known-regulator recall).** Master Th2 TFs are the strongest genome-wide
   suppressors: **GATA3 rank 6/11,526 (0.043 pctile), STAT6 top 3.2%**; the 14 Th1 regulators
   have **0/14 false-recall** into the selective box. Effector cytokines / NuRD do *not*
   recover — consistent with partial CRISPRi in non-polarized cells (the paper's own caveat).
   (Figure: `recall_overlay.png`.)
6. **Per-condition split** (`condition_selectivity_matrix.csv`). 125 genes selective in ≥1
   condition, largely **condition-specific**: rest-only (49), stim-induced-48hr (41),
   stim-induced-8hr (28), constitutive (5), stim-induced-both-8hr-and-48hr (2). GATA3 is selective at Rest but drifts out of the
   flat band under stimulation (its ΔTh1 goes to −0.17/−0.26) — it stops being *selective*
   under stim, not being a suppressor.
7. **Magnitude-controlled composite score** (`real_vs_fp_shortlist.csv`). We regress `th2_arm`
   on the global-magnitude axes (`th1_arm`, mean |z|) and rank on the **residual**, which is
   decorrelated from the confound (r = **−0.0**). Composite = residual depth + Th1-flatness +
   donor + guide + KD, times artifact penalties (broad-DE, cell-cycle collapse, off-target,
   neighbor-KD, low-expression). GATA3 is among the deepest magnitude-controlled suppressors
   (3rd by mean residual, behind ARNT and the corepressor NCOR1); its mid-pack *combined*
   rank reflects averaged donor/guide subscores, not weak suppression. (Figure:
   `composite_volcano.png`.)
8. **Mechanism layer** (`mechanism_dossiers/`). Eight top novel QC-passing hits each got an
   independent agent-built, citation-verified dossier: molecular-function-grounded selectivity
   hypothesis, directness call, artifact scrutiny, and a confirming experiment. See
   `mechanism_dossiers/SYNTHESIS.md`.

## What to trust, what to check next

- **Trust the orientation and calibration.** GATA3/STAT6 recover; Th1 regulators never
  false-recall; the residual is genuinely decorrelated from the magnitude confound.
- **Treat the novel shortlist as hypotheses, ranked by confidence, not as hits.** All eight
  investigated candidates were called *indirect* with *some* artifact concern — the honest
  consequence of a strict conjunction on a single-perturbation, non-polarized screen. Two
  (NDFIP2, CBX5) the mechanism layer argues are likely false positives on prior biology.
- **The decisive next step is wet-lab and identical across hits:** CRISPRi-KD under
  Th2-polarizing conditions, read Th2 (GATA3/IL-4/5/13) vs Th1 (T-bet/IFNγ) with a
  proliferation/viability control, plus a candidate+GATA3 epistasis arm. This converts
  transcriptional-footprint selectivity into functional, ordered evidence.

## Reproducibility

Arms and all derived columns are in `arms.parquet` and `analysis_enriched.parquet`
(checkpoint). Annotation lists (Lambert-2018 TFs, curated known Th1/Th2 regulators) in
`annotations.json` / `lambert2018_TF.csv`. Only the 2.8 GB `zscore` layer of the 16.8 GB
h5ad was needed (contiguous uncompressed block, byte-exact range fetch).
