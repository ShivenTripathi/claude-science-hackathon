# Independent review report — Selective Th2 Suppressor Atlas

Two-part self-review: (A) a data/QC audit against the dataset's own richer QC columns, and
(B) a 6-agent parallel literature + methods audit (each finding adversarially sourced).

## Part A — Data / QC self-audit (issues found in our own pipeline, now fixed)

1. **We ignored the `neighboring_gene_KD` flag.** CRISPRi can silence a gene *adjacent* to the
   intended target. Our former #1 novel hit **AHSA1** is neighbor-flagged in Stim8hr (its selective
   Rest row is clean, but the gene is suspect). **Fix:** neighbor-flagged perturbation×conditions are
   now dropped from the high-confidence set.
2. **We used the wrong donor-reproducibility column.** The suppl-table `crossdonor` was NaN for 78%
   of hits (median 0.15). The correct `donor_correlation_hits_mean` has **median 0.81** on our set —
   our hits are *more* donor-reproducible than first reported. **Fix:** switched the donor metric;
   ARNT (0.87), ELAVL1 (0.80), GATA3 (0.82) now confirmed reproducible.
3. **Single-guide hits weren't penalized.** ARL1 and MPG rest on one guide (`single_guide_estimate`).
   **Fix:** single-guide candidates are down-weighted.
4. **The selective count is threshold-soft** (49 / 127 / 199 as the Th1 gate loosens). The honest
   robust set is the **core ~12–23 genes**, not 127.

## Part B — Literature & methods audit (6 parallel agents)

### Foundational immunology — **well supported**

**Holds up:**
- Th1 and Th2 are reciprocal, mutually antagonistic CD4+ effector lineages: their cytokine profiles are dictated by the mutually exclusive expression of the master transcription factors T-bet (Th1) and GATA3 (Th2), which directly cross-repress (T-bet binds and sequesters GATA3, blocking it from Th2 cytokine promoters).
- GATA3 is the master regulator of Th2 differentiation: enforced GATA3 drives Th2 even under Th1 conditions, and GATA3-deficient cells fail to produce IL-4/IL-5/IL-13. This supports GATA3 emerging as the top selective Th2 suppressor in our screen.
- The IL4/STAT6 axis sits upstream of GATA3: IL-4 -> IL-4Ra -> STAT6 phosphorylation induces high GATA3, and IL-4/IL-4Ra/STAT6 signaling forms a positive feedback loop stabilizing the Th2 phenotype. STAT6 is correctly paired with GATA3 as a Th2 driver.
- Th2 markers IL4, IL5, IL13 (the IL5-IL13-IL4 cytokine locus bound/modified by GATA3) and CCR4 are validated: IL-4/IL-5/IL-13 production is restricted to the CCR4+ memory CD4+ population; CCR4 is a useful surface marker of circulating Th2 effectors.
- Th1 markers are validated: T-bet/TBX21 (T-box factor on chr17) controls IFN-gamma; IL-12 signaling via STAT4 stabilizes T-bet/the Th1 phenotype; CXCR3 marks circulating IFN-gamma-producing Th1 effectors.

**Concerns:**
- 'Master regulators = GATA3 + STAT6' slightly conflates two roles: GATA3 is the lineage-defining transcription factor, whereas STAT6 is the upstream signal transducer of the IL-4 cue. GATA3 can drive Th2 commitment STAT6-independently via autoactivation (Stat6-deficient cells reconstituted by GATA3), so they are not interchangeable co-master TFs.
- IL4R (IL-4Ra) is a weaker/looser Th2 marker than IL4/IL5/IL13/CCR4: IL-4Ra is broadly expressed across many hematopoietic and non-immune cells (it is the drug target precisely because it is shared and widespread), so its inclusion in the Th2-up arm may add noise or reflect general activation rather than Th2 identity specifically.
- The Th1/Th2 dichotomy is a simplification of a broader landscape (Th17, Treg, Tfh, Th9) and CD4 T cells exhibit plasticity; 'reciprocal lineages' is correct for the T-bet/GATA3 axis but the two arms are not the only fates, which is worth acknowledging given the positive Th1-Th2 arm correlation we observed.
- Type-2 disease is not purely Th2-cell-driven: ILC2s and other type-2 sources contribute in vivo, and asthma is heterogeneous with T2-high and non-type-2 (T2-low) endotypes. The in vitro CD4+ CRISPRi system captures the Th2-cell arm only, so mapping hits to 'allergy/asthma' disease relevance should be hedged.
- GATA3 has T-cell-lineage-wide roles beyond Th2 (required for early T-cell/CD4 development and expressed in Tregs and ILC2s), so a GATA3 knockdown could exert broad effects; its appearance as the top 'selective' hit is biologically expected but does not by itself prove Th2-selectivity of the assay.

**Corrections to make:**
- Frame STAT6 as the upstream IL-4 signal transducer feeding GATA3, not as a co-equal 'master regulator' transcription factor with GATA3.
- Consider down-weighting or annotating IL4R in the Th2-up arm, since IL-4Ra is broadly expressed and less Th2-specific than IL4/IL5/IL13/CCR4.

**Sources:**
- T-bet and GATA3 are mutually exclusive master regulators that directly cross-repress; T-bet binds GATA3 and bl — _Nat Commun 2012, T-bet and GATA3 orchestrate Th1 and Th2 differentiation (PMC3535338); ScienceDirect T-bet overview_
- GATA3 is master regulator: enforced expression drives Th2 under Th1 conditions; deficiency abolishes IL-4/IL-5 — _Int Immunol 2011, Updated view on GATA3-mediated regulation of Th1/Th2 (PMC3123974)_
- IL-4->IL-4Ra->STAT6 induces GATA3; IL-4/STAT6 positive feedback stabilizes Th2; GATA3 STAT6-independent autoac — _Immunity 2000, Stat6-Independent GATA-3 Autoactivation (Ouyang et al.); PMC3557721 STAT6-dependent and -independent mechanisms_
- Th1 requires T-bet/TBX21 controlling IFN-gamma; IL-12/STAT4 stabilizes T-bet; STAT4 in Th1 — _ScienceDirect Transcription Factor T-bet overview; JEM 2018 STAT4 and T-bet (Rockefeller)_
- Th1 express CXCR3/CCR5, Th2 express CCR4/CCR3; IL-4/5/13 restricted to CCR4+ and IFN-gamma to CXCR3+ memory CD — _J Leukoc Biol 2000 Yamamoto et al. (PMID 11037980); Bonecchi et al. J Exp Med 1998 (PMID 9419219)_
- Dupilumab is anti-IL-4Ra mAb blocking both IL-4 and IL-13 (shared IL-4Ra chain); dual blockade required to inh — _JACI 2019, Dual blockade of IL-4 and IL-13 with dupilumab required to broadly inhibit type 2 inflammation (S0091-6749(19)32117-7); McCann 2024 Clin Transl Sci dupilumab MOA_


### Known-regulator direction reframe — **mostly supported**

**Holds up:**
- GATA3 is the master POSITIVE regulator of Th2 (induced by IL-4/STAT6, drives Th2 cytokines while suppressing Th1). Its knockdown lowers Th2 and de-represses Th1 - correctly classified as an activator.
- STAT6 is a POSITIVE regulator: IL-4/STAT6 drives GATA3 expression and Th2 commitment; STAT6-deficient cells default to a Th1-like response. Knockdown lowers Th2 - correctly an activator.
- IL4R (IL-4 receptor alpha) is a POSITIVE regulator: it transduces the IL-4 -> STAT6 -> GATA3 signal that promotes Th2. Knockdown lowers Th2 - correctly an activator.
- RARA (retinoic acid receptor alpha) is a POSITIVE regulator: ATRA/RARalpha signaling promotes IL-4/IL-5/IL-13 and increases Th2 output; RAR-alpha-selective agonists reproduce the pro-Th2 effect. Knockdown lowers Th2 - correctly an activator.
- ICOS is a POSITIVE costimulatory regulator of Th2 (ICOS deficiency impairs Th2 cytokine production); knockdown lowers Th2 - reasonably classified as an activator, though its effect is broadly costimulatory rather than Th2-specific.

**Concerns:**
- The clean 'activator vs repressor' dichotomy oversimplifies the NuRD biology. CHD4 is explicitly BIMODAL (Hosokawa et al., PNAS 2013): the Gata3/Chd4/p300 complex ACTIVATES Th2 cytokines (IL-4/IL-5/IL-13) while the Gata3/Chd4-NuRD complex REPRESSES Tbx21. Chd4 knockdown decreases IL-4+ cells (18.3%->7.9%) AND increases IFN-g+ cells (3.7%->13.8%). So CHD4 KD suppresses Th2 too - it is not a pure Th1-repressor, and could legitimately score on the Th2-down arm.
- SETDB1 is also mixed, not a clean Th1-repressor: Setdb1 loss enhances Th1 priming BUT also IMPAIRS Th2 commitment (via de-repression of ERVs that act as Th1 enhancers). So SETDB1 KD would push the Th2 arm down as well as the Th1 arm up - it does both, contradicting the 'induces Th1 rather than suppress Th2' phrasing.
- MBD2 is genuinely context-dependent/conflicting in the literature rather than a clean repressor: some studies show MBD2 silencing in CD4+ T cells INCREASES the Th2 ratio and IL-4 (negative regulator of Th2 / represses Th1-STAT1-IFN-g axis), while others show Mbd2-/- dendritic cells are markedly IMPAIRED in Th2 induction (positive regulator of Th2). Its direction cannot be asserted with confidence.
- Several 'activators' (GATA3, STAT6) also actively REPRESS Th1, so their KD is expected to raise the Th1 arm somewhat too - the assumption that a true selective Th2 suppressor leaves Th1 perfectly flat (|z|<1) may be too strict even for genuine positive Th2 regulators.

**Corrections to make:**
- TRAF3 is MISCLASSIFIED. The reframe lists TRAF3 as a negative regulator whose knockdown should induce Th1, but the direct T-cell evidence (Lu/Bishop lab, J Biol Chem 2024) shows TRAF3 ENHANCES STAT6 activation and PROMOTES Th2 skewing, and TRAF3 deficiency IMPAIRS Th2 (and Th1) differentiation. TRAF3 is therefore a POSITIVE Th2 regulator - its knockdown should LOWER Th2, behaving like the activators (GATA3/STAT6), not the repressors. The 'negative regulator' label likely derives from TRAF3's role in B-cell/alternative-NF-kB signaling, which does not transfer to the T-cell Th2 program.
- CHD4 should not be placed cleanly on the repressor side. Because it is bimodal (activates Th2 cytokines and represses Th1), CHD4 KD is expected to suppress Th2 as well as de-repress Th1; it can plausibly appear as a Th2 suppressor for legitimate reasons.
- SETDB1's expected phenotype should be stated as BOTH lowering Th2 and raising Th1 (mixed), not 'induces Th1 rather than suppress Th2.'
- MBD2's direction should be flagged as unresolved/context-dependent rather than asserted as a Th1-repressor.

**Sources:**
- GATA3 is the master positive regulator of Th2, induced by IL-4/STAT6, drives Th2 cytokines and suppresses Th1 — _Tindemans et al., updated view on GATA3 regulation of Th1/Th2, PMC3123974; Transcriptional regulation of Th2 differentiation, PMC3477614_
- STAT6 promotes GATA3 and Th2; STAT6/IL-4 knockouts give Th1-like responses — _STAT6-dependent mechanisms in Th2 polarization, PMC3557721; STAT6-mediated displacement of polycomb by trithorax to maintain GATA3, JEM 207:2493_
- RARalpha (RARA) mediates pro-Th2 effects; ATRA/RAR-alpha agonists promote IL-4/IL-5/IL-13 and increase Th2 out — _Retinoic Acid Receptor-alpha mediates human T-cell Th2 cytokine production, BMC Immunology 9:16 / PMC2394516; ATRA and Ro415253 regulate IL-5+ Th2 cells, PMC3882882_
- IL4R alpha binds IL-4 to promote Th2 differentiation — _IL4R GeneCards; Transcriptional regulation of Th2 differentiation, PMC3477614_
- CHD4 is bimodal: Gata3/Chd4/p300 activates Th2 cytokines, Gata3/Chd4-NuRD represses Tbx21; Chd4 KD decreases I — _Hosokawa et al., Functionally distinct Gata3/Chd4 complexes establish Th2 identity, PNAS 2013, PMC3606997_
- SETDB1 loss enhances Th1 priming but impairs Th2 commitment via ERV de-repression at Th1 enhancers — _Adoue et al., SETDB1 controls Th cell lineage integrity by repressing ERVs, Immunity 2019, PMC/PubMed 30737147_


### Novelty & prior art — **problematic**

**Holds up:**
- Our core method is sound but is essentially what Zhu & Dann et al. already did. Their released analysis code (src/4_polarization_signatures/pert2state_polarization.ipynb) uses the SAME external signature we did (Ota et al. 2021 Th2-vs-Th1), splits it into an up-arm and a down-arm (signature_gs_up / signature_gs_down), and scores each single cell separately as 'score_th2' (up genes) and 'score_th1' (down genes) with an NTC-normalized score_genes routine (score_genes_ntc_norm). This is exactly our Th2-arm / Th1-arm split.
- The 2D decomposition we treat as our angle is already in their paper. They compute per-perturbation mean score_th2 vs score_th1 and plot them on a 2D scatter with quadrant lines at x=0/y=0 (their Supplementary Fig 17, 'Effect of predicted polarization regulators on Th1 and Th2 genes'), and separately examine each perturbation's effect on Th1 genes vs Th2 genes. That is the same 2-arm / 2D scoring picture we built.
- GATA3 as the top Th2 hit is expected and reproduces theirs, not a novel discovery. GATA3 is the first entry in their curated th1_th2_known_regulators.yaml (th2 list) and is an explicitly highlighted/labeled regulator in their pert2state notebook; it is the textbook master Th2 regulator recovered by prior genome-wide CRISPR screens in T helper cells (Freimer/Marson 2022).
- Our concern about a global/magnitude confound is legitimate and shared by the authors. They guard against a closely related confound by using an independent activation signature (Arce et al. 2024, Rest-vs-Stim) as a negative control (known Th2/Th1 regulators should NOT be prioritized by activation) and K562 perturb-seq as a second negative control, and they check that polarization scores are not just tracking the activation axis.
- Using separate up/down gene-set scores for a bidirectional signature is a well-established, correct technique, so our implementation is not methodologically wrong — it is just not new (see corrections/sources).

**Concerns:**
- Novelty is low. The specific combination we pitched as our angle - split the Ota 2021 Th2-vs-Th1 signature into arms, score every genome-scale CRISPRi perturbation on both arms, decompose in 2D, and land on GATA3 - is a near-duplicate of the published Fig 4 / pert2state analysis in the very paper we are analyzing, using the identical discovery signature. Anyone reading their supplement + code would see this.
- The 2-arm / up-down decomposition of a bidirectional signature is a decades-old standard, not an innovation. Connectivity-Map connectivity scores are explicitly defined as an up-score plus a down-score computed on separately-supplied up and down gene lists; single-cell tools (UCell/pyUCell, scanpy score_genes) routinely score positive and negative gene sets separately. Framing this as a novel technique would be indefensible.
- Our claimed differentiator - selecting 'selective Th2 suppressors' by requiring the Th1 arm to stay flat (|z|<1) as a built-in control - is a modest reframing, not a new capability. The authors already visualize the same Th1-flat-vs-diagonal information in their 2D score_th2/score_th1 plot; they simply do not crown a formal 'selective vs skewing' category. Our contribution is essentially adding an explicit flatness threshold and a magnitude/'sick-cell dampening' narrative on top of their existing decomposition.
- Their regulator classification is directional-axis-based (regs_class = positive / negative / control, from signed model coefficients), i.e. an inherently 'skewing along the Th2-Th1 axis' model. So while they did not formalize 'selective suppression vs skewing' as competing categories, their whole framing is skewing-centric and our 'selective suppression' label sits inside their existing 2D data rather than beside it.
- Risk of reinventing with weaker statistics: their pipeline uses a trained, cross-dataset-validated linear model (train on Ota, reconstruct held-out genes in Hollbacher 2021, replicate across donors and culture conditions) with negative controls. Our z-score thresholding on two arm scores is a coarser version of the same idea and would be judged against their more rigorous model.

**Corrections to make:**
- Drop or heavily soften the novelty claim. We should not present 'split the Th2-vs-Th1 signature into arms and score both' or the 2D decomposition as our idea - Zhu & Dann et al. already do exactly this with the same Ota 2021 signature (score_th2/score_th1, Supplementary Fig 17). Position our work as a re-analysis/reframing, at most contributing an explicit selective-suppression flatness criterion, not a new method.
- Re-examine the GATA3-as-selective-Th2-suppressor claim; it likely conflicts with canonical biology. The classical reciprocal Th1/Th2 model holds that loss of GATA3 de-represses IFNG/T-bet and actively SKEWS toward Th1 (e.g. Gata3 loss converts Notch into a Th1 inducer; GATA3 directly represses Th1 factors). A knockdown that pushes Th2 down while leaving the Th1 arm flat (our selective definition) is biologically surprising for GATA3 and may be an artifact of the resting / short-stimulation human context, low Th1-arm expression at baseline, or our flatness threshold - flag this explicitly rather than presenting GATA3 as a clean selective suppressor.
- State the correct prior art for the technique: attribute up/down-arm decomposition to Connectivity Map (up-score + down-score) and to UCell/scanpy-style separate positive/negative gene-set scoring, so reviewers do not think we are claiming it.
- Reframe the 'sick-cell dampening / global magnitude' confound relative to their controls. The authors already control an analogous confound via an activation signature and K562/negative controls; we should either adopt an equivalent negative control (activation axis) or acknowledge that using the Th1 arm alone as the control is weaker than their approach, rather than presenting the confound insight as novel.

**Sources:**
- Zhu & Dann et al. split the Ota 2021 Th2-vs-Th1 signature into up/down arms, compute per-cell score_th2 (up) a — _github.com/emdann/GWT_perturbseq_analysis_2025 — src/4_polarization_signatures/pert2state_polarization.ipynb and polarization_signature.ipynb (signature_gs_up/down, score_th2/score_th1, regs_class positive/negative/control)_
- Fig 4C-H and Supplementary Figs 16-18 are the Th2/Th1 polarization-regulator analysis; Suppl Fig 17 is 'Effect — _github.com/emdann/GWT_perturbseq_analysis_2025 — metadata/figure_map.md and metadata/th1_th2_known_regulators.yaml_
- Their pert2state model trains on Ota 2021, validates by held-out-gene reconstruction in Hollbacher 2021, and u — _github.com/emdann/GWT_perturbseq_analysis_2025 — pert2state_polarization.ipynb markdown ('Train on discovery signature (Ota2021)', 'Validate ... Hollbacher2021', 'activation signature ... as a negative control')_
- The paper nominates regulators of Th1 and Th2 polarization by modeling perturbation signatures against populat — _bioRxiv 2025.12.23.696273 (Zhu, Dann, ... Pritchard, Marson) — abstract; biorxiv.org/content/10.64898/2025.12.23.696273v1_
- Decomposing a bidirectional signature into separately-scored up and down gene lists is a standard technique: C — _Connectivity Map up/down connectivity-score method; UCell and pyUCell (PMC12925249); scanpy score_genes_
- Canonical biology: GATA3 loss de-represses Th1 (IFNG/T-bet) and drives Th1 skewing rather than neutral loss of — _GATA-3 promotes Th2 and inhibits Th1-specific factors (Nature Cell Research, 7310002); Gata3 loss turns Notch into a Th1 inducer (PMC2062505); genome-wide CRISPR in T helper cells confirms GATA3/STAT6/IRF4 as Th2 regulators (PMC6370901)_


### Lead: ARNT — **mixed**

**Holds up:**
- There is a genuine, recent mechanistic link between ARNT-dependent HIF signaling and the Th2/GATA3 program: HIF2alpha (EPAS1) promotes Th2 differentiation and forms a HIF2alpha-GATA3 circuit, with EPAS1 directly bound by GATA-3 in Th2 cells (Cell/Immunity 2024, S1074-7613(24)00496-5; helminth paper PMC11761574).
- ARNT (HIF1-beta) is the OBLIGATE class-I dimerization partner for HIF2alpha/EPAS1 (and HIF1alpha and AhR). Because HIF2alpha is non-functional without ARNT, ARNT knockdown would be expected to abrogate the pro-Th2 HIF2alpha-GATA3 circuit, giving a coherent mechanism for ARNT KD lowering Th2/GATA3/IL4. This raises the prior above baseline that the hit is on-pathway rather than random.
- The Th2-selective (not Th1-inducing) prediction is mechanistically reasonable: HIF2alpha is the Th2-associated HIF paralog, whereas HIF1alpha is tied to Th17/glycolysis and Treg/effector-in-hypoxia biology, so loss of the ARNT/HIF2alpha axis need not push cells toward Th1.
- HIF2alpha-deficiency has been shown to IMPAIR Th2 differentiation and reduce Th2-mediated immunity / asthmatic inflammation in mouse models, matching the direction (ARNT/HIF2alpha loss -> less Th2) our pipeline nominated.

**Concerns:**
- Context mismatch: the HIF2alpha-Th2 link is established in HYPOXIC / tissue / intestinal-helminth settings and is hypoxia- or genetic-activation-dependent. Whether the ARNT/HIF2alpha axis meaningfully drives GATA3/IL4 in a 48hr in-vitro Stim of normoxic peripheral blood CD4+ T cells (typical Perturb-seq culture at ~21% O2, no HIF stabilization) is unproven and is the main reason to down-weight the lead.
- Pleiotropy / artifact risk is high precisely because ARNT is broadly and constitutively expressed and is the shared partner for HIF1alpha, HIF2alpha AND AhR. Its knockdown collapses multiple metabolic/stress pathways at once, so a 'selective' Th2 drop could reflect Th2 cells' higher metabolic/hypoxic-program dependence rather than a GATA3-specific effect. The flat Th1 arm mitigates a pure global sick-cell explanation but does NOT exclude a Th2-selective metabolic-fitness confound that mimics on-target selectivity.
- Countervailing pharmacology: AhR ACTIVATION suppresses Th2/GATA3, so losing the AhR arm via ARNT KD would be predicted to INCREASE Th2. The net effect depends on which ARNT partner dominates in this condition (AhR is reported to be largely ligand-dependent / functional mainly in Th17, so the HIF arm may dominate absent exogenous AhR ligand) - but this is an assumption, and it makes the sign of the ARNT effect genuinely context-dependent.
- Evidence is largely mouse and tissue-resident/pathogenic Th2; direct human primary-CD4 loss-of-function data for ARNT specifically on IL4/GATA3 is thin. No paper directly tests ARNT (as opposed to EPAS1/HIF2alpha) knockdown on the Th2 program.

**Corrections to make:**
- Frame the mechanistic hypothesis as ARNT-via-HIF2alpha (EPAS1), not ARNT-via-AhR or generic HIF1alpha - HIF2alpha is the Th2-relevant partner and gives the cleanest, direction-correct rationale. Any writeup should name EPAS1/HIF2alpha as the presumed effector.
- Calibrated plausibility: MODERATE, ~0.3-0.4. Above the ~random-hit baseline because a specific, recent, direction-consistent HIF2alpha-GATA3 mechanism exists, but held down by the normoxic short-stim context mismatch and ARNT's pleiotropy/fitness-confound risk. Do not present ARNT as a high-confidence GATA3-like selective suppressor.

**Sources:**
- HIF2alpha (EPAS1) promotes Th2 differentiation via a HIF2alpha-GATA3 circuit; EPAS1 is directly bound by GATA- — _Hypoxia-inducible factor 2alpha promotes pathogenic polarization of stem-like Th2 cells, Immunity 2024 (cell.com/immunity/fulltext/S1074-7613(24)00496-5)_
- EPAS1/HIF2alpha is highly expressed in intestinal CD4+ T cells during helminth infection; hypoxia or genetic H — _Hypoxia-inducible factor 2alpha promotes protective Th2 cell responses during intestinal helminth infection, PMC11761574 / bioRxiv 2025.01.09.631414_
- HIF-2 is a heterodimer of oxygen-sensitive HIF-2alpha and its obligate partner ARNT (HIF-1beta); ARNT is const — _Bidirectional modulation of HIF-2 activity, Nat Chem Biol 2019 (s41589-019-0234-5); HIF-1 review PMC1959117_
- AhR requires ARNT as heterodimer partner; AhR activation suppresses Th2 differentiation and can down-regulate  — _Aryl Hydrocarbon Receptor-Mediated Perturbations in Gene Expression during CD4+ T-cell Differentiation, PMC3412388; Cell Research cr200863_
- Confirming experiment design rationale: ARNT is obligate partner for HIF1alpha, HIF2alpha and AhR, so epistasi — _Synthesis of the above sources (ARNT pleiotropy)_


### Lead: ELAVL1 — **mostly supported**

**Holds up:**
- HuR/ELAVL1 directly binds AU-rich elements (AREs) in the 3'UTRs of GATA3, IL4, and IL13 mRNAs and stabilizes them, established by RNP-IP, biotin pull-down, and mRNA half-life assays (Techasintana/Atasoy et al., PMC5801757; Stellato lab).
- There is a specific, well-documented mechanistic link between HuR and the Th2 program: HuR coordinately regulates the master Th2 TF GATA3 plus its downstream cytokines IL4/IL13 as an ARE-linked regulon, so knocking down HuR is expected to lower the Th2 axis — consistent with our pipeline nominating ELAVL1 as a Th2 suppressor.
- Direct experimental evidence for Th2-over-Th1 SELECTIVITY exists: HuR silencing reduced GATA3 transcript stability and cut IL-13 mRNA half-life (5.1h to 2.9h) while IFN-gamma mRNA was reportedly unaffected; HuR overexpression raised GATA3/IL4/IL13 with NO increase in IFN-gamma in either Th1 or Th2 conditions. This convergence with our arm-split (Th2 arm down, Th1 arm flat) is a genuine point in the lead's favor.
- A gene-dosage/dose-dependent relationship is reported: even ~20% changes in HuR level significantly moved GATA3 mRNA and stability, and heterozygous conditional-KO Th2 cells showed reduced Gata3/Il4/Il13 mRNA — meaning partial CRISPRi knockdown could plausibly produce a measurable Th2-specific effect without full-cell collapse.
- Conditional HuR KO in CD4+ T cells causes defects in Th2 differentiation specifically (loss of IL-2 homeostasis, JAK-STAT/Th2 defects), so the differentiation-level phenotype is not just a cytokine mRNA-stability artifact (Chen et al., Mol Med 2013; Springer).

**Concerns:**
- Global-artifact risk is real and non-trivial: HuR is a pan-cellular mRNA-stability hub with hundreds of ARE targets. Full/strong HuR loss impairs core T-cell activation, proliferation, and survival, and also stabilizes Foxp3 (Treg), IL-2, and Th17 program mRNAs. Strong CRISPRi knockdown could push cells toward the 'sick-cell' global-dampening regime our own analysis flagged as the dominant confound (Th2 and Th1 arms +0.5 correlated).
- The Th2-over-Th1 selectivity claim is not clean at the mechanism level: HuR ALSO stabilizes canonical Th1/pro-inflammatory ARE-cytokine mRNAs — IFN-gamma and TNF-alpha (LFA-1/Vav1/p38 pathway, PMC3012057). So HuR is not intrinsically Th2-private; the apparent selectivity in the Stellato papers may reflect context/polarization state rather than an absolute Th2-only wiring.
- The strongest selectivity evidence comes largely from one lab (Stellato/Atasoy) and from HuR-overexpression and heterozygous/partial-loss systems, not from the strong loss-of-function regime a CRISPRi screen produces — the effect direction may hold but the Th1-sparing may not survive stronger knockdown.
- Our pipeline's Th1-arm-flat criterion could still be satisfied trivially if IFN-gamma/Th1 genes are simply less ARE-dependent at baseline in this culture condition, i.e. selectivity could be a substrate-availability quirk rather than a druggable Th2-specific dependency.

**Corrections to make:**
- Do not describe HuR/ELAVL1 as a Th2-specific factor; it is a global ARE-binding mRNA stabilizer that happens to have a disproportionately characterized effect on the GATA3/IL4/IL13 regulon. The lead is plausible but the mechanism is 'global regulator with a strong Th2 sub-module,' not 'selective Th2 gene.'
- Frame the Th1-arm control as necessary but not fully sufficient here: because HuR can also stabilize IFN-gamma/TNF, a flat Th1 arm in our data is informative but does not by itself exclude the global-dampening confound at high knockdown.

**Sources:**
- HuR binds AREs in GATA3, IL4, IL13 3'UTRs and stabilizes them; HuR silencing reduces GATA3 stability and IL-13 — _https://pmc.ncbi.nlm.nih.gov/articles/PMC5801757/_
- HuR coordinately regulates GATA-3 and Th2 cytokine gene expression in a dose-dependent manner — _https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3643703/_
- Conditional HuR KO in CD4+ T cells reveals gene-dosage effect on cytokine production and Th2 differentiation d — _https://link.springer.com/article/10.2119/molmed.2013.00127_
- HuR also stabilizes Th1-type cytokine mRNAs IFN-gamma and TNF-alpha via LFA-1/Vav1/Rac/p38/MKK3 signaling (evi — _https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3012057/_
- HuR is a global regulator: stabilizes Foxp3 in Tregs and strengthens Th17 differentiation/CD4 activation signa — _https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8357502/_
- Transcriptome-wide identification of direct and indirect HuR targets in activated CD4+ T cells (hundreds of AR — _https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4498740/_


### Methods red-team — **mixed**

**Holds up:**
- Using the Th1 arm as a built-in negative-direction control and explicitly naming global 'sick-cell' dampening as the dominant confound is the right instinct; the +0.5 arm-arm correlation is real and correctly diagnosed as a magnitude artifact rather than biology.
- Preferring a residual-on-control over a raw DE-breadth penalty is defensible: a breadth penalty would wrongly punish strong bona fide regulators like GATA3 that legitimately move many genes (notebooks/04_score.py comment is correct on this specific tradeoff).
- The gate-threshold robustness grid (TX in {-1.5,-2,-2.5} x TY in {0.5,1,1.5}, gate_robustness 0..9 in 03_credibility.py, and the 07_qc_audit sweep) is good practice and partially mitigates the arbitrariness of the hard cutoff.
- Requiring on-target KD confirmation (ontarget_significant, negative effect, frac_signif_guides>=0.5) plus cross-donor and cross-guide stability flags is a sound orthogonal-evidence layer that most naive Perturb-seq screens skip.
- Recovering GATA3 as the top hit and checking known-regulator recall/specificity is a reasonable sensitivity calibration, and separating directional 'activators' from 'repressor-complex' known genes (TH2_ACTIVATORS set) shows awareness that the known-gene list is directionally mixed.

**Concerns:**
- SCORING IS SELF-CONTAINED, NOT COMPETITIVE: the arm score is an unweighted mean of per-gene DE z-scores over signature genes. This measures absolute movement of the signature, so any global transcriptional shift (sick cell) moves both arms together. The +0.5 correlation is therefore largely manufactured by the scoring choice, not a fact of nature to be regressed away afterward. Competitive/rank-based scores (AUCell, singscore, fgsea/CAMERA-style) normalize against the rest of the genome and would remove most of this confound at the scoring step.
- NO PROPER NULL / NO FDR: z<-2 is a tail of the across-perturbation distribution, whose center is the mean over mostly-inert perturbations, not a true no-effect null. With thousands of perturbation x condition rows and a nominal ~2.3% left tail, dozens of the 172 'selective' calls are expected by chance. There is no permutation/empirical FDR and no comparison of 172 to a label-shuffled null, so the count is uncalibrated.
- 'Th1 flat' (|th1|<1) ACCEPTS THE NULL: |z|<1 conflates 'genuinely no Th1 effect' with 'Th1 estimated too noisily to reach 1'. A perturbation with a weak/underpowered Th1 measurement passes the flatness gate spuriously, inflating apparent selectivity. Flatness needs an equivalence test (TOST) with the Th1 uncertainty, not a bare threshold.
- TH1 ARM IS A BIASED, NOISY PROXY FOR GLOBAL MAGNITUDE: it is a small biased gene subset, not total DE burden. Regressing Th2 on Th1 (a) removes only the confound component that projects onto Th1 genes and (b) also removes real reciprocal Th1/Th2 biology, so the residual can MANUFACTURE selectivity for a perturbation that genuinely raises Th1. Because Th1 is measured with error, OLS slope is attenuated (regression dilution), so it under-corrects the confound it targets.
- DOUBLE-DIPPING / SELECTION BIAS: perturbations are selected for extreme Th2, then Th2 effect (residual) is ranked and reported on the same data. This is winner's-curse — top hits' effect sizes are inflated. Also the residual is fit on the full df but the gate already restricts to |th1|<1, so within the retained band there is little Th1 variance left and th2_resid ~= th2_arm — the 'control' does little where it is actually applied.
- PSEUDOREPLICATION: rows are perturbation x condition; the same gene appears up to 3x (Rest/Stim8/Stim48). The across-perturbation z-scoring, the OLS, and the gate all treat these as independent, ignoring within-gene clustering and the different dynamic range per condition (one global OLS line across conditions).
- SIGNATURE-COUNT TUNING: membership thresholds (adjp<0.05, |lfc|>0.5) are explicitly described as 'tunable to reproduce teammate counts' (172/4). Fitting gene-set definition to hit a target number is a garden-of-forking-paths / analytic-circularity risk.
- EXTERNAL SIGNATURE TRANSFER: Ota-2021 is bulk and from a different protocol/cohort; genes are lost in mapping and some 'Th2-up' genes are generic activation/proliferation markers that reintroduce the magnitude confound. The dataset's OWN matched polarization signature (present in data/) is the better-matched primary and was not used as such.
- n_DE>=10 IS A POWER FILTER IN DISGUISE: it correlates with effect magnitude and with per-perturbation cell count / KD efficiency, so it preferentially removes subtle-but-selective regulators and biases the retained set toward strong global movers — partially reintroducing the very confound being controlled. nan_to_num imputing missing gene z-scores to 0 also biases arm means toward flat/attenuated.
- BIOLOGICAL: Th2-vs-Th1 is not a clean 1D axis in CD4 cells. A knockdown can lower the Th2 arm by diverting cells to Th17/Treg/Tfh or into apoptosis/translation stress, not by specific Th2 inhibition. With only Th1 as a control, 'selective Th2 suppressor' cannot be distinguished from lineage diversion or a sick cell whose most dynamically expressed (Th2) genes fall first. No viability/proliferation or other-lineage arm rules this out; no functional (IL-4/5/13) readout confirms transcriptional -> functional suppression.

**Corrections to make:**
- Move the magnitude correction from a post-hoc regressor to the scoring step: replace the mean-of-z self-contained score with a competitive/rank-based enrichment (AUCell, singscore, or an fgsea/CAMERA/ROAST-style rotation test that normalizes against matched random gene sets). This removes most of the +0.5 confound a priori instead of trusting a noisy Th1-proxy regression.
- Build a real null from non-targeting / safe-harbor control guides: define arm z-scores and the selectivity threshold relative to the control-guide distribution, and compute an empirical/permutation FDR (shuffle signature labels or perturbation labels) so the 172 count is reported as q-value-controlled rather than a raw tail.
- Replace the hard AND gate with a continuous, uncertainty-aware selectivity statistic: per-perturbation Th2 and Th1 effects with SEs (from guide/donor replicates), test Th1 flatness by equivalence (TOST), and rank by a Th2-minus-Th1 contrast with confidence intervals — avoid dichotomizing continuous scores.
- If keeping a regression control, residualize on a DIRECTLY measured global-magnitude covariate (total DE burden, mean|z|, PC1 of the z matrix, and/or KD strength), fit WITHIN condition, and use total-least-squares/partial correlation to avoid regression-dilution. Report both raw and controlled ranks side by side.
- Use the dataset's own matched polarization signature as the primary readout and Ota-2021 as orthogonal cross-validation; require concordance across >=2 signatures (Ota + Hollbacher + Diff043 are already in combined_Th2_vs_Th1_signature.csv). Freeze membership thresholds a priori and show full sensitivity instead of tuning to reproduce 172/4.
- Add cross-validation to beat the winner's curse: fit the gene set / score on half the guides (or donors) and evaluate selectivity on the held-out half; make cross-guide and cross-donor replication the PRIMARY evidence for each hit rather than a secondary flag, and report shrinkage-adjusted effect sizes.
- Add orthogonal control arms — Th17/Treg/Tfh lineage, cell-cycle/proliferation, apoptosis, ribosome/translation — and redefine 'selective' as Th2-down while Th1 AND other-lineage AND viability arms are all flat (by equivalence). This is the single biggest fix for the lineage-diversion / sick-cell biological threat.
- Add a dose-response causal check: test that Th2 suppression scales monotonically with per-guide KD efficiency (an MR-style within-perturbation gradient), which is much stronger evidence of specific causation than a single thresholded z.
- Fix pseudoreplication: model gene as a random/grouping factor (or aggregate to one estimate per gene with condition as a covariate) in any z-scoring, regression, or inference so the 3 conditions per gene are not treated as independent observations.
- Treat GATA3 recovery as sensitivity only, not validation of novel hits; report specificity as the empirical false-selective rate under the permuted null, and plan a functional confirmation (IL-4/IL-5/IL-13 cytokine or protein readout) for top novel candidates before claiming Th2-selective suppression.

**Sources:**
- Self-contained gene-set scores (mean of member statistics) are inflated by global shifts and inter-gene correl — _Wu & Smyth CAMERA (Nucleic Acids Res 2012) and Goeman & Buhlmann (Bioinformatics 2007) on competitive vs self-contained gene-set testing_
- Rank/rotation-based enrichment normalizes against the rest of the transcriptome and controls inter-gene correl — _fgsea (Korotkevich et al. 2021); ROAST rotation test (Wu et al. 2010); AUCell/singscore for single-cell signature scoring (Aibar SCENIC 2017; Foroutan singscore 2018)_
- Accepting the null ('flat') from a non-significant test is invalid; equivalence testing (TOST) is required to  — _Lakens, Two One-Sided Tests (TOST) equivalence testing, Soc Psychol Personal Sci 2017_
- Selecting features on an extreme statistic then re-estimating that statistic on the same data biases effects u — _Kriegesk1el 'circular analysis' / double-dipping (Nat Neurosci 2009); winner's-curse effect-size inflation literature_
- Regressing on an error-laden covariate attenuates the slope (regression dilution), so a noisy proxy under-corr — _Standard errors-in-variables / attenuation bias result (Fuller, Measurement Error Models)_
- Perturb-seq best practice uses non-targeting control guides as the null and controls FDR across the perturbati — _Replogle et al. genome-scale Perturb-seq (Cell 2022); Dixit/Adamson Perturb-seq framework (Cell 2016)_




## Part C — Hardened re-analysis (acting on the methods red-team)

Implemented the four highest-impact fixes and re-ran over the full matrix (`notebooks/10_hardened.py`):

1. **Competitive rank-based scoring** (singscore-style) instead of mean-of-z: arm correlation
   **+0.54 → +0.18**. Confirms most of the confound was a scoring artifact.
2. **Permutation null → empirical FDR:** 2-arm selective = 420; expected under random
   same-size gene sets ≈ 525 → **FDR ≈ 1.25**. The selective
   category is **not enriched over chance** (Th1/Th2 reciprocity means Th2-down usually raises Th1).
3. **Multi-lineage + proliferation control arms** (Th1/Th17/Treg/cell-cycle, from the dataset's own
   vs-Th0 signatures): requiring all flat leaves 41 (FDR ≈ 5.51).
4. **Two-signature concordance** (Ota + matched Th2-vs-Th0): 7 genes pass everything
   (BRPF1, DALRD3, GLIS2, RABEPK, RELL2, SLC30A5, UQCR11); **none of the earlier 21 high-confidence genes survive**.

**GATA3 under proper scoring is a Th1-skewer, not a selective suppressor** (Th1-vs-Th0 arm +2.8),
consistent with canonical biology — invalidating the earlier calibration claim.

**Conclusion:** the naive selective-suppressor atlas does not survive rigorous statistics. Report this
as a calibrated negative result. To make any positive claim would require: competitive scoring as the
primary score, a control-guide (non-targeting) permutation FDR, equivalence (TOST) tests for arm
flatness with per-guide/donor SEs, and a functional IL-4/5/13 confirmation of top candidates.
