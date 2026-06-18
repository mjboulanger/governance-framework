# Framework Decisions Log

**Status:** Temporary working document. Delete when master PDF is regenerated.
**As-of date (last manually updated):** 2026-06-17
**⚠️ MANUAL SNAPSHOT:** This document is a point-in-time snapshot maintained by hand. It does NOT auto-update. Coverage ranges, vintages, source counts, and "as-of" dates below were accurate as of the date above and must be refreshed manually when pipelines are re-run or sources change.
**Purpose:** Captures decisions made during pipeline build phase that diverge from or update the master PDF.

---

## Source Access Decisions

### Sources Subsumed by WDI Pipeline
Originally listed as standalone pipelines in the master PDF but fully covered by the WB WDI pipeline via `wbgapi` (db=2). No standalone pipelines built.

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

**WB WBL note:** Old WBL 1.0 codes (SG.LAW.INDX series) archived by World Bank in 2024. New WBL 2.0 codes used.
**WB HCI note:** Standard HCI (HD.HCI.OVRL) not available via API. HCI+ (HD_HCIP_OVRL_TO) used as substitute.
**WB TARIFFS note:** Was missing from original WDI pipeline — added. Both simple and weighted mean retained.

---

### Sources Subsumed by QoG Pipeline
Available via the QoG Standard Time-Series dataset. One pipeline (`14_qog_pipeline.ipynb`) covers all of them.

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
| GPI | gpi_gpi | Optional cross-check; deprioritized |
| WB_INFORMAL | ied_mimic, ied_dge | Informal economy size % GDP |
| ROMELLI_CBI | cbie_index, cbie_policy, cbie_lending | Central bank independence |
| POLITY5 | p_polity2, p_durable | Supplementary. Polity project not updated since latest release — QoG version as current as source |
| NELDA | nelda_fme, nelda_mbbe, nelda_mtop, nelda_noe, nelda_noea, nelda_noel, nelda_oa, nelda_rpae, nelda_vcdbe, nelda_noee | Per-election cadence. NELDA latest release is the current ceiling — QoG version as current as source |

**QoG version:** Jan vintage. Updated annually, direct CSV, no registration. URL pattern: `qogdata.pol.gu.se/data/qog_std_ts_jan{YY}.csv`.

**⚠️ KOF_TRADE mismatch:** Master PDF specifies KOF Trade Globalization subindex. QoG only has `dr_eg` (KOF Economic Globalisation — trade + financial combined). Decision: use `dr_eg` as proxy, flag at metric pass. Fraser Area 4 retained as additional trade openness source.

**CCP gap:** QoG includes only a subset of CCP variables. Judicial independence / separation of powers sub-dimensions not clearly captured. Mitigation: V-Dem judicial indicators cover these with better quality.

---

### Sources Deprioritized — Coverage Superseded or Stale

| Source | Decision | Rationale |
|--------|----------|-----------|
| RSF WPFI | Optional manual cross-check only | Media freedom covered by V-Dem. RSF methodology break reduces comparability. |
| GPI | Optional cross-check (in QoG as gpi_gpi) | Covered by UCDP + FSI + WGI PV + V-Dem. In QoG at no marginal cost. |
| Heritage TR | Deprioritized | Fraser Area 4 supersedes. |
| Heritage PR | Deprioritized | Fraser Area 2 + WJP + V-Dem supersede. |
| DINCER_CB | Deprioritized | Stale (data ends mid-2010s). Romelli CBI in QoG covers same concept, more recent. |
| LINZER_STATON | Deprioritized | Stale and discontinued per IDEA. V-Dem judicial indicators (v2juhcind, v2juncind, v2jucomp, v2jupack, v2jupurge) current and purpose-built. V-Dem fully supersedes. |
| IRENA_POLICY | Deprioritized — not built | No clean downloadable renewable-policy dataset exists. IRENA's own downloads are statistics (capacity/generation/finance); its renewable-policy work is report-based analysis. The joint IEA/IRENA Policies & Measures DB (api.iea.org/policies?csv=true) has no clean renewable filter and would duplicate Climate Laws. Renewable deployment covered by IRENA capacity; energy/climate policy by Climate Laws; carbon pricing by WB Carbon; performance by EPI. |

**Fraser vs Heritage:** Fraser academically preferred — peer-reviewed, transparent weights, chain-linked. Heritage is policy-advocacy. Where they overlap, Fraser used.
**Fraser Area 4 (Trade Freedom):** Master PDF dropped it for Heritage overlap. Since Heritage TR deprioritized, Fraser Area 4 retained as primary trade openness index alongside KOF.

---

### Sources with Access Constraints

| Source | Constraint | Status |
|--------|-----------|--------|
| ACLED | Requires Research tier API access | Pending approval |
| BASEL_AML | Expert Edition requires institutional affiliation — personal email ineligible | Deferred |
| UCDP API | Token required since early in the year | Using bulk ZIP download instead |
| WHO GHO API | OData API deprecated | Subsumed by WDI |
| TI CPI | Direct Excel files password-protected | Using OWID instead |
| FSI | Latest editions not yet on download page | Data currency gap |
| OECD_TFI | JS-rendered simulator only — no API, not in OECD SDMX system (exhaustively verified) | Manual Category 4 |
| IMF Fiscal Rules | DataMapper blocked, no direct Excel URL | Manual Category 4 |
| IMF AREAER | Portal WAF-blocked + JS-gated (confirmed) | BUILT (FARI, manual export, notebook 32) |
| UNCTAD_NTM | Bulk download API returns 403; TRAINS portal JS-rendered | Manual Category 4 |
| RTI_RATING | Scores table is in page HTML (earlier auth-gated verdict WRONG) | BUILT (automated read_html, notebook 30) |
| REINHART_ROGOFF | Academic download; de facto FX regime | NEXT — PRIMARY tier-1 (complements AREAER), not low-priority |
| CLIMATE_LAWS | Registration form required (free) | BUILT (national-only cumulative stock) |
| PEW_GRI | Free account required | Manual Category 4 — obtained |
| IRENA_POLICY | No clean policy dataset exists | DEPRIORITIZED (see deprioritized table) |
| CIVICUS pre-window | CIVICUS API only returns recent years; earlier data not accessible via API | Historical gap — accepted |
| EPI | Only two most recent editions downloadable; no full archive | Cross-sectional limitation — accepted |

**Basel AML:** Expert Edition free for institutional users; personal email ineligible. Alternative: FATF scraper (Category 3).

---

### Sources Originally Listed as Manual That Are Now Automated

| Source | Original Category | Actual Access |
|--------|------------------|---------------|
| FSI | Cat 4 manual | Automated scrape |
| Fraser EFW | Cat 4 manual | Automated scrape |
| UCDP | Cat 4 manual | Automated bulk ZIP |
| TI CPI | Cat 4 manual | Automated via OWID |
| WJP | Cat 4 manual | Automated URL detection |
| FH FIW | Cat 4 manual | Automated URL detection |
| KOF_TRADE, PTS, OBS, ND_GAIN, GPI | Cat 4 manual | Via QoG |
| BCI, HANSON_SIGMAN, CCP, PEI, WB_INFORMAL, ROMELLI_CBI, POLITY5, NELDA | Cat 5 irregular | Via QoG |
| POWELL_THYNE | Cat 4 manual | Automated direct TXT |
| UNODC_HOMICIDE | Cat 4 manual | Automated via OWID |
| IRENA_CAPACITY | Cat 4 manual | Automated via OWID |
| IMF_IMAPP | Cat 4 manual | Automated ZIP, date auto-detection |
| YALE_EPI | Cat 4 manual | Automated scrape of downloads pages |
| WB_CARBON | Cat 4 manual | Automated via WB dashboard xlsx (existence/price/coverage/revenue) |
| DPI | Cat 4 manual | Automated via IDB CKAN API |
| CIVICUS | Cat 4 manual | Automated via REST API |

---

## Variable-Level Decisions

### Extraction grain verified against master PDF
A cross-check of extraction grain against the master PDF text confirmed:
- **FH FIW** — sub-category level (A, D, E, G; F reserved for Rule of Law) is CORRECT per master PDF ("disciplined extraction of just the sub-component"). Not a gap.
- **WJP** — individual factor level (Factors 2-8) is CORRECT per master PDF (factors mapped to specific concepts). Not a gap.
- **IMF SPI** — overall + 5 pillars (infrastructure, sources, products, services, use) is CORRECT per master PDF ("comprehensive: data infrastructure, sources, products, services, use"). Not a gap.
- **WB Carbon** — GAP RESOLVED. Master PDF specifies "carbon pricing existence AND design." Rebuilt from the WB Carbon Pricing Dashboard (replacing the OWID binary) to capture existence + price + jurisdictional coverage + revenue. See the dedicated WB Carbon methodology section below.

### V-Dem "factionalism" variable
No V-Dem variable named "faction"/"fract" exists. Master PDF label was conceptual. Factionalism covered by FSI C2 (Factionalized Elites). No VDEM_VARS change needed.

### FSI indicator naming
Master PDF mislabels C2 as "P1" and C3 as "S1". Pipeline correctly uses C2, C3.

### Fraser Area 2 — property sub-components
Master PDF specifies property sub-components only. Pipeline pulls full Area 2 aggregate. Metric-pass decision to select property-specific components.

### IRENA proxy
Master PDF calls for IRENA Renewables Capacity (MW). Using share of electricity from renewables (%) as proxy — more interpretable cross-country, normalises for country size.

### EPI cross-sectional limitation
Yale EPI makes only the two most recent editions downloadable. Pipeline stacks both on 8 consistent sub-indices; newer-edition-only sub-indices (MKP, MPE, MHP) are NaN for the earlier edition. Methodology differs between editions — limited comparability.

### IMF Fiscal Rules — quality not just presence
Initial extraction captured only binary presence of the four rule types (a shortcut). Reworked to extract presence AND quality dimensions per rule type (ER/RR/BBR/DR): legal basis (ordinal 1-5: political commitment → coalition → statutory → treaty → constitutional, per IMF codebook), formal enforcement, compliance; plus independent monitoring body, correction mechanism, well-defined triggers. Derived: count of rule types, max/mean legal basis, any enforcement. Column selection is robust NAME-BASED (composite keys from forward-filled parent header rows + un-filled leaf row, substring matching that fails loudly on rename) — replaced fragile position-based extraction.

### iMaPP — breadth not churn, and not in-force
Initial extraction captured tightening/loosening action counts + net + LTV_average. Reworked per analytical decision that the framework cares about regulatory framework *development*, not policy churn or direction. iMaPP records change events (+1/-1), not stock, so a reliable "currently in force" measure is NOT derivable (loosening ≠ removal; stable rules emit no events). Decision tree:
- **Rejected** tightening/loosening counts — measure churn/activity, not quality.
- **Rejected** "currently in force" via cumulative net-sign — misclassifies actively-managed instruments (loosening offsets); false precision.
- **Rejected** "recent window" activity — rewards churn; stable good rules drop out; converges to ever-engaged at long windows anyway.
- **Adopted** cumulative ENGAGEMENT BREADTH: count of distinct instruments (16; "Other"/OT excluded as heterogeneous) a country has ever taken action on, up to each year, total + by category (borrower-based: LTV/DSTI/LoanR/LCG; capital-based: CCB/Conservation/Capital/LVR/SIFI; liquidity-funding: Liquidity/LTD/LFX/LFC; provision-reserve-tax: LLP/RR/Tax).
- **Dropped** LTV_average — measures policy stance/stringency, not quality; its only quality-relevant content (presence) is already in the breadth count.
- Honest limitation: breadth is a proxy for framework development, NOT instruments-in-force and NOT a quality assessment. RR is noisy (IMF warns it mixes monetary + macroprudential). True quality assessment deferred to FSAP.
- Validation: China (16/16) and Korea (15) top the latest-year ranking — consistent with known comprehensive macroprudential users. Pakistan high (15) illustrates breadth ≠ quality.

### Upgrade path noted
- iMaPP "in-force" precision would require parsing the orange-tab text records for introduction/removal language — deferred unless metric pass needs current-stock.

---

### WB Carbon — national-only, with intensive/extensive EU split
Rebuilt from the World Bank Carbon Pricing Dashboard (month-stamped xlsx, auto-detected) to replace the prior OWID binary existence flag, per the master PDF's "existence AND design" requirement. Measures: existence flag, carbon price (US$/tCO2e, panel), revenue (US$m, panel), jurisdictional emissions coverage % (current snapshot).

Key methodological decisions:
- **National-only scope.** Scores sovereign-level governance. Subnational schemes (US states, Canadian provinces, Chinese pilots, Mexican states, Japanese cities) are excluded. Classification is fail-safe: an explicit national-name→ISO3 dictionary; any jurisdiction not resolving to a sovereign is excluded automatically (new subnational schemes auto-exclude; a new NATIONAL entrant requires a one-line dict addition — a flagged MANUAL UPDATE, with an in-pipeline diagnostic listing unmapped jurisdictions).
- **EU ETS handled by measure type (intensive vs extensive).** The EU ETS ("EU27+" = EU27 + Iceland, Liechtenstein, Norway) is expanded to all member states for INTENSIVE measures (price, coverage, existence — these apply identically to each member) but NOT for revenue (an EXTENSIVE total; fanning the single bloc figure to ~30 members would overstate ~30×). Revenue therefore counts only each country's own national-scheme revenue; EU members without a separate national scheme have no revenue value. Understates EU members' true carbon revenue but never overstates.
- **Within-country coverage = MAX across instruments** (the dashboard warns coverage figures are gross and overlap; max is conservative vs summing).
- **Mixed time basis:** price and revenue are full panels; jurisdictional coverage is a CURRENT SNAPSHOT (the only form the dashboard provides), broadcast across years with a `wb_carbon_coverage_is_snapshot` flag.
- **Skeleton = union** of all country-years with any carbon information (existence, coverage, price, or revenue), so no scheme/coverage country is silently dropped for lacking price/revenue. Countries with a scheme but no price/revenue series get a single current-year row (current year derived from the data).
- **Absence = INFERRED, not verified, non-existence.** A country absent from the panel may genuinely lack carbon pricing, OR have an out-of-scope instrument (dashboard tracks taxes/ETSs only), a subnational-only scheme (filtered out), an under-development scheme (existence requires Implemented), or be subject to reporting lag. At the metric pass, absent countries may be scored "no national carbon price" but should carry an inferred-absence flag. The WB dashboard is the most authoritative global tracker, so absence is decent evidence against a major national tax/ETS, but not definitive.
- **Revenue/GDP** to be computed downstream at the metric pass using WDI GDP, as an economic-materiality check (note: revenue understates free-allocation ETSs).
- **⚠️ Coverage:** ~71 countries — materially below the ~150 target, but this reflects the genuine concentration of carbon pricing, not a data defect. Flagged, not corrected.

### Climate Laws — national-only cumulative stock
Source: Climate Change Laws of the World (LSE Grantham / Climate Policy Radar), manual CSV (free registration), auto-detected in Downloads. Measures cumulative stock of domestic climate laws/policies per country-year (plus new-law annual flow).
- **UNFCCC category excluded** (international reporting — National Communications, NDCs, Global Stocktake submissions — not domestic governance). Legislative + Executive categories kept.
- **Deduplicated to Family ID** so document variants of one law count once.
- **NATIONAL-ONLY.** EU-level (EUR) documents are DROPPED — initially considered EU-expansion (attributing EU laws to members), but that double-counts EU law against members' own national transpositions (which are separately recorded), and the data has no reliable flag to identify transpositions. National records capture most transposed EU law anyway. Subnational tokens (e.g. BR-XX) dropped; the national code (BRA) is retained where present.
- Distinct laws counted per (country, Family ID) — never collapsed on (country, year), which would undercount.
- Malformed/missing dates dropped (a fixed 1900 plausibility floor, not a data vintage).
- Coverage: 199 countries — strong.

### ODIN — transparent aggregation, not the official index
Source: Open Data Inventory (Open Data Watch), manual ZIP of per-edition Excels, auto-detected by content validation (ZIP must contain year-named Excels, since the filename "2016-2024 data.zip" is unstable).
- The workbook has NO official country-level 0-100 index — only per-category element scores (0-10) across 22 data categories.
- Sub-scores (coverage, openness, overall) are a TRANSPARENT SIMPLE-MEAN aggregation of those category element scores — explicitly NOT ODIN's official national index (which uses ODIN's own category/element weighting and scaling). Raw ~0-2 scale; ranking is valid, absolute values for downstream normalization only.
- Coverage elements: indicator coverage, data availability (5/10yr), admin levels. Openness elements: machine readability, non-proprietary, download options, metadata, terms of use.
- Overlaps substantially with IMF SPI (statistical capacity) — ODIN's distinctive angle is open-data accessibility. Kept per user decision despite overlap.
- Biennial editions stacked. Coverage: 200 countries.

### Political Finance (IDEA) — directionally-defensible transparency score
Source ID retained as **TI_POLFINANCE** for continuity, but the structured data is from **International IDEA's Political Finance Database** (181 countries, 58 questions, launched 2003), NOT Transparency International. TI produces report-based analysis and standards, not a comparable structured country panel; IDEA is the authoritative structured source. Automated via a direct .xlsx export endpoint (`idea.int/data-tools/export?type=region_only&themeId=302&world=all`).

**What it measures — and critically, what it does NOT:**
- Measures the **de jure regulatory framework** (rules on paper) for money in politics.
- Does NOT measure enforcement, compliance, actual money/flows, or influence/corruption. IDEA explicitly states laws on the books ≠ adherence. The de jure/de facto gap is real (e.g. the USA scores high on disclosure *rules* despite well-known money-in-politics concerns). Enforcement/outcome dimensions are covered elsewhere (V-Dem political-finance items, WGI/V-Dem corruption indices).

**Directionality judgment (the heart of this pipeline — a documented exception to no-hardcoding):**
Of the 58 questions, ~43 are binary (Yes/No), but "Yes" is NOT uniformly "better governance." A naive density count would embed the contestable assumption IDEA warns against. We therefore score an **equal-weighted mean of only the 20 binary questions where "Yes = better governance" is defensible**, hand-curated and specified explicitly in the pipeline:
- **INCLUDED (20):** foreign-donation bans (Q1-2), anonymous-donation bans (Q7-8), government-contractor donation bans (Q9-10), partial-state-owned-firm donation bans (Q11-12), abuse-of-state-resources ban (Q13), procurement-linked-donor ban (Q26), banking-system requirement (Q27), vote-buying ban (Q38), and ALL of reporting/oversight/disclosure (Q47-54). These are transparency, anti-corruption-source, and oversight provisions with defensible directionality.
- **EXCLUDED — contested or reverse-signed:** corporate/union donation bans (Q3-6, ban-vs-disclosure is a legitimate model choice); ALL contribution and spending limits (Q14-22, Q39-46, speech-vs-fairness tension, constitutionally barred in some democracies); party commercial-activity and loan bans (Q23-25, can perversely weaken party independence); ALL public funding (Q28-37, a model choice orthogonal to governance quality).
- The resulting construct is best read as **political-finance transparency & oversight**, not "regulation breadth" or "integrity."

**Other decisions:**
- Binary questions auto-detected by answer-set membership (Yes/No/Sometimes/No data/Not applicable ≥80%); the 20 included are then selected by explicit (category, question-number) list.
- Coding: Yes=1, No=0, Sometimes=0.5; No data / Not applicable -> NaN (excluded from the mean).
- **Reliability floor:** countries answering <10 of the 20 included questions have their score set to NaN but are kept in the file (3 countries: SWZ, GNQ, STP); `polfin_n_answered` carries the count. Zero-answer rows (43 — authoritarian one-party states and small dependencies with no party-finance regime to code) are dropped entirely.
- Regional aggregates excluded; sovereign ISO3 only.
- Wave-updated cross-section (questions revised 2012/2016/2018/2020/2022; 2023 update refreshed 25 countries). The export carries no data-year column, so `data_as_of_date` is the retrieval date with a note that the true vintage is IDEA's latest update round.
- Coverage: 180 countries (177 scored).

### Concept 25 reconsideration + GDB decision (revisited)
The master PDF flagged Concept 25 (Government transparency and openness) for reconsideration due to heavy indicator overlap — only the IDEA Political Finance Database and the Global Data Barometer (GDB) are unique to it; its other sources (Open Budget Survey, RTI Rating, WJP Factor 3, V-Dem transparency indicators) are primary in other concepts (PFM, Media Freedom, Legal Quality).

**Decision (this pass): KEEP Concept 25 as a standalone concept.** "Government transparency and openness" is a coherent, investor-legible governance dimension; the overlap is tracked under the framework's repetition rule. Architectural argument for absorption (it is thematically rather than functionally defined) noted but not adopted. Still flagged to revisit with the full framework view before finalising.

**Measurement state (honest):** Concept 25's legal-framework legs are well-measured (RTI Rating, Open Budget Survey, IDEA Political Finance [built], V-Dem disclosure indicators). Its practice/sector legs are under-measured and remain v1 gaps: procurement transparency (no adequate cross-country source), lobbying transparency (very thin globally), de facto vs de jure disclosure, and open data (thin sources). These are candidates for the planned PDF-extraction / qualitative work, or accepted as v1 limitations.

**GDB (Global Data Barometer): DEPRIORITIZED — not built.** Although the master PDF lists GDB as the supplementary open-data source for Concept 25 (successor to the defunct Open Data Barometer), on review it is thin (~43-109 countries, edition-unstable, not a panel) and duplicates ODIN's open-data coverage (ODIN is already in the framework, primary in Statistical Infrastructure / cross-referenced in C25). Crucially, GDB does NOT fill Concept 25's actual measurement gaps (procurement, lobbying, de facto practice). Its marginal contribution over ODIN is too small to justify a pipeline. This is a deliberate departure from the master PDF's "supplementary, build it" treatment, documented here; the open-data leg of C25 is served (adequately if not ideally) by ODIN.

### RTI Rating — automated HTML parse, no-law floor methodology
Source: Global Right to Information Rating (Centre for Law and Democracy / Access Info Europe). PRIMARY tier-1 source for Government transparency (Concept 25, FOI/RTI leg) AND Media Freedom (Concept 23). Earlier parked as "auth-gated AJAX" — that was wrong: the full scores table is in the country-data page HTML and parses cleanly with pandas.read_html. Automated, no auth.

**What it measures:** strength of the legal framework for the right to information — rti_total (0-150) plus 7 category sub-scores (Right of Access, Scope, Requesting Procedure, Exceptions & Refusals, Appeals, Sanctions & Protections, Promotional Measures). DE JURE only; does NOT measure implementation (CLD's parallel implementation project is rti-evaluation.org — separately assessed).

**Aggregation:** we use CLD's OWN published Total (a weighted sum of 61 indicators where categories carry different point maxima — Scope/Appeals/Exceptions/Requesting each up to 30, Promotional 16, Sanctions 8, Right of Access 6). We do NOT compute our own combination; inheriting the authoritative weighting is the low-assumption choice. The 7 sub-scores are retained so the metric pass could re-weight (e.g. emphasising enforcement/oversight) if ever justified — a deliberate departure that would need explicit reasoning.

**No-law countries (a documented SCORING CHOICE):** 142 countries have an RTI law (real scores, has_rti_law=1). 54 countries with NO RTI law (taken from the deficit-list file's flag column, URL extracted dynamically from the page) are assigned a floored rti_total = (minimum observed total − 1 SD of the rated distribution), clamped ≥ 0 (currently = 9.3), with NaN sub-scores and has_rti_law=0. Rationale: "no law" is genuinely worse than the weakest law on a DE JURE dimension (a weak law still creates a right, an oversight body, an appeals mechanism; no law provides none), so it belongs below the floor — but a flat 0 overstated the gap and asserted a precise measured value where there is none. Min-minus-1SD places no-law countries below all laws by a statistically meaningful, data-derived margin. This is an assigned floor, NOT a measured value; the has_rti_law flag keeps it identifiable and the choice revisable at the metric pass.

**De facto implementation (rti-evaluation.org) — deprioritized:** CLD's parallel RTI *implementation* assessment is a bespoke country-by-country methodology applied ad hoc (Afghanistan was only the 2nd country; also Kenya, Pakistan provinces), in heterogeneous per-country PDF reports with country-specific customization, at different times and funders. Coverage is a handful of countries — far below the ~150 target and not a comparable panel — so it is NOT viable as a cross-country input. De facto RTI implementation is therefore a known v1 GAP, partially covered by V-Dem's transparency/disclosure practice measures (~180 countries, expert-coded). rti-evaluation flagged as a watch item if its coverage ever expands materially.

**Other:** ISO3 via pycountry + manual fixes; cross-section (historical time series deferred — RTI scores are sticky step-functions, low marginal value for a v1 cross-sectional framework; logged as a deferred enhancement). Coverage: 196 countries — the strongest in the framework.

### IMF AREAER — capital-account dimension resolved (manual FARI + automated derivatives)
The master PDF's AREAER row (PRIMARY tier-1: "exchange rate regime de jure and de facto"; universal IMF members) covers two dimensions — capital-account restrictiveness and exchange-rate-regime classification. Access resolution:

**Portal CONFIRMED blocked.** elibrary-areaer.imf.org Data Query and Indices pages return "The requested URL was rejected" (F5/ASM web-application-firewall block) and are JS-gated. Genuinely not automatable programmatically. The original "portal-based, no direct download" assessment was correct.

**Resolution — three complementary sources for one framework row:**
1. **IMF AREAER FARI (BUILT, manual).** The Financial Account Restrictiveness Index (capital-account restrictiveness, de jure, 0-1 higher=more restrictive) is exported by hand from the portal's Indices tab. Built notebook 32. fari_aggregate + fari_fdi_aggregate are the PRIMARY scored fields; inflow/outflow splits retained as supplementary. 194 countries, 1999-2024 (2024 partial per source). This is the IMF-NATIVE authoritative measure. MANUAL SNAPSHOT — refreshed by re-exporting each cycle. Direction validated (Hong Kong 0.02 / Singapore 0.05 open; Bangladesh 0.77 closed). The FDI sub-index is a genuine advantage over derivative indices (which collapse to a single number and cannot isolate FDI).
2. **Chinn-Ito KAOPEN (NEXT, automated).** The most-cited academic capital-account-openness index, derived from the SAME AREAER source data, freely downloadable (web.pdx.edu/~ito, year-stamped file, URL parsed dynamically). ~181 countries, 1970-2023. NOT more authoritative than AREAER — it is a derivative; used as the automatable broad-time-series complement / cross-check. Fragile personal-page URL flagged.
3. **Reinhart-Rogoff (NEXT).** De facto exchange-rate-regime classification (PRIMARY tier-1, complements AREAER's de jure focus, ~190 countries). Clean academic download. Covers the exchange-rate-regime dimension that FARI/KAOPEN (capital-account) do not.

**ACI (AREAER Change Index)** was also downloaded (companion file) but NOT built into the score: it measures policy *changes* (tightening/easing actions, a direction-of-travel signal), a different construct from FARI's *level* of restrictiveness. Deferred as optional supplementary (on hand if a policy-trajectory dimension is later added).

## Pipelines Built

| Notebook | Source | Output File | Indicators | Coverage |
|----------|--------|-------------|------------|----------|
| 03_vdem | V-Dem | vdem_filtered.csv | 64 | full series, ~181 countries |
| 04_wgi | WB WGI | wgi_clean.csv | 6 | from mid-1990s, 215 countries |
| 05_wjp | WJP | wjp_clean.csv | 8 factors + 6.5 | from early 2010s, 143 countries |
| 06_fh_fiw | FH FIW | fh_fiw_clean.csv | 4 sub-components | from early 2010s, 195 countries |
| 07_fsi | FSI | fsi_clean.csv | 4 | from mid-2000s, 179 countries |
| 08_ti_cpi | TI CPI | ti_cpi_clean.csv | 1 | from early 2010s, 182 countries |
| 09_wdi | WB WDI (34 indicators) | wdi_clean.csv | 34 | full series, 266 economies |
| 10_imf_spi | IMF SPI | spi_clean.csv | 6 | from mid-2000s, 221 countries |
| 11_acled | ACLED | — | — | Pending Research tier |
| 12_ucdp | UCDP | ucdp_clean.csv | 16 | full series, 199 countries |
| 13_fraser | Fraser EFW | fraser_clean.csv | 3 areas | full series, 165 countries |
| 14_qog | QoG Standard TS (13 sources) | qog_clean.csv | 36 | full series, 200 countries |
| 15_powell_thyne | Powell-Thyne | powell_thyne_clean.csv | 4 | full series, 204 countries |
| 16_unodc | UNODC Homicide | unodc_clean.csv | 1 | full series, 208 countries |
| 17_irena | IRENA | irena_clean.csv | 1 | full series, 226 countries |
| 18_imapp | IMF iMaPP | imapp_clean.csv | 5 (breadth total + 4 category) | full series, 135 countries |
| 19_epi | Yale EPI | epi_clean.csv | 11 | two most recent editions, 180 countries |
| 20_wb_carbon | WB Carbon | wb_carbon_clean.csv | 4 (existence, price, coverage, revenue) | price/revenue panels + coverage snapshot, 71 countries |
| 21_dpi | DPI | dpi_clean.csv | 31 | full series, 182 countries |
| 22_civicus | CIVICUS | civicus_clean.csv | 2 | recent years only, 199 countries |
| 23_idea_partip | IDEA GSoD | idea_gsod_clean.csv | 13 | full series, 174 countries |
| 24_pew_gri | Pew GRI | pew_gri_clean.csv | 2 | from mid-2000s, 198 countries |
| 25_imf_fiscal_rules | IMF Fiscal Rules | imf_fiscal_rules_clean.csv | 28 (presence + quality) | full series, 123 countries |
| 26_climate_laws | Climate Laws (LSE/CPR) | climate_laws_clean.csv | 2 (cumulative stock + new flow) | full series, 199 countries |
| 27_odin | ODIN (Open Data Watch) | odin_clean.csv | 3 (coverage, openness, overall) | biennial editions, 200 countries |
| 29_polfinance | IDEA Political Finance DB | polfinance_clean.csv | 1 score + n_answered | cross-section, 180 countries (177 scored) |
| 30_rti_rating | RTI Rating (CLD/Access Info) | rti_rating_clean.csv | total + 7 sub-scores + has_rti_law | cross-section, 196 countries (142 rated + 54 no-law) |
| 32_areaer_fari | IMF AREAER (FARI) | areaer_fari_clean.csv | 6 (aggregate + FDI aggregate + 4 inflow/outflow splits) | 1999-2024 panel, 194 countries |

---

## Consolidated Build Status (by source)

**As-of: 2026-06-18. MANUAL SNAPSHOT — does not auto-update.** Single at-a-glance view of every source's status. Authoritative structured records remain `download_log` (currency/filenames) and `source_registry.csv` (access methods). Legend: ✅ Built · ⏳ Next/in-progress · ⏸ Deferred (access pending or v2) · ❌ Deprioritized · 🔒 Blocked-not-built.

| Source | Status | Access | Output / Note |
|--------|--------|--------|---------------|
| V-Dem | ✅ | Automated | vdem_filtered.csv |
| WB WGI | ✅ | Automated | wgi_clean.csv |
| WJP | ✅ | Automated (URL detect) | wjp_clean.csv |
| FH FIW | ✅ | Automated (URL detect) | fh_fiw_clean.csv |
| FSI | ✅ | Automated scrape | fsi_clean.csv (currency gap: latest editions not posted) |
| TI CPI | ✅ | Automated (via OWID) | ti_cpi_clean.csv (direct files password-protected) |
| WB WDI (34 ind.) | ✅ | Automated | wdi_clean.csv |
| IMF SPI | ✅ | Automated | spi_clean.csv |
| UCDP | ✅ | Automated bulk ZIP | ucdp_clean.csv (API token avoided via ZIP) |
| Fraser EFW | ✅ | Automated scrape | fraser_clean.csv |
| QoG Standard TS (13 sub-sources) | ✅ | Automated | qog_clean.csv (subsumes Polity5, NELDA, Romelli CBI, Hanson-Sigman, BCI, CCP, WB Informal, PEI, GPI, OBS, ND_GAIN, KOF_TRADE, PTS) |
| Powell-Thyne | ✅ | Automated direct TXT | powell_thyne_clean.csv |
| UNODC Homicide | ✅ | Automated | unodc_clean.csv |
| IRENA (capacity) | ✅ | Automated | irena_clean.csv |
| IMF iMaPP | ✅ | Automated | imapp_clean.csv |
| Yale EPI | ✅ | Automated | epi_clean.csv (two latest editions only) |
| WB Carbon | ✅ | Automated | wb_carbon_clean.csv (71 countries, thin) |
| DPI | ✅ | Automated | dpi_clean.csv |
| CIVICUS | ✅ | Automated | civicus_clean.csv (recent years only) |
| IDEA GSoD | ✅ | Automated | idea_gsod_clean.csv |
| Pew GRI | ✅ | Manual (free account) | pew_gri_clean.csv |
| IMF Fiscal Rules | ✅ | Manual (DataMapper blocked) | imf_fiscal_rules_clean.csv |
| Climate Laws (LSE/CPR) | ✅ | Manual (free registration) | climate_laws_clean.csv (national-only) |
| ODIN (Open Data Watch) | ✅ | Manual ZIP | odin_clean.csv |
| IDEA Political Finance | ✅ | Automated (.xlsx export) | polfinance_clean.csv (de jure only) |
| RTI Rating (CLD) | ✅ | Automated (read_html) | rti_rating_clean.csv (196 countries — broadest) |
| IMF AREAER (FARI) | ✅ | Manual (portal WAF-blocked) | areaer_fari_clean.csv (194 countries, 1999-2024) |
| Chinn-Ito (KAOPEN) | ⏳ | Automated | capital-account derivative of AREAER; complement/cross-check |
| Reinhart-Rogoff | ⏳ | Manual/academic | de facto FX regime; PRIMARY tier-1, complements AREAER |
| OECD TFI | 🔒 | JS simulator, no API (verified) | trade administration; email-to-OECD route prepared, unsent |
| UNCTAD NTM | 🔒 | Bulk API 403; TRAINS JS-gated | sole source for non-tariff barriers — real gap if unbuilt |
| ACLED | ⏸ | Research-tier API | pending approval |
| Basel AML | ⏸ | Institutional affiliation required | personal email ineligible; FATF scrape as alt |
| Global Data Barometer | ❌ | (accessible) | thin (~43-109, unstable), duplicates ODIN, doesn't fill C25 gaps |
| IRENA Policy | ❌ | (no clean dataset exists) | renewable policy is report-based; Climate Laws covers |
| rti-evaluation.org | ❌ | (bespoke per-country reports) | de facto RTI implementation; too thin/heterogeneous |
| RSF WPFI | ❌ | — | media freedom covered by V-Dem; methodology break |
| Heritage TR / PR | ❌ | — | Fraser Area 4 / Area 2+WJP+V-Dem supersede |
| Dincer-Eichengreen CB | ❌ | — | stale; Romelli CBI (in QoG) supersedes |
| Linzer-Staton | ❌ | — | stale/discontinued; V-Dem judicial indicators supersede |
| SOE governance (Concept) | ⏸ | — | deferred to v2 (thinnest concept) |

**Category 1 PDF-extraction sources (not started):** PEFA, IMF FSAP, ICNL, plus multi-source infrastructure (IMF Article IVs + WB CCDRs, political-economy/institutional focus); IRENA renewable-targets to be added here.
**Category 3 web scrapes (not started):** FATF, IPU PARLINE, WTO TFA, IMF SDDS, CPJ.


## Outstanding Decisions

- KOF_TRADE: separate KOF pipeline for trade sub-index vs accept dr_eg proxy — pending
- ACLED: complete once Research tier approved
- BASEL_AML: complete once Expert Edition access obtained
- Concept 25 (Government transparency): reconsider before finalizing — indicator overlap
- SOE Governance (Concept 10): deferred to v2
- EPI sub-components: select policy/institutional sub-components at metric pass
- IRENA renewable-energy TARGETS (national ambition signal, e.g. % renewable by year): a genuinely additive policy measure, but only available embedded in IRENA reports/NDC analysis — DEFERRED to the planned Category 1 PDF-extraction infrastructure, not a clean download
- RTI Rating HISTORICAL time series / transparency TRAJECTORY (is a country's RTI framework improving or backsliding): deferred — RTI scores are sticky step-functions so annual history adds little for a v1 cross-section, but a trajectory/direction-of-travel dimension (applicable to several de jure sources) could use it later
- iMaPP in-force precision: parse text records if current-stock needed (deferred)
- WGI standard errors: optional enhancement for ranking confidence — not a master-PDF gap, user discretion
- Category 3 web scrapes not built: FATF, IPU_PARLINE, WTO_TFA, IMF_SDDS, CPJ
- Category 4 manual not built: OECD_TFI, IMF_AREAER, UNCTAD_NTM, REINHART_ROGOFF (ODIN, CLIMATE_LAWS, TI_POLFINANCE, RTI_RATING built; IRENA_POLICY and GLOBAL_DATA_BAROMETER deprioritized). RTI_RATING turned out automatable (HTML table parse) despite the earlier auth-gated-AJAX verdict — primary tier-1, 196 countries, now built.
- Category 1 PDF extraction not built: PEFA, IMF_FSAP (macroprudential + financial-sector quality assessment), ICNL

---

*This document to be deleted when master PDF is regenerated at end of pipeline build phase.*
