# Metric Methodology

**As-of (last manually updated):** 2026-07-09
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

## 2. Country spine (D2) [rule LOCKED; list SPEC PENDING]

**Rule [LOCKED]:** ISO3 list of countries with **population > 2M**, excluding **effectively closed regimes**. Coverage is always measured against this spine.

**Thin-coverage countries [LOCKED — option A]:** genuine countries meeting the pop/closed-regime rule are **included even when source coverage is thin**, carrying a low-reliability flag (§8) rather than being silently dropped. We exclude only on the pop/closed-regime rule, not on under-measurement.

**The list itself [SPEC PENDING]:** produced by the Step-0 harmonization pass from a canonical population source + an explicit closed-regime exclusion list, then reviewed. Target ~150–160. Held in `country_spine.csv` once approved.

**Harmonization requirement [evidence, Step-0 audit]:** country keys are not uniformly ISO3 — 7 files are name/id-keyed (FH, FSI, CIVICUS, Pew, DPI by name; UCDP by numeric id; IRENA by non-ISO3 code); several files carry regional/income **aggregates** (WDI ~265 tokens incl. Arab World, Euro area, EU, Fragile States); and at least one file is **suspected to use COW/Gleditsch-Ward** 3-letter codes rather than ISO3 (Powell-Thyne — to verify, not asserted). All sources must be canonicalized to ISO3, aggregates stripped, and defunct/historical entities dropped before the country×indicator matrix is built.

## 3. Directionality (D3) [LOCKED]

All indicators are normalized so **higher = better governance**. Every indicator carries an explicit `direction` and a one-line `direction_evidence` note verified **against the source codebook, not memory**. A **sign-sanity validation pass** (Step 4) checks, pre-aggregation, that known-good countries score high on each indicator. Rationale for extra care: a sign error is silent — plausible all the way to the output — so it gets its own checkpoint, not just a column.

## 4. Metric inclusion / usability [principle LOCKED; parameters SPEC PENDING]

**Principle [LOCKED]:** a metric's inclusion is judged by **current cross-sectional coverage on the spine** — the share of spine countries with a *recent-enough latest value* — **judged against the source's own cadence**. **History depth is a separate, non-gating attribute:** a metric with broad recent coverage but no long panel is fully includable; a metric with a long panel but stale/thin recent coverage may fail.

This **rejects panel-fill rate** (non-null cells ÷ all country-years) as the inclusion test: a per-election or snapshot source shows low panel-fill for structural reasons that say nothing about current usability.

**Cadence-relative recency [LOCKED principle]:** "recent enough" is relative to the source's cadence, not the calendar. **Annual** sources: a recency window applies (a country's latest value must fall within it). **Irregular/snapshot** sources (PEI per-election, PEFA latest-assessment, FATF/BRSS single-wave): **"latest available" counts as current** provided the source itself has not been superseded.

**Parameters [SPEC PENDING — at harmonization]:** the recency window for annual sources (candidate ~3–4 yr), the inclusion threshold (what current-coverage % gates a metric in), and the precise snapshot-staleness test. Step-0 reports, per metric, the **distribution of per-country latest-years** (not just the file's max year) and current-coverage under a couple of window choices, so these are set on evidence.

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

**2026-07-09** — Document created. Seeds the metric-pass methodology from the Step-0 design decisions: architecture (D1), spine (D2), directionality (D3), inclusion principle, and the D4–D7 + momentum specifications at their current lock status. Follows the Step-0 harmonization/coverage audit.
