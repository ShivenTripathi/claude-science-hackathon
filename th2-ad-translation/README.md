# Th2 selective-suppressor → atopic-dermatitis target translation

The **therapeutic-translation** layer on top of the selective Th2-suppressor re-analysis. Following a
pharma researcher's brief, it asks: *if* a selective Th2 suppressor were real, would it be a good
**atopic dermatitis (AD)** drug target — off the crowded IL-4Rα/STAT6 (Dupixent) axis, present in
patient tissue, and druggable?

> **Read [`../RECONCILIATION.md`](../RECONCILIATION.md) first.** The two re-analysis tracks in this
> repo establish a **calibrated negative**: single-gene selective Th2 suppression does not survive
> proper statistics (permutation FDR ≈ 1), and GATA3 is a Th1-skewer under the matched Th1-vs-Th0 arm.
> **This track does not overturn that.** Its filters (patient expression, druggability, off-axis
> class) are *conditioned on* the negative — they describe the additional bar a candidate would face
> *if* it ever cleared a functional selectivity test. The druggability and off-axis annotations are
> track-independent and hold regardless.

## What this track adds (three filters neither re-analysis applied)

1. **AD patient validation, two compartments.**
   - *Primary — lesional skin* (**GSE147424**, He et al. 2020; 45,332 cells): 15/16 candidates
     significantly upregulated in AD lesional-skin T cells (FDR<0.05); GATA3/STAT6 controls behave;
     signal is T-cell-specific. **Necessary but not sufficient** — NDFIP2 has the strongest patient
     upregulation yet is a likely artifact; expression ≠ causal selectivity.
   - *Secondary — circulating blood CD4, the screen-matched compartment* (**GSE189188**, 6 AD / 5 HC
     PBMC scRNA-seq, 15,446 CD4⁺ T cells; patient-level pseudobulk as the honest primary test). Only
     **4 genes replicate**: GATA3, STAT6 (controls), **RBCK1** (pb log₂FC +0.52, padj 1.6×10⁻⁴), and
     P4HB. Crucially, of the novel-mechanism leads **only RBCK1 is concordant across both skin and
     blood** — **ARNT and BRPF1 are skin-restricted** (blood ns). The two-compartment split is itself
     a useful triage: cross-compartment concordance is a higher bar than either alone.
2. **Druggability** — Open Targets tractability + Human Protein Atlas subcellular location per
   candidate. All 16 are intracellular → small-molecule; 0 antibody-tractable; 7 hard-to-drug; 2
   already drugged (P4HB, SRD5A3).
3. **Off-axis classification** — separates Dupixent-competitive nodes (ARL1/RAB21/P4HB route through
   the autocrine IL-4→STAT6→GATA3 loop) from novel-mechanism candidates (ARNT/RBCK1/BRPF1).

## Key outputs (`outputs/`)

- `AD_TARGET_REPORT.md` — integrated report (carries the negative-result banner at the top).
- `ad_target_dossier.csv` — 16 candidates × integrated columns: composite/selectivity, off-axis
  class, druggability/modality, AD patient T-cell expression, mechanism verdict, therapeutic-priority
  rank.
- `druggability_matrix.csv` — Open Targets tractability + HPA location + known drugs + AD association.
- `off_axis_ranking.csv` — mechanism-axis classification vs the Dupixent axis.
- `patient_ad_expression.csv` + `patient_validation.png` — GSE147424 lesional-skin vs-healthy T-cell
  expression per candidate.
- `patient_ad_blood_expression.csv` + `patient_validation_blood.png` — GSE189188 AD-blood-vs-HC CD4
  expression (single-cell + patient-level pseudobulk); the screen-matched secondary validation.
- `mechanism_dossiers/*.md` — 8 per-candidate agentic dossiers (investigate → adversarial verify),
  each flagging its own likely-false-positive concerns.
- `METHODS_NOTE.md` — the pipeline methods note for the selective-suppressor stage that fed this.

## Honest limitations

Selectivity is a functional claim this screen cannot make (single-perturbation, non-polarized,
transcriptomic). Patient validation is in *skin* T cells while the screen was in *circulating* CD4
(compartment mismatch — directional, not exact). Patient expression is disease-site presence, not
proof of causal target. Before any target claim: a functional IL-4/5/13 vs IFNγ readout under
polarization, with a proliferation/viability control and a control-guide FDR.

Data provenance and citations in the [top-level README](../README.md).
