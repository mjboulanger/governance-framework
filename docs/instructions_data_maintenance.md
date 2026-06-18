# Data Maintenance Instructions

**As-of date (last manually updated):** 2026-06-17
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

7. Launch JupyterLab: `jupyter lab`

### Notes
- The `.env` file is machine-specific and not tracked by git — each machine needs its own
- `data/raw/` is not tracked by git — re-run pipelines to regenerate
- `data/processed/` is tracked by git and available immediately after cloning
- GitHub is the sync mechanism between machines. Keep the project OUTSIDE OneDrive (git corruption risk)

---

## Data Update Instructions

Run `print_stale_sources()` from `src/download_log.py` to identify sources needing refresh.
Attempt and success dates for each source are recorded in `data/raw/download_log.csv`.

For each source, the pipeline derives the data "as-of" date from the data or filename — not hardcoded. The only manual inputs required on update are flagged per-source below under **MANUAL UPDATE**.

---

## Update Frequency Reference

Within each category, sources are ordered by number of indicators used in the framework.

### Category 1: PDF extraction (most manual)
| Source ID | Source Name | Frequency |
|-----------|-------------|-----------|
| PEFA | PEFA | Per-country 4–7yr |
| IMF_FSAP | IMF FSAP / BCP / IOSCO / IAIS | Per-country 5–10yr |
| ICNL | ICNL Civic Freedom Monitor | Irregular |

### Category 2: Email/form download
| Source ID | Source Name | Frequency |
|-----------|-------------|-----------|
| VDEM | V-Dem Full+Others | Annual |

### Category 3: Web scrape (not yet built)
| Source ID | Source Name | Frequency |
|-----------|-------------|-----------|
| FATF | FATF Compliance Ratings | Per-country ~10yr |
| IPU_PARLINE | IPU Parline | Continuous |
| WTO_TFA | WTO TFA Implementation | Continuous |
| IMF_SDDS | IMF SDDS Subscriptions | Continuous |
| CPJ | Committee to Protect Journalists | Continuous |

### Category 4: Manual download
| Source ID | Source Name | Built? |
|-----------|-------------|--------|
| IDEA_PARTIP | IDEA Global State of Democracy | ✅ |
| PEW_GRI | Pew GRI / SHI | ✅ |
| IMF_FISCAL_RULES | IMF Fiscal Rules Database | ✅ |
| CLIMATE_LAWS | LSE Grantham / Climate Policy Radar | Downloaded, pipeline pending |
| ODIN | Open Data Inventory | Downloaded, pipeline pending |
| IRENA_POLICY | IRENA Renewable Energy Policies | Downloaded, pipeline pending |
| OECD_TFI | OECD Trade Facilitation Indicators | Manual — pending |
| IMF_AREAER | IMF AREAER | Manual — pending |
| RSF_WPFI | RSF World Press Freedom Index | Optional cross-check only |

### Category 5: Manual irregular (not built; most superseded — see framework_decisions.md)
| Source ID | Source Name | Status |
|-----------|-------------|--------|
| UNCTAD_NTM | UNCTAD NTM Database | Pending |
| RTI_RATING | RTI Rating | Pending |
| TI_POLFINANCE | TI Political Finance Database | Pending |
| IDEA_EMB | IDEA EMB Database | Pending |
| GLOBAL_DATA_BAROMETER | Global Data Barometer | Pending |
| REINHART_ROGOFF | Reinhart-Rogoff Exchange Rate | Pending, low priority |
| DINCER_CB | Dincer-Eichengreen CB Transparency | Deprioritized (stale) |
| LINZER_STATON | Linzer-Staton Judicial Independence | Deprioritized (stale) |

Note: POLITY5 and NELDA were previously listed here but are now sourced via the QoG pipeline — see Category 6 and framework_decisions.md.

### Category 6: Automated — API or direct download
| Source ID | Source Name | Status |
|-----------|-------------|--------|
| WB_WDI | World Bank WDI | Active |
| FSI | Fragile States Index | Active |
| WGI | World Bank WGI | Active |
| TI_CPI | TI Corruption Perceptions Index | Active |
| IMF_SPI | WB Statistical Performance Indicators | Active |
| UCDP | Uppsala Conflict Data Program | Active |
| FRASER_REG / FRASER_LEGAL | Fraser EFW | Active |
| QOG | QoG Standard TS (13 sources incl. POLITY5, NELDA) | Active |
| POWELL_THYNE | Powell-Thyne Coup Database | Active |
| UNODC_HOMICIDE | UNODC Homicide Statistics | Active |
| IRENA_CAPACITY | IRENA Renewables Capacity | Active |
| IMF_IMAPP | IMF iMaPP | Active |
| YALE_EPI | Yale EPI | Active |
| WB_CARBON | World Bank Carbon Pricing | Active (dashboard: existence/price/coverage/revenue) |
| DPI | Database of Political Institutions | Active |
| CIVICUS | CIVICUS Monitor | Active |
| WJP | WJP Rule of Law Index | Active |
| FH_FIW | Freedom House FIW | Active |
| ACLED | ACLED | Pending Research tier |
| BASEL_AML | Basel AML Index | Pending Expert Edition |

---

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

### RTI_RATING — Global RTI Rating (CLD / Access Info Europe)
**Normally:** No action required — fully automated. The pipeline parses the full scores table directly from rti-rating.org/country-data via pandas.read_html, and fetches the no-law deficit list from a URL it extracts dynamically from the page (so the date in that filename never needs hand-editing).
**MANUAL UPDATE only when:** a new country appears that pycountry can't map — the pipeline prints any unmapped country names; add them to the MANUAL_ISO3 dict in 30_rti_rating_pipeline.ipynb. (Applies to both the rated table and the deficit list.)
**Scope reminder:** de jure legal-framework strength only (not implementation). No-law countries are floored at min−1SD (clamped ≥0) with has_rti_law=0 — a documented scoring choice, see framework_decisions.md.
**If read_html finds 0 tables or the wrong shape:** the page structure changed — inspect rti-rating.org/country-data and adjust the parse.

### OECD_TFI — OECD Trade Facilitation Indicators
Manual only. JS-rendered simulator at https://sim.oecd.org/default.ashx?ds=TFI — no API. Export per income/region group. Alternatively email tad.contact@oecd.org for the full dataset. Pipeline pending.

### IMF_AREAER — IMF Annual Report on Exchange Arrangements
Manual. https://www.elibrary-areaer.imf.org/ — Indices tab for FARI/ACI index data. Pipeline pending.

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

### RTI_RATING
Automated. pandas.read_html on rti-rating.org/country-data extracts the 142-country scores table (7 categories + total + law year). Deficit-list xlsx (no-law countries) URL regex-extracted from the page HTML (no hardcoded date). rti_total = CLD's own published weighted sum (NOT recomputed). No-law countries: floored rti_total = min(observed)−1SD clamped ≥0, NaN sub-scores, has_rti_law=0. ISO3 via pycountry + MANUAL_ISO3 dict. Needs pycountry installed. 196 countries.

*Technical notes for not-yet-built sources will be added as each pipeline is built.*
