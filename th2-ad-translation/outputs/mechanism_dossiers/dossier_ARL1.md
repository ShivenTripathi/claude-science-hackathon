# Mechanistic Dossier — ARL1 as a candidate selective Th2 suppressor

**Screen summary.** ARL1 knockdown (CRISPRi) in primary human CD4⁺ T cells scores as a
candidate *selective* Th2 suppressor: composite 0.693; best th2_arm −0.519 with
th1_arm −0.122 at that point; selective in **Rest** and **Stim48hr**; curated-marker
means th2_marker_z −1.41 / th1_marker_z −0.80; cellcycle_z +0.29; global_mag 0.98;
on-target KD z −17.45; cross-donor r 0.806. The KD is real, on-target, and reproducible;
the open question is whether the Th2-leaning footprint is *selective* or a by-product of
disrupting a housekeeping trafficking gene.

> **Caveat (must be stated).** These are Rest/Stim CD4⁺ T cells, **not** polarized
> Th1/Th2 cells. "Selective Th2 suppression" here means the KD's *transcriptional
> footprint* resembles selective loss of the Th2 program — a phenotypic inference from a
> single-perturbation screen, **not** a demonstrated mechanism or a functional
> polarization assay.

## 1. Gene identity & molecular function
ARL1 (ADP-ribosylation factor-like 1) is a small GTPase of the ARF/ARL superfamily that
localizes to the *trans*-Golgi network (TGN). ARF/ARL GTPases are master regulators of
vesicular membrane trafficking [PMID 28468990]. In its GTP-bound state ARL1 recruits
GRIP-domain golgins (golgin-97, golgin-245/p230) to the TGN and drives endosome→TGN
retrograde transport, secretory trafficking, and Golgi organization [PMID 28468990;
PMID 15269279]. Critically, these ARL1-dependent golgins carry *secretory cargo*: golgin-245/p230
is required for regulated cell-surface delivery of TNFα in activated macrophages, and
golgin-97 carries E-cadherin [PMID 18308930]. ARL1 has no known transcriptional activity
and no reported direct role at GATA3, STAT6, or the IL4/IL5/IL13 locus.

## 2. Selectivity hypothesis (gene → intermediate → Th2, sparing Th1)
Proposed chain:
**ARL1 KD → impaired TGN secretory/retrograde trafficking → reduced secretion of IL-4
and/or reduced surface delivery of IL-4Rα → weakened autocrine IL-4→STAT6→GATA3 feedback →
collapse of the GATA3-driven Th2 transcriptional program.**

- ARL1-effector golgins govern regulated cytokine secretion — **ESTABLISHED** for TNFα via
  golgin-245/p230 [PMID 18308930]. That IL-4 specifically transits this ARL1 route is **INFERRED**.
- IL-4→IL-4Rα→STAT6→GATA3 is a self-amplifying positive-feedback loop that stabilizes the
  Th2 program, and GATA3 autoactivates — **ESTABLISHED** [PMC3557721; PMID 12947222;
  DOI 10.1016/S1074-7613(00)80156-9].
- **Why Th1 stays flatter (INFERRED):** the Th2 program is uniquely wired around an
  autocrine, secretion-dependent IL-4/STAT6/GATA3 amplifier; blunting secretion
  preferentially starves that loop, whereas Th1 (IFNγ→STAT1→T-bet) is less dependent on a
  secretion-driven self-amplifier in resting/short-stim CD4s. This is a plausibility
  argument, not a measured asymmetry.

## 3. Directness call — **INDIRECT**
ARL1 is a Golgi trafficking GTPase with no transcriptional or DNA-binding function. Any
effect on the Th2 program must run through intermediates (secreted cytokine / surface
receptor → signaling → transcription). A direct action on Th2 machinery is not supported
by known function.

## 4. Artifact scrutiny — **SOME CONCERN**
- **Covert Th1-skewer? Ruled out.** th1_marker_z is −0.80 (Th1 markers *down*, not up);
  the KD is not pushing cells toward Th1.
- **Proliferation collapse? Unlikely.** cellcycle_z +0.29 shows no cell-cycle-arrest
  signature.
- **General secretory dampening? Real concern.** global_mag 0.98 is high, exactly what a
  housekeeping trafficking gene should produce, and th1 markers are not truly flat
  (selectivity ratio ≈ 1.76, not clean). The magnitude-controlled residual score mitigates
  but does not eliminate this: ARL1 KD plausibly imposes a broad secretory-stress dampening
  on which a modest Th2-preferential effect is superimposed. DepMap essentiality of ARL1
  should be checked directly (not verified here) to exclude a fitness confound. Verdict:
  real, reproducible signal with a genuine general-dampening confound — treat as a lead, not
  a confirmed selective suppressor.

## 5. Confirming experiment (tests the SELECTIVITY claim)
In CD4⁺ T cells under Th2-polarizing conditions, knock down ARL1 and:
1. Measure **secreted IL-4/IL-5/IL-13 vs IFNγ** (ELISA/multiplex) plus intracellular
   cytokine staining — distinguishes a secretion block from a transcriptional loss and
   tests Th2-vs-Th1 selectivity.
2. Measure **surface IL-4Rα** (flow) — tests the receptor-trafficking arm.
3. **Epistasis/rescue:** add saturating exogenous IL-4 or enforce constitutively active
   GATA3. **Expected if hypothesis true:** ARL1 KD lowers secreted Th2 cytokines and surface
   IL-4Rα, spares IFNγ, and the Th2 transcriptional defect is *rescued* by bypassing the
   autocrine loop (exogenous IL-4 / enforced GATA3) — placing ARL1 upstream of GATA3 via
   secretion/feedback. Failure to rescue would falsify the proposed route.

## 6. Citations (each verified by web_search against source metadata)
1. Yu & Lee. Multiple activities of Arl1 GTPase in the TGN. *J Cell Sci* 2017;130:1691.
   **PMID 28468990; DOI 10.1242/jcs.201319**. [verified — ARL1 TGN/secretory trafficking]
2. Lu, Tai & Hong. Golgin-97, an effector of Arl1 GTPase, in endosome→TGN traffic.
   *Mol Biol Cell* 2004;15:4426. **PMID 15269279; PMC519138**. [verified — Arl1/golgin-97 transport]
3. Lieu et al. A TGN golgin required for regulated TNF secretion in macrophages. *PNAS*
   2008;105:3351. **PMID 18308930; PMC2265200**. [verified — Arl1-golgin cytokine secretion]
4. Maier, Duschl & Horejs-Hoeck. STAT6-dependent/-independent mechanisms in Th2 polarization.
   *Eur J Immunol* 2012. **PMC3557721; DOI 10.1002/eji.201242433**. [verified — IL-4→STAT6→GATA3 autocrine]
5. Zhou & Ouyang. Functional role of GATA-3 in Th1/Th2 differentiation. *Immunol Res* 2003;28:25.
   **PMID 12947222**. [verified — GATA-3 master Th2 regulator/autoregulation]
6. Ouyang et al. Stat6-independent GATA-3 autoactivation directs Th2 commitment. *Immunity*
   2000;12:27. **PMID 10661403; DOI 10.1016/S1074-7613(00)80156-9**. [verified — GATA-3 feedback]

**No published study directly links ARL1 to the Th2/GATA3 program.** The model is assembled
from ARL1's established trafficking/secretion role plus established Th2 autocrine biology; the
bridge (IL-4 specifically using the ARL1 route) is unverified inference. Confidence is low.
