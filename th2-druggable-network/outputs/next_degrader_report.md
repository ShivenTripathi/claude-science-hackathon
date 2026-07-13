# The druggable intracellular type-2 network beyond STAT6

**A functional-genomics × chemical-tractability map for atopic dermatitis, patient-anchored.**

## The idea

STAT6 was recently degraded orally with biologic-like efficacy in atopic dermatitis (AD), proving
that an intracellular master regulator of the type-2 program can be drugged. Most Perturb-seq target
work stops at "which knockout shifts the phenotype." This analysis fuses functional genomics with
chemical tractability *inside a single ranking*: score every genome-wide perturbation for how well it
**phenocopies the STAT6/GATA3 collapse** of the type-2 program, then weight each node by whether it
is a real degrader/small-molecule handle, whether it fires only in activated cells (sparing resting
immunity), whether it has AD/allergy human-genetic support, and whether it is upregulated in AD
patient skin. The output is a *map of the druggable intracellular type-2 network beyond the
IL4R–STAT6 axis*, plus a reusable Th2-collapse scorer.

## Why anchor on STAT6/GATA3 (and why this calibrates where the naive atlas did not)

Our earlier "selective Th2 suppressor" atlas reached a calibrated negative: a naive "Th2 down & Th1
flat" residual is dominated by low-power noise and is not enriched over random gene sets (FDR ~ 1).
The fix is to anchor on a **positive** signal. GATA3 and STAT6 have a measurable trans-transcriptome
footprint (GATA3 tops the effector-marker readout), so scoring who else reproduces their collapse
direction is a positively-anchored classifier. On the informative program genes (those the two
anchors concordantly move; ~2,500 per condition) the anchors agree at r = +0.63 (vs ~ -0.1
genome-wide). The scorer calibrates:

- **Anchors self-recover**: GATA3 ranks #1 in all three conditions, STAT6 #2, and IL4R — deliberately
  held out of the signature definition — phenocopies increasingly with stimulation
  (0.12 -> 0.40 -> 0.61 across Rest -> Stim8hr -> Stim48hr), recovering the known upstream axis
  out-of-sample.
- **Permutation null**: the top non-anchor scores (0.42-0.49) sit far beyond a shuffled-weight null
  (95th percentile ~ 0.04; p < 0.001).
- **Known-regulator recovery**: canonical type-2 regulators concentrate at the top (median 87th
  percentile vs 50th for the pool; recall@10 = 0.38).

This is the opposite of the naive atlas's recall@250 = 0.00. Anchoring fixed the calibration.

## The map

We scored 3,386 well-powered perturbations (ontarget-significant, >=50 DE genes) per condition and
annotated the top 60 non-anchor nodes with Open Targets tractability, GWAS Catalog support,
stimulation-specificity, and AD patient expression. Of 63 nodes, **61 are off the IL4R–STAT6 axis**,
32 carry a small-molecule/degrader/ligandable-pocket handle, 57 are stimulation-specific, 10 have
AD/atopy/allergy GWAS support, and 26 are upregulated in AD lesional T cells. **Twelve nodes are
simultaneously off-axis, druggable, and patient-upregulated.**

### Headline off-axis candidates

| gene | collapse | stim class | tractability | AD/allergy GWAS | AD lesional T-cell logFC |
|---|---|---|---|---|---|
| **ITK** | 0.39 | stim-only | approved-drug small molecule | yes (AD, asthma, eczema) | +0.14 |
| **INPP5D (SHIP1)** | 0.35 | stim-only | advanced-clinical small molecule | yes (allergic disease, AD, eczema) | -0.22 |
| **KDM8 (JMJD5)** | 0.37 | stim-only | ligandable pocket (structure w/ ligand) | - | +2.30 |
| **UBA5** | 0.37 | activation-gated | ligandable pocket (structure w/ ligand) | - | +0.83 |
| **MYB** | 0.48 | constitutive | ligandable pocket (high-quality ligand) | yes (serum IgE) | +0.35 |
| **DOHH** | 0.33 | activation-gated | ligandable pocket | - | +0.75 |
| **NFKB2** | 0.35 | activation-gated | approved-drug small molecule | - | +0.17 |

**ITK** and **INPP5D/SHIP1** are the standouts: proximal TCR-signaling nodes with existing chemical
matter *and* independent AD/allergy genetic support, entirely off the cytokine-receptor axis that
Dupixent and the JAK inhibitors already crowd. ITK inhibitors are clinical-stage; SHIP1 modulators
are in advanced development. Both fire specifically in stimulated cells — the property seisei asked
for (spare resting immunity). **KDM8, UBA5, and DOHH** are enzyme nodes (a histone demethylase, a
UFM1-activating enzyme, and a deoxyhypusine hydroxylase) with ligandable pockets and the strongest
patient-lesional upregulation — under-explored, mechanistically legible degrader/inhibitor handles.

### A coherent under-explored module: UFMylation

Four members of the UFMylation pathway (DDRGK1, UBA5, UFL1, UFM1) phenocopy the collapse and are
activation-gated. Patient anchoring is partial and honest here: **DDRGK1 (+0.70) and UBA5 (+0.83)
are up in AD lesional T cells, but UFL1 (-0.01) and UFM1 (-0.08) are flat** — the ligase/adaptor arm
trends up while the modifier does not, so the module does not co-move coherently in patients. It is a
hypothesis to test, not a validated module.

## Caveats (carried throughout, not buried)

1. **Un-polarized cells.** The screen is Rest/Stim CD4s, not polarized Th2. The collapse score is a
   *transcriptional-footprint resemblance* to the STAT6/GATA3 collapse, not a functional type-2
   differentiation assay.
2. **The collapse score is activation-coupled.** It captures the anchors' whole footprint, which is
   heavily TCR/activation-linked; it correlates only weakly with cytokine-specific effector
   suppression (Spearman -0.14 to -0.19 in Stim). That is why the top ranks are populated by TCR
   signalosome nodes — a real feature of anchor biology, but broader than "cytokine-specific."
3. **Patient significance is nominal, not adjusted-significant.** In GSE147424 (AD skin scRNA-seq,
   T-cell compartment, 4 lesional vs 11 control pseudobulk samples) most candidate log-fold-changes
   are positive but do not survive multiple-testing correction — the cohort is small and the T-cell
   compartment sparsely sampled. Patient upregulation is *supporting evidence of direction*, not
   confirmation.
4. **Tractability is a database call, not a medicinal-chemistry verdict.** Open Targets PROTAC/
   pocket flags indicate a *handle exists*, not that a degrader is feasible.
5. **Single-perturbation screen.** Mechanism ordering (does node X act through GATA3?) is inferred,
   not measured; the confirming experiment for each hit is a double-perturbation epistasis test.

## Deliverables

- `th2_collapse_scores.csv` - every well-powered perturbation scored for STAT6/GATA3 phenocopy, per condition.
- `th2_collapse_scorer.py` - reusable, documented scorer (`build_signature` / `collapse_score` / `score_many`).
- `druggable_type2_network.csv` - the ranked map: collapse + tractability + stim-specificity + GWAS + patient, with an off-axis flag and a transparent composite confidence.
- `AD_patient_validation.csv` - candidate expression in AD lesional vs control skin (GSE147424).
- `next_degrader_network.png` - the druggability x collapse map and the patient-anchoring panel.

## Bottom line

Anchoring on the STAT6/GATA3 collapse turns a mis-calibrated selectivity residual into a positively
validated classifier, and layering chemical tractability + patient genetics + AD-skin expression onto
that ranking surfaces a druggable intracellular type-2 network beyond the IL4R–STAT6 axis. **ITK and
INPP5D/SHIP1** are the most immediately actionable off-axis nodes (existing chemical matter + AD
genetics + activation-gated firing); **KDM8, UBA5, and DOHH** are the strongest under-explored enzyme
handles with patient-lesional upregulation. All of it is transcriptional-footprint evidence in
un-polarized cells — the next step is a functional IL-4/5/13 readout in polarized Th2 plus a
double-perturbation epistasis test against GATA3.
