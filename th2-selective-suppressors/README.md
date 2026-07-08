# Selective Th2 suppressor re-analysis

Re-analysis of the Zhu & Dann et al. 2025 genome-scale CRISPRi Perturb-seq screen (primary human
CD4+ T cells), hunting **selective Th2 suppressors** — knockdowns that lower the Th2 program while
leaving Th1 flat — and then stress-testing that claim to destruction.

> **Result: a calibrated negative.** The naive selective-suppressor signal is not enriched over
> random gene sets (FDR ≈ 1), the +0.54 "confound" was largely a scoring artifact (→ +0.18 under
> competitive scoring), and GATA3 reads as a Th1-skewer under proper scoring. See
> [`outputs/synthesis.md`](outputs/synthesis.md) and [`outputs/review_report.md`](outputs/review_report.md).

## Start here
- **`dashboard.html`** — self-contained interactive report (open in a browser, or view live at the
  artifact URL in the top-level README). Embeds every figure, the shortlist, all 10 mechanism
  dossiers, the full review report, and the hardened re-analysis as readable in-page documents.
- **`review_index.html`** — a local index that links every raw artifact with relative paths.
- **`outputs/synthesis.md`** — plain-language synthesis (with the hardened-result reversal up top).
- **`outputs/review_report.md`** — independent review: Part A (data/QC audit), Part B (6-agent
  literature + methods audit), Part C (hardened re-analysis).

## Pipeline (`notebooks/`, run in order)
| step | script | what it does |
|---|---|---|
| 01 | `01_arms.py` | stream the DE matrix (parallel HTTP range reads), reconstruct Th2/Th1 arm scores |
| 02 | `02_annotations.py` | per-gene annotations: donor/guide/KD/off-target flags, target class |
| 03 | `03_credibility.py` | cutoff tiering, donor stability, KD self-silencing, recall, per-condition split |
| 04 | `04_score.py` | magnitude-controlled real-vs-false-positive composite score |
| 05 | `05_dashboard.py` | generate the self-contained dashboard |
| 06 | `06_dossiers.py` | parse the agentic mechanism dossiers |
| 07 | `07_qc_audit.py` | pull richer h5ad QC columns; robustness checks |
| 08 | `08_local_index.py` | build the local `review_index.html` |
| 09 | `09_review_report.py` | assemble the review report from the literature-audit workflow |
| 10 | `10_hardened.py` | **competitive scoring + permutation FDR + multi-lineage controls + concordance** |

The agentic layers (mechanism dossiers; 6-agent literature/methods audit) were run as multi-agent
workflows; their structured outputs are in `outputs/`.

## Reproduce
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python notebooks/01_arms.py     # streams ~2.8 GB from public S3; no download needed
python notebooks/02_annotations.py && python notebooks/03_credibility.py && python notebooks/04_score.py
python notebooks/07_qc_audit.py && python notebooks/10_hardened.py
python notebooks/05_dashboard.py
```

## Key outputs
- `outputs/plane_plot.svg` — the 2D arm plane (headline figure)
- `outputs/real_vs_fp_shortlist.csv` — scored shortlist (superseded by the hardened analysis)
- `outputs/hardened_stats.json` / `hardened_shortlist.csv` — the rigorous re-analysis
- `outputs/mechanism_dossiers/*.md` — per-candidate agentic dossiers (investigate → adversarial verify)
- `outputs/review_report.md` — the full independent review

Data provenance and citations are in the top-level README.
