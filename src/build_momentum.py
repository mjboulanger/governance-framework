"""
Momentum: the parallel change-over-time coordinate (LOCKED spec, methodology S9).
Two coordinates per (iso3, concept), NEVER blended into the level score:
  magnitude - tier-weighted mean of metric trailing slopes (SD/yr), direction+speed
  breadth   - net diffusion (share improving - share deteriorating), consensus

Computed on the FIXED-baseline panel (harmonized), current snapshot (trailing from
CURRENT_YEAR). Panel-backed metrics only; snapshot/no-history metrics contribute no
slope. A concept with <3 momentum-capable present metrics gets null breadth; a concept
with no slope-capable metrics gets null magnitude (e.g. C9, FATF-only snapshot).

Dead-band (breadth only): |slope| < 0.010 SD/yr counts as flat. Calibrated 2026-08-12
from the realized slope distribution (median 0.0034, p75 0.014): 0.010 filters jitter
while retaining slow-but-real trends (e.g. Georgia CPI -0.013/yr backsliding). Magnitude
uses raw slopes (dead-band does NOT apply to magnitude).

Output: data/processed/momentum.csv  (iso3, concept_id, magnitude, breadth,
        n_slope_metrics, n_improving, n_flat, n_deteriorating)
"""
import os
import sys
import numpy as np
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from config import PROCESSED_DIR, CURRENT_YEAR

PROC = PROCESSED_DIR
DEAD_BAND = 0.010
TIER_W = {"P1": 1.0, "P2": 0.5, "Sp": 0.0}
MIN_YEARS = 3          # need >=3 yrs of history for any slope
MIN_BREADTH_N = 3      # breadth reported only at >=3 slope-capable metrics


def _slope(g, win):
    """OLS slope of harmonized on year over the trailing `win` years; nan if <2 points."""
    s = g[g["year"] > CURRENT_YEAR - win]
    if s["year"].nunique() < 2:
        return np.nan
    return float(np.polyfit(s["year"].values, s["harmonized"].values, 1)[0])


def _blended_slope(g):
    """5yr+3yr blended trailing slope; 3yr-only if <5yr; nan if <3yr of history."""
    if g["year"].nunique() < MIN_YEARS:
        return np.nan
    s5, s3 = _slope(g, 5), _slope(g, 3)
    if np.isnan(s3):
        return np.nan
    return float(np.nanmean([s5, s3])) if not np.isnan(s5) else s3


def build_momentum():
    panel = pd.read_csv(os.path.join(PROC, "normalized_panel.csv"),
                        usecols=["iso3", "metric", "year", "harmonized"]).dropna(subset=["harmonized"])
    sel = pd.read_csv(os.path.join(PROC, "metric_selection.csv"))
    scored = sel[sel["tier"].isin(["P1", "P2", "Sp"])].dropna(subset=["concept_id"]).copy()
    scored["concept_id"] = scored["concept_id"].astype(int)
    m2c = scored.groupby("metric")[["concept_id", "tier"]].first()  # metric -> (concept, tier)

    # per (iso3, metric) blended slope, once
    slopes = {}
    for (iso, m), g in panel.groupby(["iso3", "metric"]):
        if m not in m2c.index:
            continue
        b = _blended_slope(g.sort_values("year"))
        if not np.isnan(b):
            slopes[(iso, m)] = b

    # aggregate to concept: magnitude (tier-weighted mean) + breadth (net diffusion)
    rows = []
    isos = panel["iso3"].unique()
    for iso in isos:
        for cid, cg in scored.groupby("concept_id"):
            mets = cg["metric"].tolist()
            vals = [(m, slopes[(iso, m)], TIER_W[m2c.loc[m, "tier"]])
                    for m in mets if (iso, m) in slopes]
            if not vals:
                rows.append(dict(iso3=iso, concept_id=int(cid), magnitude=np.nan, breadth=np.nan,
                                 n_slope_metrics=0, n_improving=0, n_flat=0, n_deteriorating=0))
                continue
            # magnitude: tier-weighted mean of raw slopes
            wsum = sum(w for _, _, w in vals)
            mag = sum(s * w for _, s, w in vals) / wsum if wsum > 0 else np.nan
            # breadth: dead-band classification, unweighted net diffusion
            imp = sum(1 for _, s, _ in vals if s > DEAD_BAND)
            det = sum(1 for _, s, _ in vals if s < -DEAD_BAND)
            flat = sum(1 for _, s, _ in vals if abs(s) <= DEAD_BAND)
            n = len(vals)
            breadth = (imp - det) / n if n >= MIN_BREADTH_N else np.nan
            rows.append(dict(iso3=iso, concept_id=int(cid), magnitude=mag, breadth=breadth,
                             n_slope_metrics=n, n_improving=imp, n_flat=flat, n_deteriorating=det))
    return pd.DataFrame(rows)


def write_momentum():
    m = build_momentum()
    m.to_csv(os.path.join(PROC, "momentum.csv"), index=False)
    return m


if __name__ == "__main__":
    m = build_momentum()
    print("momentum:", m.shape, "| concepts:", m.concept_id.nunique(), "| countries:", m.iso3.nunique())
    print("magnitude null (no slope-capable metrics):", int(m.magnitude.isna().sum()))
    print("breadth null (<3 slope metrics):", int(m.breadth.isna().sum()))
    print()
    print("C9 (FATF-only, should be mostly null magnitude):",
          "null mag =", int(m[m.concept_id == 9].magnitude.isna().sum()), "of", int((m.concept_id == 9).sum()))
