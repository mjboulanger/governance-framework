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
     caveats = "Scores two concepts: Concept 8 (Macroeconomic policy framework quality - which now includes public financial management after the C7 fold) as a primary leg, and Concept 25 (Government transparency and openness) as a supporting leg.",
     status = "selected",
 ),

 "idea_participation": dict(
     definition = "The Participation attribute of International IDEA's Global State of Democracy (GSoD) indices - a 0-1 measure of how much citizens engage in political life beyond voting: civil society activity, civic engagement, electoral participation, direct and local democracy.",
     source_reports = "International IDEA, Global State of Democracy (GSoD) Indices. Published as a 0-1 aggregate attribute with subcomponents. Model-based estimates combining multiple underlying sources.",
     standalone_transform = "None - used as the published 0-1 attribute score. Direction POSITIVE (higher = more participatory). Composite chosen over subcomponents: civil_society (r=0.980) and civic_engagement (r=0.832) are redundant with it; electoral_participation and direct_democracy are weak/degenerate; local_democracy scored separately as a distinct facet.",
     panel_scaling = "NOT BUILT yet (scoring layer does not exist). Already on a 0-1 scale, so scaling is light.",
     units = "Continuous 0-1, higher = better. Direction positive.",
     coverage = "174 countries, 1990-2025 (full history, current). Matches V-Dem's temporal depth - a genuine full-panel independent source, unlike CIVICUS (2022+ only).",
     caveats = "P1 in Concept 21 (Political participation beyond voting). Placed P1 specifically because C21 is otherwise V-Dem-dominated (6 of 7 existing metrics are V-Dem: the v2x_partip composite plus 5 facets); GSoD is the main independent full-history measure. Validated: Denmark 0.96, Switzerland 0.94, Norway 0.91 (top) down to North Korea 0.03 (bottom).",
     status = "built",
 ),

 "idea_local_democracy": dict(
     definition = "The Local Democracy subcomponent of IDEA GSoD's Participation attribute - a 0-1 measure of participatory institutions and engagement at the subnational/local level.",
     source_reports = "International IDEA, GSoD Indices. Subcomponent of the Participation attribute. Model-based 0-1 estimate.",
     standalone_transform = "None - published 0-1 score. Direction POSITIVE.",
     panel_scaling = "NOT BUILT yet. Light (already 0-1).",
     units = "Continuous 0-1, higher = better. Direction positive.",
     coverage = "174 countries, 1990-2025.",
     caveats = "P2 in Concept 21. Scored as a distinct facet because it is the sharpest democracy/autocracy discriminator in the GSoD participation cluster (clean-autocracy gap 0.85 vs the composite's 0.66) and only moderately correlated with the composite (r=0.744, ~half its variance independent) - captures local/subnational participation the national-focused V-Dem cluster underweights. OVERLAP: it is a subcomponent of idea_participation (also scored), so the two share mechanical variance - NAMED for the Step-4 correlation-aware weighting so they are not treated as fully independent.",
     status = "built",
 ),

 "nelda_concerns_not_free_fair": dict(
     definition = "Whether there were significant concerns, before an election, that it would not be free and fair (NELDA variable NELDA11). A pre-election red flag.",
     source_reports = "NELDA (National Elections Across Democracy and Autocracy, Hyde and Marinov), sourced via QoG Standard TS. Binary yes/no per election.",
     standalone_transform = "None - used as the raw 0/1 indicator. RENAMED from the pipeline's earlier misleading label 'nelda_free_and_fair' (which inverted the meaning: the variable flags CONCERNS, so 1 = bad). Direction NEGATIVE.",
     panel_scaling = "NOT BUILT yet. Event-level to country-year mapping and the consolidated-democracy-absence bias must be handled at scaling.",
     units = "Binary: 1 = concerns existed (worse), 0 = no concerns. Direction negative.",
     coverage = "82+ event-level coverage. NELDA is election-level: data exists only in election years (~24.5% of country-years), one observation per country-year, systematically ABSENT for ~21 consolidated democracies excluded by NELDA's design (absence implies established-democracy, i.e. implicitly clean - a coverage bias for the scaling layer to handle, not neutral missingness). Raw 99 ('unclear/could not code') converted to NaN in the QoG pipeline (nb 14).",
     caveats = "Supplementary in Concept 20 (Electoral process); C20 has 10 P1 metrics, NELDA triangulates. Validated: clean democracies 0.000, rigged autocracies 0.093.",
     status = "built",
 ),

 "nelda_media_bias_incumbent": dict(
     definition = "Whether media coverage was biased in favor of the incumbent during the election campaign (NELDA variable NELDA16).",
     source_reports = "NELDA via QoG Standard TS. Binary yes/no per election.",
     standalone_transform = "None - raw 0/1. RENAMED from the pipeline's WRONG label 'nelda_multiple_parties' (mbbe is a media-bias variable, not a party-count variable - the old name described an entirely different concept). Direction NEGATIVE.",
     panel_scaling = "NOT BUILT yet. Same event-level/scaling notes.",
     units = "Binary: 1 = media biased for incumbent (worse), 0 = not. Direction negative.",
     coverage = "82+ event-level coverage. NELDA is election-level: data exists only in election years (~24.5% of country-years), one observation per country-year, systematically ABSENT for ~21 consolidated democracies excluded by NELDA's design (absence implies established-democracy, i.e. implicitly clean - a coverage bias for the scaling layer to handle, not neutral missingness). Raw 99 ('unclear/could not code') converted to NaN in the QoG pipeline (nb 14).",
     caveats = "Supplementary in Concept 20. Sharpest NELDA discriminator: clean democracies 0.019 vs rigged autocracies 0.741.",
     status = "built",
 ),

 "nelda_riots_protests_after": dict(
     definition = "Whether there were riots and protests after the election involving allegations of vote fraud (NELDA).",
     source_reports = "NELDA via QoG Standard TS. Binary yes/no per election.",
     standalone_transform = "None - raw 0/1. RENAMED from the pipeline's WRONG label 'nelda_ruling_party_advantage' (rpae is post-election riots/protests, not ruling-party advantage). Direction NEGATIVE.",
     panel_scaling = "NOT BUILT yet. Same event-level/scaling notes.",
     units = "Binary: 1 = riots/protests after election (worse), 0 = not. Direction negative.",
     coverage = "82+ event-level coverage. NELDA is election-level: data exists only in election years (~24.5% of country-years), one observation per country-year, systematically ABSENT for ~21 consolidated democracies excluded by NELDA's design (absence implies established-democracy, i.e. implicitly clean - a coverage bias for the scaling layer to handle, not neutral missingness). Raw 99 ('unclear/could not code') converted to NaN in the QoG pipeline (nb 14).",
     caveats = "Supplementary in Concept 20. Validated: clean 0.019, rigged 0.329.",
     status = "built",
 ),

 "nelda_violence_deaths_before": dict(
     definition = "Whether there was significant violence involving civilian deaths immediately before or during the election (NELDA variable NELDA33).",
     source_reports = "NELDA via QoG Standard TS. Binary yes/no per election.",
     standalone_transform = "None - raw 0/1. RENAMED from the pipeline's imprecise label 'nelda_violence_candidate'. Direction NEGATIVE.",
     panel_scaling = "NOT BUILT yet. Same event-level/scaling notes.",
     units = "Binary: 1 = violence with civilian deaths (worse), 0 = not. Direction negative.",
     coverage = "82+ event-level coverage. NELDA is election-level: data exists only in election years (~24.5% of country-years), one observation per country-year, systematically ABSENT for ~21 consolidated democracies excluded by NELDA's design (absence implies established-democracy, i.e. implicitly clean - a coverage bias for the scaling layer to handle, not neutral missingness). Raw 99 ('unclear/could not code') converted to NaN in the QoG pipeline (nb 14).",
     caveats = "Supplementary in Concept 20. Validated: clean 0.000, rigged 0.167.",
     status = "built",
 ),

 "nelda_opposition_allowed": dict(
     definition = "Whether opposition was allowed to participate in the election (NELDA).",
     source_reports = "NELDA via QoG Standard TS. Binary yes/no per election.",
     standalone_transform = "None - raw 0/1. Name unchanged (was already correct). Direction POSITIVE (1 = opposition allowed = better).",
     panel_scaling = "NOT BUILT yet. Same event-level/scaling notes. Lower coverage (n=1130) - coded only where relevant.",
     units = "Binary: 1 = opposition allowed (better), 0 = not. Direction positive.",
     coverage = "82+ event-level coverage. NELDA is election-level: data exists only in election years (~24.5% of country-years), one observation per country-year, systematically ABSENT for ~21 consolidated democracies excluded by NELDA's design (absence implies established-democracy, i.e. implicitly clean - a coverage bias for the scaling layer to handle, not neutral missingness). Raw 99 ('unclear/could not code') converted to NaN in the QoG pipeline (nb 14).",
     caveats = "Supplementary in Concept 20. The one positively-directed NELDA metric. Validated: clean 1.000, rigged 0.727.",
     status = "built",
 ),

 "pefa_core_management": dict(
     definition = "How well a government runs the frontline machinery of managing public money - whether the budget is credible and executed as planned, and whether spending is controlled (procurement, payroll, tax administration, internal audit). Built from PEFA.",
     source_reports = "PEFA (Public Expenditure and Financial Accountability), the gold-standard PFM assessment. Indicators graded A-D (mapped to 4-1). Not a published composite - PEFA reports indicator-level grades only.",
     standalone_transform = "BUILT in src/derive_metrics.py. Mean of two PEFA PILLAR means: Pillar I (budget reliability, PI-01..03) and Pillar V (predictability and control in execution, PI-19..25). Each pillar = unweighted mean of its indicator scores; the composite = mean of the two pillar means (so the two pillars are equal-weighted regardless of indicator count). Single 2016-framework assessment per country. Validated: Georgia 3.30, Rwanda 3.06 (strong PFM), Chad 1.40, Nigeria 1.52 (weak).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 1-4 composite to the common framework scale. NOTE for Step-4: C8 uses INTENTIONAL sub-dimension weighting (fiscal 40 / monetary 40 / external 20) - this metric is in the FISCAL bucket; bucket weight must NOT be driven by metric count.",
     units = "Composite score 1-4 (D=1 to A=4). Higher is better.",
     coverage = "82 spine countries. CROSS-SECTIONAL: one assessment per country, vintage varies 2017-2026 (not a time series - PEFA assessments are irregular and cross-framework assessments are not comparable). Donor-driven coverage skews developing-heavy - a reference-class caveat at scaling.",
     caveats = "PFM leg of Concept 8 (Macroeconomic policy framework quality, which absorbed public financial management when C7 was folded in 2026-07-24). The frontline how-well-is-money-managed core, paired with pefa_accountability (back-end) and obs_open_budget_index (transparency). Single-vintage snapshot per country, NOT a trajectory.",
     status = "built",
 ),

 "pefa_accountability": dict(
     definition = "How well a government keeps and independently checks its financial books - whether accounts are properly kept, reconciled and reported, and whether external audit and legislative scrutiny of the budget and accounts function. Built from PEFA.",
     source_reports = "PEFA (Public Expenditure and Financial Accountability). Indicators graded A-D (mapped to 4-1). Not a published composite.",
     standalone_transform = "BUILT in src/derive_metrics.py. Mean of two PEFA PILLAR means: Pillar VI (accounting and reporting, PI-26..28) and Pillar VII (external scrutiny and audit, PI-29..31). Each pillar = unweighted mean of its indicators; composite = mean of the two pillar means. Single 2016-framework assessment per country. Validated: Georgia 3.67, Rwanda 2.92 (strong), Chad 1.17 (weak).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 1-4 composite to the common scale. NOTE for Step-4: in C8's FISCAL bucket (fiscal 40 / monetary 40 / external 20 sub-dimension weighting); bucket weight must NOT be driven by metric count.",
     units = "Composite score 1-4 (D=1 to A=4). Higher is better.",
     coverage = "82 spine countries. CROSS-SECTIONAL, one assessment per country, vintage varies 2017-2026 (not a time series). Donor-skewed developing-heavy coverage.",
     caveats = "PFM back-end (accounting + audit) leg of Concept 8. P2 (below pefa_core_management): more hygiene than frontline quality. IMPORTANT OVERLAP: Pillar VII (external scrutiny/audit) overlaps Concept 19 (Legislative and constitutional checks) legislative-oversight content - the audit/scrutiny signal is measured here (via PEFA) and in C19 (via V-Dem). NAMED for the Step-4 correlation-aware weighting item so the two are not treated as fully independent. Single-vintage snapshot per country.",
     status = "built",
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
     standalone_transform = "BUILT in src/derive_metrics.py. Row-wise MEAN of whichever of the three 1-5 coder columns (pts_amnesty, pts_hrw, pts_statedept) are present - a UNION (a country-year counts if ANY coder rated it). Validated: Canada/Norway/Sweden 1.0, China/Saudi 4.0, Syria 5.0 (2019); 190 countries covered.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 1-5 mean to the common scale, inverting so less state terror scores better.",
     units = "Score 1-5 (mean of available coders). Higher is WORSE (more state terror). Direction is negative.",
     coverage = "About 98% of country-years, largely via the State Department coding which has the widest reach.",
     caveats = "The three individual coder columns are not scored separately (they are the planned inputs to the mean). The combining mean is NOT yet implemented anywhere - it lives only as a plan in metric_selection. Scores two concepts: Concept 16 (Personal security and public order) as a primary leg, and Concept 22 (Civil liberties) as a supporting leg.",
     status = "built",
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
     source_reports = "Derived from V-Dem's Regimes of the World variable v2x_regime, a 0-3 typology (0 = closed autocracy, 1 = electoral autocracy, 2 = electoral democracy, 3 = liberal democracy). Per framework_decisions, the regime TYPE is not scored directionally (type is not a quality ordering), but its DURATION is a legitimate stability signal derived from it.",
     standalone_transform = "BUILT in src/derive_metrics.py. For each country-year, count consecutive years in the SAME v2x_regime category (reset to 1 the first year a new category appears; a category change resets the count). Then CAP at 30 years. A null v2x_regime breaks the run (that year is null, the run restarts after). Validated against Hungary (resets 2010 and 2018, its two real regime reclassifications) and France (stable, caps at 30).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 1-30 count to the common framework scale. The cap already handles the shape - scaling need not add further diminishing-returns treatment.",
     units = "Years in current regime category, capped at 30 (1-30). Higher = more durable/entrenched.",
     coverage = "172 spine countries (the V-Dem-covered ones). 41 spine micro-states/territories have no value; the closed regimes PRK/ERI/TKM and Taiwan are out of scope by design.",
     caveats = "DIRECTION-AGNOSTIC durability: a long-stable AUTOCRACY scores as high as a long-stable democracy - this measures entrenchment/predictability of the political order, NOT its quality, and must not be read as a governance-quality signal (it is one leg of C2, paired with coups, conflict, and WGI stability). CAP at 30 is deliberate: past ~one political generation more years do not mean more stability, and the cap makes pre-1990 left-censoring moot (a country stable since before the panel is >=30 and caps to 30 regardless of its unseen true start) AND severs the metric from panel length. Known property: compresses the top (all entrenched regimes read 30) - correct for a stability signal, which needs 'recently changed vs entrenched', not fine ranking among the entrenched. Scores Concept 2 (Political stability and government continuity).",
     status = "built",
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
    
# ---- Concept 18: Control of corruption ----
 # DIRECTION TRAP: the aggregate v2x_corr runs the OPPOSITE way to the four individual
 # corruption items. Do NOT infer direction from the "corruption" family name.

 "v2x_corr": dict(
     definition = "How corrupt a country is overall - the extent of corruption across the executive, legislature, judiciary, and public sector. V-Dem's political corruption index.",
     source_reports = "V-Dem index v2x_corr. Aggregate index scaled 0-1, where HIGHER means MORE corrupt. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 index to the common framework scale, INVERTING so that less corruption scores better.",
     units = "Index 0-1. Higher is WORSE (more corrupt). Direction is NEGATIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "REVERSE-CODED relative to the four individual V-Dem corruption items below. This aggregate runs higher=more-corrupt; the individual items run higher=LESS-corrupt. Verified empirically (v2x_corr correlates -0.88 with WGI, confirming higher=worse). Do NOT infer direction from the family name. Scores Concept 18 (Control of corruption).",
     status = "selected",
 ),

 "v2excrptps": dict(
     definition = "How free the executive is from bribery and graft - whether members of the executive grant favors in exchange for bribes or kickbacks. V-Dem's executive-bribery indicator (higher = LESS bribery).",
     source_reports = "V-Dem variable v2excrptps. Interval scale (~ -4 to +4, where HIGHER means LESS executive bribery / cleaner). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is BETTER (less bribery). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: unlike the v2x_corr aggregate, this individual item is coded higher=cleaner, so direction is POSITIVE. Scores Concept 18 (Control of corruption).",
     status = "selected",
 ),

 "v2exembez": dict(
     definition = "How free the executive is from embezzlement - whether members of the executive steal or misappropriate public funds. V-Dem's executive-embezzlement indicator (higher = LESS embezzlement).",
     source_reports = "V-Dem variable v2exembez. Interval scale (~ -4 to +4, where HIGHER means LESS embezzlement / cleaner). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is BETTER (less embezzlement). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: coded higher=cleaner, so direction is POSITIVE (opposite to the v2x_corr aggregate). Scores Concept 18 (Control of corruption).",
     status = "selected",
 ),

 "v2lgcrrpt": dict(
     definition = "How free the legislature is from corruption - whether legislators accept bribes or use their position for private gain. V-Dem's legislative-corruption indicator (higher = LESS corrupt).",
     source_reports = "V-Dem variable v2lgcrrpt. Interval scale (~ -4 to +4, where HIGHER means LESS legislative corruption / cleaner). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is BETTER (less corrupt). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: coded higher=cleaner, so direction is POSITIVE (opposite to the v2x_corr aggregate). Scores Concept 18 (Control of corruption).",
     status = "selected",
 ),

 "v2jucorrdc": dict(
     definition = "How free the judiciary is from corruption - whether judges or court officials accept bribes or improperly influence decisions. V-Dem's judicial-corruption indicator (higher = LESS corrupt).",
     source_reports = "V-Dem variable v2jucorrdc. Interval scale (~ -4 to +4, where HIGHER means LESS judicial corruption / cleaner). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is BETTER (less corrupt). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: coded higher=cleaner, so direction is POSITIVE (opposite to the v2x_corr aggregate). Rounds out the four-branch corruption picture (executive bribery, executive embezzlement, legislative, judicial) alongside the reverse-coded aggregate. Scores Concept 18 (Control of corruption).",
     status = "selected",
 ),

 # ---- Concept 19: Legislative and constitutional checks (interval + one 0-1 aggregate, direction +) ----
 "v2xlg_legcon": dict(
     definition = "How much the legislature constrains the executive - whether parliament can genuinely check and oversee the government. V-Dem's legislative-constraints index.",
     source_reports = "V-Dem index v2xlg_legcon. Aggregate index scaled 0-1, higher = stronger legislative constraints on the executive. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 index to the common framework scale.",
     units = "Index 0-1. Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "The headline index for this concept. Concept 19 is now SINGLE-SOURCE (V-Dem only) after Polity and CCP were dropped at Step-1 - see framework_decisions. Scores Concept 19 (Legislative and constitutional checks).",
     status = "selected",
 ),

 "v2lgoppart": dict(
     definition = "How much power the legislative opposition has - whether opposition parties can meaningfully participate in and influence legislative business. V-Dem's opposition-parties indicator.",
     source_reports = "V-Dem variable v2lgoppart. Interval scale (~ -4 to +4, higher = stronger opposition role). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 19 (Legislative and constitutional checks).",
     status = "selected",
 ),

 "v2lgqstexp": dict(
     definition = "Whether the legislature questions the executive - whether parliament routinely interrogates government officials about their conduct. V-Dem's legislature-questions-officials indicator.",
     source_reports = "V-Dem variable v2lgqstexp. Interval scale (~ -4 to +4, higher = more questioning of the executive). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 19 (Legislative and constitutional checks).",
     status = "selected",
 ),

 "v2lginvstp": dict(
     definition = "Whether the legislature can investigate the executive in practice - whether parliament has and uses the power to hold inquiries into government wrongdoing. V-Dem's legislature-investigates indicator.",
     source_reports = "V-Dem variable v2lginvstp. Interval scale (~ -4 to +4, higher = stronger investigative capacity). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 19 (Legislative and constitutional checks).",
     status = "selected",
 ),

 "v2lgotovst": dict(
     definition = "Whether an executive oversight body exists and operates - an independent body (like an ombudsman or comptroller) that monitors the executive on the legislature's behalf. V-Dem's executive-oversight indicator.",
     source_reports = "V-Dem variable v2lgotovst. Interval scale (~ -4 to +4, higher = stronger executive oversight). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 19 (Legislative and constitutional checks).",
     status = "selected",
 ),

# ---- Concept 20: Electoral process and competition ----
 # NOTE: v2elirreg/v2elintim/v2elvotbuy read like "bad things" but V-Dem codes them
 # higher=CLEANER (few irregularities = high score), so direction is POSITIVE.

 "v2x_polyarchy": dict(
     definition = "How democratic a country's elections and core political freedoms are overall - free and fair elections plus the freedoms that make them meaningful. V-Dem's electoral democracy (polyarchy) index.",
     source_reports = "V-Dem index v2x_polyarchy. Aggregate index scaled 0-1, higher = more electoral democracy. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 index to the common framework scale.",
     units = "Index 0-1. Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "The headline electoral-democracy index. Scores Concept 20 (Electoral process and competition).",
     status = "selected",
 ),

 "v2elfrfair": dict(
     definition = "How free and fair a country's elections are - taken as a whole, whether the most recent national election was clean. V-Dem's free-and-fair-elections indicator.",
     source_reports = "V-Dem variable v2elfrfair. Interval scale (~ -4 to +4, higher = freer and fairer). Coded for election years. Annual (carried between elections in the source).",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 20 (Electoral process and competition).",
     status = "selected",
 ),

 "v2elirreg": dict(
     definition = "How free elections are from irregularities - ballot-box fraud, miscounts, and other administrative manipulation. V-Dem's election-irregularities indicator (higher = FEWER irregularities).",
     source_reports = "V-Dem variable v2elirreg. Interval scale (~ -3 to +3, where HIGHER means FEWER irregularities / cleaner). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -3 to +3). Higher is BETTER (fewer irregularities). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: the name reads like a bad thing, but V-Dem codes it higher=cleaner, so direction is POSITIVE. Scores Concept 20 (Electoral process and competition).",
     status = "selected",
 ),

 "v2elintim": dict(
     definition = "How free elections are from voter intimidation - threats or coercion aimed at voters. V-Dem's election-intimidation indicator (higher = LESS intimidation).",
     source_reports = "V-Dem variable v2elintim. Interval scale (~ -3 to +3, where HIGHER means LESS intimidation). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -3 to +3). Higher is BETTER (less intimidation). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: coded higher=less-intimidation, so direction is POSITIVE. Scores Concept 20 (Electoral process and competition).",
     status = "selected",
 ),

 "v2elvotbuy": dict(
     definition = "How free elections are from vote-buying - offering money or goods in exchange for votes. V-Dem's vote-buying indicator (higher = LESS vote-buying).",
     source_reports = "V-Dem variable v2elvotbuy. Interval scale (~ -3 to +3, where HIGHER means LESS vote-buying). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -3 to +3). Higher is BETTER (less vote-buying). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: coded higher=less-vote-buying, so direction is POSITIVE. Scores Concept 20 (Electoral process and competition).",
     status = "selected",
 ),

 "v2elaccept": dict(
     definition = "Whether losing parties accept election results - whether defeated candidates concede peacefully rather than reject the outcome. V-Dem's election-acceptance indicator.",
     source_reports = "V-Dem variable v2elaccept. Interval scale (~ -4 to +4, higher = results more readily accepted by losers). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 20 (Electoral process and competition).",
     status = "selected",
 ),

 "v2elembaut": dict(
     definition = "How autonomous the election management body is - whether the body running elections is free from government interference. V-Dem's EMB-autonomy indicator.",
     source_reports = "V-Dem variable v2elembaut. Interval scale (~ -3 to +4, higher = more autonomous election administration). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -3 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Closes the C20 election-administration leg and supersedes a standalone IDEA EMB build (V-Dem's EMB items cover it with clean directionality). Scores Concept 20 (Electoral process and competition).",
     status = "selected",
 ),

 "v2elembcap": dict(
     definition = "How capable the election management body is - whether it has the capacity and resources to run elections properly. V-Dem's EMB-capacity indicator.",
     source_reports = "V-Dem variable v2elembcap. Interval scale (~ -3 to +4, higher = more capable election administration). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -3 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "The capacity companion to v2elembaut; together they close the C20 EMB leg. Scores Concept 20 (Electoral process and competition).",
     status = "selected",
 ),

 # ---- Concept 21: Political participation beyond voting (several also score C24/C25) ----
 "v2x_partip": dict(
     definition = "How much citizens participate in political life beyond just voting - through civil society, local government, and direct engagement. V-Dem's participatory component index.",
     source_reports = "V-Dem index v2x_partip. Aggregate index scaled 0-1, higher = more participation. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 index to the common framework scale.",
     units = "Index 0-1. Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "The headline participation index. Scores Concept 21 (Political participation beyond voting).",
     status = "selected",
 ),

 "v2psprlnks": dict(
     definition = "How parties connect to citizens - whether parties link to voters through genuine engagement rather than clientelism or personality alone. V-Dem's party-linkages indicator.",
     source_reports = "V-Dem variable v2psprlnks. Interval scale (~ -4 to +4, higher = stronger programmatic party-citizen linkages). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 21 (Political participation beyond voting).",
     status = "selected",
 ),

 "v2pscohesv": dict(
     definition = "How cohesive political parties are - whether parties act as organized, disciplined bodies rather than loose personal vehicles. V-Dem's party-cohesion indicator.",
     source_reports = "V-Dem variable v2pscohesv. Interval scale (~ -4 to +4, higher = more cohesive parties). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "The weakest V-Dem signal against WGI (correlation +0.34) - a genuine but modest contributor. Scores Concept 21 (Political participation beyond voting).",
     status = "selected",
 ),

 "v2cseeorgs": dict(
     definition = "How free civil society organizations are to enter and operate - whether people can form and run CSOs without state obstruction. V-Dem's CSO-entry-and-exit indicator.",
     source_reports = "V-Dem variable v2cseeorgs. Interval scale (~ -4 to +4, higher = freer CSO entry/operation). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores TWO concepts: Concept 21 (Political participation beyond voting) and Concept 24 (Civil society space and vitality).",
     status = "selected",
 ),

 "v2dlconslt": dict(
     definition = "How much the government consults the public in policymaking - whether major decisions involve genuine consultation with affected groups. V-Dem's engaged-consultation indicator.",
     source_reports = "V-Dem variable v2dlconslt. Interval scale (~ -4 to +4, higher = more public consultation). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores TWO concepts: Concept 21 (Political participation beyond voting) and Concept 25 (Government transparency and openness).",
     status = "selected",
 ),

 "v2csreprss": dict(
     definition = "How free civil society is from government repression - whether the state harasses, restricts, or crushes civil society organizations. V-Dem's CSO-repression indicator (higher = LESS repression).",
     source_reports = "V-Dem variable v2csreprss. Interval scale (~ -4 to +4, where HIGHER means LESS repression). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is BETTER (less repression). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: coded higher=less-repression, so direction is POSITIVE despite the name. Scores TWO concepts: Concept 21 (Political participation beyond voting) and Concept 24 (Civil society space and vitality).",
     status = "selected",
 ),

# ---- Concept 22: Civil liberties (interval items + v2x_civlib/v2x_clpriv 0-1 aggregates) ----
 "v2x_civlib": dict(
     definition = "How well a country protects civil liberties overall - physical integrity, private freedoms, and political liberties combined. V-Dem's civil liberties index.",
     source_reports = "V-Dem index v2x_civlib. Aggregate index scaled 0-1, higher = stronger civil liberties. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 index to the common framework scale.",
     units = "Index 0-1. Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "The headline civil-liberties index. Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 "v2x_clpriv": dict(
     definition = "How well a country protects private civil liberties - freedom from forced labor, property rights, freedom of movement, and freedom of religion. V-Dem's private civil liberties index.",
     source_reports = "V-Dem index v2x_clpriv. Aggregate index scaled 0-1, higher = stronger private liberties. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 index to the common framework scale.",
     units = "Index 0-1. Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 "v2clrelig": dict(
     definition = "How free people are to practice religion - whether the state restricts religious belief and worship. V-Dem's freedom-of-religion indicator.",
     source_reports = "V-Dem variable v2clrelig. Interval scale (~ -4 to +4, higher = more religious freedom). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 "v2cldmovem": dict(
     definition = "How free men are to move around - domestic and foreign travel without arbitrary restriction. V-Dem's freedom-of-movement-for-men indicator.",
     source_reports = "V-Dem variable v2cldmovem. Interval scale (~ -4 to +4, higher = more freedom of movement). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Paired with the women's movement item (v2cldmovew). Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 "v2cldmovew": dict(
     definition = "How free women are to move around - domestic and foreign travel without arbitrary restriction. V-Dem's freedom-of-movement-for-women indicator.",
     source_reports = "V-Dem variable v2cldmovew. Interval scale (~ -4 to +4, higher = more freedom of movement). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "The women's counterpart to v2cldmovem (the master names the pair 'v2cldmovem/w'). Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 "v2clsocgrp": dict(
     definition = "How equally civil liberties are enjoyed across social groups - whether some ethnic, religious, or other groups face weaker rights protection. V-Dem's social-group-equality-in-liberties indicator.",
     source_reports = "V-Dem variable v2clsocgrp. Interval scale (~ -4 to +4, higher = more equal enjoyment of liberties across groups). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 "v2clslavef": dict(
     definition = "How free people are from forced labor - the absence of slavery and coerced work. V-Dem's freedom-from-forced-labor indicator (higher = LESS forced labor).",
     source_reports = "V-Dem variable v2clslavef. Interval scale (~ -4 to +4, where HIGHER means LESS forced labor). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is BETTER (less forced labor). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: coded higher=less-forced-labor, so direction is POSITIVE. Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 # ---- Concept 23: Media freedom and pluralism ----
 # The individual media items read like bad things (censorship, harassment, self-censorship,
 # bias) but V-Dem codes them higher=BETTER (less of the bad thing). Verified against the data.

 "v2x_freexp_altinf": dict(
     definition = "How free expression and access to alternative information are overall - media freedom, freedom of speech, and the availability of independent information sources. V-Dem's freedom-of-expression index.",
     source_reports = "V-Dem index v2x_freexp_altinf. Aggregate index scaled 0-1, higher = more free expression and information access. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 index to the common framework scale.",
     units = "Index 0-1. Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "The headline media/expression index. Scores Concept 23 (Media freedom and pluralism).",
     status = "selected",
 ),

 "v2mecenefm": dict(
     definition = "How free the media is from government censorship - direct and indirect censorship of print and broadcast. V-Dem's media-censorship indicator (higher = LESS censorship).",
     source_reports = "V-Dem variable v2mecenefm. Interval scale (~ -3 to +3, where HIGHER means LESS censorship). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -3 to +3). Higher is BETTER (less censorship). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: coded higher=less-censorship, so direction is POSITIVE. Scores Concept 23 (Media freedom and pluralism).",
     status = "selected",
 ),

 
 "v2mecorrpt": dict(
     definition = "How free the media is from corruption - whether journalists and outlets take bribes to publish or suppress stories. V-Dem's media-corruption indicator (higher = LESS media corruption).",
     source_reports = "V-Dem variable v2mecorrpt. Interval scale (~ -3 to +3, where HIGHER means LESS media corruption). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -3 to +3). Higher is BETTER (less corruption). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: coded higher=less-media-corruption, so direction is POSITIVE. Scores Concept 23 (Media freedom and pluralism).",
     status = "selected",
 ),

 
 "v2merange": dict(
     definition = "How wide the range of political perspectives in the media is - whether many viewpoints are represented or coverage is narrow. V-Dem's media-perspectives-range indicator.",
     source_reports = "V-Dem variable v2merange. Interval scale (~ -3 to +3, higher = wider range of perspectives). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -3 to +3). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 23 (Media freedom and pluralism).",
     status = "selected",
 ),

 "v2mebias": dict(
     definition = "How free media coverage is from bias - whether outlets cover the opposition as well as the government fairly. V-Dem's media-bias indicator (higher = LESS bias).",
     source_reports = "V-Dem variable v2mebias. Interval scale (~ -3 to +3, where HIGHER means LESS bias). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -3 to +3). Higher is BETTER (less bias). Direction is POSITIVE.",
     coverage = "Near-universal (~180 countries).",
     caveats = "DIRECTION: coded higher=less-bias, so direction is POSITIVE. Scores Concept 23 (Media freedom and pluralism).",
     status = "selected",
 ),

 
 # ---- Concept 24: Civil society space (C24-only; the other C24 items sit under C21) ----
 "v2cscnsult": dict(
     definition = "How routinely the government consults civil society organizations - whether CSOs are involved in policymaking. V-Dem's CSO-consultation indicator.",
     source_reports = "V-Dem variable v2cscnsult. Interval scale (~ -4 to +4, higher = more CSO consultation). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 24 (Civil society space and vitality).",
     status = "selected",
 ),

 "v2csprtcpt": dict(
     definition = "How actively citizens participate in civil society organizations - whether CSOs draw broad, engaged membership rather than being hollow or elite-only. V-Dem's CSO-participatory-environment indicator.",
     source_reports = "V-Dem variable v2csprtcpt. Interval scale (~ -4 to +4, higher = more active civil-society participation). Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "V-Dem interval scale (~ -4 to +4). Higher is better.",
     coverage = "Near-universal (~180 countries).",
     caveats = "Scores Concept 24 (Civil society space and vitality).",
     status = "selected",
 ),

# ================= WB Carbon Pricing Dashboard =================

 "wb_carbon_pricing_exists": dict(
     definition = "Whether a country has a carbon price in force - a carbon tax or emissions trading scheme actually implemented. From the World Bank Carbon Pricing Dashboard.",
     source_reports = "World Bank Carbon Pricing Dashboard, per instrument (carbon taxes and ETS) with status and jurisdiction. Not a country-level flag as delivered.",
     standalone_transform = "Built in-pipeline (nb 20): set to 1 if the country has at least one IMPLEMENTED national carbon-pricing instrument (planned/under-consideration excluded). EU ETS is expanded to all EU member states. Otherwise 0.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: use the 0/1 flag on the common framework scale.",
     units = "Binary 0/1. 1 = a carbon price exists. Higher is better.",
     coverage = "Broad; most countries (0 where no scheme).",
     caveats = "National schemes only; subnational (e.g. US state) schemes are not counted at country level. Scores Concept 12 (Environmental and climate governance).",
     status = "selected",
 ),

 "wb_carbon_price_usd": dict(
     definition = "How high a country's carbon price is - the price per tonne of CO2, a measure of how strong the price signal is. From the World Bank Carbon Pricing Dashboard.",
     source_reports = "World Bank Carbon Pricing Dashboard, price per instrument in US dollars per tonne CO2-equivalent.",
     standalone_transform = "Built in-pipeline (nb 20): the MEAN price across a country's implemented instruments in each country-year, in US$/tCO2e. Zero or blank where no scheme.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the price to the common framework scale.",
     units = "US dollars per tonne CO2e. Higher = stronger price signal (better).",
     coverage = "Only countries with a carbon price (others are zero/absent).",
     caveats = "Price LEVEL, a strength signal distinct from mere existence. Scores Concept 12 (Environmental and climate governance).",
     status = "selected",
 ),

 "wb_carbon_coverage_pct": dict(
     definition = "What share of a country's greenhouse-gas emissions its carbon price covers - how much of the economy the price signal reaches. From the World Bank Carbon Pricing Dashboard.",
     source_reports = "World Bank Carbon Pricing Dashboard, share of jurisdiction emissions covered by each instrument.",
     standalone_transform = "Built in-pipeline (nb 20): the MAX jurisdictional coverage share for the country. Flagged as a current SNAPSHOT (wb_carbon_coverage_is_snapshot) where only the latest coverage figure is available rather than a full time series.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the coverage percentage to the common framework scale.",
     units = "Percent of emissions covered (0-100). Higher is better.",
     coverage = "Only countries with a carbon price. Some values are a latest-snapshot rather than time-varying.",
     caveats = "Coverage BREADTH, distinct from price level and existence. Snapshot flag matters for historical years. Scores Concept 12 (Environmental and climate governance).",
     status = "selected",
 ),

 "wb_carbon_revenue_pct_gdp": dict(
     definition = "How much carbon-pricing revenue a country raises relative to the size of its economy - revenue as a share of GDP. Planned, from World Bank carbon revenue and WDI GDP.",
     source_reports = "World Bank Carbon Pricing Dashboard provides raw carbon revenue (stored as wb_carbon_revenue_usd_m, US$ millions). GDP would come from WDI. The RATIO is not published.",
     standalone_transform = "BUILT in src/derive_metrics.py. Raw carbon revenue (wb_carbon_revenue_usd_m, US$m) x 1e6 / total GDP x 100, expressed as PERCENT of GDP. Total GDP is reconstructed as wdi_gdp_per_capita_usd x wdi_population_total (same WDI row, so exact). Coverage is the INTERSECTION of carbon-revenue and GDP (39 countries). Validated: Sweden 0.39pct, France 0.35pct, Germany 0.30pct of GDP - the expected 0.1-0.7pct band for EU carbon-pricers.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the revenue/GDP ratio to the common framework scale.",
     units = "Planned: carbon revenue as percent of GDP. Higher = more revenue raised relative to economy.",
     coverage = "Would be the intersection of countries with carbon revenue and GDP data.",
     caveats = "PLANNED metric - the ratio is not yet computed (raw revenue is stored, the /GDP step is deferred to the metric pass). Scores Concept 12 (Environmental and climate governance).",
     status = "built",
 ),

 # ================= Powell-Thyne Coups =================
 # Raw coup counts; more coups = worse (direction negative).

 "pt_coup_successful": dict(
     definition = "How many successful coups d'etat a country has had - forcible, unconstitutional seizures of executive power that succeeded. From the Powell-Thyne coup dataset.",
     source_reports = "Powell and Thyne coup dataset (via the authors' data). Coup events coded by outcome; a successful coup is one where the perpetrators held power at least a week. Raw event count.",
     standalone_transform = "None beyond selection/rename (from the source's successful-coup coding). A count of successful coups per country-year.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: likely a recency-weighted or windowed treatment of the count, then convert to the common scale, inverting so fewer coups score better.",
     units = "Count of successful coups. Higher is WORSE. Direction is negative.",
     coverage = "Global, 1950 onward. Most country-years are zero.",
     caveats = "Paired with pt_coup_failed. A direct instability signal. Scores Concept 2 (Political stability and government continuity).",
     status = "selected",
 ),

 "pt_coup_failed": dict(
     definition = "How many failed coup attempts a country has had - unconstitutional seizure attempts that did not succeed. From the Powell-Thyne coup dataset.",
     source_reports = "Powell and Thyne coup dataset. A failed coup is an attempt where perpetrators did not hold power for at least a week. Raw event count.",
     standalone_transform = "None beyond selection/rename (from the source's failed-coup coding). A count of failed coup attempts per country-year.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: as with successful coups, a windowed treatment then convert to the common scale, inverting so fewer attempts score better.",
     units = "Count of failed coup attempts. Higher is WORSE. Direction is negative.",
     coverage = "Global, 1950 onward. Most country-years are zero.",
     caveats = "Even FAILED attempts signal instability, so they are scored alongside successful coups rather than ignored. Scores Concept 2 (Political stability and government continuity).",
     status = "selected",
 ),

 # ================= WDI - built vs planned =================

 "wdi_tariff_rate_simple_mean": dict(
     definition = "A country's average import tariff rate - the simple (unweighted) mean tariff across product lines. A marker of trade openness. From World Development Indicators.",
     source_reports = "World Bank WDI, simple mean applied tariff rate, all products (code TM.TAX.MRCH.SM.AR.ZS). Published as a percentage. HIGHER = higher tariffs (more protectionist).",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale, inverting so lower tariffs score better.",
     units = "Percent (average tariff rate). Higher is WORSE (more protectionist). Direction is negative.",
     coverage = "Broad, most countries, though tariff data lags a few years.",
     caveats = "Simple (unweighted) mean, so every product line counts equally regardless of trade volume. Scores Concept 11 (Trade governance).",
     status = "selected",
 ),

 "wdi_education_index": dict(
     definition = "A country's education outcomes overall - a planned composite of schooling and learning indicators. Intended to be built from World Development Indicators components.",
     source_reports = "World Bank WDI. The pipeline pulls education COMPONENT indicators (e.g. completion rates, enrollment), but WDI publishes no single 'education index' at this composition.",
     standalone_transform = "NOT BUILT. The composite column does not exist in wdi_clean.csv - only the raw components do. It appears only in the metric_selection record. PLANNED: combine the education components into one index (likely a mean of available components, so coverage would be their UNION).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the composite to the common framework scale.",
     units = "Planned composite (scale to be set on construction). Higher = better education outcomes.",
     coverage = "Would follow the component union once built.",
     caveats = "PLANNED metric - neither the composite nor its scoring exists yet. Scores Concept 5 (Public service delivery and human development).",
     status = "selected",
 ),

 "wdi_health_index": dict(
     definition = "A country's health outcomes overall - a planned composite of health indicators. Intended to be built from World Development Indicators components.",
     source_reports = "World Bank WDI. The pipeline pulls health COMPONENT indicators (e.g. UHC coverage, immunization, mortality), but publishes no single 'health index' at this composition.",
     standalone_transform = "NOT BUILT. The composite does not exist in wdi_clean.csv - only raw components (including wdi_uhc_coverage_index, which IS a published WB sub-index). PLANNED: combine health components into one index (likely mean-of-available, coverage = union).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the composite to the common framework scale.",
     units = "Planned composite. Higher = better health outcomes.",
     coverage = "Would follow the component union once built.",
     caveats = "PLANNED metric - not yet built. Scores Concept 5 (Public service delivery and human development).",
     status = "selected",
 ),

 "wdi_infrastructure_index": dict(
     definition = "A country's infrastructure quality overall - a planned composite of access indicators (electricity, water, sanitation, connectivity). Intended to be built from World Development Indicators components.",
     source_reports = "World Bank WDI. The pipeline pulls infrastructure COMPONENT indicators, but publishes no single 'infrastructure index' at this composition.",
     standalone_transform = "NOT BUILT. The composite does not exist in wdi_clean.csv - only raw components. PLANNED: combine infrastructure-access components into one index (likely mean-of-available, coverage = union).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the composite to the common framework scale.",
     units = "Planned composite. Higher = better infrastructure.",
     coverage = "Would follow the component union once built.",
     caveats = "PLANNED metric - not yet built. Scores Concept 5 (Public service delivery and human development).",
     status = "selected",
 ),

 "wdi_social_protection_index": dict(
     definition = "A country's social-protection coverage overall - a planned composite of social-safety-net indicators. Intended to be built from World Development Indicators components.",
     source_reports = "World Bank WDI. The pipeline pulls social-protection COMPONENT indicators, but publishes no single 'social protection index' at this composition.",
     standalone_transform = "NOT BUILT. The composite does not exist in wdi_clean.csv - only raw components. PLANNED: combine social-protection components into one index (likely mean-of-available, coverage = union).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the composite to the common framework scale.",
     units = "Planned composite. Higher = better social protection.",
     coverage = "Would follow the component union once built.",
     caveats = "PLANNED metric - not yet built. Scores Concept 5 (Public service delivery and human development).",
     status = "selected",
 ),

 
# ================= WJP Rule of Law Index =================
 # Eight factor scores, all 0-1, higher = more rule of law. Scored individually
 # (decompose): the framework, not WJP, controls how factors weight into concepts.

 "wjp_f2_absence_corruption": dict(
     definition = "How free a country's government is from corruption - across the executive, judiciary, military/police, and legislature. WJP Rule of Law Index, Factor 2.",
     source_reports = "World Justice Project Rule of Law Index, Factor 2 (Absence of Corruption). Published 0-1, higher = less corruption. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 score to the common framework scale.",
     units = "Score 0-1. Higher is better (less corruption).",
     coverage = "About 140 countries.",
     caveats = "Scored as its own factor (decompose-or-keep-whole: the framework controls how WJP factors weight into concepts, not WJP). Scores Concept 18 (Control of corruption).",
     status = "selected",
 ),

 "wjp_f3_open_government": dict(
     definition = "How open a country's government is - publicized laws, right to information, civic participation, and complaint mechanisms. WJP Rule of Law Index, Factor 3.",
     source_reports = "World Justice Project Rule of Law Index, Factor 3 (Open Government). Published 0-1, higher = more open. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 score to the common framework scale.",
     units = "Score 0-1. Higher is better.",
     coverage = "About 140 countries.",
     caveats = "Scores TWO concepts: Concept 7 (Public financial management) and Concept 25 (Government transparency and openness).",
     status = "selected",
 ),

 "wjp_f4_fundamental_rights": dict(
     definition = "How well a country protects fundamental rights - equal treatment, life and security, due process, expression, religion, privacy, association, and labor rights. WJP Rule of Law Index, Factor 4.",
     source_reports = "World Justice Project Rule of Law Index, Factor 4 (Fundamental Rights). Published 0-1, higher = stronger rights protection. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 score to the common framework scale.",
     units = "Score 0-1. Higher is better.",
     coverage = "About 140 countries.",
     caveats = "Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

 "wjp_f5_order_security": dict(
     definition = "How well a country maintains order and security - control of crime, civil conflict, and political violence. WJP Rule of Law Index, Factor 5.",
     source_reports = "World Justice Project Rule of Law Index, Factor 5 (Order and Security). Published 0-1, higher = more order/security. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 score to the common framework scale.",
     units = "Score 0-1. Higher is better.",
     coverage = "About 140 countries.",
     caveats = "Scores TWO concepts: Concept 16 (Personal security and public order) and Concept 2 (Political stability and government continuity).",
     status = "selected",
 ),

 "wjp_f6_regulatory_enforcement": dict(
     definition = "How well a country enforces regulations - whether rules are applied and enforced without improper influence or unreasonable delay, with respect for due process. WJP Rule of Law Index, Factor 6.",
     source_reports = "World Justice Project Rule of Law Index, Factor 6 (Regulatory Enforcement). Published 0-1, higher = better enforcement. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 score to the common framework scale.",
     units = "Score 0-1. Higher is better.",
     coverage = "About 140 countries.",
     caveats = "Scores TWO concepts: Concept 6 (Regulatory quality and business environment) and Concept 14 (Legal quality and predictability).",
     status = "selected",
 ),

 "wjp_f6_5_no_expropriation": dict(
     definition = "How free people and businesses are from unlawful expropriation - whether the government takes property without due process or adequate compensation. WJP sub-factor 6.5.",
     source_reports = "World Justice Project Rule of Law Index, sub-factor 6.5 (government does not expropriate without lawful process and adequate compensation). Published 0-1, higher = more protected. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 score to the common framework scale.",
     units = "Score 0-1. Higher is better.",
     coverage = "About 140 countries.",
     caveats = "A sub-factor (not a top-level factor), pulled specifically for its expropriation signal. Scores Concept 17 (Property rights and contract enforcement).",
     status = "selected",
 ),

 "wjp_f7_civil_justice": dict(
     definition = "How accessible and effective a country's civil justice is - whether people can resolve civil disputes affordably, without discrimination or delay, through impartial courts. WJP Rule of Law Index, Factor 7.",
     source_reports = "World Justice Project Rule of Law Index, Factor 7 (Civil Justice). Published 0-1, higher = better civil justice. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 score to the common framework scale.",
     units = "Score 0-1. Higher is better.",
     coverage = "About 140 countries.",
     caveats = "Scores Concept 15 (Judicial independence and quality).",
     status = "selected",
 ),

 "wjp_f8_criminal_justice": dict(
     definition = "How effective and fair a country's criminal justice is - effective investigation and adjudication, impartiality, due process, and freedom from corruption in the criminal system. WJP Rule of Law Index, Factor 8.",
     source_reports = "World Justice Project Rule of Law Index, Factor 8 (Criminal Justice). Published 0-1, higher = better criminal justice. Annual.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-1 score to the common framework scale.",
     units = "Score 0-1. Higher is better.",
     coverage = "About 140 countries.",
     caveats = "Scores Concept 15 (Judicial independence and quality).",
     status = "selected",
 ),

 # ================= Freedom in the World (Freedom House) =================
 # Sub-aggregate point totals scored individually (decompose), each with its own max.

 "fh_a_electoral_process": dict(
     definition = "How free and fair a country's electoral process is - whether the head of government and legislature are chosen in genuine elections under fair laws. Freedom in the World subcategory A.",
     source_reports = "Freedom House, Freedom in the World, subcategory A (Electoral Process) point total. Scored 0-12 (three questions, 0-4 each), higher = freer elections. Annual.",
     standalone_transform = "None. Selected and used as-published (the FH subcategory total, not the rolled-up PR/CL scores).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-12 total to the common framework scale.",
     units = "Point total 0-12. Higher is better.",
     coverage = "Near-universal (~195 countries/territories).",
     caveats = "Scored at the subcategory level, not FH's aggregate PR/CL scores (decompose: the framework controls how FH parts weight into concepts). Scores Concept 20 (Electoral process and competition).",
     status = "selected",
 ),

 "fh_d_expression_belief": dict(
     definition = "How free expression and belief are - freedom of media, religious practice, academic freedom, and open private discussion. Freedom in the World subcategory D.",
     source_reports = "Freedom House, Freedom in the World, subcategory D (Freedom of Expression and Belief) point total. Scored 0-16 (four questions, 0-4 each), higher = freer. Annual.",
     standalone_transform = "None. Selected and used as-published (the FH subcategory total).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-16 total to the common framework scale.",
     units = "Point total 0-16. Higher is better.",
     coverage = "Near-universal (~195 countries/territories).",
     caveats = "Scores TWO concepts: Concept 23 (Media freedom and pluralism) and Concept 22 (Civil liberties).",
     status = "selected",
 ),

 "fh_e_associational_rights": dict(
     definition = "How free people are to associate and organize - freedom of assembly, freedom for civic and NGO groups, and free trade unions. Freedom in the World subcategory E.",
     source_reports = "Freedom House, Freedom in the World, subcategory E (Associational and Organizational Rights) point total. Scored 0-12 (three questions, 0-4 each), higher = freer. Annual.",
     standalone_transform = "None. Selected and used as-published (the FH subcategory total).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-12 total to the common framework scale.",
     units = "Point total 0-12. Higher is better.",
     coverage = "Near-universal (~195 countries/territories).",
     caveats = "Scores Concept 24 (Civil society space and vitality).",
     status = "selected",
 ),

 "fh_g_personal_autonomy": dict(
     definition = "How much personal autonomy and individual rights people have - freedom of movement, property rights, personal social freedoms, and equality of opportunity. Freedom in the World subcategory G.",
     source_reports = "Freedom House, Freedom in the World, subcategory G (Personal Autonomy and Individual Rights) point total. Scored 0-16 (four questions, 0-4 each), higher = more autonomy. Annual.",
     standalone_transform = "None. Selected and used as-published (the FH subcategory total).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-16 total to the common framework scale.",
     units = "Point total 0-16. Higher is better.",
     coverage = "Near-universal (~195 countries/territories).",
     caveats = "Scores Concept 22 (Civil liberties).",
     status = "selected",
 ),

# ================= EPI (Yale Environmental Performance Index) =================
 # Issue-category scores 0-100, higher=better. Scored at issue-category level (decompose),
 # not the nested parent objectives.

 "epi_agr": dict(
     definition = "How sustainable a country's agriculture is - sustainable nitrogen use and agricultural practices. Yale EPI issue category, Agriculture.",
     source_reports = "Yale Environmental Performance Index, issue category 'agr' (Agriculture). Published 0-100, higher = more sustainable. Biennial.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-100 score to the common framework scale.",
     units = "Score 0-100. Higher is better.",
     coverage = "About 180 countries.",
     caveats = "Scored at the issue-category level (decompose), not EPI's nested parent objectives. Scores Concept 12 (Environmental and climate governance).",
     status = "selected",
 ),

 "epi_bdh": dict(
     definition = "How well a country protects biodiversity and habitat - protected areas, species protection, and habitat conservation. Yale EPI issue category, Biodiversity and Habitat.",
     source_reports = "Yale Environmental Performance Index, issue category 'bdh' (Biodiversity and Habitat). Published 0-100, higher = better protection. Biennial.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-100 score to the common framework scale.",
     units = "Score 0-100. Higher is better.",
     coverage = "About 180 countries.",
     caveats = "Scored at the issue-category level (decompose). Scores Concept 12 (Environmental and climate governance).",
     status = "selected",
 ),

 "epi_cch": dict(
     definition = "How well a country is mitigating climate change - progress on cutting greenhouse-gas emissions and related trends. Yale EPI issue category, Climate Change.",
     source_reports = "Yale Environmental Performance Index, issue category 'cch' (Climate Change). Published 0-100, higher = better mitigation. Biennial.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-100 score to the common framework scale.",
     units = "Score 0-100. Higher is better.",
     coverage = "About 180 countries.",
     caveats = "Scored at the issue-category level (decompose). An outcome/trend measure alongside the policy-based climate metrics. Scores Concept 12 (Environmental and climate governance).",
     status = "selected",
 ),

 "epi_wrs": dict(
     definition = "How well a country manages water resources - chiefly wastewater treatment and sanitation infrastructure. Yale EPI issue category, Water Resources.",
     source_reports = "Yale Environmental Performance Index, issue category 'wrs' (Water Resources). Published 0-100, higher = better management. Biennial.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-100 score to the common framework scale.",
     units = "Score 0-100. Higher is better.",
     coverage = "About 180 countries.",
     caveats = "Scored at the issue-category level (decompose). Scores Concept 12 (Environmental and climate governance).",
     status = "selected",
 ),

 # ================= ASCOR (TPI Centre / LSE) sovereign climate assessment =================

 "ascor_climate_governance": dict(
     definition = "How well a sovereign governs its climate transition - the strength of its climate policy framework: legislation, targets, carbon pricing, and just-transition provisions. Built from the ASCOR assessment.",
     source_reports = "ASCOR (Assessing Sovereign Climate-related Opportunities and Risks), TPI Centre at LSE. An investor-led assessment answering yes/no/partial questions across several climate-policy areas. Not a single published score.",
     standalone_transform = "Built in-pipeline (nb 40): take the MEAN across the 5 assessment areas that ALL assessed countries answer, deliberately excluding areas that ASCOR exempts for certain income groups (so every country is scored on a common basis). Higher = stronger climate governance.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the composite to the common framework scale.",
     units = "Built composite (mean of 5 areas). Higher is better.",
     coverage = "About 85 countries, EM/frontier-oriented.",
     caveats = "OUR composite over the 5 universally-answered areas (not all 9 - the income-group-exempted areas are excluded by design so coverage is comparable). ASCOR_SCORED_AREAS is a hardcoded pipeline judgment flagged for re-validation on any methodology change. Added at source level 2026-07-21. Scores Concept 12 (Environmental and climate governance).",
     status = "selected",
 ),

 # ================= RTI Rating =================

 "rti_total": dict(
     definition = "How strong a country's right-to-information (freedom of information) LAW is on paper - the legal framework for public access to government-held information. The RTI Rating total.",
     source_reports = "RTI Rating (Access Info Europe and the Centre for Law and Democracy). Total of 7 sub-category point scores, on a 0-150 scale, higher = stronger RTI law. Parses cleanly from the RTI Rating website. Updated as laws change.",
     standalone_transform = "None. The published total is used as-published (the 7 sub-scores are dropped - decompose-or-keep-whole: one coherent legal-quality construct on the CLD international-standards weighting).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert the 0-150 total to the common framework scale.",
     units = "Score 0-150. Higher is better (stronger law).",
     coverage = "About 140 countries with an RTI law (a has_rti_law flag marks those without, which are floored).",
     caveats = "DE JURE - measures the LAW on paper, not whether access works in practice (e.g. Afghanistan scores 139/150 on paper). Scores TWO concepts: Concept 25 (Government transparency and openness) and Concept 23 (Media freedom and pluralism).",
     status = "selected",
 ),

 # ================= TI Political Finance Database =================

 "polfin_transparency_integrity": dict(
     definition = "How transparent and well-regulated a country's political finance is - rules on disclosure, donation limits, and oversight of money in politics. From the political finance database.",
     source_reports = "Political finance transparency/integrity sub-index (International IDEA / TI political finance data). Higher = stronger political-finance regulation and transparency.",
     standalone_transform = "None. Selected and used as-published.",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "Sub-index score. Higher is better.",
     coverage = "Broad, most countries.",
     caveats = "One of the few sources unique to Concept 25 (little overlap with other concepts' sources). Scores Concept 25 (Government transparency and openness).",
     status = "selected",
 ),

 # ================= OECD Trade Facilitation Indicators =================

 "tfi_avg": dict(
     definition = "How efficient a country's trade procedures are - the average of OECD Trade Facilitation Indicators covering customs, formalities, documentation, and border-agency cooperation. A measure of how smoothly goods cross the border.",
     source_reports = "OECD Trade Facilitation Indicators, average across the TFI sub-indicators. Published roughly 0-2, higher = better trade facilitation. Periodic updates.",
     standalone_transform = "None. Selected and used as-published (the TFI average).",
     panel_scaling = "NOT BUILT yet (the scoring layer does not exist). Planned: convert to the common framework scale.",
     units = "TFI score (~0-2). Higher is better.",
     coverage = "About 160 countries.",
     caveats = "Scores Concept 11 (Trade governance).",
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