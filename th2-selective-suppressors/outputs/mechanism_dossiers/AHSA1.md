# AHSA1 — selective Th2-suppressor mechanism dossier

**Screen signal:** Th2-arm z = -2.11, magnitude-controlled residual = -2.53, condition = Rest, class = other
**Final verdict (post–adversarial review):** UNCERTAIN  ·  investigator: uncertain (low conf) · citations: partially_supported

## Hypothesis
Loss of AHSA1 (Aha1), the sole mammalian activator of HSP90 ATPase, impairs HSP90 chaperoning of the metastable Th2-defining clients STAT6 and GATA3, collapsing the GATA3/IL4/IL5/IL13 program while leaving the less chaperone-addicted T-bet/IFNG axis intact.

## Mechanism
AHSA1/Aha1 stimulates HSP90's ATPase cycle and is preferentially required for maturation of a subset of "hard-to-fold," metastable clients (kinases, steroid receptors, v-Src) rather than for bulk proteostasis. STAT6 (the IL-4/STAT6 axis that induces and sustains GATA3) and GATA3 itself are dosage-sensitive, chaperone-dependent signaling proteins, so reduced HSP90 productivity from AHSA1 knockdown could lower functional STAT6/GATA3 and thereby the whole IL4/IL5/IL13 output. Because the mechanism acts by removing positive Th2 drivers rather than by inducing T-bet, it would not push cells toward Th1. Importantly, unlike HSP90 or core translation/RNA machinery, Aha1 is non-essential (viable KO cell lines and dispensable in yeast/basal conditions), so its knockdown need not globally kill or arrest the cell.

**Bypasses T-bet / Th1?** True — The proposed route (impaired HSP90 chaperoning of STAT6/GATA3) removes Th2-positive drivers and provides no mechanism to activate T-bet or STAT4; Aha1 loss is not known to induce a Th1 program, so it fits a 'selective suppressor' rather than a 'Th1 driver' that indirectly cross-represses Th2.

## Evidence
- AHSA1/Aha1 is the only known mammalian activator of HSP90 ATPase activity; it is a stress-regulated co-chaperone that drives HSP90 into its closed, ATPase-active state.  
  _source:_ Recruitment of Ahsa1 to Hsp90 is regulated by a conserved peptide that inhibits ATPase stimulation, PMC11316058
- Aha1 is dispensable under basal conditions (non-essential in yeast; viable human AHSA1-KO cell lines exist), but its loss selectively impairs activation of hard-to-fold clients such as v-Src and hormone receptors — i.e., it modulates a client subset rather than bulk proteostasis.  
  _source:_ Silencing of HSP90 cochaperone AHA1 decreases client protein activation (PubMed 18281495); Abcam human AHSA1 KO HeLa line ab265043; Panaretou/Prodromou co-chaperone reviews
- STAT6 is required to induce/sustain GATA3 and the Th2 cytokine program; STAT6 or GATA3 loss/inhibition selectively abrogates IL4/IL5/IL13 and allergic inflammation without driving Th1.  
  _source:_ STAT6 inhibitor AS1517499 reduces Th2 cytokines and regulates GATA3 (PMC8851827); GATA-3 promotes Th2 responses (Nature Cell Research, 7310002)
- HSP90/heat-shock chaperone machinery is physically and functionally linked to GATA3 function (e.g., HSP60 maintains GATA3-dependent Pol II pausing at the Il5 locus; Aha1 modulates GATA3-dependent phenotypes in vivo).  
  _source:_ Methylation of Gata3 at Arg-261 / HSP60-GATA3 at Il5 (PMC4505565); zebrafish Aha1a modifies GATA3-mutant craniofacial phenotype
- HSP90 also chaperones Dicer1 and thereby miRNA maturation, illustrating that Aha1/HSP90 perturbation can have pleiotropic, program-shaping downstream effects.  
  _source:_ HSP90 and Aha1 modulate microRNA maturation through folding of Dicer1, PMC9262616

## Proposed confirming experiment
Arrayed CRISPRi knockdown of AHSA1 (plus non-targeting and a known Th2 driver e.g. GATA3/STAT6 as positive controls) in primary human CD4+ T cells cultured in parallel under Th2-polarizing (anti-CD3/28 + IL-4 + anti-IL-12) and Th1-polarizing (IL-12 + anti-IL-4) conditions. Primary readout: intracellular flow/qPCR for GATA3, IL-4/IL-5/IL-13 vs T-bet/IFN-gamma, with the key test being a Th2-specific drop and NO increase in T-bet/IFN-gamma. Mechanistic readouts: STAT6 total and phospho-STAT6 levels after IL-4, GATA3 protein half-life by cycloheximide chase, and HSP90 co-IP with STAT6/GATA3 upon AHSA1 KD (expect reduced client stability/association). Critical artifact controls: CellTrace proliferation, viability, and a global-magnitude panel (total protein synthesis / housekeeping TF such as RUNX or general activation markers) to confirm the effect is Th2-selective and not global dampening; also confirm on-target via multiple guides and rescue with guide-resistant AHSA1.

## Adversarial review
- **Citations check:** partially_supported
- **Agrees artifact call (False):** True
- **Notes:** Cited sources are all real and I confirmed each. However support is partial and the mechanism has an unsupported core. Confirmed: PMC11316058 (Aha1 ICD autoinhibition), PMC9262616 (Aha1/HSP90-Dicer1), PubMed 18281495 (client-subset modulation), PMC8851827 (STAT6i reduces Th2), zebrafish PMC3759348. Key objections: (1) The load-bearing premise that STAT6 and GATA3 are HSP90/Aha1 clients is NOT supported by any cited source; Aha1's known client subset is kinases/v-Src/steroid receptors/CFTR, not these TFs, so AHSA1->HSP90->STAT6/GATA3 is an inference gap. (2) The 'HSP90/GATA3 machinery' citation PMC4505565 is actually about HSP60 (not HSP90/Aha1) and HSP60 REPRESSES Il5 by pausing Pol II — a misleading, arguably wrong-direction link. (3) The zebrafish paper shows Aha1a knockdown alleviates a GATA3 loss-of-function (HDR) phenotype, i.e. a genetic modifier, not that GATA3 is an Aha1 client. (4) 'Only/sole mammalian activator' is overstated — source says 'most potent stimulator'; AHSA2 paralog exists. (5) The 'bypasses T-bet' selectivity is contradicted by evidence that HSP90 blockade (17-DMAG, PMC3976086) suppresses Th1/Th17 (IFN-g, IL-17) and disrupts Lck/TCR signaling, i.e. broad T-cell dampening rather than Th2-specific collapse. Partial defense: AHSA1 KD is milder and more client-selective than HSP90 inhibition (viable KO lines), so a selective phenotype is not impossible. Net: gene is real and biology is coherent enough that the screen hit is unlikely a pure artifact (agree likely_artifact=false), but the specific selective-Th2 mechanism is speculative and under-supported; 'uncertain' is appropriate, leaning skeptical.
