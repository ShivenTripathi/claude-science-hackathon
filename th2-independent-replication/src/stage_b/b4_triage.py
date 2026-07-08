"""B4 — two-axis target triage: validity (data-internal) x novelty, with druggability tier. Preliminary
(uses Haltavey's arms + Stage A hardening + coherence; full arm-recompute/per-donor pending download)."""
import numpy as np, pandas as pd, re, glob, os
pd.set_option("display.width", 200)

REPO = "/Users/shiventripathi/dev/GWT_perturbseq_analysis_2025"
S = "/Users/shiventripathi/dev/science/th2_suppressor_hardening"
T, SL = f"{S}/results/tables", f"{S}/results/shortlist"

m = pd.read_parquet(f"{T}/arms_hardened.parquet")
sh = m[m.selective].copy()
coh = pd.read_csv(f"{T}/coherence_scores.csv")
sh = sh.merge(coh[["gene","condition","coherence","coh_z_vs_null","best_anchor"]], on=["gene","condition"], how="left")

# ---------- druggability annotation ----------
def load_list(fn):
    try:
        s = pd.read_csv(f"{REPO}/metadata/gene_lists/{fn}", header=None, sep="\t")[0].astype(str)
        return set(s[~s.str.contains("gene", case=False, na=False)])
    except Exception: return set()
classes = {c: load_list(f"{c}.tsv") for c in
           ["kinases","enzymes","gpcr_union","nuclear_receptors","ion_channels",
            "catalytic_receptors","transporters","cytokine_receptors","cytokines","gpi_anchored"]}
lam = pd.read_csv(f"{REPO}/metadata/Lambert_2018_HumanTF.csv")
tfs = set(lam.loc[lam.is_TF == "Yes", "Name"])
SM = {"kinases","enzymes","gpcr_union","nuclear_receptors","ion_channels","catalytic_receptors","transporters"}
SURF = {"cytokine_receptors","cytokines","gpi_anchored"}
UBQ = re.compile(r"^(RNF|TRIM|RBCK|HOIL|HOIP|UBR|UBE|UBA|NEDD4|ITCH|WWP|HECW|DTX|MARCH|MARCHF|CBL|FBXO|FBXW|KLHL|SOCS|SPSB|ASB|CUL|BTRC|NDFIP|SMURF|PELI|MDM|RNF8|BIRC|TRAF)")

def annotate(g):
    hits = [c for c, s in classes.items() if g in s]
    if g in (classes["kinases"]|classes["enzymes"]|classes["gpcr_union"]|classes["nuclear_receptors"]
             |classes["ion_channels"]|classes["catalytic_receptors"]|classes["transporters"]):
        tier, tname = 3, "small-molecule"
    elif g in (classes["cytokine_receptors"]|classes["cytokines"]|classes["gpi_anchored"]):
        tier, tname = 2, "surface/antibody"
    elif g in tfs:
        tier, tname = 1, "TF (hard)"
    else:
        tier, tname = 0, "unannotated"
    return pd.Series({"drug_tier": tier, "drug_class": tname,
                      "is_enzyme": g in classes["enzymes"],
                      "ubiquitin_system": bool(UBQ.match(g)), "class_hits": ",".join(hits)})
sh = pd.concat([sh, sh.gene.apply(annotate)], axis=1)

# ---------- scores ----------
sh["validity"] = (2.0*sh.hardened_pass.astype(int)
                  + sh.stability_score
                  + (sh.donor_evidence == "robust").astype(int)
                  + np.clip(-sh.th2_z, 0, 4)/4
                  + np.clip(sh.coh_z_vs_null.fillna(0), 0, 4)/8)          # coherence = small bonus
sh["novelty"] = sh.atlas_class.map({"novel_selective":1.0,"not_in_atlas":0.8,"moderate":0.5,"concordant":0.1}).fillna(0.8)
# final priority for the FINDING shortlist: validity, but novel hits must clear a higher validity bar (built in via requiring hardened_pass)
sh["priority"] = sh.validity * (0.5 + 0.5*sh.novelty) + 0.3*sh.drug_tier

sh = sh.sort_values("priority", ascending=False)
cols = ["gene","condition","th2_z","th1_z","hardened_pass","donor_evidence","stability_score",
        "atlas_class","coherence","coh_z_vs_null","drug_tier","drug_class","ubiquitin_system",
        "validity","novelty","priority"]
sh[cols].to_csv(f"{SL}/triage_ranked.csv", index=False)

# ---------- report ----------
print("="*70, "\nTARGET TRIAGE (preliminary) — 172 selective hits ranked")
print("-"*70)
print("druggability tiers among the 172:", sh.drug_class.value_counts().to_dict())
print("ubiquitin-system genes in the 172:", sorted(set(sh.loc[sh.ubiquitin_system,"gene"])))
print("\n>>> TOP 20 PRIORITIZED (hardened + novel + druggable, validity-ranked):")
top = sh[sh.hardened_pass].head(20)
print(top[["gene","condition","th2_z","donor_evidence","stability_score","atlas_class",
           "coh_z_vs_null","drug_class","priority"]].to_string(index=False))

print("\n>>> DUAL-EVIDENCE core (hardened + coherence z>2 — arm AND phenocopy):")
dual = sh[(sh.hardened_pass) & (sh.coh_z_vs_null > 2)]
print(dual[["gene","condition","th2_z","coh_z_vs_null","best_anchor","atlas_class","drug_class"]].to_string(index=False))

print("\n>>> DRUGGABLE + hardened + differentiated-from-atlas (small-molecule tractable):")
drug = sh[(sh.hardened_pass) & (sh.drug_tier==3) & (sh.atlas_class.isin(["novel_selective","not_in_atlas","moderate"]))]
print(drug[["gene","condition","th2_z","donor_evidence","stability_score","atlas_class","drug_class","class_hits"]].head(15).to_string(index=False))
print("\nsaved -> results/shortlist/triage_ranked.csv")
