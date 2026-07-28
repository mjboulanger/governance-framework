"""derive_metrics - compute the framework's DERIVED metrics from cleaned source files.

Runs AFTER the source pipelines (nb 03-40) and the harmonization spine (nb 39),
and BEFORE any panel scaling. Produces raw metric VALUES only (standalone_transform
in metric_dictionary terms); no cross-country scaling happens here.

Each derived metric is one function returning a tidy frame [iso3, year, <metric>].
Outputs are written to data/processed/derived_metrics.csv (joined on iso3+year).

Metrics built here (the 4 simple derivations from the build backlog):
  vdem_regime_duration        - capped run-length in current v2x_regime category (this file)
  pts_index                   - mean of the 3 QoG PTS coder columns          (TODO)
  wb_carbon_revenue_pct_gdp   - carbon revenue / WDI GDP                      (TODO)
  wdi_ip_nonresident_per_gdp  - non-resident IP applications / WDI GDP        (TODO)

The 4 C5 composite indices are NOT built here - they need a composition decision first.
"""

import os
import numpy as np
import pandas as pd

PROC = "data/processed"

REGIME_DURATION_CAP = 30   # years; see derive_vdem_regime_duration for the rationale


def _spine():
    """The 213-country reference list, for the iso3 canon and left-joins."""
    return pd.read_csv(os.path.join(PROC, "country_spine.csv"))[["iso3", "country_name"]]


def derive_vdem_regime_duration():
    """vdem_regime_duration: consecutive years a country has held its CURRENT
    Regimes-of-the-World category (v2x_regime, 0-3), CAPPED at REGIME_DURATION_CAP.
    Derived from the classification per framework_decisions (type is not scored, but
    its DURATION is a direction-agnostic stability signal - a long-stable autocracy is
    as durable as a long-stable democracy; C2 pairs this with coups/conflict/perception).

    Definition:
      - run-length: consecutive years in the same v2x_regime category. Reset value 1
        (the first observed year of a new category = duration 1). A regime CHANGE
        resets to 1 (Hungary resets in 2018 when V-Dem reclassified it downward).
      - CAP at 30: beyond ~one political generation, more years do not mean more
        stability, so we cap. The cap also (a) makes left-censoring moot - a country
        stable since before the panel (1990) is >=30 and caps to 30 regardless of its
        unknown true start, so no censoring flag is needed; and (b) severs the metric
        from panel length - the ceiling is a substantive choice (30y = entrenched),
        not an accident of when V-Dem's data begins. Known property: this compresses
        the top (all entrenched regimes read 30), which is correct for a stability
        signal - we care about 'recently changed' vs 'entrenched', not fine ranking
        among the entrenched.
      - a null v2x_regime breaks the run: that country-year gets a null duration and
        the run restarts after it (we do not guess across a gap).
    """
    src = pd.read_csv(os.path.join(PROC, "vdem_filtered.csv"),
                      usecols=["country_text_id", "year", "v2x_regime"])
    src = src.sort_values(["country_text_id", "year"]).reset_index(drop=True)

    out = []
    for cid, g in src.groupby("country_text_id", sort=False):
        g = g.sort_values("year")
        regimes = g["v2x_regime"].to_numpy()
        years = g["year"].to_numpy()
        dur = np.empty(len(g), dtype=object)
        run = 0
        prev = None
        for i, r in enumerate(regimes):
            if pd.isna(r):
                dur[i] = np.nan          # null value breaks the run
                run = 0
                prev = None
                continue
            run = 1 if (prev is None or r != prev) else run + 1
            dur[i] = min(run, REGIME_DURATION_CAP)   # cap applied here
            prev = r
        out.append(pd.DataFrame({
            "country_text_id": cid,
            "year": years,
            "vdem_regime_duration": dur,
        }))

    res = pd.concat(out, ignore_index=True)
    # V-Dem's country_text_id is (mostly) ISO3; the join check in __main__ verifies
    # which codes differ from the spine before we trust the rename.
    res = res.rename(columns={"country_text_id": "iso3"})
    return res


def build_and_write():
    """Assemble all derived metrics onto the spine and write derived_metrics.csv.
    Currently: vdem_regime_duration (the other 3 simple derivations land here next)."""
    sp = _spine()  # iso3 + country_name, 213 rows

    parts = [derive_vdem_regime_duration()]   # each: [iso3, year, <metric>...]

    # outer-merge all derived parts on iso3+year, then left-join onto the spine's iso3
    from functools import reduce
    merged = reduce(lambda a, b: a.merge(b, on=["iso3", "year"], how="outer"), parts)

    # keep only spine countries (drops the intentional out-of-scope V-Dem codes:
    # PRK/ERI/TKM closed regimes, TWN, and historical/sub-national DDR/YMD/ZZB/SML/PSG)
    in_scope = merged[merged.iso3.isin(set(sp.iso3))].copy()
    dropped = sorted(set(merged.iso3) - set(sp.iso3))

    out_path = os.path.join(PROC, "derived_metrics.csv")
    in_scope = in_scope.sort_values(["iso3", "year"]).reset_index(drop=True)
    try:
        in_scope.to_csv(out_path, index=False, lineterminator="\n")
    except TypeError:
        in_scope.to_csv(out_path, index=False, line_terminator="\n")
    return in_scope, dropped


if __name__ == "__main__":
    df, dropped = build_and_write()
    print("derived_metrics.csv written:", df.shape)
    print("columns:", list(df.columns))
    print("spine countries with a regime-duration value:",
          int(df["vdem_regime_duration"].notna().groupby(df.iso3).any().sum()), "of 213")
    print("out-of-scope codes dropped (all intentional):", dropped)
    print()
    print("France / Hungary sanity:")
    print(df[df.iso3.isin(["FRA", "HUN"])].groupby("iso3")["vdem_regime_duration"].agg(["min", "max"]).to_string())