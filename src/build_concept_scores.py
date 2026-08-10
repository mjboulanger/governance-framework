"""
D4: within-concept aggregation. Turn the normalized panel into concept scores.

Latest-available value per metric per country (no recency-drop; recency governs
inclusion at Step-1, not scoring). Tier-weighted mean (P1=1.0/P2=0.5/Sp=0),
renormalized over PRESENT metrics. C8 uses 40/40/20 Fiscal/Monetary/External
bucket weighting (locked 2026-07-24) instead of a flat mean. Min >=1 present to
score; <50% of a concept's included indicators present -> low-confidence flag
(display-only). Metric-level staleness flag (>=4yr) carried in the contributions
table, ZERO score-effect (pure provenance).

Two outputs:
  data/processed/concept_scores.csv        - WIDE: iso3 x concept score + flags (headline)
  data/processed/concept_contributions.csv - LONG: iso3 x concept x metric audit trail
"""
import os
import numpy as np
import pandas as pd
import sys
sys.path.insert(0, os.path.dirname(__file__))
from config import PROCESSED_DIR, CURRENT_YEAR

PROC = PROCESSED_DIR
TIER_W = {"P1": 1.0, "P2": 0.5, "Sp": 0.0}
STALE_YEARS = 4                       # metric-level staleness flag threshold (DEFAULT, revisit Step 4)
LOWCONF_FRAC = 0.50                   # <50% of included indicators present -> low-confidence (locked Step 0.5)

# C8 sub-dimension bucket weighting (LOCKED 2026-07-24). Reconciled to the scored
# set: areaer_er is EXCLUDED (regime type is policy stance not quality), imapp is
# Monetary (macroprudential = financial-stability policy), P2 so romelli stays dominant.
C8_BUCKETS = {
    "fiscal":   (0.40, ["fr_num_rule_types", "fr_max_legal_basis", "fr_any_enforcement",
                        "fr_compliance_mean", "obs_open_budget_index",
                        "pefa_core_management", "pefa_accountability"]),
    "monetary": (0.40, ["romelli_cbi_index", "imapp_breadth_total"]),
    "external": (0.20, ["fari_aggregate", "fari_fdi_aggregate", "fari_fdi_inflow", "kaopen_norm"]),
}
C8_CONCEPT_ID = 8


def _tier_weighted_mean(rows):
    """rows: DataFrame with harmonized + tier. Return (score, sum_present_weight)
    over PRESENT (non-null harmonized) metrics, weights renormalized. Sp (w=0)
    contributes nothing. None if no present metric carries positive weight."""
    r = rows[rows["harmonized"].notna()].copy()
    r["w"] = r["tier"].map(TIER_W).fillna(0.0)
    denom = r["w"].sum()
    if denom <= 0:
        return None, 0.0
    return float((r["w"] * r["harmonized"]).sum() / denom), denom


def _score_c8(rows):
    """C8 bucket-then-tier: within each bucket a tier-weighted mean of present
    metrics; combine buckets at 40/40/20 renormalized over PRESENT buckets (a
    bucket with no present metric drops out and its weight redistributes)."""
    num, wsum = 0.0, 0.0
    detail = {}
    for bucket, (bw, metrics) in C8_BUCKETS.items():
        brows = rows[rows["metric"].isin(metrics)]
        bscore, bpresent = _tier_weighted_mean(brows)
        detail[bucket] = bscore
        if bscore is not None:
            num += bw * bscore
            wsum += bw
    if wsum <= 0:
        return None, detail
    return num / wsum, detail


def build():
    panel = pd.read_csv(os.path.join(PROC, "normalized_panel.csv"))
    sel = pd.read_csv(os.path.join(PROC, "metric_selection.csv"))
    scored = sel[sel["tier"].isin(["P1", "P2", "Sp"])][
        ["metric", "concept_id", "tier"]].dropna(subset=["concept_id"]).copy()
    scored["concept_id"] = scored["concept_id"].astype(int)

    # latest-available value per iso3 x metric (no recency-drop)
    latest = panel.sort_values("year").groupby(["iso3", "metric"]).tail(1).copy()
    latest["stale"] = (CURRENT_YEAR - latest["year"]) >= STALE_YEARS

    # attach concept + tier (a metric can feed several concepts -> merge expands)
    lm = latest.merge(scored, on="metric", how="inner")

    # included-indicator count per concept (denominator for the low-conf flag):
    # count of DISTINCT metrics assigned to the concept (present or not)
    included_n = scored.groupby("concept_id")["metric"].nunique().to_dict()

    score_rows, contrib_rows = [], []
    for (iso3, cid), g in lm.groupby(["iso3", "concept_id"]):
        if cid == C8_CONCEPT_ID:
            score, _detail = _score_c8(g)
        else:
            score, _wsum = _tier_weighted_mean(g)
        present_n = int(g["harmonized"].notna().sum())
        inc_n = included_n.get(cid, present_n)
        low_conf = present_n < LOWCONF_FRAC * inc_n
        if score is None:                 # no present indicator with weight -> no score
            continue
        score_rows.append(dict(iso3=iso3, concept_id=cid, score=score,
                               n_present=present_n, n_included=inc_n,
                               low_confidence=bool(low_conf)))
        for _, r in g.iterrows():
            contrib_rows.append(dict(
                iso3=iso3, concept_id=cid, metric=r["metric"], tier=r["tier"],
                tier_weight=TIER_W.get(r["tier"], 0.0),
                harmonized=r["harmonized"], latest_year=int(r["year"]),
                stale=bool(r["stale"]), present=bool(pd.notna(r["harmonized"]))))

    scores = pd.DataFrame(score_rows).sort_values(["iso3", "concept_id"]).reset_index(drop=True)
    contribs = pd.DataFrame(contrib_rows).sort_values(["iso3", "concept_id", "metric"]).reset_index(drop=True)

    # WIDE headline table: iso3 x concept score, + a companion low-confidence wide flag
    wide = scores.pivot(index="iso3", columns="concept_id", values="score")
    wide.columns = ["C%d_score" % c for c in wide.columns]
    lc = scores.pivot(index="iso3", columns="concept_id", values="low_confidence")
    lc.columns = ["C%d_lowconf" % c for c in lc.columns]
    wide = wide.join(lc).reset_index()

    wide.to_csv(os.path.join(PROC, "concept_scores.csv"), index=False)
    contribs.to_csv(os.path.join(PROC, "concept_contributions.csv"), index=False)
    return scores, contribs, wide


if __name__ == "__main__":
    scores, contribs, wide = build()
    print("concept_scores.csv (long form):", scores.shape,
          "| distinct concepts:", scores.concept_id.nunique(),
          "| distinct countries:", scores.iso3.nunique())
    print("concept_scores.csv (WIDE):", wide.shape)
    print("concept_contributions.csv:", contribs.shape)
    print("score range: [%.3f, %.3f]  mean %.3f" % (scores.score.min(), scores.score.max(), scores.score.mean()))
    print("low-confidence concept-scores: %d / %d (%.1f%%)" % (
        scores.low_confidence.sum(), len(scores), 100*scores.low_confidence.mean()))
    print("stale metric-contributions: %d / %d (%.1f%%)" % (
        contribs.stale.sum(), len(contribs), 100*contribs.stale.mean()))
    # concepts actually produced
    print("concepts scored:", sorted(scores.concept_id.unique()))
