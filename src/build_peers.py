"""
build_peers.py - default peer groups for the governance dashboard.

For each in-scope country, selects the TOP 10 peer countries by a similarity score:
  score = income_distance + region_penalty + size_penalty     (income dominates)
    - income_distance: |log(GDPpc_usd) - log(focus GDPpc_usd)|   (primary)
    - region_penalty:  0 same region, 0.15 near region, 0.40 far  (soft lean)
    - size_penalty:    0.08 * |log(pop) - log(focus pop)|, capped 0.35 (soft lean)
Excludes as peers: territories, countries without GDPpc, micro-states (pop < 1M),
and low-coverage countries (< 110 distinct metrics) UNLESS the income-neighbourhood
is broadly data-thin (then the coverage filter relaxes - e.g. Sub-Saharan Africa).

Output: data/processed/country_peers.csv  (iso3, peers)  peers = comma-separated ISO3.
This file is the editable source of truth - hand-edit a row to override a country's
default peers; re-running regenerates all defaults. Documented in instructions doc.

Run:  python src/build_peers.py
"""
import os, sys, math
import pandas as pd, numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from config import PROCESSED_DIR, write_csv

PROC = PROCESSED_DIR
N_PEERS = 10
COV_FLOOR = 110
POP_FLOOR = 1_000_000
SIZE_SCALE = 0.13
SIZE_CAP = 0.55
INCOME_DEADZONE = 1.15   # income within +/-15% treated as equal
INCOME_SQRT_SCALE = 0.55  # concave compression of income distance beyond the deadzone

# ---- region mapping (ISO3 -> broad region) + near-region adjacency ----
REGION = {}
def _add(region, isos):
    for i in isos.split(): REGION[i] = region
_add("North America", "USA CAN")
_add("Latam & Caribbean", "MEX GTM BLZ SLV HND NIC CRI PAN CUB DOM HTI JAM TTO BHS BRB "
     "COL VEN ECU PER BOL BRA PRY URY ARG CHL GUY SUR")
_add("Western Europe", "GBR IRL FRA DEU NLD BEL LUX CHE AUT ITA ESP PRT GRC MLT CYP "
     "DNK SWE NOR FIN ISL")
_add("Eastern Europe & Central Asia", "POL CZE SVK HUN ROU BGR HRV SVN EST LVA LTU "
     "SRB BIH MKD ALB MNE XKX UKR BLR MDA RUS GEO ARM AZE KAZ UZB TKM KGZ TJK")
_add("MENA", "MAR DZA TUN LBY EGY JOR LBN SYR IRQ ISR PSE SAU YEM OMN ARE QAT BHR KWT IRN TUR")
_add("Sub-Saharan Africa", "SEN MLI BFA NER GIN SLE LBR CIV GHA TGO BEN NGA CMR TCD CAF "
     "COD COG GAB GNQ AGO ZMB MWI MOZ ZWE BWA NAM ZAF LSO SWZ MDG MUS "
     "KEN UGA TZA RWA BDI ETH ERI SOM SSD SDN DJI GMB GNB CPV COM")
_add("South Asia", "IND PAK BGD LKA NPL BTN AFG MDV")
_add("East Asia & Pacific", "CHN JPN KOR PRK MNG TWN HKG "
     "VNM LAO KHM THA MMR MYS SGP IDN PHL BRN TLS "
     "AUS NZL PNG FJI SLB VUT WSM TON")
NEAR = {
 "North America": {"Latam & Caribbean", "Western Europe", "East Asia & Pacific"},
 "Latam & Caribbean": {"North America"},
 "Western Europe": {"Eastern Europe & Central Asia", "North America"},
 "Eastern Europe & Central Asia": {"Western Europe", "MENA"},
 "MENA": {"Eastern Europe & Central Asia", "Sub-Saharan Africa", "South Asia"},
 "Sub-Saharan Africa": {"MENA"},
 "South Asia": {"East Asia & Pacific", "MENA"},
 "East Asia & Pacific": {"South Asia", "North America"},
}
def region_of(iso): return REGION.get(iso, "Other")

def load():
    w = pd.read_csv(os.path.join(PROC, "wdi_clean.csv"))
    gcol = "wdi_gdp_per_capita_usd"
    g = w[["country_code", "year", gcol]].dropna(subset=[gcol])
    g = g.sort_values("year").groupby("country_code").tail(1).set_index("country_code")[gcol]
    cov = pd.read_csv(os.path.join(PROC, "country_coverage.csv")).set_index("iso3")
    spine = pd.read_csv(os.path.join(PROC, "country_spine.csv")).set_index("iso3")
    con = pd.read_csv(os.path.join(PROC, "concept_contributions.csv"))
    con = con[con["present"] == True] if "present" in con.columns else con
    ndist = con.groupby("iso3")["metric"].nunique()
    df = pd.DataFrame(index=cov.index)
    df["terr"] = cov["is_territory"].astype(bool)
    df["gdppc"] = g.reindex(df.index)
    df["ndist"] = ndist.reindex(df.index).fillna(0).astype(int)
    df["pop"] = spine["population"].reindex(df.index)
    df["region"] = [region_of(i) for i in df.index]
    return df

def peers_for(df, focus, n=N_PEERS):
    if focus not in df.index or pd.isna(df.loc[focus, "gdppc"]):
        return []
    f = df.loc[focus]; freg = f["region"]
    cand = df.drop(index=focus).copy()
    cand = cand[~cand["terr"]]
    cand = cand[cand["gdppc"].notna()]
    cand = cand[cand["pop"].fillna(0) >= POP_FLOOR]
    lf = math.log(f["gdppc"])
    _raw = (np.log(cand["gdppc"]) - lf).abs()
    _thr = math.log(INCOME_DEADZONE)
    cand["ldist"] = np.sqrt((_raw - _thr).clip(lower=0)) * INCOME_SQRT_SCALE  # deadzone then concave
    def rbonus(r):
        if r == freg: return 0.0
        if r in NEAR.get(freg, set()): return 0.10
        return 0.22
    cand["rpen"] = [rbonus(r) for r in cand["region"]]
    lpf = math.log(f["pop"]) if pd.notna(f["pop"]) and f["pop"] > 0 else None
    if lpf is not None:
        cand["spen"] = ((np.log(cand["pop"].clip(lower=1)) - lpf).abs() * SIZE_SCALE).clip(upper=SIZE_CAP)
    else:
        cand["spen"] = 0.0
    # coverage filter, relaxed if the income-neighbourhood is broadly thin
    near_inc = cand.nsmallest(15, "ldist")
    if near_inc["ndist"].median() >= COV_FLOOR:
        cand = cand[cand["ndist"] >= COV_FLOOR]
    cand["score"] = cand["ldist"] + cand["rpen"] + cand["spen"]
    # deterministic tie-break: score, then iso3
    out = cand.assign(_iso=cand.index.astype(str)).sort_values(["score", "_iso"], kind="mergesort")
    return list(out.head(n).index)

def build():
    df = load()
    rows = []
    no_gdp = []
    for iso in df.index:
        if df.loc[iso, "terr"]:
            continue  # territories get no default peer set (not a focus)
        p = peers_for(df, iso)
        if not p:
            no_gdp.append(iso)
        rows.append({"iso3": iso, "peers": ",".join(p)})
    out = pd.DataFrame(rows).sort_values("iso3")
    write_csv(out, os.path.join(PROC, "country_peers.csv"))
    n_with = sum(1 for r in rows if r["peers"])
    print("country_peers.csv written: %d countries, %d with peers, %d without (no GDPpc)"
          % (len(rows), n_with, len(rows) - n_with))
    if no_gdp:
        print("  no-GDP (empty peer list, manual add in UI):", ", ".join(no_gdp))

if __name__ == "__main__":
    build()
