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