"""Generate the live dashboard HTML from current outputs. Re-run after each phase."""
import base64, json, re, html as _html, numpy as np, pandas as pd, yaml
from pathlib import Path
ROOT = Path("/Users/shiventripathi/dev/science/th2_selective")
DATA, OUT = ROOT/"data", ROOT/"outputs"

def b64(p):
    p = OUT/p
    return "data:image/png;base64,"+base64.b64encode(p.read_bytes()).decode() if p.exists() else ""

def _inline(s):
    s = _html.escape(s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<em>\1</em>', s)
    s = re.sub(r'(?<!_)_([^_]+)_(?!_)', r'<em>\1</em>', s)
    return s

def md2html(text):
    """Minimal markdown -> HTML for embedded documents (headings, lists, quotes, rules, inline)."""
    out=[]; lst=None
    def close():
        nonlocal lst
        if lst: out.append(f"</{lst}>"); lst=None
    for raw in text.splitlines():
        ln=raw.rstrip()
        if not ln.strip(): close(); continue
        m=re.match(r'^(#{1,6})\s+(.*)', ln)
        if m: close(); h=min(len(m.group(1))+1,6); out.append(f"<h{h}>{_inline(m.group(2))}</h{h}>"); continue
        if re.match(r'^(---+|\*\*\*+)$', ln.strip()): close(); out.append("<hr>"); continue
        if ln.lstrip().startswith('>'): close(); out.append(f"<blockquote>{_inline(ln.lstrip()[1:].strip())}</blockquote>"); continue
        m=re.match(r'^\s*(\d+)\.\s+(.*)', ln)
        if m:
            if lst!='ol': close(); out.append("<ol>"); lst='ol'
            out.append(f"<li>{_inline(m.group(2))}</li>"); continue
        if re.match(r'^\s*[-*•]\s+', ln):
            if lst!='ul': close(); out.append("<ul>"); lst='ul'
            item=_inline(re.sub(r'^\s*[-*•]\s+','',ln)); out.append(f"<li>{item}</li>"); continue
        close(); out.append(f"<p>{_inline(ln.strip())}</p>")
    close(); return "\n".join(out)

DOCS={}  # id -> rendered html, collected for the modal viewer
def add_doc(doc_id, title, md_text):
    DOCS[doc_id] = f'<h2 class="docttl">{_html.escape(title)}</h2>' + md2html(md_text)
def readbtn(doc_id, label="Read full →"):
    return f'<button class="readbtn" onclick="showDoc(\'{doc_id}\')">{label}</button>'

arms = pd.read_parquet(OUT/"arms.parquet")
short = pd.read_csv(OUT/"real_vs_fp_shortlist.csv") if (OUT/"real_vs_fp_shortlist.csv").exists() else pd.DataFrame()
ctx = pd.read_csv(OUT/"condition_selectivity_matrix.csv") if (OUT/"condition_selectivity_matrix.csv").exists() else pd.DataFrame()
bg = arms.dropna(subset=["th2_arm","th1_arm"])
corr = np.corrcoef(bg.th2_arm, bg.th1_arm)[0,1]
n_sel = int(((arms.th2_arm<-2)&(arms.th1_arm.abs()<1)).sum())
n_skew = int(((arms.th2_arm<-2)&(arms.th1_arm>1)).sum())
n_hc = short.target_gene.nunique() if len(short) else 0
ctxcnt = ctx.context.value_counts().to_dict() if len(ctx) else {}
dossiers = sorted((OUT/"mechanism_dossiers").glob("*.md")) if (OUT/"mechanism_dossiers").exists() else []

# ---- phase config: (title, desc, status, out-html) ----
def chip(s): return {'done':'<span class="chip done">Done</span>','run':'<span class="chip run">Running</span>',
                     'pend':'<span class="chip pend">Queued</span>'}[s]
P4 = 'done' if dossiers else 'run'
phases = [
 ("Phase 0 · Setup & data access","Streamed the authoritative DE_stats.h5ad from public S3 via parallel HDF5 range reads (contiguous float64 matrix; only the 2.8&nbsp;GB zscore layer, not the full 16.8&nbsp;GB).","done",""),
 ("Phase 1 · Reconstruct Th2 / Th1 arms","Projected every perturbation×condition onto the two Ota-2021 arm gene sets; z-scored; validated against the teammate’s checkpoint.","done",
   f"arm corr = {corr:+.2f} (teammate +0.49) · selective = {n_sel} · skewers = {n_skew} · GATA3 = top hit ✓"),
 ("Phase 2 · Credibility pack","Cutoff tiering · donor stability · KD self-silencing · known-regulator recall · per-condition split.","done",
   "Known Th2 activators w/ detectable KD recovered 2/4 (GATA3, RARA; STAT6 trending) · Th1 regulators correctly excluded (0 in box)"),
 ("Phase 3 · Real-vs-false-positive score","KD-confirmed + real-footprint + magnitude-controlled selectivity (Th2 residual after regressing out the Th1 arm) → ranked shortlist.","done",
   f"GATA3 ranks #1 (0.90), RARA #2 — known positives at the top · high-confidence set = {n_hc} genes"),
 ("Phase 4 · Agentic mechanism layer","Per top novel hit: agent investigates literature + pathways → mechanistic hypothesis bypassing T-bet → proposed confirming experiment, citations verified.",P4,
   (f"{len(dossiers)} mechanism dossiers generated" if dossiers else "running on top novel candidates…")),
]

def phase_html(t,d,s,o):
    out = f'<div class="out">{o}</div>' if o else ''
    return f'''<div class="phase">{chip(s)}<div class="body"><div class="pt">{t}</div>
      <div class="pd">{d}</div>{out}</div></div>'''

# ---- shortlist table ----
rows=""
if len(short):
    sh = short.sort_values("real_score",ascending=False).head(22)
    for _,r in sh.iterrows():
        b = "known" if r.bucket=="known_calibration" else "novel"
        bchip = f'<span class="tag {"known" if b=="known" else "novel"}">{b}</span>'
        drug = '<span class="tag drug">druggable</span>' if r.get("druggable",False) else ''
        dc = '✓' if r.get("donor_confirmed",False) else '·'
        rows += (f'<tr><td><b>{r.target_gene}</b> {bchip}{drug}</td>'
                 f'<td class="n">{r.real_score:.2f}</td><td class="n">{r.th2_arm:+.2f}</td>'
                 f'<td class="n">{r.th2_resid:+.2f}</td><td>{r.culture_condition}</td>'
                 f'<td>{r.target_class}</td><td style="text-align:center">{dc}</td></tr>')

ctx_bars=""
if ctxcnt:
    order=["rest_only","stim_induced","mixed","constitutive"]
    labels={"rest_only":"Rest-only","stim_induced":"Stim-induced","mixed":"Mixed","constitutive":"Constitutive"}
    mx=max(ctxcnt.values())
    for k in order:
        v=ctxcnt.get(k,0)
        ctx_bars+=(f'<div class="ctxrow"><div class="ctxlab">{labels[k]}</div>'
                   f'<div class="ctxbar"><div class="ctxfill" style="width:{100*v/mx:.0f}%"></div></div>'
                   f'<div class="ctxn">{v}</div></div>')

plane=b64("plane_plot.png"); recall=b64("recall_overlay.png")

# ---- dossier cards ----
doss_html=""; doss_synth=""
if dossiers:
    metas=[]
    for dp in dossiers:
        try: m=json.loads(dp.with_suffix(".json").read_text()) if dp.with_suffix(".json").exists() else {}
        except Exception: m={}
        m.setdefault("gene",dp.stem); metas.append(m)
    VC={"plausible":("good",0),"uncertain":("warn",1),"unlikely":("bad",2),"likely_artifact":("bad",3)}
    metas.sort(key=lambda m: VC.get(str(m.get("verdict","")).lower(),("warn",1))[1])
    import html as _h
    for m in metas:
        verdict=str(m.get("verdict","")); vclass=VC.get(verdict.lower(),("warn",1))[0]
        drug='<span class="tag drug">druggable</span>' if m.get("druggable") else ''
        gene=m.get("gene")
        mdp=(OUT/"mechanism_dossiers"/f"{gene}.md")
        if mdp.exists(): add_doc(f"doc-{gene}", f"{gene} — mechanism dossier", mdp.read_text())
        rb=readbtn(f"doc-{gene}","Read full dossier →") if mdp.exists() else ""
        doss_html+=(f'<div class="doss"><div class="dh"><b>{gene}</b>'
                    f'<span class="chip {vclass}">{verdict.replace("_"," ")}</span></div>'
                    f'<div class="dhyp">{m.get("hypothesis","")}</div>'
                    f'<div style="margin-top:8px">{drug}<span class="tag known">cites: {m.get("citations_check","")}</span></div>'
                    f'<div style="margin-top:8px">{rb}</div></div>')
    leads=[m["gene"] for m in metas if str(m.get("verdict")).lower() in ("plausible","uncertain") and not m.get("likely_artifact")]
    nart=sum(1 for m in metas if str(m.get("verdict")).lower()=="likely_artifact")
    doss_synth=(f"Adversarial review of the top {len(metas)} candidates kept "
                f"<b>{', '.join(leads) if leads else 'none'}</b> as the non-artifact leads worth following up; "
                f"{nart} were flagged as likely global-effect false positives. The mechanism layer is doing the "
                f"triage the numeric score can’t — surfacing which high-scoring hits are real Th2 biology vs. sick-cell artifacts.")

# ---- independent-review section ----
review_html=""
rf=OUT/"review_findings.json"
if rf.exists():
    VMAP={"well_supported":"good","mostly_supported":"good","mixed":"warn","problematic":"bad"}
    for f in json.loads(rf.read_text()):
        vc=VMAP.get(str(f.get("verdict")),"warn")
        review_html+=(f'<div class="doss"><div class="dh"><b>{f["title"]}</b>'
                      f'<span class="chip {vc}">{str(f.get("verdict","")).replace("_"," ")}</span></div>'
                      f'<div class="dhyp"><b>Concern:</b> {f.get("top_concern","")}</div>'
                      +(f'<div class="dhyp" style="margin-top:6px"><b>Fix:</b> {f.get("top_correction","")}</div>' if f.get("top_correction") else '')
                      +'</div>')
LIMITS=[
 "<b>This is a re-analysis, not a novel method.</b> The two-arm decomposition duplicates the paper's own score_th2/score_th1 (Supplementary Fig 17) using the same Ota-2021 signature; up/down signature scoring is a standard technique (Connectivity Map, UCell). Our contribution is the explicit selective-suppression criterion + the agentic mechanism-triage layer.",
 "<b>GATA3 as a ‘selective’ suppressor is biologically surprising.</b> Canonically GATA3 loss de-represses T-bet/IFNG and skews toward Th1; a flat Th1 arm here may reflect the resting/short-stim human context rather than true selectivity. Treat GATA3 recovery as a sensitivity check, not validation.",
 "<b>The +0.5 arm correlation is partly manufactured by the scoring choice.</b> Unweighted mean-of-z measures absolute signature movement, so both arms move together by construction; a competitive/rank-based score (AUCell/singscore) would remove most of it at the scoring step.",
 "<b>No null / no FDR.</b> The z<-2 gate is an uncalibrated tail; a control-guide permutation null and empirical FDR are needed before trusting the count. Robust set is the core ~12–23 genes, not 127.",
 "<b>Single control arm.</b> ‘Th2 down, Th1 flat’ can't yet exclude lineage diversion (Th17/Treg) or apoptosis; needs other-lineage + viability arms and a functional IL-4/5/13 readout.",
]
limitations_html="".join(f"<li>{x}</li>" for x in LIMITS)
# ---- hardened re-analysis ----
hardened_html=""
hs=OUT/"hardened_stats.json"
if hs.exists():
    h=json.loads(hs.read_text())
    surv=h.get("survivors_from_old",[]); hg=h.get("hardened_genes",[])
    tiles=[("arm corr (mean-of-z)",f"{h['old_corr']:+.2f}","the manufactured confound"),
           ("arm corr (competitive)",f"{h['new_corr']:+.2f}","after rank-based scoring"),
           ("selective, 2-arm",str(h['sel_2arm']),f"FDR {h['fdr_2arm']:.2f}"),
           ("selective, multi-arm",str(h['sel_multi']),f"+Th17/Treg/prolif flat · FDR {h['fdr_multi']:.2f}"),
           ("hardened survivors",str(len(hg)),"+2-signature concordance")]
    kp="".join(f'<div class="kpi"><div class="n">{v}</div><div class="k">{k}</div><div class="t">{t}</div></div>' for k,v,t in tiles)
    hardened_html=(f'<div class="kpis">{kp}</div>'
        f'<div class="q" style="border-left-color:var(--skew)"><b style="color:var(--skew)">The rigorous re-analysis undercuts the original claim — honestly.</b>'
        f'<ul style="margin:10px 0 0;padding-left:18px;font-size:14px;color:var(--muted)">'
        f'<li>Competitive rank scoring collapses the arm correlation <b>{h["old_corr"]:+.2f}→{h["new_corr"]:+.2f}</b> — most of the "global-magnitude confound" was a scoring artifact, as the review predicted.</li>'
        f'<li>Permutation null: the 2-arm selective set (<b>{h["sel_2arm"]}</b>) is <b>not enriched over random gene sets</b> of the same size (expected ~{int(h["sel_2arm"]*h["fdr_2arm"])}, empirical FDR ≈ {h["fdr_2arm"]:.2f}). Genuine selective suppressors are no more common than chance here — a consequence of real Th1/Th2 reciprocity.</li>'
        f'<li><b>GATA3 fails under proper scoring:</b> with the matched Th1-vs-Th0 arm, GATA3 KD drives the Th1 arm to +2.8 — it reads as a Th1-<em>skewer</em>, exactly as canonical biology predicts. The earlier "top selective hit" was a mean-of-z + noisy-Ota-arm artifact.</li>'
        f'<li>Only <b>{len(hg)} genes</b> pass the strict multi-arm + 2-signature concordance gate, and none of the earlier 21 survive; with FDR ≥ 1 even these are not credible targets.</li>'
        f'</ul></div>'
        f'<p class="lede" style="max-width:74ch"><b>Bottom line:</b> the naive selective-Th2-suppressor atlas does not survive rigorous statistics. The real deliverables are the <b>calibrated negative result</b>, the reproducible pipeline, and the agentic review/QC infrastructure — not a target list. The right next step is a functional (IL-4/5/13) readout and control-guide-based FDR before any hit is claimed.</p>')

# ---- local file manifest ----
def man(paths):
    out=""
    for p in paths:
        pp=ROOT/p
        if pp.exists(): out+=f'<li><code>{p}</code></li>'
    return out
manifest_html=man(["dashboard.html","review_index.html","outputs/synthesis.md","outputs/review_report.md",
 "outputs/real_vs_fp_shortlist.csv","outputs/selective_tiered.csv","outputs/condition_selectivity_matrix.csv",
 "outputs/qc_audit_highconf.csv","outputs/plane_plot.svg","outputs/recall_overlay.svg",
 "outputs/mechanism_dossiers/","notebooks/01_arms.py … 09_review_report.py"])

# register long-form documents for the modal viewer
if (OUT/"synthesis.md").exists(): add_doc("doc-synthesis","Synthesis", (OUT/"synthesis.md").read_text())
if (OUT/"review_report.md").exists(): add_doc("doc-review","Independent review report", (OUT/"review_report.md").read_text())
docs_hidden = "".join(f'<div class="doc" id="{k}">{v}</div>' for k,v in DOCS.items())
modal_html = ('<div id="ovl" onclick="hideDoc(event)"><div id="modalpanel">'
              '<button id="mclose" onclick="hideDoc(event,true)" aria-label="Close">&times;</button>'
              '<div id="modalbody"></div></div></div>'
              '<div id="docstore" hidden>'+docs_hidden+'</div>'
              '<script>'
              'function showDoc(id){var s=document.getElementById(id);if(!s)return;'
              'document.getElementById("modalbody").innerHTML=s.innerHTML;'
              'document.getElementById("ovl").style.display="flex";'
              'document.getElementById("modalpanel").scrollTop=0;document.body.style.overflow="hidden";}'
              'function hideDoc(e,force){if(force||e.target.id==="ovl"){'
              'document.getElementById("ovl").style.display="none";document.body.style.overflow="";}}'
              'document.addEventListener("keydown",function(e){if(e.key==="Escape")hideDoc(null,true);});'
              '</script>')

CSS = open(ROOT/"_dash_css.html").read()
HTML = f'''{CSS}
<div class="wrap">
  <div class="eyebrow">Built-with-Claude · Life Sciences · Researcher track</div>
  <h1>Selective Th2 Suppressor Atlas</h1>
  <p class="lede">Knockdowns that take the Th2 program <em>down</em> without flipping CD4+ T cells toward Th1 — the allergy-relevant target the paper’s single Th2−Th1 axis structurally can’t resolve.</p>
  <div class="docbar">{readbtn("doc-synthesis","📄 Synthesis")} {readbtn("doc-review","🔍 Full review report")}</div>

  <div class="kpis">
    <div class="kpi"><div class="n" style="color:var(--accent)">{corr:+.2f}</div><div class="k">Arm correlation</div><div class="t">confound = global magnitude</div></div>
    <div class="kpi"><div class="n">{n_sel}</div><div class="k">Selective (2D gate)</div><div class="t">Th2↓, Th1 flat</div></div>
    <div class="kpi"><div class="n" style="color:var(--skew)">{n_skew}</div><div class="k">True Th1-skewers</div><div class="t">rare — confirms selectivity</div></div>
    <div class="kpi"><div class="n" style="color:var(--accent)">{n_hc}</div><div class="k">High-confidence genes</div><div class="t">KD-confirmed + footprint</div></div>
  </div>

  <div class="q"><b>Calibration.</b> GATA3 (Th2 master regulator) is the #1 selective hit and ranks #1 in the scored shortlist. The known-Th2 list is directionally mixed: activators (GATA3, RARA, STAT6) recover as suppressors, while NuRD/chromatin members (MTA2, CHD4, SETDB1) appear high on the Th1 arm — though literature review shows CHD4/SETDB1 are bimodal, so this is a soft calibration, not a clean dichotomy.</div>

  <div class="q" style="border-left-color:var(--skew)"><b style="color:var(--skew)">Honest status (read this first).</b> This is a rigorous <em>re-analysis + reasoning layer</em>, not a novel method. Independent review (below) flagged real limitations:
    <ul style="margin:10px 0 0;padding-left:18px;font-size:14px;color:var(--muted)">{limitations_html}</ul></div>

  <section>
    <div class="sec-head"><h2>The 2D arm plane</h2><span class="label">headline result</span></div>
    {'<figure><img src="'+plane+'" alt="Th2 vs Th1 arm plane"><figcaption>Every point is one perturbation×condition. Green = selective Th2 suppressor (Th2 arm down, Th1 flat); red = Th1-skewer. The cloud tilts along the diagonal (positive arm correlation) — the dominant confound is global dampening, which the Th1 arm controls for.</figcaption></figure>' if plane else '<p class="placeholder">plane plot pending</p>'}
  </section>

  <section>
    <div class="sec-head"><h2>Context-dependence</h2><span class="label">the novel cut</span></div>
    <p class="lede" style="max-width:68ch">Selectivity is strongly stimulation-dependent — something the paper’s per-condition 1D coefficients can’t express as selectivity. Most selective suppressors act in only one context (GATA3 itself is selective at Rest/Stim8hr but not Stim48hr).</p>
    <div class="ctx">{ctx_bars}</div>
  </section>

  <section>
    <div class="sec-head"><h2>Scored shortlist</h2><span class="label">real vs false-positive</span></div>
    <div class="scroll"><table><thead><tr><th>Gene</th><th>Score</th><th>Th2 arm</th><th>Th2 resid</th><th>Context</th><th>Class</th><th>Donor✓</th></tr></thead><tbody>
    {rows}
    </tbody></table></div>
    <p class="pd" style="color:var(--muted);font-size:13px;margin-top:8px">Th2 resid = Th2 suppression after regressing out the Th1 (global-magnitude) arm. Donor✓ = cross-donor reproducibility confirmed.</p>
  </section>

  {'<section><div class="sec-head"><h2>Mechanism dossiers</h2><span class="label">agentic layer · investigate → verify</span></div><p class="lede" style="max-width:72ch">'+doss_synth+'</p><div class="doss-grid">'+doss_html+'</div></section>' if doss_html else ''}

  <section>
    <div class="sec-head"><h2>Known-regulator recall</h2><span class="label">calibration</span></div>
    {'<figure><img src="'+recall+'" alt="recall overlay"><figcaption>Known Th2 regulators (red) on the plane. Activators land in/near the selective box; repressor-complex members sit high (Th1 induced), correctly excluded.</figcaption></figure>' if recall else ''}
  </section>

  {'<section><div class="sec-head"><h2>Independent review</h2><span class="label">6-agent literature + methods audit</span></div><p class="lede" style="max-width:72ch">Each dimension was audited by a separate agent with web-sourced citations. Verdicts and the top concern/fix per dimension:</p><div class="doss-grid">'+review_html+'</div><div style="margin-top:12px">'+readbtn("doc-review","🔍 Read the full review report (with sources) →")+'</div><p class="pd" style="color:var(--muted);font-size:13px;margin-top:10px">Data/QC fixes already applied: neighboring-gene-KD filter, corrected donor metric (hits-mean, median 0.81), single-guide penalty.</p></section>' if review_html else ''}

  {'<section><div class="sec-head"><h2>Hardened re-analysis</h2><span class="label">answering the review</span></div><p class="lede" style="max-width:74ch">Directly addressing the methods critique: competitive rank-based scoring (removes the confound at the scoring step), a permutation null → empirical FDR, multi-lineage + proliferation control arms, and two-signature concordance.</p>'+hardened_html+'</section>' if hardened_html else ''}

  <section>
    <div class="sec-head"><h2>Review independently</h2><span class="label">self-contained + local files</span></div>
    <p class="lede" style="max-width:72ch">This page embeds everything (figures, full shortlist, full dossiers, review). For click-through access to the raw files on your machine, open <code>review_index.html</code> at the project root — it links every artifact with relative paths.</p>
    <div class="scroll"><ul style="columns:2;font-size:13px;color:var(--muted)">{manifest_html}</ul></div>
  </section>

  <section>
    <div class="sec-head"><h2>Pipeline</h2><span class="label">2026-07-08</span></div>
    {''.join(phase_html(*p) for p in phases)}
  </section>

  <div class="foot">Dataset: Zhu &amp; Dann et al. 2025, genome-scale CRISPRi Perturb-seq in primary human CD4+ T cells (Marson lab). Signature: Ota et al. 2021. · Streamed live from the public Virtual Cells S3 bucket.</div>
</div>
{modal_html}'''

(ROOT/"dashboard.html").write_text(HTML)
print("wrote dashboard.html  | selective", n_sel, "skew", n_skew, "hc", n_hc, "dossiers", len(dossiers))
