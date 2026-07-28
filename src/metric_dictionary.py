"""metric_dictionary - operational description of each SCORED metric.

Companion to metric_selection.py. Selection owns WHAT is scored (concept, tier,
direction, inclusion). This file owns HOW each scored metric is computed. The two
join on the metric name `m`; they hold disjoint information and cannot contradict.
Only scored metrics appear here (exclusions carry their reason in selection.why).

Three-stage calculation, kept separate on purpose:
  source_reports       - the provider's raw variable(s), native encoding and units,
                         before we touch anything. Describes the SOURCE.
  standalone_transform - country-independent recode to a clean metric value
                         (recodes, component means, unit changes, functional
                         transforms). Runs on ONE country in isolation. Ours.
  panel_scaling        - cross-sectional placement into a comparable score
                         (percentile / z / fixed-anchor, winsorize, missingness
                         penalty, spine zero-fill). Needs the WHOLE panel. Ours.
                         Usually TBD until Step-3.

status: 'selected' = source_reports + standalone_transform locked at Step-1,
         panel_scaling TBD at Step-3. 'built' = all fields final.

 BUILD-STATUS DISCIPLINE (added 2026-07-24): describe only what EXISTS.
   - standalone_transform = what a SOURCE PIPELINE (nb 03-40) actually does today.
     In-source aggregations (FATF IO-mean, BRSS weighted mean, ODIN category-mean,
     iMaPP breadth, Climate-Laws cumulative, compliance mean) ARE built - read from code.
   - Anything computed LATER (log1p, per-capita, min-max, percentile, winsorize,
     missingness penalty, spine zero-fill, cross-coder means like PTS, tier weighting)
     is NOT built: the scoring/normalization layer does not exist yet. nb 39 only
     PROPOSES a per-metric method (metric_distribution_profile.csv); human disposes at
     Step 1/3. So panel_scaling states 'NOT BUILT yet' before naming the planned method.
 """

DICT = {

 # ================= WGI (World Bank Worldwide Governance Indicators) =================
 # 3 of 6 WGI indicators scored; the other 3 are category cross-checks (see metric_selection).
 # All three share the World Bank estimate scale and are used exactly as published.

 "wgi_political_stability": dict(
     definition = "How stable a country's government is, and how free it is from political violence and terrorism. World Bank's Political Stability indicator.",
     source_reports = "World Bank Worldwide Governance Indicators, code GOV_WGI_PV.EST. Published as a score from about -2.5 (least stable) to +2.5 (most stable), where 0 is roughly the world average that year. Updated yearly since 2003 (every two years before that).",
     standalone_transform = "None. We use the World Bank's published score as-is.",
     panel_scaling = "Decided at Step 3: the -2.5 to +2.5 score will be converted to the common framework scale.",
     units = "Score about -2.5 (worst) to +2.5 (best). Higher is better.",
     coverage = "Nearly every country (200+). Exact latest-year count not measured, as coverage this broad affects no decision.",
     caveats = "COMBINED index: the World Bank builds it by averaging many other sources, so it overlaps with several metrics we use and we treat it as a broad cross-check, not an independent signal. We never use how closely a metric tracks WGI to decide inclusion, only to check direction. Scores Concept 2 (Political stability and government continuity).",
     status = "selected",
 ),

 "wgi_government_effectiveness": dict(
     definition = "How well a country's government delivers public services, sets and carries out policy, and runs a competent civil service free of political interference. World Bank's Government Effectiveness indicator.",
     source_reports = "World Bank Worldwide Governance Indicators, code GOV_WGI_GE.EST. Same scale as the other WGI indicators: about -2.5 (worst) to +2.5 (best), 0 is roughly the world average that year. Updated yearly since 2003.",
     standalone_transform = "None. We use the World Bank's published score as-is.",
     panel_scaling = "Decided at Step 3: the -2.5 to +2.5 score will be converted to the common framework scale.",
     units = "Score about -2.5 (worst) to +2.5 (best). Higher is better.",
     coverage = "Nearly every country (200+). Exact latest-year count not measured, as coverage this broad affects no decision.",
     caveats = "COMBINED index (see wgi_political_stability): overlaps with other metrics, used as a cross-check; direction-only for the WGI-correlation rule. Scores Concept 4 (Government effectiveness and administrative capacity).",
     status = "selected",
 ),

 "wgi_regulatory_quality": dict(
     definition = "How well a country designs and applies rules and regulations that let the private sector work - avoiding both red tape and gaps that let harm through. World Bank's Regulatory Quality indicator.",
     source_reports = "World Bank Worldwide Governance Indicators, code GOV_WGI_RQ.EST. Same scale as the other WGI indicators: about -2.5 (worst) to +2.5 (best), 0 is roughly the world average that year. Updated yearly since 2003.",
     standalone_transform = "None. We use the World Bank's published score as-is.",
     panel_scaling = "Decided at Step 3: the -2.5 to +2.5 score will be converted to the common framework scale.",
     units = "Score about -2.5 (worst) to +2.5 (best). Higher is better.",
     coverage = "Nearly every country (200+). Exact latest-year count not measured, as coverage this broad affects no decision.",
     caveats = "COMBINED index (see wgi_political_stability): overlaps with other metrics, used as a cross-check; direction-only for the WGI-correlation rule. Scores Concept 6 (Regulatory quality and business environment).",
     status = "selected",
 ),

# ================= Fraser Institute — Economic Freedom of the World =================

 "fraser_trade_freedom": dict(
     definition = "How free a country is to trade internationally - low tariffs, few trade barriers, few capital and exchange controls. Fraser Institute's Area 4 (Freedom to Trade Internationally).",
     source_reports = "Fraser Institute Economic Freedom of the World, Area 4 score. Published 0-10, higher = freer trade. Annual from 2000, every five years before that.",
     standalone_transform = "None. We use Fraser's published 0-10 area score as-is.",
     panel_scaling = "Decided at Step 3: the 0-10 score will be converted to the common framework scale.",
     units = "Score 0-10. Higher is better (freer).",
     coverage = "About 165 countries.",
     caveats = "Supersedes the older Heritage Trade Freedom measure (documented). Scores Concept 11 (Trade governance).",
     status = "selected",
 ),

 "fraser_regulation": dict(
     definition = "How lightly and sensibly a country regulates credit, labour, and business - avoiding costly or arbitrary rules. Fraser Institute's Area 5 (Regulation).",
     source_reports = "Fraser Institute Economic Freedom of the World, Area 5 score. Published 0-10, higher = lighter/better-designed regulation. Annual from 2000, every five years before that.",
     standalone_transform = "None. We use Fraser's published 0-10 area score as-is.",
     panel_scaling = "Decided at Step 3: the 0-10 score will be converted to the common framework scale.",
     units = "Score 0-10. Higher is better.",
     coverage = "About 165 countries.",
     caveats = "Scores Concept 6 (Regulatory quality and business environment).",
     status = "selected",
 ),

 "fraser_legal_system": dict(
     definition = "How strong a country's legal system and property rights are - judicial independence, impartial courts, protection of property, enforcement of contracts. Fraser Institute's Area 2 (Legal System and Property Rights).",
     source_reports = "Fraser Institute Economic Freedom of the World, Area 2 score. Published 0-10, higher = stronger legal system and property protection. Annual from 2000, every five years before that.",
     standalone_transform = "None. We use Fraser's published 0-10 area score as-is.",
     panel_scaling = "Decided at Step 3: the 0-10 score will be converted to the common framework scale.",
     units = "Score 0-10. Higher is better.",
     coverage = "About 165 countries.",
     caveats = "We score the whole Area 2 aggregate. There is an OPEN item (see framework_decisions): the concept calls for a property-rights-specific sub-component, but the cleaned Fraser file carries only the area totals, so this uses the full area for now. Scores Concept 17 (Property rights and contract enforcement).",
     status = "selected",
 ),

 # ================= Pew Research — Religious Restrictions =================
 # Both indices run 0-10 where HIGHER = MORE restriction/hostility = WORSE (direction is negative).

 "pew_gov_restrictions_index": dict(
     definition = "How much a government restricts religious beliefs and practices through laws, policies, and official actions. Pew's Government Restrictions Index.",
     source_reports = "Pew Research Center, Government Restrictions Index (GRI). Published 0-10, where HIGHER means MORE restriction. Annual.",
     standalone_transform = "None. We use Pew's published 0-10 index as-is.",
     panel_scaling = "Decided at Step 3: the 0-10 index will be converted to the common framework scale, inverting so that less restriction scores better.",
     units = "Index 0-10. Higher is WORSE (more restriction). Direction is negative.",
     coverage = "About 198 countries.",
     caveats = "Direction verified against the data: New Zealand 0.35 (low restriction), China 9.09 (high). Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 "pew_social_hostilities_index": dict(
     definition = "How much religious hostility comes from private actors in society - mob or sectarian violence, harassment, terrorism over religion. Pew's Social Hostilities Index.",
     source_reports = "Pew Research Center, Social Hostilities Index (SHI). Published 0-10, where HIGHER means MORE hostility. Annual.",
     standalone_transform = "None. We use Pew's published 0-10 index as-is.",
     panel_scaling = "Decided at Step 3: the 0-10 index will be converted to the common framework scale, inverting so that less hostility scores better.",
     units = "Index 0-10. Higher is WORSE (more hostility). Direction is negative.",
     coverage = "About 198 countries.",
     caveats = "Measures societal hostility (private actors), the companion to GRI's government restriction. Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 # ================= ODIN — Open Data Inventory (Open Data Watch) =================
 # IMPORTANT: these are NOT ODIN's official national index. We build them ourselves by
 # simple-averaging ODIN's published category scores; the scale is a raw ~0-2, not rescaled.

 "odin_openness": dict(
     definition = "How openly a country publishes its official statistics - machine-readable formats, non-proprietary files, download options, metadata, clear terms of use. Built from Open Data Watch's ODIN openness elements.",
     source_reports = "Open Data Watch, ODIN. ODIN publishes per-category element scores (each roughly 0-10) but no single official openness number at the scale we need. Biennial editions.",
     standalone_transform = "WE BUILD THIS. We take ODIN's five openness elements (machine readability, non-proprietary, download options, metadata, terms of use), average them across ODIN's data categories, then average those - a transparent simple mean. This is NOT ODIN's official weighting. The result sits on a raw relative scale (roughly 0-2), deliberately not rescaled.",
     panel_scaling = "Decided at Step 3: this raw ~0-2 score will be converted to the common framework scale. Rankings are meaningful now; the absolute numbers exist only to feed that later step.",
     units = "Built score, raw relative scale (~0-2). Higher is better (more open).",
     coverage = "See the ODIN edition; roughly 190 countries.",
     caveats = "OUR aggregation, not ODIN's published index (which uses ODIN's own weighting and 0-100 scaling). Overlaps substantially with the IMF SPI statistical-capacity metric. Scores Concept 3 (Statistical capacity and data transparency).",
     status = "selected",
 ),

 "odin_overall": dict(
     definition = "A country's overall open-data performance - the average of its data openness and its data coverage. Built from Open Data Watch's ODIN scores.",
     source_reports = "Open Data Watch, ODIN. Same source as odin_openness; ODIN publishes per-category element scores, not a single official number at the scale we need. Biennial editions.",
     standalone_transform = "WE BUILD THIS. Simple mean of our two built ODIN sub-scores (odin_openness and odin_coverage). Same raw ~0-2 relative scale, not rescaled. Not ODIN's official national index.",
     panel_scaling = "Decided at Step 3: this raw ~0-2 score will be converted to the common framework scale.",
     units = "Built score, raw relative scale (~0-2). Higher is better.",
     coverage = "See the ODIN edition; roughly 190 countries.",
     caveats = "OUR aggregation, not ODIN's published index. Scored as a Supplementary leg of Concept 25 (Government transparency and openness). See odin_openness for the aggregation detail.",
     status = "selected",
 ),

 # ================= CIVICUS Monitor =================

 "civicus_score": dict(
     definition = "How open and protected civic space is - the freedom to associate, assemble, and speak without state repression. CIVICUS Monitor's underlying numeric score.",
     source_reports = "CIVICUS Monitor, via its public API. A numeric civic-space score (the basis for CIVICUS's five-point Open/Narrowed/Obstructed/Repressed/Closed rating). Higher = more open.",
     standalone_transform = "None. We use the API's numeric score as-is (keeping the latest rating in each calendar year).",
     panel_scaling = "Decided at Step 3: the score will be converted to the common framework scale.",
     units = "CIVICUS numeric score. Higher is better (more open civic space).",
     coverage = "About 199 countries, but ONLY from 2022 onward - the API returns no earlier data even though CIVICUS launched in 2016. This is a real recency floor to be aware of.",
     caveats = "The five-point categorical rating (Open/Narrowed/...) is the published headline; we score the finer numeric score behind it and drop the coarser rating. Scores Concept 21 (Political participation beyond voting) and Concept 24 (Civil society space and vitality).",
     status = "selected",
 ),

# ================= QoG-sourced (Quality of Government Standard dataset) =================
 # QoG re-serves other providers' variables unchanged. We pull the named variable and
 # use it as-published; the ORIGINAL provider is what matters for interpretation.

 "bci_corruption_index": dict(
     definition = "How corrupt a country is overall, pooled statistically from many existing corruption measures. The Bayesian Corruption Indicator.",
     source_reports = "Bayesian Corruption Indicator (Standaert), obtained via the Quality of Government dataset (QoG variable bci_bci). A model that combines many published corruption indicators into one score. HIGHER means MORE corruption.",
     standalone_transform = "None. QoG carries the indicator unchanged; we use it as-is.",
     panel_scaling = "Decided at Step 3: converted to the common framework scale, inverting so that less corruption scores better.",
     units = "Index (roughly 0-100 style). Higher is WORSE (more corruption). Direction is negative.",
     coverage = "Broad, most countries.",
     caveats = "Direction verified against the data: Finland scores low (-3.5, clean), Guinea-Bissau high (78.9, corrupt). Being a POOLED index, it shares inputs with other corruption metrics we use (e.g. TI CPI) - treat as convergent evidence, not fully independent. Scores Concept 18 (Control of corruption).",
     status = "selected",
 ),

 "gpi_peace_index": dict(
     definition = "How peaceful a country is - levels of violence, conflict, militarization, and personal safety. The Global Peace Index.",
     source_reports = "Global Peace Index (Institute for Economics and Peace), via the Quality of Government dataset (QoG variable gpi_gpi). HIGHER means LESS peaceful (more violence/conflict).",
     standalone_transform = "None. QoG carries the index unchanged; we use it as-is.",
     panel_scaling = "Decided at Step 3: converted to the common framework scale, inverting so that more peaceful scores better.",
     units = "Index (roughly 1-5). Higher is WORSE (less peaceful). Direction is negative.",
     coverage = "About 160+ countries.",
     caveats = "Scores two concepts: Concept 2 (Political stability and government continuity) and Concept 16 (Personal security and public order).",
     status = "selected",
 ),

 "obs_open_budget_index": dict(
     definition = "How transparent a government's budget is - how much budget information it publishes and how accessible it is to the public. The Open Budget Index.",
     source_reports = "Open Budget Index (International Budget Partnership), via the Quality of Government dataset (QoG variable ibp_obi). Published 0-100, higher = more budget transparency.",
     standalone_transform = "None. QoG carries the index unchanged; we use it as-is.",
     panel_scaling = "Decided at Step 3: the 0-100 index will be converted to the common framework scale.",
     units = "Index 0-100. Higher is better (more transparent).",
     coverage = "About 120 countries.",
     caveats = "Scores two concepts: Concept 7 (Public financial management) as a primary leg, and Concept 25 (Government transparency and openness) as a supporting leg.",
     status = "selected",
 ),

 "pei_electoral_integrity_index": dict(
     definition = "How much integrity a country's elections have - fairness of the process from laws and boundaries through voting, counting, and results. The Perceptions of Electoral Integrity index.",
     source_reports = "Perceptions of Electoral Integrity (Norris and colleagues), via the Quality of Government dataset (QoG variable pei_peii_1). An expert-survey index of election quality, higher = more integrity.",
     standalone_transform = "None. QoG carries the index unchanged; we use it as-is.",
     panel_scaling = "Decided at Step 3: converted to the common framework scale.",
     units = "Index (roughly 0-100). Higher is better (more electoral integrity).",
     coverage = "Countries that held elections in the covered period. Measured PER ELECTION, not every year, so a country only has a value in years it held a national election - expect high missingness between elections.",
     caveats = "Scores Concept 20 (Electoral process and competition).",
     status = "selected",
 ),

# ================= OWID-distributed pass-throughs (TI CPI, UNODC, IRENA) =================

 "ti_cpi_score": dict(
     definition = "How corrupt a country's public sector is seen to be by experts and business people. Transparency International's Corruption Perceptions Index.",
     source_reports = "Transparency International Corruption Perceptions Index, obtained via Our World in Data (TI's own files are password-protected). Published 0-100, where HIGHER means CLEANER (less corruption). Annual, covers 2012 onward.",
     standalone_transform = "None. Renamed and regional aggregates removed; the 0-100 score is used as-is.",
     panel_scaling = "Decided at Step 3: the 0-100 score will be converted to the common framework scale.",
     units = "Score 0-100. Higher is better (cleaner). Note this is already the 'good' direction, unlike most corruption measures.",
     coverage = "About 180 countries, 2012 onward.",
     caveats = "A perceptions index built from multiple expert/business surveys, so it overlaps with other corruption metrics (BCI, WGI). Scores Concept 18 (Control of corruption).",
     status = "selected",
 ),

 "unodc_homicide_rate": dict(
     definition = "How many intentional homicides a country has per 100,000 people - a direct measure of lethal violence. UN Office on Drugs and Crime data.",
     source_reports = "UNODC intentional homicide statistics, via Our World in Data. Published as homicides per 100,000 population. HIGHER means MORE violence.",
     standalone_transform = "None. Renamed and regional aggregates removed; the rate is used as-is.",
     panel_scaling = "Decided at Step 3: converted to the common framework scale, inverting so that lower homicide scores better.",
     units = "Homicides per 100,000 people. Higher is WORSE. Direction is negative.",
     coverage = "About 208 countries, 1990-2024.",
     caveats = "Already a per-population rate, so it is comparable across countries of different sizes. Scores Concept 16 (Personal security and public order).",
     status = "selected",
 ),

 "irena_renewables_share_pct": dict(
     definition = "What share of a country's electricity comes from renewable sources - a marker of energy-transition progress. IRENA/Ember data.",
     source_reports = "Share of electricity from renewables, originally IRENA/Ember, via Our World in Data. Published as a percentage (0-100).",
     standalone_transform = "None. Renamed and regional aggregates removed; the percentage is used as-is.",
     panel_scaling = "Decided at Step 3: the 0-100 percentage will be converted to the common framework scale.",
     units = "Percent of electricity from renewables (0-100). Higher is better.",
     coverage = "About 226 countries, 1990-2025.",
     caveats = "An OUTCOME measure (how much renewable electricity exists), not a governance measure of climate policy itself - it sits alongside the policy-based climate metrics rather than replacing them. Scores Concept 12 (Environmental and climate governance).",
     status = "selected",
 ),

 # ================= Climate Change Laws of the World (LSE Grantham) =================

 "climate_laws_cumulative": dict(
     definition = "How many domestic climate laws and policies a country has put in place over time - the running total in force. Built from the Climate Change Laws of the World database.",
     source_reports = "Climate Change Laws of the World (LSE Grantham / Climate Policy Radar). A registry of individual climate laws and executive policies with enactment dates - NOT a pre-built score.",
     standalone_transform = "WE BUILD THIS. We keep legislative and executive records (drop UNFCCC international-reporting entries), deduplicate so each law counts once, then for each country-year count all its national laws enacted that year or earlier - a cumulative running total. EU-level laws are dropped so they are not double-counted against members' own national laws.",
     panel_scaling = "Decided at Step 3: the cumulative count will be converted to the common framework scale.",
     units = "Count of climate laws in force (cumulative). Higher = more laws.",
     coverage = "Broad, most countries.",
     caveats = "This counts VOLUME, not quality - a country with many weak laws can outscore one with a few strong ones, and the count is not normalized by country size or need. For that reason it was DEMOTED from a primary to a secondary (P2) leg. Scores Concept 12 (Environmental and climate governance). We also keep an annual 'new_laws' flow, which is not scored (momentum is a separate idea).",
     status = "selected",
 ),

 # ================= Chinn-Ito KAOPEN =================

 "kaopen_norm": dict(
     definition = "How open a country's capital account is by law - how free cross-border financial flows are from official controls. The normalized Chinn-Ito index.",
     source_reports = "Chinn-Ito KAOPEN index, from the authors' data file (kaopen_YYYY.xls). We use the normalized version (their ka_open column), scaled 0-1, where HIGHER means MORE open. Built from the IMF's AREAER capital-control records.",
     standalone_transform = "None. We use the authors' published normalized 0-1 value as-is (the raw PCA version is kept but not scored).",
     panel_scaling = "Decided at Step 3: the 0-1 value will be converted to the common framework scale.",
     units = "Index 0-1. Higher = more open. (Note: OPPOSITE sign to FARI, where higher = more restrictive.)",
     coverage = "About 180 countries, long history to recent years.",
     caveats = "DEMOTED to a Supplementary leg because it measures the SAME underlying thing as FARI (capital-account openness) and is built from the SAME IMF AREAER source - it is a cross-check on FARI, not an independent signal. Direction spot-checked in the pipeline (Hong Kong/Singapore open, Iran/Syria closed). Scores Concept 8 (Macroeconomic policy framework quality).",
     status = "selected",
 ),

# ================= World Bank WDI-distributed (LPI, HCI+, WBL 2.0) =================

 "wdi_lpi_overall": dict(
     definition = "How well a country's logistics and trade infrastructure works - customs efficiency, infrastructure quality, shipment timeliness, tracking. World Bank Logistics Performance Index, overall score.",
     source_reports = "World Bank Logistics Performance Index, overall score (WDI code LP.LPI.OVRL.XQ). Published on a 1-5 scale, higher = better logistics. Released roughly every two years.",
     standalone_transform = "None. We use the World Bank's published overall LPI score as-is.",
     panel_scaling = "Decided at Step 3: the 1-5 score will be converted to the common framework scale.",
     units = "Score 1-5. Higher is better.",
     coverage = "About 160 countries, in survey years.",
     caveats = "Released only every couple of years, so between-survey years may be missing. Scores Concept 11 (Trade governance).",
     status = "selected",
 ),

 "wdi_hci_plus_overall": dict(
     definition = "How much human capital a child born today can expect to accumulate by adulthood, given the country's health and education - a composite of survival, schooling, and health. World Bank Human Capital Index (HCI+ version).",
     source_reports = "World Bank Human Capital Index Plus, overall (WDI code HD_HCIP_OVRL_TO). Published 0-1, higher = more human capital realized. We use HCI+ because the standard HCI is not available through the World Bank API.",
     standalone_transform = "None. We use the World Bank's published HCI+ overall score as-is.",
     panel_scaling = "Decided at Step 3: the 0-1 score will be converted to the common framework scale.",
     units = "Score 0-1. Higher is better.",
     coverage = "About 170 countries, in release years.",
     caveats = "HCI+ substitutes for standard HCI (API availability). An OUTCOME-oriented measure of human-capital delivery, used as evidence of public-service capacity. Scores Concept 5 (Public service delivery and human development).",
     status = "selected",
 ),

 "wbl_legal_framework": dict(
     definition = "How equal a country's LAWS are for women across their working life - the legal rights on the books covering mobility, workplace, pay, marriage, parenthood, entrepreneurship, assets, and pensions. World Bank Women, Business and the Law, legal-framework score.",
     source_reports = "World Bank Women, Business and the Law 2.0, overall legal-framework score (WDI code GD_WBL_OVL_LAW). Published 0-100, higher = more legal gender equality. Annual.",
     standalone_transform = "None. We use the World Bank's published 0-100 score as-is.",
     panel_scaling = "Decided at Step 3: the 0-100 score will be converted to the common framework scale.",
     units = "Score 0-100. Higher is better.",
     coverage = "About 190 countries.",
     caveats = "One of three WBL 2.0 facets we score together at Concept 22 (legal framework, supportive frameworks, enforcement) - deliberate source concentration, as WBL is the standard cross-country measure of women's legal equality. This one covers the LAW as written. Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 "wbl_supportive_framework": dict(
     definition = "Whether a country has the institutions and mechanisms that make gender-equality laws real - the supporting frameworks behind the rights on paper. World Bank Women, Business and the Law, supportive-frameworks score.",
     source_reports = "World Bank Women, Business and the Law 2.0, supportive-frameworks score (WDI code GD_WBL_OVL_SFR). Published 0-100, higher = stronger supporting institutions. Annual.",
     standalone_transform = "None. We use the World Bank's published 0-100 score as-is.",
     panel_scaling = "Decided at Step 3: the 0-100 score will be converted to the common framework scale.",
     units = "Score 0-100. Higher is better.",
     coverage = "About 190 countries.",
     caveats = "Second of the three WBL 2.0 facets scored at Concept 22 (see wbl_legal_framework). This one covers the supporting institutions that back the laws. Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 "wbl_enforcement_perceptions": dict(
     definition = "How well gender-equality laws are actually enforced and experienced in practice, not just written down. World Bank Women, Business and the Law, enforcement score.",
     source_reports = "World Bank Women, Business and the Law 2.0, enforcement score (WDI code GD_WBL_OVL_ENF). Published 0-100, higher = better enforcement in practice. Annual.",
     standalone_transform = "None. We use the World Bank's published 0-100 score as-is.",
     panel_scaling = "Decided at Step 3: the 0-100 score will be converted to the common framework scale.",
     units = "Score 0-100. Higher is better.",
     coverage = "About 190 countries.",
     caveats = "Third of the three WBL 2.0 facets scored at Concept 22 (see wbl_legal_framework). This one is the DE FACTO leg - whether the laws work in practice, complementing the de jure legal-framework score. Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

# ================= Fragile States Index (Fund for Peace) =================
 # All four FSI components run 0-10 where HIGHER = MORE fragile = WORSE (direction negative).

 "fsi_c1_security_apparatus": dict(
     definition = "How compromised a country's security apparatus is - internal conflict, insurgency, crime, and the state's monopoly on force. Fragile States Index indicator C1.",
     source_reports = "Fund for Peace Fragile States Index, indicator C1 (Security Apparatus). Published 0-10, where HIGHER means MORE fragile/worse. Annual.",
     standalone_transform = "None. We use the published 0-10 component score as-is.",
     panel_scaling = "Decided at Step 3: converted to the common framework scale, inverting so that less fragility scores better.",
     units = "Score 0-10. Higher is WORSE (more fragile). Direction is negative.",
     coverage = "About 178 countries.",
     caveats = "Scores Concept 13 (State capacity and monopoly on force). Note C13 draws two FSI components (this and others) - deliberate source concentration.",
     status = "selected",
 ),

 "fsi_c2_factionalized_elites": dict(
     definition = "How fragmented and factionalized a country's ruling elites are - power struggles, brinkmanship, and use of nationalist or identity rhetoric among leaders. Fragile States Index indicator C2.",
     source_reports = "Fund for Peace Fragile States Index, indicator C2 (Factionalized Elites). Published 0-10, HIGHER means MORE factionalized/worse. Annual.",
     standalone_transform = "None. We use the published 0-10 component score as-is.",
     panel_scaling = "Decided at Step 3: converted to the common framework scale, inverting so that less factionalism scores better.",
     units = "Score 0-10. Higher is WORSE. Direction is negative.",
     coverage = "About 178 countries.",
     caveats = "Scores Concept 1 (Political settlement and elite bargain).",
     status = "selected",
 ),

 "fsi_c3_group_grievance": dict(
     definition = "How much division and grievance exists between groups in society - along ethnic, religious, regional, or other lines, including exclusion and communal tension. Fragile States Index indicator C3.",
     source_reports = "Fund for Peace Fragile States Index, indicator C3 (Group Grievance). Published 0-10, HIGHER means MORE grievance/worse. Annual.",
     standalone_transform = "None. We use the published 0-10 component score as-is.",
     panel_scaling = "Decided at Step 3: converted to the common framework scale, inverting so that less grievance scores better.",
     units = "Score 0-10. Higher is WORSE. Direction is negative.",
     coverage = "About 178 countries.",
     caveats = "Scores Concept 1 (Political settlement and elite bargain).",
     status = "selected",
 ),

 "fsi_p2_public_services": dict(
     definition = "How well a country provides basic public services - health, education, water, sanitation, infrastructure - and how evenly. Fragile States Index indicator P2.",
     source_reports = "Fund for Peace Fragile States Index, indicator P2 (Public Services). Published 0-10, HIGHER means WORSE service provision. Annual.",
     standalone_transform = "None. We use the published 0-10 component score as-is.",
     panel_scaling = "Decided at Step 3: converted to the common framework scale, inverting so that better services score better.",
     units = "Score 0-10. Higher is WORSE. Direction is negative.",
     coverage = "About 178 countries.",
     caveats = "Scores Concept 5 (Public service delivery and human development).",
     status = "selected",
 ),

 # ================= IMF Statistical Performance Indicators (SPI) =================

 "spi_overall": dict(
     definition = "How strong a country's national statistical system is overall - whether it produces timely, reliable, well-sourced official data. World Bank/IMF Statistical Performance Indicators, overall score.",
     source_reports = "Statistical Performance Indicators, overall score (WDI code IQ.SPI.OVRL). Published 0-100, higher = stronger statistical system. Full coverage from 2016, partial from 2004.",
     standalone_transform = "None. We use the published 0-100 overall score as-is.",
     panel_scaling = "Decided at Step 3: the 0-100 score will be converted to the common framework scale.",
     units = "Score 0-100. Higher is better.",
     coverage = "About 221 countries.",
     caveats = "The five underlying pillars are not scored separately (they decompose this overall score). Overlaps with the ODIN open-data metrics, which measure a related aspect of statistical capacity. Scores Concept 3 (Statistical capacity and data transparency).",
     status = "selected",
 ),

 # ================= IMF iMaPP (Macroprudential Policies) =================

 "imapp_breadth_total": dict(
     definition = "How broad a country's macroprudential policy toolkit is - how many distinct financial-stability instruments it has ever put to use. Built from the IMF's iMaPP database.",
     source_reports = "IMF integrated Macroprudential Policy (iMaPP) database. It records, for each instrument and month, whether a country tightened (+1), loosened (-1), or did nothing (0) - an ACTION log, not a score.",
     standalone_transform = "WE BUILD THIS. We treat ANY non-zero action as 'this country has used this instrument' (ignoring tighten vs loosen), then for each country-year count how many of 16 instruments it has EVER activated up to that point - a cumulative-ever breadth count. The 'Other' instrument category is excluded as too mixed.",
     panel_scaling = "Decided at Step 3: the breadth count will be converted to the common framework scale.",
     units = "Count of instruments ever used (0-16, cumulative). Higher = broader toolkit.",
     coverage = "About 135 countries, 1990-2024.",
     caveats = "Measures BREADTH of the toolkit, NOT quality or whether instruments are currently in force - it is a ratchet that only ever rises (once an instrument is used, it stays counted). Quality assessment is deferred to IMF FSAP. Documented example: Pakistan reads 15 of 16. Scores Concept 8 (Macroeconomic policy framework quality). The four category sub-counts are not scored separately.",
     status = "selected",
 ),

 # ================= IMF AREAER FARI (capital-account restrictiveness) =================
 # All FARI indices run 0-1 where HIGHER = MORE restrictive = WORSE (direction negative).

 "fari_aggregate": dict(
     definition = "How restricted a country's capital account is overall by law - the extent of official controls on cross-border financial flows. IMF's Financial Account Restrictiveness Index, aggregate.",
     source_reports = "IMF AREAER Financial Account Restrictiveness Index (FARI), aggregate. Exported by hand from the AREAER portal (the portal is firewall-blocked to automation). Published 0-1, where HIGHER means MORE restrictive.",
     standalone_transform = "None. We use the IMF's published 0-1 index as-is.",
     panel_scaling = "Decided at Step 3: converted to the common framework scale. Direction is a judgment item - restrictiveness is a policy stance, not self-evidently good or bad governance - to be settled then.",
     units = "Index 0-1. Higher = more restrictive. Direction treated as negative (openness scores better), pending the Step-3 direction call.",
     coverage = "About 194 countries, 1999-2024 (2024 partial).",
     caveats = "The IMF-native authoritative capital-account measure; KAOPEN is the automated cross-check on it. Scores Concept 8 (Macroeconomic policy framework quality). Manual export each cycle.",
     status = "selected",
 ),

 "fari_fdi_aggregate": dict(
     definition = "How restricted a country's foreign direct investment flows are by law specifically - the FDI-focused slice of capital-account restrictiveness. IMF's FARI, FDI aggregate.",
     source_reports = "IMF AREAER FARI, FDI aggregate sub-index. Published 0-1, HIGHER means MORE restrictive on FDI. Same manual export as fari_aggregate.",
     standalone_transform = "None. We use the IMF's published 0-1 sub-index as-is.",
     panel_scaling = "Decided at Step 3: converted to the common framework scale (same direction treatment as fari_aggregate).",
     units = "Index 0-1. Higher = more restrictive on FDI. Direction treated as negative.",
     coverage = "About 194 countries, 1999-2024 (2024 partial).",
     caveats = "The FDI-specific slice is a genuine advantage over indices that collapse to one number - it isolates investment-relevant restrictions. Scores Concept 8 (Macroeconomic policy framework quality).",
     status = "selected",
 ),

 "fari_fdi_inflow": dict(
     definition = "How restricted INBOUND foreign direct investment is by law - controls on money coming into the country. IMF's FARI, FDI inflow.",
     source_reports = "IMF AREAER FARI, FDI inflow sub-index. Published 0-1, HIGHER means MORE restrictive on inbound FDI. Same manual export.",
     standalone_transform = "None. We use the IMF's published 0-1 sub-index as-is.",
     panel_scaling = "Decided at Step 3: converted to the common framework scale (same direction treatment as fari_aggregate).",
     units = "Index 0-1. Higher = more restrictive on inbound FDI. Direction treated as negative.",
     coverage = "About 194 countries, 1999-2024 (2024 partial).",
     caveats = "DELIBERATE partial double-count: this is scored at full weight ALONGSIDE fari_fdi_aggregate, a considered choice to tilt Concept 8 toward INBOUND capital access, which matters more to a sovereign investor than outbound. The outflow splits are dropped (outbound less material). Scores Concept 8 (Macroeconomic policy framework quality).",
     status = "selected",
 ),

 # ================= Political Terror Scale (combined) =================

 "pts_index": dict(
     definition = "How severe state-perpetrated physical-integrity violations are - political imprisonment, torture, killings, and disappearances by the state. A combined Political Terror Scale score.",
     source_reports = "Political Terror Scale, obtained via the Quality of Government dataset. PTS publishes THREE separate 1-5 codings of the same year, one each from Amnesty International, Human Rights Watch, and the US State Department (higher = more state terror). We combine them.",
     standalone_transform = "None yet in a pipeline. The source provides THREE separate 1-5 coder columns (pts_amnesty, pts_hrw, pts_statedept); they are carried through unchanged, not yet combined.",
     panel_scaling = "NOT BUILT - the scoring layer does not exist yet. PLANNED (per the metric_selection derive= note): for each country-year take the MEAN of whichever coder scores are present (a union, so a country counts if ANY coder rated it, maximizing coverage; checks showed no systematic coder-severity bias). Then convert to the common scale, inverting so less state terror scores better.",
     units = "Score 1-5 (mean of available coders). Higher is WORSE (more state terror). Direction is negative.",
     coverage = "About 98% of country-years, largely via the State Department coding which has the widest reach.",
     caveats = "The three individual coder columns are not scored separately (they are the planned inputs to the mean). The combining mean is NOT yet implemented anywhere - it lives only as a plan in metric_selection. Scores two concepts: Concept 16 (Personal security and public order) as a primary leg, and Concept 22 (Civil liberties) as a supporting leg.",
     status = "selected",
 ),

# ================= CCP (Comparative Constitutions Project, via QoG) =================
 # NOTE: value 96 is a MISSING sentinel in the source, not data - recode to blank before use.

 "ccp_civil_rights_provisions": dict(
     definition = "Whether a country's constitution contains civil-rights provisions written into the text. From the Comparative Constitutions Project.",
     source_reports = "Comparative Constitutions Project (variable ccp_civil), via the Quality of Government dataset. Higher = more civil-rights provisions in the constitution.",
     standalone_transform = "Recode needed before use: the source uses 96 as a MISSING marker (not a real value), so 96 must be set to blank (affects ~23 countries). This recode is flagged as a build step in metric_selection and is NOT yet applied. Otherwise the value is used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "Constitutional-provision measure (de jure). Higher is better.",
     coverage = "Most countries with codified constitutions.",
     caveats = "DE JURE only - measures what the constitution SAYS, not whether rights are honored in practice. Scores Concept 14 (Legal quality and predictability).",
     status = "selected",
 ),

 "ccp_information_access": dict(
     definition = "Whether a country's constitution guarantees access to government information - a constitutional right-to-information provision. From the Comparative Constitutions Project.",
     source_reports = "Comparative Constitutions Project (variable ccp_infoacc), via the Quality of Government dataset. Higher = information-access provisions present in the constitution.",
     standalone_transform = "Recode needed before use: the source uses 96 as a MISSING marker, so 96 must be set to blank (affects ~6 countries). Flagged in metric_selection, NOT yet applied. Otherwise used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "Constitutional-provision measure (de jure). Higher is better.",
     coverage = "Most countries with codified constitutions.",
     caveats = "DE JURE only - what the constitution SAYS, not practice. Scores Concept 14 (Legal quality and predictability).",
     status = "selected",
 ),

 # ================= Romelli Central Bank Independence (via QoG) =================

 "romelli_cbi_index": dict(
     definition = "How independent a country's central bank is by law - insulation from political interference in its governance, objectives, policy, and financing of government. Romelli's extended Central Bank Independence index.",
     source_reports = "Romelli Central Bank Independence Extended (CBIE) index, variable cbie_index, via the Quality of Government dataset. A de jure index built from central-bank legislation, higher = more independent. Long history (1923-2023).",
     standalone_transform = "None. QoG carries the index unchanged; we use it as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "Index (roughly 0-1). Higher is better (more independent).",
     coverage = "About 155 countries.",
     caveats = "DE JURE - measures independence written into central-bank law, not day-to-day operational independence. The policy and lending sub-components exist but are not scored separately (they decompose this overall index). Scores Concept 8 (Macroeconomic policy framework quality).",
     status = "selected",
 ),

 # ================= UCDP (Uppsala Conflict Data Program) =================

 "ucdp_sb_intrastate_deaths_best": dict(
     definition = "How much lethal internal armed conflict a country suffers - the best estimate of battle-related deaths in state-based INTRASTATE conflicts (government versus internal armed groups) in a year. From UCDP.",
     source_reports = "Uppsala Conflict Data Program, country-year organized-violence dataset. Field: best estimate of deaths in state-based intrastate conflicts. A raw death COUNT, higher = more conflict deaths.",
     standalone_transform = "None yet beyond selection/rename. The pipeline (nb 12) selects the intrastate death count as-published. INTRASTATE only is deliberate: interstate conflict is external aggression, a different construct (e.g. Ukraine's file-max interstate deaths would invert the meaning). Non-state and one-sided violence are excluded.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned (per metric_selection): express per-capita (raw counts favor large countries), apply log1p (the distribution is extreme and zero-inflated), zero-fill countries with no recorded conflict to the spine (absence = a true zero, ~99.5% of the panel), then convert to the common scale, inverting so fewer deaths score better.",
     units = "Battle-related deaths (raw count as delivered; per-capita + log planned). Higher is WORSE. Direction is negative.",
     coverage = "About 199 countries, 1989-2024. Most country-years are true zeros (no conflict).",
     caveats = "Interstate deaths deliberately excluded (external aggression is not internal-stability failure). Scores Concept 2 (Political stability and government continuity).",
     status = "selected",
 ),

 # ================= CPJ (Committee to Protect Journalists) =================
 # Live census: CPJ's endpoints only return countries with >=1, so absence = a true zero.

 "cpj_imprisoned": dict(
     definition = "How many journalists a country has jailed for their work - a live count of those currently imprisoned. From the Committee to Protect Journalists.",
     source_reports = "Committee to Protect Journalists, via its public API. A live census snapshot: the count of journalists currently imprisoned for their work, per country. Raw count, higher = more repression.",
     standalone_transform = "Built in-pipeline (nb 36): CPJ's count endpoint only lists countries with at least one jailed journalist, so absence from the list means a TRUE ZERO - the pipeline fills those countries with 0. One row per country. No denominator applied (see caveats).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned (per metric_selection): apply log1p (counts are zero-inflated and skewed), keep as a raw count NOT per-capita, then convert to the common scale, inverting so fewer jailed journalists score better.",
     units = "Count of imprisoned journalists (raw). Higher is WORSE. Direction is negative.",
     coverage = "All framework countries (those not on CPJ's list are true zeros). Live snapshot, refreshed on each run.",
     caveats = "Deliberately NOT per-capita: dividing by population inverts the ranking wrongly (China would look better than tiny Eritrea despite jailing far more journalists in absolute terms). CPJ lumps Israel/OPT under one code. Scores Concept 23 (Media freedom and pluralism).",
     status = "selected",
 ),

 "cpj_murders_unsolved": dict(
     definition = "How many journalist murders in a country have gone unsolved - complete-impunity killings over a rolling recent window. A measure of impunity for violence against the press. From the Committee to Protect Journalists.",
     source_reports = "Committee to Protect Journalists, via its public API. The count of journalist murders classified 'Complete Impunity' (unsolved) over a rolling window of the last few years. Raw count, higher = more impunity.",
     standalone_transform = "Built in-pipeline (nb 36): derived from per-case murder records by tallying complete-impunity cases per country; absence from CPJ's data means a true zero, filled with 0. Rolling window auto-derived from the current year (not hardcoded). One row per country.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned (per metric_selection): apply log1p, keep as a raw count, then convert to the common scale, inverting so fewer unsolved murders score better.",
     units = "Count of unsolved journalist murders (raw, rolling window). Higher is WORSE. Direction is negative.",
     coverage = "All framework countries (absence = true zero). Slow-moving over the window.",
     caveats = "The impunity signal (unsolved), distinct from raw murder counts. The separate confirmed-murder count was DROPPED from scoring (conflict-contaminated - Israel/OPT alone was 32 of 99 in one pull). Scores Concept 23 (Media freedom and pluralism).",
     status = "selected",
 ),

 # ================= FATF Mutual Evaluations =================
 # Two axes on the SAME 0-3 scale, both higher=better, both built in-pipeline (nb 35 cell 5).

 "fatf_effectiveness": dict(
     definition = "How effective a country's anti-money-laundering and counter-terrorist-financing system is IN PRACTICE - the real-world outcomes, as judged by FATF's Mutual Evaluations. The de facto AML/CFT measure.",
     source_reports = "Financial Action Task Force Mutual Evaluations. FATF rates 11 'Immediate Outcomes' (effectiveness) on a 4-level scale: High, Substantial, Moderate, Low. Higher = more effective.",
     standalone_transform = "Built in-pipeline (nb 35): map the 4 levels to numbers (High=3, Substantial=2, Moderate=1, Low=0), then take the MEAN across the 11 Immediate Outcomes. Higher = more effective in practice.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-3 mean to the common framework scale.",
     units = "Mean effectiveness 0-3. Higher is better.",
     coverage = "About 199 countries (latest assessment per country).",
     caveats = "DE FACTO leg - real-world outcomes, weighted more heavily (via tier) than the de jure compliance leg because it is the scarcer, better-discriminating signal. Measures AML/CFT specifically, not the whole financial-supervision remit. Scores Concept 9 (Financial sector regulatory and supervisory quality).",
     status = "selected",
 ),

 "fatf_technical_compliance": dict(
     definition = "How well a country's laws and rules match the FATF anti-money-laundering STANDARD on paper - technical compliance with the 40 Recommendations. The de jure AML/CFT measure.",
     source_reports = "Financial Action Task Force Mutual Evaluations. FATF rates the 40 Recommendations on a 4-level scale: Compliant, Largely Compliant, Partially Compliant, Non-Compliant. Higher = better legal compliance with the standard.",
     standalone_transform = "Built in-pipeline (nb 35): map the 4 levels to numbers (Compliant=3, Largely=2, Partially=1, Non=0), then take the MEAN across the Recommendations. IMPORTANT: a Recommendation rated 'N/A' (not applicable to that country) becomes blank and is EXCLUDED from the mean, never counted as 0 - it is a structural exclusion, not a low score.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-3 mean to the common framework scale.",
     units = "Mean technical compliance 0-3. Higher is better.",
     caveats = "DE JURE - compliance with the FATF STANDARD on paper, NOT real-world effectiveness. The gap between this and fatf_effectiveness is the framework's clearest illustration of why rules-on-paper overstate governance (compliance averages far higher than effectiveness). Scores Concept 9 (Financial sector regulatory and supervisory quality).",
     coverage = "About 199 countries.",
     status = "selected",
 ),

 # ================= WB Bank Regulation & Supervision Survey =================

 "brss_regstringency": dict(
     definition = "How stringent a country's banking regulation and supervision are on paper - the strength of prudential rules across supervisory power, independence, capital, monitoring, resolution, and related areas. Built from the World Bank's Bank Regulation and Supervision Survey.",
     source_reports = "World Bank Bank Regulation and Supervision Survey (BRSS), 2019 wave (2016 reference year). A questionnaire of yes/no and numeric items on banking prudential regulation - not a pre-built index.",
     standalone_transform = "Built in-pipeline (nb 38): from 9 clear-directional sub-constructs (supervisory power, independence, private monitoring, resolution regime, macroprudential, capital stringency, provisioning, liquidity/concentration, supervisory capacity). Each item is normalized 0-1 and signed for direction, combined into the 9 sub-scores, then a WEIGHTED MEAN produces the headline (weights: power/independence/private-monitoring/resolution/macroprudential = 2; capital/provisioning/liquidity/supervisory-capacity = 1). A coverage-reliability FLAG (not a penalty) excludes sparse entries downstream. Validated against Anginer et al. 2019.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 stringency score to the common framework scale.",
     units = "De jure stringency index 0-1. Higher = stronger rules on paper.",
     coverage = "About 161 countries (155 reliable after the coverage flag).",
     caveats = "DE JURE rules-on-paper, NOT supervisory effectiveness. Scored as a SUPPLEMENTARY leg purely because the data is frozen at the 2016 vintage (too stale to drive a current score), NOT because banking regulation is peripheral - it is central to Concept 9 and would be a primary leg if current. Scores Concept 9 (Financial sector regulatory and supervisory quality).",
     status = "selected",
 ),

# ================= V-Dem (Varieties of Democracy) =================
 # The pipeline (nb 03) SELECTS V-Dem variables and uses them as-published - no direction
 # handling, no recoding. Two scales: v2x_* aggregate INDICES run 0-1; individual v2cl*/
 # v2ex*/v2el*/v2ju* items are interval measurement-model point estimates (~ -4 to +4,
 # centered near 0). Direction is taken from the metric_selection record, NOT inferred from
 # the variable family - see the corruption cluster, where the family name misleads.

 # ---- Concept 1: Political settlement and elite bargain ----
 "v2pepwrses": dict(
     definition = "How equally political power is distributed across socioeconomic groups - whether the rich dominate politics or power is shared across income levels. V-Dem's power-by-socioeconomic-position indicator.",
     source_reports = "V-Dem variable v2pepwrses. Interval measurement-model scale (roughly -4 to +4, higher = more equal distribution of power). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the interval scale to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better (more equal).",
     coverage = "Near-universal (V-Dem covers ~180 countries).",
     caveats = "Scores Concept 1 (Political settlement and elite bargain).",
     status = "selected",
 ),

 "v2pepwrsoc": dict(
     definition = "How equally political power is distributed across social groups - by ethnicity, religion, region, race, language, or caste. V-Dem's power-by-social-group indicator.",
     source_reports = "V-Dem variable v2pepwrsoc. Interval scale (~ -4 to +4, higher = more equal across social groups). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 1 (Political settlement and elite bargain).",
     status = "selected",
 ),

 "v2x_egal": dict(
     definition = "How egalitarian a country's democracy is overall - whether rights, freedoms, and resources are distributed equally across groups. V-Dem's egalitarian component index.",
     source_reports = "V-Dem index v2x_egal. Aggregate index scaled 0-1, higher = more egalitarian. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 index to the common framework scale.",
     units = "Index 0-1. Higher is better (more egalitarian).",
     coverage = "Near-universal (~180 countries).",
     caveats = "An aggregate index (0-1 scale), unlike the individual V-Dem items on the interval scale. Scores Concept 1 (Political settlement and elite bargain).",
     status = "selected",
 ),

 "v2psoppaut": dict(
     definition = "How free opposition parties are to operate independently - without control or interference from the ruling party or government. V-Dem's opposition-party-autonomy indicator.",
     source_reports = "V-Dem variable v2psoppaut. Interval scale (~ -4 to +4, higher = more autonomous opposition). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 1 (Political settlement and elite bargain).",
     status = "selected",
 ),

 # ---- Concept 4: Government effectiveness and administrative capacity ----
 "v2clrspct": dict(
     definition = "How rigorous and impartial public administration is - whether officials apply the law consistently and without bias, rather than arbitrarily or corruptly. V-Dem's rigorous-and-impartial-administration indicator.",
     source_reports = "V-Dem variable v2clrspct. Interval scale (~ -4 to +4, higher = more rigorous and impartial). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 4 (Government effectiveness and administrative capacity).",
     status = "selected",
 ),

 # ---- Concept 10: State control over the economy ----
 "v2clstown": dict(
     definition = "How much the state controls private property and economic activity - low state ownership/control at the high end, pervasive state control at the low end. V-Dem's state-ownership-of-economy indicator.",
     source_reports = "V-Dem variable v2clstown. Interval scale (~ -4 to +4, higher = MORE private/less state control). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better (less state control).",
     coverage = "Near-universal (~180 countries).",
     caveats = "Direction was evidence-resolved (2026-07-21): the relationship to governance quality is monotonic and roughly linear, with no threshold effect. The only scored indicator for Concept 10, which stays single-indicator (a second-indicator pairing was tested and declined). Scores Concept 10 (State control over the economy).",
     status = "selected",
 ),

 # ---- Concept 13: State capacity and monopoly on force ----
 "v2svstterr": dict(
     definition = "How much of its territory the state actually controls - the share of the country over which the government has effective authority. V-Dem's state-authority-over-territory indicator.",
     source_reports = "V-Dem variable v2svstterr. Published as a percentage (0-100) of territory controlled, higher = more control. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "Percent of territory controlled (0-100). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 13 (State capacity and monopoly on force). C13 draws two V-Dem items plus FSI - deliberate concentration on the strongest state-capacity signals.",
     status = "selected",
 ),

 "v2svdomaut": dict(
     definition = "How free a country's government is from foreign control over domestic policy - whether it makes its own decisions or is constrained by outside powers. V-Dem's domestic-autonomy indicator.",
     source_reports = "V-Dem variable v2svdomaut. Interval scale (~ -4 to +4, higher = more autonomous). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 13 (State capacity and monopoly on force).",
     status = "selected",
 ),

 # ---- Concept 14: Legal quality and predictability (v2cltrnslw also scores C25) ----
 "v2cltrnslw": dict(
     definition = "How transparent and predictable a country's laws are - whether laws are public, clear, and stable rather than secret, vague, or arbitrarily changed. V-Dem's transparent-laws indicator.",
     source_reports = "V-Dem variable v2cltrnslw. Interval scale (~ -4 to +4, higher = more transparent/predictable laws). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores TWO concepts: Concept 14 (Legal quality and predictability) and Concept 25 (Government transparency and openness).",
     status = "selected",
 ),

 "v2clacjstm": dict(
     definition = "How equal men's access to justice is - whether men can secure fair treatment from the courts regardless of status or connections. V-Dem's access-to-justice-for-men indicator.",
     source_reports = "V-Dem variable v2clacjstm. Interval scale (~ -4 to +4, higher = more equal access). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Paired with the women's-access item (v2clacjstw) to cover access to justice across genders. Scores Concept 14 (Legal quality and predictability).",
     status = "selected",
 ),

 "v2clacjstw": dict(
     definition = "How equal women's access to justice is - whether women can secure fair treatment from the courts. V-Dem's access-to-justice-for-women indicator.",
     source_reports = "V-Dem variable v2clacjstw. Interval scale (~ -4 to +4, higher = more equal access). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "The women's counterpart to v2clacjstm. Scores Concept 14 (Legal quality and predictability).",
     status = "selected",
 ),

 "v2xeg_eqaccess": dict(
     definition = "How equal access to power and resources is across the population overall - a composite of equal access regardless of gender, social group, and socioeconomic position. V-Dem's equal-access index.",
     source_reports = "V-Dem index v2xeg_eqaccess. Aggregate index scaled 0-1, higher = more equal access. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 index to the common framework scale.",
     units = "Index 0-1. Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "An aggregate index (0-1), unlike the individual items on the interval scale. Scores Concept 14 (Legal quality and predictability).",
     status = "selected",
 ),

# ---- Concept 2: Political stability and government continuity ----
 "vdem_regime_duration": dict(
     definition = "How long a country has continuously held its current type of political regime - a measure of regime stability/continuity. A derived metric based on V-Dem's regime classification.",
     source_reports = "Would be derived from V-Dem's Regimes of the World variable v2x_regime, a 0-3 typology (0 = closed autocracy, 1 = electoral autocracy, 2 = electoral democracy, 3 = liberal democracy). V-Dem itself does not publish a duration variable.",
     standalone_transform = "NOT BUILT. This metric does not exist in any pipeline yet - it appears only in the metric_selection record as a planned scored metric. The column is absent from vdem_filtered.csv. PLANNED: count consecutive years a country has stayed in the same v2x_regime category (a run-length from the regime series). The exact derivation rule is not yet fixed in code.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the duration count to the common framework scale.",
     units = "Planned: years in current regime type (count). Higher = longer continuity.",
     coverage = "Would follow v2x_regime coverage (~180 countries) once built.",
     caveats = "PLANNED metric, not yet implemented anywhere - both the derivation and the scoring are outstanding build tasks. Scores Concept 2 (Political stability and government continuity). Direction assumes longer regime continuity is better, which is defensible for stability but worth revisiting (a long-stable autocracy also scores high on duration alone).",
     status = "selected",
 ),

 # ---- Concept 15: Judicial independence and quality (all interval-scale, direction +) ----
 "v2juhcind": dict(
     definition = "How independent the high court is from government pressure - whether top judges rule on the law or bend to those in power. V-Dem's high-court-independence indicator.",
     source_reports = "V-Dem variable v2juhcind. Interval scale (~ -4 to +4, higher = more independent). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 15 (Judicial independence and quality).",
     status = "selected",
 ),

 "v2juncind": dict(
     definition = "How independent the lower courts are from government pressure - judicial independence below the high court. V-Dem's lower-court-independence indicator.",
     source_reports = "V-Dem variable v2juncind. Interval scale (~ -4 to +4, higher = more independent). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 15 (Judicial independence and quality).",
     status = "selected",
 ),

 "v2jucomp": dict(
     definition = "How reliably government officials comply with court rulings - whether judicial decisions are actually obeyed. V-Dem's compliance-with-judiciary indicator.",
     source_reports = "V-Dem variable v2jucomp. Interval scale (~ -4 to +4, higher = more compliance with courts). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 15 (Judicial independence and quality).",
     status = "selected",
 ),

 "v2jupack": dict(
     definition = "How free the judiciary is from court-packing - whether the government manipulates the composition of courts by appointing loyalists. V-Dem's court-packing indicator (higher = less packing).",
     source_reports = "V-Dem variable v2jupack. Interval scale (~ -4 to +4, higher = LESS court-packing / more protected). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better (less packing).",
     coverage = "Near-universal (~180 countries).",
     caveats = "Higher already means BETTER (less court-packing) on V-Dem's coding, so direction is positive. Scores Concept 15 (Judicial independence and quality).",
     status = "selected",
 ),

 "v2jupurge": dict(
     definition = "How free the judiciary is from arbitrary purges - whether judges are removed for political reasons. V-Dem's judicial-purge indicator (higher = fewer purges).",
     source_reports = "V-Dem variable v2jupurge. Interval scale (~ -4 to +4, higher = FEWER arbitrary removals). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better (fewer purges).",
     coverage = "Near-universal (~180 countries).",
     caveats = "Higher already means BETTER (fewer purges) on V-Dem's coding, so direction is positive. Scores Concept 15 (Judicial independence and quality).",
     status = "selected",
 ),

 # ---- Concept 16: Personal security and public order (interval-scale, direction +) ----
 "v2cltort": dict(
     definition = "How free people are from torture by the state - whether the government uses or tolerates torture. V-Dem's freedom-from-torture indicator (higher = less torture).",
     source_reports = "V-Dem variable v2cltort. Interval scale (~ -4 to +4, higher = LESS torture / more freedom from it). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better (less torture).",
     coverage = "Near-universal (~180 countries).",
     caveats = "Higher already means BETTER (less torture) on V-Dem's coding, so direction is positive despite the grim subject. Scores Concept 16 (Personal security and public order).",
     status = "selected",
 ),

 "v2clkill": dict(
     definition = "How free people are from political killings by the state - extrajudicial executions and killings for political reasons. V-Dem's freedom-from-political-killings indicator (higher = fewer killings).",
     source_reports = "V-Dem variable v2clkill. Interval scale (~ -4 to +4, higher = FEWER political killings). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better (fewer killings).",
     coverage = "Near-universal (~180 countries).",
     caveats = "Higher already means BETTER (fewer killings) on V-Dem's coding, so direction is positive. Scores Concept 16 (Personal security and public order).",
     status = "selected",
 ),

 "v2clrgunev": dict(
     definition = "How evenly civil liberties are applied across a country's territory - whether rights protection is uniform or varies sharply by region. V-Dem's rights-unevenness indicator (higher = more even/uniform).",
     source_reports = "V-Dem variable v2clrgunev. Interval scale (~ -4 to +4, higher = MORE uniform application of rights across territory). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better (more even).",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 16 (Personal security and public order).",
     status = "selected",
 ),

 # ---- Concept 17: Property rights and contract enforcement ----
 "v2clprptym": dict(
     definition = "How secure men's property rights are - whether men can own and use property free from arbitrary seizure. V-Dem's property-rights-for-men indicator.",
     source_reports = "V-Dem variable v2clprptym. Interval scale (~ -4 to +4, higher = more secure property rights). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Paired with the women's property item (v2clprptyw) to cover property rights across genders. Scores Concept 17 (Property rights and contract enforcement).",
     status = "selected",
 ),

 "v2clprptyw": dict(
     definition = "How secure women's property rights are - whether women can own and use property free from arbitrary seizure. V-Dem's property-rights-for-women indicator.",
     source_reports = "V-Dem variable v2clprptyw. Interval scale (~ -4 to +4, higher = more secure property rights). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "The women's counterpart to v2clprptym. Scores Concept 17 (Property rights and contract enforcement).",
     status = "selected",
 ),

 "v2xcl_prpty": dict(
     definition = "How secure property rights are overall - a composite of men's and women's property security. V-Dem's property-rights index.",
     source_reports = "V-Dem index v2xcl_prpty. Aggregate index scaled 0-1, higher = more secure property rights. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 index to the common framework scale.",
     units = "Index 0-1. Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "An aggregate index (0-1), unlike the individual property items on the interval scale. Scores Concept 17 (Property rights and contract enforcement).",
     status = "selected",
 ),
    










    

















    
 # ================= IMF_FISCAL_RULES (C8 Macroeconomic policy framework quality) =================

 "fr_num_rule_types": dict(
     definition = "Count of fiscal-rule types a country has in force (of 4: expenditure, revenue, budget-balance, debt)",
     source_reports = "IMF Fiscal Rules Dataset 1985-2024. Per rule type, presence flag '1' if in force, '-' otherwise. Codebook: presence entered as 1 in the rule-type column.",
     standalone_transform = "Sum of the four presence flags (each 1/0). Range 0-4. Higher = broader fiscal-rule architecture.",
     panel_scaling = "TBD Step-3: 0-4 count, fixed-anchor or percentile; S7 missingness penalty.",
     units = "count 0-4",
     coverage = "123 countries in latest year. Latest-year distribution 0->1, 1->20, 2->49, 3->46, 4->7.",
     caveats = "De jure breadth, not quality or adherence. A country can hold many weak rules or one strong one; breadth is only one axis (strength and teeth are the other two metrics).",
     status = "selected",
 ),

 "fr_max_legal_basis": dict(
     definition = "Strongest legal footing among a country's fiscal rules",
     source_reports = "IMF Fiscal Rules Dataset 1985-2024, 'Legal or political basis (highest norm)', per rule type, ordinal 1-5. Codebook: 1=political commitment, 2=coalition agreement, 3=statutory, 4=international treaty, 5=constitutional.",
     standalone_transform = "Max of the per-rule-type legal-basis values across the rule types in force. Null if country has no rules. Range 1-5, higher = more entrenched.",
     panel_scaling = "TBD Step-3: 1-5 ordinal, fixed-anchor or percentile; S7 missingness penalty. Null (no rules) enters missingness layer.",
     units = "ordinal 1-5",
     coverage = "101 countries in latest year (22 with zero rules are correctly null). Latest-year distribution 1->11, 2->4, 3->73, 5->13.",
     caveats = "De jure strength. Max (not mean) chosen deliberately: mean penalizes breadth (adding a weak rule lowers the mean), max captures firmest footing. fr_mean_legal_basis excluded for that reason.",
     status = "selected",
 ),

 "fr_any_enforcement": dict(
     definition = "Whether any of a country's fiscal rules carries a formal enforcement procedure",
     source_reports = "IMF Fiscal Rules Dataset 1985-2024, 'Formal enforcement procedure', per rule type, binary. Codebook: 1=formal enforcement procedure exists, 0=none.",
     standalone_transform = "1 if any per-rule-type enforcement flag is 1, else 0 (NaN treated as 0 in the OR). Binary.",
     panel_scaling = "TBD Step-3: binary, fixed-anchor {0,1}; S7 missingness penalty.",
     units = "binary 0/1",
     coverage = "123 countries in latest year. Latest-year split 75 no / 48 yes.",
     caveats = "De jure teeth. Binary, lower discrimination than the two P1 metrics, and partly implied by legal basis (entrenched rules more often carry enforcement) - hence P2.",
     status = "selected",
 ),

 "fr_compliance_mean": dict(
     definition = "Mean fiscal-rule compliance across the rule types a country has in force",
     source_reports = "IMF Fiscal Rules Dataset 1985-2024, 'Compliance', per rule type (ER/RR/BBR/DR), code {0,1,2}. Codebook (2024 technical manual): 0=complies with none, 1=complies with all, 2=complies with some but not all (partial). NOTE the codes sheet in the workbook omits this definition; it is defined in the technical manual, verified 2026-07-24.",
     standalone_transform = "Map code {0,1,2} -> {0.0, 1.0, 0.5} (partial=0.5 sits BETWEEN none and full, NOT above full), then mean across present rule types. Null if country has no rules. Result 0-1 share, higher = more compliant.",
     panel_scaling = "TBD Step-3: percentile-rank 0-1 share across scored panel; S7 missingness penalty.",
     units = "0-1 share (1 = complies with all its rules)",
     coverage = "54 countries with any compliance value (~28% of 192 sovereigns). SUB-60%, coverage-flagged.",
     caveats = "The only de facto leg in an otherwise de jure source. ENDOGENEITY: compliance partly reflects rule laxity (lax rules are easier to meet), so its direction is weaker than the de jure legs - caps at P2. PIPELINE BUG (nb 25): current build uses to_num max() across rule types and does not remap 2->0.5, so it mis-ranks multi-rule and partial-compliance countries. Must fix (max->mean-of-mapped, 2->0.5, conditional on presence) BEFORE this metric is scored.",
     status = "selected",
 ),

}