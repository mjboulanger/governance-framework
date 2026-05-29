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

4. Create a `.env` file in the project root with machine-specific paths:

   **Mac:**
   `PROJECT_ROOT=/Users/{username}/Documents/governance-framework`
   `DOWNLOADS_DIR=/Users/{username}/Downloads`

   **Windows:**
   `PROJECT_ROOT=C:\Users\{username}\governance-framework`
   `DOWNLOADS_DIR=C:\Users\{username}\Downloads`

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
| YALE_EPI | Yale EPI | Biennial |
| OECD_TFI | OECD Trade Facilitation Indicators | Biennial |
| ND_GAIN | ND-GAIN Country Index | Annual |
| IRENA_CAPACITY | IRENA Renewables Capacity Statistics | Annual |
| IRENA_POLICY | IRENA Renewable Energy Policies | Continuous |
| KOF_TRADE | KOF Globalisation Index — Trade | Annual |
| FRASER_REG | Fraser Economic Freedom — Regulation | Annual |
| FRASER_LEGAL | Fraser Economic Freedom — Legal System | Annual |
| OBS | Open Budget Survey | Biennial |
| ODIN | Open Data Inventory | Biennial |
| IMF_FISCAL_RULES | IMF Fiscal Rules Database | Annual |
| IMF_AREAER | IMF AREAER | Annual |
| IMF_IMAPP | IMF iMaPP | Annual |
| UCDP | Uppsala Conflict Data Program | Annual |
| DPI | Database of Political Institutions | Annual |
| IDEA_PARTIP | IDEA Global State of Democracy | Annual |
| UNDP_HDI | UNDP HDI Sub-indicators | Annual |
| WB_CARBON | World Bank Carbon Pricing Dashboard | Annual |
| UNODC_HOMICIDE | UNODC Homicide Statistics | Annual |
| PTS | Political Terror Scale | Annual |
| POWELL_THYNE | Powell-Thyne Coup Database | Annual |
| RSF_WPFI | RSF World Press Freedom Index | Annual |
| CIVICUS | CIVICUS Monitor | Annual |
| GPI | Global Peace Index | Annual |
| HERITAGE_TR | Heritage Trade Freedom | Annual |
| HERITAGE_PR | Heritage Property Rights | Annual |
| CLIMATE_LAWS | LSE Grantham Climate Laws Database | Continuous |
| PEW_GRI | Pew GRI / SHI | Annual |
| BASEL_AML | Basel AML Index | Annual |

---

### Category 5: Manual Excel / CSV download — irregular

| Source ID | Source Name | Frequency |
|-----------|-------------|-----------|
| CCP | Comparative Constitutions Project | Irregular |
| PEI | Electoral Integrity Project | Per-election |
| POLITY5 | Polity5 | Irregular |
| NELDA | NELDA | Irregular |
| UNCTAD_NTM | UNCTAD NTM Database | Irregular |
| WB_INFORMAL | World Bank Informal Economy Database | Irregular |
| RTI_RATING | RTI Rating | Irregular |
| TI_POLFINANCE | TI Political Finance Database | Irregular |
| IDEA_EMB | IDEA EMB Database | Irregular |
| GLOBAL_DATA_BAROMETER | Global Data Barometer | Irregular |
| ROMELLI_CBI | Romelli CBI Index | Irregular |
| DINCER_CB | Dincer-Eichengreen CB Transparency | Irregular |
| REINHART_ROGOFF | Reinhart-Rogoff Exchange Rate | Irregular |
| HANSON_SIGMAN | Hanson-Sigman State Capacity | Irregular |
| LINZER_STATON | Linzer-Staton Judicial Independence | Irregular |
| BCI | Bayesian Corruption Indicator | Irregular |

---

### Category 6: Automated — API or direct download (least manual)

| Source ID | Source Name | Frequency |
|-----------|-------------|-----------|
| WB_WDI | World Bank WDI | Annual |
| FSI | Fragile States Index | Annual |
| WHO_GHO | WHO Global Health Observatory | Annual |
| UNESCO_UIS | UNESCO Institute for Statistics | Annual |
| WGI | World Bank WGI | Annual |
| TI_CPI | TI Corruption Perceptions Index | Annual |
| IMF_SPI | WB Statistical Performance Indicators | Annual |
| WB_WBL | World Bank Women Business and the Law | Annual |
| ACLED | ACLED | Continuous |
| WIPO | WIPO IP Statistics | Annual |
| ILO_SOCIAL | ILO Social Security Coverage | Annual |
| WB_LPI | World Bank LPI | Irregular |
| WB_HCI | World Bank Human Capital Index | Biennial |
| WJP | WJP Rule of Law Index | Annual |
| FH_FIW | Freedom House FIW | Annual |

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
4. Save the ZIP to your Downloads folder
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

*Per-source instructions for remaining sources will be added as each pipeline is built.*

---

## Source Technical Notes

Reference information about each source's access method, URL patterns, and technical details.

---

### VDEM — V-Dem Full+Others
- URL: https://www.v-dem.net/data/the-v-dem-dataset/
- Check for new release: https://www.v-dem.net/data/dataset-archive/
- URL changes with each version — check archive page for latest
- File naming convention: `vdem_full_v{VERSION}.csv`
- Variables: 65 indicators across all framework concepts
- Coverage: 1789–present, ~180 countries, annual

---

### WGI — World Bank Worldwide Governance Indicators
- Access: `wbgapi`, db=3, indicator prefix `GOV_WGI_`
- Metadata and latest year derived automatically from API — no hardcoding
- Coverage: 1996–present; annual from 2003, biennial 1996–2002
- Indicators: 6 components, `.EST` format (estimate, -2.5 to +2.5)

---

### WJP — World Justice Project Rule of Law Index
- URL pattern: `https://worldjusticeproject.org/rule-of-law-index/downloads/{YEAR}_wjp_rule_of_law_index_HISTORICAL_DATA_FILE.xlsx`
- Auto-detection: pipeline tries current year, falls back to prior years, validates Content-Type
- 2017 edition was not published
- Sub-indicator 6.5 retained for Property Rights concept
- Coverage: 2012–present (no 2017), 142–143 countries

---

### FH_FIW — Freedom House Freedom in the World
- URL pattern: `/sites/default/files/{YYYY}-{MM}/All_data_FIW_2013-{END}.xlsx`
- Auto-detection: constructs candidate URLs from recent year/month combinations, validates Content-Type
- Sub-components used: A (Electoral Process), D (Expression and Belief), E (Associational Rights), G (Personal Autonomy) plus sub-questions
- Countries only — territories excluded
- FH changed data distribution policy in 2026; direct download may eventually be gated
- Coverage: 2013–present, 195 countries

---

### FSI — Fragile States Index
- Download page: https://fragilestatesindex.org/excel/
- Auto-detection: scrapes page for all Excel links, deduplicates by year, downloads and stacks all years from FRAMEWORK_START_YEAR
- Requires browser User-Agent header to avoid 403 block
- Indicators used: C1 (Security Apparatus), C2 (Factionalized Elites), C3 (Group Grievance), P2 (Public Services)
- Coverage: 2006–present, ~179 countries, annual
- Note: 2024 and 2025 editions not yet on download page as of May 2026 — data currency gap

---

### TI_CPI — Transparency International Corruption Perceptions Index
- Source: Our World in Data historical panel (original data: Transparency International)
- URL: `https://ourworldindata.org/grapher/ti-corruption-perception-index.csv?v=1&csvType=full&useColumnShortNames=false`
- TI direct Excel files are password-protected — OWID is the practical access route
- Coverage: 2012–present, 182 countries

---

*Technical notes for remaining sources will be added as each pipeline is built.*