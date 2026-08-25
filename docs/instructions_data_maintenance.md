# Data Maintenance Instructions

**As-of date (last manually updated):** 2026-07-09
**⚠️ MANUAL SNAPSHOT:** This document is maintained by hand and does NOT auto-update. Source categories, URLs, version labels, and per-source steps below were accurate as of the date above. When sources change their access methods or a new vintage is released, this document must be updated manually. Any place where a value must be hand-edited on update is flagged inline with **MANUAL UPDATE**.

This document contains instructions for setting up the project on a new machine, and for maintaining and updating data sources.

---

## Machine Setup

### First-time setup on a new machine

1. Clone the repo:
   `git clone https://github.com/mjboulanger/governance-framework.git`

2. Navigate to the project folder:
   - **Mac:** `cd ~/Documents/governance-framework`
   - **Windows:** `cd C:\Users\{username}\governance-framework`

3. Create conda environment:
   `conda env create -f environment.yml`
   `conda activate governance-framework`

4. Create a `.env` file in the project root with machine-specific paths and credentials.
   **On Windows, create it with ASCII encoding to avoid a BOM that breaks parsing:**
   ```powershell
   Set-Content -Path .env -Encoding ascii -Value "PROJECT_ROOT=C:\Users\{username}\governance-framework`nDOWNLOADS_DIR=C:\Users\{username}\Downloads`nACLED_EMAIL=your_acled_email`nACLED_PASSWORD=your_acled_password"
   ```
   **On Mac:**
   ```
   PROJECT_ROOT=/Users/{username}/Documents/governance-framework
   DOWNLOADS_DIR=/Users/{username}/Downloads
   ACLED_EMAIL=your_acled_email
   ACLED_PASSWORD=your_acled_password
   ```

5. Install python-dotenv if missing: `pip install python-dotenv`

6. Register the Jupyter kernel:
   `python -m ipykernel install --user --name governance-framework --display-name "governance-framework"`

7. **Windows only — SSL / certificate fix** (`sitecustomize.py`). Under OpenSSL 3.0.21+ Python crashes with `ssl.SSLError: [ASN1: NOT_ENOUGH_DATA]` when loading the Windows cert store, which blocks JupyterLab and all HTTPS calls (full cause in the troubleshooting note under **Notes**). Create a `sitecustomize.py` in the env's site-packages so Python loads CA certs from certifi via the working `cafile=` path:
   ```powershell
   python -c "import certifi; print(certifi.where())"
   notepad "$env:CONDA_PREFIX\Lib\site-packages\sitecustomize.py"
   ```
   Paste this, save, close:
   ```python
   # CPython #151504 workaround: OpenSSL 3.0.21+ breaks Windows-store cert load via cadata=.
   # Load CA certs from certifi via the working cafile= path instead. Full verification preserved.
   import ssl as _ssl
   import certifi as _certifi
   _orig = _ssl.SSLContext.load_default_certs
   def _load_default_certs(self, purpose=_ssl.Purpose.SERVER_AUTH):
       try:
           self.load_verify_locations(cafile=_certifi.where())
       except Exception:
           try: _orig(self, purpose)
           except Exception: pass
   _ssl.SSLContext.load_default_certs = _load_default_certs
   ```
   Verify: `python -c "import ssl; ssl.create_default_context(); print('SSL OK')"` should print `SSL OK`. Auto-loads every session, survives restarts, no admin needed. Remove the file once CPython/conda ship the upstream fix. (Not needed on Mac unless the same error appears — see Notes.)

   *Prior approach (still relevant for OTHER SSL errors, but does NOT fix this one):* setting `SSL_CERT_FILE` to the certifi path (`setx SSL_CERT_FILE "<certifi-path>"`, new window) points cert-consuming libraries (requests, urllib3) at certifi and resolves cert-source problems there. It does **not** fix the `create_default_context` / JupyterLab crash, because `load_default_certs()` reads the Windows store regardless of `SSL_CERT_FILE`. Keep it as a first thing to try for SSL errors that are *not* the `ASN1: NOT_ENOUGH_DATA` / `create_default_context` failure.

8. Launch JupyterLab: `jupyter lab`

### Notes
- The `.env` file is machine-specific and not tracked by git — each machine needs its own
- `data/raw/` is not tracked by git — re-run pipelines to regenerate
- `data/processed/` is tracked by git and available immediately after cloning
- GitHub is the sync mechanism between machines. Keep the project OUTSIDE OneDrive (git corruption risk)
- **SSL `ASN1: NOT_ENOUGH_DATA` troubleshooting (env fix in setup step 7).** Symptom: `jupyter lab` or any HTTPS call crashes with `ssl.SSLError: [ASN1: NOT_ENOUGH_DATA]`, traceback ending in `_load_windows_store_certs` → `load_verify_locations(cadata=certs)` inside `create_default_context()`. **Cause (confirmed):** CPython bug #151504 — OpenSSL 3.0.21+ (CVE-2026-34180 ASN.1 hardening) changed the internal code returned at end-of-cert-buffer; Python's `_ssl` treats that normal end-of-buffer as fatal, breaking the Windows-store load (passed as `cadata=` bytes). **Not** a corrupt certificate and **not** a conda problem. Downgrading OpenSSL does **not** help (both 3.5.x and 3.6.x carry the change). The `cafile=` path is unaffected — only `cadata=` (the Windows-store path) is broken; that is why the step-7 `sitecustomize.py` (forcing `cafile=`) resolves it. **Cross-machine caveat (honest limits):** the underlying bug is cross-platform (any Python built against OpenSSL 3.0.21+), but it manifests through `_load_windows_store_certs`, the **Windows** cert path. macOS/Linux use different default-cert mechanisms, so whether the Mac env hits the *same* crash is **unverified as of 2026-07-21** — it may not, or may fail differently. If the Mac (or any machine) shows the same error, the same `sitecustomize.py` applies (the override is generic), path adjusted to that env's site-packages. If no SSL error appears there, no action needed. First encountered and fixed on the Windows PC, 2026-07-21.

---

## Peer groups (country comparison sets)

Each country has a default peer group (~10 countries) used by the dashboard's compare
view. These are generated by `src/build_peers.py` into `data/processed/country_peers.csv`
(tracked). Peers are selected by a similarity score (lower = closer); the top 10 become the default set:

- **GDP per capita (USD nominal)** - the primary axis. Distance uses a **dead zone**: countries
  within ~15% income of the focus are treated as equal (income within ~$1-2K at middle-income
  levels is not a meaningful tier difference), and distance beyond the dead zone is **concave**
  (square-root) so genuine tier gaps still count but small differences do not dominate.
- **Region** - a soft lean toward same/near region (penalty 0.10 near, 0.22 far; not a hard
  filter, so income-similar countries from other regions still appear - e.g. Australia is a US peer).
- **Population** - a soft lean toward similar-size countries (log-distance x 0.13, capped 0.55),
  so large economies are not matched only to tiny income-twins.

The exact weights are constants at the top of `build_peers.py` (INCOME_DEADZONE, INCOME_SQRT_SCALE,
region penalties, SIZE_SCALE, SIZE_CAP) - adjust there to retune.

Excluded as peers: territories, countries without GDP/capita, micro-states (population
< 1,000,000), and low-coverage countries (< 110 distinct metrics) - unless the whole
income-neighbourhood is data-thin (e.g. Sub-Saharan Africa), where the coverage filter
relaxes so a country still gets a sensible regional set.

**To regenerate:** `python src/build_peers.py` (re-run after score/coverage/WDI updates).

**To override a country's peers by hand:** edit its row in `data/processed/country_peers.csv`
(the `peers` column is a comma-separated list of ISO3 codes). Hand edits persist until the
next `build_peers.py` run overwrites them - so record any permanent overrides, or adjust the
parameters at the top of `build_peers.py` (N_PEERS, COV_FLOOR, POP_FLOOR, size weight) instead.

The dashboard data layer (`build_dashboard_data.py`) reads `country_peers.csv` and attaches
each country's peer list to the JSON, so regenerate the data layer after changing peers.

## Metric display names

Human-readable metric names live in `data/reference/metric_labels.csv` (columns: `metric`,
`source_label`, `metric_name`). The dashboard data layer joins this in and shows each metric as
`Metric name (Source)` (e.g. "Homicide rate (UNODC)"). This file is the canonical source of
metric display names - edit it to rename a metric or change a source label, then rebuild the
dashboard data layer. It is hand-maintained (not generated); every metric in
`concept_contributions.csv` should have a row here.

## Building the dashboard

The HTML dashboard is generated from the processed data and a template. Two build
artifacts are **gitignored** (regenerable, large): `dashboard/dashboard_data.json`
(~6MB) and `dashboard/governance_map.html` (~11MB). Everything needed to regenerate them
is tracked. From a fresh clone, run two commands in order:

```bash
python src/build_dashboard_data.py    # reads data/processed/*.csv -> dashboard/dashboard_data.json
python src/build_dashboard.py         # inlines the JSON + Plotly into the template -> dashboard/governance_map.html
```

- **`src/build_dashboard_data.py`** reads the current score/history/momentum/contribution/
  coverage CSVs plus labels (`concept_sources.py`, `metric_dictionary.py`) and writes one
  compact `dashboard_data.json`. Re-run it after any score/data regeneration. It additionally
  reads `data/processed/metric_normalization_params.csv` (per-metric method, baseline params, and
  harmonize rule) into `meta.metrics`, and the latest-year `raw_value` per (country, metric) from
  `data/processed/normalized_panel.csv`, attaching each to the contribution rows. These feed the
  metric-level calculation breakdown (see below); if either file is missing, those fields are
  omitted and the metric breakdown shows the method in words without the arithmetic. No new manual
  input: method, params, and raw values all come from the data.
- **`src/build_dashboard.py`** reads `dashboard/dashboard_template.html` (tracked - the UI),
  inlines the real `dashboard_data.json` and the Plotly JS bundle, and writes the
  self-contained `dashboard/governance_map.html`. It opens offline on `file://` (no internet),
  which is the target for restricted environments.
- **Dependency:** the `plotly` Python package supplies the inlined JS
  (`plotly.offline.get_plotlyjs()`); it is in the `governance-framework` conda env. No
  separate Plotly download is needed.
- To change the UI, edit `dashboard/dashboard_template.html` (tracked) and re-run
  `build_dashboard.py`. The template carries a small embedded sample dataset so it can be
  opened directly during development (with internet, for the CDN Plotly); the build step
  replaces that sample with the full data and inlines Plotly for the shippable file.

## Drill-down contribution decomposition

The drill-down shows two kinds of bar per row, which use **different references on purpose**:

- **Position bars ("vs universe" / "vs median")** show where the country sits in the sovereign
  distribution. They are scaled to the **p05-p95** span (so tail values stay distinguishable
  rather than clamping at the quartiles) with tick marks at **p25/p50/p75**. Reference = the
  sovereign **median**. This answers "where does this country rank".

- **Contribution bars ("contribution to category")** show each item's signed contribution to
  the category score, defined as:

  > contribution = (canonical weight) x (item value - sovereign **mean** for that item)

  Metric bars use `renormalized_weight` (from `concept_contributions.csv`); concept bars use the
  concept's **weight share** of its category, derived from `effective_weight`
  (`concept_attribution.csv`). **Weights are read from the pipeline outputs, never redefined in
  the dashboard layer.** Both columns are shown on **one shared scale** (contribution to
  category), so a metric bar and a concept bar are directly comparable across the screen. Warm
  bars pull the category score down; cool bars lift it.

**Why the mean (not the median) for contributions.** The mean chains additively
(metric -> concept -> category): a concept's contribution equals the sum of its metrics'
contributions, so the levels reconcile on one scale. The median does not chain (a country at the
concept median is not the sum of metrics at their metric medians), which is why position bars
(rank) use the median but contribution bars (decomposition) use the mean.

**Known limitation.** The additive chaining is exact for most (country, concept) pairs (median
residual ~0.001, 95th percentile ~0.007) but has a thin tail (up to ~0.1) concentrated where a
concept has heavy **per-country metric missingness** (renormalized weights then diverge from the
sovereign-mean profile). This residual is accepted for the drill-down as a visual aid.

**Reference toggle (World / Peers).** The drill-down has a World/Peers toggle (right of the
country selector). In **World** mode the reference is the sovereign mean (contributions) and
sovereign median (position). In **Peers** mode the reference shifts to the country's peer group:
contribution bars use the **peer mean**, position bars center on the **peer median**, and the
category-column driver call-outs rank by deviation from the peer reference. Because the
decomposition is `weight x (focus - reference)`, swapping the reference keeps the chaining intact
(verified: peer contributions chain metric -> concept -> category with the same residual profile
as the world reference).

**Scale stays universe-anchored in Peers mode.** Only the *reference point* shifts to the peers;
the *bar-length scale* remains the overall-universe scale (world contribution range for
contribution bars, world p05-p95 for position bars). Peers are similar to the focus country, so a
peer-spread scale would amplify tiny differences into long bars; keeping the universe scale means
a small gap versus similar peers stays a short bar. The on-screen note states this explicitly.

**Peer contributions are computed live in the display layer, by design.** Fixed-reference
derivations (scores, weights, world contributions) are computed once in the pipeline. But the peer
set is **user-editable** (see below), so peer contributions depend on live UI state and *cannot*
be precomputed. They are therefore computed in JS from **canonical primitives**: the peer
reference is just the average of the peers' own concept scores / category scores / metric values
(read from the JSON), and the contribution is `focus weight x (focus value - peer average)` using
the **focus country's** canonical weights. Peers contribute only their averaged scores as
reference points; all attribution is a focus-country operation. The one field the pipeline exposes
for this is the concept **weight share** (`ws` in each concept record of the JSON), so JS never
recomputes a weight. This is the minimum computation that must live in the display layer; nothing
else about peers is derived there.

**Editable, cross-screen peer set.** The peer chips shown under the toggle (Peers mode only) are
editable: remove a peer with its x, add one via "+ Add". Edits mutate the shared `activePeers`
state, which is the *same* state the map screen's compare mode uses - so a peer edit on either
screen is reflected on the other. Changing the focus country reseeds `activePeers` to that
country's default peers. If a country has no peer group (territories, micro-states), the Peers
button is disabled and a note explains why. The reseed fires on every focus-change path (either
country dropdown, clicking the map, or clicking a "Similar countries" row), and switching to the
map re-renders its panel so a peer edit made on the drill-down is reflected there; turning on
Compare no longer resets existing edits.

**Rebuild reminder.** Percentile/contribution changes live in `build_dashboard_data.py`, so after
editing it you must re-run **both** steps (`build_dashboard_data.py` then `build_dashboard.py`) -
rebuilding only the second step reuses the stale JSON.

## Distribution panel and calculation breakdown

Clicking any category, concept, or metric row in the drill-down opens a right-hand panel with two parts.

**Distribution histogram.** A real binned histogram (~24 bins, no smoothing) of that item's values across the 192 sovereigns, with the focus country marked (an orange line) and quartile ticks (p25/p50/p75, dotted). In Peers mode the peers are marked as teal lines, each with a clickable dot at the top. Colours are deliberate and shared with the rest of the UI: focus = the negative-callout orange (the `.dn` colour, `rgb(201,106,74)`); peers = teal (`--radar-fill`, `#2f8f9e`).

**Peer identification (screenshot-safe).** Peer lines carry no label by default. Click a peer's dot to pin its country name as a horizontal label at the top (like the focus label); click again to remove it. Hovering a dot previews the name and value. A "Show all peer names" button lists every peer vertically along the bottom axis (the compact way to show ten at once), with a bounded left/right nudge so crowded names stay legible; at high peer density some overlap remains by design. The panel height is content-sized: it grows only enough to fit the longest visible name, so there is no empty band when names are hidden.

**Calculation breakdown ("how this score is built").** Drills exactly one level down. Category -> a weighted table of its concepts (score, weight share, contribution). Concept -> a weighted table of its metrics (harmonized value, weight, contribution). Metric -> a "Metric definition" header, the definition and scale/source, then the raw -> harmonized arithmetic for the metric's method family (z-score, log1p z-score, percentile, or binary), reproducing the harmonized value from the raw value. This is what the two extra data-layer reads (under "Building the dashboard") exist for. Concepts have no definition field in the data, so the definition header appears only at the metric level.

**Screenshot-standalone principle (project-wide).** Charts are built to be lifted out and dropped into other materials. The chart plus its caption note is the exportable artifact; anything purely tool UI (buttons, click/hover hints, interaction affordances) is kept OUTSIDE that region so it never lands in a screenshot. Data that a click pins (a peer name, the focus label) is part of the chart and belongs in the shot; the control that produces it does not. The "Show all peer names" button and its hint therefore sit below the caption note, between the note and the methodology section. Apply this rule to any new chart or panel.

---

## Documentation tab

The Documentation tab is a reader-facing summary of the framework, generated from the data so it cannot drift from what is scored. It has no hand-maintained content except where noted below.

**Structure and sources.**

- The Category -> Concept -> Metric hierarchy table, the per-entity sections, the stable anchor ids (`doc-cat-*`, `doc-concept-*`, `doc-metric-*`), the left contents nav, and the scroll-spy highlighting are all built in `renderDocs` from `DATA.meta` and `DATA.contributions`. No entity list is hand-authored.
- **Concept weights** shown in parentheses next to each concept name are the canonical `effective_weight` (relevance x measurement-quality), read straight from `data/processed/concept_weights.csv` by `build_dashboard_data.py` into `meta.concepts[cid].w`. No share or derived figure is recomputed; the value is emitted as-is (1.0 for 21 of 24 concepts; C9 = 0.75, C11 / C12 = 0.5).
- **Concept descriptions** are parsed at build time from the master doc: `build_dashboard_data.py` reads each `### Concept N:` section's `**Scope:**` line out of `docs/governance_framework_master.md` and emits it as `meta.concepts[cid].desc` (bold markers stripped). Single source: edit the Scope line in the master, rebuild, and the tab updates. Categories carry no description because the master defines none.
- **Metric definitions and source labels** come from `meta.metrics[m].def` / `.src`, already emitted for the calculation breakdown.
- **Metric tiers.** P1 = primary (the workhorse metric, most direct and central), P2 = primary supporting, Sp = supplementary. Tier weights are fixed (LOCKED, `metric_methodology.md` S6): **P1 = 1.0, P2 = 0.5, Sp = 0** (supplementary is shown but not scored by default), equal-weighted within a tier and renormalized over the metrics present. The Documentation tab shows these weights in a block below the hierarchy table, and a tier legend also appears on the drill-down page whenever a concept is open.

**No new manual input.** Nothing on this tab requires hard-coding for ongoing updates: the hierarchy, weights, descriptions, and definitions all derive from the data and the master doc.

**Layout note.** On the drill-down page the three columns scroll horizontally within their own region (`.drill-cols { overflow-x: auto }`) rather than colliding with the distribution panel when the window is too narrow to fit both.

**Deferred to post-v1** (tracked in `docs/dashboard_worklist.md`): per-metric source links (need a `url` column added to `source_registry.csv` plus a clean metric-to-source join), and human-readable rewrites of the concept descriptions (currently the master's internal `Scope` notes) plus category descriptions.

---

## Time series tab

The Time series tab plots governance scores over time (2005 to 2026). It is built by `renderTimeseries` in the template entirely from `DATA.history` (category and concept trajectories, each year scored on the fixed current baseline). No pipeline change was needed; the history is already emitted by `build_dashboard_data.py`.

**Two modes.**

- **Profile** (View = "All categories"): the focus country's five category lines.
- **Single item** (View = a category or a concept): the focus country's line over the universe distribution, shown as shaded 5 to 95th and 25 to 75th percentile bands with a dotted median. The bands are computed client-side per year across all sovereigns scored that year (`tsUniverse`, cached per item), so the denominator shifts as coverage grows; the per-year country count appears in the median hover.

**Peers.** A "Show peers" button overlays the peer set on the single-item chart (the bands stay on). The peer set is `activePeers`, shared with the map and drill-down in both directions: changing the focus country reseeds peers, and editing peers here carries across pages. Clicking a peer chip highlights that peer's line and pins its name at the right edge. Focus is drawn in the distribution's orange, peers in teal, matching the drill-down convention.

**Score composition.** Below the chart, "How this score is built" reuses the drill-down's `renderCalc` via its `boxId` parameter (rendering into `tscalc`), so the two pages cannot drift. It is latest-observation only (the full series is the chart above) and labelled as such, and carries a "View in documentation" link.

**Cross-links.** The drill-down calc panel has a "View time series" link (via `openTimeseries`) that switches to this tab, sets the View dropdown, and renders for the current focus country: a category opens its category series, a concept its concept series, and a metric falls back to its parent concept.

**No new manual input.** Everything derives from `DATA.history` and the shared state; nothing requires hard-coding for ongoing updates.

**Metric-level time series is deliberately absent.** The dashboard inlines only latest-year metric values (into `contributions`), not per-year metric history; that lives in `normalized_panel.csv` (about 80MB), which is not inlined. A metric's line and its universe band therefore have no data source in the browser. Adding it would need a pipeline emit and would add several MB to the distributed file. Tracked in `docs/dashboard_worklist.md`.

---

## Data Update Instructions

Run `print_stale_sources()` from `src/download_log.py` to identify sources needing refresh.
Attempt and success dates for each source are recorded in `data/raw/download_log.csv`.

For each source, the pipeline derives the data "as-of" date from the data or filename — not hardcoded. The only manual inputs required on update are flagged per-source below under **MANUAL UPDATE**.

**`download_log.data_as_of_date` now dates cross-sectional metrics in the scoring panel [2026-07-24].** The normalization step (`src/build_normalized_panel.py`, methodology §5) reads `data_as_of_date` from `data/raw/download_log.csv` to stamp the panel year of the four scored sources that carry **no `year` column** (WB_BRSS, CPJ, RTI_RATING, TI_POLFINANCE). The code parses the leading 4-digit year from that field, so any format works (`2016`, `2026-06`, or free-text like `2016 (BRSS 5th wave...)`). This is data-driven: when a pipeline re-fetches one of these sources and updates the log, the panel year follows automatically with no code change. **What to keep current:** ensure a re-fetch of any of these four updates its `data_as_of_date` in the log. The one that will NOT auto-move is **WB_BRSS**; it is a frozen 2016-reference wave, so its `data_as_of_date` stays `2016` until a 6th BRSS wave is released (see the WB_BRSS per-source note); this is a deliberate fixed value, not a stale one. If a year-less source is ever added without a log entry, the panel build raises `no download_log vintage for year-less source ...` rather than silently stamping the current year. Fill its `data_as_of_date` to resolve. **Note:** `data/processed/normalized_panel.csv` (~56MB) is a **regenerable build artifact and is git-ignored** (not committed); it is the deterministic output of `python3 src/build_normalized_panel.py` from the committed clean source files, profile, and tags. Regenerate it after any change to a source file, a metric's `final_method`, a direction, or a missingness tag. The reproducibility guarantee lives in the committed inputs + code, not the file.

---

## Source status, access method and update frequency

The per-source build status, access method, update frequency, coverage and `data_as_of_date` are **not maintained here**. They live in two places that are authoritative:

- **`data/processed/source_registry.csv`** — written by each pipeline at build time (`source_id`, `access_method`, `python_approach`, `update_frequency`, `coverage_countries`, `coverage_years`, `highest_tier`, `category`, `tier`, `data_as_of_date`, `coverage`, `notes`). This is the build-truth record; see the Source Registry Architecture section of `framework_decisions.md` for how it is written and why the notebook seed list diverges from it.
- **`docs/framework_decisions.md`** — the Consolidated Build Status table (by source) and the Build-Status by Concept audit, for a human-readable at-a-glance view.

*A hand-maintained copy of that information used to sit here as six "Category 1-6" tables. It drifted out of date (built pipelines still listed as pending, dropped sources still listed as pending) because it duplicated a generated artifact, so it was removed 2026-07-24. To find which sources need a refresh, run `print_stale_sources()` from `src/download_log.py`.*

**Access-category vocabulary** (used throughout `framework_decisions.md` and the per-source sections below; the `category` column in `source_registry.csv` carries it per source):
- **Category 1** — PDF extraction (most manual; narrative reports with no structured dataset).
- **Category 2** — email / form-gated download.
- **Category 3** — web scrape.
- **Category 4** — manual download of a structured file (regular cadence).
- **Category 5** — manual download, irregular / no cadence.
- **Category 6** — automated (API or direct download); no action needed unless the pipeline fails.

## Per-Source Instructions

Only sources requiring manual action are listed. Automated sources need no action unless the pipeline fails (fallback notes in source technical notes).

### VDEM — V-Dem Full+Others
**On each update:**
1. Go to: https://www.v-dem.net/data/the-v-dem-dataset/
2. Download "Country-Year: V-Dem Full+Others" (latest version), CSV, email required
3. Save to Downloads folder
4. **MANUAL UPDATE:** set `VDEM_VERSION` in `notebooks/exploration/03_vdem_pipeline.ipynb` to the new version number (e.g. the next integer)
5. Re-run the notebook

### IDEA_PARTIP — IDEA Global State of Democracy
**On each update:**
1. Go to: https://www.idea.int/democracytracker/gsod-indices
2. Download the CSV version
3. Save to Downloads folder (replacing any older copy)
4. Re-run `notebooks/exploration/23_idea_partip_pipeline.ipynb` — version is auto-detected from the filename; no manual edit needed

### PEW_GRI — Pew Global Restrictions on Religion
**On each update:**
1. Log in (free account) at pewresearch.org and find the Global Restrictions on Religion dataset
2. Download the ZIP
3. Save to Downloads folder (replacing any older copy)
4. Re-run `notebooks/exploration/24_pew_gri_pipeline.ipynb` — ZIP and CSV auto-detected; no manual edit needed

### IMF_FISCAL_RULES — IMF Fiscal Rules Database
**On each update:**
1. Go to: https://www.imf.org/en/topics/fiscal-policies/fiscal-rules-dataset
2. Download the Excel dataset
3. Save to Downloads folder (replacing any older copy)
4. Re-run `notebooks/exploration/25_imf_fiscal_rules_pipeline.ipynb` — file auto-detected by glob; columns selected by name. If the IMF restructures the sheet and a column section is renamed, the name-based selector will raise a clear error identifying the missing fragment — update the `col_spec` fragments in that case (this is the only manual intervention, and only on a template change)

### CLIMATE_LAWS — LSE Grantham / Climate Policy Radar
**On each update:**
1. Go to: https://climate-laws.org and complete the data download request form (free)
2. Download the CSV (delivered via link)
3. Save to Downloads folder (replacing any older copy)
4. Re-run `notebooks/exploration/26_climate_laws_pipeline.ipynb` — auto-detects Document_Data_Download*.csv by glob; no manual edit needed

### ODIN — Open Data Inventory
**On each update:**
1. Go to: https://odin.opendatawatch.com/data
2. Download complete data (delivered as a ZIP of per-year Excel files)
3. Save to Downloads folder (replacing any older copy). **Keep only the current ODIN ZIP in Downloads** — the pipeline globs *data*.zip and validates by contents, so a stale ODIN ZIP could be ambiguous.
4. Re-run `notebooks/exploration/27_odin_pipeline.ipynb` — auto-detects the ZIP, stacks per-edition Excels; no manual edit needed

### IRENA_POLICY — DEPRIORITIZED (not built)
No clean downloadable renewable-policy dataset exists. The IRENA "Stats Tool" .xlsb is renewable STATISTICS (capacity/generation/finance), not policy. IRENA's renewable-policy work is report-based analysis. The only structured renewable-policy data is the joint IEA/IRENA Policies & Measures DB (api.iea.org/policies?csv=true), which has no clean renewable filter and would duplicate Climate Laws. DEFERRED: IRENA national renewable-energy TARGETS via the planned PDF-extraction infrastructure.

### WB_CARBON — World Bank Carbon Pricing Dashboard
**Normally:** No action required — fully automated (auto-detects latest month-stamped xlsx).
**MANUAL UPDATE only when:** (a) a new SOVEREIGN country adopts carbon pricing — add it to the national-name→ISO3 dict in `20_wb_carbon_pipeline.ipynb` (the pipeline prints unmapped jurisdictions to catch this); (b) EU/EEA ETS membership changes — update the EU27+ member list in the same cell.
**If the dashboard download fails** (rate-limited or moved): wait and re-run; if the URL pattern changed, find the current xlsx at https://carbonpricingdashboard.worldbank.org and update the base path.

### TI_POLFINANCE — Political Finance (International IDEA)
**Normally:** No action required — fully automated. The pipeline downloads the IDEA Political Finance Database directly via its .xlsx export endpoint (`idea.int/data-tools/export?type=region_only&themeId=302&world=all`) and validates the response is a spreadsheet.
**Note on source naming:** the source ID is TI_POLFINANCE for continuity, but the data is from International IDEA (the authoritative structured source), not Transparency International.
**MANUAL UPDATE only when:** IDEA revises its question set (last revised 2022). The pipeline scores a hand-curated list of 20 directionally-defensible binary questions (see `29_polfinance_pipeline.ipynb` INCLUDED_QUESTIONS and the rationale in framework_decisions.md). If IDEA renumbers or changes questions, revisit that inclusion list — the pipeline asserts each included question resolves to exactly one column and will raise loudly if the schema shifts.
**Scope reminder:** de jure regulation only (rules on paper, not enforcement/compliance/actual money).

### IMF_AREAER — FARI capital-account restrictiveness (MANUAL)
**MANUAL SNAPSHOT — does not auto-update.** The portal (elibrary-areaer.imf.org) is WAF-blocked to programmatic access and JS-gated, so the data MUST be exported by hand.
**To refresh (MANUAL UPDATE, each cycle):**
1. Go to https://www.elibrary-areaer.imf.org/ → **Indices** tab.
2. Select **FARI Aggregate** and the **FARI - FDI** family (Aggregate + Inflow + Outflow for each), **all countries**, **annual** frequency, full year range.
3. Download to your Downloads folder (it saves as `FARIReportByCountry_<date>.xlsx`).
4. (Optional) Also export the ACI report if a policy-trajectory dimension is ever added — currently NOT used.
5. Run notebook 32_areaer_fari_pipeline.ipynb — it auto-detects the latest `FARIReportByCountry*.xlsx` in Downloads (prefix match, ignores the date suffix), drops footnote rows, reshapes wide→long, maps to ISO3.
**MANUAL UPDATE — ISO3:** if the pipeline prints any unmapped country names, add them to the MANUAL_ISO3 dict in the notebook (IMF uses quirky names; note it uses a CURLY apostrophe in "Côte d'Ivoire").
**If the portal hangs on a large export:** narrow to FARI-only / annual, or export in year-chunks; the pipeline tolerates a single combined file.
**Caveats:** latest year (currently 2024) is PARTIAL per source footnote. Values are 0-1, higher = MORE restrictive. Complemented by Chinn-Ito (automated) and Reinhart-Rogoff (de facto regime).

### CHINN_ITO — Chinn-Ito Index (KAOPEN), capital-account openness
**Normally:** No action required — fully automated. `31_chinn_ito_pipeline.ipynb` scrapes the faculty page (web.pdx.edu/~ito/Chinn-Ito_website.htm) for the newest `kaopen_YYYY.xls`, parses the year from the link (no hardcoded year), downloads to `data/raw/`, and reads it with the `xlrd` engine.
**Dependency:** needs `xlrd` in the env (legacy `.xls`; openpyxl cannot read it). Install via `conda install -c conda-forge xlrd`. **MANUAL UPDATE:** ensure `xlrd` is listed in `environment.yml` so a fresh clone picks it up.
**MANUAL UPDATE — fragile URL fallback:** if discovery raises "No kaopen_YYYY.xls link found", the personal faculty page was restructured or moved. Fallback: (1) find the current Chinn-Ito page/file (search "Chinn-Ito index"); (2) if the page URL moved, update `PAGE_URL` in the notebook; (3) if the file-naming pattern changed, update the `kaopen_(\d{4})\.xls` regex; (4) last resort — download `kaopen_<latest>.xls` by hand into `data/raw/` and skip the discovery + download cells.
**MANUAL UPDATE — legacy ISO3:** if the "Non-standard ISO3 remaining" print shows anything besides `['ANT']`, add a mapping to the `LEGACY_ISO3` dict in the notebook (an old code → its current ISO3) and re-run.
**Caveats:** `kaopen` higher = MORE open — **OPPOSITE sign to AREAER FARI** (invert one before any cross-check). Version non-stable: each release recomputes the PCA over the whole sample, so the pipeline FULL-REPLACES on every run (never append). Data-year Y = AREAER report (Y+1) = end-of-Y status.

### RTI_RATING — Global RTI Rating (CLD / Access Info Europe)
**Normally:** No action required — fully automated. The pipeline parses the full scores table directly from rti-rating.org/country-data via pandas.read_html, and fetches the no-law deficit list from a URL it extracts dynamically from the page (so the date in that filename never needs hand-editing).
**MANUAL UPDATE only when:** a new country appears that pycountry can't map — the pipeline prints any unmapped country names; add them to the MANUAL_ISO3 dict in 30_rti_rating_pipeline.ipynb. (Applies to both the rated table and the deficit list.)
**Scope reminder:** de jure legal-framework strength only (not implementation). No-law countries are floored at min−1SD (clamped ≥0) with has_rti_law=0 — a documented scoring choice, see framework_decisions.md.
**If read_html finds 0 tables or the wrong shape:** the page structure changed — inspect rti-rating.org/country-data and adjust the parse.

### PEFA — Public Expenditure and Financial Accountability (PFM)
**Manual download of a STRUCTURED file (not PDF).** PEFA's "Scores Downloads" page exports A–D indicator/dimension scores as a CSV — no parsing needed.
**To refresh (MANUAL UPDATE, each cycle):**
1. Go to https://www.pefa.org/assessments/batch-downloads ("Scores Downloads").
2. Set **Framework = 2016**, **Type = National**, **Status = Final**. (Framework is single-select; to also pull 2011 for a future backfill, download it as a separate file — the pipeline ingests every `assessments_*.csv` in Downloads.)
3. Click **Download** — it saves as `assessments_<unixtime>.csv` in Downloads.
4. **Clear any old `assessments_*.csv` from Downloads first** — the pipeline globs ALL of them and concatenates (dedup-to-latest mitigates, but cleanliness is safer).
5. Run `33_pefa_pipeline.ipynb` — auto-detects the file(s), snapshots to `data/raw/pefa_assessments_raw.csv`, filters to framework + national, dedups to latest per country, maps A–D→numeric, writes `pefa_clean.csv`.
**MANUAL UPDATE — framework version:** the single knob is `PEFA_FRAMEWORK` (Cell 2), currently `"2016"`. Change only to adopt a new national framework version as the core — a deliberate SCOPE choice that cannot be auto-derived.
**MANUAL UPDATE — ISO3:** if the notebook prints unmapped country names, add them to the `OVERRIDES` dict (Cell 4).
**Scope/caveats:** core = 2016 framework, national, latest per country (~85 countries, 2017–2026). Subnational entities ("Country - Subentity") auto-excluded. 2011 backfill deferred (stale — see framework_decisions.md). `data_as_of` auto-derived from max assessment year (no hardcode).

### OECD_TFI — OECD Trade Facilitation Indicators
Manual export. Compare Your Country tool (https://www.compareyourcountry.org/trade-facilitation) — robots-blocked, no API/batch. Overview → Change view (table) → download selection gives the composite-average export (`exportedData.xlsx`, ~164 countries, years 2017/2019/2022) to Downloads. Re-run `notebooks/exploration/34_tfi_pipeline.ipynb` — auto-detects `exportedData*.xlsx` by glob, derives latest year + download date from the sheet. Composite level only (A–K sub-indicators not exported; future enhancement).

### FATF — Mutual Evaluation Ratings (AML/CFT, Concept 9) (MANUAL — Cloudflare-gated)
The fatf-gafi.org site is behind Cloudflare's anti-bot challenge, so the files **cannot** be fetched by `curl`/`requests`/the pipeline — they must be downloaded by a real browser. A scripted download returns a ~5 KB "Just a moment..." HTML stub instead of the file.
1. In a browser, go to: https://www.fatf-gafi.org/en/publications/Mutualevaluations/Assessment-ratings.html
2. Download **both** Excel files (the "Download" button under each): *Consolidated assessment ratings under the 2022 Methodology – Excel* and *...under the 2013 Methodology – Excel*.
3. Leave both in `~/Downloads` with default names (`consolidated-assessment-ratings-2022-methodology.xlsx`, `consolidated-assessment-ratings-2013-methodology.xlsx`). Verify they are real spreadsheets, not ~5 KB HTML stubs: `ls -la ~/Downloads/consolidated-assessment-ratings-*.xlsx` (2013 ~150 KB, 2022 ~16 KB; a few-KB file means Cloudflare blocked it — retry in the browser).
4. Re-run `notebooks/exploration/35_fatf_pipeline.ipynb` — both files auto-detected by glob, methodology round parsed from each filename, as-of date derived from the latest report date in the data. **No manual notebook edit needed**, even when a new methodology round appears (a future `*-2030-methodology.xlsx` is picked up automatically).

*Dependency: requires `pycountry` (in `environment.yml`). Only an in-sheet layout change (banner rows / column order) would need a code update — the positional column-mapping would raise a clear error in that case.*

### IMF_AREAER_ERREGIME — AREAER de-facto exchange-rate regime (MANUAL TRANSCRIPTION)
**MANUAL SNAPSHOT — does not auto-update.** AREAER Online is paywalled and the published classification (IMF *Annual Report* Appendix II.9) is a **borderless 2-D matrix** with no reliable automated extraction, so the source is maintained as a **hand-transcribed CSV**: `data/raw/areaer_defacto_regime.csv`.
**Annual refresh = edit the source CSV only — NO code changes.** The pipeline derives everything (including the `data_as_of` vintage) from that CSV; nothing is hardcoded in `37_areaer_defacto_er_pipeline.ipynb`.
**To refresh (MANUAL UPDATE, annual, ~30 min):**
1. Get the latest IMF *Annual Report* appendices PDF (free/public) and open **Appendix II.9** ("De Facto Classification of Exchange Rate Arrangements, as of <date>").
2. Most jurisdictions don't change year-to-year; the matrix flags reclassified ones with a `(month/year)` marker. **Update only those rows** in the CSV — change `areaer_arrangement` (and `areaer_mpf`/`areaer_anchor_currency` if the column moved), set `areaer_reclassified` to the new `YYYY-MM`, and clear stale reclassification markers.
3. **Set `areaer_as_of` on every row** to the new matrix "as-of" date (e.g. `2026-04-30`). This one value is how the pipeline learns the vintage — do NOT put a date in code.
4. **Validate against the PDF's own checksums** (this is what makes hand-transcription safe): each arrangement row AND each monetary-policy-framework column states its country count in the PDF — confirm your per-arrangement and per-column totals still match after editing (both axes sum to the jurisdiction total).
5. Re-run `notebooks/exploration/37_areaer_defacto_er_pipeline.ipynb` end-to-end → `data/processed/areaer_er_clean.csv` + updated `download_log`; then re-run the `IMF_AREAER_ERREGIME` cell at the end of `02_source_registry.ipynb` (coverage is derived from the clean CSV).
**MANUAL UPDATE — ISO3 (`ISO3_OVERRIDES`, Cell 2):** add a mapping ONLY if a new oddly-named jurisdiction appears — Cell 5 prints any name that neither `pycountry` (exact) nor the override map resolves. No fuzzy matching by design (data contains fuzzy-dangerous pairs: Niger/Nigeria, the three Guineas, Congo/DR Congo, Sudan/South Sudan).
**MANUAL UPDATE — IMF taxonomy (`ARRANGEMENT_ORDINAL`/`ARRANGEMENT_GROUP` in Cell 2; `VALID_MPF`/`VALID_ANCHOR` in Cell 6):** these encode the IMF's fixed 10-category arrangement + 4-way monetary-framework vocabulary; they change ONLY if the IMF revises its taxonomy (rare). A new/renamed value trips the Cell-4 vocabulary guard or the Cell-6 domain guard, which names the offender — update the relevant constant then.
**Caveats:** cross-section snapshot (NO `year`; vintage = `areaer_as_of`). `areaer_regime_ordinal` (1–10, most-fixed→most-flexible) follows IMF matrix row order; **`other_managed` (8) is a RESIDUAL, not a true flexibility rank** — prefer `areaer_regime_group` for scoring, or handle other_managed separately (metric-pass flag). Supersedes Reinhart-Rogoff as the current-state ER-regime primary.

### ASCOR - Assessing Sovereign Climate-related Opportunities and Risks (MANUAL DOWNLOAD, email-gated)
**MANUAL DOWNLOAD - does not auto-update.** The TPI Centre ASCOR tool serves its data through a JS interface behind an access request; there is no stable direct-download URL. Request access via the ASCOR tool page (https://www.transitionpathwayinitiative.org/ascor); the export arrives by return email as a zip (TPI ASCOR data - DDMMYYYY.zip) containing five .xlsx files.
**Annual refresh = replace three files - NO code changes.** The pipeline derives the vintage, country list, assessment rounds, and area/indicator membership from the files; nothing about the data is hardcoded in 40_ascor_pipeline.ipynb.
**To refresh (MANUAL UPDATE, annual, ~10 min):**
1. Request/download the current export, then extract the .xlsx files into data/raw/ **with lowercase names, overwriting in place** (one-liner: read the zip members and write each to data/raw with os.path.basename(name).lower()). Filenames are **deliberately undated** (ascor_assessments_results.xlsx, ascor_countries.xlsx, ascor_indicators.xlsx) so a new export drops in on top with no path edits. The pipeline reads only those three; the other two (ascor_benchmarks, ascor_assessments_results_trends_pathways) are emissions-pathway metrics, kept in raw for reference only.
2. Re-run notebooks/exploration/40_ascor_pipeline.ipynb end-to-end -> data/processed/ascor_clean.csv + updated download_log; then re-run the ASCOR cell in 02_source_registry.ipynb (coverage is derived from the clean CSV).
3. Confirm Cell 5 reports **ascor_n_areas_scored = 5 for every row**. This is the comparability guarantee - see below.
**MANUAL UPDATE - ASCOR_SCORED_AREAS / ASCOR_DIAGNOSTIC_AREAS (Cell 2):** the only hardcoded judgment in this pipeline. ASCOR_SCORED_AREAS is the set of areas **every country answers**, which is what makes the metric comparable across income groups. **Re-validate it on any methodology change** - Cell 4 fails loudly if an area code stops resolving, and the Cell-6 guard fails if any country is scored on fewer than all five. If ASCOR restructures its areas or changes which groups are exempt from what, both constants need review against the new methodology note (Appendix 1, Exemptions by country group) before the output can be trusted.
**v2.0 OVERHAUL PENDING.** This build targets ASCOR **v1.2** (Nov 2025 methodology). A v2.0 revision is in progress (consultation closed Jan 2026) and may restructure pillars, areas or indicators. On the first v2.0 export, expect Cell 4 to fail - that is the guard working. Re-validate the area constants, then re-run.
**Caveats:** **PANEL** source (year from Assessment date), 3 rounds to date - momentum needs >=3 points, so it is computable for only 25 of 85 countries. Scored metric is on a **fixed 0-1 anchor**, passed through unnormalized (S5 fixed-anchor family) - do NOT let the D4 rule reclassify it to z-score, which would reintroduce ASCOR advanced-economy sample skew. **ASCOR is already wealth-adjusted by design** (income-group exemptions) - flagged for the wealth-adjustment layer. Licence **CC BY-NC 4.0 (non-commercial)** - flagged for the framework-wide licence audit. Full rationale: framework_decisions.md -> ASCOR composite specification.

### WB_BRSS — World Bank Bank Regulation & Supervision Survey (Concept 9, banking — SUPPLEMENTARY)
**Mostly automated; ONE recurring manual trigger.** Cell 4 auto-discovers and downloads the latest BRSS
`.xlsx` from the permanent WB Data Catalog page (dataset `0038632`), caching to `data/raw/`. The reference
year (2016) is derived from the question codes at runtime — nothing hardcoded.
**⚠️ MANUAL-MAINTENANCE CONSTANT — `BRSS_CATALOG_URL` (Cell 2):** the permanent catalog URL. Stable by
design (a dataset id, NOT a version-pinned file link — which is exactly what rots). Update ONLY if the World
Bank restructures its data catalog.
**MANUAL UPDATE — check for a 6th wave (the real recurring task):** BRSS is a FROZEN, IRREGULAR survey
(waves 2001 / 2003 / 2007 / 2011 / 2019 — no fixed cadence). It will NOT auto-refresh with new data on any
schedule; periodically check the catalog page for a 6th wave. If one is posted:
1. Cell 4's auto-discover picks up the new `.xlsx` automatically (no code edit needed to fetch it).
2. **RE-VALIDATE `INCLUDED_QUESTIONS` (Cell 3)** against the new questionnaire — a new wave may renumber or
   reword questions. Cell 5 auto-derives the year suffix per code and **FAILS LOUDLY**, listing any base code
   that no longer resolves, so a schema shift cannot silently produce wrong output — but the *directional*
   meaning of any changed question must be re-checked by hand.
3. Re-run `notebooks/exploration/38_wb_brss_pipeline.ipynb` end-to-end → `data/processed/wb_brss_clean.csv`
   + updated `download_log`; then re-run the `WB_BRSS` cell in `02_source_registry.ipynb`.
**MANUAL UPDATE — `CACHE_YEAR` (Cell 4, = 2021):** the file-year of the wave the cache and the Cell-3 curation target (2019 wave, 2021-updated release). Cell 4 compares the catalog's newest file-year against it; if a newer wave is found it prints a LOUD alert and deliberately keeps using the cache rather than auto-adopting, because a new wave can renumber questions. **Bumping `CACHE_YEAR` (and deleting the old cache) is the step that actually adopts a new wave** — do it only AFTER re-validating `INCLUDED_QUESTIONS`. *(Improvement noted for Step 3: this could be derived by persisting the downloaded file's year rather than hand-set.)*
**MANUAL UPDATE — reliability threshold (`RELIABILITY_MIN_COVERAGE`, Cell 6, = 0.70):** a scoring/scope
constant, NOT a per-update edit; change only to revisit the reliable-vs-flagged cutoff (see framework_decisions.md).
**Caveats:** DE JURE regulatory-stringency (rules on paper), NOT supervisory effectiveness — advanced
economies mid-pack is correct. Cross-section snapshot (NO `year`). Bespoke construct-aligned score (NOT the
published BCL indices). CC-BY-4.0. 161 jurisdictions (155 reliable).

### ACLED — Armed Conflict Location and Event Data
Pending Research tier approval. Once approved, run `11_acled_pipeline.ipynb`. Credentials already in `.env`.

### BASEL_AML — Basel AML Index
Pending Expert Edition access (institutional affiliation). Alternative: FATF scraper (Category 3).

---

## Source Technical Notes

(Automated-source fallback procedures and API details. Coverage figures are data facts as of the as-of date above.)

### VDEM
Pipeline handles ZIP and direct CSV. 64 indicators. **MANUAL UPDATE:** `VDEM_VERSION`.

### WGI
`wbgapi`, db=3. 6 components. Latest year auto-derived from API.

### WB_WDI
`wbgapi`, db=2. 34 indicators, fetched one at a time (API timeout avoidance). Subsumes WHO GHO, UNESCO UIS, WB WBL (2.0 codes), WB LPI, WB HCI (HCI+), WIPO, ILO_SOCIAL, UNDP HDI, and WB tariffs.

### WJP
Auto-detects latest year by URL pattern, falls back to prior years. 8 factors + sub-factor 6.5.

### FH_FIW
Auto-detects via recent year/month URL candidates. Sub-components A, D, E, G. Requires BROWSER_HEADERS.

### FSI
Scrapes download page for all Excel links. C1, C2, C3, P2. Requires BROWSER_HEADERS.

### TI_CPI
Via OWID CSV. (TI direct files password-protected.)

### IMF_SPI
`wbgapi`, db=2. Overall + 5 pillars.

### UCDP
Auto-detects version codes from current year backwards. Bulk ZIP (API now needs token).

### FRASER
Scrapes annual report page for XLSX URL. Areas 2, 4, 5. Requires BROWSER_HEADERS.

### QOG
URL pattern `qogdata.pol.gu.se/data/qog_std_ts_jan{YY}.csv`, auto-detected. Covers KOF_TRADE (dr_eg proxy), PTS, OBS, ND_GAIN, BCI, HANSON_SIGMAN, CCP, PEI, GPI, WB_INFORMAL, ROMELLI_CBI, POLITY5, NELDA. See framework_decisions.md for KOF mismatch and CCP gap.

### POWELL_THYNE
Direct TXT. Version embedded in data, auto-detected.

### UNODC_HOMICIDE
Via OWID CSV.

### IRENA_CAPACITY
Via OWID CSV. Share of electricity from renewables (%) as proxy for capacity.

### IMF_IMAPP
URL pattern `elibrary-areaer.imf.org/Macroprudential/Documents/iMaPP_database-{YYYY}-{MM}-{DD}.zip`, latest auto-detected by date iteration (timeout ≥20s; IMF server is slow). Measures cumulative toolkit BREADTH (count of distinct instruments ever activated, total + 4 categories), not direction or in-force. See framework_decisions.md.

### YALE_EPI
Scrapes all pages of epi.yale.edu/epi-downloads; all editions stacked; years parsed from filenames.

### WB_CARBON
WB Carbon Pricing Dashboard month-stamped xlsx (`data_{MM}_{YYYY}.xlsx`), latest auto-detected by month iteration with retry/backoff (server rate-limits). Gen Info sheet is the spine; Price/Revenue joined via Unique ID / Instrument name. Measures: existence, price (US$/tCO2e, panel), revenue (US$m, panel), jurisdictional coverage % (current snapshot). National-only via explicit ISO3 dict (fail-safe; unmapped excluded). EU ETS expanded to members for price/coverage/existence but NOT revenue. Absence = inferred non-existence. ~71 countries (carbon pricing concentrated). **MANUAL UPDATE:** the national-name→ISO3 dictionary (if a new sovereign adopts carbon pricing — an in-pipeline diagnostic lists unmapped jurisdictions) and the EU27+ member list (if EU/EEA ETS membership changes).

### DPI
IDB CKAN API: `data.iadb.org/api/3/action/package_show?id=the-database-of-political-institutions-dpi-{year}`. Latest auto-detected by iterating years backwards.

### CIVICUS
REST API `monitor.civicus.org/api/countries/`. Latest rating per year retained. API returns recent years only.

### IDEA_PARTIP
Manual CSV. Auto-detects latest `gsod_indices_v{N}.csv` in Downloads by version number.

### PEW_GRI
Manual ZIP. Auto-detects `Global-Restrictions-on-Religion*.zip`, extracts CSV. Headline GRI + SHI only.

### IMF_FISCAL_RULES
Manual Excel. Auto-detects `*Fiscal Rules*.xlsx`. Robust NAME-BASED column selection from the 4-row nested header (composite keys: parent rows forward-filled, leaf row un-filled; substring match; fails loudly on rename). Presence + quality (legal basis 1-5, enforcement, compliance, monitoring, correction). **MANUAL UPDATE only if IMF renames a header section** — selector will raise a clear error.

---

### CLIMATE_LAWS
Manual CSV (free registration) from climate-laws.org. Auto-detects Document_Data_Download*.csv in Downloads. Cumulative stock of domestic climate laws/policies per country-year + new_laws flow. UNFCCC excluded; Legislative+Executive kept; deduped to Family ID. NATIONAL-ONLY (EU-level EUR docs dropped to avoid double-count with national transpositions; subnational dropped). 1900 plausibility floor on dates (fixed validation constant, not a vintage). Coverage: 199 countries.

### ODIN
Manual ZIP from odin.opendatawatch.com/data. Globs *data*.zip and validates by contents (ZIP must contain year-named Excels — filename is unstable). Sub-scores are a TRANSPARENT SIMPLE-MEAN aggregation of ODIN's per-category element scores — NOT ODIN's official 0-100 index. Raw ~0-2 scale (ranking valid, downstream-normalized). Biennial editions stacked. Overlaps substantially with IMF SPI. Coverage: 200 countries. MANUAL: keep only the current ODIN ZIP in Downloads.

### TI_POLFINANCE
Automated .xlsx export from International IDEA Political Finance Database (themeId=302). Score = equal-weighted mean of 20 directionally-defensible binary questions (Yes=1/No=0/Sometimes=0.5; No data/NA=NaN). Reliability floor: <10 of 20 answered -> NaN (kept), 0 answered -> dropped. Binary questions auto-detected by answer-set membership; the 20 included selected by explicit (category, question#) list encoding a directionality judgment. Wave-updated cross-section; no data-year in export (data_as_of = retrieval date). 180 countries (177 scored).

### IMF_AREAER
Manual export (portal WAF-blocked). FARI Index Report xlsx: metadata rows 0-1, header row 2, six FARI index variants stacked (Aggregate/Inflow/Outflow x overall/FDI), years as wide columns (1999-2024 dates), footnote rows interleaved (filtered by valid Index Name). Reshape wide->long->pivot to one column per index. fari_aggregate + fari_fdi_aggregate primary. IFS-code file; ISO3 via name + MANUAL_ISO3 (needs pycountry). 194 countries.

### IMF_AREAER_ERREGIME
Hand-transcribed from the AREAER de-facto classification borderless matrix (IMF *Annual Report* Appendix II.9); AREAER Online paywalled, `extract_tables` finds no grid. Source CSV `data/raw/areaer_defacto_regime.csv` (195 juris), validated at transcription against the PDF's per-arrangement (row) AND per-monetary-framework (column) country-count checksums (both axes sum to 195). Pipeline encodes `areaer_regime_ordinal` (1–10 flexibility, matrix order; other_managed=8 residual) + `areaer_regime_group` (IMF 4-way) via fixed Cell-2 lookups; `areaer_mpf` (incl. inflation-targeting flag) + `areaer_anchor_currency` carried from source; `areaer_reclassified` (YYYY-MM regime-change recency). Cross-section snapshot, NO year; `data_as_of` = `areaer_as_of` (derived from CSV). ISO3 via pycountry EXACT + `ISO3_OVERRIDES` (no fuzzy). Distinct from IMF_AREAER (FARI capital-account). Supersedes Reinhart-Rogoff. 195 jurisdictions, as-of 2025-04-30.

### CHINN_ITO
Automated. Scrapes web.pdx.edu/~ito for the newest `kaopen_YYYY.xls`; year parsed from the link (no hardcode); downloaded to `data/raw/` and read with `xlrd`. Source ships ISO3 (`ccode`) + IMF–WB numeric (`cn`); long panel `cn|ccode|country_name|year|kaopen|ka_open`. Standardize: drop `cn`, rename `ccode`→country_code / `ka_open`→kaopen_norm; `ZAR`→`COD` remap; drop empty (NaN) country-years (removes unscored Serbia/Timor placeholders); `ANT` (Netherlands Antilles, dead code) retained, flagged. `kaopen` (raw PCA, higher = more open — OPPOSITE sign to FARI) primary; `kaopen_norm` (0–1) supplementary. 181 valid-ISO3 + ANT = 182, 1970–2023. Version non-stable → full-replace each run. Needs `xlrd`.

### RTI_RATING
Automated. pandas.read_html on rti-rating.org/country-data extracts the 142-country scores table (7 categories + total + law year). Deficit-list xlsx (no-law countries) URL regex-extracted from the page HTML (no hardcoded date). rti_total = CLD's own published weighted sum (NOT recomputed). No-law countries: floored rti_total = min(observed)−1SD clamped ≥0, NaN sub-scores, has_rti_law=0. ISO3 via pycountry + MANUAL_ISO3 dict. Needs pycountry installed. 196 countries.

### PEFA
Manual download of a structured CSV from the "Scores Downloads" page (NOT PDF — reclassified out of the Category-1 PDF batch). Globs every `assessments_*.csv` in Downloads, concatenates + dedups, snapshots full raw (all frameworks) to RAW_DIR, then filters to `PEFA_FRAMEWORK` (="2016") + national, dedups latest per country (85). Wide→long melt of PI-XX (indicator) and PI-XX.Y (dimension) columns; A–D→numeric (7pt indicator: D=1…A=4, `+`→.5; 4pt dimension); `*` stripped + quality_flag; NU/NR/blank→missing/dropped. ISO3 via pycountry + OVERRIDES. Subnational ("Country - Subentity") excluded. 2011 deferred (stale). `data_as_of` = max assessment_year (derived).

### WB_BRSS
Automated fetch (Cell 4 auto-discovers the latest `.xlsx` from WB Data Catalog dataset `0038632`; no version-pinned URL). Workbook = raw survey responses across 15 topic sheets in TRANSPOSED layout (questions as rows, countries as columns), no pre-computed indices; Cell 5 resolves each base code to its latest `<code>_<YYYY>` variant (year auto-derived; fails loudly on any unresolved code) and transposes to a country×question frame (161 juris). Bespoke construct-aligned scoring (Cell 6, NOT the published BCL indices): 9 sub-constructs, 56 scored items (67 underlying codes; 2 blocks — Tier-1-deductions fraction, borrower-based-caps "any"), 5 reverse-coded; Activity Restrictions excluded; provisioning/macropru trimmed of prescriptive items penalizing IFRS-9. Equal-weight within construct; overall `brss_regstringency` weights 5 governance constructs 2× (power / independence / private-monitoring / resolution / macropru). NO coverage penalty (mean of ANSWERED items); `brss_reliable` = coverage ≥ 0.70 (155/161). ISO3 in-file (+ Curaçao override). Output: cross-section, `country_code`-keyed, NO `year`/`country_name`; 13 cols. Scratch extracts `brss_act.txt` / `brss_ctx.txt` are build-time only, NOT runtime inputs. CC-BY-4.0.

*Technical notes for not-yet-built sources will be added as each pipeline is built.*
