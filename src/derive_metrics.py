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
import sys
sys.path.insert(0, os.path.dirname(__file__))
from country_harmonization import add_iso3

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


def derive_pts_index():
    q = pd.read_csv(os.path.join(PROC, "qog_clean.csv"), low_memory=False,
                    usecols=["country_code", "year", "pts_amnesty", "pts_hrw", "pts_statedept"])
    coders = ["pts_amnesty", "pts_hrw", "pts_statedept"]
    q["pts_index"] = q[coders].mean(axis=1, skipna=True)
    q = q.rename(columns={"country_code": "iso3"})
    return q[["iso3", "year", "pts_index"]].dropna(subset=["pts_index"])


def _wdi_total_gdp():
    w = pd.read_csv(os.path.join(PROC, "wdi_clean.csv"), low_memory=False,
                    usecols=["country_code", "year", "wdi_gdp_per_capita_usd", "wdi_population_total"])
    w["gdp_usd"] = w["wdi_gdp_per_capita_usd"] * w["wdi_population_total"]
    return w[["country_code", "year", "gdp_usd"]].dropna(subset=["gdp_usd"])


def derive_wb_carbon_revenue_pct_gdp():
    c = pd.read_csv(os.path.join(PROC, "wb_carbon_clean.csv"), low_memory=False,
                    usecols=["country_code", "year", "wb_carbon_revenue_usd_m"]).dropna(subset=["wb_carbon_revenue_usd_m"])
    g = _wdi_total_gdp()
    m = c.merge(g, on=["country_code", "year"], how="inner")
    m["wb_carbon_revenue_pct_gdp"] = (m["wb_carbon_revenue_usd_m"] * 1e6) / m["gdp_usd"] * 100.0
    m = m.rename(columns={"country_code": "iso3"})
    return m[["iso3", "year", "wb_carbon_revenue_pct_gdp"]]


# PEFA composite metrics for C8 (Option C: two composites, not four pillars). Each composite =
# mean of its constituent PILLAR means (so pillars are equal-weighted within a composite -
# framework-controlled, not driven by indicator counts). Pillar means = unweighted mean of that
# pillar's indicator scores (1-4, D=1..A=4), single 2016-framework assessment per country.
# CROSS-SECTIONAL: one assessment per country, vintage varies 2017-2026 (not a time series).
#   pefa_core_management  = mean(Pillar I reliability, Pillar V execution control)  -> C8 P1
#   pefa_accountability   = mean(Pillar VI accounting, Pillar VII external scrutiny) -> C8 P2
# Pillars II/III/IV excluded (II transparency overlaps OBS; III peripheral/SOE v2; IV overlaps
# C8 fiscal-rules leg). VII (audit/scrutiny) overlaps C19 legislative oversight - named in dict.
# quality_flag ignored (2/2621 rows, immaterial). Pillar-level detail not persisted (unscored).
_PEFA_PILLAR_INDS = {
    "I":   ["PI-01", "PI-02", "PI-03"],
    "V":   ["PI-19", "PI-20", "PI-21", "PI-22", "PI-23", "PI-24", "PI-25"],
    "VI":  ["PI-26", "PI-27", "PI-28"],
    "VII": ["PI-29", "PI-30", "PI-31"],
}
_PEFA_COMPOSITES = {
    "pefa_core_management": ["I", "V"],
    "pefa_accountability":  ["VI", "VII"],
}


def derive_pefa_composites():
    import pandas as pd
    d = pd.read_csv(os.path.join(PROC, "pefa_clean.csv"), low_memory=False)
    core = d[(d.framework_version == 2016) & (d.level == "indicator")].copy()
    # pillar mean per country
    pillar = {}
    for pil, inds in _PEFA_PILLAR_INDS.items():
        pillar[pil] = (core[core.indicator_code.isin(inds)]
                       .groupby("country_code")["numeric_score"].mean().rename(pil))
    pil_df = pd.concat(pillar.values(), axis=1)  # index=country_code, cols=pillars
    # composite = mean of its pillar means (equal pillar weight; NaN pillars skipped)
    out = core[["country_code", "assessment_year"]].drop_duplicates().rename(
        columns={"country_code": "iso3", "assessment_year": "year"})
    for comp, pils in _PEFA_COMPOSITES.items():
        s = pil_df[pils].mean(axis=1, skipna=True).rename(comp).reset_index().rename(
            columns={"country_code": "iso3"})
        out = out.merge(s, on="iso3", how="left")
    return out


def derive_fatf_composites():
    """FATF Mutual Evaluation composites (C9 Financial sector regulatory quality).

    fatf_effectiveness        = mean of the 11 Immediate Outcomes  (IO*_num, 0-3: LE/ME/SE/HE)  -> DE FACTO
    fatf_technical_compliance = mean of the 40 Recommendations     (R*_num,  0-3: NC/PC/LC/C)   -> DE JURE

    N/A ratings arrive as NaN and are EXCLUDED from the mean (never counted as 0) - a
    structural exclusion per the metric dictionary, handled by mean(skipna=True).
    Cross-sectional source (one latest assessment per jurisdiction): the value is placed
    at its own assessment year, same convention as derive_pefa_composites.
    """
    import pandas as pd
    d = pd.read_csv(os.path.join(PROC, "fatf_clean.csv"), low_memory=False)

    io_cols = [c for c in d.columns if c.startswith("IO") and c.endswith("_num")]
    r_cols  = [c for c in d.columns if c.startswith("R") and c.endswith("_num")
               and c[1:-4].isdigit()]
    assert len(io_cols) == 11, "expected 11 Immediate Outcome cols, got %d" % len(io_cols)
    assert len(r_cols) == 40, "expected 40 Recommendation cols, got %d" % len(r_cols)

    out = pd.DataFrame({
        "iso3": d["iso3"],
        "year": pd.to_datetime(d["report_date"], errors="coerce").dt.year,
        "fatf_effectiveness":        d[io_cols].mean(axis=1, skipna=True),
        "fatf_technical_compliance": d[r_cols].mean(axis=1, skipna=True),
    })
    out = out[out["iso3"].notna() & out["year"].notna()].copy()
    out["year"] = out["year"].astype(int)
    return out


_WDI_INDICES = {
    # C5 sub-composites (framework_decisions "decompose and equal-weight yourself":
    # else health = 41% of C5 purely on series count). Components combined as
    # equal-weight mean-of-available of their WINSORIZED-Z values (normalize.py,
    # methodology S5 engine) so each contributes equally regardless of raw scale.
    # Inverted components (higher = worse) are negated after the z-transform.
    "wdi_health_index": [
        ("wdi_life_expectancy",            +1),
        ("wdi_mortality_under5",           -1),
        ("wdi_maternal_mortality",         -1),
        ("wdi_immunization_dpt",           +1),
        ("wdi_immunization_measles",       +1),
        ("wdi_uhc_coverage_index",         +1),
        ("wdi_hospital_beds_per_1000",     +1),
        ("wdi_nurses_per_1000",            +1),
        ("wdi_physicians_per_1000",        +1),
    ],
    "wdi_education_index": [
        # pupil_teacher_ratio_PRIMARY excluded separately (0.0% current coverage);
        # expenditure metrics excluded as INPUT-not-outcome (C5 scope)
        ("wdi_primary_completion_rate",       +1),
        ("wdi_primary_enrollment_gross",      +1),
        ("wdi_secondary_enrollment_gross",    +1),
        ("wdi_pupil_teacher_ratio_secondary", -1),
    ],
    "wdi_infrastructure_index": [
        ("wdi_electricity_access",       +1),
        ("wdi_basic_water_access",       +1),
        ("wdi_basic_sanitation_access",  +1),
    ],
    "wdi_social_protection_index": [
        ("wdi_safety_net_coverage",        +1),
        ("wdi_social_insurance_coverage",  +1),
        ("wdi_social_protection_coverage", +1),
    ],
}


def derive_wdi_indices():
    """C5 service-delivery sub-composites from WDI sector components.

    Each component is winsorized-z transformed (S5 engine, its own trailing-20yr
    pooled baseline), direction-aligned (inverted components negated), then the
    index = equal-weight mean of AVAILABLE component z's (union coverage, S4).
    The finished index is itself normalized later as a single metric in S5 -
    re-standardizing an average of z's is benign (preserves order/distances).
    """
    import pandas as pd
    from normalize import normalize_zfamily
    need = sorted({c for comps in _WDI_INDICES.values() for c, _ in comps})
    d = pd.read_csv(os.path.join(PROC, "wdi_clean.csv"),
                    usecols=["country_code", "year"] + need, low_memory=False)
    d = d.rename(columns={"country_code": "iso3"})
    out = d[["iso3", "year"]].copy()
    for index_name, comps in _WDI_INDICES.items():
        zcols = []
        for col, sign in comps:
            z, _prov = normalize_zfamily(d, col, "zscore")
            zc = "_z_%s" % col
            d[zc] = sign * z
            zcols.append(zc)
        out[index_name] = d[zcols].mean(axis=1, skipna=True)
        d.drop(columns=zcols, inplace=True)
    # keep only rows where at least one index has a value
    idx_cols = list(_WDI_INDICES)
    out = out[out[idx_cols].notna().any(axis=1)].copy()
    out["year"] = out["year"].astype(int)
    return out

COUP_WINDOW = 10   # years; trailing-window count of coups (Step-4 parameter, metric_selection)


def derive_pt_coups():
    """pt_coup_successful / pt_coup_failed as 10-YEAR TRAILING WINDOW COUNTS per
    country-year (metric_selection spec). Powell-Thyne stores one row per country-year
    with per-year event counts; a single latest year is nearly always 0 for everyone
    (coups are rare), so the raw per-year value carries almost no cross-country signal.
    The trailing window is what discriminates coup-proneness (Mali 2024 window=4: the
    2020+2021 coups). Powell-Thyne uses COW/GW codes, NOT iso3 - must harmonize.
    Each country reindexed to a continuous year range so the window is a true 10-calendar-
    year lookback (not last-10-rows, which would miscount across gaps)."""
    d = pd.read_csv(os.path.join(PROC, "powell_thyne_clean.csv"))
    d = add_iso3(d, filename_hint="powell_thyne_clean.csv")   # COW/GW -> iso3
    d = d[d["iso3"].notna()][["iso3", "year", "pt_coup_successful", "pt_coup_failed"]].copy()
    d["year"] = pd.to_numeric(d["year"], errors="coerce")
    d = d.dropna(subset=["year"]).astype({"year": int})

    def _window(df, col):
        out = []
        for iso, g in df.groupby("iso3", sort=False):
            g = g.groupby("year")[col].sum()            # collapse any dup rows
            full = pd.Series(0.0, index=range(int(g.index.min()), int(g.index.max()) + 1))
            full.loc[g.index] = g.values
            roll = full.rolling(window=COUP_WINDOW, min_periods=1).sum()
            out.append(pd.DataFrame({"iso3": iso, "year": roll.index.astype(int),
                                     col: roll.values}))
        return pd.concat(out, ignore_index=True)

    succ = _window(d, "pt_coup_successful")
    fail = _window(d, "pt_coup_failed")
    return succ.merge(fail, on=["iso3", "year"], how="outer")


def derive_ucdp_percapita():
    """ucdp_sb_intrastate_deaths_best as log1p(deaths per 100k population)
    (metric_selection spec, corrected: the original 'per-capita, log1p' was a no-op
    because log1p of a ~1e-4 fraction leaves it unchanged; per-100k puts the rate on an
    O(1-100) scale where log1p meaningfully compresses the heavy tail - Syria 2024 =
    8.9/100k -> 2.29, peaceful countries = 0). Size-normalizes (small-country conflict
    is not dwarfed by a large country's) then tail-compresses. Needs WDI population."""
    u = pd.read_csv(os.path.join(PROC, "ucdp_clean.csv"), low_memory=False)
    u = add_iso3(u, filename_hint="ucdp_clean.csv")
    u = u[u["iso3"].notna()][["iso3", "year", "ucdp_sb_intrastate_deaths_best"]].copy()
    u["year"] = pd.to_numeric(u["year"], errors="coerce")
    u = u.dropna(subset=["year"]).astype({"year": int})
    w = pd.read_csv(os.path.join(PROC, "wdi_clean.csv"), low_memory=False)
    w = add_iso3(w, filename_hint="wdi_clean.csv")
    pop = w[w["iso3"].notna() & w["wdi_population_total"].notna()][
        ["iso3", "year", "wdi_population_total"]].copy()
    pop["year"] = pd.to_numeric(pop["year"], errors="coerce")
    m = u.merge(pop, on=["iso3", "year"], how="left")
    per100k = m["ucdp_sb_intrastate_deaths_best"] / m["wdi_population_total"] * 100000.0
    m["ucdp_sb_intrastate_deaths_best"] = np.log1p(per100k)
    # rows where population is missing -> per100k NaN -> drop (can't size-normalize)
    return m[["iso3", "year", "ucdp_sb_intrastate_deaths_best"]].dropna(
        subset=["ucdp_sb_intrastate_deaths_best"])

def build_and_write():
    """Assemble all derived metrics onto the spine and write derived_metrics.csv.
    Currently: vdem_regime_duration, pts_index, wb_carbon_revenue_pct_gdp,
    pefa_core_management + pefa_accountability, fatf_effectiveness + fatf_technical_compliance."""
    sp = _spine()  # iso3 + country_name, 213 rows

    parts = [derive_vdem_regime_duration(), derive_pts_index(), derive_wb_carbon_revenue_pct_gdp(), derive_pefa_composites(), derive_fatf_composites(), derive_wdi_indices(), derive_pt_coups(), derive_ucdp_percapita()]   # each: [iso3, year, <metric>...]

    # outer-merge all derived parts on iso3+year, then left-join onto the spine's iso3
    from functools import reduce
    merged = reduce(lambda a, b: a.merge(b, on=["iso3", "year"], how="outer"), parts)

    # keep only spine countries (drops the intentional out-of-scope V-Dem codes:
    # PRK/ERI/TKM closed regimes, TWN, and historical/sub-national DDR/YMD/ZZB/SML/PSG)
    in_scope = merged[merged.iso3.isin(set(sp.iso3))].copy()
    dropped = sorted(set(merged.iso3) - set(sp.iso3))

    out_path = os.path.join(PROC, "derived_metrics.csv")
    # drop exact-duplicate (iso3,year) rows from the outer-merge of derived parts
    # (e.g. YEM 1990 unification-year: a predecessor polity produced an identical second row)
    in_scope = in_scope.drop_duplicates().reset_index(drop=True)
    _dup = in_scope.duplicated(subset=["iso3", "year"], keep=False)
    if _dup.any():
        raise ValueError("conflicting duplicate iso3-year rows in derived_metrics: %s"
                         % in_scope[_dup][["iso3", "year"]].drop_duplicates().to_dict("records"))
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