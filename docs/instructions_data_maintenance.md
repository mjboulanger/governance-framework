# Data Maintenance Instructions

This document contains update and download instructions for all data sources in the governance framework.
Run `print_stale_sources()` from `src/download_log.py` to identify sources needing refresh.

---

## Update Frequency Reference

Full attempt and success dates for each source are recorded in `data/raw/download_log.csv`.
Run `print_stale_sources()` from `src/download_log.py` to see current status.

| Source ID | Source Name | Frequency | Last Manual Step Required |
|-----------|-------------|-----------|--------------------------|
| VDEM | V-Dem Full+Others | Annual (March) | Yes — form download |
| WGI | World Bank WGI | Annual | No — API |
| WDI | World Bank WDI | Annual | No — API |
| WJP | WJP Rule of Law Index | Annual | Yes — Excel download |
| FH_FIW | Freedom House FIW | Annual | Yes — Excel download |
| FSI | Fragile States Index | Annual | Yes — Excel download |
| IMF_FISCAL_RULES | IMF Fiscal Rules Database | Annual | Yes — Excel download |
| IMF_AREAER | IMF AREAER | Annual | Yes — Excel download |
| IMF_IMAPP | IMF iMaPP | Annual | Yes — Excel download |
| IMF_SPI | WB Statistical Performance Indicators | Annual | No — API |
| ROMELLI_CBI | Romelli CBI Index | Irregular | Yes — replication data |
| DINCER_CB | Dincer-Eichengreen CB Transparency | Irregular | Yes — replication data |
| REINHART_ROGOFF | Reinhart-Rogoff Exchange Rate | Irregular | Yes — replication data |
| UNODC_HOMICIDE | UNODC Homicide Statistics | Annual | Yes — Excel download |
| PTS | Political Terror Scale | Annual | Yes — Excel download |
| POWELL_THYNE | Powell-Thyne Coup Database | Annual | Yes — CSV download |
| UCDP | Uppsala Conflict Data Program | Annual | Yes — CSV download |
| ACLED | ACLED | Continuous | Yes — API key required |
| TI_CPI | TI Corruption Perceptions Index | Annual | Yes — Excel download |
| RSF_WPFI | RSF World Press Freedom Index | Annual | Yes — CSV download |
| CPJ | Committee to Protect Journalists | Continuous | Yes — CSV download |
| CIVICUS | CIVICUS Monitor | Annual | Yes — Excel download |
| IDEA_EMB | IDEA EMB Database | Irregular | Yes — Excel download |
| PEI | Electoral Integrity Project | Per-election | Yes — CSV download |
| CCP | Comparative Constitutions Project | Irregular | Yes — CSV download |
| DPI | Database of Political Institutions | Annual | Yes — Excel download |
| GPI | Global Peace Index | Annual | Yes — Excel download |
| ODIN | Open Data Inventory | Biennial | Yes — CSV download |
| PEFA | PEFA | Per-country 4-7yr | Yes — PDF extraction |
| OBS | Open Budget Survey | Biennial | Yes — Excel download |
| FATF | FATF Mutual Evaluation Ratings | Per-country 10yr | Yes — web scrape |
| BASEL_AML | Basel AML Index | Annual | Yes — Excel download |
| HERITAGE_TR | Heritage Trade Freedom | Annual | Yes — Excel download |
| HERITAGE_PR | Heritage Property Rights | Annual | Yes — Excel download |
| WB_LPI | World Bank LPI | Irregular | No — API |
| OECD_TFI | OECD Trade Facilitation Indicators | Biennial | Yes — Excel download |
| KOF_TRADE | KOF Globalisation Index | Annual | Yes — Excel download |
| UNCTAD_NTM | UNCTAD NTM Database | Irregular | Yes — Excel download |
| YALE_EPI | Yale EPI | Biennial | Yes — CSV download |
| CLIMATE_LAWS | LSE Climate Laws Database | Continuous | Yes — CSV download |
| ND_GAIN | ND-GAIN Country Index | Annual | Yes — CSV download |
| IRENA_CAPACITY | IRENA Renewables Capacity | Annual | Yes — Excel download |
| IRENA_POLICY | IRENA Renewable Energy Policies | Continuous | Yes — Excel download |
| WB_CARBON | WB Carbon Pricing Dashboard | Annual | Yes — Excel download |
| WTO_TFA | WTO TFA Implementation | Continuous | Yes — web scrape |
| IPU_PARLINE | IPU Parline | Continuous | Yes — web scrape |
| RTI_RATING | RTI Rating | Irregular | Yes — Excel download |
| TI_POLFINANCE | TI Political Finance Database | Irregular | Yes — Excel download |
| WIPO | WIPO IP Statistics | Annual | No — API |
| ILO_SOCIAL | ILO Social Security Coverage | Annual | No — API |
| WB_INFORMAL | WB Informal Economy Database | Irregular | Yes — Excel download |
| FRASER_REG | Fraser Regulation Area | Annual | Yes — Excel download |
| FRASER_LEGAL | Fraser Legal System | Annual | Yes — Excel download |
| PEW_GRI | Pew GRI / SHI | Annual | Yes — Excel download |
| WB_WBL | WB Women Business and the Law | Annual | No — API |
| NELDA | NELDA | Irregular | Yes — CSV download |
| IDEA_PARTIP | IDEA Global State of Democracy | Annual | Yes — Excel download |
| BCI | Bayesian Corruption Indicator | Irregular | Yes — CSV download |
| GLOBAL_DATA_BAROMETER | Global Data Barometer | Irregular | Yes — CSV download |
| IMF_SPI_SDDS | IMF SDDS Subscriptions | Continuous | Yes — web scrape |
| WHO_GHO | WHO Global Health Observatory | Annual | No — API |
| UNESCO_UIS | UNESCO Institute for Statistics | Annual | No — API |
| UNDP_HDI | UNDP HDI Sub-indicators | Annual | Yes — CSV download |
| WB_HCI | WB Human Capital Index | Biennial | No — API |
| POLITY5 | Polity5 | Irregular | Yes — Excel download |
| LINZER_STATON | Linzer-Staton Judicial Independence | Irregular | Yes — CSV download |
| ICNL | ICNL Civic Freedom Monitor | Irregular | Yes — manual review |
| HANSON_SIGMAN | Hanson-Sigman State Capacity | Irregular | Yes — CSV download |

---

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