# Mechanistic Dossier: ARNT (HIF-1β) as a candidate selective Th2 suppressor

**Screen summary (Zhu & Dann et al. 2025, CRISPRi Perturb-seq, primary human CD4+ T cells).**
Composite confidence 0.46; selective only in **Stim48hr** (1/3 conditions). Best th2_arm −0.559
(Th2 program down), th1_arm +0.016 (Th1 flat). th2_marker_z −1.34, th1_marker_z +0.07,
cellcycle_z +1.04, global_mag 1.78, on-target KD z −19.15, cross-donor r 0.868.

> **Caveat up front.** These are Rest/Stim CD4+ T cells, *not* polarized Th1/Th2 cells.
> "Selective Th2 suppression" means the KD's *transcriptional footprint* resembles selective loss
> of the Th2 program — a phenotypic inference from a single-perturbation screen, **not** a
> demonstrated mechanism and **not** a functional assay. Everything below is a testable
> hypothesis, not proven wiring.

## 1. Gene identity & molecular function
ARNT (aryl hydrocarbon receptor nuclear translocator; a.k.a. **HIF-1β**, Gene ID 405) is a
bHLH-PAS transcription factor. It is not a standalone effector: it is the **obligate common
dimerization partner** for the class-I bHLH-PAS proteins — AHR and the hypoxia-inducible factors
HIF-1α, HIF-2α (EPAS1) and HIF-3α [Bersten 2013]. ARNT is required for these complexes to bind
DNA and activate transcription; ARNT-deficient cells lose HIF-1 DNA binding and hypoxic induction
entirely [Wood 1996]. Knockdown removes the shared β-subunit of *all* AHR- and HIF-driven
transcription at once.

## 2. Selectivity hypothesis (Th2 down, Th1 flat)
**Proposed route:** ARNT loss → loss of functional HIF-2α complex → collapse of the HIF-2α–GATA3
circuit → Th2 effector program (GATA3/IL4/IL5/IL13) falls, while T-bet/IFNγ is untouched.

- **ARNT is obligate for HIF-2α transcriptional activity** — ESTABLISHED [Wood 1996; Bersten 2013].
- **A HIF-2α–GATA3 feedback circuit drives the Th2 effector program**; HIF2α deficiency impairs
  Th2 differentiation and alleviates asthmatic inflammation, and EPAS1 is itself a GATA3 target
  (feedback loop) — ESTABLISHED in mouse/human asthma & CRS [Zou 2024].
- **The Th1 axis does not depend on ARNT partners.** HIF-1α is a Th17/Treg metabolic checkpoint;
  its deletion does *not* alter Th1 (or Th2) differentiation, and T-bet/IFNγ has no known ARNT/HIF
  requirement — ESTABLISHED [Shi 2011]. So removing the shared β-subunit preferentially disables
  the HIF-2α→GATA3 Th2 branch and leaves the T-bet/Th1 branch intact — INFERRED, but grounded.

**Honest tension (INFERRED).** AHR — the other major ARNT partner — has been reported to *suppress*
Th2 when ligand-activated; losing AHR function should, if anything, *raise* Th2. The observed
net Th2-down therefore implies the HIF-2α arm dominates over the AHR arm in Stim48hr cells. This
is a real complication, not a clean single-arm story.

## 3. Directness call: **INDIRECT**
ARNT does not bind Th2 effector loci as an autonomous regulator. Its influence on the Th2 program
runs through an intermediate transcription factor it partners — HIF-2α — which in turn engages
GATA3. The molecular contact (ARNT↔HIF-2α) is direct, but the effect on IL4/IL5/IL13/GATA3 is
one relay removed. Directness = **indirect (via HIF-2α→GATA3)**.

## 4. Artifact scrutiny — verdict: SOME CONCERN
- **Proliferation collapse?** No. cellcycle_z is +1.04 (mildly positive), the opposite of a
  sick-cell / low-proliferation signature. Not a viability artifact.
- **Covert Th1-skewer?** No. th1_marker_z +0.07 and th1_arm +0.016 are flat — Th1 is not being
  pushed up, so the "selective" label is not masking a polarization switch.
- **Broad transcriptome shift?** The main flag. global_mag 1.78 is elevated — *biologically
  expected* for a pleiotropic bHLH-PAS hub (AHR + all HIF programs move at once), but broad
  magnitude is the dominant confound class. Mitigating: the selective score is
  residual-decorrelated from the global-magnitude axis, so the Th2-specific signal survives
  magnitude control, and th2_marker_z (−1.34) exceeds th1_marker_z — the drop is not uniform.
- **Robustness.** Strong on-target KD (z −19.15) and high cross-donor reproducibility (r 0.868)
  argue against noise, **but** selectivity appears in only 1/3 conditions and composite is modest
  (0.46). Verdict: **some concern** — not clean (pleiotropic hub, single condition), not likely
  an artifact (no proliferation/Th1 signature; magnitude-controlled).

## 5. Confirming experiment (tests the SELECTIVITY claim)
In naive human CD4+ T cells, CRISPRi-knock down ARNT vs non-targeting control and differentiate in
parallel under **Th2-polarizing** (anti-CD3/CD28 + IL-4 + anti-IFNγ) and **Th1-polarizing**
(IL-12 + anti-IL-4) conditions. **Readout:** intracellular GATA3, IL-4, IL-5, IL-13 (Th2) vs
T-bet, IFN-γ (Th1) by flow, plus RT-qPCR. **Expected if the hypothesis is true:** ARNT KD lowers
GATA3/IL4/IL5/IL13 under Th2 conditions while T-bet/IFN-γ under Th1 conditions is unchanged.
**Epistasis to test the HIF-2α route:** co-knock down ARNT + EPAS1 (HIF-2α); if ARNT acts through
HIF-2α, the double KD is *no worse* than EPAS1 KD alone (epistatic), and re-expressing HIF-2α
cannot rescue Th2 output in ARNT-null cells.

## 6. Citations (verified)
1. **Wood SM et al.** *J Biol Chem* 1996;271(25):15117–23. **PMID 8662957**; DOI 10.1074/jbc.271.25.15117.
   — ARNT/HIF-1β is essential for HIF-1 DNA binding and hypoxic transcription.
2. **Bersten DC et al.** "bHLH-PAS proteins in cancer." *Nat Rev Cancer* 2013;13(12):827–41.
   DOI 10.1038/nrc3621. — ARNT as common dimerization partner for AHR and HIF-α.
3. **Zou et al.** *Immunity* 2024;57(12):2808–2826.e6. **PMID 39609127**;
   DOI 10.1016/j.immuni.2024.10.011. — HIF2α–GATA3 circuit; HIF2α deficiency impairs Th2 and
   alleviates asthma; EPAS1 is a GATA3 target.
4. **Shi LZ et al.** *J Exp Med* 2011;208(7):1367–76. **PMID 21708926**; DOI 10.1084/jem.20110278.
   — HIF-1α is a Th17/Treg metabolic checkpoint; HIF-1α deficiency does not alter Th1 or Th2.

*Verification pass:* each citation was checked against web_search results this session. All four
resolve to real, indexed papers whose titles/topics match the claim attached (Wood — ARNT
essential for HIF-1 DNA binding; Bersten — bHLH-PAS review naming ARNT the common partner; Zou —
HIF-2α/Th2/GATA3 in asthma; Shi — HIF-1α as Th17/Treg checkpoint sparing Th1/Th2). Verification
here means existence + title/abstract-level topical match via search snippets, not full-text
reading of every result. The AHR→Th2-suppression "tension" in §2 is stated qualitatively, labeled
INFERRED, and pinned to no single PMID; no claim depends on an unverified source.
