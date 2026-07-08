"""
Phase 3: real-vs-false-positive composite score over selective candidates.
Hard gate = KD-confirmed + real transcriptional footprint + Th1-flat + not artifact class.
Ranking driver = magnitude-controlled selectivity: regress the Th2 arm on the Th1 arm
(the built-in control) and rank on the *residual* Th2 suppression (isolates the +0.54
global-dampening confound far better than a raw DE-breadth penalty, which wrongly hurts
strong real regulators like GATA3).
Run after 03_credibility.py -> outputs/real_vs_fp_shortlist.csv
"""
import numpy as np, pandas as pd, yaml, statsmodels.api as sm
from pathlib import Path
ROOT = Path("/Users/shiventripathi/dev/science/th2_selective")
DATA, OUT = ROOT/"data", ROOT/"outputs"
df = pd.read_parquet(OUT/"candidates_full.parquet")
known = yaml.safe_load(open(DATA/"th1_th2_known_regulators.yaml"))
th2_known = set(known["th2"])

# --- magnitude control: residual Th2 after regressing out the Th1 arm (global mode) ---
d = df.dropna(subset=["th2_arm","th1_arm"]).copy()
X = sm.add_constant(d["th1_arm"].to_numpy())
res = sm.OLS(d["th2_arm"].to_numpy(), X).fit()
d["th2_resid"] = d["th2_arm"].to_numpy() - res.predict(X)
df = df.merge(d[["obs_index","th2_resid"]], on="obs_index", how="left")

def unit(x, lo, hi): return np.clip((np.asarray(x,float)-lo)/(hi-lo), 0, 1)

# --- hard confidence gate ---
df["evidence_ok"] = df.n_total_de_genes.fillna(0) >= 10           # real transcriptional footprint
nbr = df.get("neighbor_kd_flag", pd.Series(False,index=df.index)).fillna(False)
df["hc_selective"] = (df.sel_default & df.kd_ok & df.evidence_ok
                      & ~df.is_artifact_class.fillna(False) & ~df.offtarget_flag.fillna(False)
                      & ~nbr)                                      # drop neighboring-gene-KD artifacts (e.g. AHSA1)
sel = df[df.hc_selective].copy()

# cross-condition consistency: per gene, fraction of tested conditions with th2_arm<0
cons = df.groupby("target_gene").apply(lambda g:(g.th2_arm<0).mean(), include_groups=False).rename("consistency")
sel = sel.merge(cons, on="target_gene", how="left")

donor_metric = sel.get("donor_hits", pd.Series(np.nan,index=sel.index)).fillna(sel["crossdonor_correlation_mean"])
sel["s_selectivity"] = unit(-sel["th2_resid"], 0, 3)                      # deeper residual suppression
sel["s_guide"]       = unit(sel["crossguide_correlation"].fillna(sel["crossguide_correlation"].median()), 0, 1)
sel["s_donor"]       = np.where(donor_metric.isna(), 0.5, unit(donor_metric, 0, 1))
sel["s_consistency"] = sel["consistency"].fillna(0)
sel["single_guide_flag"] = sel.get("single_guide_flag", pd.Series(False,index=sel.index)).fillna(False)
W = dict(s_selectivity=.40, s_donor=.25, s_guide=.15, s_consistency=.20)
sel["real_score"] = sum(sel[k]*w for k,w in W.items()) * np.where(sel["single_guide_flag"], 0.85, 1.0)

DRUGGABLE = {"E3_ligase","kinase"}
sel["druggable"] = sel["target_class"].isin(DRUGGABLE)
sel["donor_confirmed"] = donor_metric.fillna(-1) >= 0.3
sel["bucket"] = np.where(sel.target_gene.isin(th2_known), "known_calibration", "novel_candidate")

best = sel.sort_values("real_score", ascending=False).drop_duplicates("target_gene")
out_cols = ["target_gene","bucket","real_score","culture_condition","th2_arm","th1_arm","th2_resid",
            "consistency","donor_confirmed","target_class","druggable","tier","n_total_de_genes",
            "ontarget_effect_size","frac_signif_guides","crossdonor_correlation_mean","crossguide_correlation"]
best = best[out_cols].sort_values("real_score", ascending=False)
best.to_csv(OUT/"real_vs_fp_shortlist.csv", index=False)

print(f"[hc gate] selective+KD+footprint rows={len(sel)}  unique genes={best.target_gene.nunique()}")
print("[bucket]\n", best.bucket.value_counts())
print("\n[known calibration recovered]")
print(best[best.bucket=='known_calibration'][["target_gene","real_score","th2_arm","th2_resid","donor_confirmed"]].to_string(index=False))
print("\n[top 20 novel candidates]")
print(best[best.bucket=='novel_candidate'].head(20)[
    ["target_gene","real_score","culture_condition","th2_arm","th2_resid","target_class","druggable","donor_confirmed","tier"]].to_string(index=False))
print("\n[druggable (E3/kinase) novel candidates]")
dn = best[(best.bucket=='novel_candidate') & best.druggable]
print(dn[["target_gene","real_score","culture_condition","th2_resid","target_class","donor_confirmed"]].to_string(index=False) if len(dn) else "  (none in high-confidence set)")
