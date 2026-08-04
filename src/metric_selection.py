"""metric_selection - Step-1 metric-level decisions.

One entry per metric. `at` lists the (concept_id, tier) placements; an empty `at`
means the metric is not scored and `why` records the reason. Direction: '+' higher
is better, '-' higher is worse. Contested or structural calls are written up in
framework_decisions.md; notes here are index-level only.

Session 2026-07-23. Sources reviewed: WGI, all 1-3 metric sources, FSI, CPJ,
POWELL_THYNE, WB_CARBON, IMF_AREAER_ERREGIME, CCP, IMF_IMAPP, IMF_SPI, IMF_AREAER.
Not yet reviewed: VDEM(66), FATF(102), WDI(31), DPI(28), IMF_FISCAL_RULES(24),
FH_FIW(18), UCDP(14), IDEA_PARTIP(12), WB_BRSS(11), YALE_EPI(11), NELDA(9),
RTI_RATING(9), WJP(8), ASCOR(pending coverage-table regen).
"""

D = [
 # ---- WGI: 3 scored, 3 reserved as category-level cross-checks ----
 dict(m="wgi_political_stability",      s="WGI", d="+", at=[(2,"P1")]),
 dict(m="wgi_government_effectiveness", s="WGI", d="+", at=[(4,"P1")]),
 dict(m="wgi_regulatory_quality",       s="WGI", d="+", at=[(6,"P1")]),
 dict(m="wgi_control_of_corruption",    s="WGI", d="",  at=[], why="category cross-check (Rule of Law roll-up); aggregator sharing sources with CPI"),
 dict(m="wgi_rule_of_law",              s="WGI", d="",  at=[], why="category cross-check (Rule of Law roll-up)"),
 dict(m="wgi_voice_accountability",     s="WGI", d="",  at=[], why="category cross-check (Accountability roll-up)"),

 # ---- single-metric sources ----
 dict(m="ti_cpi_score",                 s="TI_CPI",         d="+", at=[(18,"P1")]),
 dict(m="unodc_homicide_rate",          s="UNODC_HOMICIDE", d="-", at=[(16,"P1")]),
 dict(m="pei_electoral_integrity_index",s="PEI",            d="+", at=[(20,"P1")]),
 dict(m="nelda_concerns_not_free_fair", s="NELDA", d="-", at=[(20,"Sp")],
      note="NELDA11: pre-election concerns elections wont be free/fair (1=concern=BAD, d=-). Event-level (election years only, ~24.5pct of country-years), one obs per country-year. NELDA EXCLUDES ~21 consolidated democracies by design, so absence = established-democracy (implicitly clean), a coverage bias to note at scaling. Supplementary: C20 has 10 P1 metrics; NELDA triangulates. Raw 99 (unclear) -> NaN in pipeline"),
 dict(m="nelda_media_bias_incumbent", s="NELDA", d="-", at=[(20,"Sp")],
      note="NELDA16: media bias favoring incumbent (1=bias=BAD, d=-). Sharpest NELDA separator (clean 0.019 vs rigged 0.741). Same event-level/coverage caveats as nelda_concerns_not_free_fair"),
 dict(m="nelda_riots_protests_after", s="NELDA", d="-", at=[(20,"Sp")],
      note="NELDA: riots/protests after election with vote-fraud allegations (1=occurred=BAD, d=-). Same event-level/coverage caveats"),
 dict(m="nelda_violence_deaths_before", s="NELDA", d="-", at=[(20,"Sp")],
      note="NELDA33: significant violence w/ civilian deaths before/during election (1=occurred=BAD, d=-). Same event-level/coverage caveats"),
 dict(m="nelda_opposition_allowed", s="NELDA", d="+", at=[(20,"Sp")],
      note="NELDA: was opposition allowed (1=allowed=GOOD, d=+). Lower coverage (n=1130) as it is only coded where relevant. Same event-level/coverage caveats"),
 dict(m="nelda_mtop_low_signal", s="NELDA", d="", at=[],
      why="EXCLUDED: near-zero discrimination between clean democracies (1.000) and rigged autocracies (0.964) - carries almost no signal for electoral quality. Renamed from the misleading nelda_meaningful_opposition; kept in qog_clean.csv as documented-low-signal, not scored"),
 dict(m="nelda_election_held", s="NELDA", d="", at=[],
      why="EXCLUDED: election-TYPE descriptor (values 1-5), not a quality measure - type-not-quality principle. Same for nelda_executive_election / nelda_legislative_election"),
 dict(m="wdi_lpi_overall",              s="WB_LPI",         d="+", at=[(11,"P1")]),
 dict(m="tfi_avg",                      s="OECD_TFI",       d="+", at=[(11,"P1")]),
 dict(m="fraser_trade_freedom",         s="HERITAGE_TR",    d="+", at=[(11,"P1")], note="Fraser Area 4; supersedes Heritage Trade Freedom"),
 dict(m="fraser_regulation",            s="FRASER_REG",     d="+", at=[(6,"P2")]),
 dict(m="fraser_legal_system",          s="FRASER_LEGAL",   d="+", at=[(17,"P2")]),
 dict(m="wdi_hci_plus_overall",         s="WB_HCI",         d="+", at=[(5,"P2")]),
 dict(m="hanson_sigman_state_capacity", s="HANSON_SIGMAN",  d="", at=[],
      why="RECENCY FAIL: 0.0% current sovereign coverage (series ends 2015); named as a dead tail in metric_methodology S4"),
 dict(m="irena_renewables_share_pct",   s="IRENA_CAPACITY", d="+", at=[(12,"P1")]),
 dict(m="bci_corruption_index",         s="BCI",            d="-", at=[(18,"P2")], note="direction verified: Finland -3.5 low, Guinea-Bissau 78.9 high"),
 dict(m="gpi_peace_index",              s="GPI",            d="-", at=[(2,"P2"),(16,"P2")]),
 dict(m="obs_open_budget_index",        s="OBS",            d="+", at=[(8,"P1"),(25,"P2")]),
 dict(m="pefa_core_management",         s="PEFA",           d="+", at=[(8,"P1")],
      note="PEFA composite (folded into C8 with PFM). Mean of Pillar I (budget reliability, PI-01..03) and Pillar V (predictability/control in execution, PI-19..25) pillar-means - the frontline how-well-is-money-managed core. P1: central to PFM quality. CROSS-SECTIONAL, one 2016-framework assessment per country, vintage varies 2017-2026 (not a panel). 82 countries, donor-skewed developing-heavy coverage - reference-class caveat at scaling"),
 dict(m="pefa_accountability",          s="PEFA",           d="+", at=[(8,"P2")],
      note="PEFA composite. Mean of Pillar VI (accounting/reporting, PI-26..28) and Pillar VII (external scrutiny/audit, PI-29..31) pillar-means - the back-end books-and-audit accountability layer. P2 (below core management): more hygiene than frontline quality. VII/scrutiny OVERLAPS C19 legislative oversight - flagged for Step-4 correlation-aware weighting. Same cross-sectional/vintage-varies/coverage caveats as pefa_core_management"),
 dict(m="polfin_transparency_integrity",s="TI_POLFINANCE",  d="+", at=[(25,"P2")], note="master flags possible C18 cross-reference"),
 dict(m="pew_gov_restrictions_index",   s="PEW_GRI",        d="-", at=[(22,"P2")], note="direction verified: NZ 0.35 low, China 9.09 high"),
 dict(m="pew_social_hostilities_index", s="PEW_GRI",        d="-", at=[(22,"P2")]),
 dict(m="wbl_legal_framework",          s="WB_WBL",         d="+", at=[(22,"P2")]),
 dict(m="wbl_supportive_framework",     s="WB_WBL",         d="+", at=[(22,"P2")]),
 dict(m="wbl_enforcement_perceptions",  s="WB_WBL",         d="+", at=[(22,"P2")]),
 dict(m="romelli_cbi_index",            s="ROMELLI_CBI",    d="+", at=[(8,"P1")]),
 dict(m="romelli_cbi_lending",          s="ROMELLI_CBI",    d="",  at=[], why="decomposition of romelli_cbi_index"),
 dict(m="romelli_cbi_policy",           s="ROMELLI_CBI",    d="",  at=[], why="decomposition of romelli_cbi_index"),
 dict(m="climate_laws_cumulative",      s="CLIMATE_LAWS",   d="+", at=[(12,"P2")], note="DEMOTED P1->P2: volume not quality; unnormalized cumulative count"),
 dict(m="new_laws",                     s="CLIMATE_LAWS",   d="",  at=[], why="annual flow = first difference of stock; momentum is a separate coordinate"),
 dict(m="odin_openness",                s="ODIN",           d="+", at=[(3,"P1")], note="ODIN's distinctive leg per master; coverage leg overlaps SPI"),
 dict(m="odin_overall",                 s="ODIN",           d="+", at=[(25,"Sp")]),
 dict(m="odin_coverage",                s="ODIN",           d="",  at=[], why="redundant with SPI (both measure whether data exists)"),
 dict(m="civicus_score",                s="CIVICUS",        d="+", at=[(21,"P1"),(24,"P1")]),
 dict(m="idea_participation",           s="IDEA_GSOD", d="+", at=[(21,"P1")],
      note="IDEA GSoD Participation attribute (0-1, higher=more participatory). P1: direct on-concept measure of participation, and an INDEPENDENT full-history source (1990-2025, 174 countries) in a concept otherwise dominated by V-Dem (6 of 7 existing metrics are V-Dem: its composite v2x_partip plus 5 facets; CIVICUS covers only 2022+). Breaks the V-Dem monoculture across the whole panel. Validated: Denmark 0.96 / Switzerland 0.94 down to North Korea 0.03. GSoD composite chosen over its subcomponents - civil_society (r=0.98) and civic_engagement (r=0.83) are redundant with it"),
 dict(m="idea_local_democracy",         s="IDEA_GSOD", d="+", at=[(21,"P2")],
      note="IDEA GSoD Local Democracy subcomponent (0-1). P2: the sharpest democracy/autocracy discriminator in the GSoD participation cluster (gap 0.85 > composite 0.66) and only moderately correlated with the composite (r=0.744, so ~half its variance is independent) - captures subnational/local participation that the national-focused V-Dem cluster and the GSoD composite underweight. Mechanical overlap with idea_participation (its parent composite) flagged for Step-4 correlation-aware weighting"),
 dict(m="idea_civil_society",           s="IDEA_GSOD", d="", at=[],
      why="EXCLUDED: redundant with idea_participation (r=0.980, essentially the composite restated). Scoring it would double-count the composite"),
 dict(m="idea_civic_engagement",        s="IDEA_GSOD", d="", at=[],
      why="EXCLUDED: largely redundant with idea_participation (r=0.832)"),
 dict(m="idea_electoral_participation", s="IDEA_GSOD", d="", at=[],
      why="EXCLUDED: weak discriminator (clean 0.666 vs autocracy 0.453, gap 0.21) - electoral participation/turnout separates democracies from autocracies poorly (autocracies can drive high turnout via mobilisation/coercion). Also duplicates C20 electoral-process content"),
 dict(m="idea_direct_democracy",        s="IDEA_GSOD", d="", at=[],
      why="EXCLUDED: degenerate for scoring (mean 0.089 - most countries near zero, few have referenda/initiative mechanisms) and weak discriminator (gap 0.15). Measures presence of direct-democracy institutions, a narrow feature, not general participatory quality"),
 dict(m="civicus_rating",               s="CIVICUS",        d="",  at=[], why="ordinal coarsening of civicus_score"),
 dict(m="kaopen_norm",                  s="CHINN_ITO",      d="+", at=[(8,"Sp")], note="DEMOTED P1->Sp: same construct as FARI from same AREAER source data"),
 dict(m="kaopen",                       s="CHINN_ITO",      d="",  at=[], why="raw scale; kaopen_norm preferred (bounded)"),
 dict(m="polity5_score",                s="POLITY5",        d="",  at=[], why="RECENCY FAIL: series ends 2018 (165 ctry), 7 yrs stale vs 4-yr window"),
 dict(m="polity5_regime_durability",    s="POLITY5",        d="",  at=[], why="RECENCY FAIL: series ends 2018"),
 dict(m="kof_economic_globalisation",   s="KOF_TRADE",      d="",  at=[], why="source closed; C11 proxy abandoned"),
 dict(m="nd_gain_readiness",            s="ND_GAIN",        d="",  at=[], why="source dropped 2026-07-22 on construct validity (capacity not governance)"),
 dict(m="nd_gain_governance_readiness", s="ND_GAIN",        d="",  at=[], why="source dropped 2026-07-22; WGI-repackaged"),

 # ---- combined metrics (derived in scoring pipeline) ----
 dict(m="pts_index", s="PTS", d="-", at=[(16,"P1"),(22,"P2")], derive="mean of pts_amnesty, pts_hrw, pts_statedept where present",
      note="coverage 97.9% via State Dept (union of available coders, NOT min). No coder severity effect: common-sample means 3.135/3.167/3.073 (n=96); own-sample spread is coverage not severity"),
 dict(m="pts_amnesty",    s="PTS", d="", at=[], why="component of pts_index"),
 dict(m="pts_hrw",        s="PTS", d="", at=[], why="component of pts_index"),
 dict(m="pts_statedept",  s="PTS", d="", at=[], why="component of pts_index"),
 dict(m="wb_informal_economy", s="WB_INFORMAL", d="", at=[],
      why="RECENCY FAIL: both dge and mimic at 0.0% current sovereign coverage (series ends 2020); named as a dead tail in metric_methodology S4"),
 dict(m="wb_informal_economy_dge",   s="WB_INFORMAL", d="", at=[], why="component of wb_informal_economy"),
 dict(m="wb_informal_economy_mimic", s="WB_INFORMAL", d="", at=[], why="component of wb_informal_economy"),

 # ---- FSI ----
 dict(m="fsi_c1_security_apparatus",   s="FSI", d="-", at=[(13,"P1")]),
 dict(m="fsi_c2_factionalized_elites", s="FSI", d="-", at=[(1,"P1")], note="C1 takes two FSI components - source concentration"),
 dict(m="dpi_total_fragmentation", s="DPI", d="", at=[],
      why="EXCLUDED from C1 on validity, not data quality (2026-07-24). The DPI pipeline is CORRECT (pure rename of raw DPI columns, no transform bug) and the data is REAL - dpi_total_fragmentation follows DPI Frac exactly (prob two random deputies differ in party; Barbados one-party legislature = 0.0 confirms the definition). But DPI Frac is an INVALID proxy for C1 horizontal-elite-organisation: it measures seat-dispersion across party LABELS, which conflates genuine pluralism with managed-autocracy pseudo-pluralism. Belarus reads 0.994 (regime permits many toothless nominal parties) - same as a real multiparty democracy - so the measure cannot distinguish democratic fragmentation from authoritarian pseudo-fragmentation, i.e. it is confounded by the very regime type C1 assesses. Related DPI fragmentation cols (govfrac, oppfrac, herfindahls, polariz) share the confound. C1 keeps FSI Factionalized Elites (P1) - expert-coded ACTUAL elite fragmentation with no regime-type confound. NOTE: raw DPI numgov appears to be government SEATS not party count (~85pct confidence: Barbados 30 = House size; not codebook-verified). DPI data/pipeline are fine and remain available for other concepts if a non-confounded variable fits."),
 dict(m="fsi_c3_group_grievance",      s="FSI", d="-", at=[(1,"P1")]),
 dict(m="fsi_p2_public_services",      s="FSI", d="-", at=[(5,"P1")]),

 # ---- IMF SPI / iMaPP ----
 dict(m="spi_overall",        s="IMF_SPI",   d="+", at=[(3,"P1")]),
 dict(m="spi_pillar1_data_use",           s="IMF_SPI", d="", at=[], why="decomposition of spi_overall"),
 dict(m="spi_pillar2_data_services",      s="IMF_SPI", d="", at=[], why="decomposition of spi_overall"),
 dict(m="spi_pillar3_data_products",      s="IMF_SPI", d="", at=[], why="decomposition of spi_overall"),
 dict(m="spi_pillar4_data_sources",       s="IMF_SPI", d="", at=[], why="decomposition of spi_overall"),
 dict(m="spi_pillar5_data_infrastructure",s="IMF_SPI", d="", at=[], why="decomposition of spi_overall"),
 dict(m="imapp_breadth_total", s="IMF_IMAPP", d="+", at=[(8,"P1")],
      note="cumulative-ever ratchet: breadth not quality (docs: Pakistan 15/16). Diluted - C8 is well populated"),
 dict(m="imapp_breadth_borrower_based",      s="IMF_IMAPP", d="", at=[], why="decomposition of imapp_breadth_total"),
 dict(m="imapp_breadth_capital_based",       s="IMF_IMAPP", d="", at=[], why="decomposition of imapp_breadth_total"),
 dict(m="imapp_breadth_liquidity_funding",   s="IMF_IMAPP", d="", at=[], why="decomposition of imapp_breadth_total"),
 dict(m="imapp_breadth_provision_reserve_tax",s="IMF_IMAPP",d="", at=[], why="decomposition of imapp_breadth_total"),

 # ---- AREAER FARI: inflow at full weight, deliberate partial double-count ----
 dict(m="fari_aggregate",     s="IMF_AREAER", d="-", at=[(8,"P1")], note="higher = more restrictive; direction is a D3 item (policy stance vs quality)"),
 dict(m="fari_fdi_aggregate", s="IMF_AREAER", d="-", at=[(8,"P1")]),
 dict(m="fari_fdi_inflow",    s="IMF_AREAER", d="-", at=[(8,"P1")],
      note="DELIBERATE partial double-count with fdi_aggregate - user decision to tilt toward inbound access"),
 dict(m="fari_inflow",     s="IMF_AREAER", d="", at=[], why="split; aggregates are the doc-mandated scored fields"),
 dict(m="fari_outflow",    s="IMF_AREAER", d="", at=[], why="split; outbound less material to sovereign investor"),
 dict(m="fari_fdi_outflow",s="IMF_AREAER", d="", at=[], why="split; outbound less material to sovereign investor"),

 # ---- AREAER de-facto ER: regime TYPE is not a quality ordering ----
 dict(m="areaer_regime_ordinal", s="IMF_AREAER_ERREGIME", d="", at=[], why="regime type is a policy choice not a quality ordering (HK peg vs ARG crawl); ordinal 8 is a residual"),
 dict(m="areaer_arrangement",    s="IMF_AREAER_ERREGIME", d="", at=[], why="categorical label; see areaer_regime_ordinal"),
 dict(m="areaer_regime_group",   s="IMF_AREAER_ERREGIME", d="", at=[], why="regime type not quality"),
 dict(m="areaer_mpf",            s="IMF_AREAER_ERREGIME", d="", at=[], why="PENDING: derive inflation-targeting binary; IT is defensibly better governance where regime type is not"),

 # ---- CCP: 96 is a MISSING sentinel, not data ----
 dict(m="ccp_civil_rights_provisions", s="CCP", d="+", at=[(14,"P1")], note="BLOCKED: recode 96 -> NaN first (23 countries)"),
 dict(m="ccp_information_access",      s="CCP", d="+", at=[(14,"P1")], note="BLOCKED: recode 96 -> NaN first (6 countries)"),
 dict(m="ccp_equality_provisions",     s="CCP", d="",  at=[], why="no variance: 176/4 split"),
 dict(m="ccp_government_system",       s="CCP", d="",  at=[], why="no variance: 188/4 split. C19 loses its only non-VDEM source"),
 dict(m="ccp_market_economy_provisions",s="CCP",d="",  at=[], why="81/19 binary, de jure constitutional text; too weak as a 2nd indicator for C10"),

 # ---- CPJ: global census, so absence is verified zero. Zero-fill to spine ----
 dict(m="cpj_imprisoned",       s="CPJ", d="-", at=[(23,"P1")],
      note="zero-fill to spine; log1p (zero-inflated). Raw count, no denominator - per-capita inverts ranking (China 0.04/m vs Eritrea 4.3/m)"),
 dict(m="cpj_murders_unsolved", s="CPJ", d="-", at=[(23,"P2")], note="impunity signal; zero-fill to spine"),
 dict(m="cpj_murdered_confirmed",s="CPJ",d="",  at=[], why="conflict-contaminated (Israel/OPT 32 of 99 total); duplicated by unsolved"),
 dict(m="cpj_murdered_total",   s="CPJ", d="",  at=[], why="superseded by cpj_murdered_confirmed"),

 # ---- Powell-Thyne: rare events, needs a trailing window ----
 dict(m="pt_coup_successful", s="POWELL_THYNE", d="-", at=[(2,"P1"),(1,"Sp")],
      derive="10-year trailing window count", note="window length is a Step-4 parameter; 27 successful coups in last 5 yrs"),
 dict(m="pt_coup_failed",     s="POWELL_THYNE", d="-", at=[(2,"P1")], derive="10-year trailing window count"),
 dict(m="pt_coup_alleged",    s="POWELL_THYNE", d="",  at=[], why="weaker evidence than realised events"),
 dict(m="pt_autocoup",        s="POWELL_THYNE", d="",  at=[], why="too rare to discriminate"),

 # ---- WB Carbon: absence INFERRED not verified; zero-fill with caveat ----
 dict(m="wb_carbon_pricing_exists", s="WB_CARBON", d="+", at=[(12,"P1")],
      note="zero-fill to spine; absence is INFERRED non-existence (docs) - out-of-scope/subnational instruments possible"),
 dict(m="wb_carbon_price_usd",      s="WB_CARBON", d="+", at=[(12,"P1")], note="zero-fill to spine"),
 dict(m="wb_carbon_coverage_pct",   s="WB_CARBON", d="+", at=[(12,"P2")], note="already a percentage; no denominator needed"),
 dict(m="wb_carbon_revenue_pct_gdp",s="WB_CARBON", d="+", at=[(12,"P2")],
      derive="revenue_usd_m * 1e6 / (wdi_gdp_per_capita_usd * wdi_population_total)",
      note="denominator is CURRENT US$ (NY.GDP.PCAP.CD) - nominal over nominal"),
 dict(m="wb_carbon_revenue_usd_m",  s="WB_CARBON", d="", at=[], why="component of wb_carbon_revenue_pct_gdp"),
]

# Actions required before the affected metrics can be scored.
PENDING = [
 "CCP: recode sentinel 96 -> NaN in 14_qog_pipeline (blocks both C14 metrics)",
 "AREAER: derive inflation-targeting binary from areaer_mpf",
 "CPJ: zero-fill to spine; verify Israel/OPT combined row vs spine ISO3 split",
 "POWELL_THYNE: build 10-yr trailing window counts",
 "WB_CARBON: zero-fill to spine; derive revenue_pct_gdp",
 "C19 Legislative and constitutional checks: now VDEM-ONLY (Polity recency + CCP no-variance) - measurement gap",
 "FATF: 102 metrics need collapsing to constructs before C9 review",
 "PEFA: long format, needs pivot before C7 review",
 "metric_coverage.csv: regenerate to include ascor_clean.csv",
]

def to_rows():
    rows = []
    for e in D:
        base = dict(metric=e["m"], source_id=e["s"], direction=e.get("d", ""),
                    derive=e.get("derive", ""), note=e.get("note", ""))
        if e["at"]:
            for cid, tier in e["at"]:
                rows.append(dict(base, concept_id=cid, tier=tier, include=True, exclude_reason=""))
        else:
            rows.append(dict(base, concept_id="", tier="", include=False,
                             exclude_reason=e.get("why", "")))
    return rows
# =====================================================================
# V-Dem block (66 variables). Appended 2026-07-23.
# DIRECTION VERIFIED EMPIRICALLY vs the WGI 6-dimension composite (n=176,
# latest year): 65 of 66 correlate POSITIVELY (+0.338 to +0.871). Only the
# constructed index v2x_corr is reverse-coded (-0.880).
# IMPORTANT: V-Dem's individual corruption ITEMS are coded higher = LESS
# corrupt (v2excrptps +0.871, v2jucorrdc +0.843, v2exembez +0.821,
# v2lgcrrpt +0.772) - OPPOSITE to the v2x_corr index. Asserting these signs
# from the codebook would have inverted four of C18's five V-Dem metrics.
# Concept placements are doc-anchored: every one is named in the master's
# per-concept source tables.
# =====================================================================
_VDEM = {
 1:  ["v2pepwrses", "v2pepwrsoc", "v2x_egal", "v2psoppaut"],
 4:  ["v2clrspct"],
 10: ["v2clstown"],
 13: ["v2svstterr", "v2svdomaut"],
 14: ["v2cltrnslw", "v2clacjstm", "v2clacjstw", "v2xeg_eqaccess"],
 15: ["v2juhcind", "v2juncind", "v2jucomp", "v2jupack", "v2jupurge"],
 16: ["v2cltort", "v2clkill", "v2clrgunev"],
 17: ["v2xcl_prpty"],  # collapsed 3->1 (2026-07-24, within-source collapse); dropped v2clprptym/v2clprptyw as excluded entries below
 18: ["v2x_corr", "v2excrptps", "v2exembez", "v2lgcrrpt", "v2jucorrdc"],
 19: ["v2xlg_legcon", "v2lgoppart", "v2lgqstexp", "v2lginvstp", "v2lgotovst"],
 20: ["v2x_polyarchy", "v2elfrfair", "v2elirreg", "v2elintim", "v2elvotbuy",
      "v2elaccept", "v2elembaut", "v2elembcap"],
 21: ["v2x_partip", "v2psprlnks", "v2pscohesv", "v2cseeorgs", "v2dlconslt", "v2csreprss"],
 22: ["v2x_civlib", "v2x_clpriv", "v2clrelig", "v2cldmovem", "v2cldmovew",
      "v2clsocgrp", "v2clslavef"],
 23: ["v2x_freexp_altinf", "v2mecenefm", "v2mecorrpt", "v2merange", "v2mebias"],  # collapsed 8->5 (2026-07-24, within-source collapse rule); dropped v2meharjrn/v2meslfcen/v2mecrit as excluded entries below
 24: ["v2cseeorgs", "v2csreprss", "v2cscnsult", "v2csprtcpt"],
 25: ["v2cltrnslw", "v2dlconslt"],
}

_VNOTE = {
 "v2x_corr":   "REVERSE-CODED (r=-0.880 vs WGI). V-Dem's individual corruption items run the OTHER way - do not infer sign from the family",
 "v2clstown":  "direction evidence-resolved 2026-07-21: monotonic/linear, no threshold",
 "v2elembaut": "EMB autonomy - closes the C20 EMB leg; supersedes IDEA EMB Database",
 "v2elembcap": "EMB capacity - closes the C20 EMB leg; supersedes IDEA EMB Database",
 "v2cldmovew": "master names the pair as 'v2cldmovem/w'",
 "v2pscohesv": "weakest V-Dem signal vs WGI (r=+0.338)",
}

_vplace = {}
for _cid, _vs in _VDEM.items():
    for _v in _vs:
        _vplace.setdefault(_v, []).append((_cid, "P1"))

D += [dict(m=_v, s="VDEM", d=("-" if _v == "v2x_corr" else "+"),
           at=_ats, note=_VNOTE.get(_v, ""))
      for _v, _ats in _vplace.items()]

D += [
 dict(m="vdem_regime_duration", s="VDEM", d="+", at=[(2, "P1")],
      derive="years since v2x_regime last changed, computed from the panel",
      note="master specifies regime DURATION via V-Dem's own classification; raw type is not a quality ordering"),
 dict(m="v2x_regime", s="VDEM", d="", at=[],
      why="regime TYPE is a classification not a quality ordering; input to vdem_regime_duration"),
 dict(m="v2x_horacc", s="VDEM", d="", at=[],
      why="aggregate of components already scored (r=+0.976 with v2xlg_legcon, +0.86 with judicial family) and spans C19/C15 which the framework deliberately separated; category cross-check for Accountability (horizontal)"),
 dict(m="v2meharjrn", s="VDEM", d="", at=[],
      why="COLLAPSED out of C23 Media freedom (2026-07-24, within-source metric collapse rule, methodology S6). Harassment of journalists. Gate 1: r>0.85 with composite v2x_freexp_altinf and siblings. Gate 2 FAILED: top divergences from the composite are clean-end scale/ceiling noise (Denmark, Switzerland score higher on the component than the composite - both agree 'very free'), no material distinction. C23 keeps composite + v2mecorrpt/v2merange/v2mecenefm/v2mebias, each retained for distinct decision-relevant signal"),
 dict(m="v2meslfcen", s="VDEM", d="", at=[],
      why="COLLAPSED out of C23 Media freedom (2026-07-24, within-source collapse rule). Media self-censorship. Gate 1: r>0.85 with composite. Gate 2 FAILED: divergences small and top-end scale wobble (Switzerland etc.), no interpretable distinction the composite blends away"),
 dict(m="v2mecrit", s="VDEM", d="", at=[],
      why="COLLAPSED out of C23 Media freedom (2026-07-24, within-source collapse rule). Print/broadcast critical of government. Gate 1: r>0.85 with composite. Gate 2 FAILED: divergences are clean-end scale noise (Germany etc.), no distinct signal"),
 dict(m="v2clprptym", s="VDEM", d="", at=[],
      why="COLLAPSED out of C17 Property rights (2026-07-24, within-source collapse rule, methodology S6). Property rights for men. Gate 1: r=0.942 with composite v2xcl_prpty. Gate 2 FAILED for C17's purpose: divergences from the composite are extreme-low-tail wobble (Afghanistan, North Korea, Somalia - both already 'near-absent'), not decision-relevant distinctions for investor-facing property/expropriation risk. Option (c) chosen: collapse the V-Dem cluster to the composite; the gendered men/women disaggregation is a civil-liberties/gender dimension that belongs in C22 (which already carries WB Women Business and the Law), not in C17's contract-enforcement/expropriation scope. C17 stays adequately measured (composite + WJP no-expropriation + Fraser legal, 3 independent sources)"),
 dict(m="v2clprptyw", s="VDEM", d="", at=[],
      why="COLLAPSED out of C17 Property rights (2026-07-24, within-source collapse rule). Property rights for women. Gate 1: r=0.935 with composite. Its divergences ARE somewhat interpretable (Jordan/Cuba - women's property rights lagging the general environment via discriminatory inheritance/marital law), i.e. a real gender-gap signal - but that signal belongs to C22 (Civil liberties / gender), not C17's investor-facing property-rights-and-contract-enforcement scope. Collapsed to keep C17 focused on the general expropriation/enforcement environment (composite). If the property-rights gender gap is wanted, it should be added to C22, not retained here"),
]

PENDING += [
 "VDEM: derive vdem_regime_duration (years since v2x_regime change) for C2",
 "MASTER: C22 row lists phantom 'v2clpriv' alongside real 'v2x_clpriv' - remove",
]



PENDING += [
 "COVERAGE RULE: derived metrics inherit UNION coverage when mean-of-available, MIN when product/ratio",
 "SCOUT: QoG Expert Survey (C4) - coverage ~70% clears the locked 60% bar; open question is recency (wave-based, latest round year unknown)",
 "SCOUT: ILO social security (C13) - audit marks unexamined; C13 now down to 3 metrics from 2 sources",
]


# =====================================================================
# WJP block (8 factors). Appended 2026-07-23.
# DIRECTION VERIFIED vs the WGI 6-dim composite (n=143, latest yr 2025):
# all 8 positive, r = +0.803 to +0.930 - the strongest-correlating block so far.
# COVERAGE: 142 of 192 sovereigns (74%). Clears the locked 60% bar, and
# metric_methodology S4 names "WJP factors 74.0%" as a confirmed rescue. But it
# is the thinnest major source in the framework and its exclusions are NOT random
# (small states and closed regimes under-represented) - reference-class caveat
# applies wherever WJP carries significant concept weight.
# All placements doc-anchored except the C4 call, which the master explicitly
# deferred here ("Borderline - keep for metric pass ... need to disambiguate").
# =====================================================================
_WJP = {
 "wjp_f2_absence_corruption":     [(18, "P1")],
 "wjp_f3_open_government":        [(14, "P1"), (25, "P1")],
 "wjp_f4_fundamental_rights":     [(14, "P1")],
 "wjp_f5_order_security":         [(16, "P1"), (2, "P2")],
 "wjp_f6_regulatory_enforcement": [(6, "P1"), (4, "P2")],
 "wjp_f6_5_no_expropriation":     [(17, "P1")],
 "wjp_f7_civil_justice":          [(15, "P1")],
 "wjp_f8_criminal_justice":       [(15, "P1")],
}

_WNOTE = {
 "wjp_f6_regulatory_enforcement":
   "C4 disambiguation resolved: P1 in C6 (tightest construct fit - the factor IS regulatory enforcement), "
   "P2 in C4 (sub-factors 6.3/6.4 cover administrative-procedure quality). Follows the established WJP "
   "pattern (F5 = P1 C16 / P2 C2; F3 = P1 both C14 and C25). Only the aggregate is extracted, so a clean "
   "6.1-6.4 split is not available",
 "wjp_f6_5_no_expropriation":
   "sub-component pulled specifically for C17; full Factor 6 stays in C6",
 "wjp_f3_open_government":
   "P1 in both C14 and C25 per master; repetition tracked under principle 5",
}

D += [dict(m=_k, s="WJP", d="+", at=_v, note=_WNOTE.get(_k, ""))
      for _k, _v in _WJP.items()]

PENDING += [
 "WJP reference-class: 74% sovereign coverage, non-random exclusions (small states, closed regimes) - "
 "record as a known limitation for C6/C14/C15/C16/C17/C18/C25",
]


# =====================================================================
# WDI block (31 metrics). Appended 2026-07-23.
# C5 uses FOUR SUB-COMPOSITES, not 22 raw metrics. WDI subsumes four of C5's
# nominal sources (WHO GHO, UNESCO UIS, UNDP HDI sub-indicators, plus WDI's own
# sector series), so raw equal-weighting would give HEALTH 9 of 22 slots = 41% of
# the concept - a weight determined by how many series the World Bank happens to
# publish, not by importance. Same failure the ASCOR area-level roll-up fixed.
# Each sub-composite = mean of its z-normalized, direction-aligned components,
# under the S7 two-level missingness penalty (f>=0.5 no penalty; 0<f<0.5 sliding;
# f=0 null).
# ENDOGENEITY TAG: AMBIGUOUS -> capped partial penalty. WDI service-delivery gaps
# are mixed - a large state not reporting hospital beds is a capacity signal, but
# a microstate absent from a household-survey series simply was not surveyed.
# =====================================================================
_WDI_HEALTH = ["wdi_immunization_dpt", "wdi_immunization_measles", "wdi_life_expectancy",
               "wdi_uhc_coverage_index", "wdi_hospital_beds_per_1000", "wdi_nurses_per_1000",
               "wdi_physicians_per_1000", "wdi_maternal_mortality", "wdi_mortality_under5"]
_WDI_EDU   = ["wdi_primary_completion_rate", "wdi_primary_enrollment_gross",
              "wdi_secondary_enrollment_gross", "wdi_pupil_teacher_ratio_secondary"]
_WDI_INFRA = ["wdi_basic_water_access", "wdi_basic_sanitation_access", "wdi_electricity_access"]
_WDI_SOCP  = ["wdi_safety_net_coverage", "wdi_social_insurance_coverage",
              "wdi_social_protection_coverage"]
# components entering NEGATIVE (higher = worse), flipped before averaging
_WDI_NEG = {"wdi_maternal_mortality", "wdi_mortality_under5", "wdi_pupil_teacher_ratio_secondary"}

D += [
 dict(m="wdi_health_index", s="WDI", d="+", at=[(5, "P1")],
      derive="mean of z-normalized " + ", ".join(_WDI_HEALTH) +
             " (maternal_mortality and mortality_under5 sign-flipped)",
      note="9 components; equal-weighting these raw would give health 41% of C5"),
 dict(m="wdi_education_index", s="WDI", d="+", at=[(5, "P1")],
      derive="mean of z-normalized " + ", ".join(_WDI_EDU) +
             " (pupil_teacher_ratio_secondary sign-flipped)",
      note="pupil_teacher_ratio_PRIMARY excluded separately: 0.0% current coverage"),
 dict(m="wdi_infrastructure_index", s="WDI", d="+", at=[(5, "P1")],
      derive="mean of z-normalized " + ", ".join(_WDI_INFRA),
      note="ceiling-piled at ~100%; S5 keeps these on z-score, NOT percentile - the pile is informative and z preserves distance-from-universal"),
 dict(m="wdi_social_protection_index", s="WDI", d="+", at=[(5, "P1")],
      derive="mean of z-normalized " + ", ".join(_WDI_SOCP),
      note="thinnest sub-composite: components at 61-68% coverage, all irregular cadence"),

 # ---- C11 trade ----
 dict(m="wdi_tariff_rate_simple_mean", s="WDI", d="-", at=[(11, "P1")],
      note="higher tariffs = less open; direction is a D3 item (policy stance vs governance quality, same question as FARI). 84.9% coverage"),
 dict(m="wdi_tariff_rate_weighted_mean", s="WDI", d="", at=[],
      why="same construct as simple mean; trade-weighting is endogenous to trade patterns (prohibitive tariffs suppress the trade that would weight them)"),

 # ---- C17 property / IP ----
 dict(m="wdi_ip_nonresident_per_gdp", s="WB_WDI", d="", at=[], why="DROPPED v1 2026-07-24: per-GDP ratio pathological at small economies (Sao Tome ~6720, ~100x real innovation hubs - small IP count over tiny GDP explodes, measuring economy size not IP-regime quality). C17 well-carried without it (V-Dem x3 + Heritage + Fraser + WJP 6.5). Non-resident-share-of-total-filings is the correct construction if an IP signal is wanted in v2"),
 dict(m="wdi_patent_applications_resident", s="WDI", d="", at=[],
      why="measures domestic innovation activity, not IP protection quality; also 57.8% coverage, below the 60% bar"),
 dict(m="wdi_trademark_applications_resident", s="WDI", d="", at=[],
      why="measures domestic innovation activity, not IP protection quality"),

 # ---- excluded: inputs, income context, dead tail ----
 dict(m="wdi_education_expenditure_gdp", s="WDI", d="", at=[],
      why="INPUT not outcome - C5's scope is explicitly 'what citizens receive from the state'. High spending with poor outcomes is what weak service delivery looks like. Reaches C5 only via the master's UNESCO subsumption, which contradicts the concept's own scope"),
 dict(m="wdi_education_expenditure_govt", s="WDI", d="", at=[],
      why="INPUT not outcome - see wdi_education_expenditure_gdp"),
 dict(m="wdi_gni_per_capita_ppp", s="WDI", d="", at=[],
      why="income measure, not governance. Named in the master under the UNDP HDI subsumption but fails construct validity outright; also PPP, against the USD-only standing rule"),
 dict(m="wdi_gdp_per_capita_usd", s="WDI", d="", at=[],
      why="income context; spine registers role=context, in_scoring=False. Used as a denominator and for the wealth-adjustment layer, never scored"),
 dict(m="wdi_gdp_per_capita_ppp", s="WDI", d="", at=[],
      why="income context, and PPP - against the USD-only standing rule"),
 dict(m="wdi_pupil_teacher_ratio_primary", s="WDI", d="", at=[],
      why="RECENCY FAIL: 0.0% current sovereign coverage (dead tail ending 2017); named in metric_methodology S4. The SECONDARY series survives at 94.3%"),
 dict(m="wdi_population_total", s="WDI", d="", at=[],
      why="identifier/denominator, not a governance metric"),
]

# health/education/infra/socprot components: excluded individually, they enter via the sub-composites
D += [dict(m=_c, s="WDI", d=("-" if _c in _WDI_NEG else "+"), at=[],
           why="component of a C5 sub-composite")
      for _c in (_WDI_HEALTH + _WDI_EDU + _WDI_INFRA + _WDI_SOCP)]

PENDING += [
 "BUILD: four C5 sub-composites (health, education, infrastructure, social protection) with the S7 sliding penalty, ambiguous-endogeneity cap",
 "BUILD: wdi_ip_nonresident_per_gdp (GDP-normalized nonresident patent + trademark filings)",
 "S7: set the ambiguous-regime penalty CAP (WDI service delivery is the first tagged case)",
]


# =====================================================================
# EPI + ASCOR block. Appended 2026-07-23.
# EPI: score the ISSUE-CATEGORY level only. Parent levels (epi_epi, epi_eco,
# epi_hlt) are excluded because scoring a parent OUTSOURCES THE SUB-DIMENSION
# WEIGHTING TO YALE (epi_eco is a weighted sum: BDH 25%, Forests 5%, Fisheries 2%)
# - the framework's method is to equal-weight sub-dimensions itself, as with the
# ASCOR area roll-up and the WDI sub-composites. Nesting confirmed empirically
# (epi_epi vs epi_eco r=+0.810; epi_eco vs epi_bdh r=+0.899).
# WEALTH-ADJUSTMENT AUDIT ENTRY #2 (after ASCOR): every EPI sub-index correlates
# with log GDP/capita at least as strongly as with the WGI composite
# (wrs +0.843 vs +0.716; hlt +0.831 vs +0.799). Yale states outright that wealth
# strongly predicts EPI performance. NOT an exclusion basis - wealth-correlation is
# expressly not an exclusion criterion - but flagged for the adjustment layer.
# =====================================================================
D += [
 dict(m="epi_agr", s="YALE_EPI", d="+", at=[(12, "P1")],
      note="Agriculture issue category - sustainable nitrogen management etc. 180 countries, biennial"),
 dict(m="epi_wrs", s="YALE_EPI", d="+", at=[(12, "P1")],
      note="Water Resources issue category (wastewater treatment). PLACEMENT FLAG: capital-infrastructure content, arguably closer to C5 service delivery than C12 environmental governance - revisit at Step 4"),
 dict(m="epi_bdh", s="YALE_EPI", d="+", at=[(12, "P2")],
      note="Biodiversity & Habitat. P2 not P1 on INTERNAL COMPARABILITY: its marine components are absent for ~27% of countries (mkp 48, mpe 49, mhp 36 of 180 NaN), so Yale renormalizes BDH over a terrestrial-only question set for landlocked countries and a fuller set for coastal ones - the ASCOR non-comparability pattern occurring inside one metric"),
 dict(m="epi_cch", s="YALE_EPI", d="+", at=[(12, "P2")],
      note="Climate Change issue category. INCLUDED despite overlapping ASCOR EP.1: different provider, different method (Yale scores continuous emissions-reduction rates and net-zero proximity; ASCOR asks 3 binaries) - triangulation under the repetition rule. CAVEAT: error is CORRELATED not independent - both measure emissions trajectory, confounded by industrial structure, growth rate and energy endowment. Two sources give more precision on a partly-confounded quantity, they do not neutralise the confound"),

 dict(m="epi_epi", s="YALE_EPI", d="", at=[],
      why="headline composite - master says 'use sub-components selectively, not headline composite'. Scoring it adopts Yale's cross-objective weighting, and it contains epi_hlt (sanitation, drinking water) which is already in wdi_infrastructure_index for C5 - cross-concept leakage"),
 dict(m="epi_eco", s="YALE_EPI", d="", at=[],
      why="policy-objective parent of bdh/agr/fsh/wrs (r=+0.899 with bdh). Scoring it outsources sub-dimension weighting to Yale and compounds opaquely with the children"),
 dict(m="epi_hlt", s="YALE_EPI", d="", at=[],
      why="policy-objective parent; its content (air quality, sanitation, drinking water, heavy metals, waste) is development/service-delivery outcome and duplicates wdi_infrastructure_index in C5"),
 dict(m="epi_fsh", s="YALE_EPI", d="", at=[],
      why="fish stock status inside an EEZ is shaped by distant-water fleets, regional fisheries bodies and ocean conditions - substantially outside national control; measures a shared resource's condition more than one state's governance. Also 39 of 180 structurally absent (landlocked) and scores INVERSELY to governance and wealth (r -0.148 WGI, -0.302 logGDP), so skipping it would advantage landlocked states"),
 dict(m="epi_mkp", s="YALE_EPI", d="", at=[],
      why="one of BDH's twelve components; only 3 of the 12 were extracted so BDH cannot be rebuilt independently, and scoring these alongside epi_bdh double-counts. Coverage was NOT the disqualifier (68% of sovereigns, above the bar)"),
 dict(m="epi_mhp", s="YALE_EPI", d="", at=[], why="BDH component - see epi_mkp"),
 dict(m="epi_mpe", s="YALE_EPI", d="", at=[], why="BDH component (Marine Protection Stringency) - see epi_mkp"),
 dict(m="country_code_epi", s="YALE_EPI", d="", at=[], why="numeric UN country code - identifier, not a metric"),

 # ---- ASCOR: spec was committed 2026-07-22 but the metric row was never written ----
 dict(m="ascor_climate_governance", s="ASCOR", d="+", at=[(12, "P2")],
      note="TIER P2 CONFIRMED at Step 1 (was provisional): 85 countries = 44% of the sovereign core, below the 60% bar, so flagged-not-dropped per S4 - retained because it is the only investor-oriented sovereign climate-governance assessment and covers the major EMs. Fixed 0-1 anchor, S5 fixed-anchor family, passed through UNNORMALIZED. Momentum available for only 25 of 85. Full spec: framework_decisions.md 'ASCOR composite specification'"),
 dict(m="ascor_full_diagnostic", s="ASCOR", d="", at=[],
      why="9-area version retained in the evidentiary layer only - includes the income-conditional areas that make cross-income comparison invalid (see ASCOR spec)"),
]

PENDING += [
 "C12 BALANCE: 8 of 11 metrics are climate/energy vs 3 non-climate environmental. Nothing measures the concept's stated core (ministry capacity, EIA processes, enforcement, regulatory capture) - the master already concedes this as a real measurement gap. Address via tier/measurement-quality weighting at Step 4, not by dropping valid sources",
 "WEALTH-ADJUSTMENT AUDIT: entry #2 = Yale EPI (all sub-indices track log GDP at least as strongly as WGI; Yale states wealth strongly predicts performance)",
 "EPI REFRESH: 2026 edition is out (177 countries, 47 indicators, 12 issue categories) vs our 2024 (180/58/11) - another methodology break, reinforcing the limited-comparability note",
]


# =====================================================================
# FH-FIW block (18 columns -> 4 scored totals). Appended 2026-07-23.
# Freedom House Freedom in the World: annual expert-coded political-rights and
# civil-liberties assessment, ~210 countries, near-universal (195 here at 99.5%).
# SCORE THE 4 SUB-CATEGORY TOTALS, not the 16 numbered indicators: each total IS
# the equal-weighted sum of its 0-4 indicators (fh_d_expression_belief = d1+d2+d3+d4,
# range 0-16), so scoring both double-counts. FH weights indicators equally within a
# sub-category, so the total already equals the equal-weight composite the framework
# would otherwise build, and keeps the cross-concept placement clean (sub-category D
# lands in both C22 and C23 at different tiers). Bounded 0-12/0-16 scales -> S5
# fixed-anchor candidate. All positive direction.
# SOURCE CAVEAT: FH is majority US-government-funded and has a documented
# US-foreign-policy-alignment critique - handled structurally (one source among
# several per concept, never alone), worth stating in output.
# =====================================================================
D += [
 dict(m="fh_a_electoral_process", s="FH_FIW", d="+", at=[(20, "P1")],
      note="sub-category A: free/fair elections, honest administration, electoral laws"),
 dict(m="fh_e_associational_rights", s="FH_FIW", d="+", at=[(24, "P1")],
      note="sub-category E: assembly, civic/NGO freedom, trade unions"),
 dict(m="fh_g_personal_autonomy", s="FH_FIW", d="+", at=[(22, "P1")],
      note="sub-category G: movement, property, personal social freedoms, equality of opportunity - fills C22's residual-autonomy scope with an independent method"),
 dict(m="fh_d_expression_belief", s="FH_FIW", d="+", at=[(23, "P2"), (22, "P2")],
      note="sub-category D: media, religious, academic freedom + private discussion. P2 in C23 Media freedom (behind V-Dem media + CPJ). P2 (not P1) in C22 Civil liberties deliberately: C22 already holds 7 V-Dem CL metrics + Pew religious-freedom, so D's content largely overlaps - triangulation without diluting the core, which a P1 placement into an already-13-metric concept would do"),
]

# 16 numbered indicators: excluded, they sum into the 4 totals
_FH_IND = {
 "fh_a1":"A electoral: free/fair executive elections", "fh_a2":"A: free/fair legislative elections",
 "fh_a3":"A: fair electoral laws and framework",
 "fh_d1":"D: free and independent media", "fh_d2":"D: religious freedom",
 "fh_d3":"D: academic freedom", "fh_d4":"D: free private discussion",
 "fh_e1":"E: freedom of assembly", "fh_e2":"E: freedom for civic/NGO groups", "fh_e3":"E: free trade unions",
 "fh_g1":"G: freedom of movement", "fh_g2":"G: property rights", "fh_g3":"G: personal social freedoms",
 "fh_g4":"G: equality of opportunity",
}
D += [dict(m=_k, s="FH_FIW", d="+", at=[],
           why="component of a FH sub-category total (" + _v.split(':')[0] + ") - scored via the total")
      for _k, _v in _FH_IND.items()]

PENDING += [
 "C22 Civil liberties now 15 metrics (8 P1 / 7 P2) - most-measured concept in the framework; the P1/P2 split is what keeps FH-D and the WBL/Pew P2 metrics from diluting the V-Dem+FH-G core. Watch at Step 4",
]


# =====================================================================
# UCDP block (13 metrics -> 1 scored). Appended 2026-07-23.
# Uppsala Conflict Data Program: academic gold-standard EVENT-COUNT source for
# organized violence (state-based, non-state, one-sided), coded from documentation
# with low/best/high fatality bounds. Only *_best shipped. Different measurement
# family from every prior block - observed body-counts, not analyst scores - so it
# adds the fatality leg to C2, which otherwise rests on expert indices + coup events.
# Pipeline ALREADY zero-filled: every column at 99.5% coverage, absence = true zero
# (global event census). 43 of 196 countries carry nonzero state-based deaths in 2024.
# SCORE ONE METRIC: intrastate battle-deaths, per-capita, log1p (zero-inflated), higher=worse.
# WHY INTRASTATE not combined state-based: interstate war is EXTERNAL AGGRESSION, not
# internal regime instability - it shows the file's max (68,099, Ukraine) but a country
# invaded by a neighbour is not exhibiting political-order failure. Scoring interstate in
# C2 would mark the victim of aggression as unstable, inverting the construct.
# =====================================================================
D += [
 dict(m="ucdp_sb_intrastate_deaths_best", s="UCDP", d="-", at=[(2, "P1")],
      derive="per-capita (/ wdi_population_total), log1p",
      note="civil-war/insurgency battle deaths - the observed-fatality leg of C2. Zero-filled census, 41 nonzero of 196 in 2024"),

 # interstate: external aggression, wrong construct for a political-STABILITY concept
 dict(m="ucdp_sb_interstate_deaths_best", s="UCDP", d="", at=[],
      why="interstate war = external aggression, not internal regime instability; scoring it in C2 would mark the victim of invasion as unstable (Ukraine is the file max). Inverts the construct"),
 dict(m="ucdp_sb_interstate_exists", s="UCDP", d="", at=[], why="interstate existence flag - see interstate_deaths"),

 # combined state-based: superseded by the intrastate split
 dict(m="ucdp_sb_deaths_best", s="UCDP", d="", at=[], why="combined state-based deaths; superseded by the intrastate split (removes interstate contamination)"),
 dict(m="ucdp_sb_conflict_exists", s="UCDP", d="", at=[], why="binary existence - strictly dominated by the deaths severity measure"),
 dict(m="ucdp_sb_conflict_count", s="UCDP", d="", at=[], why="dyad count - a fragmentation/territorial-control signal (considered for C13) but a poor severity proxy and partly a coding artifact; deaths preferred for C2"),
 dict(m="ucdp_sb_intrastate_exists", s="UCDP", d="", at=[], why="existence flag; the deaths measure already encodes existence"),

 # non-state: weak-state signal, not regime instability
 dict(m="ucdp_ns_deaths_best", s="UCDP", d="", at=[], why="non-state communal violence - a weak-state-control signal, not regime instability; not on-concept for C2"),
 dict(m="ucdp_ns_conflict_exists", s="UCDP", d="", at=[], why="non-state existence flag"),
 dict(m="ucdp_ns_conflict_count", s="UCDP", d="", at=[], why="non-state dyad count"),

 # one-sided: overlaps C16, from which the master deliberately excluded UCDP
 dict(m="ucdp_os_deaths_best", s="UCDP", d="", at=[], why="one-sided violence against civilians overlaps C16 Personal security, from which the master deliberately routed UCDP away to keep conflict data in C2"),
 dict(m="ucdp_os_violence_exists", s="UCDP", d="", at=[], why="one-sided existence flag - see os_deaths"),
 dict(m="ucdp_os_govt_killings_best", s="UCDP", d="", at=[], why="government killings of civilians - a distinct state-violence signal, but the master routed UCDP away from C16; left on the table rather than overriding that placement"),
 dict(m="ucdp_total_orgvio_deaths_best", s="UCDP", d="", at=[], why="rollup summing all three violence types, incl. the interstate/one-sided/non-state content excluded above on construct grounds"),
]


PENDING += [
 "WEIGHTING (Step 4): metric->concept weighting is UNSET. Working default = equal-weight-within-tier, with tiers (P1>P2>Sp) as coarse weighting - so every tier call this pass IS a weighting decision, and those multipliers are ALREADY LOCKED in metric_methodology S6 (2026-07-10): P1=1.0, P2=0.5, Sp=0, as revisitable DEFAULTS - an earlier version of this item wrongly said they were unset (corrected 2026-07-24); what is genuinely open at Step 4 is the equal-weight and promotion sensitivity check on those defaults. Locked already: categories equal; concepts = relevance x measurement-quality (C11 Trade and C12 Environmental at 0.5 relevance; measurement-quality 1.0/0.75/0.5 mechanism locked, per-concept values due at Step 1).",
 "WEIGHTING (Step 4): decide whether within-tier weighting should be CORRELATION-AWARE. Equal-weight-within-tier treats correlated metrics as independent, so it under-penalizes (a) over-measured concepts (C22 Civil liberties 15, C23 Media 11 - many correlated perception measures) and (b) single-source concentration (C19 Legislative checks 5-of-5 V-Dem coded as 5 independent metrics). Highest-value weighting question in the framework. Derived sub-composites (wdi_health_index, pts_index) already embed ad-hoc anti-concentration weighting that a general rule should subsume.",
]


# =====================================================================
# RTI Rating block (11 columns -> 1 scored). Appended 2026-07-23.
# Global Right to Information Rating (Centre for Law and Democracy + Access Info
# Europe): scores the DE JURE strength of a country's FOI legal framework against
# 61 indicators -> rti_total (0-150) + 7 category sub-scores. 196 countries: 142 with
# an RTI law get real scores, 54 with NO law are floored (deficit-list flag) - a
# documented scoring choice that is construct-correct: no FOI law is the worst possible
# framework, not missing data. Cross-sectional (history deferred - RTI is a sticky
# step-function).
# SCORE rti_total, drop the 7 sub-scores. This is the OPPOSITE of the WDI decomposition,
# deliberately: RTI's 7 categories are facets of ONE coherent legal-quality construct
# that stand or fall together (a well-drafted FOI law is well-drafted throughout), and
# CLD's aggregation reflects the international-standards consensus on what a strong law
# contains - there is no arbitrary source-weighting to correct, unlike WDI's genuinely
# different health/education/infra dimensions. Decompose when sub-components are rival
# constructs the framework should weight itself; keep the total when the source has
# aggregated one construct on a principled basis.
# DE JURE CAVEAT: rates the law on paper, not information actually released. Afghanistan
# scores 139/150 under a government that does not release information - the same
# rules-on-paper failure mode as WB BRSS. Record in output; do not correct here (RTI
# correctly measures the statute).
# TIER = WEIGHTING: P1 in C25 (RTI's home - the FOI legal-framework leg), P2 in C23
# (media-environment input, and C23 is already at 11 metrics).
# 0-150 bounded scale with a meaningful floor -> S5 fixed-anchor candidate, pass-through.
# =====================================================================
D += [
 dict(m="rti_total", s="RTI_RATING", d="+", at=[(25, "P1"), (23, "P2")],
      note="de jure FOI legal-framework strength, 0-150. P1 in C25 Government transparency (home concept), P2 in C23 Media freedom. Fixed-anchor candidate. DE JURE ONLY - Afghanistan 139/150 illustrates rules-on-paper vs practice"),

 dict(m="Right of Access", s="RTI_RATING", d="", at=[], why="component of rti_total (one coherent legal-quality construct; scored via the total)"),
 dict(m="Scope", s="RTI_RATING", d="", at=[], why="component of rti_total"),
 dict(m="Requesting Procedure", s="RTI_RATING", d="", at=[], why="component of rti_total"),
 dict(m="Exceptions & Refusals", s="RTI_RATING", d="", at=[], why="component of rti_total"),
 dict(m="Appeals", s="RTI_RATING", d="", at=[], why="component of rti_total"),
 dict(m="Sanctions & Protections", s="RTI_RATING", d="", at=[], why="component of rti_total"),
 dict(m="Promotional Measures", s="RTI_RATING", d="", at=[], why="component of rti_total"),
 dict(m="has_rti_law", s="RTI_RATING", d="", at=[],
      why="metadata flag (142 law / 54 floored), not a score - feeds the S8 reliability layer so a floored no-law country carries that context rather than reading as measured-and-failed"),
 dict(m="rti_law_year", s="RTI_RATING", d="", at=[], why="metadata - year the FOI law was enacted, not a governance score"),
]


# =====================================================================
# FATF block (110 columns -> 2 scored composites). Appended 2026-07-23.
# FATF Mutual Evaluations: intergovernmental AML/CFT audit, 199 countries, one row per
# country (newer methodology round wins: 192 on the 2013/4th round, 7 on 2022/5th).
# Two grading axes, each item 0-3, both at 100% coverage (all 11 IOs and ~40 Recs
# present for all 199 - no missingness, no penalty):
#   TECHNICAL COMPLIANCE (40 Recommendations, C/LC/PC/NC) = DE JURE. "Compliance" here
#     means compliance with the FATF STANDARD (are the required laws on the books),
#     NOT real-world compliance. Assessors read statutes. Faint de facto bleed (does the
#     agency exist) but essentially rules-on-paper.
#   EFFECTIVENESS (11 Immediate Outcomes, HE/SE/ME/LE) = DE FACTO. FATF built the IOs
#     precisely because countries passed on paper and failed in practice - they measure
#     whether laundering is actually detected, prosecuted, disrupted. One of the very few
#     genuine cross-country EFFECTIVENESS measures in the whole framework.
# THE GAP IS HUGE AND IS THE POINT: technical compliance averages 2.05/3, effectiveness
# 0.83/3 - nearly everyone has the laws, almost nobody achieves enforcement. Corr between
# the two axes = 0.547, so they genuinely diverge; the split is not symbolic.
# OVERWEIGHT EFFECTIVENESS VIA TIER (recorded weighting decision): effectiveness P1,
# technical compliance P2. Justified twice over - (a) de facto is the scarcer, more
# decision-relevant signal, (b) technical compliance barely discriminates (SD 0.37 vs
# 0.58), a near-constant that would not earn P1 regardless of construct.
# COLLAPSE: 102 R/IO columns = 51 items x (raw grade + numeric 0-3). Score the numeric,
# drop the raw. Then 51 items -> 2 composites (de jure/de facto), not scored individually
# (51 metrics in one concept is absurd) and not 1 (would destroy the axis that is FATF's
# most valuable feature).
# =====================================================================
import re as _re
_F = open('data/processed/fatf_clean.csv').readline().strip().split(',')
_REC_NUM = [c for c in _F if _re.match(r'^R\d+_num$', c)]
_IO_NUM  = [c for c in _F if _re.match(r'^IO\d+_num$', c)]
_REC_RAW = [c for c in _F if _re.match(r'^R\d+$', c)]
_IO_RAW  = [c for c in _F if _re.match(r'^IO\d+$', c)]

D += [
 dict(m="fatf_effectiveness", s="FATF", d="+", at=[(9, "P1")],
      derive="mean of the 11 Immediate Outcome numeric scores (IO1_num..IO11_num), 0-3",
      note="DE FACTO AML/CFT effectiveness - rare cross-country effectiveness measure. P1 (overweighted vs compliance): scarcer signal AND better discrimination (SD 0.58). Weakest globally on IO7 (ML prosecution), IO5 (legal-persons transparency), IO11 (TF sanctions) - the enforcement leg"),
 dict(m="fatf_technical_compliance", s="FATF", d="+", at=[(9, "P2")],
      derive="mean of the 40 Recommendation numeric scores (R1_num..R40_num), 0-3",
      note="DE JURE framework quality (FATF-standard compliance = laws on the books, not real-world compliance). P2 not P1: de jure discount + near-constant (mean 2.05, SD 0.37) so low discrimination. Corr 0.547 with effectiveness"),
]

# 40 Rec numerics + 11 IO numerics: components of the two composites
D += [dict(m=c, s="FATF", d="+", at=[], why="component of fatf_technical_compliance") for c in _REC_NUM]
D += [dict(m=c, s="FATF", d="+", at=[], why="component of fatf_effectiveness") for c in _IO_NUM]
# 51 raw letter-grade columns: superseded by the numeric encodings
D += [dict(m=c, s="FATF", d="", at=[], why="raw letter grade; scored via the _num encoding") for c in (_REC_RAW + _IO_RAW)]
# identifier / metadata columns
for c in ["iso3", "jurisdiction", "methodology_round", "report_type", "report_date",
          "assessment_body", "n_upgrades", "n_downgrades"]:
    D += [dict(m=c, s="FATF", d="", at=[], why="identifier/metadata, not a governance score")]

PENDING += [
 "C9 Financial sector: FATF adds AML/CFT (de jure + de facto). With BRSS (banking prudential, de jure, Supplementary) the concept now has effectiveness signal - but SECURITIES and INSURANCE regulation remain uncovered, and supervisory effectiveness beyond AML awaits FSAP (PDF-locked, outstanding). State plainly in C9 output: measures AML/CFT + banking rules, NOT securities/insurance/broad supervisory effectiveness",
 "C9 TIER DECISION now decidable with both sources in view: FATF Primary (covers the concept's core + the only effectiveness axis), BRSS Supplementary (de jure banking only). Confirm BRSS scoring next",
]


# =====================================================================
# WB BRSS block (13 columns -> 1 scored). Appended 2026-07-23.
# World Bank Bank Regulation and Supervision Survey (Barth-Caprio-Levine): survey of
# national banking regulators, ~160 countries, FROZEN at the 2019 wave / 2016 reference
# year (no newer wave). The pipeline (nb 38) did NOT take the published BCL indices - it
# built a bespoke construct-aligned DE JURE regulatory-stringency score across 9
# sub-constructs, then a weighted overall (brss_regstringency). Cadence = snapshot(no-year),
# so recency is judged cadence-relative: 76% sovereign coverage clears the bar (an annual
# source ending 2016 would fail; a snapshot does not).
# SCORE brss_regstringency (the overall index), drop the 9 sub-constructs: decompose-or-
# keep-whole - one coherent de jure banking-stringency construct the pipeline already
# aggregated on a principled basis, and a Supplementary leg should not sprawl to 9 slots.
# TIER = SUPPLEMENTARY, and the rationale is STALENESS not peripherality (recorded in
# framework_decisions). Banking prudential regulation is CENTRAL to C9, not peripheral -
# it is the concept's only non-AML, only-prudential signal. BRSS is Supplementary purely
# because the 2016 vintage is too stale to drive a 2025 score (Basel III phase-in,
# resolution reforms post-date it), while remaining useful evidentiary context (bank-rule
# frameworks are sticky, so 2016 still informs drill-down). If judged current-enough it
# would be P2, not Sp - the tier turns on staleness alone.
# DE JURE caveat: rules on paper, not supervisory effectiveness (advanced economies
# mid-pack is CORRECT, validated vs Anginer et al). Same rules-vs-practice failure mode
# as RTI and FATF technical compliance.
# =====================================================================
D += [
 dict(m="brss_regstringency", s="WB_BRSS", d="+", at=[(9, "Sp")],
      note="de jure banking regulatory stringency, 0-1, weighted mean of 9 sub-constructs. Supplementary on STALENESS (2016 vintage) NOT peripherality - it is C9's only prudential-banking signal. Would be P2 if current. Fixed-anchor candidate"),
]
_BRSS_SUB = ["supervisory_power", "supervisory_independence", "capital_stringency",
             "private_monitoring", "resolution_regime", "provisioning",
             "liquidity_concentration", "macroprudential", "supervisory_capacity"]
D += [dict(m=c, s="WB_BRSS", d="+", at=[], why="component of brss_regstringency (one de jure banking-stringency construct; scored via the overall index)")
      for c in _BRSS_SUB]
D += [
 dict(m="brss_coverage", s="WB_BRSS", d="", at=[], why="metadata - per-country survey-question coverage fraction, not a score"),
 dict(m="brss_reliable", s="WB_BRSS", d="", at=[],
why="metadata reliability flag (coverage >=70%) - GATES whether a country's BRSS score is used (excludes sparse entries), does NOT attenuate the value (score-deflation-by-coverage was rejected as incoherent). Feeds S8"),
 dict(m="country_code", s="WB_BRSS", d="", at=[], why="identifier"),
]

# =====================================================================
# IMF_FISCAL_RULES (24 cols -> 4 scored) -> C8 Macroeconomic policy framework quality.
# Fills C8's previously-absent fiscal-framework leg. De jure design (breadth, strength,
# teeth) + one de facto leg (compliance). Per-rule-type columns EXCLUDED as a class:
# self-selected reference class (quality cols populated only for countries having that
# rule type, e.g. legal_basis_rr n=13 = only 13 have revenue rules) + decompose-or-keep-whole.
# Source current to 2024. Full operational detail per metric in metric_dictionary.py.
# =====================================================================
D += [
 dict(m="fr_num_rule_types",  s="IMF_FISCAL_RULES", d="+", at=[(8, "P1")],
      note="breadth 0-4 (count of ER/RR/BBR/DR in force). De jure. Fills C8 fiscal-framework leg"),
 dict(m="fr_max_legal_basis", s="IMF_FISCAL_RULES", d="+", at=[(8, "P1")],
      note="strength: strongest legal footing among a country's rules, ordinal 1-5 (5=constitutional). MAX not mean - mean penalizes breadth"),
 dict(m="fr_any_enforcement", s="IMF_FISCAL_RULES", d="+", at=[(8, "P2")],
      note="teeth: any rule carries formal enforcement, binary. P2 - lower discrimination, partly implied by legal basis"),
 dict(m="fr_compliance_mean", s="IMF_FISCAL_RULES", d="+", at=[(8, "P2")],
      note="de facto adherence: mean over present rule types of compliance {0/0.5/1}, 2=partial->0.5 (2024 manual). COVERAGE-FLAGGED 54 ctry (~28pct). ENDOGENEITY: compliance partly reflects rule laxity - direction weaker than de jure legs, hence P2"),
]
D += [
 dict(m="fr_mean_legal_basis", s="IMF_FISCAL_RULES", d="", at=[],
      why="mean legal basis PENALIZES BREADTH: adding a weak rule lowers the mean, so a country with a strong rule scores lower for having a second weaker one. fr_max_legal_basis (firmest footing) + fr_num_rule_types (breadth) capture what mean muddles"),
]
_FR_PER_RULE = ["fr_legal_basis_er","fr_legal_basis_rr","fr_legal_basis_bbr","fr_legal_basis_dr",
                "fr_enforcement_er","fr_enforcement_rr","fr_enforcement_bbr","fr_enforcement_dr",
                "fr_compliance_er","fr_compliance_rr","fr_compliance_bbr","fr_compliance_dr",
                "fr_expenditure_rule","fr_revenue_rule","fr_budget_balance_rule","fr_debt_rule",
                "fr_indep_body_sets_assumptions","fr_indep_body_monitors",
                "fr_correction_mechanism","fr_correction_well_defined_triggers"]
D += [dict(m=c, s="IMF_FISCAL_RULES", d="", at=[],
           why="per-rule-type / feature component; scored via the derived cross-rule metrics (num_rule_types, max_legal_basis, any_enforcement, compliance_mean). Self-selected reference class if scored directly")
      for c in _FR_PER_RULE]

PENDING += [
 "IMF_FISCAL_RULES compliance PIPELINE NOTE: fr_compliance_mean is built in nb 25 via to_compliance ({0,1,2}->{0.0,1.0,0.5}, 2=partial) then mean over present rule types. If re-run, restart kernel first - cell 5 mutates fr in place and double-parsing collapses compliance to all-zero (caught 2026-07-24). Scaling (percentile vs fixed-anchor) is TBD at Step-3",
]

PENDING += [
 "C9 Financial sector: FATF effectiveness (P1, de facto AML/CFT) + FATF technical compliance (P2, de jure AML/CFT) + BRSS stringency (Sp, de jure banking). CORRECTION 2026-07-24: earlier text said '3 metrics, clears thin flag' - WRONG, the S6 trigger counts PRESENT P1+P2 and BRSS is Sp (weight 0), so C9 has 2 scored indicators, BOTH FATF, and remains THIN + SINGLE-SOURCE (rests on AML/CFT). GAPS: securities, insurance, non-AML supervisory effectiveness - all await FSAP (PDF-locked). C9 output must state it measures AML/CFT + banking rules, not the full financial-supervision remit",
]


# ---- DOC-AUDIT ADDITIONS 2026-07-24 ----
PENDING += [
 "C17 Property rights - Fraser Area 2 UNRESOLVED FLAG: metric_methodology S11 and the master both call for property-specific sub-component selection, but fraser_clean.csv carries only area aggregates and fraser_legal_system (full Area 2) was scored at P2 without resolving the flag. Either extend the Fraser pipeline to sub-components or explicitly accept the aggregate - decide before Step 3",
 "C20 Electoral process - IDEA Voter Turnout: master says keep-for-metric-pass but NO pipeline was ever built, so there is nothing to score. Status = not-built; the compulsion-adjustment question is moot unless a pipeline is added. Recorded so the master flag does not read as an open decision",
 "C10 State control over the economy - SECOND-INDICATOR PAIRING DECLINED (user decision, session 2026-07-23). The master suggested pairing v2clstown with IMF GFS Public Corporations or Fraser government-enterprises; user declined both, and the one tested candidate (ccp_market_economy_provisions) failed on variance (81/19 binary de jure constitutional text). C10 stays single-indicator, carrying its S8 weight-review flag",
]

PENDING += [
 "BUILD BACKLOG (updated 2026-07-24 after the derivation session). Original 8 scored-but-not-built "
 "metrics found during dictionary backfill, now resolved as follows. FOUR simple derivations: THREE "
 "BUILT in src/derive_metrics.py - vdem_regime_duration (capped run-length on v2x_regime), pts_index "
 "(union-mean of the 3 QoG PTS coders), wb_carbon_revenue_pct_gdp (carbon revenue / reconstructed "
 "total GDP as pct). ONE DROPPED - wdi_ip_nonresident_per_gdp (per-GDP ratio pathological at small "
 "economies; C17 well-carried without it). FOUR C5 composites RECLASSIFIED to the SCALING LAYER (not "
 "step-1 derivations): their spec is mean of z-normalized components, and z-normalization is a "
 "cross-panel scaling op, so they build with the scaling layer, not derive_metrics.py. Membership is "
 "FULLY SPECIFIED (no open composition decision): wdi_health_index (9 comps), wdi_education_index (4), "
 "wdi_infrastructure_index (3), wdi_social_protection_index (3), all C5 P1. EMBEDDED SIGN-FLIPS the "
 "scaling build MUST apply before averaging: wdi_maternal_mortality and wdi_mortality_under5 (health) "
 "and wdi_pupil_teacher_ratio_secondary (edu) are higher=WORSE, invert before the mean; all other "
 "components are higher=better. These embed equal-weight-across-components, an ad-hoc anti-concentration "
 "choice the Step-4 correlation-aware weighting rule should subsume (see the WEIGHTING pending item).",
]