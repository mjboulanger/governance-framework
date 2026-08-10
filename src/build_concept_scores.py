"""
D4: within-concept aggregation. Turn the normalized panel into concept scores,
with FULL score decomposition persisted for dashboard drill-down.

Latest-available value per metric per country (no recency-drop; recency governs
inclusion at Step-1, not scoring). Tier-weighted mean (P1=1.0/P2=0.5/Sp=0),
renormalized over PRESENT metrics. C8 (Macroeconomic and financial policy
framework) uses 40/40/20 Fiscal/Monetary/External bucket weighting (locked
2026-07-24) instead of a flat mean. Min >=1 present to score; <50% of a concept's
included indicators present -> low-confidence flag (display-only). Metric-level
staleness flag (>=4yr) carried in the contributions table, ZERO score-effect
(pure provenance).

Decomposition (every score reconstructable from stored values):
  non-C8 concept score = sum over present metrics of (renormalized_weight * harmonized)
                       = sum of metric_contribution
  bucket subtotal      = sum over present metrics in bucket of metric_contribution
  C8 concept score     = sum over present buckets of (subtotal * w_renorm)
                       = sum of bucket contribution

Outputs:
  data/processed/concept_scores.csv        - WIDE: iso3 x concept score + flags (headline)
  data/processed/concept_contributions.csv - LONG: iso3 x concept x metric audit trail,
                                             incl bucket, renormalized_weight, metric_contribution
  data/processed/bucket_attribution.csv    - LONG: iso3 x concept x bucket subtotal/weight/
                                             contribution (bucketed concepts only; C8 today)
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

# Bucketed-concept config. Keyed by concept_id so the mechanism generalizes; C8
# (Macroeconomic and financial policy framework) is the only bucketed concept today.
# C8 buckets LOCKED 2026-07-24: areaer_er EXCLUDED (regime type is policy stance not
# quality), imapp is Monetary (macroprudential = financial-stability policy), P2 so
# romelli stays dominant.
BUCKET_CONFIG = {
    8: {
        "fiscal":   (0.40, ["fr_num_rule_types", "fr_max_legal_basis", "fr_any_enforcement",
                            "fr_compliance_mean", "obs_open_budget_index",
                            "pefa_core_management", "pefa_accountability"]),
        "monetary": (0.40, ["romelli_cbi_index", "imapp_breadth_total"]),
        "external": (0.20, ["fari_aggregate", "fari_fdi_aggregate", "fari_fdi_inflow", "kaopen_norm"]),
    },
}
# (concept_id, metric) -> bucket, for tagging contribution rows in bucketed concepts
METRIC_BUCKET = {(cid, m): b
                 for cid, buckets in BUCKET_CONFIG.items()
                 for b, (_, ms) in buckets.items()
                 for m in ms}


def _tier_weighted_mean(rows):
    """rows: DataFrame with metric + harmonized + tier. Over PRESENT (non-null
    harmonized) metrics, tier-weighted mean with weights renormalized to sum 1.
    Returns (score, present_weight_sum, renorm) where renorm is dict
    metric -> renormalized weight. Sp (w=0) contributes 0. Returns (None, 0.0, {})
    if no present metric carries positive weight."""
    r = rows[rows["harmonized"].notna()].copy()
    r["w"] = r["tier"].map(TIER_W).fillna(0.0)
    denom = r["w"].sum()
    if denom <= 0:
        return None, 0.0, {}
    renorm = dict(zip(r["metric"], (r["w"] / denom)))
    score = float((r["w"] * r["harmonized"]).sum() / denom)
    return score, denom, renorm


def _score_bucketed(rows, buckets):
    """Bucket-then-tier for a bucketed concept. Within each bucket a tier-weighted
    mean of present metrics; combine buckets at nominal weights renormalized over
    PRESENT buckets (an absent bucket drops out, weight redistributes). Returns
    (score, bucket_detail, metric_renorm):
      bucket_detail: list of dicts, ALL buckets (present or dropped), each with
        bucket, subtotal, w_nominal, w_renorm, contribution, n_present, present
      metric_renorm: dict metric -> WITHIN-BUCKET renormalized weight (present only)."""
    bucket_calc = []
    metric_renorm = {}
    for bucket, (bw, metrics) in buckets.items():
        brows = rows[rows["metric"].isin(metrics)]
        bscore, _bwsum, brenorm = _tier_weighted_mean(brows)
        n_present = int(brows["harmonized"].notna().sum())
        bucket_calc.append([bucket, bscore, bw, n_present])
        metric_renorm.update(brenorm)
    wsum = sum(bw for _, bscore, bw, _ in bucket_calc if bscore is not None)
    if wsum <= 0:
        return None, [], {}
    bucket_detail, score = [], 0.0
    for bucket, bscore, bw, n_present in bucket_calc:
        if bscore is not None:
            w_renorm = bw / wsum
            contribution = bscore * w_renorm
            score += contribution
        else:
            w_renorm, contribution = 0.0, 0.0
        bucket_detail.append(dict(
            bucket=bucket, subtotal=bscore, w_nominal=bw, w_renorm=w_renorm,
            contribution=contribution, n_present=n_present, present=bscore is not None))
    return score, bucket_detail, metric_renorm


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

    score_rows, contrib_rows, bucket_rows = [], [], []
    for (iso3, cid), g in lm.groupby(["iso3", "concept_id"]):
        buckets = BUCKET_CONFIG.get(cid)
        if buckets is not None:
            score, bucket_detail, metric_renorm = _score_bucketed(g, buckets)
        else:
            score, _wsum, metric_renorm = _tier_weighted_mean(g)
        if score is None:                 # no present indicator with weight -> no score
            continue
        present_n = int(g["harmonized"].notna().sum())
        inc_n = included_n.get(cid, present_n)
        low_conf = present_n < LOWCONF_FRAC * inc_n
        score_rows.append(dict(iso3=iso3, concept_id=cid, score=score,
                               n_present=present_n, n_included=inc_n,
                               low_confidence=bool(low_conf)))
        # bucket-level attribution rows (all buckets, present or dropped) for bucketed concepts
        if buckets is not None:
            for bd in bucket_detail:
                bucket_rows.append(dict(iso3=iso3, concept_id=cid, **bd))
        # metric-level attribution rows: renorm weight + contribution to immediate parent
        for _, r in g.iterrows():
            m = r["metric"]
            h = r["harmonized"]
            rw = metric_renorm.get(m, 0.0)          # 0 if absent / NaN / Sp
            contrib = (h * rw) if pd.notna(h) else 0.0
            bkt = METRIC_BUCKET.get((cid, m))       # None outside bucketed concepts
            contrib_rows.append(dict(
                iso3=iso3, concept_id=cid, metric=m, tier=r["tier"],
                tier_weight=TIER_W.get(r["tier"], 0.0),
                harmonized=h, latest_year=int(r["year"]),
                stale=bool(r["stale"]), present=bool(pd.notna(h)),
                bucket=bkt, renormalized_weight=rw, metric_contribution=contrib))

    scores = pd.DataFrame(score_rows).sort_values(["iso3", "concept_id"]).reset_index(drop=True)
    contribs = pd.DataFrame(contrib_rows).sort_values(
        ["iso3", "concept_id", "metric"]).reset_index(drop=True)
    buckets_df = pd.DataFrame(bucket_rows).sort_values(
        ["iso3", "concept_id", "bucket"]).reset_index(drop=True)

    # WIDE headline table: iso3 x concept score, + a companion low-confidence wide flag
    wide = scores.pivot(index="iso3", columns="concept_id", values="score")
    wide.columns = ["C%d_score" % c for c in wide.columns]
    lc = scores.pivot(index="iso3", columns="concept_id", values="low_confidence")
    lc.columns = ["C%d_lowconf" % c for c in lc.columns]
    wide = wide.join(lc).reset_index()

    wide.to_csv(os.path.join(PROC, "concept_scores.csv"), index=False)
    contribs.to_csv(os.path.join(PROC, "concept_contributions.csv"), index=False)
    buckets_df.to_csv(os.path.join(PROC, "bucket_attribution.csv"), index=False)
    return scores, contribs, wide, buckets_df


if __name__ == "__main__":
    scores, contribs, wide, buckets_df = build()
    print("concept_scores.csv (long form):", scores.shape,
          "| distinct concepts:", scores.concept_id.nunique(),
          "| distinct countries:", scores.iso3.nunique())
    print("concept_scores.csv (WIDE):", wide.shape)
    print("concept_contributions.csv:", contribs.shape,
          "| new cols:", [c for c in ["bucket", "renormalized_weight", "metric_contribution"]
                          if c in contribs.columns])
    print("bucket_attribution.csv:", buckets_df.shape,
          "| concepts bucketed:", sorted(buckets_df.concept_id.unique()) if len(buckets_df) else "none",
          "| buckets:", sorted(buckets_df.bucket.unique()) if len(buckets_df) else "none")
    print("score range: [%.3f, %.3f]  mean %.3f" % (
        scores.score.min(), scores.score.max(), scores.score.mean()))
    print("low-confidence concept-scores: %d / %d (%.1f%%)" % (
        scores.low_confidence.sum(), len(scores), 100 * scores.low_confidence.mean()))
    # reconstruction self-check 1: non-bucketed concept score == sum(metric_contribution)
    nb = contribs[~contribs.concept_id.isin(BUCKET_CONFIG)].groupby(
        ["iso3", "concept_id"])["metric_contribution"].sum()
    chk = scores[~scores.concept_id.isin(BUCKET_CONFIG)].set_index(["iso3", "concept_id"])["score"]
    print("non-bucketed reconstruction max|sum(contrib)-score|: %.2e" % (nb - chk).abs().max())
    # reconstruction self-check 2: bucketed concept score == sum(bucket contribution)
    bc = buckets_df.groupby(["iso3", "concept_id"])["contribution"].sum()
    bchk = scores[scores.concept_id.isin(BUCKET_CONFIG)].set_index(["iso3", "concept_id"])["score"]
    print("bucketed reconstruction max|sum(bucket)-score|: %.2e" % (bc - bchk).abs().max())
    # reconstruction self-check 3: bucket subtotal == sum(metric_contribution in bucket)
    pb = buckets_df[buckets_df.present]
    sub = pb.set_index(["iso3", "concept_id", "bucket"])["subtotal"]
    msum = contribs[contribs.bucket.notna()].groupby(
        ["iso3", "concept_id", "bucket"])["metric_contribution"].sum().reindex(sub.index)
    print("metric->bucket reconstruction max|sum(contrib)-subtotal|: %.2e" % (msum - sub).abs().max())
    print("concepts scored:", sorted(scores.concept_id.unique()))