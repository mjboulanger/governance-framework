"""
Score validation suite (Step 4 — Validation, methodology §0).

Re-runnable checks over the committed score outputs. Component #1 (face-validity)
is implemented; the structure holds #2-#7 (directionality, coverage, single-metric
domination, sensitivity sweeps, parameter revisits) added as further check_* funcs.

Cadence tags (why each check exists, when to re-run):
  [every-update]  regression guard; run after every score regeneration
  [periodic]      run on major panel extensions
  [archival]      one-time finding; kept for reference

#1 face-validity is [every-update]: anchor priors, inversion scan, cross-category
coherence. Report-only (no asserts yet) on this first build; stable invariants get
promoted to asserts once the baseline is reviewed and known-clean.

Emits:
  data/processed/validation_report.csv  - long, machine-readable findings (diff across runs)
  docs/validation_report.md             - human-readable report (regenerated each run)

Run: python src/validate_scores.py
"""
import os
import sys
import datetime
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from config import PROCESSED_DIR
from concept_sources import CONCEPTS
from country_harmonization import add_iso3

PROC = PROCESSED_DIR
DOCS = os.path.join(os.path.dirname(__file__), "..", "docs")

# --- pre-committed face-validity priors (fixed BEFORE looking at results) ---
# High-governance anchors: expected top of most categories. SGP is a DISCRIMINATOR,
# not a monotone-high anchor - expected high on State capacity / Rule of law but
# LOWER on Accountability. A framework that ranks SGP uniformly high fails to
# discriminate governance dimensions, which is itself the finding.
ANCHORS_HIGH = ["DNK", "NZL", "NOR", "CHE", "SGP"]
ANCHORS_LOW = ["SOM", "YEM", "SSD", "SYR", "VEN"]
# Out of scope by design (D2 spine rule, EXCLUDE_CLOSED) - NOT scored, not anchors.
EXCLUDED_BY_DESIGN = ["PRK", "ERI", "TKM"]
ANCHOR_PASS_PCTILE = 0.25          # high anchors expected >= 0.75; low anchors <= 0.25
COHERENCE_REDUNDANT = 0.95         # pairwise category r above this -> categories redundant
COHERENCE_INCOHERENT = 0.30        # below this -> categories not measuring related things
TOPN = 10                          # inversion-scan list length


def _load():
    fs = pd.read_csv(os.path.join(PROC, "final_scores.csv"))
    spine = pd.read_csv(os.path.join(PROC, "country_spine.csv"))[["iso3", "country_name", "is_territory"]]
    fs = fs.merge(spine, on="iso3", how="left")
    cats = [c for c in fs.columns if c not in ("iso3", "country_name", "is_territory")]
    cs = pd.read_csv(os.path.join(PROC, "concept_scores.csv"))
    concept_name = {cid: CONCEPTS[cid]["name"] for cid in CONCEPTS}
    return fs, cats, cs, concept_name, spine


def _pctile_rank(series, iso):
    """Percentile rank of iso within the non-null series (fraction of countries
    scoring at or below it). Returns (pctile, value, rank, n) or None if unscored."""
    s = series.dropna()
    if iso not in s.index:
        return None
    v = s.loc[iso]
    n = len(s)
    below_or_equal = (s <= v).sum()
    return (below_or_equal / n, float(v), int((s > v).sum()) + 1, n)


def check_anchors(fs, cats, findings):
    """[every-update] Each anchor's percentile rank within SOVEREIGNS per category.
    High anchors expected in top 25%, low anchors in bottom 25%. Report-only."""
    sov = fs[fs["is_territory"] == False].set_index("iso3")
    for cat in cats:
        s = sov[cat]
        for iso in ANCHORS_HIGH:
            r = _pctile_rank(s, iso)
            if r is None:
                findings.append(dict(check="anchor_high", category=cat, subject=iso,
                                     measure="percentile", value=np.nan, threshold=">=0.75",
                                     status="ABSENT", detail="not scored in this category"))
                continue
            pct, val, rank, n = r
            status = "PASS" if pct >= (1 - ANCHOR_PASS_PCTILE) else "REVIEW"
            findings.append(dict(check="anchor_high", category=cat, subject=iso,
                                 measure="percentile", value=round(pct, 4), threshold=">=0.75",
                                 status=status, detail="score=%.4f rank=%d/%d" % (val, rank, n)))
        for iso in ANCHORS_LOW:
            r = _pctile_rank(s, iso)
            if r is None:
                findings.append(dict(check="anchor_low", category=cat, subject=iso,
                                     measure="percentile", value=np.nan, threshold="<=0.25",
                                     status="ABSENT", detail="not scored in this category"))
                continue
            pct, val, rank, n = r
            status = "PASS" if pct <= ANCHOR_PASS_PCTILE else "REVIEW"
            findings.append(dict(check="anchor_low", category=cat, subject=iso,
                                 measure="percentile", value=round(pct, 4), threshold="<=0.25",
                                 status=status, detail="score=%.4f rank=%d/%d" % (val, rank, n)))


def check_singapore_discrimination(fs, cats, findings):
    """[every-update] SGP should rank high on State capacity / Rule of law but
    LOWER on Accountability - tests dimensional discrimination, not monotone height."""
    sov = fs[fs["is_territory"] == False].set_index("iso3")
    ranks = {}
    for cat in cats:
        r = _pctile_rank(sov[cat], "SGP")
        ranks[cat] = r[0] if r else np.nan
    cap = ranks.get("State capacity", np.nan)
    rol = ranks.get("Rule of law", np.nan)
    acc = ranks.get("Accountability", np.nan)
    # discrimination present if capacity/rule-of-law materially exceed accountability
    gap = np.nanmin([cap, rol]) - acc
    status = "PASS" if gap > 0.15 else "REVIEW"
    findings.append(dict(check="discrimination", category="SGP capacity/rule-of-law vs accountability",
                         subject="SGP", measure="pctile_gap", value=round(gap, 4), threshold=">0.15",
                         status=status,
                         detail="capacity=%.2f rule-of-law=%.2f accountability=%.2f" % (cap, rol, acc)))


def check_inversions(fs, cats, cs, concept_name, findings):
    """[every-update] Top-N / bottom-N per category and concept, for eyeball review.
    Not auto-scored against priors; surfaces unpredicted placements (captured/failed
    state in a top list, clean state in a bottom list, territory artifacts)."""
    sov = fs[fs["is_territory"] == False]
    for cat in cats:
        s = sov[["iso3", "country_name", cat]].dropna(subset=[cat]).sort_values(cat, ascending=False)
        top = s.head(TOPN)["iso3"].tolist()
        bot = s.tail(TOPN)["iso3"].tolist()
        findings.append(dict(check="inversion_scan", category=cat, subject="TOP%d" % TOPN,
                             measure="ranking", value=np.nan, threshold="eyeball",
                             status="INFO", detail=", ".join(top)))
        findings.append(dict(check="inversion_scan", category=cat, subject="BOTTOM%d" % TOPN,
                             measure="ranking", value=np.nan, threshold="eyeball",
                             status="INFO", detail=", ".join(reversed(bot))))
    # concept-level top/bottom (sovereigns only), names for readability
    sov_iso = set(sov["iso3"])
    for col in [c for c in cs.columns if c.endswith("_score")]:
        cid = int(col[1:-6])
        d = cs[cs["iso3"].isin(sov_iso)][["iso3", col]].dropna(subset=[col]).sort_values(col, ascending=False)
        if len(d) < TOPN * 2:
            continue
        top = d.head(TOPN)["iso3"].tolist()
        bot = d.tail(TOPN)["iso3"].tolist()
        nm = concept_name.get(cid, "C%d" % cid)
        findings.append(dict(check="inversion_scan_concept", category="C%d %s" % (cid, nm),
                             subject="TOP%d" % TOPN, measure="ranking", value=np.nan,
                             threshold="eyeball", status="INFO", detail=", ".join(top)))
        findings.append(dict(check="inversion_scan_concept", category="C%d %s" % (cid, nm),
                             subject="BOTTOM%d" % TOPN, measure="ranking", value=np.nan,
                             threshold="eyeball", status="INFO", detail=", ".join(reversed(bot))))


def check_coherence(fs, cats, findings):
    """[every-update] Pairwise Pearson r across the 5 category scores (sovereigns).
    Expected moderate-high positive (0.3-0.95): correlated (governance clusters) but
    not identical (categories measure distinct facets)."""
    sov = fs[fs["is_territory"] == False]
    corr = sov[cats].corr(method="pearson")
    for i, a in enumerate(cats):
        for b in cats[i + 1:]:
            r = corr.loc[a, b]
            if r > COHERENCE_REDUNDANT:
                status = "REVIEW"
            elif r < COHERENCE_INCOHERENT:
                status = "REVIEW"
            else:
                status = "PASS"
            findings.append(dict(check="coherence", category="%s | %s" % (a, b), subject="pearson_r",
                                 measure="correlation", value=round(float(r), 4),
                                 threshold="0.30-0.95", status=status, detail=""))
    return corr

# --- #2 Directionality (three layers, all 144 metrics) [every-update] ---

DIR_ANCHOR_HIGH = ["DNK", "NZL", "NOR", "CHE"]      # SGP excluded: discriminator, not monotone-high
DIR_ANCHOR_LOW = ["SOM", "YEM", "SSD", "SYR", "VEN"]
WGI_METRICS = ["wgi_political_stability", "wgi_government_effectiveness", "wgi_regulatory_quality",
               "wgi_control_of_corruption", "wgi_rule_of_law", "wgi_voice_accountability"]
ANCHOR_GAP = 0.25


def _latest_slice(panel):
    return panel.sort_values("year").groupby(["iso3", "metric"]).tail(1)


def check_monotonicity(panel, findings):
    """[every-update] Layer 1: was the direction FLIP applied correctly by the CODE?
    harmonized is already direction-aligned (higher=better). raw vs harmonized:
    '+' metric -> POSITIVE spearman; '-' metric -> NEGATIVE (flipped). A sign
    disagreeing with the direction tag = flip mis-applied. Tests code-applied-the-tag;
    Layer 2 tests the-tag-is-right - kept independent so neither masks the other."""
    ls = _latest_slice(panel)
    for metric, g in ls.groupby("metric"):
        d = g[["raw_value", "harmonized"]].dropna()
        direction = g["direction"].dropna().iloc[0] if g["direction"].notna().any() else None
        if len(d) < 5 or d["raw_value"].nunique() < 2 or direction is None:
            findings.append(dict(check="dir_monotonicity", category=str(direction), subject=metric,
                                 measure="spearman", value=np.nan, threshold="sign matches direction",
                                 status="SKIP", detail="n<5 or constant raw or no direction"))
            continue
        rho = d["raw_value"].rank().corr(d["harmonized"].rank())  # spearman = pearson on ranks (no scipy)
        expected_positive = (direction == "+")
        ok = (rho > 0) if expected_positive else (rho < 0)
        status = "PASS" if (ok and abs(rho) > 0.1) else "REVIEW"
        findings.append(dict(check="dir_monotonicity", category=direction, subject=metric,
                             measure="spearman", value=round(float(rho), 4),
                             threshold=("+" if expected_positive else "-") + " expected",
                             status=status, detail="n=%d" % len(d)))


def check_anchor_semantic(panel, findings):
    """[every-update] Layer 2: is the direction TAG itself right? Mean harmonized
    percentile of high-anchors vs low-anchors per metric. aligned_correct (high well
    above low) confirms; aligned_WRONG (low above high) = likely sign error;
    inconclusive = metric orthogonal to overall governance (anchors don't separate) =
    INFORMATION, not failure."""
    ls = _latest_slice(panel)
    for metric, g in ls.groupby("metric"):
        h = g.set_index("iso3")["harmonized"].dropna()
        if len(h) < 10:
            continue
        pct = h.rank(pct=True)
        hi = [pct[i] for i in DIR_ANCHOR_HIGH if i in pct.index]
        lo = [pct[i] for i in DIR_ANCHOR_LOW if i in pct.index]
        if len(hi) < 2 or len(lo) < 2:
            findings.append(dict(check="dir_anchor", category="", subject=metric, measure="hi_minus_lo",
                                 value=np.nan, threshold="|gap|>0.25", status="SKIP",
                                 detail="anchors sparse (hi=%d lo=%d)" % (len(hi), len(lo))))
            continue
        gap = float(np.mean(hi) - np.mean(lo))
        if gap > ANCHOR_GAP:
            status, cls = "PASS", "aligned_correct"
        elif gap < -ANCHOR_GAP:
            status, cls = "REVIEW", "aligned_WRONG (likely sign error)"
        else:
            status, cls = "INFO", "inconclusive_orthogonal"
        findings.append(dict(check="dir_anchor", category=cls, subject=metric, measure="hi_minus_lo",
                             value=round(gap, 4), threshold="|gap|>0.25", status=status,
                             detail="hi_mean=%.2f lo_mean=%.2f (hi=%d lo=%d)" % (
                                 np.mean(hi), np.mean(lo), len(hi), len(lo))))


def check_reference_correlation(panel, sel, findings):
    """[every-update] Layer 3: does each metric track independent governance/income
    signal, right sign? Spearman of harmonized vs WGI-broad (mean of 6 WGI pillars; a
    WGI metric excluded from its OWN test) and vs GDP/capita USD (external). NB Spearman
    is rank-based, so PPP vs non-PPP GDP is near-irrelevant here. Both refs lean
    capacity/income, so weak/neg corr on accountability metrics can be EXPECTED - read
    by concept, not pass/fail. Only clearly-negative (< -0.1) is flagged."""
    ls = _latest_slice(panel)
    wg = ls[ls.metric.isin(WGI_METRICS)].pivot_table(index="iso3", columns="metric", values="harmonized")
    wgi_broad = wg.mean(axis=1)
    wdi = pd.read_csv(os.path.join(PROC, "wdi_clean.csv"), low_memory=False)
    wdi = add_iso3(wdi, filename_hint="wdi_clean.csv")
    gdp = (wdi[wdi.iso3.notna() & wdi.wdi_gdp_per_capita_usd.notna()]
           .sort_values("year").groupby("iso3").tail(1).set_index("iso3")["wdi_gdp_per_capita_usd"])
    cat_of = sel.dropna(subset=["concept_id"]).drop_duplicates("metric").set_index("metric")["concept_id"]
    for metric, g in ls.groupby("metric"):
        h = g.set_index("iso3")["harmonized"].dropna()
        if len(h) < 20:
            continue
        if metric in WGI_METRICS:
            others = [m for m in WGI_METRICS if m != metric]
            ref = ls[ls.metric.isin(others)].pivot_table(index="iso3", columns="metric", values="harmonized").mean(axis=1)
        else:
            ref = wgi_broad
        j = pd.concat([h, ref], axis=1, join="inner").dropna()
        r_wgi = j.iloc[:, 0].rank().corr(j.iloc[:, 1].rank()) if len(j) >= 20 else np.nan  # spearman via ranks
        jg = pd.concat([h, gdp], axis=1, join="inner").dropna()
        r_gdp = jg.iloc[:, 0].rank().corr(jg.iloc[:, 1].rank()) if len(jg) >= 20 else np.nan  # spearman via ranks
        neg = (pd.notna(r_wgi) and r_wgi < -0.1) or (pd.notna(r_gdp) and r_gdp < -0.1)
        findings.append(dict(check="dir_correlation", category=str(cat_of.get(metric, "")),
                             subject=metric, measure="spearman_wgi/gdp",
                             value=round(float(r_wgi), 3) if pd.notna(r_wgi) else np.nan,
                             threshold=">=-0.1 (neg=flag)", status="REVIEW" if neg else "PASS",
                             detail="r_wgi=%s r_gdp=%s n=%d" % (
                                 ("%.3f" % r_wgi) if pd.notna(r_wgi) else "na",
                                 ("%.3f" % r_gdp) if pd.notna(r_gdp) else "na", len(h))))

def _md_table(df, cols):
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def write_report(findings, corr, cats, spine):
    fdf = pd.DataFrame(findings)
    fdf.to_csv(os.path.join(PROC, "validation_report.csv"), index=False)

    ts = datetime.date.today().isoformat()
    n_review = int((fdf["status"] == "REVIEW").sum())
    n_absent = int((fdf["status"] == "ABSENT").sum())
    out = []
    out.append("# Score Validation Report")
    out.append("")
    out.append("**Generated:** %s (regenerated by `src/validate_scores.py`; do not edit by hand)" % ts)
    out.append("**Component:** #1 Face-validity [every-update cadence]. #2-#7 pending.")
    out.append("**Summary:** %d findings flagged REVIEW, %d anchor-cells ABSENT." % (n_review, n_absent))
    out.append("")
    out.append("## Scope note")
    out.append("")
    out.append("The framework scores **213 economies** = all with WDI population data, minus "
               "exactly **{PRK, ERI, TKM}** (North Korea, Eritrea, Turkmenistan), excluded by the "
               "D2 spine rule as closed regimes that cannot be meaningfully measured. Non-sovereign "
               "territories are included and flagged (`is_territory`); the checks below rank within "
               "**sovereigns only** (n=%d). Consequence: the bottom of every ranking is the lowest "
               "*in-scope* state, not the lowest on earth - three of the most-closed regimes are not "
               "scored at all. Read low ranks accordingly." % int((spine["is_territory"] == False).sum()))
    out.append("")
    out.append("## Anchor priors (pre-committed)")
    out.append("")
    out.append("High-governance anchors expected in the top 25%% of each category; low-governance "
               "anchors in the bottom 25%%. REVIEW = outside the expected band (not necessarily wrong, "
               "but worth a look). Singapore is a *discriminator*: expected high on capacity/rule-of-law, "
               "lower on accountability.")
    out.append("")
    anc = fdf[fdf["check"].isin(["anchor_high", "anchor_low"])][
        ["check", "category", "subject", "value", "status", "detail"]]
    out.append(_md_table(anc, ["check", "category", "subject", "value", "status", "detail"]))
    out.append("")
    disc = fdf[fdf["check"] == "discrimination"]
    if len(disc):
        d = disc.iloc[0]
        out.append("**Singapore discrimination:** %s (%s) - %s" % (d["status"], d["detail"], d["value"]))
        out.append("")
    out.append("## Cross-category coherence")
    out.append("")
    out.append("Pairwise Pearson r across the 5 category scores (sovereigns). Expected 0.30-0.95: "
               "correlated but not identical. Above 0.95 = redundant; below 0.30 = incoherent.")
    out.append("")
    out.append("```")
    out.append(corr.round(3).to_string())
    out.append("```")
    out.append("")
    out.append("## Inversion scan (eyeball review)")
    out.append("")
    out.append("Top/bottom %d per category and concept (sovereigns). No auto-pass; scan for "
               "captured/failed states appearing high, clean states appearing low, or thin-coverage "
               "artifacts." % TOPN)
    out.append("")
    inv = fdf[fdf["check"] == "inversion_scan"][["category", "subject", "detail"]]
    out.append(_md_table(inv, ["category", "subject", "detail"]))
    out.append("")
    out.append("### Concept-level top/bottom")
    out.append("")
    invc = fdf[fdf["check"] == "inversion_scan_concept"][["category", "subject", "detail"]]
    out.append(_md_table(invc, ["category", "subject", "detail"]))
    out.append("")

    with open(os.path.join(DOCS, "validation_report.md"), "w", encoding="utf-8", newline="") as fh:
        fh.write("\n".join(out) + "\n")
    return fdf


def build():
    fs, cats, cs, concept_name, spine = _load()
    panel = pd.read_csv(os.path.join(PROC, "normalized_panel.csv"))
    sel = pd.read_csv(os.path.join(PROC, "metric_selection.csv"))
    findings = []
    check_anchors(fs, cats, findings)
    check_singapore_discrimination(fs, cats, findings)
    check_inversions(fs, cats, cs, concept_name, findings)
    corr = check_coherence(fs, cats, findings)
    check_monotonicity(panel, findings)
    check_anchor_semantic(panel, findings)
    check_reference_correlation(panel, sel, findings)
    fdf = write_report(findings, corr, cats, spine)
    return fdf, corr


if __name__ == "__main__":
    fdf, corr = build()
    print("validation_report.csv:", fdf.shape)
    print("validation_report.md written")
    print()
    print("REVIEW findings (%d):" % int((fdf.status == "REVIEW").sum()))
    for _, r in fdf[fdf.status == "REVIEW"].iterrows():
        print("  [%s] %s / %s = %s (%s)" % (r["check"], r["category"], r["subject"], r["value"], r["detail"]))
    print()
    print("ABSENT anchor-cells (%d):" % int((fdf.status == "ABSENT").sum()))
    for _, r in fdf[fdf.status == "ABSENT"].iterrows():
        print("  %s / %s: %s" % (r["category"], r["subject"], r["detail"]))