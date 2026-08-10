# D6/D7: missingness penalty + category roll-up, with FULL attribution.
#
# Every value used to compute a penalized concept score or a category score is
# persisted at FULL PRECISION (no rounding), so the whole chain (computed score
# -> missingness penalty -> relevance/MQ -> effective weight -> category) is
# reconstructable EXACTLY from stored numbers, no black box. Rounding is a
# display concern and belongs in the dashboard layer, not the stored tables.
#
# Penalty (methodology S7, LOCKED):
#   f = present / (present + absent_penalty_relevant)   [latest slice only]
#     absent_penalty_relevant = missing metrics tagged endogenous OR ambiguous
#     (missing exogenous = blameless scope gap, EXCLUDED from denominator;
#      census always present via zero-fill; present metrics count in numerator)
#   f >= 0.5            -> no penalty
#   0 < f < 0.5         -> w = (0.5 - f) / 0.5 ; penalized = (1-w)*computed + w*floor
#     (ambiguous-driven penalty caps w at 0.5)
#   f = 0               -> no score exists (S8 requires >=1 present); not reached here
#   floor = max(0, floor_low - floor_sd) per concept, over PRE-PENALTY computed
#           scores across countries (floor_low = min, floor_sd = population SD).
#
# Category roll-up: weighted mean of penalized concept scores, weights =
# effective_weight (relevance x MQ). Categories are equal-weighted at the top
# (each category's score is its own internal weighted mean; no cross-category
# weight is applied to form the headline).
#
# Outputs:
#   concept_attribution.csv  - iso3 x concept: full concept-level chain + operands
#   category_scores.csv      - iso3 x category: category score + roll-up operands
#   final_scores.csv         - WIDE iso3 x category headline
#   concept_contributions.csv - re-emitted with missingness_tag added (metric tier)
import os
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, os.path.dirname(__file__))
from config import PROCESSED_DIR

PROC = PROCESSED_DIR
PENALTY_THRESHOLD = 0.5
AMBIG_CAP = 0.5
PENALTY_RELEVANT = {"endogenous", "ambiguous"}
CATEGORY_WEIGHT_RULE = "equal"     # categories equal-weighted at the headline (explicit, locked)


def build():
    scores = pd.read_csv(os.path.join(PROC, "concept_scores.csv"))
    contrib = pd.read_csv(os.path.join(PROC, "concept_contributions.csv"))
    weights = pd.read_csv(os.path.join(PROC, "concept_weights.csv")).set_index("concept_id")
    tags = pd.read_csv(os.path.join(PROC, "metric_missingness_tags.csv")).set_index(
        "metric")["missingness_tag"].to_dict()
    sel = pd.read_csv(os.path.join(PROC, "metric_selection.csv"))
    csrc = pd.read_csv(os.path.join(PROC, "concept_sources.csv")).drop_duplicates("concept_id")
    c2cat = csrc.set_index("concept_id")["category"].to_dict()

    # included metrics per concept (the penalty universe: all assigned scored metrics)
    sc = sel[sel["tier"].isin(["P1", "P2", "Sp"])].dropna(subset=["concept_id"]).copy()
    sc["concept_id"] = sc["concept_id"].astype(int)
    included = sc.groupby("concept_id")["metric"].apply(set).to_dict()

    # low-confidence flag per (iso3, concept), carried onto the attribution row
    lc_long = scores.melt(id_vars="iso3",
                          value_vars=[c for c in scores.columns if c.endswith("_lowconf")],
                          var_name="ccol", value_name="low_confidence").dropna(subset=["low_confidence"])
    lc_long["concept_id"] = lc_long["ccol"].str[1:-8].astype(int)
    lc_map = {(r.iso3, r.concept_id): bool(r.low_confidence) for r in lc_long.itertuples()}

    scored_cids = sorted(int(c[1:-6]) for c in scores.columns if c.endswith("_score"))
    present_set = set(zip(contrib.iso3, contrib.concept_id, contrib.metric))

    # long computed-score frame (pre-penalty), one row per present (iso3, concept)
    long = scores.melt(id_vars="iso3", value_vars=["C%d_score" % c for c in scored_cids],
                       var_name="ccol", value_name="computed").dropna(subset=["computed"])
    long["concept_id"] = long["ccol"].str[1:-6].astype(int)
    long = long.drop(columns="ccol")

    # floor per concept: max(0, min - populationSD) over PRE-PENALTY computed scores.
    # Store both operands so the floor is reconstructable, not just its result.
    floor_low, floor_sd, floor = {}, {}, {}
    for cid, g in long.groupby("concept_id"):
        lo = float(g["computed"].min())
        sd = float(g["computed"].std(ddof=0))
        floor_low[cid], floor_sd[cid] = lo, sd
        floor[cid] = max(0.0, lo - sd)

    rows = []
    for _, r in long.iterrows():
        iso, cid, computed = r["iso3"], int(r["concept_id"]), r["computed"]
        metrics = included.get(cid, set())
        present = sum(1 for m in metrics if (iso, cid, m) in present_set)
        absent_pr_metrics = [m for m in metrics
                             if (iso, cid, m) not in present_set
                             and tags.get(m) in PENALTY_RELEVANT]
        absent_pr = len(absent_pr_metrics)
        denom = present + absent_pr
        f = present / denom if denom > 0 else 1.0
        driver_ambiguous = absent_pr > 0 and all(
            tags.get(m) == "ambiguous" for m in absent_pr_metrics)
        if f >= PENALTY_THRESHOLD:
            w, regime, penalized = 0.0, "none", computed
        else:
            w = (PENALTY_THRESHOLD - f) / PENALTY_THRESHOLD
            regime = "ambiguous" if driver_ambiguous else "endogenous"
            if regime == "ambiguous":
                w = min(w, AMBIG_CAP)
            penalized = (1 - w) * computed + w * floor[cid]
        rel = float(weights.loc[cid, "relevance"])
        mq = float(weights.loc[cid, "measurement_quality"])
        eff = rel * mq
        rows.append(dict(
            iso3=iso, concept_id=cid, category=c2cat.get(cid),
            computed_score=computed,
            # missingness-penalty operands (f is reconstructable from these two)
            n_present=present, n_absent_penalty_relevant=absent_pr, f=f,
            # floor operands (floor is reconstructable: max(0, floor_low - floor_sd))
            floor_low=floor_low[cid], floor_sd=floor_sd[cid], floor=floor[cid],
            penalty_w=w, penalty_regime=regime, penalized_score=penalized,
            # concept-weight chain
            relevance=rel, measurement_quality=mq, effective_weight=eff,
            weighted_contribution=penalized * eff,
            # carried context so the row is self-contained
            low_confidence=lc_map.get((iso, cid), False)))
    ca = pd.DataFrame(rows)
    ca.to_csv(os.path.join(PROC, "concept_attribution.csv"), index=False)

    # category roll-up: weighted mean of penalized concept scores, weights = effective_weight
    cat_rows = []
    for (iso, cat), g in ca.groupby(["iso3", "category"]):
        wsum = g["effective_weight"].sum()
        cat_score = g["weighted_contribution"].sum() / wsum if wsum > 0 else np.nan
        cat_rows.append(dict(
            iso3=iso, category=cat, category_score=cat_score,
            n_concepts=len(g), sum_effective_weight=wsum,
            category_weight_rule=CATEGORY_WEIGHT_RULE))
    cats = pd.DataFrame(cat_rows)
    cats.to_csv(os.path.join(PROC, "category_scores.csv"), index=False)

    # WIDE headline
    wide = cats.pivot(index="iso3", columns="category", values="category_score").reset_index()
    wide.to_csv(os.path.join(PROC, "final_scores.csv"), index=False)

    # re-emit contributions with the missingness tag on each metric row
    contrib["missingness_tag"] = contrib["metric"].map(tags)
    contrib.to_csv(os.path.join(PROC, "concept_contributions.csv"), index=False)

    return ca, cats, wide


if __name__ == "__main__":
    ca, cats, wide = build()
    print("concept_attribution.csv:", ca.shape)
    pen = ca[ca.penalty_w > 0]
    print("  penalties fired (w>0):", len(pen),
          "| by concept:", pen.groupby("concept_id").size().to_dict())
    print("  penalty_regime:", pen.penalty_regime.value_counts().to_dict())
    print("category_scores.csv:", cats.shape, "| categories:", sorted(cats.category.unique()))
    print("final_scores.csv (wide):", wide.shape)
    # attribution completeness (now at machine precision, values stored unrounded):
    frec = ca.apply(lambda r: r.n_present / (r.n_present + r.n_absent_penalty_relevant)
                    if (r.n_present + r.n_absent_penalty_relevant) > 0 else 1.0, axis=1)
    print("f reconstruction max|rebuilt-stored|: %.2e" % (frec - ca.f).abs().max())
    frl = (ca.floor_low - ca.floor_sd).clip(lower=0)
    print("floor reconstruction max|rebuilt-stored|: %.2e" % (frl - ca.floor).abs().max())
    prec = (1 - ca.penalty_w) * ca.computed_score + ca.penalty_w * ca.floor
    print("penalized reconstruction max|rebuilt-stored|: %.2e" % (prec - ca.penalized_score).abs().max())
    catrec = ca.groupby(["iso3", "category"]).apply(
        lambda g: g.weighted_contribution.sum() / g.effective_weight.sum(), include_groups=False)
    catm = cats.set_index(["iso3", "category"])["category_score"]
    print("category reconstruction max|rebuilt-stored|: %.2e" % (catrec - catm).abs().max())
    print("\ncategory score ranges:")
    for cat in sorted(cats.category.unique()):
        s = cats[cats.category == cat]["category_score"]
        print("  %-34s [%.3f, %.3f] mean %.3f n=%d" % (cat, s.min(), s.max(), s.mean(), len(s)))