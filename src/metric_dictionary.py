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