# Mechanistic dossier: CBX5 (HP1α)

**Screen summary (Zhu & Dann et al. 2025, genome-scale CRISPRi Perturb-seq, primary human CD4⁺ T cells).** Composite confidence 0.729; selective only in **Stim48hr** (1/3 conditions). best th2_arm −0.431 (Th2 program down); th1_arm at best +0.122 (slightly positive — flagged). Curated markers: th2_marker_z −1.07, th1_marker_z −0.17, cellcycle_z +0.57, global_mag 1.12. On-target KD z −27.49 (strong self-silencing → real knockdown); cross-donor corr 0.808.

> **Caveat (must be stated).** These are Rest/Stim CD4⁺ T cells, **not polarized Th1/Th2 cells**. "Selective Th2 suppression" here is a statement about the knockdown's *transcriptional footprint* resembling loss of the Th2 program — a phenotypic inference from a single-perturbation screen, **not** a demonstrated mechanism or a functional polarization assay.

## 1. Gene identity & molecular function
CBX5 encodes **Heterochromatin Protein 1α (HP1α)**, one of three mammalian HP1 paralogs (α/CBX5, β/CBX1, γ/CBX3) [Genome Biology 2006, DOI 10.1186/gb-2006-7-7-228]. It is a non-enzymatic chromatin **reader/adaptor**: an N-terminal chromodomain binds histone H3 lysine-9 tri-methyl (H3K9me3), and a C-terminal chromoshadow domain homodimerizes and docks a wide range of chromatin partners [Genome Biology 2006]. Functionally it nucleates heterochromatin and gene silencing, but can also *activate* euchromatic genes during differentiation [Maeng et al. 2015, PMID 25588582]. It is a structural/scaffolding protein, not a sequence-specific transcription factor.

## 2. Selectivity hypothesis (each link labelled)
The most direct route runs *against* selectivity, so state it honestly:

- **ESTABLISHED:** In murine CD4 T cells the SUV39H1→H3K9me3→HP1α pathway maintains **silencing of the Th1 genes *Ifng* and *Tbx21*** to enforce Th2 lineage stability; HP1α-deficient Th2 cells de-repress Th1 genes when re-challenged, and SUV39H1 loss skews responses toward Th1 and reduces asthma pathology [Allan et al. 2012 Nature, PMID 22763435, DOI 10.1038/nature11173].
- **INFERRED (screen-consistent route):** CBX5 KD → broad H3K9me3-heterochromatin destabilization → the *transcriptional footprint* of the Th2 effector program (GATA3/IL4/IL5/IL13) contracts as part of a general program relaxation, rather than through HP1α acting *on* Th2 loci. This is consistent with global_mag 1.12.
- **Why Th1 stays flat here (INFERRED):** the canonical HP1α phenotype (Th1 de-repression) only manifests when the poised Th1 program is driven by a Th1 cytokine milieu [Allan 2012]. In non-polarized Rest/Stim cells there is no active Th1 program to de-repress, so th1_marker_z is ~0 — **the selectivity may be an artifact of context, not a true sparing of Th1.**

## 3. Directness call
**INDIRECT.** HP1α is a generic H3K9me3 reader with no reported sequence-specific binding to, or transcriptional activation of, the GATA3/IL4/IL5/IL13 loci. Its documented T-cell action is *repressive and at Th1 loci* [Allan 2012]. Any Th2-program contraction is therefore a downstream/indirect consequence of altered chromatin state, not HP1α directly operating the Th2 machinery.

## 4. Artifact scrutiny — honest verdict: **SOME CONCERN**
- **Proliferation collapse:** cellcycle_z +0.57 → **no** collapse; the Th2 signal is not a dying-cell artifact.
- **Global magnitude:** global_mag 1.12 is elevated, and HP1α is a pan-heterochromatin factor — the "Th2 down" footprint could partly reflect broad transcriptome destabilization rather than targeted Th2 loss.
- **Covert Th1-skew:** th1_marker_z −0.17 is reassuringly flat, **but** th1_arm +0.122 is positive — a faint echo of the expected Th1 de-repression. Given Allan 2012, this is the single most concerning signal: under Th2-polarizing conditions the same KD is *predicted* to de-repress Th1, which would break selectivity.
- Selective in only 1/3 conditions (Stim48hr) further weakens robustness. KD reality and reproducibility are strong; the *selectivity interpretation* is the weak link.

## 5. Confirming experiment (tests the SELECTIVITY claim)
Knock down CBX5 (CRISPRi/siRNA) in naive human CD4⁺ T cells; polarize under **Th2** conditions and read **IL4/IL5/IL13 + GATA3** vs **IFNG + TBX21** (intracellular flow + qPCR). **Critical selectivity arm:** re-culture the CBX5-KD cells under **Th1-driving** conditions and quantify IFNG/TBX21 de-repression [design per Allan 2012]. *Selective-suppressor hypothesis TRUE* iff Th2 cytokines fall **and** IFNG/TBX21 stay silenced even under Th1 challenge. Predicted from prior literature: Th2 destabilization **with** Th1 de-repression → selectivity **fails**. Complementary epistasis: CBX5+GATA3 double KD — no worse Th2 loss ⇒ acts through GATA3.

## 6. Citations (verified)
1. Allan RS, Zueva E, Cammas F, et al. *An epigenetic silencing pathway controlling T helper 2 cell lineage commitment.* Nature 2012;487:249-253. **PMID 22763435; DOI 10.1038/nature11173.** [VERIFIED — supports HP1α silencing of Ifng/Tbx21 & Th2 stability]
2. Lomberk G, Wallrath L, Urrutia R. *The Heterochromatin Protein 1 family.* Genome Biol 2006;7:228. **DOI 10.1186/gb-2006-7-7-228.** [VERIFIED — HP1 domains/function]
3. Maeng YS, Kwon JY, Kim EK, Kwon YG. *HP1α (CBX5) is a key regulator in differentiation of endothelial progenitor cells.* Stem Cells 2015;33:1512-1522. **PMID 25588582; DOI 10.1002/stem.1954.** [VERIFIED — HP1α can activate genes during differentiation]
4. Hosokawa H, et al. *Functionally distinct Gata3/Chd4 complexes coordinately establish Th2 cell identity.* PNAS 2013;110:4691-4696. **DOI 10.1073/pnas.1220865110.** [VERIFIED — GATA3/NuRD activates Th2, represses IFNG; context for §5 epistasis]
5. Noguerol J, et al. (Joffre OP, corresponding). *Heterochromatic gene silencing controls CD4⁺ T cell susceptibility to regulatory T cell-mediated suppression in a murine allograft model.* Nat Commun 2025;16:566. **DOI 10.1038/s41467-025-55848-4.** [VERIFIED — HP1α converts immunosuppressive signals into heterochromatin-dependent silencing in CD4 T cells]

No unverified citations retained.
