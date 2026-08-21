# Sovereign Governance Framework — Project Handoff

> **Purpose of this document.** A comprehensive context transfer for a new chat session, covering the project's goals, the dashboard, the data pipeline feeding it, the repository structure, what is done, what is outstanding, and the working preferences that govern how Claude should interact with the project owner (Marty). Lean is toward MORE detail. Read this in full before acting.

---

## 1. PROJECT OVERVIEW & GOALS

**What this is.** A sovereign governance assessment framework built for emerging-market (EM) sovereign research and portfolio investment decision-making. It scores countries across governance concepts, so an analyst can compare a country to the world and to its peers, understand *why* a country scores as it does (full attribution/decomposition), and track governance over time.

**Owner.** Marty (GitHub: `mjboulanger`).

**Scale.**
- **5 categories**: Accountability; Economic and fiscal governance; Political foundations; Rule of law; State capacity.
- **~24 scored concepts** distributed across the 5 categories (concept IDs are not contiguous — e.g. there is no concept 7; live IDs include 1–6, 8–25).
- **144 scored metrics** across all concepts.
- **213 economies** (192 sovereigns + 21 territories). The **scoring universe / distribution base is the 192 sovereigns**; territories are tracked but excluded from percentile/distribution computations.

**The governance module is the active focus.** Sovereign credit, macro vulnerability, and energy-transition risk are separate modules, out of scope here.

**Scoring hierarchy (how a country's numbers are built):**
- **Metric**: a raw indicator value (e.g. homicide rate, a V-Dem index) harmonized to a 0–1 score.
- **Concept**: a weighted combination of its metric scores.
- **Category**: a weighted average of its concept scores.
- Weights: concept→category uses `effective_weight` (relevance × measurement-quality). Metric→concept uses `renormalized_weight`.

**Key methodological principles (these are load-bearing — respect them):**
- **De jure vs de facto distinction matters.** Some scores are explicitly "rules on paper" (e.g. World Bank BRSS regulatory stringency) vs. effectiveness. This framing must be preserved through the metric labels and any display.
- **Reliability flags over score penalties** — sparse coverage gets a `_reliable` flag, NOT a multiplicative score penalty (which Marty deemed methodologically incoherent).
- **Don't offload judgment into flags.** If a data quirk matters to the metric, encode its effect directly in the value or calculation. If it doesn't matter, drop it. A flag that just defers a decision downstream is worse than useless at this scale.
- **Tiering principle**: tier placement reflects BOTH measurement quality AND centrality of the dimension to the concept — not quality alone.
- **Indicator repetition is tracked, not prohibited**: the same source can legitimately appear across multiple concepts.
- **Validate directionality against literature** before committing (e.g. BRSS sub-constructs checked against Anginer et al. 2019).
- **Catch future-proofing at parse time**: e.g. BRSS question codes stored without year suffixes, year auto-derived at parse with loud failure if a code no longer resolves — catches wave renumbering without manual maintenance.

---

## 2. DATA / AUTOMATION PHILOSOPHY (CRITICAL — governs all pipeline work)

Marty wants the collection/update/maintenance of data to be **as automatic as possible**, with **minimal manual hard-coding** for ongoing updates.

- Keep manual user input to an ABSOLUTE MINIMUM for ongoing updates/maintenance.
- If hard-coding is unavoidable for an update, it MUST be reflected in the instructions doc (`docs/instructions_data_maintenance.md`), and Claude must FLAG anywhere in code that requires the user to hard-code new values as data updates.
- Values like "data as of date" / "latest available date" must come FROM the data/source, never hard-coded. (E.g. vintage is parsed from `download_log.csv`, not stamped.)
- If something must be updated over time, find a way to do it without user input; if user input is truly required, make the user do it as few times as possible (ideally once, in a single config location).
- When building a data pipeline, ALWAYS check for automated options first. If unavailable, check whether a non-automated pipeline can be sourced from an automated one.
- Anything requiring user input (e.g. "user must update VDEM_VERSION") MUST be in the instructions doc.

---

## 3. ENVIRONMENT & CROSS-MACHINE SETUP

- **Mac** (current working machine): `/Users/boulanger/Documents/governance-framework`, shell = **zsh**.
- **Windows PC**: `C:\Users\mjbou\governance-framework`, shell = **PowerShell**.
- **conda env**: `governance-framework` (Anaconda). Primary interface/editor: **JupyterLab**.
- **Libraries**: pandas, Plotly (dashboard), numpy.
- **Version control / cross-machine sync**: Git + GitHub (`github.com/mjboulanger/governance-framework`). The repo IS the sync mechanism between Mac and PC.
- **OneDrive is a git-corruption risk** — the project is deliberately OUTSIDE OneDrive.
- **Cross-machine determinism is solved**: a `write_csv()` helper in `config.py` (standardized float format + LF line endings) plus `.gitattributes` enforcing LF storage. All tracked CSVs are byte-identical across machines. The two axes of cross-machine CSV churn (float representation, line endings) are both controlled at the write layer.

---

## 4. REPOSITORY STRUCTURE

> Paths are relative to the project root. Contents described generally; exact code lives in the repo.

### `src/` — pipeline & build code
- **`config.py`** — shared config: `PROCESSED_DIR`, `RAW_DIR`, `FRAMEWORK_START_YEAR`, `CURRENT_YEAR`, and the critical **`write_csv()`** helper (deterministic float format + LF endings). All CSV writes should go through this.
- **`build_normalized_panel.py`** (methodology "D3") — THE normalization engine. Reads every scored metric from its source file, applies its assigned `final_method` (z-family / percentile / binary / fixed-anchor) against a fixed trailing-20-year pooled baseline, harmonizes to 0–1, direction-aligns (higher = better), and writes:
  - `normalized_panel.csv` (long: one row per iso3 × year × metric) with columns: `iso3, year, metric, raw_value, normalized, harmonized, direction, final_method, method_source, baseline_n_years, baseline_n_obs, baseline_year_span, baseline_mean, baseline_sd`.
  - `metric_normalization_params.csv` (per-metric scalar params: `metric, final_method, method_source, direction, direction_flipped, pre_transform, baseline_mean, baseline_sd, baseline_n_obs, baseline_year_span, winsor, harmonize_rule`) — 144 rows.
  - `percentile_baselines.csv` (the actual sorted baseline vector for each percentile metric — mean/sd can't reconstruct a midrank percentile).
  - Method families present: `zscore` (~506k rows), `percentile` (~69k), `binary` (~19k), `log1p_zscore` (~5k).
  - Harmonize rule for z-family: `(clip(z, +/-winsor) + winsor) / (2*winsor)` with winsor=3. Percentile & binary: `identity (already 0-1)`.
  - Census metrics (absence = real 0) are spine-zero-filled BEFORE normalization, derived from `metric_missingness_tags.csv` (single source of truth), not hardcoded.
- **`build_final_scores.py`** — CORE scoring. `score_categories()`: category = weighted mean of penalized concept scores, weights = `effective_weight` (relevance × MQ). Writes:
  - `concept_attribution.csv` (per-concept: penalized_score, effective_weight, weighted_contribution, relevance, measurement_quality).
  - `category_scores.csv` (iso3, category, category_score, n_concepts, sum_effective_weight, category_weight_rule).
  - `final_scores.csv`, `concept_scores.csv`, `concept_contributions.csv`.
  - **NEVER casually touch this file**; if you do, verify scores are byte-identical after.
- **`build_peers.py`** — the peer-group algorithm. For each country, selects N=10 peers balancing income proximity (~15% dead zone + concave/sqrt compression), a soft regional lean, and a soft population lean. Excludes micro-states (<1M), territories, and no-GDP countries. Writes `country_peers.csv`.
- **`build_dashboard_data.py`** — transforms processed CSVs → `dashboard/dashboard_data.json` (the dashboard's data layer). ~16–17KB of code. Details in §6.
- **`build_dashboard.py`** — inlines `dashboard_data.json` + Plotly into `dashboard/dashboard_template.html` to produce the final self-contained `dashboard/governance_map.html`.
- Plus ~38 source-specific pipeline notebooks/scripts (one per data source): IMF AREAER (de facto regime, FARI), World Bank BRSS, RTI Rating, Chinn-Ito KAOPEN (reserved, not yet built), V-Dem, etc.

### `data/`
- **`data/raw/`** — raw downloaded source files (~32 cleaned source files).
- **`data/processed/`** — all pipeline outputs (CSV). Key files: `normalized_panel.csv` (~56MB, gitignored, regenerable), `metric_normalization_params.csv`, `percentile_baselines.csv`, `concept_contributions.csv`, `concept_scores.csv`, `concept_attribution.csv`, `category_scores.csv`, `final_scores.csv`, `country_peers.csv`, `country_spine.csv` (213-country spine), `metric_missingness_tags.csv`, `metric_selection.csv`, `metric_distribution_profile.csv`, `download_log.csv` (vintage/data-as-of source of truth).
- **`data/reference/`** — reference tables. Notably `metric_labels.csv` (144 rows: `metric, source_label, metric_name`) — the canonical human-readable metric names.

### `dashboard/`
- **`dashboard_template.html`** — the UI (HTML/CSS/JS + Plotly). ~183KB currently. This is what gets edited for all dashboard features. Committed.
- **`dashboard_data.json`** — the inlined data layer (~6.9MB). **Gitignored** (regenerable).
- **`governance_map.html`** — the final built dashboard (~12MB). **Gitignored** (regenerable). This is what the user opens.
- (There was a stray `dashboard.html` ~10.7MB from an old build — now gitignored/removed.)

### `docs/`
- **`governance_framework_master.md`** + **`.pdf`** — the master framework document. Comprehensive guide anyone could use to understand what's been done in detail (categories, concepts, metrics, sources, principles, methodology, workplan). The `.md` is the editable source; the `.pdf` is rendered. **Keep both current with all categories, concepts, metrics, sources, major principles, key decisions, methodology, and workplan.** Regularly check consistency with the master PDF.
- **`framework_decisions.md`** — running log of key decisions + a consolidated by-source build-status table tracking all ~38 sources. Keep current.
- **`instructions_data_maintenance.md`** — the maintenance manual. ANYTHING requiring user input for updates (hard-coded values, version bumps) MUST be documented here. Has sections on: metric display names, building the dashboard, drill-down contribution decomposition (incl. the peer-reference feature), rebuild reminders.
- **`metric_methodology.md`** — LOCKED scoring methodology sections.

### Config / hygiene
- **`.gitattributes`** — enforces LF storage for CSVs (cross-machine determinism).
- **`.gitignore`** — ignores regenerable large artifacts: `dashboard/governance_map.html`, `dashboard/dashboard.html`, `dashboard/dashboard_data.json`, `data/processed/normalized_panel.csv`, etc.

---

## 5. THE DASHBOARD (governance_map.html) — DETAILED

Self-contained HTML file, three tabs (views): **Map**, **Drill-down**, **Time series**.

### Build process (TWO steps — important)
1. `python src/build_dashboard_data.py` — data → `dashboard_data.json`.
2. `python src/build_dashboard.py` — inlines JSON + Plotly → `governance_map.html`.
- **Percentile/contribution/any data-layer change needs BOTH steps.** Rebuilding only step 2 reuses stale JSON.
- A **57-country SAMPLE** is embedded in the template as a fallback; when the sample is what's showing, the header reads "SAMPLE DATA · 57 economies" and drill-down metric/contribution features show empty. **Drill-down features only validate on real-data rebuilds** (213 economies in the header).

### Map view
- Choropleth world map (Plotly), score-colored. Side panel with a **radar** (country profile): country shape, 25–75th percentile band (as a true ring), median reference line. Adapts between Overall (5 categories) and category-level (concepts) views.
- **Compare mode**: peer overlay on the radar. Uses `activePeers` (editable peer iso3 list). `drawCompare()` live-computes the peer 25–75 band + peer median per axis from `activePeers`. Editable peer chips (add via search, remove via ×). Changing focus country reloads `activePeers` to that country's default peers.
- **`activePeers` is SHARED with the drill-down** (see below) — this is the cross-screen sync mechanism.

### Drill-down view (the most-developed view)
- **Miller-column layout**: Column 1 = Categories, Column 2 = Concepts (of clicked category), Column 3 = Metrics (of clicked concept). Clicking drills right.
- Country selector (synced with map's `currentIso`) + a **World/Peers reference toggle** (committed feature `2d778e1`).
- **Position bars** ("vs world/peer median"): where the country sits in the distribution. Scaled to the **p05–p95** span (so tail values stay distinguishable, not clamped at quartiles), tick marks at p25/p50/p75, centered on the median.
- **Contribution bars** ("contribution to category"): each item's SIGNED contribution to the category score = `weight × (item value − reference MEAN)`. Metric and concept bars share ONE scale (contribution-to-category) so they're comparable across columns. Warm = pulls category down; cool = lifts it.
- **Why mean for contributions, median for position**: the MEAN chains additively (metric→concept→category reconciles); the MEDIAN does not chain. So position bars (rank) use median, contribution bars (decomposition) use mean.
  - Known limitation: additive chaining is exact for most (country, concept) pairs (median residual ~0.001, p95 ~0.007) but has a thin tail up to ~0.1 concentrated where a concept has heavy per-country metric missingness. Accepted as a visual aid.
- **Category column** also shows up-to-4 material driver concepts (|deviation| ≥ 0.05), in true direction (▲/▼), ranked by deviation from the active reference (world or peer median).

### Peer reference toggle (COMMITTED, `2d778e1`) — KEY ARCHITECTURE
- In **Peers mode**, all three columns shift reference to the country's peer group: position bars center on peer MEDIAN, contribution bars use peer MEAN, category drivers rank by peer deviation.
- **The scale stays UNIVERSE-anchored** (world contribution range / world p05–p95). Peers are similar, so a peer-spread scale would amplify tiny differences; keeping the universe scale means a small gap vs similar peers stays a short bar. The on-screen note states this explicitly.
- **Peer contributions are computed LIVE in JS, not precomputed.** Rationale (a load-bearing principle): fixed-reference derivations (scores, weights, world contributions) are computed once in the pipeline; but the peer set is USER-EDITABLE, so peer contributions depend on live UI state and cannot be precomputed. The display layer computes them — but MINIMALLY, consuming canonical primitives:
  - Peer reference = simple AVERAGE of the peers' own concept scores / category scores / metric values (read from the JSON). Peers contribute ONLY their averaged scores/values as reference points; ALL attribution is a FOCUS-country operation using FOCUS weights.
  - The one field the pipeline exposes so JS never recomputes a weight: concept **weight share** `ws` (in each concept record).
  - Verified: `cc_p = ws × (focus_concept_score − mean(peer concept scores))` exactly reproduces the (former) precomputed values.
- **Editable peer chips** under the toggle (Peers mode only) share the map's `activePeers` — edits sync both screens. Focus change reseeds to defaults. No-peer countries (territories/micro-states) disable the Peers button with a note.
- Key JS: `activePeer()` (global: is peer mode active?), `hasPeers()`, `drillPeers()` (active peer set for the focus), `peerProfile()` (live mean/median per concept/category/metric over the active set, cached per token), `renderDrill()`, `conceptsInCategory()`, `metricsInConcept()`, `positionBar()`, `contribBar()`, `topDrivers()`, `syncRefToggle()`, `openDrillAddPeer()`.

### Distribution panel + calculation breakdown (IN PROGRESS — NOT committed, see §7)
- A right-hand panel in the drill-down. Clicking any category/concept/metric row shows, in the panel:
  1. A **histogram** of that item's actual values across the 192 sovereigns (NO smoothing — real binned counts, ~24 bins), with the focus country marked (teal line), quartile ticks (p25/p50/p75 dotted), and in Peers mode, the peer countries marked.
  2. A **calculation breakdown** ("how this number is built"), drilling ONE level down:
     - Category → weighted table of its concepts (score, weight `ws`, contribution) summing to the category score.
     - Concept → weighted table of its metrics (harmonized value, weight `w`, contribution `c`) summing to the concept score.
     - Metric → the raw→harmonized path: plain-language description of the method, then the actual arithmetic (e.g. z-score: `z = (raw − baseline_mean)/baseline_sd → clip ±3 → (clip+3)/6 = score`), plus the metric's definition and scale/source (so the raw value is interpretable). Handles all 4 method families (zscore, log1p_zscore, percentile, binary).
- `drillDist = {level, key}` drives the panel (last-clicked item at any level). `renderDist()` builds the histogram; `renderCalc(level, key)` builds the breakdown.
- **Peer marker approach is unsettled** (see §7): tried dots, then lines with hover (hover unreliable in Plotly for thin vertical lines), currently trying **vertical country labels at the base of each peer line with horizontal collision handling** (labels nudged apart + leader lines). Fallback if that fails: numbered lines + a toggleable numbered key. Design constraint: everything must be SCREENSHOT-friendly (static, no reliance on hover) because Marty puts these charts into other materials.

---

## 6. DATA LAYER — dashboard_data.json SCHEMA (~6.9MB)

JSON object keys are STRINGS. Structure:

```
meta:
  categories: [5 category names]
  concepts: { "<cid>": { name, cat } }
  metrics: { "<key>": { def, src, name, label,
                        meth, pre, bmean, bsd, nobs, winsor, hrule, dir } }
      # meth=final_method; pre=pre_transform; bmean/bsd=baseline mean/sd;
      # nobs=baseline_n_obs; winsor; hrule=harmonize_rule; dir=direction (+/-)
      # (the meth..dir fields were added for the metric<-data calc breakdown)
  percentiles:
    categories: { "<cat>": { p05, p25, p50, p75, p95 } }   # sovereigns only
    concepts:   { "<cid>": { p05, p25, p50, p75, p95 } }
  metric_percentiles: { "<key>": { p05, p25, p50, p75, p95 } }
  generated: "<date> (SAMPLE DATA)?"    # header vintage
  n_countries: <int>

countries: { "<ISO3>": {
    name, terr (bool: is territory), np (metrics present),
    mc: { total, by_cat: {<cat>: n} },
    peers: [iso3, ...],       # default peer set (empty for territories/micro-states)
    pop: <int|null>,
    cat: { "<catName>": score|null },      # category scores
    con: { "<cid>": { s, lc, mag, brd, cc, ws } }
        # s=concept score; lc=low-confidence bool; mag/brd=momentum magnitude/breadth;
        # cc=WORLD concept->category contribution (precomputed, fixed reference);
        # ws=concept weight share of its category (canonical; exposed for live peer calc)
} }

history: { ... }   # time-series trajectory (for the Time series tab; ~3MB)

contributions: { "<ISO3>": { "<cid>": [ {
    m,   # metric key
    t,   # tier
    v,   # harmonized value (0-1)
    w,   # renormalized_weight (metric weight within concept)
    c,   # metric_contribution = w * v
    sc,  # signed metric contribution vs world mean
    scat,# metric->category contribution (world; = sc * concept weight share)
    y,   # latest_year
    st,  # stale flag (0/1)
    b,   # bucket (or null)
    raw  # RAW pre-harmonized value (added for metric<-data calc breakdown)
} ] } }
```

**Fields REMOVED in the peer-toggle refactor** (do not expect them; they're now computed live in JS): `cc_p`, `pm` (concept peer contribution/median), `scat_p`, `pmed` (metric peer contribution/median), `catpm` (category peer median). The rationale is in §5 (editable peer set → display-layer computation).

---

## 7. STATUS: DONE vs OUTSTANDING

### Committed & done
- Full pipeline builds across all concepts (~38 sources): IMF AREAER (de facto regime notebook 37, FARI notebook 32), WB BRSS (notebook 38), RTI Rating (notebook 30), and others.
- Cross-machine determinism (write_csv + .gitattributes); all tracked CSVs byte-identical.
- Dashboard Map view (choropleth + radar country profile + peer-comparison radar).
- Dashboard Drill-down: Miller columns, position + contribution bars, signed mean-reference decomposition on a shared scale, p05–p95 position bars, category driver call-outs.
- Metric display names (`metric_labels.csv`, 144 rows; format `[metric name] ([source])`, de jure/de facto tags with comma).
- **Peer-reference toggle** (World/Peers) across all three columns, live-computed in display layer, editable peer chips synced with map. Committed `2d778e1`. Docs updated in `instructions_data_maintenance.md`.
- Last committed HEAD referenced this session: `2d778e1` (peer toggle). Both machines were synced to it.

### IN PROGRESS — uncommitted, NOT fully verified (the immediate task for the new chat)
The **distribution panel + calculation breakdown** feature:
- **Data layer**: `patch_calc.py` was applied to `build_dashboard_data.py` — adds normalization params to `meta.metrics` (meth/pre/bmean/bsd/nobs/winsor/hrule/dir) and `raw` to each contribution row. **Verified populating correctly** (JSON grew 6.6→6.9MB; z-score arithmetic reproduces harmonized values exactly).
- **Template**: distribution panel built (histogram + focus marker + quartiles), calc breakdown for all 3 levels built and arithmetic verified, panel styling (full-height divider, right padding), metric metadata (def + scale/source) shown. The LATEST template iteration switched peer markers to **vertical collision-handled labels** — **this last version was presented but NOT yet confirmed working or committed by Marty.** The new chat should: confirm the vertical-label peer approach renders cleanly (especially clustered peers), or fall back to numbered-lines + toggleable key; then commit the whole feature (data-layer patch + template + a docs note) as ONE unit.
- **Nothing about the distribution panel is committed yet.** Verify current git status first.

### Outstanding roadmap (Marty's rough priority order)
1. Finish + commit the distribution panel / calc breakdown (immediate).
2. Concept-click-from-map-panel → open the drill-down there.
3. Time-series screen (third tab; trajectory from `history` in JSON; no attribution).
4. Documentation/methodology: click any category/concept/metric NAME → popup with definition + methodology + the actual calculation (the calc breakdown now covers much of "actual calculation"); plus a separate readable page rendering the master doc `.md`.
5. Momentum polish (mag/brd per concept, already in JSON).
6. Stage 6 polish; Stage 7 Excel companion.

### Deferred / later
- Chinn-Ito KAOPEN pipeline (notebook 31 reserved, not built).
- Metric pass across all concepts (combine source scores into concept scores); SDG 16 review to-do; Concept 25 (Government transparency and openness) reconsideration before metric-pass finalization.
- Multi-source PDF report extraction (IMF Article IVs + WB CCDRs).
- SOE governance → v2.
- A separate political-analysis project (2026 US midterm populism ledger) belongs in a DIFFERENT project context, not here.

---

## 8. HOW TO WORK ON THE DASHBOARD (practical mechanics learned this session)

- **Claude's container ≠ the repo.** Claude's bash/view operate on Claude's own sandbox. Everything reaches the Mac via Marty running commands. To edit a real file, Claude reads an uploaded copy, patches/tests it in the container, and returns a downloadable file or a tested patch script.
- **Paste-mangling bug**: PowerShell/zsh here-strings with triple-quoted Python get mangled on paste. **Standard workflow: give patches as DOWNLOADABLE .py files (via present_files), tested in the container against the real uploaded file first.** Marty runs `cp ~/Downloads/patch.py . && python3 patch.py && rm patch.py`.
- **Stale-download bug**: the browser won't overwrite a same-named file in Downloads; Finder "Date Added" is misleading (shows original date even after overwrite; real mtime via `ls -la`). **STANDARD PATTERN: `rm -f ~/Downloads/FILE` BEFORE re-downloading**, then verify with `ls -la` / a `grep -c` marker before copying into place.
- **Two-step build** (see §5). After data-layer edits, regenerate the JSON (step 1) before rebuilding (step 2).
- **Marty cannot use keyboard shortcuts reliably** (e.g. Cmd+Shift+R). To bypass browser cache: fully CLOSE the tab and reopen via `open dashboard/governance_map.html`. To open dev console: menu bar (Chrome: View → Developer → JavaScript Console).
- **Assume uploads/downloads go to `~/Downloads`.** New files going there should replace any existing same-named file (delete-first).
- Patches should be tested in the container (apply against the real uploaded file, assert anchors match exactly, check syntax / brace + paren balance) BEFORE presenting.
- When giving a patch, verify the uploaded file is the CURRENT version first (Marty may upload a stale copy — check a marker like a byte count or a `grep -c`).

---

## 9. MARTY'S INTERACTION PREFERENCES (governs HOW Claude works with him)

### Instruction delivery
- **One instruction at a time that requires output verification or his input.** Do NOT stack dependent instructions. If an upcoming code block/instruction depends on the result of a previous one, HOLD until the result comes back. Don't spend compute assuming his input or the output of an open instruction.
- **Full file or full cell (for .ipynb) if there's MORE THAN ONE edit.** If the change is very small and targeted, tell him EXACTLY what to change — give the existing code to replace, including rows above/below for accurate placement. No general instructions.
- **If Claude corrects an edit after giving it, re-state the whole thing** (whole new file/cell if >1 change).
- **Label every code block with its language** (bash, powershell, python, etc.) so he knows where it goes.
- **Use terminal code blocks for edits to files; use the editor for creating files with nested quotes.**

### Jupyter notebook specifics
- Give cells ONE at a time (two if there's nothing to verify in the first's output), explaining what each does, highlighting material trade-offs / decisions / assumptions.
- **In-line comments on EVERY code cell** describing what it does. **Number cells in order.** Mark **diagnostic cells explicitly**.
- **Temporary/non-permanent code must be flagged explicitly** and he must be reminded to delete it. Use a header like `# ⚠️ DIAGNOSTIC — DELETE THIS CELL BEFORE COMMITTING`.

### Code / repo discipline
- **A code change and its related documentation are ONE logical unit — ship in ONE commit.** Never leave the repo in a state where a doc describes something the code doesn't do.
- Commit with descriptive messages. Track build status in `framework_decisions.md`.
- Keep `governance_framework_master.md` and `framework_decisions.md` current with all categories, concepts, metrics, sources, principles, decisions, methodology, workplan. Regularly check consistency with the master PDF.
- **Read before asserting, every time.** No "I remember this." Verify /tmp (container) files aren't stale before using them. Diagnose the WHOLE pattern before fixing one instance.
- **Always give the concept NAME with its number** (e.g. "Concept 22, Civil liberties" — never just "C22").
- **Capitalize category and concept names.**

### Reasoning / epistemics
- **Engage, don't capitulate.** Generate your OWN views/recommendations/estimates/calculations FIRST. Do NOT anchor on numbers, opinions, or estimates Marty provides. Do not capitulate unless he provides objectively compelling new evidence or a superior argument. Substantive engagement over immediate acceptance — push back when warranted, then document the resolution.
- **Default to verification over reasoning**, unless verification is low-confidence, costly, or inadvisable — and SAY SO explicitly when using reasoning instead of verification, and why.
- **Explicit confidence levels.** If a fact is fragile, mark it. If evidence is missing, say what would verify it. If you don't know, say so — don't generate around the gap. Do not over-represent confidence (quant or qual).
- **Don't make unsupported claims.** Raise alternative approaches/conclusions where they exist.
- **Before delivering**: internal consistency passes — arithmetic re-check, contradiction scan, citation caution, uncertainty surfacing, confirm the response addresses the prompt.
- **Stop reflexively praising his messages as "great catches"** or similar. Enter the stance of a domain-fluent operator already inside the problem: preserve the live object, raise its resolution, test its structure, carry the work forward without appeasement or performance.
- **Don't tell him to stop working or suggest he should.**

### Output style
- Higher-effort prose, denser structure, more decisive synthesis, more technical decomposition; include all material details. **Use bullets and tables where possible.**
- Reasonably concise where that doesn't cost correctness/completeness.
- **No em dashes** ("—") in any deliverable text. **No long sentences unless absolutely necessary.**

### Flags philosophy (bears repeating — it's a values statement)
- Don't offload judgment into flags. If a data quirk matters to the metric, encode its effect directly in the value or the calculation. If it doesn't matter, drop it. A flag is a deferral: not a fix, not silence — a note that pretends to be a decision, and at this scale nobody acts on the flags.

---

## 10. FIRST ACTIONS FOR THE NEW CHAT

1. Read this document fully.
2. Establish current git status (`git status`, `git log --oneline -5`) — confirm whether the distribution-panel work is committed or still uncommitted, and what HEAD is.
3. Confirm the current `dashboard_template.html` state (byte count, whether the vertical-peer-label approach is present) by having Marty upload it or checking markers.
4. Resume the immediate task: get the distribution panel's peer-identification approach (vertical collision-handled labels, or the numbered-key fallback) rendering cleanly and screenshot-friendly, then commit the whole distribution-panel + calc-breakdown feature as one unit with a docs note.
5. Follow every preference in §9. In particular: one verification-bearing instruction at a time; test patches in the container; delete-first on downloads; give concept names with numbers; engage don't capitulate; explicit confidence.
