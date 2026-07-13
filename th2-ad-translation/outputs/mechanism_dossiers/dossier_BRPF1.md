# Mechanistic Dossier: BRPF1

**Candidate class:** chromatin scaffold (HAT-complex subunit) · **Composite confidence:** 0.535 · **Selective condition:** Rest only

> **Screen-context caveat (read first).** These are Rest/Stim CD4+ T cells, *not* polarized Th1/Th2 cells. "Selective Th2 suppression" here means the BRPF1-knockdown transcriptional footprint *resembles* selective loss of the Th2 program on a signature-projection axis. It is a phenotypic inference from a single-perturbation CRISPRi screen — not a demonstrated mechanism and not a functional polarization assay. Every mechanistic link below is a hypothesis to be tested.

## 1. Gene identity & molecular function

BRPF1 (bromodomain and PHD finger–containing protein 1) is a chromatin-associated **scaffolding subunit** of the MOZ/MORF (KAT6A/KAT6B) and HBO1 (KAT7) MYST-family histone acetyltransferase (HAT) complexes. It has no catalytic activity of its own; instead its N-terminal region binds the MYST catalytic domain while a central Epc-homology region bridges ING4/5 and MEAF6 into a tetrameric complex — subunits that do not assemble without BRPF1 [Ullah 2008; Cheng 2023]. Functionally, complex formation with BRPF1 (plus ING5) **drastically stimulates** acetylation of nucleosomal histone H3 [Ullah 2008]. Its reader modules (PZP, bromodomain, PWWP) localize the complex to active transcription start sites, and BRPF1 directs HBO1 toward **H3K14ac/H3K23ac** [Lalonde 2013]. BRPF1 is thus a genome-wide chromatin activator, not a sequence-specific transcription factor.

## 2. Selectivity hypothesis (a route that avoids the T-bet/Th1 axis)

**BRPF1 → MOZ(KAT6A)/HBO1 HAT activity → H3K14ac at active promoters → maintenance of the GATA3/Th2 program → (KD) loss of Th2 output.**

- **L1 — BRPF1 assembles/activates MOZ & HBO1 HAT complexes:** ESTABLISHED [Ullah 2008; Lalonde 2013].
- **L2 — this complex deposits H3K14ac/H3K23ac at active loci:** ESTABLISHED [Lalonde 2013].
- **L3 — KAT6A(MOZ) is required for proliferation/differentiation of effector CD4+ T cells:** ESTABLISHED in mouse [Fu 2024].
- **L4 — that acetylation specifically maintains the GATA3/Th2 program:** INFERRED (no BRPF1- or MOZ-specific occupancy at *GATA3/IL4/IL5/IL13* has been shown).
- **L5 — why Th1 stays flat:** INFERRED. GATA3 is necessary and sufficient for Th2 cytokines and mutually antagonizes the Th1 program [Zheng 1997], so removing a GATA3-supporting coactivator lowers Th2 without needing to raise T-bet/IFNγ (STAT1/STAT4-driven). This is the mechanistic reason Th1 *could* remain flat — but see §4.

## 3. Directness call — **INDIRECT**

BRPF1 is a broad chromatin reader/scaffold with no documented sequence-specific binding to *GATA3* or Th2 cytokine loci. Any effect on the Th2 program is routed through the catalytic HAT it activates (KAT6A/KAT7) and the downstream GATA3 node — an indirect, chromatin-level mechanism. The same broad H3K14ac activity that makes the route plausible also makes true *selectivity* mechanistically unlikely at the enzyme level.

## 4. Artifact scrutiny — **SOME CONCERN**

- **Not a covert Th1-skewer.** th1_marker_z = −0.45 is *negative*, and th1_arm_at_best = +0.076 is near zero. Th1 is not being pushed up. Good.
- **But the marker readout is not selective.** The curated sets fall together — Th2 −0.46, Th1 −0.45 — i.e. both lineages dampen roughly equally. Selectivity survives only on the magnitude-controlled projection arm (th2_arm −0.403, th1_arm ~0).
- **Proliferation/global-shift confound is live.** cellcycle_z = −0.89 and global_mag = 1.22 (elevated) fit a broad-dampening signature. Critically, this is *mechanistically expected*: BRPF1's partner KAT6A is required for CD4+ T-cell proliferation [Fu 2024], so BRPF1 loss plausibly produces general effector/proliferation slowdown rather than selective Th2 loss.
- **Reassurance:** KD is real and strong (on-target z = −14.69), donor reproducibility is good (0.80), and the score is decorrelated from the global-magnitude axis.

**Verdict:** genuine, reproducible knockdown effect, but selective-Th2 attribution is not clean — the equal Th1/Th2 marker drop, negative cell-cycle z, elevated global magnitude, and BRPF1's known proliferation-supporting role all keep a general-dampening explanation on the table. Single-condition (Rest-only) support further caps confidence.

## 5. Confirming experiment (tests the *selectivity* claim)

CRISPRi-knock down BRPF1 in naive human CD4+ T cells under **Th2-polarizing conditions** (IL-4 + anti–IL-12). Readouts by flow: intracellular **IL-4/IL-5/IL-13 vs IFNγ**, **GATA3 vs T-bet** protein, plus **CellTrace proliferation + viability**.
- *If the hypothesis is true:* IL-4/IL-5/IL-13 and GATA3 fall, IFNγ/T-bet stay flat, **and** proliferation/viability match control (rules out the dampening confound).
- **Epistasis arm:** co-knock down BRPF1 + GATA3. If BRPF1 acts through GATA3, the double KD is no worse than GATA3 KD alone on Th2 output.

## 6. Citations (all verified)

1. Ullah M, et al. Molecular architecture of quartet MOZ/MORF histone acetyltransferase complexes. *Mol Cell Biol.* 2008;28(22):6828–43. PMID: 18794358. DOI: 10.1128/MCB.01297-08.
2. Lalonde ME, et al. Exchange of associated factors directs a switch in HBO1 acetyltransferase histone tail specificity. *Genes Dev.* 2013;27(18):2009–24. PMID: 24065767. DOI: 10.1101/gad.223396.113.
3. Fu JY, et al. Lysine acetyltransferase 6A maintains CD4+ T cell response via epigenetic reprogramming of glucose metabolism in autoimmunity. *Cell Metab.* 2024;36(3):557–574.e10. DOI: 10.1016/j.cmet.2023.12.016.
4. Zheng W, Flavell RA. The transcription factor GATA-3 is necessary and sufficient for Th2 cytokine gene expression in CD4 T cells. *Cell.* 1997;89(4):587–96. PMID: 9160750. DOI: 10.1016/S0092-8674(00)80240-8.
5. Cheng X, et al. The MOZ-BRPF1 acetyltransferase complex in epigenetic crosstalk linked to gene regulation, development, and human diseases. *Front Cell Dev Biol.* 2023;10:1115903. PMCID: PMC9873972. DOI: 10.3389/fcell.2022.1115903.
6. BRPF1 in cancer epigenetics: a key regulator of histone acetylation and a promising therapeutic target. *Cell Death Discov.* 2025. DOI: 10.1038/s41420-025-02730-3.

**Verification pass:** All six references were confirmed to exist with matching title/journal/identifier, and each is attached only to the claim it supports (§1–§5 links tagged ESTABLISHED cite 1–4; INFERRED links carry no citation by design). No unverified sources; no claims removed. Note L3/[Fu 2024] concerns KAT6A, not BRPF1 directly — used only to argue the *proliferation confound*, not to assert a BRPF1 T-cell function.
