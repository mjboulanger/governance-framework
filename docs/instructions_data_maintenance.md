# Data Maintenance Instructions

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

4. Create a `.env` file in the project root with machine-specific paths and credentials:

   **Mac:**
   ```
   PROJECT_ROOT=/Users/{username}/Documents/governance-framework
   DOWNLOADS_DIR=/Users/{username}/Downloads
   ACLED_EMAIL=your_acled_email
   ACLED_PASSWORD=your_acled_password
   ```

   **Windows:**
   ```
   PROJECT_ROOT=C:\Users\{username}\governance-framework
   DOWNLOADS_DIR=C:\Users\{username}\Downloads
   ACLED_EMAIL=your_acled_email
   ACLED_PASSWORD=your_acled_password
   ```

5. Register the Jupyter kernel:
   `python -m ipykernel install --user --name governance-framework --display-name "governance-framework"`

6. Launch JupyterLab:
   `jupyter lab`

### Notes
- The `.env` file is machine-specific and not tracked by git — each machine needs its own
- Large raw data files (`data/raw/`) are not tracked by git — re-run pipelines to regenerate them
- Processed files (`data/processed/`) are tracked by git and available immediately after cloning

---

## Data Update Instructions

Run `print_stale_sources()` from `src/download_log.py` to identify sources needing refresh.
Full attempt and success dates for each source are recorded in `data/raw/download_log.csv`.

---

## Update Frequency Reference

Within each category, sources are ordered by number of indicators used in the framework.

---

### Category 1: PDF extraction (most manual)

| Source ID | Source Name | Frequency |
|-----------|-------------|-----------|
| PEFA | PEFA | Per-country 4–7yr |
| IMF_FSAP | IMF FSAP / BCP / IOSCO / IAIS | Per-country 5–10yr |
| ICNL | ICNL Civic Freedom Monitor | Irregular |

---

### Category 2: Email form download

| Source ID | Source Name | Frequency |
|-----------|-------------|-----------|
| VDEM | V-Dem Full+Others | Annual (March) |

---

### Category 3: Web scrape

| Source ID | Source Name | Frequency |
|-----------|-------------|-----------|
| FATF | FATF Compliance Ratings | Per-country ~10yr |
| IPU_PARLINE | IPU Parline | Continuous |
| WTO_TFA | WTO TFA Implementation | Continuous |
| IMF_SPI_SDDS | IMF SDDS Subscriptions | Continuous |
| CPJ | Committee to Protect Journalists | Continuous |

---

### Category 4: Manual Excel / CSV download — annual or biennial

| Source ID | Source Name | Frequency |
|-----------|-------------|-----------|
| OECD_TFI | OECD Trade Facilitation Indicators | Biennial |
| IRENA_POLICY | IRENA Renewable Energy Policies | Continuous |
| ODIN | Open Data Inventory | Biennial |
| IMF_FISCAL_RULES | IMF Fiscal Rules Database | Irregular (~2-3yr) |
| IMF_AREAER | IMF AREAER | Annual |
| DPI | Database of Political Institutions | Annual |
| IDEA_PARTIP | IDEA Global State of Democracy | Annual |
| CIVICUS | CIVICUS Monitor | Annual |
| CLIMATE_LAWS | LSE Grantham / Climate Policy Radar | Continuous |
| PEW_GRI | Pew GRI / SHI | Annual |
| RSF_WPFI | RSF World Press Freedom Index | Annual (optional cross-check only) |

---

### Category 5: Manual Excel / CSV download — irregular

| Source ID | Source Name | Frequency |
|-----------|-------------|-----------|
| POLITY5 | Polity5 | Irregular |
| NELDA | NELDA | Irregular |
| UNCTAD_NTM | UNCTAD NTM Database | Irregular |
| RTI_RATING | RTI Rating | Irregular |
| TI_POLFINANCE | TI Political Finance Database | Irregular |
| IDEA_EMB | IDEA EMB Database | Irregular |
| GLOBAL_DATA_BAROMETER | Global Data Barometer | Irregular |
| DINCER_CB | Dincer-Eichengreen CB Transparency | Irregular |
| REINHART_ROGOFF | Reinhart-Rogoff Exchange Rate | Irregular |
| LINZER_STATON | Linzer-Staton Judicial Independence | Irregular |

---

### Category 6: Automated — API or direct download (least manual)

| Source ID | Source Name | Frequency | Status |
|-----------|-------------|-----------|--------|
| WB_WDI | World Bank WDI | Annual | Active |
| FSI | Fragile States Index | Annual | Active |
| WGI | World Bank WGI | Annual | Active |
| TI_CPI | TI Corruption Perceptions Index | Annual | Active |
| IMF_SPI | WB Statistical Performance Indicators | Annual | Active |
| UCDP | Uppsala Conflict Data Program | Annual | Active |
| FRASER_REG | Fraser EFW — Regulation | Annual | Active |
| FRASER_LEGAL | Fraser EFW — Legal System | Annual | Active |
| QOG | QoG Standard TS (11 sources) | Annual | Active |
| POWELL_THYNE | Powell-Thyne Coup Database | Continuous | Active |
| UNODC_HOMICIDE | UNODC Homicide Statistics | Annual | Active |
| IRENA_CAPACITY | IRENA Renewables Capacity Statistics | Annual | Active |
| IMF_IMAPP | IMF iMaPP | Annual | Active |
| YALE_EPI | Yale EPI | Biennial | Active |
| WB_CARBON | World Bank Carbon Pricing Dashboard | Annual | Active |
| ACLED | ACLED | Continuous | Pending Research tier |
| BASEL_AML | Basel AML Index | Annual | Pending Expert Edition access |
| WJP | WJP Rule of Law Index | Annual | Active |
| FH_FIW | Freedom House FIW | Annual | Active |

---

## Per-Source Instructions

Actions the user must take, or may need to take, for each source.
Sources with no manual steps are omitted from this section.

---

### VDEM — V-Dem Full+Others
**Every year (March):**
1. Go to: https://www.v-dem.net/data/the-v-dem-dataset/
2. Click "Download Country-Year: V-Dem Full+Others" (latest version)
3. Fill in the form — email required, select CSV format
4. Save the file to your Downloads folder
5. Update `VDEM_VERSION` in `notebooks/exploration/03_vdem_pipeline.ipynb` (e.g. `"17"` for v17)
6. Re-run the notebook

---

### FH_FIW — Freedom House Freedom in the World
**Normally:** No action required — fully automated.

**If pipeline fails to find a file:**
1. Email datarequest@freedomhouse.org with subject "FIW Data Request"
2. Place the received Excel file in `data/raw/`
3. Update the pipeline notebook `06_fh_fiw_pipeline.ipynb` to load from the local file instead

---

### FSI — Fragile States Index
**Normally:** No action required — fully automated.

**If pipeline fails:**
1. Go to: https://fragilestatesindex.org/excel/
2. Download the latest year's Excel file
3. Place in `data/raw/` and load manually in `notebooks/exploration/07_fsi_pipeline.ipynb`

---

### TI_CPI — Transparency International Corruption Perceptions Index
**Normally:** No action required — fully automated via Our World in Data.

**If pipeline fails:**
1. Go to: https://ourworldindata.org/grapher/ti-corruption-perception-index
2. Click "Download" then CSV
3. Place file in `data/raw/` and update pipeline to load locally

---

### UCDP — Uppsala Conflict Data Program
**Normally:** No action required — fully automated.

**If pipeline fails:**
1. Go to: https://ucdp.uu.se/downloads/
2. Download "UCDP Country-Year Dataset on Organized Violence" — CSV ZIP
3. Place ZIP in `data/raw/` and load manually in `notebooks/exploration/12_ucdp_pipeline.ipynb`

---

### FRASER_REG / FRASER_LEGAL — Fraser Institute Economic Freedom of the World
**Normally:** No action required — fully automated.

**If pipeline fails:**
1. Go to: https://www.fraserinstitute.org/economic-freedom/dataset
2. Click "Download XLSX" on the latest annual report page
3. Place file in `data/raw/` and update pipeline to load locally

---

### QOG — Quality of Government Standard Time-Series
**Normally:** No action required — fully automated.

**If pipeline fails:**
1. Go to: https://www.gu.se/en/quality-government/qog-data/data-downloads/standard-dataset
2. Download "Time-series: Download CSV" for the latest version
3. Place file in `data/raw/` and update pipeline to load locally

**Sources covered:** KOF_TRADE (proxy), PTS, OBS, ND_GAIN, BCI, HANSON_SIGMAN, CCP, PEI, GPI, WB_INFORMAL, ROMELLI_CBI

---

### POWELL_THYNE — Powell-Thyne Coup Database
**Normally:** No action required — fully automated.

**If pipeline fails:**
1. Go to: http://www.uky.edu/~clthyn2/coup_data/powell_thyne_ccode_year.txt
2. Save the file to `data/raw/`
3. Update pipeline to load locally

---

### UNODC_HOMICIDE — UNODC Homicide Statistics
**Normally:** No action required — fully automated via Our World in Data.

**If pipeline fails:**
1. Go to: https://ourworldindata.org/homicides
2. Click "Download" then CSV
3. Place file in `data/raw/` and update pipeline to load locally

---

### IRENA_CAPACITY — IRENA Renewables Capacity Statistics
**Normally:** No action required — fully automated via Our World in Data.

**If pipeline fails:**
1. Go to: https://ourworldindata.org/renewable-energy
2. Find "Share of electricity from renewables" chart
3. Click "Download" then CSV
4. Place file in `data/raw/` and update pipeline to load locally

---

### IMF_IMAPP — IMF Integrated Macroprudential Policy Database
**Normally:** No action required — fully automated.

**If pipeline fails:**
1. Go to: https://www.elibrary-areaer.imf.org/Macroprudential/Pages/iMaPPDatabase.aspx
2. Download the latest ZIP file
3. Place ZIP in `data/raw/` and update pipeline to load locally

---

### YALE_EPI — Yale Environmental Performance Index
**Normally:** No action required — fully automated.

**If pipeline fails:**
1. Go to: https://epi.yale.edu/epi-downloads
2. Download the latest edition results CSV
3. Place file in `data/raw/` and update pipeline to load locally

---

### WB_CARBON — World Bank Carbon Pricing Dashboard
**Normally:** No action required — fully automated via Our World in Data.

**If pipeline fails:**
1. Go to: https://ourworldindata.org/grapher/carbon-tax-instruments
2. Click "Download" then CSV
3. Place file in `data/raw/` and update pipeline to load locally

---

### ACLED — Armed Conflict Location and Event Data
**Status:** Pending Research tier approval — pipeline not yet active.

**Once Research access is approved:**
1. Log in to acleddata.com and confirm API access is enabled
2. Run `notebooks/exploration/11_acled_pipeline.ipynb`

**Note:** Cookie-based authentication is already configured via `.env` (ACLED_EMAIL, ACLED_PASSWORD).

---

### BASEL_AML — Basel AML Index
**Status:** Pending Expert Edition access — requires institutional affiliation.

**If access obtained:**
1. Log in to index.baselgovernance.org
2. Download CSV via Expert Edition portal
3. Build automated pipeline in `notebooks/exploration/`

**Alternative if access not obtained:** Build FATF scraper (Category 3) for AML/CFT coverage.

---

### IMF_FISCAL_RULES — IMF Fiscal Rules Database
**Every ~2-3 years (irregular):**
1. Go to: https://www.imf.org/en/topics/fiscal-policies/fiscal-rules-dataset
2. Download the Excel dataset
3. Place in `data/raw/` and run pipeline notebook

---

### IMF_AREAER — IMF Annual Report on Exchange Arrangements
**Every year:**
1. Go to: https://www.elibrary-areaer.imf.org/
2. Navigate to Indices tab for FARI and ACI index data
3. Download and place in `data/raw/` and run pipeline notebook

---

### ODIN — Open Data Inventory
**Every 2 years:**
1. Go to: https://odin.opendatawatch.com/data
2. Click "Download complete data for all available countries, years, and indicators"
3. Place in `data/raw/` and run pipeline notebook

---

### DPI — Database of Political Institutions
**Every year:**
1. Go to: https://publications.iadb.org/en/database-political-institutions
2. Download the latest Excel file
3. Place in `data/raw/` and run pipeline notebook

---

### CIVICUS — CIVICUS Monitor
**Every year:**
1. Go to: https://monitor.civicus.org
2. Navigate to Data Centre and download ratings data
3. Place in `data/raw/` and run pipeline notebook

---

### CLIMATE_LAWS — LSE Grantham Climate Laws Database
**Continuous updates:**
1. Go to: https://climate-laws.org
2. Download the latest dataset (now managed by Climate Policy Radar)
3. Place in `data/raw/` and run pipeline notebook

---

*Per-source instructions for remaining sources will be added as each pipeline is built.*

---

## Source Technical Notes

Reference information about each source's access method, URL patterns, and technical details.

---

### VDEM — V-Dem Full+Others
- URL: https://www.v-dem.net/data/the-v-dem-dataset/
- Check for new release: https://www.v-dem.net/data/dataset-archive/
- File naming convention: `V-Dem-CY-Full+Others-v{VERSION}.csv` (direct CSV) or ZIP
- Pipeline handles both ZIP and direct CSV download formats
- Variables: 64 indicators across all framework concepts
- Coverage: 1990–2025, ~181 countries, annual

---

### WGI — World Bank Worldwide Governance Indicators
- Access: `wbgapi`, db=3, indicator prefix `GOV_WGI_`
- Metadata and latest year derived automatically from API — no hardcoding
- Coverage: 1996–present; annual from 2003, biennial 1996–2002
- Indicators: 6 components, `.EST` format (estimate, -2.5 to +2.5)

---

### WB_WDI — World Bank World Development Indicators
- Access: `wbgapi`, db=2
- Fetch one indicator at a time to avoid API timeout (~1 min per indicator)
- Coverage: 1990–present, 266 economies including aggregates
- Indicators: 34 total across education, health, infrastructure, gender equality, logistics, human capital, IP protection, social protection, HDI sub-indicators, and tariffs
- Sources subsumed: WHO GHO, UNESCO UIS, WB WBL, WB LPI, WB HCI, WIPO, ILO_SOCIAL, UNDP_HDI

---

### WJP — World Justice Project Rule of Law Index
- URL pattern: `https://worldjusticeproject.org/rule-of-law-index/downloads/{YEAR}_wjp_rule_of_law_index_HISTORICAL_DATA_FILE.xlsx`
- Auto-detection: pipeline tries current year, falls back to prior years, validates Content-Type
- Sub-indicator 6.5 retained for Property Rights concept
- Coverage: 2012–present (no 2017), 142–143 countries

---

### FH_FIW — Freedom House Freedom in the World
- URL pattern: `/sites/default/files/{YYYY}-{MM}/All_data_FIW_2013-{END}.xlsx`
- Auto-detection: constructs candidate URLs from recent year/month combinations
- Sub-components used: A, D, E, G plus sub-questions
- Coverage: 2013–present, 195 countries

---

### FSI — Fragile States Index
- Download page: https://fragilestatesindex.org/excel/
- Auto-detection: scrapes page for all Excel links, deduplicates by year
- Requires BROWSER_HEADERS from config.py
- Indicators: C1, C2, C3, P2
- Coverage: 2006–present, ~179 countries, annual

---

### TI_CPI — Transparency International Corruption Perceptions Index
- Source: Our World in Data (original: Transparency International)
- URL: `https://ourworldindata.org/grapher/ti-corruption-perception-index.csv?v=1&csvType=full&useColumnShortNames=false`
- Coverage: 2012–present, 182 countries

---

### IMF_SPI — World Bank Statistical Performance Indicators
- Access: `wbgapi`, db=2
- Indicators: 6 (overall score + 5 pillars)
- Coverage: 2004–present, 221 countries

---

### UCDP — Uppsala Conflict Data Program
- Download page: https://ucdp.uu.se/downloads/
- Auto-detection: tries version codes from current year backwards
- URL pattern: `https://ucdp.uu.se/downloads/{folder}/{prefix}-{version}-csv.zip`
- Coverage: 1989–present, 199 countries, annual

---

### FRASER_REG / FRASER_LEGAL — Fraser Institute Economic Freedom of the World
- Auto-detection: scrapes annual report page to find XLSX URL
- Requires BROWSER_HEADERS from config.py
- Indicators: Area 2 (Legal System), Area 4 (Trade Freedom), Area 5 (Regulation)
- Coverage: 1990–2023, 165 countries

---

### QOG — Quality of Government Standard Time-Series
- URL pattern: `https://www.qogdata.pol.gu.se/data/qog_std_ts_jan{YY}.csv`
- Auto-detection: tries current year and falls back to prior years
- Free, no registration, direct CSV, ~68MB
- Sources covered: KOF_TRADE (dr_eg proxy), PTS, OBS, ND_GAIN, BCI, HANSON_SIGMAN, CCP, PEI, GPI, WB_INFORMAL, ROMELLI_CBI
- See docs/framework_decisions.md for KOF mismatch and CCP gap details

---

### POWELL_THYNE — Powell-Thyne Coup Database
- URL: `http://www.uky.edu/~clthyn2/coup_data/powell_thyne_ccode_year.txt`
- Direct TXT download, continuously updated
- Version embedded in data (format: V{YYYY}.{MM}.{DD}) — auto-detected
- Coverage: 1950–present, 204 countries

---

### UNODC_HOMICIDE — UNODC Homicide Statistics
- Source: Our World in Data (original: UNODC)
- URL: `https://ourworldindata.org/grapher/homicide-rate-unodc.csv?v=1&csvType=full&useColumnShortNames=false`
- Coverage: 1990–2024, 208 countries

---

### IRENA_CAPACITY — IRENA Renewables Capacity Statistics
- Source: Our World in Data (original: IRENA/Ember)
- URL: `https://ourworldindata.org/grapher/share-electricity-renewables.csv?v=1&csvType=full&useColumnShortNames=false`
- Note: using share of electricity from renewables (%) as proxy for raw capacity (MW)
- Coverage: 1990–present, 226 countries

---

### IMF_IMAPP — IMF Integrated Macroprudential Policy Database
- URL pattern: `https://www.elibrary-areaer.imf.org/Macroprudential/Documents/iMaPP_database-{YYYY}-{MM}-{DD}.zip`
- Auto-detection: iterates dates backwards from today to find latest ZIP
- Aggregated from monthly to annual country-year format
- Indicators: tightening actions, loosening actions, net tightening, LTV average
- Coverage: 1990–2024, 135 countries

---

### YALE_EPI — Yale Environmental Performance Index
- Download page: https://epi.yale.edu/epi-downloads (multiple pages)
- Auto-detection: scrapes all pages to find all available edition results CSVs
- Years parsed from filenames — no hardcoding
- All available editions stacked automatically
- Consistent sub-indices across editions: EPI, CCH, ECO, HLT, BDH, AGR, FSH, WRS
- Extended sub-indices (newer editions only): MKP, MPE, MHP
- Note: methodology differs between editions — limited comparability
- Coverage: ~180 countries, biennial

---

### WB_CARBON — World Bank Carbon Pricing Dashboard
- Source: Our World in Data (original: World Carbon Pricing Database, Dolphin & Merkle)
- URL: `https://ourworldindata.org/grapher/carbon-tax-instruments.csv?v=1&csvType=full&useColumnShortNames=false`
- Indicator: carbon tax instrument coverage (categorical: No tax / National / Sub-national)
- Coverage: 1989–present, 201 countries, annual

---

### HERITAGE_TR / HERITAGE_PR — Heritage Foundation Index of Economic Freedom
- Deprioritized — no pipeline built
- See docs/framework_decisions.md for full rationale

---

### RSF_WPFI — RSF World Press Freedom Index
- Optional manual cross-check only — no automated pipeline
- Media freedom covered by V-Dem primary indicators

---

### ACLED — Armed Conflict Location and Event Data
- Authentication: cookie-based via `.env` (ACLED_EMAIL, ACLED_PASSWORD)
- Requires Research tier access — pending approval as of June 2026

---

### BASEL_AML — Basel AML Index
- Expert Edition (CSV) requires institutional affiliation — pending access as of June 2026
- Alternative: FATF scraper (Category 3)

---

*Technical notes for remaining sources will be added as each pipeline is built.*
