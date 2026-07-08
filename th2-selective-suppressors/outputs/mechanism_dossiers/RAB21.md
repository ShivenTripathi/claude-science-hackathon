# RAB21 — selective Th2-suppressor mechanism dossier

**Screen signal:** Th2-arm z = -2.76, magnitude-controlled residual = -2.94, condition = Rest, class = other
**Final verdict (post–adversarial review):** LIKELY_ARTIFACT  ·  investigator: uncertain (low conf) · citations: supported

## Hypothesis
Loss of RAB21 could preferentially blunt the highly glycolysis/mTOR-dependent Th2 (GATA3/IL4) program by mis-sorting surface GLUT1 and impairing receptor recycling, without inducing T-bet/Th1.

## Mechanism
RAB21 is an early-endosome Rab GTPase governing retromer-mediated recycling of GLUT1/SLC2A1, integrin endo/exocytosis, EGFR/receptor recycling, and autophagy. Its KD lowers surface GLUT1 and glucose uptake, dampening cellular energy homeostasis; because Th2 induction of GATA3 depends heavily on sustained TCR/PI3K/mTOR/glycolytic signaling, reduced glucose flux or impaired cytokine-receptor (e.g. IL-2/IL-4R->STAT5) recycling could preferentially attenuate the Th2 program. However, none of these routes is Th2-specific in the literature, and Th1 is also glycolysis-dependent, so a genuinely selective effect on GATA3/IL4 over IFNG is speculative. No published work connects RAB21 to GATA3, IL4, or Th2/Th1 fate.

**Bypasses T-bet / Th1?** True — RAB21's known roles are in trafficking/metabolism/autophagy, not transcriptional Th lineage priming; there is no route by which its loss would induce T-bet or drive Th1. Any Th1-flat selectivity would arise from Th1 being less sensitive to the perturbation, not from T-bet induction. So the phenotype is not explained by a Th1-driver mechanism.

## Evidence
- RAB21 controls retromer-mediated recycling of glucose transporter GLUT1/SLC2A1; KD mis-sorts GLUT1 to lysosomes, lowers surface GLUT1, and disrupts cellular energy homeostasis and autophagy.  
  _source:_ RAB21 controls autophagy and cellular energy homeostasis by regulating retromer-mediated recycling of SLC2A1/GLUT1, Autophagy 2022/2023, PMC10012929
- RAB21 is an early-endosome small GTPase that regulates integrin internalization, cell adhesion, migration and cytokinesis via integrin endo/exocytic traffic.  
  _source:_ Small GTPase Rab21 regulates cell adhesion and controls endosomal traffic of beta1-integrins, J Cell Biol 2006, PMC2063892; Integrin trafficking regulated by Rab21 is necessary for cytokinesis, Dev Cell 2008, PMID 18804435
- RAB21 acts as a general regulator of cell-surface receptor identity (broad, non-lineage-specific trafficking role) and affects EGFR internalization/degradation.  
  _source:_ Phenotypic screens for SIRPA reveal RAB21 as a general regulator of macrophage surface identity, Cell Reports 2025, S2211-1247(25)00692-8
- No primary literature links RAB21 to GATA3, IL4, or Th2/Th1 differentiation; Th2/GATA3 induction is instead driven by TCR + STAT5/STAT6 and is glycolysis/mTOR-dependent.  
  _source:_ Transcriptional regulation of Th2 cell differentiation, PMC3477614; T cell receptor-dependent translational control of GATA-3 enhances Th2 differentiation, PMC3993005 (RAB21 absent from Th2 literature)

## Proposed confirming experiment
CRISPRi KD of RAB21 (plus non-targeting and a known Th2-essential positive control e.g. GATA3) in naive human CD4+ T cells split into parallel Th2-polarizing and Th1-polarizing arms. Read out GATA3/IL4/IL5/IL13 vs T-bet/IFNG by intracellular flow and qPCR, with a sgRNA rescue (RAB21 re-expression). Crucially, include global-dampening controls run in the same cells: proliferation (CTV dilution), viability, surface GLUT1 and glucose uptake (2-NBDG), and Seahorse ECAR/OCR. Selective Th2 suppression is supported only if GATA3/IL4 drop disproportionately to IFNG AND is not accounted for by reduced proliferation/viability or a proportional metabolic collapse; a glucose/pyruvate add-back arm tests whether the effect is purely metabolic. Rescue restoring the phenotype confirms specificity.

## Adversarial review
- **Citations check:** supported
- **Agrees artifact call (True):** True
- **Notes:** All four cited sources are real and accurately represented. Verified: (1) Autophagy 2022, PMC10012929 (PMID 35993307) - RAB21 depletion mis-sorts SLC2A1/GLUT1 to lysosomes, lowers glucose uptake, activates AMPK-ULK1, increases autophagy; also sensitizes cancer cells to energy stress. Correct. (2) J Cell Biol 2006 PMC2063892 (PMID 16754960) - Rab21/beta1-integrin adhesion/migration. Correct. (3) Dev Cell 2008 (PMID 18804435) - Rab21 integrin trafficking required for cytokinesis; loss causes multinucleate cells. Correct. (4) Cell Reports 2025 S2211-1247(25)00692-8 (PMID 40580479) - RAB21 as GENERAL regulator of macrophage surface identity, remodels whole surfaceome, reduces FcgR. Correct.

Strongest objection: the evidence directly refutes selectivity rather than supporting it. RAB21 is a broad housekeeping endosomal/retromer trafficking GTPase whose loss (a) globally remodels the surfaceome (paper's own framing: 'general regulator of surface identity'), (b) impairs cytokinesis producing multinucleate cells - which would blunt proliferation of ALL activated T cells including Th1, and (c) lowers global glucose uptake/energy. The 'preferentially blunts Th2 because Th2 is uniquely glycolysis/mTOR-dependent' premise is weak: Th1 (T-bet) and Th17 are equally or more glycolysis/mTORC1-dependent, so a GLUT1/energy hit would dampen Th1 as much as Th2 rather than sparing it - undercutting the 'without inducing T-bet/Th1' claim. No primary literature links RAB21 to GATA3/IL4/T-bet (investigator concedes this). A pan-proliferation/energy defect masquerading as Th2-selective is exactly the artifact signature. I agree with likely_artifact=true.
