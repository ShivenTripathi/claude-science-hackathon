"""Build review_index.html at the project root: a locally-navigable index with RELATIVE
links to every artifact (figures, tables, dossiers, notebooks, inputs) so the work can be
reviewed independently by opening it in a browser."""
import html
from pathlib import Path
ROOT = Path("/Users/shiventripathi/dev/science/th2_selective")
def sz(p):
    b=p.stat().st_size
    return f"{b/1e6:.1f} MB" if b>1e6 else f"{b/1e3:.0f} KB"
def links(paths, base):
    out=""
    for p in paths:
        if not p.exists(): continue
        rel=p.relative_to(ROOT)
        out+=f'<li><a href="{rel}">{html.escape(p.name)}</a> <span class="s">{sz(p)}</span></li>'
    return out

O=ROOT/"outputs"; N=ROOT/"notebooks"; D=ROOT/"data"
sections=[
 ("Start here", [ROOT/"dashboard.html", O/"synthesis.md", O/"review_report.md"],
   "The dashboard (self-contained), the plain-language synthesis, and the independent-review report."),
 ("Figures", [O/"plane_plot.svg", O/"plane_plot.png", O/"recall_overlay.svg", O/"recall_overlay.png"],
   "The 2D arm plane (headline) and the known-regulator recall overlay."),
 ("Result tables", [O/"real_vs_fp_shortlist.csv", O/"selective_tiered.csv",
   O/"condition_selectivity_matrix.csv", O/"qc_audit_highconf.csv"],
   "Ranked shortlist (known vs novel), tiered selective list, per-condition selectivity, and the QC audit of the high-confidence set."),
 ("Intermediate data", [O/"arms.parquet", O/"annotations.parquet", O/"candidates_full.parquet", O/"obs_qc.parquet"],
   "Reconstructed arm scores, per-gene annotations, merged candidates, and the pulled h5ad QC columns."),
 ("Mechanism dossiers", sorted((O/"mechanism_dossiers").glob("*.md")),
   "Per-candidate agentic dossier: hypothesis, mechanism, evidence, proposed experiment, and the adversarial review."),
 ("Analysis code (reproducible)", sorted(N.glob("*.py")),
   "01 arms -> 02 annotations -> 03 credibility -> 04 score -> 05 dashboard -> 06 dossiers -> 07 QC audit -> 08 this index."),
 ("Inputs (from the Marson-lab repo)", [D/"Ota_Th2vsTh1_DE_results.csv", D/"th1_th2_known_regulators.yaml",
   D/"DE_stats.suppl_table.csv", D/"guide_kd_efficiency.suppl_table.csv", D/"Lambert_2018_HumanTF.csv", D/"donor_info.csv"],
   "The external Th2/Th1 signature, known-regulator calibration set, and the supplementary QC tables."),
]
cards=""
for title,paths,desc in sections:
    li=links(paths, ROOT)
    if not li: continue
    cards+=f'<section><h2>{title}</h2><p>{desc}</p><ul>{li}</ul></section>'

HTML=f"""<!doctype html><html><head><meta charset="utf-8"><title>Selective Th2 Suppressor Atlas — local review index</title>
<style>
body{{font-family:system-ui,sans-serif;max-width:860px;margin:0 auto;padding:32px 22px 70px;background:#f6f8f8;color:#141a1d;line-height:1.5}}
@media(prefers-color-scheme:dark){{body{{background:#0d1315;color:#e7eded}}a{{color:#2ec9a6}}section{{background:#141c1f;border-color:#233033}}.s{{color:#6b777d}}}}
h1{{font-size:26px;margin:0 0 4px}} .lede{{color:#5c676e;margin:0 0 22px}}
section{{background:#fff;border:1px solid #e4e9ea;border-radius:10px;padding:16px 20px;margin:14px 0}}
h2{{font-size:16px;margin:0 0 4px}} section p{{color:#5c676e;font-size:14px;margin:0 0 10px}}
ul{{margin:0;padding-left:18px}} li{{margin:3px 0}} a{{color:#0f9c82;text-decoration:none}} a:hover{{text-decoration:underline}}
.s{{color:#8a959b;font-size:12px;font-variant-numeric:tabular-nums}}
.note{{font-size:13px;color:#8a959b;margin-top:24px}}
</style></head><body>
<h1>Selective Th2 Suppressor Atlas</h1>
<p class="lede">Local review index — every artifact, linked with relative paths. Open this file in a browser to click through the analysis independently.</p>
{cards}
<p class="note">All paths are relative to this file. CSV/parquet open in your spreadsheet tool or a notebook; .md and .py open as text; .svg/.png in the browser. Generated from the outputs/ and notebooks/ directories.</p>
</body></html>"""
(ROOT/"review_index.html").write_text(HTML)
print("wrote review_index.html with", HTML.count("<li>"), "linked files")
