# Submission — Built with Claude: Life Sciences (Researcher track)

**Project:** Selective Th2 suppressors, and a druggable type-2 network beyond STAT6
**Repo:** https://github.com/ShivenTripathi/claude-science-hackathon
**Start here:** [`RECONCILIATION.md`](./RECONCILIATION.md) · live landing page via GitHub Pages

---

## Written summary (177 words)

Selective Th2 suppressors, and a druggable type-2 network beyond STAT6 — Researcher track.

We re-analyzed the Marson lab's genome-scale CRISPRi Perturb-seq screen in primary human CD4+ T
cells, asking whether single-gene knockdowns can selectively suppress the Th2
(allergy/atopic-dermatitis) program without flipping cells toward Th1 — the distinction the paper's
single bidirectional axis cannot make.

Across four independent Claude Science pipelines, the selective claim is an honest, calibrated
negative: a permutation null shows no enrichment over random gene sets (FDR ≈ 1), and GATA3 — the
apparent top hit — is actually a Th1-skewer under a matched control. Two from-scratch pipelines
agree; a third adds AD-patient-expression and druggability filters.

The fourth track reframes the question to the bar an oral STAT6 degrader actually clears — collapse
phenocopy, not selectivity — which calibrates as a classifier (permutation p < 0.001) and nominates
druggable off-axis targets (ITK, INPP5D/SHIP1) by fusing Open Targets tractability, AD GWAS, and AD
patient skin.

Everything reproduces: we stream a 16.8 GB remote matrix by byte-range without downloading it, and
every claim carries an adversarial self-audit.

---

## 3-minute demo video script

*Target ~450 spoken words. Screen cues in brackets. Record with Loom/QuickTime; the landing page +
deck + a terminal are the only things you need on screen.*

### 0:00–0:25 · The hook (why this matters)
> "Atopic dermatitis is a Th2-driven disease. Dupixent — anti-IL-4-receptor — proved you can treat
> it by hitting that axis, and STAT6 was just *orally degraded* with biologic-like efficacy. So the
> question isn't only 'what's a Th2 target' — it's 'what *druggable* intracellular target sits off
> the crowded IL-4R/STAT6 axis?' We went looking in the Marson lab's genome-scale CRISPRi
> Perturb-seq screen — every gene knocked down in primary human CD4 T cells."

[On screen: GitHub Pages landing page, the two-act "Honest bottom line" note.]

### 0:25–1:10 · The honest negative (Impact + Depth: we tried to kill our own result)
> "First, the honest part. We asked the sharp version — can a knockdown drop Th2 *while leaving Th1
> flat*? We built it, and then we tried to break it. Under a permutation null the 'selective' set is
> no better than random gene sets — FDR about one. And GATA3, the apparent top hit, flips to a
> Th1-skewer under the correct matched control. Two independently-built pipelines reach that same
> negative. That agreement is the result — Th1 and Th2 are genuinely reciprocal."

[On screen: scroll RECONCILIATION.md — the tracks table, the GATA3 correction.]

### 1:10–2:10 · The reframe (Claude Use + the finding)
> "But 'selective' may be the wrong bar. An oral STAT6 degrader doesn't act selectively — it
> collapses the whole type-2 axis, and it works. So we reframed: score every perturbation for how
> well it *phenocopies the STAT6/GATA3 collapse*. That's a positive anchor, and it calibrates where
> the residual failed — GATA3 and STAT6 come back as the top two, held-out IL4R recovers,
> permutation p < 0.001. Then we fused three layers Claude pulled live: Open Targets tractability,
> AD GWAS, and expression in real atopic-dermatitis patient skin. Out comes a ranked druggable map —
> ITK and INPP5D/SHIP1, both off the Dupixent axis, both with existing chemical matter and allergy
> genetics."

[On screen: the deck — network scatter (panel a) + patient lollipop (panel b).]

### 2:10–2:45 · How Claude Science did it (Claude Use)
> "Every layer was Claude Science. It streamed a 16.8-gigabyte remote matrix by byte-range —
> we never downloaded it. It ran the Open Targets and GWAS connectors, delegated the druggability
> and patient tracks to parallel sub-agents, and — the part I trust most — an adversarial reviewer
> audited each claim, and caught us overclaiming more than once. Four tracks, one reconciled view,
> fully reproducible notebooks."

[On screen: terminal — `python 02_score_collapse.py` printing GATA3 #1 (0.948); then the repo tree.]

### 2:45–3:00 · Close
> "The scientific answer is a calibrated negative on selectivity — stated honestly — plus a
> reusable collapse-scorer and a degrader-oriented target map for what to test next. It's all open,
> it all reproduces, and it all reconciles in one document."

[On screen: the landing page, four cards.]

---

## Submission checklist
- [x] Open-source license (MIT) at repo root
- [x] Public GitHub repository, pushed and live
- [x] Reproducible pipeline (notebooks verified end-to-end against committed data)
- [x] Written summary (177 words, above)
- [ ] 3-minute demo video — record from the script above, upload to Loom/YouTube, paste link on the CV platform
- [ ] Paste summary + repo URL + video link at https://cerebralvalley.ai/e/built-with-claude-life-sciences/hackathon/submit (deadline July 13, 9:00 PM ET)
