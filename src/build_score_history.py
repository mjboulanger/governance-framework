"""
Historical score panel: score every year on the fixed (current) baseline, so each
country's concept/category trajectory shows ABSOLUTE movement on one comparable scale.

Reuses the SAME scoring functions as the live build (no parallel path, no drift):
  score_slice()      from build_concept_scores  -> concept scores for an as-of year
  score_categories() from build_final_scores     -> category roll-up for that year

Design decisions (2026-08-12):
  D1 Fixed baseline: panel `harmonized` is pre-normalized on the current baseline, so
     reading year-Y values gives fixed-baseline scores for free (no re-normalization).
  D2 Available metrics per year: each year scored on whatever metrics have data at/before
     it; thin early years carry the per-year low_confidence flag (n_present-driven).
  D3 History floor = 2005 (coverage adequate: ~98 of 137 metrics). Concepts/categories
     start when their data starts; C3 (Statistical infrastructure) and C9 (Financial-
     sector regulation) go dark before ~2013-2015 (their sources start then).
  Composition-change flag (Part 2): per (iso3, concept, year), whether the present-metric
     set changed vs the prior year, with a human-readable summary naming the metric(s)
     and their within-concept weight share.

Note: FRAMEWORK_START_YEAR (1990) is the raw-data floor; HISTORY_START (2005) is the
scoring floor - distinct concepts. Per-year floors in score_categories reflect each
year's own scored-country distribution (self-consistent, not fixed).

Outputs:
  data/processed/score_history.csv    - iso3 x concept_id x year: score + flags
  data/processed/category_history.csv - iso3 x category x year: category_score
"""
import os
import sys
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from config import PROCESSED_DIR, CURRENT_YEAR, write_csv
from build_concept_scores import score_slice
from build_final_scores import score_categories
from concept_sources import to_rows

PROC = PROCESSED_DIR
HISTORY_START = 2005


def _wide(cs_long):
    """long concept scores (iso3,concept_id,score,low_confidence) -> wide C{n}_score/C{n}_lowconf,
    exactly as build_concept_scores.build() does before calling score_categories."""
    w = cs_long.pivot(index="iso3", columns="concept_id", values="score")
    w.columns = ["C%d_score" % c for c in w.columns]
    lc = cs_long.pivot(index="iso3", columns="concept_id", values="low_confidence")
    lc.columns = ["C%d_lowconf" % c for c in lc.columns]
    return w.join(lc).reset_index()


def build_history():
    panel = pd.read_csv(os.path.join(PROC, "normalized_panel.csv"))
    sel = pd.read_csv(os.path.join(PROC, "metric_selection.csv"))
    scored = sel[sel["tier"].isin(["P1", "P2", "Sp"])][
        ["metric", "concept_id", "tier"]].dropna(subset=["concept_id"]).copy()
    scored["concept_id"] = scored["concept_id"].astype(int)
    weights = pd.read_csv(os.path.join(PROC, "concept_weights.csv")).set_index("concept_id")
    tags = pd.read_csv(os.path.join(PROC, "metric_missingness_tags.csv")).set_index(
        "metric")["missingness_tag"].to_dict()
    c2cat = pd.DataFrame(to_rows()).drop_duplicates("concept_id").set_index(
        "concept_id")["category"].to_dict()

    concept_rows, category_rows = [], []
    comp_by_year = {}
    for Y in range(HISTORY_START, CURRENT_YEAR + 1):
        cs_long, contribs, _bkt = score_slice(panel, sel, scored, Y)
        wide = _wide(cs_long)
        ca, cats, _w, _c = score_categories(wide, contribs, weights, tags, sel, c2cat)
        # capture present-metric composition per (iso3, concept) for the comp-change flag
        pres = contribs[contribs["present"]]
        for (iso, cid), g in pres.groupby(["iso3", "concept_id"]):
            comp_by_year.setdefault((iso, int(cid)), {})[Y] = {
                r.metric: (r.tier, float(r.renormalized_weight)) for r in g.itertuples()}
        for r in cs_long.itertuples():
            concept_rows.append(dict(iso3=r.iso3, concept_id=int(r.concept_id), year=Y,
                                     score=r.score, low_confidence=bool(r.low_confidence)))
        for r in cats.itertuples():
            category_rows.append(dict(iso3=r.iso3, category=r.category, year=Y,
                                      category_score=r.category_score))
    # composition-change flag: compare each (iso3,concept,year) present-metric set to prior year
    def _fmt(m, tw, w):
        tier = {1.0: "P1", 0.5: "P2", 0.0: "Sp"}.get(tw, tw)
        return "%s (%s, %d%% wt)" % (m, tier, round(100 * w))
    for row in concept_rows:
        key = (row["iso3"], row["concept_id"]); Y = row["year"]
        cur = comp_by_year.get(key, {}).get(Y, {})
        prev = comp_by_year.get(key, {}).get(Y - 1, {})
        if Y == HISTORY_START or not prev:
            row["comp_changed"] = False
            row["comp_summary"] = ""
            continue
        added = [m for m in cur if m not in prev]
        removed = [m for m in prev if m not in cur]
        if not added and not removed:
            row["comp_changed"] = False
            row["comp_summary"] = ""
        else:
            parts = []
            if added:
                parts.append("added " + ", ".join(_fmt(m, cur[m][0], cur[m][1]) for m in added))
            if removed:
                parts.append("removed " + ", ".join(_fmt(m, prev[m][0], prev[m][1]) for m in removed))
            row["comp_changed"] = True
            row["comp_summary"] = "; ".join(parts)
    # concept_start flag: first year each (iso3, concept) has any score.
    # Critical for late/rolling-start concepts (e.g. C9 Financial-sector regulation,
    # scored on FATF only, appears per-country on FATF's rolling evaluation schedule).
    first_year = {}
    for row in concept_rows:
        k = (row["iso3"], row["concept_id"])
        y = row["year"]
        if k not in first_year or y < first_year[k]:
            first_year[k] = y
    for row in concept_rows:
        row["concept_start"] = (row["year"] == first_year[(row["iso3"], row["concept_id"])])
    return pd.DataFrame(concept_rows), pd.DataFrame(category_rows)


def write_history():
    ch, cath = build_history()
    write_csv(ch, os.path.join(PROC, "score_history.csv"))
    write_csv(cath, os.path.join(PROC, "category_history.csv"))
    return ch, cath


if __name__ == "__main__":
    ch, cath = write_history()
    print("score_history:", ch.shape, "| years:", ch.year.min(), "-", ch.year.max(),
          "| concepts:", ch.concept_id.nunique(), "| countries:", ch.iso3.nunique())
    print("category_history:", cath.shape)
    print("low_confidence rate by year (sample):")
    print(ch.groupby("year")["low_confidence"].mean().round(3).to_string())
