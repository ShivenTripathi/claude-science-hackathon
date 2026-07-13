# Mechanistic Dossier — RBCK1 (HOIL-1L)

**Screen call:** selective Th2 suppressor, Stim48hr only. composite 0.621 · best_th2_arm −0.375 · th1_arm_at_best +0.059 · on-target KD z −5.76 · donor corr 0.834 · th2_marker_z −1.27 · th1_marker_z −0.79 · cellcycle_z +0.87 · global_mag 1.11.

> **Framing caveat (must be stated).** These are Rest/Stim CD4⁺ T cells, not polarized Th1/Th2 cells. "Selective Th2 suppression" here means the KD's *transcriptional footprint* resembles selective loss of the Th2 program — a phenotypic inference from a single-perturbation screen, **not** a functional polarization assay and **not** a demonstrated pathway.

## 1. Gene identity & molecular function
RBCK1 (a.k.a. HOIL-1/HOIL-1L, RNF54) has two documented activities, explaining the TF;E3/ubiquitin tag. (i) It is the accessory subunit of the **linear ubiquitin chain assembly complex (LUBAC)** with catalytic HOIP/RNF31 and SHARPIN; LUBAC is the only ligase making Met1-linked ubiquitin and potentiates canonical NF-κB by linearly ubiquitinating NEMO and the CARD11–BCL10–MALT1 (CBM) hub [1,2]. (ii) It was first cloned as a PKC-interacting RING-B-box-coiled-coil protein with intrinsic **DNA-binding and transcriptional-activator** activity requiring its RING and B-box motifs [3,4]. In T cells it is itself a MALT1 substrate [5].

## 2. Selectivity hypothesis (Th2 down, Th1 flat)
Proposed route: **RBCK1 → LUBAC-supported canonical NF-κB → p50(NF-κB1)-dependent GATA3/IL-4 induction → Th2 program.**
- RBCK1 is required for LUBAC assembly/linear-ubiquitin output → NF-κB. *ESTABLISHED* [1,2,6].
- The **p50 arm of NF-κB is selectively required for GATA3 and IL-4/IL-5/IL-13**: p50⁻/⁻ CD4⁺ T cells fail to induce GATA3 under Th2 conditions but retain normal T-bet and IFN-γ under Th1 conditions [7]. Conversely, the c-Rel subunit is required for Th1/Th17-driven autoimmune inflammation (EAE), whereas p50-deficiency selectively blocks Th2 [7,8]. This establishes that different NF-κB subunits act lineage-selectively — the crux that makes "Th2 down while Th1 flat" mechanistically conceivable. *ESTABLISHED* [7,8].
- That RBCK1 KD preferentially dials down the p50/GATA3 arm (rather than NF-κB globally) is *INFERRED* and unproven.

Th1 stays flat because IFN-γ/T-bet lean on RelA/c-Rel + STAT4 and on APC-derived cytokines, a branch not selectively dependent on the p50→GATA3 input [7,8]. *INFERRED.*

## 3. Directness call — **INDIRECT**
No established data place RBCK1 at the GATA3 or IL4/5/13 loci. Its plausible reach into the Th2 program runs through a signaling intermediate (LUBAC→NF-κB→GATA3 induction) and possibly its coactivator role (CBP/PML interaction) [4]. Its intrinsic TF activity does not target known Th2 machinery. The effect is therefore an inferred indirect (signaling-level) consequence, not a direct action on Th2 transcription.

## 4. Artifact scrutiny — **SOME CONCERN**
- **Proliferation collapse:** excluded. cellcycle_z = +0.87 (cell-cycle genes not depressed).
- **Covert Th1-skewer:** excluded. th1_marker_z = −0.79 and th1_arm = +0.059 — Th1 is flat-to-slightly-down, never rising.
- **General activation/survival dampening:** *this is the real concern.* global_mag = 1.11 (elevated broad shift), and LUBAC is an established pro-survival/pro-activation module — LUBAC ligase-dead CD4⁺ T cells fail IκBα phosphorylation and die faster [6]. So part of "Th2 down" could be a broad effector dampening. Mitigating: the score is magnitude-controlled (residual decorrelated from the global axis); |th2_marker_z| (1.27) exceeds |th1_marker_z| (0.79); KD is strong (z −5.76) and reproducible (donor corr 0.834). Weakening: the Th2-minus-Th1 margin is modest, and it is selective in only **one** condition (Stim48hr, n_cond=1). **Big skeptical flag:** a 2025 study reports LUBAC is *largely dispensable* for TCR-induced NF-κB in **human** CD4⁺ T cells [5], directly undercutting the proposed NF-κB route. Verdict: plausible but not clean — medium confidence.

## 5. Confirming experiment (tests the *selectivity* claim)
CRISPRi-KD RBCK1 vs safe-harbor control in naive human CD4⁺ T cells cultured under Th2-polarizing conditions (anti-CD3/CD28 + IL-4 + anti-IL-12). **Readouts:** GATA3 and IL-4/IL-5/IL-13 (Th2) vs T-bet/IFN-γ (Th1) by intracellular staining/qPCR; plus viability/proliferation (CellTrace dilution, Annexin V) to exclude a survival artifact; plus an NF-κB nuclear-translocation/reporter readout. **Expected if hypothesis true:** GATA3 + IL-4/5/13 fall, T-bet/IFN-γ unchanged, viability roughly preserved. **Epistasis arm:** RBCK1 KD + enforced GATA3 re-expression — if GATA3 rescues the Th2 defect, RBCK1 acts upstream of GATA3 (consistent with the NF-κB→GATA3 route).

## 6. Citations (all verified)
1. Spit M, Rieser E, Walczak H. Linear ubiquitination at a glance. *J Cell Sci* 2019;132(2):jcs208512. PMID 30659056 · DOI 10.1242/jcs.208512.
2. Oikawa D, Hatanaka N, Suzuki T, Tokunaga F. Cellular and mathematical analyses of LUBAC involvement in TCR-mediated NF-κB activation pathway. *Front Immunol* 2020;11:601926. PMID 33329596 · PMC7732508 · DOI 10.3389/fimmu.2020.601926.
3. Tatematsu K et al. Transcriptional activity of RBCK1: requirement of RING-finger and B-box motifs. *Biochem Biophys Res Commun* 1998;247:392-6. PMID 9642138 · DOI 10.1006/bbrc.1998.8795.
4. Tokunaga C et al. Molecular cloning of a novel PKC-interacting protein with RBCC motifs (RBCK1). *Biochem Biophys Res Commun* 1998;244:353-9. PMID 9514928 · DOI 10.1006/bbrc.1998.8270.
5. Graß C et al. LUBAC modulates CBM complex functions downstream of TRAF6 in T cells. *Nat Commun* 2025. PMC12602705 · DOI 10.1038/s41467-025-65879-6.
6. Okamura K et al. Survival of mature T cells depends on signaling through HOIP. *Sci Rep* 2016;6:36135. PMID 27786304 · PMC5081559 · DOI 10.1038/srep36135.
7. Das J, Chen CH, Yang L, Cohn L, Ray P, Ray A. A critical role for NF-κB in Gata3 expression and TH2 differentiation in allergic airway inflammation. *Nat Immunol* 2001;2(1):45-50. PMID 11135577 · DOI 10.1038/83158.
8. Hilliard BA et al. Critical roles of c-Rel in autoimmune inflammation and helper T cell differentiation. *J Clin Invest* 2002;110:843-50. DOI 10.1172/JCI15254.

*Verification pass (web search, per citation): all 8 references were confirmed to exist with the stated identifiers and to support the attached claims. Three author attributions were corrected during verification — [1] is Spit/Rieser/Walczak (not Fuseya & Iwai), [2] is Oikawa/Hatanaka/Suzuki/Tokunaga (not "Fujita et al"), and [6] is Okamura et al. (not "Teh et al"). Content checks: Das 2001 [7] shows p50/NF-κB1 is required for GATA3/Th2 with T-bet/IFN-γ intact; Graß 2025 [5] states LUBAC is largely dispensable for TCR-induced NF-κB in human CD4⁺ T cells (the load-bearing counter-evidence in §4). No unverified citations; no claim rests on an unverifiable source.*
