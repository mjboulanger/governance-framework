"""
D3 orchestration: build the normalized metric panel (methodology S5).

Reads every scored metric from its source file, applies its assigned final_method
(z-family / percentile / binary / fixed-anchor) against the fixed trailing-20yr
pooled baseline, harmonizes to a common 0-1 scale, direction-aligns so higher =
better, and writes one long panel: data/processed/normalized_panel.csv.

Inputs (all already built):
  - metric_selection.csv          : the 144 scored metrics, tier, direction
  - metric_distribution_profile.csv: final_method + the source FILE per metric
  - metric_missingness_tags.csv    : census metrics needing spine zero-fill
  - country_spine.csv              : the 213-country spine
  - the ~32 cleaned source files

Output columns (long, one row per iso3 x year x metric):
  iso3, year, metric, raw_value, normalized, harmonized, direction,
  final_method, method_source, baseline_n_years, baseline_n_obs, baseline_year_span
"""
import os
import numpy as np
import pandas as pd

import sys
sys.path.insert(0, os.path.dirname(__file__))
import re
from config import PROCESSED_DIR, RAW_DIR, FRAMEWORK_START_YEAR, CURRENT_YEAR
from country_harmonization import add_iso3
from normalize import (normalize_zfamily, normalize_percentile,
                       normalize_binary, normalize_fixed_anchor)

PROC = PROCESSED_DIR
ZFAMILY = {"zscore", "log_zscore", "log1p_zscore"}
# census metrics whose absent spine country-years are a REAL 0 (D5a build note):
CENSUS_ZEROFILL = {"climate_laws_cumulative", "wb_carbon_pricing_exists"}


def _load_vintage_years():
    """source_id -> data-as-of YEAR, parsed from download_log.csv (pipeline-
    maintained vintage field). Dates cross-sectional sources that carry no year
    column so 'latest available' enters at its TRUE vintage (BRSS 2016), not
    stamped current. Data-driven: re-fetch updates the log, vintage flows."""
    dl = pd.read_csv(os.path.join(RAW_DIR, "download_log.csv"), dtype=str)
    out = {}
    for _, r in dl.iterrows():
        s = r.get("data_as_of_date")
        if pd.isna(s):
            continue
        m = re.search(r"(19|20)\d{2}", str(s))
        if m:
            out[r["source_id"]] = int(m.group(0))
    return out


_VINTAGE = _load_vintage_years()


def _harmonize(normalized, method):
    """Map a normalized Series to the common 0-1 scale (S5 harmonization).
    z-family: (clip(z,+/-3)+3)/6. percentile/binary/fixed-anchor: already 0-1."""
    if method in ZFAMILY:
        return (normalized.clip(-3, 3) + 3) / 6.0
    return normalized  # percentile, binary, fixed-anchor already on 0-1


def _load_metric(metric, fname, spine, source_id):
    """Read one metric's [iso3, year, value] from its source file, spine-filtered,
    framework-era (>=FRAMEWORK_START_YEAR). Year-less cross-sectional sources are
    dated at their true download_log vintage. Census metrics are spine-zero-filled."""
    d = pd.read_csv(os.path.join(PROC, fname), low_memory=False)
    d = add_iso3(d, filename_hint=fname)
    d = d[d["iso3"].notna() & d["iso3"].isin(spine)]
    if metric not in d.columns:
        return None
    if "year" not in d.columns:
        # cross-sectional source (BRSS, CPJ, RTI, polfinance): no time dimension.
        # Date at TRUE vintage from download_log.data_as_of_date, NOT CURRENT_YEAR
        # ("latest available" is not "current" - BRSS is a 2016 wave). Baseline
        # then collapses to the cross-section of countries, exactly like PEFA.
        vint = _VINTAGE.get(source_id)
        if vint is None:
            raise ValueError("no download_log vintage for year-less source %s (metric %s)" % (source_id, metric))
        d = d.copy()
        d["year"] = vint
    out = d[["iso3", "year", metric]].rename(columns={metric: "value"})
    out["value"] = pd.to_numeric(out["value"], errors="coerce")
    out["year"] = pd.to_numeric(out["year"], errors="coerce")
    out = out.dropna(subset=["year"]).copy()
    out["year"] = out["year"].astype(int)
    # framework era only: drop pre-1990 history (baseline still uses the recent
    # 20yr window regardless; this just trims the emitted panel to 1990+)
    out = out[out["year"] >= FRAMEWORK_START_YEAR]

    if metric in CENSUS_ZEROFILL:
        # full spine x year grid, fill absent country-years with 0, KEEP present
        # values (correct for cumulative: 0 before first law, actual after)
        yrs = range(FRAMEWORK_START_YEAR, CURRENT_YEAR + 1)
        grid = pd.MultiIndex.from_product([sorted(spine), yrs], names=["iso3", "year"]).to_frame(index=False)
        out = grid.merge(out, on=["iso3", "year"], how="left")
        out["value"] = out["value"].fillna(0.0)
    return out
def build():
    spine = set(pd.read_csv(os.path.join(PROC, "country_spine.csv"))["iso3"])
    sel = pd.read_csv(os.path.join(PROC, "metric_selection.csv"))
    scored = sel[sel["tier"].isin(["P1", "P2", "Sp"])].drop_duplicates("metric")
    direction = scored.set_index("metric")["direction"].to_dict()
    source_of = scored.set_index("metric")["source_id"].to_dict()
    prof = pd.read_csv(os.path.join(PROC, "metric_distribution_profile.csv"))
    file_of = prof.set_index("metric")["file"].to_dict()
    method_of = prof.set_index("metric")["final_method"].to_dict()
    msource_of = prof.set_index("metric")["method_source"].to_dict()

    metrics = sorted(scored["metric"].unique())
    parts, skipped = [], []

    for m in metrics:
        fname = file_of.get(m)
        method = method_of.get(m)
        d = _load_metric(m, fname, spine, source_of.get(m))
        if d is None or d["value"].notna().sum() == 0:
            skipped.append((m, "no data / not loadable"))
            continue

        if method in ZFAMILY:
            norm, prov = normalize_zfamily(d, "value", method)
        elif method == "percentile":
            norm, prov = normalize_percentile(d, "value")
        elif method == "binary":
            norm, prov = normalize_binary(d, "value")
        elif method == "fixed_anchor":
            norm, prov = normalize_fixed_anchor(d, "value")
        else:
            skipped.append((m, "unknown method %r" % method))
            continue

        harm = _harmonize(norm, method)
        # direction-align: higher = better everywhere. flip if metric is "-".
        if str(direction.get(m)).strip() == "-":
            harm = 1.0 - harm

        span = prov.get("baseline_year_span")
        part = pd.DataFrame({
            "iso3": d["iso3"].values, "year": d["year"].values, "metric": m,
            "raw_value": d["value"].values,
            "normalized": norm.values, "harmonized": harm.values,
            "direction": direction.get(m), "final_method": method,
            "method_source": msource_of.get(m),
            "baseline_n_years": prov.get("baseline_n_years"),
            "baseline_n_obs": prov.get("baseline_n_obs"),
            "baseline_year_span": ("%d-%d" % (span[0], span[1])) if span else None,
        })
        # drop rows with no raw value (census keeps its 0s; others drop NaN)
        part = part[part["raw_value"].notna()]
        parts.append(part)

    panel = pd.concat(parts, ignore_index=True)
    panel = panel.sort_values(["metric", "iso3", "year"]).reset_index(drop=True)
    out_path = os.path.join(PROC, "normalized_panel.csv")
    try:
        panel.to_csv(out_path, index=False, lineterminator="\n")
    except TypeError:
        panel.to_csv(out_path, index=False, line_terminator="\n")
    return panel, skipped


if __name__ == "__main__":
    panel, skipped = build()
    print("normalized_panel.csv written:", panel.shape)
    print("distinct metrics:", panel["metric"].nunique(), "/ 144 scored")
    print("distinct countries:", panel["iso3"].nunique())
    print("year range:", int(panel["year"].min()), "-", int(panel["year"].max()))
    print("harmonized range: [%.3f, %.3f]  mean %.3f" % (
        panel["harmonized"].min(), panel["harmonized"].max(), panel["harmonized"].mean()))
    if skipped:
        print("\nSKIPPED metrics (%d) - INVESTIGATE:" % len(skipped))
        for m, why in skipped:
            print("  ", m, "->", why)
    else:
        print("\nno metrics skipped - all 144 normalized")
