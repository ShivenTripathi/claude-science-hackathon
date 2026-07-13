# Submission — Selective Th2 suppressors, reconciled three ways

**Track:** Researcher · **Dataset:** Zhu & Dann et al. 2025 genome-scale CRISPRi Perturb-seq, primary
human CD4⁺ T cells (Marson lab)

---

## Written summary (168 words)

Can a genome-scale CRISPRi Perturb-seq screen in human CD4⁺ T cells nominate a **selective Th2
suppressor** — a knockdown that dials down the allergy-driving Th2 program without flipping cells
toward Th1? We attacked this question **three independent ways** and reconciled them. Two statistical
pipelines (built separately, one streaming the 16.8 GB matrix over HTTP byte-ranges) both reach a
**calibrated negative**: under competitive scoring, a permutation null, and a matched Th1-vs-Th0 arm,
the "selective" set is no more enriched than random, and the apparent top hit GATA3 is actually a
Th1-skewer. A third analysis added an **orthogonal drug-discovery layer** — atopic-dermatitis
patient single-cell validation plus Open Targets druggability — and honestly reports that it *cannot*
rescue a statistically-failed candidate. The capstone: three analyses produce **almost-disjoint
candidate lists**, and of 102 statistically-hardened survivors only one has AD genetic support — the
discredited GATA3. The deliverable is a rigorously-negative result, a reusable hardening + streaming
+ agentic-review + patient-validation methods stack, and an honest reconciliation.

---

## Why this scores on the rubric

**Impact (25%).** A *calibrated negative* on a high-profile screen is a finding others can build on:
it tells a drug-discovery team not to start a program off this screen alone, and names the one
experiment (functional IL-4/5/13 readout + control-guide FDR) that would settle it. It also
demonstrates a reusable honesty protocol for perturb-seq target nomination.

**Claude Use (25%).** Claude Science drove the whole arc end-to-end: MCP connectors (Open Targets
GraphQL for tractability/genetics, STRING for pathway classification), a 280k-cell patient scRNA-seq
analysis, an **agentic investigator→skeptic mechanism-review layer**, a **6-agent literature/methods
self-audit**, and a continuous adversarial-auditor loop that caught real bugs mid-flight (a colormap
inversion, a fabricated citation, a mislabeled axis) and forced fixes.

**Depth & Execution (20%).** The project *inverted its own optimistic first result* under
hardening — the opposite of a quick hack. Byte-range streaming of a 16.8 GB matrix, a GATA3
row-order guardrail, permutation FDR, and a cross-pipeline reconciliation are all real engineering.

**Demo (30%).** The story is genuinely compelling to watch: "we found a target… and then we proved
ourselves wrong, twice, independently, and that's the point."

---

## 3-minute demo script / outline

**[0:00–0:25] The hook — the trap.**
"Genome-scale Perturb-seq in human T cells. The question: is there a knockdown that selectively
shuts down the Th2 allergy program without flipping cells to Th1? Our first pass said yes — 127
hits, GATA3 on top. That's the trap. Here's how Claude helped us climb out of it."

**[0:25–1:05] Hardening inverts the result.** *(screen: synthesis.md diff + plane_plot)*
"Competitive scoring collapsed the confound correlation from +0.54 to +0.18. A permutation null: the
selective set is no better than random — FDR ≈ 1. And with a matched Th1-vs-Th0 arm, GATA3 flips to a
Th1-*skewer*, exactly as textbook biology predicts. The atlas doesn't survive statistics."

**[1:05–1:40] Independent replication — same answer.** *(screen: replication README + streaming code)*
"We rebuilt it from scratch, different tooling, streaming the 16.8 GB matrix over HTTP byte-ranges —
never downloading it. A GATA3 guardrail caught a silent row-order scramble. Same negative, GATA3
again a skewer. Two independent pipelines agreeing is the point."

**[1:40–2:20] The orthogonal layer — and honest limits.** *(screen: AD dotplot + druggability map)*
"Then a different question: atopic dermatitis, off the dupilumab axis, validated in a 280k-cell
patient skin atlas, with Open Targets druggability. It surfaces leads like NR4A3 — but we report
plainly that a patient-expression layer *cannot* rescue a statistically-failed candidate."

**[2:20–2:55] The reconciliation — the capstone.** *(screen: recon_overlap_matrix.png)*
"Three analyses, three almost-disjoint gene lists. Of 102 statistically-hardened survivors, exactly
one has atopic-dermatitis genetic support — GATA3, the hit we already disproved. Non-convergence
*is* the evidence. The deliverable isn't a target; it's a rigorously honest negative and a reusable
methods stack — hardening, streaming, agentic review, patient-validation."

**[2:55–3:00] Close.** "Claude Science didn't just run the analysis — it audited us into telling the
truth."

---

## Repository layout

```
claude-science-hackathon/
├── th2-selective-suppressors/     # Analysis 1 — atlas + hardening + agentic review
├── th2-independent-replication/   # Analysis 2 — independent streaming pipeline
└── ad-offaxis-druggability/       # Analysis 3 + reconciliation (this work)
    ├── reconciled_view.md
    ├── SUBMISSION.md
    ├── reconciliation_sets.csv / reconciliation_overlaps.csv / recon_overlap_matrix.png
    ├── their_survivors_common_footing.csv
    ├── ad_offaxis_target_atlas.csv / ad_offaxis_lead_shortlist.csv
    ├── ad_patient_validation.csv / ad_target_report.md
    └── figures/  (figA patient dotplot, figB druggability×patient, figC shortlist)
```
