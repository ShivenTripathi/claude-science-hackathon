"""Parse the Phase-4 workflow result into per-gene dossiers (.md + .json) + synthesis."""
import json, sys
from pathlib import Path
ROOT = Path("/Users/shiventripathi/dev/science/th2_selective")
OUT = ROOT/"outputs"; DD = OUT/"mechanism_dossiers"; DD.mkdir(exist_ok=True)
raw = Path(sys.argv[1]).read_text()
data = json.loads(raw)
arr = data["result"] if isinstance(data, dict) and "result" in data else data

FINAL = {"plausible":"plausible","uncertain":"uncertain","unlikely":"unlikely","likely_artifact":"likely_artifact"}
rows = []
for r in arr:
    inv = r.get("investigate") or {}; ver = r.get("verify") or {}; c = r.get("cand") or {}
    gene = c.get("gene") or inv.get("gene")
    final_verdict = ver.get("adjusted_verdict") or inv.get("verdict") or "uncertain"
    ev = inv.get("evidence") or []
    md = f"""# {gene} — selective Th2-suppressor mechanism dossier

**Screen signal:** Th2-arm z = {c.get('th2_arm')}, magnitude-controlled residual = {c.get('th2_resid')}, condition = {c.get('condition')}, class = {c.get('target_class')}{' · druggable' if c.get('druggable') else ''}
**Final verdict (post–adversarial review):** {final_verdict.upper()}  ·  investigator: {inv.get('verdict')} ({inv.get('confidence')} conf) · citations: {ver.get('citations_check')}

## Hypothesis
{inv.get('hypothesis','')}

## Mechanism
{inv.get('th2_mechanism','')}

**Bypasses T-bet / Th1?** {inv.get('bypasses_tbet',{}).get('answer')} — {inv.get('bypasses_tbet',{}).get('rationale','')}

## Evidence
""" + "\n".join(f"- {e.get('claim','')}  \n  _source:_ {e.get('source','')}" for e in ev) + f"""

## Proposed confirming experiment
{inv.get('proposed_experiment','')}

## Adversarial review
- **Citations check:** {ver.get('citations_check')}
- **Agrees artifact call ({inv.get('likely_artifact')}):** {ver.get('artifact_agree')}
- **Notes:** {ver.get('notes','')}
"""
    (DD/f"{gene}.md").write_text(md)
    (DD/f"{gene}.json").write_text(json.dumps({
        "gene": gene, "verdict": final_verdict, "hypothesis": inv.get("hypothesis",""),
        "investigator_verdict": inv.get("verdict"), "confidence": inv.get("confidence"),
        "citations_check": ver.get("citations_check"), "likely_artifact": inv.get("likely_artifact"),
        "druggable": c.get("druggable"), "class": c.get("target_class"),
    }, indent=2))
    rows.append((gene, final_verdict, inv.get("verdict"), ver.get("citations_check"),
                 inv.get("likely_artifact"), c.get("target_class")))

from collections import Counter
verd = Counter(r[1] for r in rows)
print(f"[dossiers] wrote {len(rows)} to {DD}")
print("[final verdicts]", dict(verd))
print(f"{'gene':10s} {'final':14s} {'investig':10s} {'citations':18s} artifact  class")
for g,fv,iv,cc,art,cl in rows:
    print(f"{g:10s} {fv:14s} {str(iv):10s} {str(cc):18s} {str(art):8s} {cl}")
