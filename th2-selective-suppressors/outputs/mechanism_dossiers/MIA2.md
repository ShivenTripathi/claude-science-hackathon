# MIA2 — selective Th2-suppressor mechanism dossier

**Screen signal:** Th2-arm z = -2.01, magnitude-controlled residual = -1.71, condition = Rest, class = other
**Final verdict (post–adversarial review):** LIKELY_ARTIFACT  ·  investigator: unlikely (medium conf) · citations: partially_supported

## Hypothesis
If MIA2 knockdown selectively lowered the Th2 program, it would most plausibly be by degrading the ER-export/secretory capacity that autocrine IL-4/STAT6/GATA3 feedback (and the high secretory load of Th2 cells) depends on, rather than by any Th2-specific transcriptional role.

## Mechanism
MIA2 has no described role in TCR signaling, STAT6, GATA3 induction, or the IL4/IL5/IL13 locus. It encodes the TANGO1-family ER-exit-site proteins TALI/cTAGE5, which partner with TANGO1 (MIA3) and Sec12/Sar1/COPII to export bulky cargo (procollagen, ApoB chylomicrons/VLDL) from the ER. The only speculative Th2 route is indirect: Th2 differentiation runs on an IL-4 -> IL-4R -> STAT6 -> GATA3 autocrine positive-feedback loop, so a cell-wide secretory-pathway defect could blunt establishment of that loop. However, IL-4/IL-5/IL-13 are small conventional-secretion cargoes that do not require TANGO1/TALI bulky-cargo machinery, so this link is mechanistically weak, and it would predict a broad secretory/fitness defect rather than a clean transcriptional Th2 collapse.

**Bypasses T-bet / Th1?** True — An ER-export/secretory-pathway gene has no known activity that would drive T-bet or IFNG. If MIA2 loss impairs anything, it is secretory capacity/fitness, which would if anything dampen rather than divert toward Th1. So the observed Th1-flat, Th2-down pattern is consistent with a non-Th1-driving (secretory-stress or magnitude) effect rather than active Th1 induction. This is a point in favor of it not being a mislabeled Th1 driver, but it does not establish a Th2-specific mechanism.

## Evidence
- MIA2 encodes the ER-exit-site proteins TALI and cTAGE5, which cooperate with TANGO1 (MIA3), Sec12 and COPII (Sar1) to export bulky cargo such as pre-chylomicrons/VLDL and collagen from the ER; it is a secretory-pathway component, not a transcription factor.  
  _source:_ Santos et al., TANGO1 and Mia2/cTAGE5 (TALI) cooperate to export bulky pre-chylomicrons/VLDLs from the ER, eLife 2016 (PMC4862334); OMIM 602132 MIA2
- MIA2 localizes to ER exit sites (transitional ER) and shows low immune-cell specificity; it is expressed most abundantly in glandular/hepatic and neuronal cells, not enriched in T cells.  
  _source:_ Human Protein Atlas, MIA2 (ENSG00000150527), immune cell and tissue expression
- MIA2 transcription in hepatocytes is driven by IL-6/STAT3 and TGF-beta/SMAD, not by TCR- or Th2-associated cytokines; no literature links MIA2/TALI/cTAGE5 to GATA3, STAT6, or the IL4/IL5/IL13 program.  
  _source:_ GeneCards MIA2; literature search (PubMed) returned no MIA2-Th2/GATA3 associations
- The Th2 program is controlled by an IL-4 -> STAT6 -> GATA3 autocrine feedback loop; GATA3 (not any secretory factor) opens the IL4/IL5/IL13 locus and represses IFN-gamma.  
  _source:_ Zhu et al., GATA3 and the T-cell lineage, Immunol Rev 2010 (PMC2998182); Nawijn/Zhu, Cell Research 7310002

## Proposed confirming experiment
Arrayed CRISPRi knockdown of MIA2 (plus non-targeting and a positive-control GATA3 guide) in naive human CD4+ T cells, split into parallel Th2-polarizing (IL-4 + anti-IFNg/anti-IL-12) and Th1-polarizing (IL-12 + anti-IL-4) cultures. Primary readout: GATA3 and IL4/IL5/IL13 vs T-bet/IFNG by intracellular flow and qPCR/RNA-seq to confirm the arm-selective transcriptional effect. Critically add specificity controls that separate a real Th2 regulator from a secretory/global-dampening artifact: (1) viability, proliferation (CellTrace), and total mRNA/blast size to catch fitness/magnitude effects; (2) a general secretion reporter (e.g., secreted Gaussia luciferase or bulk supernatant protein) and an ER-stress marker (XBP1 splicing, BiP) to test whether MIA2 KD broadly impairs secretion/induces ER stress; (3) rescue by exogenous IL-4 -> if adding saturating IL-4 restores GATA3, the effect is upstream/secretory rather than a dedicated Th2 transcriptional role. A genuine selective suppressor should lower GATA3/IL4 with intact viability, normal bulk secretion/no ER stress, and not be rescued simply by exogenous IL-4.

## Adversarial review
- **Citations check:** partially_supported
- **Agrees artifact call (True):** True
- **Notes:** Confirmed all four claims against primary sources. MIA2 encodes TALI/cTAGE5, an ER-exit-site COPII accessory that cooperates with TANGO1 (MIA3) to export bulky cargo (pre-chylomicrons/VLDL, collagen) — a secretory component, not a TF (Malhotra et al. 2016; OMIM 602132). CITATION ERROR: this paper is in Journal of Cell Biology (213:343-354, PMID 27138255), NOT eLife as cited, though the PMC ID (PMC4862334) is correct and real. HPA confirms glandular/hepatic/neuronal expression, liver-abundant, low immune specificity. Hepatocyte MIA2 is driven by IL-6/STAT3 + TGF-beta/SMAD (Bosserhoff PMID 12586826), with no literature link to GATA3/STAT6/IL4-5-13. The task's 'bypasses T-bet' question does not apply — the dossier makes no T-bet argument. Strongest objection to a genuine hit: knocking out an essential ER-export gene in the most secretion-heavy Th subset (high autocrine IL-4 load) plausibly produces a selective-Th2 dropout as a secretory-capacity confounder, not a Th2-specific role — which is exactly an artifact signature and would also be expected to broadly impair effector/proliferative function. I agree with unlikely/likely_artifact.
