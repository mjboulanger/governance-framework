# Metric Methodology

**As-of (last manually updated):** 2026-07-10
**⚠️ MANUAL SNAPSHOT:** maintained by hand; does not auto-update. This is the canonical home for the **metric-pass (scoring) methodology**. Source-level build decisions live in `framework_decisions.md`; framework architecture and per-concept source rosters live in `governance_framework_master.md`.

**Status legend:**
- **[LOCKED]** — ratified; parameters fixed.
- **[SPEC PENDING]** — principle agreed; operational parameters await evidence (the Step-0 harmonization/coverage audit, or the Step-4 sensitivity analysis).
- **[OPEN]** — not yet decided.

Every decision carries a status tag. As `[SPEC PENDING]` items lock, the tag is flipped and parameters filled — this document is the running worksheet for the metric pass, not a retrospective write-up.

---

## 0. The metric pass — structure and sequence

Turns the ~34 processed source files into concept and category scores. Two sub-phases:

- **(A) Metric selection** — for each concept, choose the specific indicators within each chosen source (the "largest task"; codebook-driven). Resolves the localized flags (§11).
- **(B) Scoring / aggregation** — normalize → align directionality → aggregate to concept → aggregate to category, with weighting and reliability handling.

**Sequence:**
1. **Step 0 — Harmonization + coverage audit.** Canonicalize country keys to ISO3, strip aggregates/defunct entities, propose the country spine, measure current-coverage per metric. Produces the evidence base for D4–D7 and the inclusion parameters.
2. **Step 0.5 — Lock D4–D7** against the audit evidence.
3. **Step 1 — Metric selection**, concept-by-concept; resolve localized flags (§11).
4. **Step 3 — Build the scoring pipeline** (nb 40+), panel-first.
5. **Step 4 — Validation** — face-validity, directionality sanity, sensitivity/uncertainty analysis (incl. z-score vs percentile head-to-head), coverage report.

---

## 1. Architecture — two-layer output (D1) [LOCKED]

Two layers from a single **panel-first** pipeline:

- **Scoring layer** — the current-state cross-section: 26 concept scores → 5 category scores. The headline, and the object aggregation/weighting/normalization operate on.
- **Evidentiary layer** — the full time series behind every score, concept-level and underlying-metric-level, for drill-down ("click a concept → see its history, and its metrics' history").

The pipeline **normalizes and aggregates on the full available panel** (every year with data); the scoring layer is the **latest-year slice** (`panel.loc[latest]`). One code path; current scores fall out of the panel. Trajectory is served by momentum (§9), not by the level scores.

A **single framework-level composite** (one number per country) is **optional and explicitly caveated, not the headline** — a single number hides the profile that drives investment decisions (strong property rights + weak political stability ≠ "average"). Primary deliverable = concept + category scores.

## 2. Country spine (D2) [LOCKED — revised 2026-07-10]

**Rule [LOCKED, revised 2026-07-10]:** the spine includes **ALL economies with WDI population data** (`SP.POP.TOTL`), excluding only the closed regimes **PRK, ERI, TKM**. **No population floor.** Non-sovereign territories are included and flagged (`is_territory`) so downstream views can filter to sovereigns. Coverage is always measured against this spine. *Revision log: the original rule (pop > 2M, ratified 2026-07-09) was deliberately revised on Step-0 evidence — the 2M line cut through investable sovereigns (Latvia, Estonia, Guyana, Suriname, Brunei, Iceland), and with reliability flags carrying thin coverage (option A) the floor bought nothing.*

**Thin-coverage countries [LOCKED — option A]:** genuine countries meeting the pop/closed-regime rule are **included even when source coverage is thin**, carrying a low-reliability flag (§8) rather than being silently dropped. We exclude only on the pop/closed-regime rule, not on under-measurement.

**The list [LOCKED]:** `data/processed/country_spine.csv` — **213 economies, 21 territories flagged** (built by nb 39; population vintage 2025; integrity-checked: unique ISO3, valid tokens, no closed regimes, positive population). Regenerate only on a WDI population refresh, a closed-regime-list change, or a resolver extension.

**Harmonization [DONE — `src/country_harmonization.py`]:** all country-key resolution lives in the module's `add_iso3()` (code-first, name-fallback; loud failure on undetectable keys). Contents: code overrides — the **Powell-Thyne COW/GW suspicion was confirmed** (25 divergent codes) and its live-country mappings verified against the file's own names (CDI→CIV, TAZ→TZA, SRI→LKA, CAM→KHM, BFO→BFA, RUM→ROU, BOS→BIH, DRC→COD, DRV→VNM, GFR→DEU, AAB→ATG) plus legacy codes (KOS/ROM/PSG); name overrides (DPI abbreviations incl. FRG/Germany→DEU, PRC→CHN, UAE→ARE); a parenthetical-strip retry (fixes UCDP's “Russia (Soviet Union)” pattern); and explicit drop-lists (defunct states, quasi-states, WDI/OWID/UN aggregates). As of 2026-07-10 every unresolved token across all 34 files is a verified legitimate exclusion — zero live countries lost. Metric-pass notebooks MUST import this module; never resolve country keys ad hoc.

## 3. Directionality (D3) [LOCKED]

All indicators are normalized so **higher = better governance**. Every indicator carries an explicit `direction` and a one-line `direction_evidence` note verified **against the source codebook, not memory**. A **sign-sanity validation pass** (Step 4) checks, pre-aggregation, that known-good countries score high on each indicator. Rationale for extra care: a sign error is silent — plausible all the way to the output — so it gets its own checkpoint, not just a column.

## 4. Metric inclusion / usability [LOCKED — 2026-07-10]

**Principle [LOCKED]:** a metric's inclusion is judged by **current cross-sectional coverage on the spine** — the share of spine countries with a *recent-enough latest value* — **judged against the source's own cadence**. **History depth is a separate, non-gating attribute:** a metric with broad recent coverage but no long panel is fully includable; a metric with a long panel but stale/thin recent coverage may fail.

This **rejects panel-fill rate** (non-null cells ÷ all country-years) as the inclusion test: a per-election or snapshot source shows low panel-fill for structural reasons that say nothing about current usability.

**Cadence-relative recency [LOCKED principle]:** "recent enough" is relative to the source's cadence, not the calendar. **Annual** sources: a recency window applies (a country's latest value must fall within it). **Irregular/snapshot** sources (PEI per-election, PEFA latest-assessment, FATF/BRSS single-wave): **"latest available" counts as current** provided the source itself has not been superseded.

**Parameters [LOCKED — 2026-07-10, on Step-0 coverage evidence]:**

- **Recency window (annual sources):** a country's latest observation must fall within **4 years** of the source's most recent year (`latest ≥ file_max_year − 4`). Evidence: the `median_latest_yr` distribution across the 255 annual metrics is sharply bimodal — 239 cluster at 2023–2026, a near-empty valley at 2021–22, then a dead tail of 6 at ≤2020; a 4-yr window cuts cleanly through the valley (window choice is low-sensitivity in the 3–5 range).
- **Cadence-relative rule (snapshot/irregular sources):** latest-available value counts as current, provided the source has not been superseded (unchanged principle above).
- **Denominator = sovereign core (192):** current-coverage is measured against the 192 sovereigns (spine of 213 minus 21 flagged territories), **not** the full spine — so strong sources are not penalized for microstate/territory gaps. Evidence: on the 213 denominator, WJP (covers 143 sovereigns) read 67%; on 192 it reads 74%, its true current-coverage.
- **Inclusion threshold = ≥60% current-coverage of sovereigns.** Metrics ≥60% are included; metrics **<60% are flagged for individual review at Step 1, never auto-dropped**. Result: **246 of 255 annual metrics** clear the bar. Confirmed rescues: WJP factors 74.0%, Romelli CBI 78.6%, WDI tariffs 84.9%. Correctly flagged (dead tail, 0% current): Polity5 (ended 2018), Hanson-Sigman (2015), WB informal-economy (2020), WDI pupil-teacher-ratio (2017).
- **Two ways to fail, reviewed differently:** a **recency failure** (live but lagging — e.g. UNODC homicide, broad but publishes with a multi-year lag) is kept with a cadence-appropriate window or a staleness flag; a **breadth failure** (current but narrow — e.g. IMF fiscal rules, 122 countries) is kept-and-flagged where it is the sole source for its concept. Only metrics that fail **and** are redundant (e.g. Polity5, superseded live by V-Dem) are retired — each an explicit per-metric decision at Step 1, with full history preserved in the evidentiary layer (§1).
- **Evidence artifact:** `data/processed/metric_coverage.csv` (built by nb 39) carries `curcov_pct_w4` (vs 213), `curcov_sov_pct_w4` (vs 192 — the inclusion measure), `cadence`, `median_latest_yr`, and `hist_depth_avg_yrs` per metric.

## 5. Normalization (D4) [SPEC PENDING]

**Requirement [LOCKED]:** sources arrive on incompatible scales (V-Dem interval, WGI ~N(0,1), 0–100 indices, ordinals, zero-inflated long-tailed counts — homicide, coups, journalist killings, conflict deaths). Everything is **re-normalized from raw to one common convention** before aggregation; source-native scaling is ignored.

**Recommended default [SPEC PENDING]:** **z-score with winsorization at ±3 SD** across the scored universe — preserves relative magnitude (gap size is signal for tail-risk), standard in composite-indicator methodology, combines cleanly under weighted averaging. **Skewed/count sources** (homicide, coups, killings, conflict deaths, carbon revenue) flagged for **log-transform-then-z or percentile**, decided per-indicator in the scaffold (z+winsorize distorts on heavy skew).

**Live alternative:** **percentile rank** — robust and interpretable, but flattens the tails (bad where "how bad is the failing state" is signal). Decided **empirically at Step 4** (build both; keep whichever is more stable/defensible under sensitivity analysis).

**Within-year vs fixed-baseline fork [SPEC PENDING — consequential]:** normalizing **within each year** answers "where did this country rank that year"; a **fixed pooled baseline** makes movement reflect real change, not shifting peers. Different time series, different momentum. **Momentum (§9) requires the fixed-baseline panel regardless** — the strongest argument for using fixed-baseline for the level scores too. Resolved at Step 0.5.

## 6. Within-concept aggregation (D5) [principle LOCKED; params SPEC PENDING]

**Principle [LOCKED]:** concept score = **tier-weighted mean** of its normalized, direction-aligned indicators, with **weights renormalized over present indicators** (missingness doesn't zero a concept — same pattern as BRSS/RTI). Tier reflects directness + centrality (master principle 7).

**No formal decorrelation in v1:** overlapping indicators (V-Dem/WJP/FH measuring adjacent content) are controlled via tier weighting + the repetition rule, not PCA/factor analysis (opaque, hard to defend to investment users). Decorrelation noted post-v1.

**Periodic indicators** are collapsed to their **latest-within-window** value before entering the concept (not "latest calendar year", which would drop a genuinely-current per-election reading).

**Parameters [SPEC PENDING]:** coarse tier-weight values (illustrative 1.0 / 0.5 / 0.25) at Step 0.5.

## 7. Category & framework weighting (D6) [OPEN]

**Intended basis [committed in master]:** weighting at category and framework levels uses the per-concept **economic-relevance annotations** (Very strong / Strong / Moderate / Thin).

**Blocker:** annotations exist for concepts 1–9 but are **missing for Concept 11 (Trade) and Concept 12 (Environmental)** — complete before this locks.

**Open sub-decisions:** how ordinal annotations map to numeric weights; whether across-category weighting is relevance-based or equal (lean: concept→category by relevance; category→framework with caution — see §1, single composite optional/caveated).

## 8. Reliability & coverage (D7) [principle LOCKED; threshold SPEC PENDING]

**Principle [LOCKED]:** every score (concept and category) carries a **coverage/confidence flag**. A minimum coverage is required to emit a score. **No imputation in v1** — gaps flagged, not filled. One framework-wide convention **subsumes the per-source flags already built** (`brss_reliable`, RTI `has_rti_law`, the BRSS 0.70 threshold) rather than ad-hoc per source.

**Threshold [SPEC PENDING]:** the min-coverage cutoff is read off the coverage distribution **after harmonization** (the Step-0 histogram shows a workable core/tail break near the ≥20-source knee, but the cutoff can't finalize until the 7 name/id-keyed files are folded in and aggregates stripped).

## 9. Momentum (parallel output) [structure LOCKED; params SPEC PENDING]

A **separate, parallel coordinate — never blended into the level score** (blending destroys both signals: a high-stable country must be distinguishable from a low-improving one).

**Computed at the concept level [LOCKED]**, from two components:
- **Magnitude** — tier-weighted average of the **trailing-window slope** of each panel-backed metric (normalized). Slope over a window, not year-over-year Δ (YoY is dominated by single-year jitter and by sticky de-jure sources that sit flat then jump).
- **Breadth — net diffusion:** **(share of metrics improving − share deteriorating)**. Net (not just "share improving") so a concept churning in both directions doesn't read as strong momentum. Diffusion-index logic (as macro uses for PMI internals): a broad-based move is more trustworthy than a narrow one.

Reported as **two coordinates, not collapsed by default** ("avg +0.3/yr, 4 of 5 improving" is more decision-useful than "momentum 0.42"). If ever collapsed: **breadth-discounted magnitude** — low breadth widens the confidence band / discounts trust; it does **not** shrink the magnitude (a real measurement).

**Availability [LOCKED]:** defined **only for panel-backed metrics/concepts**; **null (not zero)** where no usable history exists. Snapshot sources (AREAER-ER, FATF, CPJ, PEFA, IDEA-PolFinance, RTI, WB-BRSS) are excluded from the breadth denominator — "no history" ≠ "flat". Consequence: momentum is rich for democracy/rights/stability/corruption concepts and structurally absent for C9 (financial — FATF+BRSS both snapshot), the de-facto-ER leg of C8, C7 PFM (PEFA), and the RTI/PolFinance leg of C25.

**Normalization dependency [LOCKED]:** momentum is computed on the **fixed-baseline** normalized panel (within-year normalization would read a country as "improving" merely because peers deteriorated — a ranking artifact).

**Parameters [SPEC PENDING — at Step 0.5, needs history-depth evidence]:** window length (lean ~5 yr, **adaptive** — short panels like CIVICUS 2022–25, ODIN, EPI can't support 5 yr and get a low-confidence flag); dead-band threshold for "flat"; minimum-metric count for trustworthy breadth (lean ~3; below that, magnitude-only + breadth flagged low-confidence); whether breadth is tier-weighted (magnitude is).

## 10. Deferred / open design questions (register)

- **Equality incorporation** [OPEN] — left open when equality was removed as a standalone concept. Time-boxed decision at Step 1: v1-in (distributed across existing concepts) or v1-deferred. Not to become a re-architecture.
- **Track-record / predictability / payment-culture composite** [OPEN] — distributed content vs standalone dimension. Same Step-1 time-box.
- **Process/outcome classification of metrics** [OPEN] — established principle, not yet applied concept-by-concept. At Step 1.
- **Concept 25 boundary** — decided KEEP (2026-06-18); flagged to revisit with the full framework view before finalizing.

## 11. Localized metric-selection flags (pointer)

Resolved during Step-1 metric selection, concept-by-concept. Authoritative per-source detail in `framework_decisions.md`; summary:

- **C8** — AREAER `other_managed` is a residual, not a flexibility rank (handle separately / flag).
- **C9** — FATF 2013-vs-2022 methodology-scale comparability (`methodology_round` flag is the lever: use-as-is / filter / down-weight). BRSS 0.70 reliability threshold sensitivity.
- **C11** — KOF proxy (`dr_eg` = Economic, not Trade subindex) vs dedicated pipeline. Economic-relevance annotation missing.
- **C12** — EPI policy/institutional sub-component selection. WB-carbon inferred-absence flag; revenue/GDP materiality. Economic-relevance annotation missing.
- **C17** — Fraser Area-2 property-specific sub-component selection.
- **C18/C25** — IDEA Political Finance cross-reference (homed in C25, also anti-corruption transparency).
- **C20** — IDEA Voter Turnout compulsion adjustment.
- **C22** — Pew SHI presence confirm.
- **C23** — CPJ Israel/OPT lumped under ISR.
- **C25** — RTI no-law floor (min−1SD assigned floor; `has_rti_law` flag) revisit.
- **Cross-cutting** — WGI standard errors (optional ranking-confidence enhancement); WDI WBL/HCI/social-protection sparse recent coverage (investigate at harmonization); SPI-overall sparser than pillar-1 (flag); GTD/BCI currency verification.

## Changelog

**2026-07-10 (Step 0.5)** — Metric inclusion rule LOCKED (§4): recency window 4 yr for annual sources; cadence-relative for snapshot/irregular; denominator = 192 sovereigns; threshold ≥60% current-coverage; sub-threshold flagged for Step-1 review, never auto-dropped. 246/255 annual metrics clear. Evidence: `metric_coverage.csv`.

**2026-07-10** — Step-0 harmonization + spine COMPLETE (nb 39, `src/country_harmonization.py`, `country_spine.csv`). D2 revised: population floor removed (“include everything”); spine = 213 economies, 21 territories flagged. Powell-Thyne COW/GW coding confirmed and mapped; UCDP/DPI live-country name misses fixed (Russia, Germany, China, UAE recovered). Per-metric current-coverage table generated (459 metrics; 60 under 60% flagged for Step-1 inclusion review). Next: lock D4–D7 + inclusion/momentum parameters at Step 0.5 against this evidence.

**2026-07-09** — Document created. Seeds the metric-pass methodology from the Step-0 design decisions: architecture (D1), spine (D2), directionality (D3), inclusion principle, and the D4–D7 + momentum specifications at their current lock status. Follows the Step-0 harmonization/coverage audit.
