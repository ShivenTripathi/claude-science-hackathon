# Mechanistic dossier — TFAP4 (AP-4 / bHLHc41)

**Screen call:** composite 0.406 · selective only in Stim48hr · best th2_arm −0.468, th1_arm 0.038 · th2_marker_z −1.42, th1_marker_z **+1.11** · cellcycle_z −1.40 · global_mag 1.06 · on-target KD z −4.02 · cross-donor r 0.812.

> **Framing caveat (must be stated):** these are Rest/Stim CD4+ T cells, **not** polarized Th1/Th2. "Selective Th2 suppression" here means the KD's *transcriptional footprint* resembles selective loss of the Th2 program. It is a phenotypic inference from a single-perturbation screen — not a demonstrated mechanism and not a functional polarization assay. Perturb-seq measures consequences, not wiring.

## 1. Gene identity & molecular function
TFAP4 (AP-4) is a basic-helix-loop-helix-leucine-zipper transcription factor that binds the E-box CAGCTG and acts as both repressor and activator of target genes [C1]. It is a **direct c-MYC target**: MYC induces AP4, which then represses the CDK inhibitor p21, sustaining a proliferative, progenitor-like state [C2]. More broadly it is a MYC-network hub coupling proliferation, metabolism, stemness, EMT and senescence-suppression [C4]. In T cells its one well-characterized role is in **CD8+** cells: c-Myc induces AP4, and AP4 then *maintains* the c-Myc-initiated metabolic/activation program after Myc protein decays, sustaining clonal expansion; AP4 protein accumulates specifically in CD25-high (IL-2Rα-high) cells and IL-2R signaling sustains it [C3]. There is **no established link** between TFAP4 and GATA3, STAT6, the IL4/IL5/IL13 locus, chromatin regulators of Th2, or allergy.

## 2. Selectivity hypothesis (Th2 down, Th1 flat)
Because no direct TFAP4→Th2 wiring exists, the only plausible route is indirect, through the proliferation/IL-2R axis:

**TFAP4 → (sustained c-Myc-driven proliferative + IL-2Rα/CD25 metabolic program) → (IL-2/STAT5 tone) → GATA3 / IL4-IL5-IL13 output.**

- Link A — TFAP4 sustains the Myc-initiated proliferative/metabolic program and associates with CD25-high state: **ESTABLISHED** in CD8 T cells [C3]; **INFERRED** for CD4.
- Link B — IL-2/STAT5 signaling is required for the Th2/IL-4 program (STAT5 acts directly at Il4; GATA3 is the master regulator): **ESTABLISHED** [C5].
- Link C — reduced Myc/IL-2R tone therefore lowers Th2 effector output while sparing Th1 (Th1/Th17 lean on mTORC1 rather than STAT5), which could even let Th1 markers drift up: **INFERRED** (this is exactly the direction of the observed th1_marker_z +1.11).

## 3. Directness call — **INDIRECT**
TFAP4's documented targets are cell-cycle (p21/p16), metabolic and IL-2Rα genes [C2][C3][C4], not Th2 lineage genes. Any effect on GATA3/IL-4 is most parsimoniously routed through the proliferation/IL-2R intermediate. A direct action on Th2 machinery is unsupported by current literature.

## 4. Artifact scrutiny — honest verdict: **SOME CONCERN**
This candidate sits squarely on the dominant confound. TFAP4's *canonical* function is proliferation/effector-amplitude amplification [C2][C3][C4] — precisely the "sick-cell / low-proliferation dampening" the score is meant to control for. Supporting worry: cellcycle_z −1.40 (measurable proliferation reduction), global_mag 1.06 (broad transcriptome shift), selectivity in only one condition (Stim48hr, where proliferation differences are largest), modest composite 0.406. Most important, **th1_marker_z = +1.11**: the curated Th1 marker set goes *up*, contradicting the near-zero projected th1_arm (0.038) — a discrepancy that could indicate a covert relative Th1 skew rather than clean selectivity. Counterweights: the effect is reproducible (cross-donor r 0.812), the KD is real (on-target z −4.02), and the score is magnitude-decorrelated, so the th2_arm signal is not purely global. Not dismissible as a pure artifact, but the proliferation/activation-amplitude explanation is at least as likely as genuine Th2 selectivity. **Confidence: low.**

## 5. Confirming experiment (tests the SELECTIVITY claim)
KD TFAP4 (vs non-targeting guide) in naive human CD4+ T cells under **Th2-polarizing** conditions (anti-CD3/CD28 + IL-4 + anti-IFNγ), with a **proliferation-matched** readout: measure GATA3, IL-4, IL-5, IL-13 vs T-bet/IFNγ (intracellular flow + qPCR) alongside CellTrace dilution / Ki67 and a viability stain.
- **Hypothesis true (selective):** Th2 output (GATA3/IL-4/IL-5/IL-13) drops while T-bet/IFNγ do **not** rise, *and* the Th2 loss exceeds what the proliferation deficit alone predicts.
- **Artifact:** Th2 fall tracks proportionally with reduced proliferation/viability and/or IFNγ rises (Th1 skew).

Decisive add-on — **epistasis**: co-KD TFAP4 + GATA3 vs GATA3 alone. No further Th2 loss ⇒ TFAP4 acts through GATA3 (indirect, upstream). This screen is single-perturbation, so ordering is inferred, not measured.

## 6. Citations (all verified this session)
- **[C1]** UniProt Q01664 (TFAP4, human) + OMIM **600743** (gene identity, bHLH-ZIP; both records directly retrieved). Primary source for E-box CAGCTG binding: Mermod N, Williams TJ, Tjian R. "Enhancer binding factors AP-4 and AP-1 act in concert to activate SV40 late transcription in vitro." *Nature* 1988;332:557–561. DOI **10.1038/332557a0** — the Nature record (title, journal, volume/pages, DOI) was directly retrieved. PMID **2833704** is the PubMed identifier commonly attached to this paper but was NOT independently confirmed against a retrieved PubMed record in this session; treat the DOI as the authoritative identifier.
- **[C2]** Jung P, Menssen A, Mayr D, Hermeking H. "AP4 encodes a c-MYC-inducible repressor of p21." *PNAS* 2008;105:15046–15051. DOI **10.1073/pnas.0801773105**; PMCID **PMC2553359**.
- **[C3]** Chou C, et al. (Egawa T). "c-Myc-induced transcription factor AP4 is required for host protection mediated by CD8+ T cells." *Nat Immunol* 2014;15:884–893. PMID **25029552**; DOI **10.1038/ni.2943**; PMCID **PMC4139462**.
- **[C4]** Review: "Transcription Factor AP4 Mediates Cell Fate Decisions: To Divide, Age, or Die." *Cells* 2021. PMCID **PMC7914591**. — AP4 as MYC-network hub (proliferation, EMT, stemness, senescence, adaptive immunity).
- **[C5]** Review: "Transcriptional regulation of Th2 cell differentiation." PMCID **PMC3477614**. — STAT6→GATA3 master regulator; IL-2/STAT5 required for Th2/IL-4.

**Verification pass:** C2–C5 identifiers were each matched to a directly retrieved result URL/record supporting the attached claim (C2 PMC2553359 + PNAS DOI, MYC→AP4→p21; C3 PMID 25029552 + ni.2943 + PMC4139462, c-Myc-induced AP4 in CD8 T cells; C4 PMC7914591, AP4 cell-fate/MYC-hub review; C5 PMC3477614, STAT6/GATA3 + IL-2/STAT5 Th2 requirement) — **4 fully verified**. For C1, the *Nature* 1988 record (title/journal/volume/DOI 10.1038/332557a0) was retrieved and UniProt Q01664/OMIM 600743 confirm gene identity, but its PubMed identifier (PMID 2833704) was not independently re-retrieved this session — flagged **[PMID UNVERIFIED]** in the entry; the DOI is authoritative. No TFAP4→GATA3/Th2 primary source exists; that link is explicitly labeled INFERRED, not cited. **Net: 4 fully verified, 1 (C1) verified by DOI with an unverified PMID; 0 fabricated identifiers retained.**
