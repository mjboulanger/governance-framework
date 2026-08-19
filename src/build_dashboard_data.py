"""
Dashboard data layer: read all processed score/history/momentum/contribution files,
join human labels, emit ONE compact dashboard_data.json that every view and the Excel
companion read.

Compression: metric definitions/sources live ONCE in meta.metrics (referenced by key,
not repeated per country); scores rounded to 3dp; comp_summary stored sparsely.

Run from repo root:  python src/build_dashboard_data.py
Output: dashboard/dashboard_data.json
"""
import os
import sys
import json
import math
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from config import PROCESSED_DIR
from concept_sources import to_rows
from metric_dictionary import DICT as METRIC_DICT

PROC = PROCESSED_DIR
OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dashboard")
CATEGORIES = ["Accountability", "Economic and fiscal governance",
              "Political foundations", "Rule of law", "State capacity"]


def _n(x, dp=3):
    if x is None:
        return None
    try:
        f = float(x)
    except (TypeError, ValueError):
        return None
    if math.isnan(f) or math.isinf(f):
        return None
    return round(f, dp)


def _b(x):
    return bool(x) if x == x else False


def build():
    csrc = pd.DataFrame(to_rows()).drop_duplicates("concept_id")
    concept_name = dict(zip(csrc.concept_id, csrc.concept_name))
    concept_cat = dict(zip(csrc.concept_id, csrc.category))

    fs = pd.read_csv(os.path.join(PROC, "final_scores.csv")).set_index("iso3")
    cs = pd.read_csv(os.path.join(PROC, "concept_scores.csv")).set_index("iso3")
    cov = pd.read_csv(os.path.join(PROC, "country_coverage.csv")).set_index("iso3")
    mom = pd.read_csv(os.path.join(PROC, "momentum.csv"))
    mom_by = {(r.iso3, int(r.concept_id)): r for r in mom.itertuples()}
    scored_cids = sorted(int(c[1:-6]) for c in cs.columns if c.endswith("_score"))

    countries = {}
    # distinct-metric counts per country (total + per category) for the panel header.
    # (country_coverage.metrics_present over-counts; use distinct metrics actually scoring.)
    _con = pd.read_csv(os.path.join(PROC, "concept_contributions.csv"))
    _con = _con[_con["present"] == True] if "present" in _con.columns else _con
    _con = _con.copy()
    _con["_cat"] = _con["concept_id"].map({cid: concept_cat.get(cid) for cid in scored_cids})
    metric_counts = {}
    for _iso, _g in _con.groupby("iso3"):
        _by = {c: int(gg["metric"].nunique()) for c, gg in _g.groupby("_cat") if c}
        metric_counts[_iso] = {"total": int(_g["metric"].nunique()), "by_cat": _by}

    # default peer groups (from build_peers.py); iso3 -> list of peer iso3
    import os as _os
    _peers_path = _os.path.join(PROC, "country_peers.csv")
    peers_map = {}
    if _os.path.exists(_peers_path):
        _pf = pd.read_csv(_peers_path)
        for _, _r in _pf.iterrows():
            _pl = str(_r["peers"]).split(",") if pd.notna(_r["peers"]) and str(_r["peers"]).strip() else []
            peers_map[_r["iso3"]] = [x for x in _pl if x]

    for iso in fs.index:
        cats = {cat: _n(fs.loc[iso, cat]) for cat in CATEGORIES if cat in fs.columns}
        concepts = {}
        for cid in scored_cids:
            col = "C%d_score" % cid
            if col not in cs.columns:
                continue
            sc = cs.loc[iso, col]
            if _n(sc) is None:
                continue
            m = mom_by.get((iso, cid))
            concepts[cid] = {
                "s": _n(sc),
                "lc": _b(cs.loc[iso, "C%d_lowconf" % cid]) if "C%d_lowconf" % cid in cs.columns else False,
                "mag": None if m is None else _n(m.magnitude, 4),
                "brd": None if m is None else _n(m.breadth, 2),
            }
        countries[iso] = {
            "name": cov.loc[iso, "country_name"] if iso in cov.index else iso,
            "terr": _b(cov.loc[iso, "is_territory"]) if iso in cov.index else False,
            "np": int(cov.loc[iso, "metrics_present"]) if iso in cov.index else 0,
            "mc": metric_counts.get(iso, {"total": 0, "by_cat": {}}),
            "peers": peers_map.get(iso, []),
            "cat": cats,
            "con": concepts,
        }

    # history: round to 3dp; comp_summary sparse (only where present)
    ch = pd.read_csv(os.path.join(PROC, "score_history.csv"))
    cath = pd.read_csv(os.path.join(PROC, "category_history.csv"))
    history = {}
    for iso, g in ch.groupby("iso3"):
        cbyc = {}
        for cid, gg in g.groupby("concept_id"):
            pts = []
            for r in gg.sort_values("year").itertuples():
                p = {"y": int(r.year), "s": _n(r.score)}
                if _b(r.low_confidence):
                    p["lc"] = 1
                if _b(r.concept_start):
                    p["st"] = 1
                if _b(r.comp_changed):
                    p["cc"] = 1
                    if isinstance(r.comp_summary, str) and r.comp_summary:
                        p["cs"] = r.comp_summary
                pts.append(p)
            cbyc[int(cid)] = pts
        history.setdefault(iso, {})["c"] = cbyc
    for iso, g in cath.groupby("iso3"):
        cbc = {}
        for cat, gg in g.groupby("category"):
            cbc[cat] = [{"y": int(r.year), "s": _n(r.category_score)}
                        for r in gg.sort_values("year").itertuples()]
        history.setdefault(iso, {})["cat"] = cbc

    # metric label lookup ONCE (dedup the 5.3MB of repeated strings)
    metrics_meta = {}
    con = pd.read_csv(os.path.join(PROC, "concept_contributions.csv"))
    con = con[con["present"] == True] if "present" in con.columns else con
    for m in con.metric.unique():
        d = METRIC_DICT.get(m, {})
        metrics_meta[m] = {"def": d.get("definition", ""), "src": d.get("source_reports", "")}

    contributions = {}
    for iso, g in con.groupby("iso3"):
        by_c = {}
        for cid, gg in g.groupby("concept_id"):
            rows = []
            for r in gg.sort_values("metric_contribution", ascending=False).itertuples():
                rows.append({
                    "m": r.metric,
                    "t": r.tier,
                    "v": _n(r.harmonized),
                    "w": _n(r.renormalized_weight),
                    "c": _n(r.metric_contribution),
                    "y": int(r.latest_year) if r.latest_year == r.latest_year else None,
                    "st": 1 if _b(r.stale) else 0,
                    "b": (r.bucket if isinstance(r.bucket, str) else None),
                })
            by_c[int(cid)] = rows
        contributions[iso] = by_c

    # percentile bands (p25/p50/p75) for the radar, over SOVEREIGNS ONLY (exclude territories)
    sov = cov[~cov["is_territory"].astype(bool)].index
    pct = {"categories": {}, "concepts": {}}
    for cat in CATEGORIES:
        if cat in fs.columns:
            v = fs.loc[fs.index.isin(sov), cat].dropna()
            if len(v):
                pct["categories"][cat] = {"p25": _n(v.quantile(.25)), "p50": _n(v.quantile(.50)), "p75": _n(v.quantile(.75))}
    for cid in scored_cids:
        col = "C%d_score" % cid
        if col in cs.columns:
            v = cs.loc[cs.index.isin(sov), col].dropna()
            if len(v):
                pct["concepts"][cid] = {"p25": _n(v.quantile(.25)), "p50": _n(v.quantile(.50)), "p75": _n(v.quantile(.75))}

    meta = {
        "concepts": {cid: {"name": concept_name.get(cid, "C%d" % cid),
                           "cat": concept_cat.get(cid, "")} for cid in scored_cids},
        "categories": CATEGORIES,
        "percentiles": pct,
        "metrics": metrics_meta,
        "generated": pd.Timestamp.today().strftime("%Y-%m-%d"),
        "n_countries": len(countries),
        "history_years": [int(ch.year.min()), int(ch.year.max())],
    }

    data = {"meta": meta, "countries": countries, "history": history, "contributions": contributions}
    os.makedirs(OUT_DIR, exist_ok=True)
    out = os.path.join(OUT_DIR, "dashboard_data.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, separators=(",", ":"))
    mb = os.path.getsize(out) / 1e6
    print("wrote %s  (%.1f MB)" % (out, mb))
    for k in data:
        print("  %-14s %.1f MB" % (k, len(json.dumps(data[k], separators=(",", ":"))) / 1e6))
    return data


if __name__ == "__main__":
    build()
