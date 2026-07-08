# GPATCH8 — selective Th2-suppressor mechanism dossier

**Screen signal:** Th2-arm z = -2.18, magnitude-controlled residual = -1.94, condition = Rest, class = other
**Final verdict (post–adversarial review):** UNCERTAIN  ·  investigator: uncertain (low conf) · citations: supported

## Hypothesis
As a branchpoint splicing quality-control factor, GPATCH8 loss could selectively impair productive splicing/expression of a Th2-program transcript (e.g., GATA3 or an upstream STAT6/IL4-axis component), lowering Th2 output without engaging the T-bet/Th1 axis.

## Mechanism
GPATCH8 is a G-patch protein that activates the RNA helicase DHX15 in branchpoint/intron quality control, functionally opposing SUGP1; it is required for aberrant splicing induced by mutant SF3B1. There is no direct evidence linking GPATCH8 to GATA3, IL4, or Th2 differentiation. A selective route would have to run through splicing: GPATCH8-dependent retention or correct processing of a Th2-enabling transcript (GATA3 has multiple isoforms and is dosage-sensitive), such that KD skews toward non-productive isoforms of a Th2 node while leaving Th1 transcription factors unaffected. This is mechanistically conceivable for a splicing factor but is entirely speculative for GPATCH8 specifically.

**Bypasses T-bet / Th1?** True — GPATCH8 is a splicing quality-control factor, not a Th1 transcription factor or T-bet inducer; there is no known route by which losing it would activate the Th1 program. The observed Th1-flat/Th2-down pattern is therefore consistent with a mechanism that reduces Th2 output directly rather than by diverting cells into Th1, so the selectivity is not explained by simple T-bet induction.

## Evidence
- GPATCH8 is a G-patch splicing quality-control factor that activates DHX15 and antagonizes SUGP1 in branchpoint selection; it is required for mutant SF3B1-induced mis-splicing.  
  _source:_ Benbarche et al., 'GPATCH8 modulates mutant SF3B1 mis-splicing and pathogenicity in hematologic malignancies', Molecular Cell 2024 (PMC11102302)
- Silencing GPATCH8 corrected ~one-third of mutant-SF3B1 splicing defects and IMPROVED dysfunctional hematopoiesis in mice and primary human progenitors, indicating its loss is well tolerated (not an essential/lethal gene).  
  _source:_ Benbarche et al., Molecular Cell 2024; ASH Blood 2023 abstract 179848
- GPATCH8 domain architecture: N-terminal G-patch (RNA-processing) domain, C2H2 zinc finger, lysine-rich and serine-rich regions; a serine-region variant is linked to hyperuricemia — i.e., a ubiquitous RNA-processing protein, not a T-cell-restricted regulator.  
  _source:_ UniProt Q9UKJ3; OMIM 614396; GeneCards GPATCH8
- The screen is the genome-scale CRISPRi perturb-seq in primary human CD4+ T cells nominating Th1/Th2 polarization regulators; GPATCH8 is not otherwise reported as a Th2 regulator in the T-cell/GATA3 literature.  
  _source:_ Genome-scale perturb-seq in primary human CD4+ T cells, bioRxiv 2025.12.23.696273 (Marson lab); no GPATCH8 hits in GATA3/Th2 reviews e.g. Nat Rev Immunol nri2476

## Proposed confirming experiment
CRISPRi knock down GPATCH8 in primary human CD4+ T cells, then split into Th2-polarizing and Th1-polarizing arms in parallel. Read out (i) intracellular IL4/IL5/IL13 and GATA3 vs IFNG/T-bet by flow, plus qPCR, to confirm Th2-selective loss; (ii) matched viability/proliferation (CellTrace, live-cell counts) and a global transcriptional-magnitude metric to exclude nonspecific dampening; (iii) RNA-seq with splicing analysis (rMATS/LeafCutter) focused on GATA3 and Th2-axis transcripts to test whether a specific mis-splicing/isoform shift underlies the phenotype. Epistasis test: rescue with GATA3 cDNA (splicing-insensitive ORF) — restoration of Th2 output would pin the effect on a GATA3-axis splicing dependency rather than global toxicity.

## Adversarial review
- **Citations check:** supported
- **Agrees artifact call (False):** True
- **Notes:** Sources are real and each cited factual claim checks out. Confirmed Benbarche et al., Mol Cell 2024 (PMC11102302): GPATCH8 is a G-patch branchpoint quality-control factor that interacts with DHX15 and functionally opposes SUGP1; "Gpatch8 silencing was well-tolerated in WT mouse BM cells despite ~80% reduction" and silencing "partially rescued impaired hematopoietic growth" — so loss is not lethal/essential (supports claims 1-2). The Marson-lab genome-scale CD4+ perturb-seq preprint (bioRxiv 2025.12.23.696273) is real and does nominate Th1/Th2 polarization regulators via the screen; I could not extract the specific GPATCH8 hit line (403 on full text), but the investigator honestly concedes GPATCH8 is not independently reported as a Th2/GATA3 regulator. Strongest objection: the "bypasses T-bet / selectively suppresses Th2" hypothesis is entirely speculative and unsupported by any cited source. GPATCH8 is a ubiquitous RNA-processing factor whose ONLY characterized function is enabling MUTANT-SF3B1 mis-splicing; in WT context its loss perturbs little splicing, so a clean mechanistic link to GATA3/STAT6/IL4 splicing is unestablished and there is no data showing Th1/T-bet is spared. A splicing-QC factor scoring as a Th2 hit could equally reflect broad transcriptional/translational dampening rather than genuine Th2 selectivity. I agree likely_artifact=false only in the narrow sense that documented tolerability of GPATCH8 loss argues against a pure fitness/dead-cell artifact — but selectivity remains unproven and the mechanism is weak; "uncertain" is appropriate, arguably leaning toward the skeptical end.
