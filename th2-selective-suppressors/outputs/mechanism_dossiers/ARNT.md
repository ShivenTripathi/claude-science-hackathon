# ARNT — selective Th2-suppressor mechanism dossier

**Screen signal:** Th2-arm z = -2.51, magnitude-controlled residual = -2.59, condition = Stim48hr, class = TF
**Final verdict (post–adversarial review):** UNCERTAIN  ·  investigator: plausible (medium conf) · citations: partially_supported

## Hypothesis
ARNT (HIF-1β) is the obligate dimerization partner for HIF-1α/HIF-2α, and because stimulation-induced HIF signaling promotes the GATA3/IL-4 Th2 program while Th1/T-bet is relatively HIF-independent, ARNT knockdown collapses HIF output and selectively lowers Th2 without inducing Th1.

## Mechanism
ARNT is the shared, obligate bHLH-PAS partner that HIF-1α and HIF-2α (and AHR) require to form functional transcription factors. TCR/mTOR signaling induces HIF-1α even under normoxia during activation, and multiple studies show HIF-1α and HIF-2α positively drive Th2 differentiation, GATA3, and IL-4/IL-13 (a HIF-1α inhibitor suppresses Th2/IL-4/IL-13; HIF-2α deficiency impairs Th2 and asthmatic inflammation; a 2024 Immunity paper shows HIF-2α promotes pathogenic stem-like Th2 polarization). Losing ARNT would abrogate both HIF-1α and HIF-2α output simultaneously, removing this pro-Th2 input. Because HIF preferentially supports Th17/glycolysis and Th2, and Th1/T-bet commitment is comparatively HIF-independent, the Th1 arm can stay flat rather than being reciprocally induced.

**Bypasses T-bet / Th1?** True — The proposed route works by removing a positive HIF-driven input to the Th2/GATA3 program, not by relieving Th2 repression of Th1. Loss of HIF/ARNT is not known to induce T-bet or IFNG; if anything HIF drives Th17 and glycolysis, and Th1 commitment is comparatively HIF-independent. So a Th2-down/Th1-flat pattern is mechanistically consistent with selective suppression rather than Th1 induction. Caveat: the AHR:ARNT arm points the opposite way (AHR activation suppresses Th2, AHR loss raises IL-4), so the net Th2-down phenotype implies the HIF arm dominates in this stimulated normoxic context.

## Evidence
- ARNT/HIF-1β is the obligate heterodimeric partner required by both HIF-1α and HIF-2α (and AHR); it is ubiquitously expressed and its total loss is embryonic lethal (a hub/essential factor).  
  _source:_ Conditional Disruption of Arnt, Mol Endocrinol 2000; Arnt endothelial KO embryonic lethality, PMC1559728; ScienceDirect ARNT overview
- HIF-1α promotes Th2 differentiation and IL-4/IL-13; a HIF-1α inhibitor restrains HIF-1α and inhibits Th2 differentiation and IL-4/IL-13 expression.  
  _source:_ Frontiers Immunol 2022, HIF-1α in inflammatory autoimmune diseases (10.3389/fimmu.2022.1073971)
- HIF-2α promotes pathogenic polarization of stem-like Th2 cells; HIF-2α deficiency impairs Th2 differentiation and alleviates asthmatic inflammation.  
  _source:_ Immunity 2024, 'Hypoxia-inducible factor 2α promotes pathogenic polarization of stem-like Th2 cells' (Cell Press S1074-7613(24)00496-5)
- Hypoxia/HIF-1α augment Tc2/Th2 responses via JAK1/3 and GATA-3, linking HIF output to GATA3 induction and IL-4 signaling.  
  _source:_ J Allergy Clin Immunol / Hypoxia enhances CD8+ Tc2 via HIF-1α, PMC11098440
- HIF-1α drives glycolysis (Glut1, glycolytic enzymes) and tips Th17 vs Treg balance; loss impairs Th17 but not classically Th1 — supporting that HIF loss is not a Th1 driver.  
  _source:_ Shi et al., J Exp Med 2011, PMC3135370 (HIF1α glycolytic checkpoint for Th17/Treg)
- Via the AHR arm, ARNT loss would be expected to INCREASE Th2: AHR activation (TCDD) suppresses Th2 cytokines/allergy, and AHR deficiency elevates IL-4 — a direction opposite to the screen hit, indicating the HIF arm must dominate.  
  _source:_ AhR master regulator of allergic immune responses, PMC9806217; Differential regulation of asthmatic phenotype by AhR, PMC8566992

## Proposed confirming experiment
Single-gene ARNT CRISPRi knockdown in primary human CD4+ T cells under explicit Th2-polarizing vs Th1-polarizing conditions, reading GATA3, IL4, IL5, IL13 vs TBX21/IFNG by intracellular cytokine flow and qPCR. Critically distinguish selective suppression from global dampening by co-measuring: (a) proliferation/viability, total protein synthesis, and blast size; (b) glycolytic flux (ECAR, GLUT1/SLC2A1, LDHA) to confirm HIF axis engagement; (c) normoxia vs hypoxia (1% O2) and CoCl2 stabilization to test HIF-dependence. Run epistasis/rescue: compare ARNT KD to HIF1A + HIF2A double KD (should phenocopy) and to AHR KD (predicted opposite/Th2-up), and rescue ARNT KD with a HIF-target-independent GATA3 overexpression to test whether Th2 loss is downstream of GATA3. Confirm direct regulation with HIF/ARNT ChIP-seq or CUT&RUN at the GATA3/IL4 loci. Selective, HIF-dependent GATA3/IL4 loss with intact viability and flat Th1 would confirm a genuine selective Th2 suppressor rather than a magnitude artifact.

## Adversarial review
- **Citations check:** partially_supported
- **Agrees artifact call (False):** True
- **Notes:** Confirmed: the cited primary sources are real and accurate for what they individually say. The Immunity 2024 HIF-2α paper (PMID 39609127) robustly supports HIF-2α promoting Th2 via a HIF2a-GATA3 circuit, with HIF2a deficiency lowering GATA3/IL-4/IL-5/IL-13 and alleviating asthma. Shi 2011 JEM (PMC3135370) is correctly cited but concerns Th17/Treg glycolysis and does NOT address Th1; the claim that HIF loss is not a Th1 driver is an unsupported inference, and the 'bypasses T-bet' framing is a strawman (the mechanism never engages T-bet). The core weakness: NO source demonstrates ARNT knockdown selectively lowering Th2 in CD4 cells — the entire ARNT link is inferential through HIF. ARNT is a pleiotropic hub (obligate for HIF-1a, HIF-2a, AND AHR); ARNT deletion in CD8 T cells broadly impairs effector function (perforin/granzyme/migration), which favors the competing 'broadly dampens the cell' hypothesis over Th2 selectivity. The investigator also concedes the AHR arm predicts the opposite direction (AHR loss raises IL-4), so net Th2 suppression rests on an untested assumption that the HIF arm dominates. Not likely an artifact (HIF genuinely drives Th2, so a Th2-lowering hit is mechanistically coherent), but 'plausible' overstates the selectivity case given hub pleiotropy and absent direct ARNT-Th2 evidence; downgrading to uncertain.
