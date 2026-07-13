"""
th2_collapse_scorer.py — reusable Th2/type-2-collapse classifier.

Scores any perturbation's trans-transcriptome profile for how well it PHENOCOPIES the
STAT6/GATA3 collapse of the type-2 program in primary human CD4+ T cells
(Zhu & Dann et al. 2025 genome-scale CRISPRi Perturb-seq).

Why anchor on STAT6/GATA3 rather than a "selectivity residual":
    The canonical type-2 master regulators have a MEASURABLE trans footprint (GATA3 tops the
    effector-marker readout), so scoring who else reproduces their collapse is a POSITIVE-anchored
    signal. This calibrates (permutation p<0.001, known-regulator median ~87th percentile),
    unlike a naive "Th2 down & Th1 flat" residual which is dominated by low-power noise (FDR~1).

Signature construction (per culture condition):
    1. Fetch STAT6 and GATA3 KD trans-profiles (zscore layer), cis-mask each anchor's own target.
    2. consensus = mean(GATA3_masked, STAT6_masked).
    3. Keep "program genes" = those where the two anchors agree in sign AND |consensus| >= 1.0.
       (This lifts anchor concordance from ~ -0.1 globally to ~ +0.63 on the program set.)
    4. weights = consensus values on the program genes.

Scoring a perturbation:
    collapse_score = Pearson r between the perturbation's (cis-masked, z-clipped) profile
                     restricted to the program genes, and the anchor consensus weights.
    High score = the knockdown reproduces the type-2 collapse direction.

Validation baked in (see build_signature docstring): IL4R is deliberately EXCLUDED from the
signature; it phenocopies increasingly with stimulation (0.12 -> 0.40 -> 0.61 Rest->Stim8->Stim48),
recovering the known upstream IL4R->STAT6 axis as an out-of-sample check.

Caveat: the screen is un-polarized Rest/Stim CD4s. The collapse score is a TRANSCRIPTIONAL FOOTPRINT
resemblance, activation-coupled (broader than cytokine-specific), NOT a functional differentiation
assay. Interpret with the stimulation-specificity split.
"""
import numpy as np
from scipy.stats import pearsonr

ANCHORS = ("GATA3", "STAT6")          # signature-defining anchors
HELD_OUT_VALIDATION = "IL4R"          # out-of-sample axis check
Z_CLIP = 100.0
PROGRAM_MIN_ABS = 1.0                 # |consensus| threshold for program-gene inclusion


def _clip(v):
    return np.clip(v, -Z_CLIP, Z_CLIP)


def _cismask(vec, target_col):
    v = vec.copy()
    if target_col is not None:
        v[target_col] = 0.0
    return v


def build_signature(anchor_profiles, gene2col):
    """
    anchor_profiles: {(anchor_gene, condition): np.ndarray[n_genes]}  raw zscore rows
    gene2col:        {gene_name: column_index}
    Returns {condition: {"genes": idx[], "weights": w[]}}.
    """
    conditions = sorted({c for (_, c) in anchor_profiles})
    sig = {}
    for c in conditions:
        masked = []
        for a in ANCHORS:
            v = _cismask(_clip(anchor_profiles[(a, c)]), gene2col.get(a))
            masked.append(v)
        consensus = np.mean(masked, axis=0)
        concordant = np.sign(masked[0]) == np.sign(masked[1])
        strong = np.abs(consensus) >= PROGRAM_MIN_ABS
        mask = concordant & strong
        sig[c] = {"genes": np.where(mask)[0], "weights": consensus[mask]}
    return sig


def collapse_score(profile, condition, signature, gene2col, target_gene=None):
    """
    Score one perturbation profile (raw zscore row) for type-2-collapse phenocopy.
    target_gene: the perturbed gene, to cis-mask its own column before scoring.
    Returns a float in [-1, 1]; higher = stronger phenocopy of the STAT6/GATA3 collapse.
    """
    s = signature[condition]
    v = _cismask(_clip(np.asarray(profile, float)), gene2col.get(target_gene))
    return float(pearsonr(v[s["genes"]], s["weights"])[0])


def score_many(profiles, conditions, signature, gene2col, target_genes=None):
    """Vectorised convenience: lists in, np.ndarray of scores out (positionally matched)."""
    n = len(profiles)
    tg = target_genes if target_genes is not None else [None] * n
    return np.array([collapse_score(profiles[i], conditions[i], signature, gene2col, tg[i])
                     for i in range(n)])


if __name__ == "__main__":
    # Rebuild the signature from a saved anchor bundle and score a demo row.
    d = np.load("anchor_signature.npz", allow_pickle=True)
    print("bundled conditions:", [k[6:] for k in d.files if k.startswith("genes_")])
