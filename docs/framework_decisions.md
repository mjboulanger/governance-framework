# Framework Decisions Log

**Status:** Temporary working document. Delete when master PDF is regenerated.
**Purpose:** Captures decisions made during pipeline build phase that diverge from or update the master PDF.

---

## Source Access Decisions

### Sources Subsumed by WDI Pipeline
The following sources were originally listed as standalone pipelines in the master PDF but are fully covered by the WB WDI pipeline via `wbgapi` (db=2). No standalone pipelines were built for these.

| Source | Indicators Covered | WDI Codes |
|--------|-------------------|-----------|
| WHO GHO | Physicians/1000, nurses/1000, hospital beds/1000, UHC coverage index | SH.MED.PHYS.ZS, SH.MED.NUMW.P3, SH.MED.BEDS.ZS, SH_UHC_SCI |
| UNESCO UIS | Education expenditure % GDP/govt, pupil-teacher ratios | SE.XPD.TOTL.GD.ZS, SE.XPD.TOTL.GB.ZS, SE.PRM.ENRL.TC.ZS, SE.SEC.ENRL.TC.ZS |
| WB WBL | Gender equality — legal, supportive, enforcement frameworks | GD_WBL_OVL_LAW, GD_WBL_OVL_SFR, GD_WBL_OVL_ENF |
| WB LPI | Logistics Performance Index overall | LP.LPI.OVRL.XQ |
| WB HCI | Human Capital Index (HCI+ used — standard HCI not available via API) | HD_HCIP_OVRL_TO |
| WIPO | Patent and trademark applications resident/nonresident | IP.PAT.RESD, IP.PAT.NRES, IP.TMK.RSCT, IP.TMK.NRCT |
| ILO_SOCIAL | Social protection, safety net, social insurance coverage | per_allsp.cov_pop_tot, per_sa_allsa.cov_pop_tot, per_si_allsi.cov_pop_tot |
| UNDP HDI | Life expectancy, GNI per capita PPP | SP.DYN.LE00.IN, NY.GNP.PCAP.PP.CD |
| WB TARIFFS | Tariff rate applied, simple mean and weighted mean | TM.TAX.MRCH.SM.AR.ZS, TM.TAX.MRCH.WM.AR.ZS |

**Note on WB WBL:** Old WBL 1.0 indicator codes (SG.LAW.INDX series) were archived by World Bank in 2024. New WBL 2.0 codes used instead.

**Note on WB HCI:** Standard HCI (HD.HCI.OVRL) not available via API. HCI+ (HD_HCIP_OVRL_TO) used as substitute.

**Note on WB TARIFFS:** WB tariff data (Primary tier 1 for Trade governance) was missing from original pipeline — added in June 2026. Both simple mean and weighted mean retained.

---

### Sources Subsumed by QoG Pipeline
The following sources are available via the QoG Standard Time-Series dataset. One pipeline (`14_qog_pipeline.ipynb`) covers all of them.

| Source | QoG Variable(s) | Notes |
|--------|----------------|-------|
| KOF_TRADE | dr_eg | ⚠️ MISMATCH — see below |
| PTS | gd_ptsa, gd_ptsh, gd_ptss | All three source-agency versions retained |
| OBS | ibp_obi | Open Budget Index score 0-100 |
| ND_GAIN | gain_gov, gain_read | Sub-scores per master PDF spec |
| BCI | bci_bci | Currency verification recommended at metric pass |
| HANSON_SIGMAN | lld_capacity | Double-counting caveat: incorporates V-Dem and other sources |
| CCP | ccp_syst, ccp_market, ccp_civil, ccp_infoacc, ccp_equal | Gap: judicial independence sub-dimensions not in QoG CCP subset |
| PEI | pei_peii_1 | Per-election cadence; high missingness expected |
| GPI | gpi_gpi | Optional cross-check; deprioritized per framework decisions |
| WB_INFORMAL | ied_mimic, ied_dge | Informal economy size % GDP; coverage 1990-2020 |
| ROMELLI_CBI | cbie_index, cbie_policy, cbie_lending | Coverage: 1923-2023, 155 countries |
| POLITY5 | p_polity2, p_durable | Supplementary. Coverage: 1946-2020. Polity project not updated since ~2018 — QoG version as current as source |
| NELDA | nelda_fme, nelda_mbbe, nelda_mtop, nelda_noe, nelda_noea, nelda_noel, nelda_oa, nelda_rpae, nelda_vcdbe, nelda_noee | Per-election cadence, ~2000-2020. NELDA latest release is 2020 |

**QoG version:** Jan 2026 (`qog_std_ts_jan26.csv`). Updated annually, direct CSV download, no registration required. URL pattern: `https://www.qogdata.pol.gu.se/data/qog_std_ts_jan{YY}.csv`.

**⚠️ KOF_TRADE mismatch:** Master PDF specifies "KOF Globalisation Index — Trade Globalization subindex." QoG only has `dr_eg` (KOF Economic Globalisation — combines trade and financial). Trade-specific sub-index not in QoG. Decision: use `dr_eg` as proxy, flag at metric pass. Fraser Area 4 retained as additional trade openness source.

**CCP gap:** QoG includes only 18 CCP variables. Judicial independence and separation of powers sub-dimensions not clearly captured. Mitigation: V-Dem judicial independence indicators (Primary tier 1) cover these dimensions with better quality anyway.

---

### Sources Deprioritized — Coverage Superseded

| Source | Decision | Rationale |
|--------|----------|-----------|
| RSF WPFI | Optional manual cross-check only | Media freedom covered by V-Dem. RSF 2022+ methodology break. |
| GPI | Optional cross-check (in QoG as gpi_gpi) | Covered by UCDP + FSI + WGI PV + V-Dem. In QoG at no marginal cost. |
| Heritage TR | Deprioritized | Fraser Area 4 supersedes. |
| Heritage PR | Deprioritized | Fraser Area 2 + WJP + V-Dem supersede. |
| DINCER_CB | Deprioritized | Stale (latest data 2019). Romelli CBI in QoG (2023) covers same concept with more recent data. |

**On Fraser vs Heritage:** Fraser is academically preferred — peer-reviewed methodology, transparent weights, chain-linked series. Heritage is a policy advocacy product. Where they overlap, Fraser is used.

**On Fraser Area 4 (Trade Freedom):** Master PDF dropped it due to overlap with Heritage. Since Heritage TR was deprioritized, Fraser Area 4 is retained as primary trade openness index alongside KOF.

---

### Sources with Access Constraints

| Source | Constraint | Status |
|--------|-----------|--------|
| ACLED | Requires Research tier API access | Pending approval — email sent June 2026 |
| BASEL_AML | Expert Edition requires institutional affiliation — personal email not eligible | Deferred |
| UCDP API | Token required since Feb 2026 | Using bulk ZIP download instead |
| WHO GHO API | OData API deprecated end-2025 | Subsumed by WDI |
| TI CPI | Direct Excel files password-protected | Using OWID instead |
| FSI | 2024 and 2025 editions not yet on download page as of June 2026 | Data currency gap |
| OECD_TFI | JS-rendered simulator only — no API, not in OECD SDMX system | Manual Category 4 |
| IMF Fiscal Rules | DataMapper blocked, no direct Excel URL | Manual Category 4 |
| IMF AREAER | Portal-based, no direct download | Manual Category 4 |

**Basel AML note:** Expert Edition free for public-sector, multilateral, non-profit, and academic organisations. Personal email not eligible. If institutional affiliation obtained: apply at index.baselgovernance.org/subscription. Alternative: FATF scraper (Category 3).

---

### Sources Originally Listed as Manual That Are Now Automated

| Source | Original Category | Actual Access |
|--------|------------------|---------------|
| FSI | Category 4 manual | Automated scrape |
| Fraser EFW | Category 4 manual | Automated scrape |
| UCDP | Category 4 manual | Automated bulk ZIP |
| TI CPI | Category 4 manual | Automated via OWID |
| WJP | Category 4 manual | Automated URL detection |
| FH FIW | Category 4 manual | Automated URL detection |
| KOF_TRADE | Category 4 manual | Via QoG |
| PTS | Category 4 manual | Via QoG |
| OBS | Category 4 manual | Via QoG |
| ND_GAIN | Category 4 manual | Via QoG |
| BCI | Category 5 irregular | Via QoG |
| HANSON_SIGMAN | Category 5 irregular | Via QoG |
| CCP | Category 5 irregular | Via QoG |
| PEI | Category 5 irregular | Via QoG |
| GPI | Category 4 manual | Via QoG |
| WB_INFORMAL | Category 5 irregular | Via QoG |
| ROMELLI_CBI | Category 5 irregular | Via QoG |
| POLITY5 | Category 5 irregular | Via QoG |
| NELDA | Category 5 irregular | Via QoG |
| POWELL_THYNE | Category 4 manual | Automated direct TXT |
| UNODC_HOMICIDE | Category 4 manual | Automated via OWID |
| IRENA_CAPACITY | Category 4 manual | Automated via OWID |
| IMF_IMAPP | Category 4 manual | Automated ZIP with date auto-detection |
| YALE_EPI | Category 4 manual | Automated scrape of downloads pages |
| WB_CARBON | Category 4 manual | Automated via OWID |
| DPI | Category 4 manual | Automated via IDB CKAN API |
| CIVICUS | Category 4 manual | Automated via REST API |

---

## Variable-Level Decisions

### V-Dem "factionalism" variable (Concept 1)
No V-Dem variable with "faction" or "fract" in the name exists in V-Dem v16. Master PDF's "factionalism" label was conceptual, not a specific variable code. Factionalism dimension covered by FSI C2 (Factionalized Elites). No addition to VDEM_VARS needed.

### FSI indicator naming discrepancy
Master PDF incorrectly labels C2 as "P1" and C3 as "S1". Pipeline correctly uses C2 and C3.

### Fraser Area 2 — property sub-components
Master PDF specifies "property sub-components only" for Property rights. We pull full Area 2 aggregate. Metric-level pass decision — select property-specific sub-components at that stage.

### EPI cross-sectional limitation
Yale EPI only makes 2022 and 2024 editions available for download. No full time series accessible. Pipeline stacks both editions on 8 consistent sub-indices. 2024-only sub-indices (MKP, MPE, MHP) are NaN for 2022 rows.

### IRENA proxy
Master PDF calls for IRENA Renewables Capacity Statistics (MW). Using share of electricity from renewables (%) as proxy — more interpretable cross-country, normalises for country size.

### WB TARIFFS gap resolved
Master PDF lists "World Bank tariff data (WITS/WDI)" as Primary tier 1 for Trade governance. Was missing from original WDI pipeline. Added in June 2026: TM.TAX.MRCH.SM.AR.ZS (simple mean) and TM.TAX.MRCH.WM.AR.ZS (weighted mean).

---

## Pipelines Built

| Notebook | Source | Output File | Indicators | Coverage |
|----------|--------|-------------|------------|----------|
| 03_vdem | V-Dem | vdem_filtered.csv | 64 | 1990–2025, 181 countries |
| 04_wgi | WB WGI | wgi_clean.csv | 6 | 1996–2024, 215 countries |
| 05_wjp | WJP | wjp_clean.csv | 8 | 2012–2025, 143 countries |
| 06_fh_fiw | FH FIW | fh_fiw_clean.csv | 4 sub-components | 2013–2025, 195 countries |
| 07_fsi | FSI | fsi_clean.csv | 4 | 2006–2023, 179 countries |
| 08_ti_cpi | TI CPI | ti_cpi_clean.csv | 1 | 2012–2024, 182 countries |
| 09_wdi | WB WDI (34 indicators) | wdi_clean.csv | 34 | 1990–2025, 266 economies |
| 10_imf_spi | IMF SPI | spi_clean.csv | 6 | 2004–2024, 221 countries |
| 11_acled | ACLED | — | — | Pending Research tier |
| 12_ucdp | UCDP | ucdp_clean.csv | 16 | 1990–2024, 199 countries |
| 13_fraser | Fraser EFW | fraser_clean.csv | 3 areas | 1990–2023, 165 countries |
| 14_qog | QoG Standard TS (13 sources) | qog_clean.csv | 36 | 1990–2025, 200 countries |
| 15_powell_thyne | Powell-Thyne | powell_thyne_clean.csv | 4 | 1990–2025, 204 countries |
| 16_unodc | UNODC Homicide | unodc_clean.csv | 1 | 1990–2024, 208 countries |
| 17_irena | IRENA | irena_clean.csv | 1 | 1990–2025, 226 countries |
| 18_imapp | IMF iMaPP | imapp_clean.csv | 4 | 1990–2024, 135 countries |
| 19_epi | Yale EPI | epi_clean.csv | 11 | 2022, 2024; 180 countries |
| 20_wb_carbon | WB Carbon | wb_carbon_clean.csv | 1 | 1990–2025, 201 countries |
| 21_dpi | DPI | dpi_clean.csv | 31 | 1990–2023, 182 countries |
| 22_civicus | CIVICUS | civicus_clean.csv | 2 | 2022–2025, 199 countries |

---

## Outstanding Decisions

- KOF_TRADE: build separate KOF pipeline for trade sub-index vs accept dr_eg proxy — decision pending
- ACLED: complete pipeline once Research tier approved
- BASEL_AML: complete once Expert Edition access obtained (requires institutional affiliation)
- Concept 25 (Government transparency): reconsider before finalizing — significant indicator overlap
- SOE Governance (Concept 10): deferred to v2
- EPI sub-components: specific policy/institutional sub-components to select at metric pass
- IDEA EMB Database: not same as QoG ideaesd_* variables — evaluate at metric pass
- Category 3 web scrapes not yet built: FATF, IPU_PARLINE, WTO_TFA, IMF_SDDS, CPJ
- Category 4 manual pipelines not yet built: OECD_TFI, IMF_FISCAL_RULES, IMF_AREAER, CLIMATE_LAWS, ODIN, IRENA_POLICY, IDEA_PARTIP, PEW_GRI
- Category 5 irregular pipelines not yet built: REINHART_ROGOFF, LINZER_STATON, RTI_RATING, TI_POLFINANCE, GLOBAL_DATA_BAROMETER, UNCTAD_NTM
- Category 1 PDF extraction not yet built: PEFA, IMF_FSAP, ICNL

---

*This document to be deleted when master PDF is regenerated at end of pipeline build phase.*
