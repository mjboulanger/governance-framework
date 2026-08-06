# Framework Decisions Log

**Status:** Temporary working document. Delete when master PDF is regenerated.
**As-of date (last manually updated):** 2026-07-09
**⚠️ MANUAL SNAPSHOT:** This document is a point-in-time snapshot maintained by hand. It does NOT auto-update. Coverage ranges, vintages, source counts, and "as-of" dates below were accurate as of the date above and must be refreshed manually when pipelines are re-run or sources change.
**Purpose:** Captures decisions made during pipeline build phase that diverge from or update the master PDF.
**Metric-pass methodology** (scoring, normalization, aggregation, weighting, reliability, momentum, metric inclusion) lives in `docs/metric_methodology.md`; this log retains source-level and build decisions.

---

## Recent Structural Decisions

**2026-07-24 - D1 complete: all 144 scored metrics profiled + normalization method resolved.** The 29 metrics created after the July-16 profile build (PEFA/NELDA/FATF/WDI-indices/wbl/fr/spi/obs/pei/gpi/ascor/pts/vdem_regime_duration/wb_carbon) were profiled using the EXACT nb 39 _classify logic and thresholds (skew 1/3, zero-frac 0.30/0.60, bimodality BC 0.75, ordinal <=6 levels, pile 0.20) on the spine-filtered pooled panel, so they classify identically to the original 115. Profile grew 330->359 rows. Then final_method was filled for all 144 scored metrics: 132 rule (mechanical from suggested_method), 12 reviewed. **5 new REVIEW/borderline cases resolved:** fr_compliance_mean kept zscore (genuinely bimodal fiscal-rule compliance - 24% fully-noncompliant, 59% fully-compliant, real middle; humps are real signal per spec); wb_carbon_revenue_pct_gdp OVERRODE to log1p_zscore (zero-inflated magnitude, 20% zeros + right tail, same threshold-miss as cpj_imprisoned); pts_index kept zscore (bounded 1-5, distance meaningful); wdi_infrastructure_index kept zscore (bimodality is the real global development divide, spec keeps access indicators on z); fr_max_legal_basis -> percentile via the ordinal rule (genuine 4-level legal-basis category). Final method mix across 144: 124 zscore, 8 percentile, 7 binary, 4 log1p_zscore, 1 log_zscore. **This completes D1** - every scored metric now has a measured distribution and a resolved normalization method, the precondition for the D3 orchestration run.

**2026-07-24 - Task D foundations: normalization transform engine + 6 previously-unbuilt metrics (2 FATF + 4 WDI sub-composites); verified end-to-end.** Start of the scoring layer (Stage 3). **(1) Transform engine (src/normalize.py):** the z-family winsorized-z transform (methodology S5) as a standalone, unit-tested function - the atom the rest of the scoring layer calls. Implements the fixed-pooled trailing-20yr baseline (params computed once on the metric's own most-recent-20yr window, applied to ALL history including out-of-window years, which are winsorized against the fixed reference), three variants (zscore / log_zscore / log1p_zscore via a pre-transform), winsorization at +/-3, population SD, and the three S5 baseline-provenance attributes (baseline_n_years, baseline_n_obs, baseline_year_span). Built BEFORE the full D3 orchestration deliberately: it is independently verifiable AND the WDI sub-composites depend on it. Non-z methods (percentile / occurrence / fixed-anchor) are NOT in this module - simpler, and belong to the orchestration layer. **(2) FATF composites:** fatf_effectiveness = mean of the 11 Immediate Outcomes (IO*_num, de facto AML/CFT), fatf_technical_compliance = mean of the 40 Recommendations (R*_num, de jure); N/A ratings excluded from the mean, never zeroed. Validated: 189 countries, the de-jure-over-de-facto gap holds emphatically (compliance mean 2.05 vs effectiveness 0.82, +1.24, compliance>effectiveness in 187/189) - the framework's flagship rules-overstate-governance result. **(3) 4 WDI service-delivery sub-composites (C5):** health (9 components), education (4), infrastructure (3), social protection (3) - 19 components total, each tagged in metric_selection. Construction: each component winsorized-z transformed via the engine, direction-aligned (3 inverted components negated: under-5 mortality, maternal mortality, secondary pupil-teacher ratio), then index = equal-weight mean-of-available of the component z's (union coverage, S4). Validated: direction correct (highest-under-5-mortality countries score NEGATIVE health, lowest score POSITIVE), face-valid (Norway/Japan/Germany high infra ~+0.8, Chad/CAR/South Sudan ~-2.1 to -2.6). **Verification (three lifecycle checks, all clean):** (a) Fiji -> C18 full trace raw->normalize->direction-align->harmonize->tier-weighted-mean = 0.590, five independent corruption measures converge at 0.55-0.63, WJP-absent correctly excluded-not-floored; (b) methodology-break audit - TI CPI (2012) and FH sub-categories (2013) confirmed to carry NO pre-break data, so no non-comparable observations pool into any baseline (invariant: pre-break data must not be in the panel at all); (c) Georgia -> PEFA two-level pillar-mean-of-means verified exact vs derivation, cross-sectional baseline correctly pools 82 one-per-country assessments (n_obs=82 flagged). **Also:** the 8 REVIEW normalization methods resolved (6 kept zscore, cpj_imprisoned + imapp_breadth_total overridden to log1p as zero-inflated counts the 0.60 threshold missed). Z-math verified exact vs hand-computation. Scored count unchanged (144); these 6 were already selected, now computable.

**2026-07-24 - THIN reviews closed (C3, C9); Task B complete.** Dispositioned the two remaining THIN flags (both document-only, no metric change). **C3 (Statistical infrastructure): intrinsically thin, adequately measured** - 2 independent P1 sources (ODIN, IMF SPI) cover a coherent narrow concept; the obvious third candidate (WB Statistical Capacity Indicator) was superseded BY SPI (same lineage, not independent), so there is no honest way to add a third. No action. **C9 (Financial regulation): thin-with-known-gap, and sharper than 'thin'** - because BRSS is Supplementary (weight 0), C9's SCORED content is entirely FATF, i.e. a single source measuring only the AML/CFT slice standing in for all of financial-sector regulation (the C19 single-source problem, but narrower). AML compliance is a weak proxy for banking-prudential or securities/insurance regulation - a real v1 validity limitation. But it is not an unaddressed oversight: the filling source (FSAP + embedded BCP/IOSCO/IAIS) is confirmed PDF-only and already deferred to the Category-1 PDF-extraction batch. Documented as thin-with-known-gap-pending-FSAP. **Also fixed a doc bug:** the C23 media-collapse note had been mis-appended to C9's state-of-measurement line (wrong SoM matched during the C23 edit); moved it to C23 where it belongs. **TASK B COMPLETE.** Full disposition of all flagged concepts: OVER - C8 (weighting, done earlier), C22 (collapsed 7->6 V-Dem, residual is legitimate breadth), C23 (collapsed 8->5); collapse pass also hit C17 (3->1), C18 (5->3), C14 (4->3); C19 and C20 examined and NOT collapsed (distinct signal / single-source); THIN - C3 (intrinsic, adequate), C9 (known FSAP gap), C10 (deferred v2). Scored count net across Task B: 153->144.

**2026-07-24 - C22 (Civil liberties) V-Dem collapsed 7 to 6; OVER flag resolved as legitimate breadth.** Dropped v2x_clpriv (private civil liberties INDEX), kept v2x_civlib (broad CL index) + 5 components. Gate 1: the two indices correlate r=0.96 - the concept was scoring the same aggregate twice. Gate 2 FAILED: v2x_clpriv's divergences from v2x_civlib are modest (max 0.85z vs 1.7-1.95z for genuinely distinct metrics retained in C18/C23) and merely reflect political repression exceeding private-sphere restriction (Zimbabwe/Venezuela/Bangladesh/Belarus) or the reverse (Qatar) - a pattern the retained components already capture directly, since v2x_clpriv aggregates exactly those components. **Key finding: C22's components are the most DISTINCT of any V-Dem cluster examined** - v2clsocgrp (social group equality) r 0.59-0.69, v2clslavef (forced labour) r 0.59-0.75, and the movement gender pair r=0.81 carries REAL signal (legal restrictions on women's movement genuinely diverge from men's in some jurisdictions), unlike C14's r=0.96 access-to-justice twins. So only one metric was redundant. **OVER-flag disposition:** C22 stays flagged OVER at 14 metrics, but this is LEGITIMATE BREADTH - 14 metrics across 5 genuinely different sources (V-Dem, Pew, WB Women Business and the Law, PTS, Freedom House) measuring distinct facets. Residual is a Step-4 weighting matter (like C8), not a trimming one. **Resolves the C17 open item:** the property-rights gender gap should NOT be moved into C22 - gender is already well covered there via WB WBL (3 metrics) + the movement pair; adding it would duplicate WBL legal-framework content. Scored 145->144, cross-check clean 144/144.

**2026-07-24 - C14 (Legal quality) V-Dem collapsed 4 to 3; collapse pass COMPLETE.** Dropped v2clacjstm (access to justice, men), kept v2clacjstw (women). The pair correlates r=0.96 - near-identical twins, the highest redundancy in any collapse. Unlike C17 property rights (gender split diverged interpretably via discriminatory inheritance law), procedural access to justice is barely gender-differentiated, so the men metric added no distinct signal (Gate 2 fail). Kept the distinct constructs: v2cltrnslw (transparent/predictable law) and v2xeg_eqaccess (equal-access index, r~0.72, most distinct). Lightest collapse of the four - just one duplicate removed. C14 8->7, scored 146->145, cross-check clean 145/145.

**COLLAPSE PASS SUMMARY (2026-07-24).** The within-source metric collapse rule (two-gate test, methodology S6 / master principle 11) was defined and applied consistently across the high-correlation V-Dem clusters flagged by the cross-concept scan: **C23 Media freedom 8->5** (kept composite + corruption/range/censorship/bias; dropped 3 scale-noise components), **C17 Property rights 3->1** (composite only; gender split sent to C22's domain), **C18 Control of corruption 5->3** (kept composite + legislative + judicial branch signal; dropped 2 executive as already-most-measured), **C14 Legal quality 4->3** (dropped 1 near-identical access-to-justice twin). **C19 Legislative checks: examined, NOT collapsed** - components carry distinct oversight-function signal AND it is single-source (5-of-5 V-Dem) with no composite fallback, so collapsing would thin a concentrated concept without addressing its real problem (source diversity, a separate scouting gap already documented). **What the pass demonstrated:** the two-gate test is proportionate, not mechanical - it collapses toward the composite where components are redundant scale-noise (C23/C17), KEEPS components where they carry distinct decision-relevant signal (C18 branches, C19 oversight functions), and removes only genuine duplicates (C14). High correlation alone never drove a drop; Gate 2 (distinct-information test) did the deciding work every time. Total across the pass: 153->145 scored (8 metrics removed as redundant).

**2026-07-24 - C18 (Control of corruption) V-Dem collapsed 5 to 3 (3rd application; first that KEEPS components over composite-only).** Kept v2x_corr (composite) + v2lgcrrpt (legislative) + v2jucorrdc (judicial); dropped v2excrptps (exec bribery) + v2exembez (exec embezzlement). **Why keep the branch components:** the branch split carries decision-relevant distinctions the composite blends away - countries split sharply on WHERE corruption concentrates (Burkina Faso/Ghana: corrupt courts, clean legislature; PNG/Sri Lanka: the reverse), and judicial corruption specifically threatens contract enforcement, an investor concern. Judicial-legislative inter-correlation is only 0.77 (below threshold), confirming distinct signal. **Why drop the two executive metrics:** executive corruption is the most-measured dimension in C18 already - it is what TI CPI, BCI, and WJP predominantly capture, plus it sits in the composite - so the two V-Dem executive sub-metrics (r=0.89 with each other, same branch) add no distinct signal (Gate 2 fail). **Significance:** C18 is the first collapse that retains COMPONENTS rather than collapsing to composite-only - proving the two-gate test protects distinctive metrics (C23/C17 collapsed toward the composite because their components were redundant; C18's branch components are not). The rule discriminates by distinct signal, not by a mechanical keep-the-composite default. C18 stays very well-measured (6 metrics, 4 sources). Scored 148->146, cross-check clean 146/146. Remaining collapse candidates: C19 (r=0.84), C14 (0.81).

**2026-07-24 - C17 (Property rights) V-Dem collapsed 3 to 1 (2nd application of the collapse rule).** C17's V-Dem cluster (composite v2xcl_prpty + men v2clprptym + women v2clprptyw) collapsed to the composite only. Both components r>0.93 with the composite (Gate 1). Men's divergences are extreme-low-tail wobble (Afghanistan/North Korea - no decision-relevant distinction). Women's divergences are genuinely interpretable (Jordan/Cuba - women's property rights lagging the general environment via discriminatory law), a real gender-gap signal - BUT that signal belongs to C22 (Civil liberties / gender, already carrying WB Women Business and the Law), not to C17's investor-facing expropriation/contract-enforcement scope. Chose option (c): collapse to composite, keep C17 focused on the general property environment; if the property-rights gender gap is wanted it should be ADDED to C22, not retained in C17. **Refinement surfaced on this 2nd application:** the collapse rule interacts with concept THINNESS - on a small concept you must check the collapse doesn't drop it below adequacy. Here C17 goes 5->3 metrics but stays adequate (composite + WJP no-expropriation + Fraser legal, 3 INDEPENDENT sources), so the collapse is safe. **Also surfaced:** which metric is 'the redundant one' is purpose-dependent - considered keeping men+women and dropping the composite (option b, preserves the gender gap) but rejected it because the gender dimension is C22's, not C17's. Scored 150->148, cross-check clean 148/148. Remaining collapse candidates: C18 (r=0.86), C19 (0.84), C14 (0.81).

**2026-07-24 - C23 (Media freedom) V-Dem metrics collapsed 8 to 5; establishes the within-source collapse rule.** A cross-concept scan found many concepts score multiple highly-correlated V-Dem sub-indicators (C17 mean r=0.90, C23 0.86, C18 0.86, C19 0.84, etc.) - C23 was not special, so a uniform RULE was defined rather than an ad-hoc C23 trim. **The rule (methodology S6, master principle 11): within-source metric collapse under a two-gate test.** Gate 1 (quantitative): a component is a removal CANDIDATE only if highly correlated (mean pairwise r > ~0.85) with a composite that exists to carry the shared signal. Gate 2 (qualitative): the candidate is removed ONLY IF it also fails to make material, interpretable distinctions the composite blends away (checked by inspecting the countries where it most diverges from the composite). BOTH gates must fail; high correlation alone never drops a metric. This is editorial redundancy pruning, distinct from formal decorrelation (still ruled out - no PCA/factor analysis) and from pure weighting control. **C23 application:** kept v2x_freexp_altinf (composite), v2mecorrpt (isolates media-corruption/bribery vs state-control - Vietnam/Hong Kong are controlled-not-corrupt), v2merange (isolates pluralism - Iraq dangerous-but-plural), v2mecenefm (censorship channel), v2mebias (propaganda channel); dropped v2meharjrn, v2meslfcen, v2mecrit whose divergences from the composite were clean-end scale/ceiling noise. Scored 153->150. **Residual point:** collapse handled REDUNDANCY; C23 still leans V-Dem (5 of 9 metrics), which is a separate SOURCE-WEIGHT question - V-Dem is the higher-quality comprehensive source and may deserve more weight than the narrow independent sources (CPJ/FH/RTI), but that is set by deliberate Step-4 weighting, not metric count (same principle as C8's 40/40/20). **Remaining:** the same two-gate test still needs applying to the other high-correlation concepts (C17, C18, C19, C14, ...) - C23 is the worked template.

**2026-07-24 - C10 (State control over the economy) THIN flag: deferred to v2.** C10 has a single metric (V-Dem v2clstown, government ownership of the economy, P1). The thinness is a KNOWN, already-reasoned state: C10 was created narrow, with SOE (state-owned enterprise) governance - the natural second dimension - explicitly deferred to v2 when the concept was added. Rather than spend more effort sourcing a second metric now, leave C10 single-metric for v1 and carry the second-metric search (SOE governance data, and/or economic-freedom state-ownership subcomponents from Fraser/Heritage) as a v2 development item. Documented as intrinsically-thin-pending-v2, not an unaddressed gap.

**2026-07-24 - IDEA GSoD Participation scored into C21 (last Stage-2 source).** Scored 2 metrics: idea_participation (GSoD Participation attribute, 0-1, 174 countries 1990-2025) at **P1**, and idea_local_democracy at **P2**. **P1 revised UP from source-level 'Primary tier 2'**: C21 (Political participation beyond voting) is otherwise V-Dem-dominated - 6 of 7 existing metrics are V-Dem (the v2x_partip composite plus 5 facets: psprlnks, pscohesv, cseeorgs, dlconslt, csreprss), and the only non-V-Dem metric (CIVICUS) covers just 2022+. GSoD is the main INDEPENDENT full-history participation measure, so it earns P1 both on direct-measurement merit and for breaking the single-source concentration across the whole panel. **Composite over subcomponents:** scored the top-level Participation attribute rather than decomposing, because civil_society (r=0.980) and civic_engagement (r=0.832) are redundant with it. **local_democracy added at P2** as a distinct facet - the sharpest democracy/autocracy discriminator in the cluster (clean-autocracy gap 0.85 vs composite 0.66), only moderately correlated with the composite (r=0.744, ~half its variance independent), capturing subnational participation the national-focused V-Dem cluster underweights; its mechanical overlap with the composite is flagged for Step-4 correlation-aware weighting. **Excluded:** electoral_participation (weak discriminator gap 0.21; autocracies can drive high turnout; duplicates C20), direct_democracy (degenerate, mean 0.089). Data clean and valid (Denmark 0.96 to North Korea 0.03) - no label/direction issues, unlike DPI/NELDA. Scored 151->153, cross-check clean 153/153. **This closes Task-C (Stage-2): every selected source is now scored or excluded-with-rationale.**

**2026-07-24 - NELDA scored into C20 (Supplementary); QoG pipeline NELDA renames corrected.** Scored 5 binary NELDA election-quality flags into Concept 20 (Electoral process): nelda_concerns_not_free_fair (NELDA11), nelda_media_bias_incumbent (NELDA16), nelda_riots_protests_after, nelda_violence_deaths_before (NELDA33) - all direction NEGATIVE (1=problem); nelda_opposition_allowed - direction POSITIVE. All Supplementary tier. **Tier revised from source-level 'Primary tier 2' DOWN to Supplementary**: C20 already holds 10 P1 metrics, and NELDA is sparse (event-level, ~24.5% of country-years) and systematically absent for ~21 consolidated democracies NELDA excludes by design (absence = implicitly clean, a coverage bias for scaling). **PIPELINE CORRECTION (nb 14):** the QoG pipeline's original NELDA friendly-names were WRONG - mbbe was mislabeled 'multiple_parties' but is actually media-bias-favoring-incumbent; rpae was mislabeled 'ruling_party_advantage' but is post-election riots/protests; fme ('free_and_fair') was direction-inverted (the variable flags CONCERNS, so 1=bad). Caught by a democracy-vs-autocracy reality check (clean democracies scored 0.000 on 'free_and_fair', which was backwards) then verified against the NELDA/QoG codebook. Corrected the rename dict + added raw-99 ('unclear') -> NaN handling in nb 14, regenerated qog_clean.csv (Jan26, same version; diffed all 27 non-NELDA columns - only float-ULP noise, no substantive change to other metrics). **Excluded:** nelda_mtop (near-zero discrimination, clean 1.000 vs rigged 0.964); election-type descriptors noe/noea/noel (type-not-quality). Data valid (separates democracies from autocracies cleanly); the problem was labeling, not the source. Scored 146->151, cross-check clean 151/151.

**2026-07-24 - PEFA scored into C8; C8 sub-dimension weighting locked 40/40/20.** Two PEFA composites added to C8 (the PFM leg after the C7 fold): pefa_core_management (P1 - mean of PEFA Pillar I budget reliability + Pillar V execution control) and pefa_accountability (P2 - mean of Pillar VI accounting + Pillar VII external scrutiny/audit). Chose two composites (Option C) over four pillar metrics (over-concentrates PEFA to ~25% of C8) and over one metric (loses the frontline-vs-oversight split). Each composite = mean of its PILLAR means (pillars equal-weighted regardless of indicator count). Pillars II/III/IV excluded (transparency overlaps OBS; assets/liabilities peripheral/SOE-v2; fiscal strategy overlaps C8 rules leg). PEFA is CROSS-SECTIONAL (one 2016-framework assessment per country, vintage varies 2017-2026, 82 countries, donor-skewed). Pillar VII overlaps C19 legislative oversight - named in the dict for Step-4 correlation-aware weighting. C8 SUB-DIMENSION WEIGHTING LOCKED (Step-4 requirement): Fiscal 40 / Monetary 40 / External 20 - set intentionally so metric count does not drive bucket weight (monetary = 1 metric would fall to ~9% under equal-weight-within-tier; it should be co-equal with fiscal). Within a bucket, metrics share the bucket weight by tier. Resolves C8's OVER flag: 12 metrics is fine once buckets carry fixed weight. Step-4 must implement bucket-level weighting for C8.

**2026-07-24 — Concept 7 (PFM) folded into Concept 8; C8 rescoped.** Public financial management retired as a standalone concept and folded into Macroeconomic policy framework quality. Concept number 7 is now a vacant stable ID (concept numbers are fixed IDs, not positions — C8–C25 unchanged); unique-concept inventory 25→24. **C8 rescoped** from 'design of macro-policy institutions' to 'design AND management of macro-policy institutions', explicitly a two-level concept: (1) policy-framework design (fiscal rules, CBI, monetary/ER regime, macroprudential) and (2) PFM (budget credibility/execution, controls, procurement, accounting, audit). **Rationale:** PFM is thematically closer to fiscal-policy institutions than to general administrative capacity (C4) — the budget is the central instrument of fiscal policy. Options weighed: (A) keep C7 standalone, (B) fold into C8, (C) fold into C4. Chose B. C4-overlap acknowledged (PFM is also administrative competence) but the fiscal-policy theme dominates; C4 fold was also rejected because it would relocate PFM out of the Economic-and-fiscal category. Fold also resolved C7's standalone thinness structurally. **Mechanics:** OBS re-pointed C7→C8 in metric_selection (scored); its dictionary entry updated. PEFA remains pipelined-but-unscored — to be scored into C8 next (pillar-aggregate selection). **v2 to-do (recorded):** C8 has no OUTCOME/execution legs (budget-execution-vs-plan, inflation-target-hit-rate); folding surfaced this gap. Deferred to v2 pending the governance-vs-outcome module-boundary decision — outcomes may belong to the sibling sovereign-credit / macro-vulnerability modules rather than this governance framework.

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
| OECD_TFI | JS simulator/CYC, no API, not in OECD SDMX (exhaustively verified). Composite average downloadable from Compare Your Country (Overview table). Sub-indicators A–K only one-at-a-time (50+ downloads) — not feasible manually. | BUILT (composite, manual download). A–K = future enhancement, not a to-do. |
| IMF Fiscal Rules | DataMapper blocked, no direct Excel URL | Manual Category 4 |
| IMF AREAER | Portal WAF-blocked + JS-gated (confirmed) | BUILT (FARI, manual export, notebook 32) |
| UNCTAD_NTM | WITS bulk download AVAILABLE (wits.worldbank.org NTM Data Download, direct CSV) — no API/JS block. BUT data is stale: latest cross-country vintage is staggered 2012-2017 (9-14 yr old), ~76 countries (frequency/coverage-ratio level). | DROPPED — currency. NTBs = accepted v1 gap. |
| RTI_RATING | Scores table is in page HTML (earlier auth-gated verdict WRONG) | BUILT (automated read_html, notebook 30) |
| REINHART_ROGOFF | Academic download; de facto FX regime; data ends ~2019 | DEMOTED to supplementary — superseded as current-state primary by AREAER de-facto ER classification (BUILT, manual transcription, notebook 37) |
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

**FATF methodology rounds (2013 vs 2022) — one-row-per-country, newer-wins, flag retained.** FATF publishes two consolidated ratings files by methodology generation: 2013 (4th round, 192 countries here) and 2022 (5th round, 7 countries so far). Same output scales (IO: HE/SE/ME/LE; R: C/LC/PC/NC) but the 2022 standard is stricter (shorter 6-yr cycle, tightened R.24 beneficial-ownership, virtual assets, proliferation financing) — so a 2013 'C' and a 2022 'C' are not strictly comparable, and FATF publishes no crosswalk. Pipeline keeps **one row per country, newer methodology round wins**, with a `methodology_round` flag on every row. All 7 of the 2022 countries are also in the 2013 file (zero coverage cost either way). A proposed differential-adjustment (estimate 2022-equivalent scores for the 192 from the 7 overlap countries) was **rejected**: n=7, non-representative (rich-country leading edge), conflates methodology change with real-world change, ordinal scale, no official crosswalk — would manufacture false precision. Comparability handling (use as-is / filter to 2013-only / down-weight the 7) is **deferred to the metric pass**; the flag is the lever. Consistent with the RTI/carbon precedent: make the structural call in-pipeline, flag it, leave the judgment revisable downstream.


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

### C12 (Environmental & climate governance) — source decisions (2026-07-21)
Decided in working session. C12 is assessed through a **governance lens** (climate is one angle from which to assess how a country is governed), not a climate-outcomes lens.
- **ASCOR (TPI/LSE) — ADD.** Investor-led sovereign climate-*policy* assessment (climate legislation, carbon pricing, targets, just transition) — strong governance-lens fit and purpose-built for sovereign-bond investors. Coverage ~85 countries (2025), oriented to sovereign-bond-index (EM/frontier) countries; free/open-source. **Tier (P1 vs P2) to be set at Step-1 metric selection by its developing-country coverage overlap with the spine** (EM/frontier depth is what matters, not headline count). Scouted 2026-07-21: structure confirmed (3 pillars, 14 topic areas; Pillar 2 Climate Policies + CF2/CF3 transparency are the governance-relevant core; Pillar 1 emissions pathways largely outcome/trajectory); v1.2 methodology (Nov 2025); **v2.0 overhaul in progress** (consultation closed Jan 2026, results imminent — build against v1.2 now per decision, re-sync at v2.0). Data access is **email-gated — requested 2026-07-21, awaiting reply**; pipeline build proceeds on receipt. Note: ascor.org is legitimate (TPI Ltd); ascorproject.org has lapsed to a squatter — do not use.
- **ND-GAIN — DROP from C12 scoring** (reverses an earlier "use readiness not governance" note). Under the governance lens, ND-GAIN *readiness* (economic + social) is **fundamentally an adaptive-capacity / development measure** (wealth, infrastructure, education) where governance is at most a weak distal factor — it fails construct validity for governance, not merely on wealth-correlation. ND-GAIN *governance readiness* is WGI-repackaged (double-counts C4/C14/C18). ND-GAIN *vulnerability* is physical exposure, not governance. Vulnerability may be retained only as unscored context, if at all.
- **EPI — decompose at Step 1:** use policy/governance-relevant sub-components, not pure environmental-outcome sub-components (e.g. air-quality levels driven by geography/industry mix). (See existing EPI cross-sectional note.)

### C10 split / state-control un-deferral via V-Dem v2clstown (2026-07-21)
Decided in working session. Assessment of whether V-Dem **v2clstown** ("State ownership of economy": does the state own or directly control important sectors of the economy?) un-defers Concept 10.
- **Coverage — PASS.** 179/179 in the latest year (2025), complete and annual back through at least 2021; interval-scored via the V-Dem measurement model (range approx. -4.15 to 2.98). Decisively clears the ~50-country threshold that the OECD SOE sources (OECD SOE Guidelines reviews, Corporate Governance Factbook, iSOEF) failed — the original deferral reason.
- **Construct — SPLITS the concept.** The question captures state *ownership or direct control* of economic sectors — the **extent of state control / state economic footprint**. It does NOT measure **SOE governance quality** (board independence, hard budget constraints, competitive neutrality, transparency). Since v2clstown scores extent-not-quality, keeping the two dimensions merged would make the concept score misrepresent what it measures (construct-validity failure).
- **Decision: partial un-defer.** *State control over the economy* → LIVE in v1 (Concept 10, scored via v2clstown). *SOE governance quality* → split out, remains deferred to v2 (moved to future-enhancements list; not separately numbered). Headline inventory unchanged (25 unique / 29 instances); all 25 now scored.
- **Open items:** (1) **Directionality [evidence-resolved 2026-07-21]** — more control = worse, scored **monotonically/linearly, no threshold.** The "non-monotonic" hypothesis was tested against the WGI 6-dim governance composite (n=166, latest year) and rejected: Pearson +0.42 ≈ Spearman +0.41, quadratic adds R² +0.005 (no curvature). Signal is **moderate** (r ≈ 0.42, R² ≈ 0.18) — valid but noisy, reinforcing the single-indicator flag and modest weight. Wealth-loading **low** (r ≈ 0.25 vs log GDP/capita USD) — not a wealth proxy. Folds into the framework-wide D3 sign-pass for consistency; sign/shape settled. (2) **Single-indicator thinness** — one indicator trips the <3-indicator weight-review flag (§8 / D5); may pair a second state-footprint source (IMF GFS Public Corporations, Fraser government-enterprises) at Step 1, coverage permitting. (3) **Placement note:** V-Dem locates v2clstown under Property Rights (3.9.4), reflecting an economic-freedom lens; used here for the state-control construct.

### ASCOR composite specification (2026-07-22, revised after building)
TPI Centre (LSE) sovereign climate assessment. 85 countries, 3 rounds (2023/25, 2024/70, 2025/85), 43 live Yes/No indicators in 14 areas. ASCOR publishes **no composite** — the framework builds its own. Pipeline: `40_ascor_pipeline.ipynb`.

**Scored metric — 5 equally-weighted areas, the ones EVERY country answers:** `EP.1` emissions trends, `CP.1` climate legislation, `CP.5` adaptation, `CP.6` just transition, `CF.3` transparency in climate spending. Each area = share of its applicable (Yes/No) indicators answered Yes; Exempt / Not applicable / No data excluded from denominators (the data records "not assessed", not "absent" — India is Exempt on the energy-efficiency question and has an energy-efficiency law). Fixed **0–1 anchor**, entered under the §5 **fixed-anchor** family, passed through unnormalized.

**Why only 5 of 9 candidate areas.** ASCOR **deliberately asks different questions of different income groups** — methodology Appendix 1, "Exemptions by country group", implementing common-but-differentiated-responsibilities. Its "LI" group (WB lower-middle + low income; 14 countries here) is blanket-exempt from carbon pricing, fossil fuels and sectoral transitions. Separately, **UNFCCC developed** countries are exempt from transparency-in-climate-costing (the Paris Agreement doesn't require them to disclose finance needs) — criterion is UNFCCC status, not income, which is why 14 high-income countries still answer it. Areas differ sharply in difficulty (fossil fuels mean 0.22; costing transparency 0.61), so scoring each country on its own set compresses a real 0.108 governance gap to 0.023 and **inverts the income ordering** (lower-middle above upper-middle). The 5 universal areas are comparable by construction; verified 5/5 areas present for all 180 panel rows.

**Diagnostic retained, not scored:** `ascor_full_diagnostic` (9 areas, renormalized over present areas) is in the clean file for the evidentiary layer and Step-4 checks. Rank correlation with the scored metric ≈ 0.94.

**Never used:** `CF.1` international climate finance (donor-only, 63 of 85 exempt); `CF.4` renewable energy opportunities (no Yes/No indicators); `EP.2`/`EP.3`/`EP.4` targets (discriminating variance is ambition-benchmarking against a 1.5°C fair share, not governance quality — five of their indicators sit at 2–6% Yes).

**Correction to the earlier entry:** it claimed duplicate indicator codes (`CP.2.c` ×4, `CF.1.b` ×3) "would quadruple-count one carbon-pricing question" and required deduplication. **Wrong** — those columns are entirely empty (superseded question versions retained as columns), so they self-exclude under the applicable-response filter. No dedup step is needed; the pipeline reports them for visibility only.

**ASCOR is already wealth-adjusted by design** — the income-group exemptions ARE an income adjustment. **First confirmed entry for the wealth-adjustment audit**: applying a framework-level income adjustment on top would double-credit poorer countries. (Contrast ND-GAIN, which explicitly excludes GDP/capita to avoid double-penalising.)

**Known characteristic, Step-4 face validity:** three of the five scored areas (adaptation planning, climate budget tagging, rights conventions) are donor-supported activities in aid-receiving countries, so some low-income countries score above the high-income median (Kenya 0.700, Uganda 0.687, vs 0.583). The metric records that a plan exists, not that the state produced it autonomously.

**Tier: P2 provisional** — 85 countries = 44% of the 192-sovereign core (below the 60% threshold: flags for review, not auto-drop); 35 non-high-income, Sub-Saharan Africa 6, South Asia 4. Confirm at Step-1.

**Other:** momentum computable for only 25 of 85 (needs ≥3 rounds). CC BY-NC 4.0 — non-commercial, flagged for the licence audit. v1.2 methodology; v2.0 overhaul in progress (consultation closed Jan 2026) — pipeline Cell 4 fails loudly if area codes stop resolving.

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
1. **IMF AREAER FARI (BUILT, manual).** The Financial Account Restrictiveness Index (capital-account restrictiveness, de jure, 0-1 higher=more restrictive) is exported by hand from the portal's Indices tab. Built notebook 32. fari_aggregate + fari_fdi_aggregate are PRIMARY scored fields (both C8 P1). Step-1 (2026-07-23) ALSO scored fari_fdi_inflow at C8 P1 (full weight) - a deliberate, documented partial double-count with fari_fdi_aggregate to tilt C8 toward INBOUND capital access, which matters more to a sovereign investor than outbound. The outflow splits are DROPPED, not scored (outbound access is less material). Direction is a D3 item (restrictiveness is a policy stance, not self-evidently a governance quality). 194 countries, 1999-2024 (2024 partial per source). This is the IMF-NATIVE authoritative measure. MANUAL SNAPSHOT — refreshed by re-exporting each cycle. Direction validated (Hong Kong 0.02 / Singapore 0.05 open; Bangladesh 0.77 closed). The FDI sub-index is a genuine advantage over derivative indices (which collapse to a single number and cannot isolate FDI).
2. **Chinn-Ito KAOPEN (BUILT, automated — notebook 31).** The most-cited academic capital-account-openness index, derived from the SAME AREAER source data, freely downloadable (web.pdx.edu/~ito, year-stamped file, URL parsed dynamically — no hardcoded year). 182 countries (181 valid-ISO3 + ANT dead-code retained; Serbia/Timor present in source but unscored → dropped; ZAR→COD remap), 1970-2023. `kaopen` (raw PCA, higher = MORE open — **OPPOSITE sign to FARI**) primary; `kaopen_norm` (0-1) supplementary. NOT more authoritative than AREAER — it is a derivative; used as the automatable broad-time-series complement / cross-check. Fragile personal-page URL flagged (fallback in instructions_data_maintenance.md). ⚠ **Version non-stable:** each release recomputes the PCA over the whole sample → full-replace, never append. Needs `xlrd` engine for the legacy .xls.
3. **Exchange-rate-regime dimension (de facto) — sourced from AREAER's own classification; BUILT (manual transcription, notebook 37).** The IMF AREAER publishes a *de facto* exchange-rate-arrangement classification (annual, current to April 30 2025, 195 jurisdictions) — the IMF-native current-state primary for the ER-regime dimension that FARI/KAOPEN (capital-account) do not cover. AREAER Online is paywalled and the published table (IMF Annual Report 2025 Appendix II.9) is a **borderless 2-D matrix** (monetary-policy-framework columns × ER-arrangement rows) with currency unions collapsed into cells, footnote superscripts and reclassification dates — `extract_tables` finds no grid, so a coordinate parse would be fragile and re-break each edition. **Build-vs-manual decision: hand-transcription is materially more reliable and no more time-consuming here**, because the PDF states per-category (row) AND per-column (MPF) country counts — built-in checksums that make transcribe-then-validate robust. A hand-maintained source CSV (`data/raw/areaer_defacto_regime.csv`), validated at transcription against all row + column checksums (all pass, 2025 vintage), is read by an automated pipeline (`37_areaer_defacto_er_pipeline.ipynb`) → `areaer_er_clean.csv`. Fields: `areaer_arrangement` (10-way) + `areaer_regime_ordinal` (1–10 flexibility, matrix order) + `areaer_regime_group` (IMF 4-way; **`other_managed` is a RESIDUAL, not a flexibility rank** — flag for metric pass) + `areaer_mpf` (monetary-policy framework incl. **inflation-targeting flag**) + `areaer_anchor_currency` + `areaer_reclassified` (YYYY-MM regime-change recency). Cross-section snapshot; NO year (vintage = `areaer_as_of`, data-derived — no hardcoded date). Annual refresh = re-transcribe only reclassified countries + bump `areaer_as_of` in the source CSV, then re-run (no code changes); see instructions_data_maintenance.md. **Reinhart-Rogoff demoted to supplementary**: data ends ~2019 (≈7-yr stale, worst in the stressed-EM cases where regime classification matters most); retained only as an independent, parallel-market-aware cross-check / historical layer, not the primary.

**ACI (AREAER Change Index)** was also downloaded (companion file) but NOT built into the score: it measures policy *changes* (tightening/easing actions, a direction-of-travel signal), a different construct from FARI's *level* of restrictiveness. Deferred as optional supplementary (on hand if a policy-trajectory dimension is later added).

### WB BRSS — bespoke construct-aligned banking-supervision stringency (Barth-Caprio-Levine)
**Supplementary is a STALENESS judgment, not a peripherality one [recorded 2026-07-23].** BRSS banking prudential regulation is CENTRAL to Concept 9, not peripheral — it is the concept’s only non-AML, only-prudential measure (FATF, both axes, is AML/CFT). BRSS sits at Supplementary purely because the 2016 reference vintage is too stale to drive a current score (post-2016 Basel III phase-in and resolution reforms), while remaining useful evidentiary context since bank-rule frameworks are sticky. Were it judged current-enough it would be P2. Do not read the low tier as a low-importance judgment or a reason to drop it. Scoring uses `brss_regstringency` (the overall index); the 9 sub-constructs are its components (decompose-or-keep-whole → keep the total).
Source: World Bank **Bank Regulation and Supervision Survey (BRSS)** — the Barth-Caprio-Levine survey the
master lists as Concept 9's supplementary banking source, now BUILT (nb 38, `wb_brss_clean.csv`). 5th wave
(fielded 2017, released 2019; **reference year 2016**, derived from the question codes — not hardcoded).
SUPPLEMENTARY tier. Fills the banking-regulation *de jure* leg that FATF (AML/CFT) does not cover. CC-BY-4.0.
Auto-discovers the latest `.xlsx` from the permanent WB catalog page (dataset `0038632`); the flagged
constants are `BRSS_CATALOG_URL` (Cell 2) and `CACHE_YEAR` (Cell 4, the new-wave detection sentinel that must be bumped to adopt a new wave). Note the reference year (2016) IS derived from the question codes; it is the cache/wave year that is hand-set.

**What it measures — and what it does NOT:** a **de jure regulatory-STRINGENCY** score (rules on paper), NOT
supervisory effectiveness/implementation. Advanced economies scoring mid-pack is CORRECT and expected (top of
the reliable ranking: Nigeria, Qatar, Slovenia); validated against Anginer et al. (2019), whose
high-income/developing directional pattern this reproduces with zero construct inversions. FSAP's BCP
assessment (effectiveness) and IOSCO/IAIS (securities/insurance) remain the un-built complements.

**Method — bespoke construct-aligned select-and-score (explicitly NOT the published BCL indices;** the
2019-wave question-to-index mappings are not cleanly available). The workbook is raw survey responses across
15 topic sheets in transposed layout (questions as rows, countries as columns), no pre-computed indices.
Curated comparable, high-coverage (≥80% per-item) directional questions → **9 sub-constructs, 56 scored
items** (67 underlying question codes; two are multi-question blocks scored as one — a 9-item
Tier-1-deductions *fraction* and a 4-item borrower-based-caps *any*). Each item Yes/No→1/0 or numeric
min-max normalized, sign applied, averaged (over ANSWERED items) into the sub-construct.
- **Sub-constructs (9):** supervisory power · supervisory independence · capital stringency · private
  monitoring · resolution regime · provisioning · liquidity/concentration · macroprudential · supervisory capacity.
- **Reverse-coded (5):** `Q12_3` (deposit-takers outside prudential supervision), `Q12_12`/`Q12_13`
  (personal/agency liability → weaker independence protection), `Q9_5`/`Q9_6` (lax income recognition /
  immediate upgrade). Verified against parent question text.
- **Activity Restrictions DROPPED** — contested directionality (more restriction ≠ better; literature split).
- **Provisioning & macroprudential TRIMMED** of prescriptive-rule items that penalize IFRS-9 / expected-loss /
  principle-based regimes (dropped `Q9_9`, `Q9_12`, `Q12_26`) — avoids de-jure "stringency inflation" that
  would mis-rank principle-based supervisors as weak.

**Aggregation (a documented departure from equal-weight):** equal-weight WITHIN each construct; the overall
`brss_regstringency` headline is a **weighted** mean of the 9 constructs — **5 weighted 2× (supervisory power,
independence, private monitoring, resolution, macroprudential); 4 weighted 1× (capital stringency,
provisioning, liquidity, capacity).** The 2× set is the supervisory-*governance*
dimensions (powers, independence, market discipline, resolution, systemic oversight); the 1× set is the
technical-calibration dimensions — reflecting the framework's tiering principle (centrality to the
concept, not just data quality). Weights renormalize over PRESENT constructs so missing data doesn't zero
the headline.
- **NO coverage penalty:** scores are the mean of ANSWERED items (missing ≠ weak); coverage is emitted
  separately as a flag rather than deflating the score.
- **Reliability:** `brss_reliable = per-country coverage ≥ 70%` (`RELIABILITY_MIN_COVERAGE`, a flagged
  methodology constant in the gap between the sparse ≤60% tail and the ≥85% mass; revisit post-v1).
  **161 jurisdictions scored, 155 reliable**; 6 flagged out (Comoros, DRC, Eswatini, Euro Area, Montserrat,
  Turks & Caicos). Score still emitted for all; exclusion is downstream.

**Output:** cross-section, `country_code`-keyed, NO `year`, NO `country_name` (house convention; re-attached
at merge). 13 cols = country_code + 9 sub-scores + `brss_regstringency` + `brss_coverage` + `brss_reliable`.

**Update = MANUAL check for a 6th wave** (frozen, irregular survey: 2001/03/07/11/19, no cadence — will NOT
auto-refresh). If a 6th wave posts, the catalog auto-discover picks up the new `.xlsx` automatically, but
`INCLUDED_QUESTIONS` must be re-validated (renumbering/rewording) — Cell 5 auto-derives the year suffix and
**fails loudly** listing any code that no longer resolves. See instructions_data_maintenance.md.

## Source Registry Architecture (build-truth model)

`data/processed/source_registry.csv` is the **authoritative, build-time record** of each source's access method, approach, and notes. It is written by two mechanisms, and the model matters:

- **`02_source_registry.ipynb` cells 1–2 (the seed list)** = *decision-time intent*. Hardcoded dicts from the original source-decision pass, with first-guess access methods (`bulk_download`, `api`). ~48 of ~68 entries are deliberately stale relative to the CSV — builds revealed the real access path (e.g. many sources turned out subsumed in bundle pipelines → `via_qog`/`via_wdi`, or gated → `manual_download`).
- **Per-pipeline updates + `02` cells 4–41** = *build-time truth*. Each built source's correct row is written by its own pipeline's registry cell (e.g. nb 35 for FATF) and/or a targeted `.loc` patch cell in `02`. These are authoritative.

**The CSV is the source of truth; the seed is historical intent. They are expected to diverge.** Do **not** rely on re-running `02` end-to-end to "refresh" build-status — it does not re-derive anything; cells 4–41 are a static correction layer.

**Clobber guard (fixed):** `02` cell 3 previously did an unconditional `to_csv`, overwriting the whole CSV from the seed and wiping pipeline-written corrections (this happened live once — FATF reverted `manual_download` → `tier2_structured`). Cell 3 is now a **non-destructive merge**: existing CSV rows are preserved untouched; only seed rows for genuinely-absent `source_id`s are added. First-ever run still writes the full seed.

### Potential improvement (NOT a task; not required for production)

Cells 4–41 each rewrite the whole CSV via targeted `.loc` patches. They touch only their own named source (cannot clobber other rows), so this is **not a blocker and not a running task item** — the catastrophic failure mode (cell 3's all-rows overwrite) is already fixed. The residual edge case: if a source's access method changes *after* its correction cell was written, and that cell isn't updated, re-running it would re-apply the stale value — bounded to one row, visible in git, trivially recoverable. **Verdict: does not block production.** The clean-architecture alternative (fold all corrections back into the seed, delete cells 4–41) is a larger refactor pursued only if `02` is ever wanted as a single-pass regenerator — optional, low value under the build-truth model.

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
| 31_chinn_ito | Chinn-Ito (KAOPEN) | chinn_ito_clean.csv | 2 (kaopen raw + kaopen_norm 0-1) | 1970-2023 panel, 182 countries (181 ISO3 + ANT) |
| 32_areaer_fari | IMF AREAER (FARI) | areaer_fari_clean.csv | 6 (aggregate + FDI aggregate + 4 inflow/outflow splits) | 1999-2024 panel, 194 countries |
| 37_areaer_defacto_er | IMF AREAER (de facto ER regime) | areaer_er_clean.csv | 6 (arrangement + flexibility ordinal 1–10 + IMF group + MPF/IT-flag + anchor + reclassified) | cross-section snapshot, 195 jurisdictions (as-of 2025-04-30) |
| 38_wb_brss | WB BRSS (Barth-Caprio-Levine) | wb_brss_clean.csv | 9 sub-construct scores + weighted headline + coverage + reliable flag | cross-section, 161 juris (2019 wave, ref yr 2016); 155 reliable |

---

## Consolidated Build Status (by source)

**As-of: 2026-07-09. MANUAL SNAPSHOT — does not auto-update.** Single at-a-glance view of every source's status. Authoritative structured records remain `download_log` (currency/filenames) and `source_registry.csv` (access methods). Legend: ✅ Built · ⏳ Next/in-progress · ⏸ Deferred (access pending or v2) · ❌ Deprioritized · 🔒 Blocked-not-built.

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
| Chinn-Ito (KAOPEN) | ✅ | Automated scrape | chinn_ito_clean.csv (182 countries, 1970-2023); capital-account derivative/cross-check of AREAER FARI; ⚠ version non-stable → full-replace |
| IMF AREAER (de facto ER) | ✅ | Manual transcription (checksum-validated) | areaer_er_clean.csv — ER-regime primary; 195 juris, as-of 2025-04-30; BUILT nb 37 (borderless matrix hand-transcribed; row + column checksums pass) |
| WB BRSS (Barth-Caprio-Levine) | ✅ | Automated (WB catalog auto-discover) | wb_brss_clean.csv — Concept 9 banking-reg *de jure* leg, SUPPLEMENTARY; bespoke construct-aligned stringency (NOT published BCL indices); 161 juris (155 reliable), 2019 wave; BUILT nb 38 |
| Reinhart-Rogoff | ⏸ | Manual/academic | DEMOTED to optional supplementary cross-check (data ends ~2019); not a primary |
| PEFA | ✅ | Manual download (structured CSV) | pefa_clean.csv — Scores Downloads (NOT PDF); 2016/national/latest-per-country (85 ctry, 31 ind, 2017–2026); 2011 deferred (stale) |
| OECD TFI | ✅ | Manual download (CYC Overview table) | tfi_clean.csv — **composite average** (0–2), 164 countries, 2017/2019/2022. Sufficient: admin triangulation real (LPI built in wdi_clean + TFI; WTO TFA dropped — licence). A–K sub-indicators = future enhancement (CYC one-at-a-time; PDF-annex route), NOT a to-do. TAD email moot. |
| UNCTAD NTM | ❌ | WITS bulk CSV available, but data stale | DROPPED — currency. Latest cross-country vintage 2012-2017 (staggered, 9-14 yr old), ~76 countries. Too stale/thin for a primary even at low weight. NTBs = accepted v1 gap. WITS route works if UNCTAD ever refreshes. |
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

**Category 1 PDF-extraction sources (not started):** IMF FSAP, plus multi-source infrastructure (IMF Article IVs + WB CCDRs, political-economy/institutional focus). _(IMF AREAER de-facto ER removed — now BUILT via checksum-validated manual transcription, `37_areaer_defacto_er_pipeline`, not a PDF parse. PEFA removed — structured "Scores Downloads" CSV, BUILT as manual-download `33_pefa_pipeline`. ICNL removed — HTML country notes, supplementary `tier3_web`.)_
**Category 3 web scrapes:** IPU PARLINE, IMF SDDS (not started). _(FATF built nb 35; CPJ built nb 36 — both were listed here in error. WTO TFA dropped — licence, not a scrape target.)_


## Build-Status by Concept (verified audit)

_Verified 2026-06-24. Reconciles each concept's primary sources against actual processed files. **Verification basis:** the 8 multi-source *bundle* files — WDI, Fraser, QoG, V-Dem, WJP, FSI, FH-FIW (columns inspected directly) + IDEA-GSoD (build-log) — are file-verified, so "source hidden inside a bundle" cases (e.g. LPI lives in `wdi_clean`) are caught. The ~22 single-source standalones are **build-log-trusted** (no subsumption risk). Source location is shown in italics (which file each lives in)._

**Buckets:** ✅ Built (pipeline exists, data in processed files) · 🟡 Outstanding (needed, not built) · ⚪ Closed (dropped / superseded / proxied).
**Evidence tags on Outstanding** (the "why incomplete"): `parked` = probed, cost known, deferred/blocked · `classified, unprobed` = labelled by a prior pass on assumption, access never actually tested (**TFI and NTM were here and both turned out accessible — quick-win candidates**) · `unexamined` = bare concept-table entry, no access investigation at all.

| Concept | Status |
|---------|--------|
| **1 · Political settlement** | **✅ Built:** V-Dem power-distribution *(vdem)* · FSI Factionalized Elites *(fsi c2)* · FSI Group Grievance *(fsi c3)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** — |
| **2 · Political stability & regime durability** | **✅ Built:** WGI Pol. Stability *(wgi)* · V-Dem regime data *(vdem)* · Powell-Thyne coups *(powell_thyne)* · UCDP *(ucdp)* · GPI *(QoG)* · WJP F5 *(wjp)*<br>**🟡 Outstanding:** ACLED `[parked: research-API approval pending]`<br>**⚪ Closed:** — |
| **3 · Statistical & informational infrastructure** | **✅ Built:** WB SPI *(spi_clean)* · ODIN *(odin_clean)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** IMF SDDS (tier-2) *(dropped — redundant with SPI + ODIN, which cover the dissemination/transparency facet continuously and, for ODIN, with independent audit; SDDS is a coarse ~4-level ordinal, partly self-reported. Re-entry: cheap public DSBB source if a de jure commitment signal distinct from de facto capacity is later wanted.)* |
| **4 · Government effectiveness & admin quality** | **✅ Built:** WGI Govt Effectiveness *(wgi)* · V-Dem v2clrspct *(vdem)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** — |
| **5 · Service delivery & public goods** | **✅ Built:** WDI sector indicators *(WDI)* · WB Human Capital Index *(WDI)* · FSI Public Services *(fsi p2)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** WHO GHO *(subsumed by WDI — physicians/nurses/beds/UHC all WDI series; GHO OData API deprecated)* · UNESCO UIS *(subsumed by WDI — expenditure + pupil-teacher series are WDI codes; deeper UIS learning data = future enhancement, not v1 gap)* · UNDP HDI sub-indicators *(subsumed by WDI — life expectancy + GNI are core WDI series; use sub-indicators not composite)* |
| **6 · Regulatory quality** | **✅ Built:** WGI Regulatory Quality *(wgi)* · WJP F6 Reg. Enforcement *(wjp)* · Fraser Regulation area *(fraser)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** Heritage Business Freedom *(superseded by Fraser Regulation — same dimension, both tier-2; house overlap rule prefers Fraser (peer-reviewed, transparent weights) over Heritage (advocacy framing), as already applied to Heritage Trade & Property)* |
| **7 · Public financial management (PFM)** | **⛔ RETIRED / FOLDED INTO C8 (2026-07-24).** PFM is now scored under Concept 8 (rescoped to design AND management of macro-policy institutions). Number 7 is a vacant stable ID; C8–C25 unchanged; inventory 25→24. OBS moved C7→C8 (scored). PEFA still to be scored into C8 (pillar-aggregate selection pending). See changelog. |
| **8 · Macroeconomic policy framework quality** (now incl. PFM, folded from C7) | **✅ Built:** Romelli CBI *(QoG)* · IMF Fiscal Rules *(imf_fiscal_rules)* · AREAER FARI *(areaer_fari)* · Chinn-Ito KAOPEN *(chinn_ito)* · IMF iMaPP *(imapp)* · AREAER de-facto ER *(areaer_er, nb 37)* · Open Budget Survey *(QoG obs, folded from C7)*<br>**🟡 Outstanding:** PEFA *(pefa_clean, BUILT pipeline but NOT yet scored into selection — pillar-aggregate metric selection pending)*<br>**⚪ Closed:** — |
| **9 · Financial-sector regulatory & supervisory quality** | **✅ Built:** FATF Mutual Evaluations *(fatf_clean)* — AML/CFT, 199 countries · WB BRSS *(wb_brss, nb 38)* — banking-regulation *de jure* stringency, SUPPLEMENTARY, 161 juris (155 reliable)<br>**🟡 Outstanding:** IMF/WB FSAP `[verified PDF-only (scouted) — narrative FSSA/FSA/DAR reports, no structured cross-country dataset; voluntary/irregular publication; PDF-extraction batch — banking *de jure* reg leg now partly filled by WB BRSS (nb 38); FSAP residual marginal value = securities (IOSCO) + insurance (IAIS) + supervisory *effectiveness*]` · BCP / IOSCO / IAIS `[NOT separate sources — they are the banking/securities/insurance Detailed Assessment Reports embedded WITHIN FSAP; collapse into the FSAP PDF-batch]` · Basel AML Index `[parked: requires institutional affiliation; largely synthesises FATF (now built) — partly redundant]`<br>**⚪ Closed:** — |
| **10 · State-owned enterprise governance** | **✅ Built:** —<br>**🟡 Outstanding:** — entire concept DEFERRED TO v2 (thinnest concept; out of v1 scope)<br>**⚪ Closed:** — |
| **11 · Trade governance** | **✅ Built:** WB LPI *(WDI)* · OECD TFI *(tfi_clean)* · WB tariffs *(WDI)* · Fraser Trade *(fraser)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** WTO TFA *(dropped — licence: WTO material requires written permission for commercial use, conflicting with the framework's commercial/investment purpose (IPU-Parline precedent). Access is NOT the blocker — a bulk Notifications Matrix XLSX now exists (tfadatabase.org); the licence is. Admin already triangulated via LPI + TFI; TFA is self-reported commitment, not performance.)* · KOF Trade *(proxied via QoG kof_economic_globalisation (combined trade+financial, not pure trade subindex))* · Heritage Trade Freedom *(superseded by Fraser Trade)* · UNCTAD NTM *(dropped — currency (2012-2017, ~76 ctry))* |
| **12 · Environmental & climate governance** | **✅ Built:** Yale EPI *(epi_clean)* · Climate Laws *(climate_laws)* · ND-GAIN *(QoG)* · IRENA capacity *(irena)* · WB Carbon *(wb_carbon)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** — |
| **13 · State capacity (structural core)** | **✅ Built:** V-Dem state authority *(vdem)* · FSI Security Apparatus *(fsi c1)* · ~~WB Informal Economy~~ *(EXCLUDED at Step-1 2026-07-23 - 0.0% current sovereign coverage, series ends 2020; Hanson-Sigman likewise excluded, ends 2015. C13 now scores on 3 metrics from 2 sources: V-Dem x2 + FSI)*<br>**🟡 Outstanding:** ILO social security (tier-2) `[unexamined — WDI social-protection cols may cover; confirm]`<br>**⚪ Closed:** — |
| **14 · Legal quality & predictability** | **✅ Built:** V-Dem v2cltrnslw/v2clacjstm/w/v2xeg_eqaccess *(vdem)* · WJP F4 Fundamental Rights *(wjp)* · WJP F3 Open Govt *(wjp)* · CCP legal features *(QoG ccp — civil-rights/equality/info-access)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** — |
| **15 · Judicial independence & quality** | **✅ Built:** V-Dem judicial v2juhcind… *(vdem)* · WJP F7 Civil Justice *(wjp)* · WJP F8 Criminal Justice *(wjp)*<br>**🟡 Outstanding:** CCP judicial-independence features `[QoG CCP extract has no judicial column (only govt-system/market/rights/info/equality); V-Dem+WJP cover the concept]`<br>**⚪ Closed:** — |
| **16 · Personal security & order** | **✅ Built:** UNODC Homicide *(unodc)* · V-Dem v2cltort/v2clkill/v2clrgunev *(vdem)* · Political Terror Scale *(QoG pts)* · WJP F5 *(wjp)* · GPI societal safety *(QoG)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** — |
| **17 · Property rights & contract enforcement** | **✅ Built:** V-Dem property v2clprptym/w/v2xcl_prpty *(vdem)* · WJP F6.5 No-expropriation *(wjp)* · Fraser Legal-System area *(fraser)* · WIPO IP — partial *(WDI patents/trademarks)*<br>**🟡 Outstanding:** CCP property provisions `[QoG CCP extract has no property column (market_economy ≠ property); V-Dem property covers]`<br>**⚪ Closed:** Heritage Property Rights *(superseded by Fraser/WJP/V-Dem (documented))* |
| **18 · Control of corruption** | **✅ Built:** V-Dem corruption v2x_corr… *(vdem)* · TI CPI *(ti_cpi)* · WJP F2 Absence of Corruption *(wjp)* · Bayesian Corruption Indicator *(QoG bci)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** — |
| **19 · Legislative & constitutional checks** | **✅ Built:** V-Dem v2xlg_legcon + components *(vdem)* · ~~CCP separation-of-powers~~ *(ccp_government_system EXCLUDED at Step-1 - no variance, 188/4 split)* · ~~Polity5 XCONST~~ *(EXCLUDED - series ends 2018, fails 4-yr recency; XCONST was never in the QoG extract regardless)*. **KNOWN LIMITATION: C19 is now SINGLE-SOURCE (V-Dem only, 5 metrics)** - both non-V-Dem legs died at Step-1 (Polity recency, CCP variance). Permanent for v1; surfaced for the correlation-aware weighting item*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** IPU Parline *(dropped from v1 — scouted: free open REST API at `api.data.ipu.org`, 193 countries, BUT licensed **CC BY-NC-SA (non-commercial only)**, which conflicts with the framework's commercial/investment purpose; also largely redundant with V-Dem v2xlg_legcon + CCP + Polity for legislative checks. Access route recorded; not a pending task)* |
| **20 · Electoral process & competition** | **✅ Built:** V-Dem electoral v2x_polyarchy… + EMB autonomy/capacity v2elembaut/v2elembcap *(vdem, nb 03)* · FH-FIW Electoral Process (PR-A) *(fh)* · Electoral Integrity (PEI) *(QoG)* · NELDA *(QoG)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** IDEA EMB Database *(deprioritized — EMB independence/capability leg now filled by V-Dem v2elembaut/v2elembcap (functional, clean directionality, nb 03); IDEA EMB's unique content is a de jure model taxonomy with contested directionality (Independent ≠ better). IDEA's own GSoD EMB-autonomy indicator is V-Dem v2elembaut re-served.)* |
| **21 · Political participation beyond voting** | **✅ Built:** V-Dem participation v2x_partip… *(vdem)* · CIVICUS *(civicus)* · IDEA GSoD Participatory *(idea_gsod — build-log)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** — |
| **22 · Civil liberties** | **✅ Built:** FH-FIW CL-D & CL-G *(fh)* · V-Dem civil liberties v2x_civlib… *(vdem)* · Pew GRI + SHI *(pew_gri - both confirmed present and scored C22 P2 at Step-1)* · Political Terror Scale *(QoG pts)* · WB Women Business & the Law *(WDI wbl)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** — |
| **23 · Media freedom & pluralism** | **✅ Built:** V-Dem media v2x_freexp_altinf… *(vdem)* · FH-FIW CL-D *(fh)* · RTI Rating *(rti_rating)* · CPJ journalist-safety *(cpj_clean)* - Step-1 scores cpj_imprisoned (P1) + cpj_murders_unsolved (P2) only; cpj_murdered_confirmed DROPPED (conflict-contaminated - Israel/OPT alone is 32 of 99). Zero-filled to the spine (global census, absence = verified zero), so UNIVERSAL coverage, not 50<br>**🟡 Outstanding:** —<br>**⚪ Closed:** RSF World Press Freedom Index *(dropped — V-Dem covers; methodology break)* |
| **24 · Civil society space & vitality** | **✅ Built:** V-Dem CSO v2cseeorgs… *(vdem)* · CIVICUS *(civicus)* · FH-FIW CL-E Associational *(fh)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** — |
| **25 · Government transparency & openness** | **✅ Built:** V-Dem v2cltrnslw/v2dlconslt *(vdem)* · WJP F3 Open Govt *(wjp)* · RTI Rating *(rti_rating)* · Open Budget Survey *(QoG obs)* · IDEA Political Finance *(polfinance)*<br>**🟡 Outstanding:** —<br>**⚪ Closed:** — |

**C9 THINNESS CORRECTION [2026-07-24]:** earlier notes (incl. the BRSS commit) said C9 "now has 3 metrics, clears the thin flag." WRONG - the S6 weight-review trigger counts PRESENT P1+P2 indicators, and BRSS is Supplementary (weight 0). C9 has 2 scored indicators, BOTH FATF, so it remains THIN and is additionally SINGLE-SOURCE (rests entirely on AML/CFT). This is the §6 case that gets a qualitative weight review at Step-1, where promoting BRSS to a scored weight is an explicit option (live, given BRSS is central-but-stale). BRSS being Supplementary was still correct on staleness; only the "clears the flag" claim was wrong.

**Headline:** ~11 concepts fully built; most of the rest are tier-1-complete with gaps only in 3rd/supplementary legs. **Concept 9 (financial-sector regulatory quality) remains among the thinnest concepts** (AML/CFT via FATF and banking-regulation *de jure* via WB BRSS, nb 38, now built; securities, insurance and supervisory *effectiveness* await FSAP), but its most accessible primary — FATF Mutual Evaluations — is now built (199 countries; the `classified scrape` verdict proved wrong, like TFI/NTM). Remaining Concept 9 sources are FSAP (PDF-batch, unprobed), Basel AML (affiliation-blocked), and BCP/IOSCO/IAIS (unexamined). The one remaining genuine tier-1 build gap is ACLED (C2, research-tier access pending); WTO TFA (C11) dropped on licence, IDEA EMB (C20) deprioritized (V-Dem EMB supersedes), IPU Parline (C19) dropped on licence, and CPJ (C23) built (nb 36). Remaining `classified/unprobed` scout targets (FSAP, IMF SDDS) are next — prior "hard" verdicts on TFI/NTM/FATF all proved wrong on inspection.


## Outstanding Decisions

### Metric-selection principle: decompose-or-keep-whole [recorded 2026-07-23]
When a source ships a composite AND its components, score ONE level, never both (scoring both double-counts: the components sum into the total). Which level:
- **Keep the source total** when its parts are facets of ONE construct that stand or fall together and the source aggregated them on a principled/standards basis. The framework adds nothing by re-weighting. Applied: `rti_total` (7 FOI-law categories = one legal-quality construct on the CLD international-standards weighting); `spi_overall`; `imapp_breadth_total`.
- **Decompose to components and equal-weight them yourself** when the parts are genuinely different sub-dimensions and the source’s internal weighting is arbitrary for the framework’s purpose — scoring the parent would outsource that weighting to the source. Applied: WDI service delivery (four sub-composites, else health = 41% of C5 purely on series count); Yale EPI issue-category level not the parent objectives (r=+0.90 nesting); FH sub-category totals.
- The two rules are consistent: score at the level where the framework, not the source, controls the sub-dimension weighting — which is the total when the source’s weighting is principled, the components when it is not.

### Metric-selection principle: type is not a quality ordering [recorded 2026-07-23]
A categorical CLASSIFICATION is not a quality scale and must not be scored directionally — there is no “better” end. A fixed exchange-rate regime is not worse governance than a float (HK peg vs ARG crawl); presidential is not worse than parliamentary; an autocracy’s regime code is not a low score. Excluded on this basis: `v2x_regime` (used instead to DERIVE regime duration, which is a quality signal), `areaer_regime_ordinal`/`areaer_arrangement`/`areaer_regime_group` (score the inflation-targeting flag instead — a rules-based framework IS defensibly better), `ccp_government_system`. Where a type plausibly maps to quality, derive the quality signal from it rather than scoring the type.

### Limits of the WGI-composite comparison [recorded 2026-07-23]
Several Step-1 blocks were checked by correlating each candidate metric against a 6-dimension WGI composite. **That comparison is valid for DIRECTION and for wealth-loading comparison. It is NOT a test of whether something is governance, and its magnitude must not drive inclusion or tier.**

- **Why it works for direction:** asking which way a variable runs is separable from asking what it measures. This caught a real error - V-Dem’s individual corruption items are coded higher = LESS corrupt while only the `v2x_corr` index is reverse-coded, so asserting the family sign from the codebook would have inverted four of C18’s five V-Dem metrics.
- **Why magnitude is circular:** if WGI were an adequate measure of governance, this framework would be redundant. Treating WGI agreement as the criterion privileges WGI’s implicit construct over the one the framework specifies, and penalises exactly the dimensions WGI omits. WGI has no environmental component, so a low correlation for an EPI sub-index cannot distinguish “not governance” from “environmental governance WGI does not measure.”
- **Correction applied:** EPI sub-indices were briefly demoted to P2 on low WGI correlation; that demotion was withdrawn. `epi_agr` and `epi_wrs` restored to P1 per the master. `epi_bdh` remains P2 on an independent basis (internal comparability - marine components absent for ~27% of countries). Tier priors come from the master and are refined on construct and measurement-quality grounds, never on correlation with another index.

### Reference-class distortion in normalization [recorded 2026-07-22]
Distributional normalization (z, log-z, percentile) scores a country against the reference distribution of **whichever countries happen to be measured**. Where an indicator has **non-random coverage**, that reference class is unrepresentative and the resulting scores are distorted in the direction of the coverage skew. Worked example: ASCOR is advanced-economy-skewed (85 countries, 50 high-income), so a typical EM z-scores about 0.05 lower on a 0-1 scale than it would against a representative reference class - i.e. being *measured* becomes a disadvantage relative to being omitted. **PEFA runs the opposite way** (donor-driven, developing-heavy), so a developing country may score better against PEFA-s reference class than it would globally. Same mechanism, inverted sign.

**Step-1 check, per indicator:** is coverage plausibly representative of the 192-sovereign core? If not, prefer an **absolute / fixed-anchor** scoring where the data admits one (categorical Yes/No data, bounded indices with theoretical anchors) - see metric_methodology.md S5 fixed-anchor family. Where only distributional normalization is possible, record the skew direction as a known limitation of that metric.

### Metric-selection principle: construct validity (process AND outcomes) [recorded 2026-07-21]
For the Step-1 metric-selection pass, across all concepts:
- **Process and outcome indicators are both wanted.** Outcomes often proxy governance *better* than process, because process measures (laws/institutions on paper) frequently do not reflect how a country is actually governed. Do not prefer process over outcomes.
- **The test is construct validity:** does the indicator signal *governance quality*? Keep governance-signaling outcomes even when they also partly reflect development (e.g. service delivery) — flag the mixed ones, don't exclude them.
- **Wealth-correlation is NOT an exclusion criterion.** Governance and development are inherently correlated (good governance produces development; development enables governance), so nearly all good governance indicators correlate with wealth. Filtering on wealth-correlation would discard valid signal. Income-loading is handled downstream, once, by the planned wealth-adjustment layer — not by selection filtering.
- **Bar for exclusion is high and specific:** exclude only where an indicator is *fundamentally* measuring something other than governance (e.g. ND-GAIN readiness = adaptive/development capacity), with governance at most a weak distal cause. When genuinely ambiguous, **include** (possibly flagged / lower-tier) — a noisy governance proxy beats discarded signal, given the absence of clean direct governance measures.

**Licence audit before production (framework-wide).** IPU Parline surfaced a real issue: its data is free but **CC BY-NC-SA (non-commercial)**, conflicting with the framework's commercial/investment purpose — so it was dropped. Other sources may carry similar non-commercial or share-alike terms. A deliberate per-source licence audit (commercial-use permissibility, attribution/share-alike obligations) should run before production. Noted consideration, not yet a scheduled task.


- KOF_TRADE: separate KOF pipeline for trade sub-index vs accept dr_eg proxy — pending
- ACLED: complete once Research tier approved
- BASEL_AML: complete once Expert Edition access obtained
- Concept 25 (Government transparency): reconsider before finalizing — indicator overlap
- SOE Governance (Concept 10): deferred to v2
- EPI sub-components: select policy/institutional sub-components at metric pass
- IRENA renewable-energy TARGETS (national ambition signal, e.g. % renewable by year): a genuinely additive policy measure, but only available embedded in IRENA reports/NDC analysis — DEFERRED to the planned Category 1 PDF-extraction infrastructure, not a clean download
- RTI Rating HISTORICAL time series / transparency TRAJECTORY (is a country's RTI framework improving or backsliding): deferred — RTI scores are sticky step-functions so annual history adds little for a v1 cross-section, but a trajectory/direction-of-travel dimension (applicable to several de jure sources) could use it later
- iMaPP in-force precision: parse text records if current-stock needed (deferred)
- BRSS reliability threshold (0.70 coverage): revisit post-v1 (low priority) — sits between the ≤60% sparse tail and ≥85% mass; a metric-pass sensitivity check could confirm
- WGI standard errors: optional enhancement for ranking confidence — not a master-PDF gap, user discretion
- Category 3 web scrapes not built: IPU_PARLINE, IMF_SDDS (FATF built nb 35; CPJ built nb 36; WTO_TFA dropped — licence)
- Category 4 manual not built: none outstanding (ODIN, CLIMATE_LAWS, TI_POLFINANCE, RTI_RATING, OECD_TFI, IMF_AREAER de-facto ER [nb 37, checksum-validated transcription] built; IRENA_POLICY and GLOBAL_DATA_BAROMETER deprioritized; UNCTAD_NTM dropped — currency). RTI_RATING turned out automatable (HTML table parse) despite the earlier auth-gated-AJAX verdict — primary tier-1, 196 countries, now built. OECD_TFI built at composite level via Compare Your Country manual download (A–K sub-indicators = future enhancement, not a to-do). UNCTAD_NTM: WITS bulk CSV is accessible but latest cross-country data is 2012-2017 (~76 countries) — too stale; dropped, NTBs accepted as a v1 gap.
- Category 1 PDF extraction not built: IMF_FSAP (macroprudential + financial-sector quality assessment). _(IMF AREAER de-facto ER removed — now BUILT via checksum-validated manual transcription, nb 37, not a PDF/coordinate parse. PEFA reclassified → structured manual-download pipeline, BUILT. ICNL → supplementary `tier3_web`.)_

---

*This document to be deleted when master PDF is regenerated at end of pipeline build phase.*
