# STK35 — selective Th2-suppressor mechanism dossier

**Screen signal:** Th2-arm z = -2.11, magnitude-controlled residual = -1.82, condition = Stim8hr, class = kinase · druggable
**Final verdict (post–adversarial review):** UNLIKELY  ·  investigator: uncertain (low conf) · citations: partially_supported

## Hypothesis
Losing STK35 could lower the Th2 program indirectly by blunting the AKT/glycolysis-driven proliferative and metabolic burst that GATA3/IL4 induction disproportionately depends on, rather than by acting as a dedicated Th2 transcriptional regulator.

## Mechanism
STK35 (STK35L1) is a nuclear/nucleolar Ser/Thr kinase with no reported function in T cells, Th2/Th1 differentiation, GATA3, IL4, or TCR/cytokine signaling. Its documented roles are cell-cycle control (inhibits G1-to-S via CDKN2A/p16, binds nuclear actin), endothelial migration/angiogenesis, spermatogenesis, and promotion of glycolysis plus suppression of apoptosis through AKT signaling (colorectal cancer). The only route to the Th2 program is therefore indirect: AKT-mTOR and glycolytic flux support proliferation and biosynthesis, and Th2/GATA3/IL4 induction upon stimulation is more metabolically and proliferation-demanding than the (here already flat) Th1 readout. Reduced STK35 could thus preferentially shrink the higher-dynamic-range Th2 output without any GATA3-specific mechanism.

**Bypasses T-bet / Th1?** True — There is no evidence STK35 drives Th1/T-bet, so its loss is not expected to induce IFNG/T-bet. The Th1-flat pattern is trivially consistent with a global/metabolic dampener (both arms suppressed or Th1 already low), not with active Th1 skewing. So it plausibly avoids the 'it's just a Th1 driver' explanation, but this bypass is trivial and does not by itself demonstrate genuine Th2-selective regulation.

## Evidence
- STK35L1 is a nuclear/nucleolar Ser/Thr kinase that binds nuclear actin and regulates endothelial cell cycle (G1-to-S via CDKN2A/p16), migration and angiogenesis; no T-cell/Th2 role reported.  
  _source:_ STK35L1 Associates with Nuclear Actin and Regulates Cell Cycle and Migration of Endothelial Cells, PLOS ONE 2011, PMC3024402
- STK35 promotes glycolysis and inhibits apoptosis via the AKT signaling pathway and is ubiquitinated by NEDD4L (colorectal cancer chemoresistance) — a metabolic/survival/proliferation profile.  
  _source:_ STK35 Is Ubiquitinated by NEDD4L and Promotes Glycolysis and Inhibits Apoptosis Through Regulating the AKT Signaling Pathway, Front Cell Dev Biol 2020, PMC7578231
- Reviewed functions of STK35/STK35L1 span cell cycle, migration, angiogenesis, DNA damage response and spermatogenesis/gametogenesis; the locus also encodes an oxidative-stress-responsive lncRNA. No immune/Th2 function is described.  
  _source:_ The Multifaceted Role of STK35/STK35L1 in Human Diseases, Kinases and Phosphatases 2025, doi:10.3390/kinasesphosphatases3020012; PMC6124569
- GATA3 is the master Th2 regulator (opens IL4/IL5/IL13 locus, represses IFNG); no upstream link to STK35 exists in the literature, so any STK35 effect on this axis would be indirect.  
  _source:_ GATA-3 promotes Th2 responses..., Cell Research 2006, nature.com/articles/7310002

## Proposed confirming experiment
Arrayed CRISPRi knockdown of STK35 (plus non-targeting and a known Th2-selective control such as GATA3) in primary human CD4+ T cells under matched Th2- and Th1-polarizing conditions. Primary readout: intracellular GATA3/IL4/IL5/IL13 vs T-bet/IFNG by flow at 8hr and after full polarization. Critically, co-measure the global-dampening confounders on the SAME cells: proliferation (CellTrace dilution), viability, live-cell yield, and metabolic state (glucose uptake / Seahorse ECAR, plus pAKT/pS6). Test whether the IL4/GATA3 deficit persists after normalizing per-live-cell and per-division, and whether supplementing exogenous IL-2 or restoring glycolysis/AKT rescues Th2. Genuine selective suppression = GATA3/IL4 drop that survives proliferation/viability/metabolic normalization while IFNG and total activation (CD25/CD69, blast size) are spared; a metabolic-dampener artifact = Th2 loss that tracks with reduced division/glycolysis and is rescued by metabolic support.

## Adversarial review
- **Citations check:** partially_supported
- **Agrees artifact call (True):** True
- **Notes:** All four sources are real and verified (PMC3024402, PMC7578231, 2025 Kinases&Phosphatases review, PMC6124569, GATA3 Cell Research 2006/7310002); each broadly supports its claim. One unverified embellishment: the "(G1-to-S via CDKN2A/p16)" detail is not confirmed by the 2011 PLOS ONE abstract, hence partially_supported. Strongest objection: the pro-proliferation mechanism is internally inconsistent — in endothelial cells STK35L1 depletion ACCELERATES G1-to-S (inhibitory role), opposite to the CRC pro-glycolysis/AKT role, so "blunting a proliferative burst" is direction-inconsistent and context-dependent. There is zero immune/T-cell evidence; a generic AKT/glycolysis/proliferation dependency is the classic proliferation/metabolic-fitness confound in Th2-selective screens (Th2 cells are highly glycolytic/proliferative), making apparent selectivity most likely an artifact rather than dedicated Th2 transcriptional regulation. The "bypasses T-bet" concern is moot since no evidence touches T-bet and the hypothesis is itself indirect/metabolic. Mild mitigation: an AKT1->GATA3 phosphorylation axis (Nat Commun 2016) gives a thin plausible indirect route, so not fully dismissable. I agree with likely_artifact=true but rate the selective-Th2-suppressor claim as unlikely rather than merely uncertain.
