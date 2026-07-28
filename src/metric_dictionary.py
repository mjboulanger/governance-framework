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