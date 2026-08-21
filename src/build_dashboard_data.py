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
    # concept effective_weights (canonical, from the scoring pipeline) for concept->category contribution
    _ca = pd.read_csv(os.path.join(PROC, "concept_attribution.csv"))
    concept_eff_weight = {(r.iso3, int(r.concept_id)): r.effective_weight for r in _ca.itertuples()}
    # concept weight SHARE of its category (canonical): eff_weight / sum(eff_weight) within (iso, category).
    _catsum = _ca.groupby(["iso3", "category"])["effective_weight"].sum().to_dict()
    concept_weight_share = {}
    for r in _ca.itertuples():
        _tot = _catsum.get((r.iso3, r.category))
        concept_weight_share[(r.iso3, int(r.concept_id))] = (r.effective_weight / _tot) if _tot else None
    # map concept_id -> category (for the metric->category chain)
    concept_to_cat = {int(r.concept_id): r.category for r in _ca.itertuples()}
    cov = pd.read_csv(os.path.join(PROC, "country_coverage.csv")).set_index("iso3")
    sov = cov[~cov["is_territory"].astype(bool)].index  # sovereigns (hoisted: used by concept medians + percentiles)
    spine = pd.read_csv(os.path.join(PROC, "country_spine.csv")).set_index("iso3")
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


    # concept medians across sovereigns (same basis as the concept position bars), computed once

    concept_median = {}
    concept_ref_mean = {}

    for _cid in scored_cids:

        _col = 'C%d_score' % _cid

        if _col in cs.columns:

            _vv = cs.loc[cs.index.isin(sov), _col].dropna()
            if len(_vv):
                concept_median[_cid] = float(_vv.quantile(.50))
                concept_ref_mean[_cid] = float(_vv.mean())


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
            # concept->category signed contribution: canonical effective_weight x deviation from
            # the concept's sovereign median. effective_weight is a pipeline output (concept_attribution.csv);
            # nothing weight-related is defined here.
            _ew = concept_eff_weight.get((iso, cid))
            _cmed = concept_median.get(cid)
            _cshare = concept_weight_share.get((iso, cid))
            _crefm = concept_ref_mean.get(cid)
            _cc = _n(_cshare * (sc - _crefm)) if (_cshare is not None and _crefm is not None and sc == sc) else None
            concepts[cid] = {
                "s": _n(sc),
                "lc": _b(cs.loc[iso, "C%d_lowconf" % cid]) if "C%d_lowconf" % cid in cs.columns else False,
                "mag": None if m is None else _n(m.magnitude, 4),
                "brd": None if m is None else _n(m.breadth, 2),
                "cc": _cc,
                "ws": _n(_cshare, 4),
            }
        countries[iso] = {
            "name": cov.loc[iso, "country_name"] if iso in cov.index else iso,
            "terr": _b(cov.loc[iso, "is_territory"]) if iso in cov.index else False,
            "np": int(cov.loc[iso, "metrics_present"]) if iso in cov.index else 0,
            "mc": metric_counts.get(iso, {"total": 0, "by_cat": {}}),
            "peers": peers_map.get(iso, []),
            "pop": (int(spine.loc[iso, "population"]) if (iso in spine.index and pd.notna(spine.loc[iso, "population"])) else None),
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

    # readable metric labels (canonical reference): metric -> {name, source_label, label="Name (Source)"}
    _refdir = os.path.join(os.path.dirname(PROC), "reference")
    _lab = pd.read_csv(os.path.join(_refdir, "metric_labels.csv"))
    metric_labels = {}
    for _r in _lab.to_dict("records"):
        _nm = str(_r.get("metric_name", "") or "").strip()
        _sl = str(_r.get("source_label", "") or "").strip()
        _full = (_nm + " (" + _sl + ")") if (_nm and _sl) else (_nm or str(_r["metric"]))
        metric_labels[_r["metric"]] = {"name": _nm, "source_label": _sl, "label": _full}

    # metric normalization params (per-metric static: method + baseline params + harmonize rule),
    # from metric_normalization_params.csv. These let the dashboard reconstruct raw -> harmonized.
    # Stored ONCE per metric in meta.metrics (not per country). The per-(country,metric) RAW value
    # is read separately below and attached to each contribution row.
    _params = {}
    _pp_path = os.path.join(PROC, "metric_normalization_params.csv")
    if os.path.exists(_pp_path):
        _pdf = pd.read_csv(_pp_path)
        for _r in _pdf.itertuples():
            _params[_r.metric] = {
                "meth": (_r.final_method if isinstance(_r.final_method, str) else None),
                "pre": (_r.pre_transform if isinstance(_r.pre_transform, str) else None),
                "bmean": _n(_r.baseline_mean, 4) if _r.baseline_mean == _r.baseline_mean else None,
                "bsd": _n(_r.baseline_sd, 4) if _r.baseline_sd == _r.baseline_sd else None,
                "nobs": int(_r.baseline_n_obs) if _r.baseline_n_obs == _r.baseline_n_obs else None,
                "winsor": _n(_r.winsor, 2) if _r.winsor == _r.winsor else None,
                "hrule": (_r.harmonize_rule if isinstance(_r.harmonize_rule, str) else None),
                "dir": (_r.direction if isinstance(_r.direction, str) else None),
            }
    # RAW values per (iso, metric) at the latest available year, from the normalized panel.
    # The panel is large (~56MB, all years); read only needed columns and keep the latest year
    # per (iso, metric). This is a build-time read of a regenerable artifact.
    _raw_by = {}
    _np_path = os.path.join(PROC, "normalized_panel.csv")
    if os.path.exists(_np_path):
        _np = pd.read_csv(_np_path, usecols=["iso3", "year", "metric", "raw_value"])
        _np = _np.dropna(subset=["raw_value"])
        # latest year per (iso, metric)
        _np = _np.sort_values("year").drop_duplicates(["iso3", "metric"], keep="last")
        for _r in _np.itertuples():
            _raw_by[(_r.iso3, _r.metric)] = _r.raw_value

    # metric label lookup ONCE (dedup the 5.3MB of repeated strings)
    metrics_meta = {}
    con = pd.read_csv(os.path.join(PROC, "concept_contributions.csv"))
    con = con[con["present"] == True] if "present" in con.columns else con
    for m in con.metric.unique():
        d = METRIC_DICT.get(m, {})
        _lb = metric_labels.get(m, {})
        _pm = _params.get(m, {})
        metrics_meta[m] = {"def": d.get("definition", ""), "src": d.get("source_reports", ""),
                           "name": _lb.get("name", ""), "label": _lb.get("label", m),
                           "meth": _pm.get("meth"), "pre": _pm.get("pre"),
                           "bmean": _pm.get("bmean"), "bsd": _pm.get("bsd"),
                           "nobs": _pm.get("nobs"), "winsor": _pm.get("winsor"),
                           "hrule": _pm.get("hrule"), "dir": _pm.get("dir")}

    # per-metric world percentiles (p25/p50/p75 of the harmonized value across sovereigns),
    # for the drill-down value-vs-universe bars. Dedup (metric, iso3) since a metric can appear
    # under multiple concepts with the same harmonized value.
    _cc = pd.read_csv(os.path.join(PROC, "concept_contributions.csv"))
    _cc = _cc[_cc["present"] == True] if "present" in _cc.columns else _cc
    _cc = _cc[_cc["iso3"].isin(sov)]
    _mv = _cc[["metric", "iso3", "harmonized"]].dropna(subset=["harmonized"]).drop_duplicates(["metric", "iso3"])
    metric_pct = {}
    metric_ref_mean = {}
    for _m, _g in _mv.groupby("metric"):
        _v = _g["harmonized"]
        if len(_v):
            metric_pct[_m] = {"p05": _n(_v.quantile(.05)), "p25": _n(_v.quantile(.25)), "p50": _n(_v.quantile(.50)), "p75": _n(_v.quantile(.75)), "p95": _n(_v.quantile(.95))}
            metric_ref_mean[_m] = float(_v.mean())

    contributions = {}
    for iso, g in con.groupby("iso3"):
        by_c = {}
        for cid, gg in g.groupby("concept_id"):
            rows = []
            for r in gg.sort_values("metric_contribution", ascending=False).itertuples():
                # signed contribution: canonical weight x deviation from the metric's world median.
                # weight (renormalized_weight) and value (harmonized) are canonical pipeline outputs;
                # median comes from metric_pct (computed once above). Not recomputed anywhere else.
                _rm = metric_ref_mean.get(r.metric)
                _sc = None
                if _rm is not None and r.harmonized == r.harmonized and r.renormalized_weight == r.renormalized_weight:
                    _sc = _n(r.renormalized_weight * (r.harmonized - _rm))
                # metric -> category contribution: sc x concept's weight share of the category (canonical).
                _share = concept_weight_share.get((iso, int(cid)))
                _scat = _n(_sc * _share) if (_sc is not None and _share is not None) else None
                rows.append({
                    "m": r.metric,
                    "t": r.tier,
                    "v": _n(r.harmonized),
                    "w": _n(r.renormalized_weight),
                    "c": _n(r.metric_contribution),
                    "sc": _sc,
                    "scat": _scat,
                    "y": int(r.latest_year) if r.latest_year == r.latest_year else None,
                    "st": 1 if _b(r.stale) else 0,
                    "b": (r.bucket if isinstance(r.bucket, str) else None),
                    "raw": _n(_raw_by.get((iso, r.metric)), 4),
                })
            by_c[int(cid)] = rows
        contributions[iso] = by_c

    # percentile bands (p25/p50/p75) for the radar, over SOVEREIGNS ONLY (exclude territories)
    pct = {"categories": {}, "concepts": {}}
    for cat in CATEGORIES:
        if cat in fs.columns:
            v = fs.loc[fs.index.isin(sov), cat].dropna()
            if len(v):
                pct["categories"][cat] = {"p05": _n(v.quantile(.05)), "p25": _n(v.quantile(.25)), "p50": _n(v.quantile(.50)), "p75": _n(v.quantile(.75)), "p95": _n(v.quantile(.95))}
    for cid in scored_cids:
        col = "C%d_score" % cid
        if col in cs.columns:
            v = cs.loc[cs.index.isin(sov), col].dropna()
            if len(v):
                pct["concepts"][cid] = {"p05": _n(v.quantile(.05)), "p25": _n(v.quantile(.25)), "p50": _n(v.quantile(.50)), "p75": _n(v.quantile(.75)), "p95": _n(v.quantile(.95))}


    meta = {
        "concepts": {cid: {"name": concept_name.get(cid, "C%d" % cid),
                           "cat": concept_cat.get(cid, "")} for cid in scored_cids},
        "categories": CATEGORIES,
        "percentiles": pct,
        "metric_percentiles": metric_pct,
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
