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
 dict(m="obs_open_budget_index",        s="OBS",            d="+", at=[(7,"P1"),(25,"P2")]),
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
 17: ["v2clprptym", "v2clprptyw", "v2xcl_prpty"],
 18: ["v2x_corr", "v2excrptps", "v2exembez", "v2lgcrrpt", "v2jucorrdc"],
 19: ["v2xlg_legcon", "v2lgoppart", "v2lgqstexp", "v2lginvstp", "v2lgotovst"],
 20: ["v2x_polyarchy", "v2elfrfair", "v2elirreg", "v2elintim", "v2elvotbuy",
      "v2elaccept", "v2elembaut", "v2elembcap"],
 21: ["v2x_partip", "v2psprlnks", "v2pscohesv", "v2cseeorgs", "v2dlconslt", "v2csreprss"],
 22: ["v2x_civlib", "v2x_clpriv", "v2clrelig", "v2cldmovem", "v2cldmovew",
      "v2clsocgrp", "v2clslavef"],
 23: ["v2x_freexp_altinf", "v2mecenefm", "v2meharjrn", "v2mecorrpt",
      "v2meslfcen", "v2merange", "v2mebias", "v2mecrit"],
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
 dict(m="wdi_ip_nonresident_per_gdp", s="WDI", d="+", at=[(17, "P2")],
      derive="mean of z-normalized (patent_applications_nonresident, trademark_applications_nonresident), each divided by GDP current US$ (wdi_gdp_per_capita_usd * wdi_population_total)",
      note="partial proxy for the master's WIPO IP row. NONRESIDENT only: foreign firms seeking protection in a jurisdiction is revealed-preference evidence of confidence in that protection; resident filings measure domestic innovation capacity, not governance. GDP-normalized - raw counts are dominated by economy size"),
 dict(m="wdi_patent_applications_nonresident", s="WDI", d="", at=[], why="component of wdi_ip_nonresident_per_gdp"),
 dict(m="wdi_trademark_applications_nonresident", s="WDI", d="", at=[], why="component of wdi_ip_nonresident_per_gdp"),
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
