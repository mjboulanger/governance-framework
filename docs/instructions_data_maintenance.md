# Data Maintenance Instructions

This document contains update and download instructions for all data sources in the governance framework.
Run `print_stale_sources()` from `src/download_log.py` to identify sources needing refresh.

---

## Update Frequency Reference

Full attempt and success dates for each source are recorded in `data/raw/download_log.csv`.
Run `print_stale_sources()` from `src/download_log.py` to see current status.
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
| WJP | WJP Rule of Law Index | Annual |
| FH_FIW | Freedom House FIW | Annual |
| YALE_EPI | Yale EPI | Biennial |
| OECD_TFI | OECD Trade Facilitation Indicators | Biennial |
| FSI | Fragile States Index | Annual |
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
| TI_CPI | TI Corruption Perceptions Index | Annual |
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

### Category 6: Automated API (least manual)

| Source ID | Source Name | Frequency |
|-----------|-------------|-----------|
| WB_WDI | World Bank WDI | Annual |
| WHO_GHO | WHO Global Health Observatory | Annual |
| UNESCO_UIS | UNESCO Institute for Statistics | Annual |
| WGI | World Bank WGI | Annual |
| IMF_SPI | WB Statistical Performance Indicators | Annual |
| WB_WBL | World Bank Women Business and the Law | Annual |
| ACLED | ACLED | Continuous |
| WIPO | WIPO IP Statistics | Annual |
| ILO_SOCIAL | ILO Social Security Coverage | Annual |
| WB_LPI | World Bank LPI | Irregular |
| WB_HCI | World Bank Human Capital Index | Biennial |


## Per-Source Instructions

---

### VDEM — V-Dem Full+Others

- **Current version:** v16 (March 2026), covers 1789–2024
- **Update frequency:** Annual, typically March
- **Manual step required:** Yes — email form submission
- **Instructions:**
  1. Go to: https://www.v-dem.net/data/the-v-dem-dataset/
  2. Click "Download Country-Year: V-Dem Full+Others" (latest version)
  3. Fill in the form — email required, select CSV format
  4. Extract the ZIP and place the CSV in `data/raw/`
  5. Rename to `vdem_full_v{VERSION}.csv` e.g. `vdem_full_v16.csv`
  6. Update `VDEM_VERSION` in `notebooks/exploration/03_vdem_pipeline.ipynb`
- **Check for new release:** https://www.v-dem.net/data/dataset-archive/
- **Notes:** URL changes with each version — check archive page for latest.

---

*Per-source instructions for remaining sources will be added as each pipeline is built.*