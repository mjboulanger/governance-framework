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

**Note on WB WBL:** Old WBL 1.0 indicator codes (SG.LAW.INDX series) were archived by World Bank in 2024 following a methodology change. New WBL 2.0 codes used instead.

**Note on WB HCI:** Standard HCI (HD.HCI.OVRL) not available via World Bank API. HCI+ (HD_HCIP_OVRL_TO) used as substitute — same concept, expanded methodology.

**Note on UNDP HDI:** Years of schooling not available via WDI. Primary and secondary enrollment rates used as substitute for the education dimension.

---

### Sources Subsumed by QoG Pipeline
The following sources were originally listed as standalone pipelines but are available via the QoG Standard Time-Series dataset (`qog_std_ts_jan{YY}.csv`). One pipeline (`14_qog_pipeline.ipynb`) covers all of them.

| Source | QoG Variable(s) | Notes |
|--------|----------------|-------|
| KOF_TRADE | dr_eg | ⚠️ MISMATCH — see below |
| PTS | gd_ptsa, gd_ptsh, gd_ptss | All three source-agency versions retained |
| OBS | ibp_obi | Open Budget Index score 0-100 |
| ND_GAIN | gain_gov, gain_read | Sub-scores per master PDF spec |
| BCI | bci_bci | Currency verification recommended at metric pass |
| HANSON_SIGMAN | lld_capacity | Double-counting caveat: incorporates V-Dem and other sources |
| CCP | ccp_syst, ccp_market, ccp_civil, ccp_infoacc, ccp_equal | Gap: judicial independence and separation of powers sub-dimensions not in QoG CCP subset |
| PEI | pei_peii_1 | Per-election cadence; high missingness expected |
| GPI | gpi_gpi | Optional cross-check; deprioritized per framework decisions |
| WB_INFORMAL | ied_mimic, ied_dge | Informal economy size % GDP; coverage 1990-2020 |
| ROMELLI_CBI | cbie_index, cbie_policy, cbie_lending | Coverage: 1923-2023, 155 countries |

**QoG version:** Jan 2026 (`qog_std_ts_jan26.csv`). Updated annually, direct CSV download, no registration required. URL pattern: `https://www.qogdata.pol.gu.se/data/qog_std_ts_jan{YY}.csv`.

**⚠️ KOF_TRADE mismatch:** Master PDF specifies "KOF Globalisation Index — Trade Globalization subindex" as Primary tier 1 for Trade governance concept. QoG Standard dataset contains only `dr_eg` (KOF Economic Globalisation Index), which combines trade and financial globalization. The trade-specific sub-index is not in QoG. **Decision:** use `dr_eg` as proxy, flag at metric pass. Fraser Area 4 (Trade Freedom) retained as additional trade openness measure.

**CCP gap:** QoG includes 18 CCP variables — a subset of CCP's full variable set. Master PDF calls for specific sub-dimensions including judicial independence constitutional features and separation of powers provisions. These are not clearly identifiable in the 18 QoG CCP variables. Mitigation: the direct V-Dem judicial independence and legislative constraint indicators (primary tier 1) cover these dimensions with better measurement quality than CCP variables would anyway. CCP remains as supplementary de jure reference.

---

### Sources Deprioritized — Coverage Superseded

| Source | Decision | Rationale |
|--------|----------|-----------|
| RSF WPFI | Optional manual cross-check only | Media freedom covered comprehensively by V-Dem primary indicators. RSF 2022+ uses new methodology incompatible with pre-2022 series. No automated download available. |
| GPI | Optional manual cross-check only (included in QoG as gpi_gpi) | Political stability covered by UCDP + FSI + WGI PV + V-Dem. Available in QoG so included at no marginal cost. |
| Heritage TR | Deprioritized | Fraser Area 4 (Trade Freedom) covers same concept with superior academic methodology. Heritage adds ~20 countries but not within target sample. |
| Heritage PR | Deprioritized | Fraser Area 2 (Legal System) + WJP + V-Dem cover property rights more comprehensively. Heritage adds nothing not already captured. |

**On Fraser vs Heritage:** Fraser Institute EFW is the academically preferred economic freedom dataset — peer-reviewed methodology, transparent component weights, chain-linked historical series. Heritage Index is a policy advocacy product with less transparent methodology and no chain-linked series. Where the two overlap, Fraser is used.

**On Fraser Area 4 (Trade Freedom):** The master PDF dropped Fraser Area 4 from Trade governance (Concept 11) due to overlap with Heritage Trade Freedom. Since Heritage TR was subsequently deprioritized, Fraser Area 4 is now retained as the primary trade openness index source alongside KOF. This reverses the master PDF's drop decision for Area 4.

---

### Sources with Access Constraints

| Source | Constraint | Status |
|--------|-----------|--------|
| ACLED | Requires Research tier API access — free tier gives aggregated data only | Pending approval — email sent to research@acleddata.com June 2026 |
| BASEL_AML | Expert Edition (free CSV access) requires institutional affiliation | Deferred pending eligibility — see below |
| UCDP API | Token required since February 2026 | Using bulk ZIP download instead — no token needed |
| WHO GHO API | OData API deprecated end-2025; new implementation at data.who.int not stable | Subsumed by WDI |
| TI CPI | Direct Excel files password-protected | Using OWID historical panel CSV instead |
| FSI | 2024 and 2025 editions not yet on download page as of May 2026 | Data currency gap — latest available: 2023 |

**Basel AML access note:** Expert Edition subscription is free for public-sector, multilateral, non-profit, and academic organisations. Personal email accounts are not eligible. If institutional affiliation becomes available: apply at index.baselgovernance.org/subscription and automate via direct CSV download. If not: build FATF scraper (Category 3) as alternative for AML/CFT coverage, or accept gap in Financial sector concept. Same deferral situation as ACLED.

---

### Sources Automated That Were Listed as Manual

| Source | Original Category | Actual Access |
|--------|------------------|---------------|
| FSI | Category 4 manual | Automated scrape of download page |
| Fraser EFW | Category 4 manual | Automated scrape of annual report page |
| UCDP | Category 4 manual | Automated bulk ZIP download |
| TI CPI | Category 4 manual | Automated via OWID CSV |
| WJP | Category 4 manual | Automated direct URL detection |
| FH FIW | Category 4 manual | Automated URL detection |
| KOF_TRADE | Category 4 manual | Via QoG automated download |
| PTS | Category 4 manual | Via QoG automated download |
| OBS | Category 4 manual | Via QoG automated download |
| ND_GAIN | Category 4 manual | Via QoG automated download |
| BCI | Category 5 irregular | Via QoG automated download |
| HANSON_SIGMAN | Category 5 irregular | Via QoG automated download |
| CCP | Category 5 irregular | Via QoG automated download |
| PEI | Category 5 irregular | Via QoG automated download |
| GPI | Category 4 manual | Via QoG automated download |
| WB_INFORMAL | Category 5 irregular | Via QoG automated download |
| ROMELLI_CBI | Category 5 irregular | Via QoG automated download |

---

### Sources Not in QoG — Requiring Separate Pipelines

| Source | Concept | Priority |
|--------|---------|----------|
| CIVICUS | Political participation, Civil society | High — Primary tier 1, unique data |
| DPI | Political settlement, Electoral process | High — Primary tier 2 |
| POWELL_THYNE | Political settlement, Political stability | High — Primary tier 1 |
| UNODC_HOMICIDE | Personal security | High — Primary tier 1 |
| IRENA_CAPACITY | Environmental/climate governance | High — Primary tier 1 |
| CLIMATE_LAWS | Environmental/climate governance | High — Primary tier 1 |
| IMF_FISCAL_RULES | Macroeconomic policy | High — Primary tier 1 |
| IMF_AREAER | Macroeconomic policy | High — Primary tier 1 |
| IMF_IMAPP | Macroeconomic policy | High — Primary tier 1 |
| ODIN | Statistical infrastructure | Medium — Primary tier 1 |
| BASEL_AML | Financial sector | Medium — Primary tier 1 (deferred) |
| PEW_GRI | Civil liberties | Medium — Primary tier 2 |
| KOF_TRADE (sub-index) | Trade governance | Decision pending — using dr_eg proxy |

---

## Variable-Level Decisions

### V-Dem "factionalism" variable (Concept 1 — Political settlement)
Master PDF listed "factionalism" as a V-Dem indicator alongside v2pepwrses, v2pepwrsoc, v2x_egal, v2psoppaut. No V-Dem variable with "faction" or "fract" in the name exists in V-Dem v16. The candidates `v2pscnslnl` (party system consolidation) and `v2pscomprg` (party competition) are not direct factionalism measures. **Decision:** no additional V-Dem variable added. The factionalism dimension for Political settlement is covered by FSI C2 (Factionalized Elites) — Primary tier 1, already in pipeline.

### FSI indicator naming discrepancy
Master PDF labels FSI Factionalized Elites as "P1" and Group Grievance as "S1" — these are incorrect FSI codes. Correct codes are C2 (Factionalized Elites) and C3 (Group Grievance). Our pipeline correctly uses C2 and C3. The master PDF labels are erroneous but the indicators are correct.

### Fraser Area 2 — property sub-components
Master PDF specifies "property sub-components only" for Property rights concept (Concept 17). We pull the full Area 2 aggregate score. This is a metric-level pass issue — at the pipeline level, having Area 2 is correct. At the metric pass, select the property-specific sub-components within Area 2.

---

## Pipelines Built

| Notebook | Source | Output File | Indicators | Coverage |
|----------|--------|-------------|------------|----------|
| 03_vdem_pipeline | V-Dem | vdem_filtered.csv | 64 | 1990–2025, 181 countries |
| 04_wgi_pipeline | WB WGI | wgi_clean.csv | 6 | 1996–2024, 215 countries |
| 05_wjp_pipeline | WJP | wjp_clean.csv | 8 | 2012–2025, 143 countries |
| 06_fh_fiw_pipeline | FH FIW | fh_fiw_clean.csv | 4 sub-components | 2013–2025, 195 countries |
| 07_fsi_pipeline | FSI | fsi_clean.csv | 4 | 2006–2023, 179 countries |
| 08_ti_cpi_pipeline | TI CPI | ti_cpi_clean.csv | 1 | 2012–2024, 182 countries |
| 09_wdi_pipeline | WB WDI (32 indicators) | wdi_clean.csv | 32 | 1990–2025, 266 economies |
| 10_imf_spi_pipeline | IMF SPI | spi_clean.csv | 6 | 2004–2024, 221 countries |
| 11_acled_pipeline | ACLED | — | — | Pending Research tier |
| 12_ucdp_pipeline | UCDP | ucdp_clean.csv | 16 | 1990–2024, 199 countries |
| 13_fraser_pipeline | Fraser EFW | fraser_clean.csv | 3 areas | 1990–2023, 165 countries |
| 14_qog_pipeline | QoG Standard TS (11 sources) | qog_clean.csv | 21 | 1990–2025, 200 countries |

---

## Outstanding Decisions

- KOF_TRADE: build separate KOF pipeline for trade sub-index vs accept dr_eg proxy — decision pending
- ACLED: complete pipeline once Research tier approved
- BASEL_AML: complete pipeline once Expert Edition access obtained (requires institutional affiliation)
- Concept 25 (Government transparency and openness): reconsider before finalizing — significant indicator overlap
- SOE Governance (Concept 10): deferred to v2
- EPI sub-components: QoG has wrong granularity — address via separate Yale EPI pipeline
- NELDA: too stale in QoG (2020) — evaluate at metric pass whether to build separate pipeline
- IDEA EMB Database: not same as QoG ideaesd_* variables — evaluate at metric pass

---

*This document to be deleted when master PDF is regenerated at end of pipeline build phase.*
