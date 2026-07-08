# Plan: Selective Th2-Suppressor Atlas + Agentic Mechanism Layer

## Context

**The project.** Built-with-Claude Life Sciences hackathon (Researcher track), team = catchmeifyocan (us — AI/engineering) + Haltavey (Th2 immunologist, published an E3-ligase→Th2 Nat Comms paper). Dataset = the Zhu & Dann et al. 2025 Marson-lab **genome-scale CRISPRi Perturb-seq in primary human CD4+ T cells** (repo: `/Users/shiventripathi/dev/GWT_perturbseq_analysis_2025`; data on public S3 `s3://genome-scale-tcell-perturb-seq/marson2025_data/`).

**What we established scientifically (do not re-derive):**
- The original "genome-wide Th2 regulator atlas" idea is a re-run of the paper's own Fig 4 — not novel.
- The novel, defensible question: **which knockdowns selectively suppress the Th2 program without merely flipping the cell toward Th1** (the allergy-relevant target). The paper only has a single bidirectional Th2−Th1 axis, which structurally cannot separate these.
- Empirical test (teammate, on the Ota-2021 Th2-vs-Th1 signature split into a Th2-up arm and a Th1-up arm): the **selective quadrant is real (~172 hits)**, true **Th1-skewers are rare (~4)**, and the two arms are **positively correlated (~+0.49)** — meaning the dominant confound is **global magnitude** (sick-cell / low-proliferation dampening pulling both arms down together), *not* skewing.
- Payoff: the Th1 arm doubles as a **built-in control** — "Th1 not down" kills global-dampening artifacts, "Th1 not up" kills skewers. One 2D decomposition → clean Th2-specific suppression.
- **GATA3 is the #1 hit** → sign convention correct and known-biology recall works.

**What we're building this session (full scope, per user):** (1) a rigor/credibility pack the team can post now, (2) a real-vs-false-positive composite score (Haltavey's ask), and (3) the **agentic mechanism layer** — a Claude agent that, per top novel hit, produces a mechanistic hypothesis + proposed confirming experiment. The agent layer is our differentiator (the prebrief thesis: graph → interesting signal → Claude investigates → mechanism → experiment).

**Ground rules:** The GWT repo is the upstream authors' git repo — **read-only reference, never modify**. All new code/outputs go under a fresh working dir `/Users/shiventripathi/dev/science/th2_selective/`.

---

## Data sources (all confirmed present unless noted)

**Pull from S3 (authoritative, user's choice):**
- `GWCD4i.DE_stats.h5ad` — per-perturbation×condition DE, `n_obs=33,983`, `n_vars=10,282`. Layers: `log_fc, zscore, p_value, adj_p_value, baseMean, lfcSE`; `.varm.measured_genes_stats_{Rest,Stim8hr,Stim48hr}`; `.obs.culture_condition`. **The arm-reconstruction + target-self-silencing source.**
- (If needed) `GWCD4i.pseudobulk_merged.h5ad` for any cell-count/QC follow-up.

**Local precomputed (reuse directly — most checks are joins, not recomputes):**
- `metadata/suppl_tables/DE_stats.suppl_table.csv` (33,983 rows): `ontarget_effect_size, ontarget_significant, offtarget_flag, crossdonor_correlation_mean/min, crossguide_correlation, n_cells_target, n_total_de_genes, culture_condition`.
- `metadata/suppl_tables/guide_kd_efficiency.suppl_table.csv` (73,765 rows): per-guide `signif_knockdown, high_confidence_no_effect_guides, culture_condition`.
- `metadata/suppl_tables/Th2_Th1_polarization_signature_DE_results_full.suppl_table.csv` + `src/4_polarization_signatures/results/Ota_Th2vsTh1_DE_results.csv` — the **Ota 2021 signature** to split into the two arms.
- `metadata/th1_th2_known_regulators.yaml` — **calibration set** (th2: GATA3, IL4R, STAT6, SETDB1, MTA2, CHD4, MBD2, TRAF3, RARA, PTPN2, IL4, ICOS; th1: STAT1, IFNGR1/2, TBX21, STAT4, RASGRP1, IRF1, IRF9, STAT2, JAK2).
- `metadata/Lambert_2018_HumanTF.csv` (TF annotation for target-class tagging), `metadata/donor_info.csv` (D1–D4), `metadata/enrichment_database/` (pathway sets for the agent layer).
- Precomputed robustness tables: `src/3_DE_analysis/results/DE_donor_robustness_correlation.csv`, `DE_by_guide.correlation_results.csv`.

**Reference-only code (mirror the method, don't import blindly):**
- `src/4_polarization_signatures/polarization_signature.ipynb` — how arms/signature are built.
- `src/1_preprocess/estimate_guide_effect.ipynb` — KD-efficiency method.
- `src/3_DE_analysis/donor_robustness/get_donor_robustness.py` — donor robustness.
- `src/utils.py`, `src/3_DE_analysis/DE_analysis_utils.py`, `MultiStatePerturbSeqDataset.py` — loaders/plot helpers.

---

## Phase 0 — Setup & data acquisition
- Create `/Users/shiventripathi/dev/science/th2_selective/` (`data/`, `outputs/`, `notebooks/`).
- Slim env (don't need full `gwt-env`/rapids/scvi): `anndata, scanpy, pandas, numpy, scipy, statsmodels, matplotlib, seaborn, pyyaml, pyarrow, requests`.
- `aws s3 ls --no-sign-request s3://genome-scale-tcell-perturb-seq/marson2025_data/` → download `GWCD4i.DE_stats.h5ad` to `data/`.
- Copy (not move) the local CSVs/yaml we need into `data/` for a self-contained working set.

## Phase 1 — Reconstruct the two arms with a full index (validation checkpoint)
- Split the **Ota 2021 Th2-vs-Th1 signature** into a **Th2-arm** gene set (sig. up in Th2, padj<thr, positive z) and a **Th1-arm** gene set (sig. up in Th1). Record thresholds.
- For each perturbation × condition in `DE_stats.h5ad`, compute `th2_arm_z` and `th1_arm_z` (signature-score projection of the perturbation's DE profile onto each arm — matching the teammate's construction).
- **Checkpoint:** reproduce ~172 selective / ~4 skewer / +0.49 arm-correlation; confirm GATA3 is the top selective hit. If the teammate shares `th2_arm.npy/th1_arm.npy`, cross-correlate (expect ≈1).
- Output: `outputs/arms.parquet` (perturbation × condition × {th2_arm_z, th1_arm_z, n_cells}, joined to DE_stats.suppl columns).

## Phase 2 — Credibility pack (5 artifacts to post to the team)
1. **Cutoff tiering.** Gate = `th2_arm_z < t_x` AND `|th1_arm_z| < t_y`. Sweep `t_x∈{−1.5,−2,−2.5}`, `t_y∈{0.5,1,1.5}`. Label each candidate **confident core** (selected under strictest gate / all settings) vs **borderline**. → `outputs/selective_tiered.csv`.
2. **Donor stability.** Join `crossdonor_correlation_mean/min`; flag/drop hits carried by 1–2 donors (threshold vs NTC null). Cross-check `DE_donor_robustness_correlation.csv`.
3. **KD / target self-silencing.** This resolves Haltavey's hand-wavy "statistically they are": require **`ontarget_significant` + meaningful `ontarget_effect_size`** (the target's *own* transcript is down), plus per-guide `signif_knockdown` fraction from `guide_kd_efficiency`. Flag `offtarget_flag`. Drop hits that never silenced their target.
4. **Known-regulator recall overlay.** Overlay `th1_th2_known_regulators.yaml` on the (th2_arm, th1_arm) plane; show Th2 regulators land in the selective box (recall metric = fraction in box), Th1 regulators elsewhere. GATA3 = anchor. → `outputs/recall_overlay.svg`.
5. **Per-condition (Rest/Stim8hr/Stim48hr) selectivity split** *(the novel cut)*. Because arms are per condition, classify selectivity within each condition → categories: constitutive vs stim-induced vs rest-only selective suppressor. Note design imbalance (Stim48hr from run R2). This is exactly the original "does it depend on stimulation context?" question, answered in 2D where the paper's 1D axis can't. → `outputs/condition_selectivity_matrix.csv` + figure.

## Phase 3 — Real-vs-false-positive composite score
Per candidate, combine (each a documented subscore):
- **guide concordance** (`crossguide_correlation` / fraction signif guides),
- **cross-condition consistency** (sign/magnitude agreement across conditions present),
- **selectivity depth, magnitude-controlled** — regress out the global-magnitude axis (use th1_arm / overall DE magnitude as covariate) and rank on residual Th2 suppression, so ranking isn't secretly re-sorting on the +0.49 confound,
- **artifact flags** — demote ribosomal / mito / cell-cycle / essential / broad-effect (`n_total_de_genes` high, both arms down) genes,
- **druggability / target class** — tag TF (Lambert list), kinase, **E3 ligase** (Haltavey's interest), surface receptor.
Output `outputs/real_vs_fp_shortlist.csv`, split into **known (calibration)** vs **novel-but-plausible (finding)** buckets, ranked.

## Phase 4 — Agentic mechanism layer (differentiator)
For the top N novel selective suppressors, run a Claude agent per candidate (Workflow pipeline: investigate → adversarially verify):
- Pull literature (WebSearch/WebFetch) + pathway/PPI context (`metadata/enrichment_database/`, STRING/Reactome).
- Answer the selectivity question: **is there a plausible route gene → GATA3/IL4/Th2 program that does NOT run through T-bet/Th1?** (explains why Th2 falls but Th1 doesn't).
- Emit a structured dossier: mechanistic hypothesis, confidence, **verifiable citations**, and a **proposed confirming experiment** (e.g., "KD + measure IL4 vs IFNG under Th2-polarizing conditions"). A verify pass checks citations are real.
- Output `outputs/mechanism_dossiers/*.md` + a synthesis. This is the demo.

---

## Live tracking artifact (NEW)
Maintain an HTML **dashboard artifact** the user reviews and tracks alongside execution: the scientific thread, phase status, checkpoint numbers (172/4/+0.49, GATA3), the tiered list, recall metric + plane plot, per-condition split, real-vs-FP shortlist, and mechanism dossiers. **Redeploy/update it after each phase completes** (same file path → same URL). Embed figures as inline SVG / base64 PNG (artifacts are self-contained; no external hosts).

## Deliverables (artifact checklist)
- Live HTML dashboard artifact (updated per phase).
- Reproduced plane plot + 172/4/+0.49 validation.
- `outputs/arms.parquet`.
- `outputs/selective_tiered.csv` (core vs borderline + donor/KD/off-target/artifact flags).
- `outputs/recall_overlay.svg` + recall metric.
- `outputs/condition_selectivity_matrix.csv` + figure.
- `outputs/real_vs_fp_shortlist.csv` (known vs novel, druggability tags).
- `outputs/mechanism_dossiers/` + synthesis.
- Short methods note (notebook/markdown) to paste in Discord.

## Verification
- **Reproduction:** our reconstructed arms reproduce ~172/~4/+0.49 and GATA3 as top selective hit; if teammate's `.npy` provided, arm correlation ≈1.
- **Calibration:** known Th2 regulators recall into the selective box; Th1 regulators do not.
- **Spot-checks:** for 3–5 top hits, confirm `ontarget_significant`, cross-donor correlation, and guide KD fraction against the suppl tables independently.
- **Magnitude control sanity:** after regressing out global magnitude, ribosomal/cell-cycle genes drop in rank; genuine selective hits persist.
- **Agent layer:** each dossier's citations resolve to real papers (adversarial verify); proposed experiments are concrete and specific to the selectivity claim.
