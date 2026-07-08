"""Parse the self-review literature workflow into a review report + dashboard findings json,
and print the key concerns/corrections for the novelty, leads, and methods audits."""
import json, sys, textwrap
from pathlib import Path
ROOT = Path("/Users/shiventripathi/dev/science/th2_selective"); OUT = ROOT/"outputs"
data = json.loads(Path(sys.argv[1]).read_text())
arr = data["result"] if isinstance(data,dict) and "result" in data else data
byk = {r["key"]: r["finding"] for r in arr if r.get("finding")}

TITLES = {"foundational_biology":"Foundational immunology","known_regulator_directions":"Known-regulator direction reframe",
 "novelty_priorart":"Novelty & prior art","lead_ARNT":"Lead: ARNT","lead_ELAVL1":"Lead: ELAVL1","methods_redteam":"Methods red-team"}

# ---- dashboard json ----
findings=[]
for k,f in byk.items():
    findings.append({"key":k,"title":TITLES.get(k,k),"verdict":f.get("verdict"),
        "top_concern": (f.get("concerns") or [""])[0], "top_correction": (f.get("corrections") or [""])[0]})
(OUT/"review_findings.json").write_text(json.dumps(findings,indent=2))

# ---- markdown report ----
def block(k):
    f=byk.get(k);
    if not f: return f"### {TITLES.get(k,k)}\n(no result)\n"
    s=f"### {TITLES.get(k,k)} — **{f.get('verdict','').replace('_',' ')}**\n\n"
    if f.get("confirmed"): s+="**Holds up:**\n"+"\n".join(f"- {x}" for x in f["confirmed"][:5])+"\n\n"
    if f.get("concerns"): s+="**Concerns:**\n"+"\n".join(f"- {x}" for x in f["concerns"])+"\n\n"
    if f.get("corrections"): s+="**Corrections to make:**\n"+"\n".join(f"- {x}" for x in f["corrections"])+"\n\n"
    if f.get("sources"): s+="**Sources:**\n"+"\n".join(f"- {e.get('claim','')[:110]} — _{e.get('source','')}_" for e in f["sources"][:6])+"\n\n"
    return s

md = f"""# Independent review report — Selective Th2 Suppressor Atlas

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

{block('foundational_biology')}
{block('known_regulator_directions')}
{block('novelty_priorart')}
{block('lead_ARNT')}
{block('lead_ELAVL1')}
{block('methods_redteam')}
"""
(OUT/"review_report.md").write_text(md)
print("[wrote] review_report.md + review_findings.json\n")
for k in ["novelty_priorart","lead_ARNT","lead_ELAVL1","methods_redteam"]:
    f=byk.get(k,{})
    print("="*80); print(k.upper(), "->", f.get("verdict"))
    print("CONCERNS:"); [print("  -",c) for c in (f.get("concerns") or [])]
    print("CORRECTIONS:"); [print("  -",c) for c in (f.get("corrections") or [])]
