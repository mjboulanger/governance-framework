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

### Sources Deprioritized — Coverage Superseded

| Source | Decision | Rationale |
|--------|----------|-----------|
| RSF WPFI | Optional manual cross-check only | Media freedom covered comprehensively by V-Dem primary indicators. RSF 2022+ uses new methodology incompatible with pre-2022 series. No automated download available. |
| GPI | Optional manual cross-check only | Political stability covered by UCDP + FSI + WGI PV + V-Dem. IEP blocks automated downloads. |
| Heritage TR | Deprioritized | Fraser Area 4 (Trade Freedom) covers same concept with superior academic methodology. Heritage adds ~20 countries but not within target sample. |
| Heritage PR | Deprioritized | Fraser Area 2 (Legal System) + WJP + V-Dem cover property rights more comprehensively. Heritage adds nothing not already captured. |

**On Fraser vs Heritage:** Fraser Institute EFW is the academically preferred economic freedom dataset — peer-reviewed methodology, transparent component weights, chain-linked historical series. Heritage Index is a policy advocacy product with less transparent methodology and no chain-linked series. Where the two overlap, Fraser is used.

---

### Sources with Access Constraints

| Source | Constraint | Status |
|--------|-----------|--------|
| ACLED | Requires Research tier API access — free tier gives aggregated data only | Pending approval — email sent to research@acleddata.com June 2026 |
| UCDP API | Token required since February 2026 | Using bulk ZIP download instead — no token needed |
| WHO GHO API | OData API deprecated end-2025; new implementation at data.who.int not stable | Subsumed by WDI |
| TI CPI | Direct Excel files password-protected | Using OWID historical panel CSV instead |
| FSI | 2024 and 2025 editions not yet on download page as of May 2026 | Data currency gap — latest available: 2023 |

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

---

## Outstanding Decisions

- Heritage TR and Heritage PR: confirm final decision to deprioritize before master PDF regeneration
- RSF WPFI: confirm manual cross-check only status
- GPI: confirm manual cross-check only status
- ACLED: complete pipeline once Research tier approved
- Concept 26 (Government transparency): reconsider before finalizing — significant indicator overlap with other concepts
- SOE Governance (Concept 10): deferred to v2

---

*This document to be deleted when master PDF is regenerated at end of pipeline build phase.*
