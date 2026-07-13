> ⚠️ **READ [`../../RECONCILIATION.md`](../../RECONCILIATION.md) FIRST.** This report was written
> under the optimistic (Ota Th2-vs-Th1 arm) framing, in which candidates read as *selective*
> suppressors. The hardened re-analysis and the independent replication in this repo show that
> **single-gene selective Th2 suppression does not survive proper statistics** (permutation FDR ≈ 1),
> and that **GATA3 is a Th1-skewer under the matched Th1-vs-Th0 arm** — so the "defensible leads"
> below are *not* validated targets. They are the least-artifactual candidates *conditioned on* a
> premise the rigorous analysis rejects. What holds up here independently of the negative is the
> **druggability annotation**, the **off-axis (Dupixent-competitive) classification**, and the
> observation that these genes are **present/upregulated in AD patient skin** — the additional filters
> a target would have to pass *if* it ever cleared a functional selectivity test. Treat this as the
> translational-filter layer, not a target list.

# Off-axis, patient-validated drug targets for atopic dermatitis

**From a genome-scale CD4⁺ T-cell Perturb-seq screen to AD-specific, non-IL-4R/STAT6, patient-corroborated, druggable targets.**

This analysis follows a specific brief from a pharma researcher, applied on top of the project's
existing 626 selective Th2-suppressor atlas and its druggability layer:

1. **Focus on one disease — atopic dermatitis (AD)** — where Th2 cells are most central to pathogenesis.
2. **Go off the IL-4Rα–STAT6 axis.** Dupilumab (anti-IL-4Rα) made that pathway the crowded
   center of AD drug development; the valuable target is a *novel* selective Th2 suppressor
   **outside** IL-4R/STAT6.
3. **Validate in patient tissue.** Confirm each candidate is actually **upregulated in AD patient
   skin, T-cell-resolved**, using single-cell transcriptomes of patient samples.
4. **Keep druggability first-class** — membrane→antibody, intracellular→small molecule, graded
   from Open Targets.

The result is a four-axis convergence: **transcriptional selectivity (screen) × off-axis novelty
× AD-specific human genetics × patient single-cell upregulation × druggability.**

---

## What was done

**Off-axis classification (STRING v12, high-confidence ≥700).** Each of the 626 selective
suppressors was tested for membership in the IL-4Rα–STAT6 axis — the six core genes
(IL4, IL13, IL4R, IL13RA1, IL13RA2, STAT6), the shared JAK signalling module, and their
high-confidence STRING interactors. **603 are off-axis; 23 are on-axis** (STAT6 itself plus 13
IL-4R/STAT6 interactors — including IL5RA, ICAM1, CTLA4, STAT1, OSMR — and 9 JAK interactors).
The on-axis set is set aside as "dupilumab-adjacent"; everything downstream operates on the
off-axis space.

**AD-specific genetics.** The earlier atopy genetics (asthma-dominated) were re-queried against
AD-specific EFO terms (atopic eczema, dermatitis, atopic-IgE). This re-ranks the genetic evidence
toward the disease of interest — notably **STAT6 drops from 0.75 (asthma) to 0.32 (AD)**, while
eczema loci (IL18RAP, IL1RL1, ARRDC1, PRORP, REL, KIF3A, OVOL1, NR4A3) rise. 14 targets carry
AD genetic-association ≥ 0.3.

**Patient single-cell validation.** Candidate expression was measured in the **CELLxGENE Atopic
Dermatitis Atlas** (Nat Commun 2026; DOI 10.1038/s41467-026-69587-7; dataset
`b0ef440b-e303-4ad2-ada8-ce13336280ba`) — 280,518 skin cells spanning **Lesional (122,826) /
Non-lesional (97,947) / Healthy (59,745)**, with a resolved **T/NK compartment (25,831 cells)**.
For each candidate we computed mean log-normalized expression and fraction expressing per disease
group, in T cells and across all cells, and the **lesional-vs-healthy log₂ fold-change**.

**Positive-control check.** The canonical Th2/dupilumab-axis genes behave exactly as expected in
patient T cells — **IL13 (log₂FC +3.7)** and **IL4R (+1.3)** are among the most strongly
lesional-upregulated genes measured — confirming the readout is disease- and cell-type-honest
before it is used to judge the novel candidates.

![Patient validation dotplot]({{artifact:art_5c5221ac-517d-4e89-8412-d5364735a4d9}})

*T-cell expression of the off-axis leads across AD lesion status (dot size = % expressing, colour
= mean log-norm expression). Purple bold = fully-convergent leads; grey = IL-4R/STAT6-axis
positive controls (IL13, IL4R, STAT6), which rise toward lesional as expected.*

---

## Headline result

**Of the 603 off-axis selective Th2 suppressors, 342 are pharmacologically tractable and 75 are
upregulated in AD-patient lesional T cells; 72 satisfy all of off-axis + patient-upregulated +
tractable + selective simultaneously.**

Three targets are **fully convergent** — off-axis, upregulated in patient T cells, transcriptionally
selective, *and* sitting on an AD genetic-association locus (≥0.3):

| Target | Biology | Modality | AD genetics | Patient T-cell log₂FC | Selectivity |
|--------|---------|----------|-------------|----------------------|-------------|
| **NR4A3** | orphan nuclear receptor (NR4A TF family) | small molecule | 0.35 | **+0.99** (up) | 0.63 |
| **MAP3K14 / NIK** | NF-κB-inducing kinase (non-canonical NF-κB) | small molecule | 0.35 | **+0.78** (up) | 0.57 |
| **PTPA / PPP2R4** | PP2A phosphatase activator | small molecule | 0.37 | **+0.59** (up) | 0.57 |

All three are **small-molecule-tractable, undrugged, off the IL-4R/STAT6 axis, and genetically tied
to AD** — precisely the profile the brief asked for. NR4A3 is the strongest: an orphan nuclear
receptor (a ligand-binding fold, i.e. a real small-molecule target class) that is a NR4A-family
TF, carries an AD eczema-locus association, and is the most strongly lesional-upregulated of the
three in patient T cells.

![Off-axis druggability vs patient upregulation]({{artifact:art_a8216a4a-239f-4a12-8496-a33c56575185}})

*Every off-axis target with real patient detection, placed by patient upregulation (x) against
druggability (y); size = AD genetics, purple ring = AD GWAS ≥ 0.3. The decision corner
(upper-right) holds targets that are both up in patient lesions and tractable.*

---

## The off-axis, patient-validated shortlist

Beyond the three convergent hits, the shortlist (`ad_offaxis_lead_shortlist.csv`, 72 targets)
groups the off-axis, patient-upregulated, tractable, selective leads. The biologically legible
ones — transcription factors, kinases, chromatin/RNA regulators, and immune/surface proteins —
are the most credible new-target stories:

- **Transcription factors:** NR4A3, SREBF2, LDB1, GTF2A1 — small-molecule or degrader space.
- **Kinases:** MAP3K14/NIK, MAPKAPK2 — classic small-molecule inhibitor targets, both up in
  patient T cells.
- **Chromatin / RNA regulators:** RCOR1 (CoREST), L3MBTL3, BRD7, BRD9, SSBP4, YTHDF2 — the
  bromodomain and CoREST members are actively pursued by degrader/inhibitor chemistry.
- **Immune / surface:** TNFRSF9 (4-1BB/CD137, antibody-accessible, strongly lesional-up +1.8),
  ADA (adenosine deaminase, approved-drug precedent).

![Off-axis patient-validated shortlist]({{artifact:art_aac9dc5a-64e5-4cf1-9b30-7ebf375675fc}})

*Novelty-forward AD lead score for the legible off-axis, patient-validated shortlist. ↑ = T-cell
log₂FC (lesional/healthy); tags mark AD-GWAS, clinical-stage drug precedent, and
knockdown-mimicking pharmacology. Purple bold = fully-convergent leads.*

---

## Positioning against dupilumab and the IL-4R/STAT6 field

Dupilumab (anti-IL-4Rα) and the wave of programs it triggered — anti-IL-13, anti-TSLP, JAK
inhibitors, and emerging **STAT6** degraders — all act on the cytokine-sensing and
signal-transduction spine of type-2 immunity. This analysis deliberately **removes that spine**
(the 23 on-axis genes, STAT6 included) and asks what selective Th2-suppressing biology remains
that is *also* elevated in real patient lesions. The answer is a set of **intracellular
regulators** — an orphan nuclear receptor (NR4A3), a non-canonical NF-κB kinase (NIK/MAP3K14),
a PP2A activator (PTPA), and chromatin machinery (CoREST, BRD7/9) — that a cytokine-blocking
antibody cannot reach and that degrader / small-molecule chemistry is increasingly able to.
This is the complementary target class to dupilumab, not a competitor within its pathway.

---

## Method — the AD-target score

`ad_target_score = (0.24·tractability + 0.20·patient_upregulation + 0.16·AD_genetics
+ 0.16·selectivity + 0.12·drug_precedent + 0.12·off_axis) × (1 − 0.4·safety_penalty)`

with each component in [0,1]. The **patient-upregulation** component is the T-cell lesional-vs-
healthy log₂FC (all-cell fallback, discounted, when a gene is undetected in T cells), saturating at
3 log₂FC. The **off-axis** component rewards distance from the IL-4R/STAT6 spine. For the headline
*shortlist* a novelty-forward score is used instead, which up-weights patient upregulation and
selectivity and does **not** reward off-indication drug precedent — so that an approved oncology
inhibitor does not outrank a genuinely novel, AD-relevant target. Convergence into decision tiers
is a rule-based overlay (off-axis + patient-up + tractable + selective + [genetics or KD-mimicking
drug]).

---

## Caveats (first-class)

- **Expression corroborates, it does not prove direction.** A gene being *up* in lesional T cells
  is consistent with — but does not establish — that *suppressing* it would help. Direction of
  effect needs the functional and genetic (colocalization / eQTL-sign) follow-up.
- **Low baseline fractions.** Several leads are expressed in only 3–6% of lesional T cells, so a
  large fold-change sits on a low baseline; the shortlist carries a fraction-expressing robustness
  flag, and genes undetected in the dataset (e.g. IL18RAP in T cells) were excluded from the
  patient axis rather than plotted at noisy extreme fold-changes.
- **Transcriptional, not functional (inherited).** The selectivity is a transcriptional footprint
  in Rest/Stim CD4⁺ T cells, not a polarized-Th2 differentiation assay.
- **One patient dataset.** Validation rests on a single (large, well-annotated) AD atlas;
  replication in an independent AD cohort would harden the calls.
- **Off-axis by STRING topology.** "Off-axis" means no high-confidence STRING edge to the core
  axis; a gene could still act on the pathway through an interaction STRING does not capture.
- **Housekeeping confound in the raw shortlist.** Some high-scoring off-axis, patient-up genes are
  broadly-expressed metabolic/ribosomal genes; these are down-weighted in the report's legible
  shortlist but remain visible in the atlas for transparency.

---

## Files

- `ad_offaxis_target_atlas.csv` — all 626 selective suppressors × 37 columns: off-axis classification,
  AD-specific genetics, per-modality druggability + existing drugs, patient T-cell and all-cell
  lesional/non-lesional/healthy expression + log₂FC + upregulation call, the six score components,
  and the final AD-target score.
- `ad_offaxis_lead_shortlist.csv` — 72 off-axis, patient-upregulated, tractable, selective leads.
- `ad_patient_validation.csv` — per-gene patient expression statistics (mean, fraction, fold-change)
  in T cells and all cells, with dataset provenance.
- `figA_patient_validation_dotplot.png`, `figB_offaxis_druggability_patient.png`,
  `figC_ad_shortlist.png`.
