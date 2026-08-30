#!/usr/bin/env python3
"""
Export a tidy CSV time series of category-level scores for every economy.

Source of truth: data/processed/category_history.csv — the SAME file the
dashboard reads to draw its category time series (see build_dashboard_data.py).
No scores are recomputed here, so this export cannot diverge from the dashboard.
Country names and the territory flag come from data/processed/country_coverage.csv.

Nothing about the data is hard-coded: the year range and the country set come
entirely from the files. The ONE hard-coded value is the canonical category
ORDER below (used only for row ordering), because that order lives in the master
document / build_dashboard_data.py, not in any data file.

Output (long / tidy): data/outputs/category_score_history.csv
  columns: iso3, country_name, is_territory, category, year, category_score

Run from the repo root:
    python src/export_category_history.py
"""
import os
import pandas as pd

# --- paths (relative to the repo root) ---
PROC = os.path.join("data", "processed")
OUTDIR = os.path.join("data", "outputs")
SRC = os.path.join(PROC, "category_history.csv")     # iso3, category, year, category_score
COV = os.path.join(PROC, "country_coverage.csv")     # iso3, country_name, is_territory, ...
OUT = os.path.join(OUTDIR, "category_score_history.csv")

# ⚠️ HARD-CODED VALUE — the only one in this script.
# Canonical category order (matches the master document and
# build_dashboard_data.py's CATEGORIES). Used ONLY to order rows. If the
# framework's categories are ever renamed/reordered/added, update this list
# (and keep it in sync with build_dashboard_data.py).
CATEGORY_ORDER = ["Political foundations", "State capacity", "Rule of law",
                  "Accountability", "Economic and fiscal governance"]


def main():
    # fail early with a clear message if run from the wrong directory
    assert os.path.exists(SRC), f"missing {SRC} (run from the repo root)"
    assert os.path.exists(COV), f"missing {COV} (run from the repo root)"

    # canonical category-score history
    hist = pd.read_csv(SRC)                                   # iso3, category, year, category_score
    n_src = len(hist)

    # country name + territory flag (same source the dashboard uses)
    cov = pd.read_csv(COV)[["iso3", "country_name", "is_territory"]]
    assert cov["iso3"].is_unique, "country_coverage.csv has duplicate iso3 rows; join would multiply rows"

    # left-join names/territory onto every history row
    df = hist.merge(cov, on="iso3", how="left")
    assert len(df) == n_src, "row count changed on join (unexpected duplication)"

    # surface any history iso3 with no coverage match (name/flag would be blank)
    n_missing = int(df["country_name"].isna().sum())
    if n_missing:
        iso_missing = sorted(df.loc[df["country_name"].isna(), "iso3"].unique())
        print(f"  WARNING: {n_missing} rows have no country_name match in coverage: {iso_missing}")

    # order rows: canonical category order, then country, then year
    df["category"] = pd.Categorical(df["category"], categories=CATEGORY_ORDER, ordered=True)
    assert df["category"].notna().all(), \
        "a category in the data is missing from CATEGORY_ORDER; update the constant"
    df = df.sort_values(["category", "country_name", "year"], kind="mergesort").reset_index(drop=True)

    # tidy column order
    df = df[["iso3", "country_name", "is_territory", "category", "year", "category_score"]]

    os.makedirs(OUTDIR, exist_ok=True)
    df.to_csv(OUT, index=False)

    # report from the data (nothing hard-coded)
    yr_lo, yr_hi = int(df["year"].min()), int(df["year"].max())
    print(f"wrote {OUT}")
    print(f"  {len(df):,} rows | {df['iso3'].nunique()} economies | "
          f"{df['category'].nunique()} categories | years {yr_lo}-{yr_hi}")


if __name__ == "__main__":
    main()
