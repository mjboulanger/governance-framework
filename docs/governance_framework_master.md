# Governance Framework — Master Document

*Framework architecture, principles, source-level measurement decisions for 25 concepts, future enhancements, and outstanding work.*

> **Document status.** This is the **living master** for the framework's design (concepts, categories, source rosters, per-concept measurement decisions). It is edited directly as decisions are made; **git history is the record of changes** (the dated changelog at the end is frozen; it covered the May-to-July 2026 migration from the original PDF and is no longer maintained). Per-metric selection outcomes live in `data/processed/metric_selection.csv` (authoritative) and `src/metric_selection.py`; pipeline build status and data currency in `docs/framework_decisions.md`, `data/processed/source_registry.csv`, and the download log.

---

## Purpose

This framework provides a structure for assessing governance quality at the national level, oriented to the question of how governance affects economic and development outcomes. It is designed to apply across the full country spine — all economies with population data (**213** as of 2026-07; non-sovereign territories included and flagged) — excluding effectively closed regimes (PRK, ERI, TKM), supporting cross-country comparison and analytical decomposition of governance into substantively meaningful dimensions. *(Scope revised 2026-07-10 from the original >2M-population target — see changelog and `docs/metric_methodology.md` §2.)* The ultimate use case is investment decisions — whether to allocate capital to a country — with this framework providing the governance assessment piece. Sovereign credit, macroeconomic vulnerability, and other risk factors live outside this framework in separate modules.

**Coverage (characterization as of 2026-07-10; figures regenerable, not hardcoded).** Coverage is strong and well-characterized across the sovereign core: every sovereign carries a broad indicator set (range ~84–385 present metrics; median ~358), and the sparse tail is **exclusively non-sovereign territories** (retained and flagged, not dropped). The authoritative, *live* coverage tables are maintained as tracked data — `data/processed/metric_coverage.csv` (per metric) and `data/processed/country_coverage.csv` (per country) — rather than embedded here, so the numbers never go stale; **per-concept** coverage is produced at metric selection (Step 1), once concepts are assembled. Reliability handling reads off these tables: see `docs/metric_methodology.md` §4 (metric inclusion) and §8 (per-concept reliability flags).

The framework draws on academic measurement projects (V-Dem, Polity, Quality of Government Institute, others), multilateral institutions (World Bank, IMF, OECD), think tanks and NGOs (Freedom House, Bertelsmann, Mo Ibrahim, World Justice Project, Transparency International, RSF, CIVICUS, IDEA, Pew), and ratings agency methodologies where relevant.

---

## Framework structure and primary measurement sources

The framework organises governance into **5 categories** containing **25 unique concepts** (29 total instances after multi-placement of 4 concepts). The table below summarises categorisation alongside the primary and secondary measurement sources selected for each concept at the source-level pass. Detailed source-by-source rationale (including sources considered but excluded) appears in the per-concept sections.

> **Note on concept count.** The working inventory is **24 unique concepts (28 instances)** as of 2026-07-24, after Concept 7 (PFM) was folded into Concept 8 and retired (number 7 now a vacant stable ID; C8–C25 unchanged). Was 25 before the fold. An earlier note recorded a revision to 26 (Concept 11 trade/state-control refinement); that count was not reconciled against the offsetting **Government Effectiveness + Public Administration Quality merge** (see consolidations), which removed one — netting 25, not 26. Verified 2026-07-17 (25 per-concept sections; 25 unique summary-table rows; 4 multi-placed → 29 instances). Concept numbering in the per-concept sections follows the current working order. **Update 2026-07-21:** Concept 10 was split — the *state control over the economy* dimension is now LIVE (scored via V-Dem v2clstown), and *SOE governance quality* was moved to the deferred/future-enhancements list. The headline count is unchanged (Concept 10 remains one numbered concept, now scored rather than deferred; SOE governance quality is a named deferred concept, not separately numbered), so the inventory stays **25 unique / 29 instances** — but all 25 are now scored in v1.

| Category | Concept | Primary sources | Secondary / supplementary |
|----------|---------|-----------------|---------------------------|
| **1. Political foundations** | Political settlement | V-Dem power-distribution indicators; FSI Factionalized Elites (P1); FSI Group Grievance (S1); Powell-Thyne coups *(DPI excluded on validity - see C1 section)* | (none selected as supplementary tier) |
| | Political stability and regime durability | WGI Political Stability; V-Dem regime duration; Powell-Thyne coups; UCDP and/or ACLED; GPI; WJP Factor 5 | Polity Durable (cross-check); GTD (currency caveat); MMP; ICRG/EIU (optional paid) |
| **2. State capacity** | State capacity | V-Dem state authority indicators; FSI Security Apparatus (C1) | WB Informal Economy Database; ILO social security coverage; Hanson-Sigman state capacity |
| | Statistical and informational infrastructure* | World Bank SPI; Open Data Inventory | IMF SDDS subscriptions *(dropped v1 — redundant with SPI/ODIN)* |
| | Government effectiveness and admin quality | WGI Government Effectiveness; V-Dem Rigorous and Impartial Public Admin (v2clrspct) | WJP Regulatory Enforcement (borderline); QoG Expert Survey impartiality/Weberianism (borderline) |
| | Service delivery and provision of public goods | WB WDI sector indicators; WHO GHO; UNESCO UIS; UNDP HDI sub-indicators; WB Human Capital Index; FSI Public Services (P2) | (none — concept measured directly from sector-specific sources) |
| | Regulatory quality* | WGI Regulatory Quality; WJP Regulatory Enforcement (Factor 6) | Heritage Business Freedom; Fraser Regulation area (with framing caveats) |
| **3. Accountability (horizontal)** | Legislative and constitutional checks* | V-Dem legislative constraint indicators (v2xlg_legcon and components); CCP separation-of-powers features | Polity5 XCONST (with supersession caveat) |
| | Judicial independence and quality* | V-Dem judicial indicators; WJP Factors 7 and 8; CCP judicial independence features | Linzer-Staton latent variable; Henisz POLCON |
| **Accountability (vertical)** | Electoral process and competition | V-Dem electoral indicators (incl. EMB autonomy/capacity); FH Electoral Process sub-component; Electoral Integrity Project (PEI); IDEA EMB Database *(deprioritized — V-Dem EMB supersedes)* | NELDA; IDEA Voter Turnout (compulsion adjustment needed); Polity electoral indicators; CCP electoral provisions; DPI |
| | Political participation beyond voting | V-Dem participation indicators; CIVICUS Monitor; IDEA GSoD Participation (P1, scored 2026-07-24) | (IDEA GSoD moved to scored) |
| | Civil liberties | FH Civil Liberties sub-categories D and G; V-Dem civil liberties indicators | Pew GRI and SHI; Political Terror Scale; WB Women Business and the Law; US State Dept Human Rights Reports (Tier 3) |
| | Media freedom and pluralism | RSF World Press Freedom Index; V-Dem media indicators; CPJ journalist safety data | FH Civil Liberties sub-category D (repetition tracked); CLD/AIE RTI Rating; UNESCO Journalist Killings Observatory; Article 19 |
| | Civil society space and vitality | V-Dem CSO indicators; CIVICUS Monitor; FH Civil Liberties sub-category E | ICNL Civic Freedom Monitor; ILO CEACR (Tier 3) |
| | Government transparency and openness | V-Dem transparency-relevant indicators; WJP Factor 3; CLD/AIE RTI Rating | Open Budget Survey (repetition with PFM tracked); IDEA Political Finance Database; ODIN. *(Global Data Barometer deprioritized — see changelog)* |
| | Statistical and informational infrastructure* | *(see State capacity row above; same source list applies — multi-placed)* | |
| **4. Rule of law** | Legal quality and predictability | V-Dem v2cltrnslw; V-Dem v2clacjstm/v2clacjstw; V-Dem v2xeg_eqaccess; WJP Factor 4; WJP Factor 3; CCP | (none selected) |
| | Judicial independence and quality* | *(see Accountability horizontal row above — multi-placed)* | |
| | Personal security and order | UNODC Homicide Statistics; V-Dem physical violence indicators; Political Terror Scale; WJP Factor 5 | Global Peace Index societal safety and security domain |
| | Property rights and contract enforcement | V-Dem property rights indicators; Heritage Property Rights; CCP property provisions; WJP Factor 6 sub-component 6.5 | Fraser Legal System and Property Rights area (selective); WIPO IP data |
| | Control of corruption | V-Dem corruption indicators; Transparency International CPI; WJP Factor 2 | Bayesian Corruption Indicator (currency verification); UNCAC review content (Tier 3, supplementary) |
| | Legislative and constitutional checks* | *(see Accountability horizontal row above — multi-placed)* | |
| **5. Economic and fiscal governance** | Public financial management (PFM) | PEFA (where current); Open Budget Survey | IMF Fiscal Transparency Evaluations (coverage verify); IMF WEO fiscal outcomes (low S/N, low weight) |
| | Macroeconomic and financial policy framework | Romelli CBI Index; IMF Fiscal Rules Database; IMF AREAER (FARI); Chinn-Ito KAOPEN; IMF iMaPP; IMF AREAER de-facto ER classification (BUILT — nb 37, checksum-validated transcription) | Reinhart-Rogoff (de facto regime, supplementary; data ends 2019); Dincer-Eichengreen CB Transparency (deprioritized); Heritage Monetary Freedom / Fraser Sound Money (monetary only); EIU Country Risk macro (optional paid) |
| | Regulatory quality* | *(see State capacity row above — multi-placed)* | |
| | Financial sector regulatory and supervisory quality | FSAP/BCP/IOSCO/IAIS assessments (where available); FATF compliance ratings; Basel AML Index | Barth-Caprio-Levine bank regulation survey (2019); IMF FSI outcomes (low weight, low S/N) |
| | State control over the economy | V-Dem v2clstown (state ownership/control of economy) | *(SOE governance quality split out, deferred to v2)* |
| | Trade governance | WB Logistics Performance Index; OECD Trade Facilitation Indicators; WTO TFA implementation *(dropped — licence)*; KOF Globalisation Index Trade subindex; WB WITS tariff data; Heritage Trade Freedom | WTO Trade Policy Reviews (Tier 3); WTO RTA database |
| | Environmental and climate governance | Yale EPI policy/institutional sub-components; LSE Grantham Climate Laws Database; ~~ND-GAIN~~ *(dropped at Step-1)*; ASCOR sovereign climate assessment; IRENA Renewables Capacity Statistics; WB Carbon Pricing Dashboard | IEA energy data and Policies Database (free portions); BNEF Climatescope; WEF Energy Transition Index. *(IRENA Renewable Energy Policies Database deprioritized — see changelog)* |

\* *Concept appears in more than one category. Inventory: 25 unique concepts, 29 instances. WGI Voice and Accountability serves as Accountability category roll-up cross-check; WGI Rule of Law as Rule of Law category cross-check.*

---

## Framework architecture and principles

### Architecture

The framework operates at two structured levels. **Categories** (5 thematic groupings) provide the top-level reporting and communication structure. **Concepts** (25 unique, 29 instances) sit within categories and represent the substantive dimensions of governance that are scored. Within Accountability, concepts are further organised into horizontal accountability (government checks on government) and vertical accountability (government accountability to non-state actors).

Below the concept level, **sources** (datasets and measurement projects) are selected for each concept based on coverage, precision, signal quality, and accessibility. **Metrics** (specific indicators within sources) are selected at the metric-level pass that follows source-level decisions. **The metric-pass scoring methodology — inclusion, normalization, aggregation, weighting, reliability, and momentum — is documented in `docs/metric_methodology.md`.**

### Guiding design principles

- **Substantive categorisation.** Concepts are grouped by what they are about rather than by where they sit in a causal chain or what governance is functionally for. This prioritises navigability and matches how governance is taught and discussed.
- **Multi-placement where genuinely warranted.** A concept is placed in more than one category when it substantively serves more than one categorical function — not merely when it relates to other categories. The operational test: direct dual-function rather than indirect downstream effect. Four concepts qualify.
- **Economic relevance as cross-cutting lens.** Each concept carries an annotation of the strength of evidence linking it to economic and development outcomes. This informs eventual weighting decisions but is not used to exclude concepts at the structural stage.

### Working principles for source and metric selection

The following principles guide source-level and (eventually) metric-level decisions. They were established iteratively through the source-level pass and apply across all concepts.

1. **Country coverage threshold.** Sources should cover the large majority of the framework's **well-measured sovereign core (~150–160 countries)**. The scored spine is broader — 213 economies including flagged territories and microstates (2026-07-10 revision) — but source selection is NOT judged against the full spine: microstate/territory gaps are expected, carried by reliability flags, and are not grounds to drop a source. Sources with systematic regional or income-group exclusions are dropped even when methodologically strong. Borderline-coverage sources (~135–145) are kept on the table at source level with final inclusion decided at metric-level pass against the specific sample.
2. **Precision-of-fit.** Prefer sources that conceptually target the specific concept. Broader aggregate sources can be considered but are excluded where precise concept-specific sources exist. Where broad aggregates duplicate content captured directly by underlying sources we use, the aggregates serve as category-level cross-checks rather than concept primaries.
3. **Signal-to-noise consideration.** Prefer metrics where cross-country and over-time variation is driven primarily by the governance concept rather than by exogenous, cyclical, or confounding factors. Lower-S/N metrics can be supplementary but shouldn't drive scoring. Particularly relevant for outcome metrics (e.g., fiscal outcomes have low S/N for PFM because they're heavily driven by commodity cycles and external conditions).
4. **Outcome metrics OK if signal-rich.** Don't categorically exclude outcome measures. Evaluate by S/N for the specific concept. UNODC homicide is a good outcome measure for personal security (high S/N). Tax-to-GDP is a poor outcome measure for extractive capacity (low S/N due to economic structure confound).
5. **Indicator-level repetition tracked, not prohibited.** Where the same indicator legitimately measures content for multiple concepts, it can appear in both. The discipline is awareness and documentation, not exclusion. Several indicators appear in multiple concepts (e.g., PTS in Personal Security and Civil Liberties).
6. **Conceptual chain awareness within categories.** Concepts within a category often sit on a causal chain (e.g., State capacity → Government effectiveness and administrative quality → Service delivery). The same indicators should not measure structural ability, current use, and realised outputs simultaneously. Disciplined assignment of indicators to specific points on the chain.
7. **Tiering reflects both directness and centrality.** Source tier-1 vs tier-2 placement reflects (a) quality and directness of measurement for the dimension covered, and (b) centrality of that dimension to the concept's role within its category. A direct measure of a peripheral sub-dimension is tier 2 even if methodologically strong.
8. **WGI components as category-level cross-checks.** Where the framework uses WGI components' underlying sources directly (V-Dem, WJP, FH, etc.), the WGI aggregate is treated as a category-level cross-check at roll-up rather than as a concept primary. Avoids double-counting through aggregation.
9. **Ideologically-loaded sources used selectively.** Heritage and Fraser indices have ideological framings of varying intensity across components. Components with low loading and broad expert consensus alignment (e.g., Heritage Trade Freedom for openness; Heritage Property Rights; Heritage Monetary Freedom) are usable. Components with high loading (Heritage Fiscal Freedom, Government Size; Fraser Government Size) are excluded as they conflate policy stance with governance quality.
10. **Subscription sources require cumulative case.** Tier 4 paid sources (EIU at ~$2k/year, ICRG at ~$7k/year, Gallup, MSCI, IISS) are kept off the primary list unless the cumulative case across multiple concepts justifies the cost. To date, neither EIU nor ICRG has earned primary placement across concepts on precision grounds; the cumulative case for paying is weak.
11. **Within-source metric collapse (two-gate test).** Where one source contributes a composite index plus its own components to a single concept and those components are highly correlated, redundant components are pruned at selection - but only under two gates, BOTH of which must fail before a component is dropped: (Gate 1) high correlation with the composite (mean pairwise r > ~0.85) AND a composite exists to carry the shared signal; (Gate 2) the component fails to make material, interpretable distinctions the composite blends away (checked by inspecting where it most diverges from the composite). High correlation ALONE never drops a metric - a component that discriminates materially in a decision-relevant subset of countries is kept even at r > 0.9. This is editorial redundancy pruning, NOT formal statistical decorrelation (no PCA/factor analysis in v1). Residual correlation among retained metrics is handled separately by tier weighting and the Step-4 correlation-aware weighting item. See metric_methodology.md S6 for the operational rule; first applied to C23 Media freedom (8 V-Dem media metrics collapsed to 5).

### Key consolidation decisions

Four consolidations were made at the framework-design stage to reduce overlap and double-counting that would otherwise distort category-level aggregation:

- **Internal cohesion absorbed into Political stability.** Cohesion is a structural condition; stability is the outcome it most directly drives. Cohesion data (FSI Factionalized Elites and Group Grievance, V-Dem group exclusion) feeds in. After subsequent refinement, cohesion-related indicators (FSI P1, S1) were placed in Political settlement instead, leaving Political stability purely outcome-focused.
- **Government effectiveness and Public administration quality merged.** Conceptually distinct (current deployment vs. standing civil service quality) but available cross-country indicators do not reliably separate them. Merged concept retains content from both: V-Dem Rigorous and Impartial Public Administration (v2clrspct) for Weberian/impartiality content; WGI Government Effectiveness for policy-implementation effectiveness.
- **Constraints on executive power renamed and narrowed.** Original scope substantially overlapped with judicial independence, electoral process, civil society, media freedom, and rule of law. Renamed **Legislative and constitutional checks** and narrowed to legislative oversight, constitutional architecture, and non-corruption-focused independent oversight bodies (central bank, audit institutions, EMBs).
- **Rule of law renamed and narrowed.** Original scope overlapped with judicial independence, property rights, personal security, corruption control, and legislative/constitutional checks. Renamed **Legal quality and predictability** and narrowed to the residual: quality of the law itself, equal treatment in non-judicial contexts, congruence between law and practice, and predictability of legal application beyond the courts.

### Multi-placed concepts

Each placed equally in both categories (no primary/secondary placement):

- **Statistical and informational infrastructure:** State capacity + Accountability (vertical)
- **Legislative and constitutional checks:** Accountability (horizontal) + Rule of law
- **Judicial independence and quality:** Rule of law + Accountability (horizontal)
- **Regulatory quality:** Economic and fiscal governance + State capacity

---

## Outstanding work

### To-do list (v1 framework, pending decisions and work)

Items remaining for v1 framework completion, in approximate order of dependency:

- **Consolidated cross-concept source table.** Show which sources appear across which concepts. Helps prioritise metric-level pass and gives visibility on source overlap and reuse patterns. Will be produced as separate review document.
- **Metric-level pass.** For each concept, decide on specific indicators within each chosen source. The largest remaining task. Requires familiarity with each source's codebook. Borderline-coverage sources to be evaluated against specific country sample at this stage.
- **EIU vs ICRG subscription decision.** Based on cumulative source-level pass: neither has earned primary placement on precision grounds. Cumulative case appears weak. Decision to finalise at metric-pass stage but lean is toward not subscribing in v1.
- **Track record / predictability / payment culture composite design.** Originally deferred. Multiple sourcing options exist: sovereign rating action histories, fiscal-rule compliance rates, IMF program completion records, CDS spreads, EMBI sub-components. Decision needed on whether to handle as distributed content across existing concepts or as a standalone composite dimension.
- **Equality incorporation design.** Left as open question when equality was removed as standalone concept. Options: disaggregated scoring of existing indicators by group, equality-specific indicators within relevant concepts, or other approach.
- **Process/outcome classification of metrics.** Original framework principle (process = within state apparatus; outcome = touches non-state actors) is established but hasn't been applied concept-by-concept. Address at metric-pass stage.
**Full decomposability [LOCKED 2026-08-10].** Every score is traceable to source. The scoring layer (D6/D7) persists three attribution tables - metric-level, concept-level, category-level - each carrying the ACTUAL intermediate values (metric scores + tier weights; the three concept-level adjustments: missingness penalty with its fraction/floor/weight, relevance, and measurement-quality; and the category roll-up contributions). A dashboard user can click into any concept and see exactly how it scored, with no black boxes. Intermediates are stored even when a step is a no-op. This is the investor-legibility guarantee: no number in the framework is unexplained.

**Concept-level weighting: relevance x measurement-quality [values SET 2026-08-10; data/processed/concept_weights.csv].**

**Why two concept-level multipliers.** A concept's contribution to its category is scaled by two orthogonal judgments (methodology S7): **relevance** (does this dimension MATTER to the category core?) and **measurement-quality** (can it be MEASURED well, for all countries, by the metrics that exist?). Distinct axes - a dimension can matter greatly yet be poorly measured, or be secondary yet measured cleanly - so keeping them separate preserves information a single number would lose. Metric-level quality is handled separately by tiering (P1/P2/Sp) WITHIN each concept; these two multipliers operate BETWEEN concepts. Effective concept weight = relevance x measurement-quality; categories are equal-weighted.

**Both multipliers default to 1.0** - a concept is downgraded only for a demonstrated reason. Only 3 of 24 carry any downgrade:

| Concept | Relevance | Meas.-quality | Effective | Note |
|---|---|---|---|---|
| C1 Political settlement | 1.00 | 1.00 | 1.00 |  |
| C2 Political stability and regime durability | 1.00 | 1.00 | 1.00 |  |
| C3 Statistical and informational infrastructure | 1.00 | 1.00 | 1.00 |  |
| C4 Government effectiveness and administrative quality | 1.00 | 1.00 | 1.00 |  |
| C5 Service delivery and provision of public goods | 1.00 | 1.00 | 1.00 |  |
| C6 Regulatory quality | 1.00 | 1.00 | 1.00 |  |
| C8 Macroeconomic and financial policy framework | 1.00 | 1.00 | 1.00 |  |
| C9 Financial sector regulatory and supervisory quality | 1.00 | 0.75 | 0.75 | construct gap |
| C10 State control over the economy | 1.00 | 1.00 | 1.00 |  |
| C11 Trade governance | 0.50 | 1.00 | 0.50 | half relevance (locked 2026-07-21) |
| C12 Environmental and climate governance | 0.50 | 1.00 | 0.50 | half relevance (locked 2026-07-21) |
| C13 State capacity (structural core) | 1.00 | 1.00 | 1.00 |  |
| C14 Legal quality and predictability | 1.00 | 1.00 | 1.00 |  |
| C15 Judicial independence and quality | 1.00 | 1.00 | 1.00 |  |
| C16 Personal security and order | 1.00 | 1.00 | 1.00 |  |
| C17 Property rights and contract enforcement | 1.00 | 1.00 | 1.00 |  |
| C18 Control of corruption | 1.00 | 1.00 | 1.00 |  |
| C19 Legislative and constitutional checks | 1.00 | 1.00 | 1.00 |  |
| C20 Electoral process and competition | 1.00 | 1.00 | 1.00 |  |
| C21 Political participation beyond voting | 1.00 | 1.00 | 1.00 |  |
| C22 Civil liberties | 1.00 | 1.00 | 1.00 |  |
| C23 Media freedom and pluralism | 1.00 | 1.00 | 1.00 |  |
| C24 Civil society space and vitality | 1.00 | 1.00 | 1.00 |  |
| C25 Government transparency and openness | 1.00 | 1.00 | 1.00 |  |

**Rationale for the sub-1 concepts:**
- **C9 (Financial sector regulatory and supervisory quality) - measurement-quality 0.75.** The one genuine CONSTRUCT gap: the construct is supervisory effectiveness, but the only de-facto signal (fatf_effectiveness) is a narrow AML/CFT slice and the rest (fatf_technical_compliance, brss) are de jure rules-on-paper. No broad prudential-effectiveness measure exists for any country. Nudged (0.75) not gutted (0.5) - a real de-facto signal does exist. This is the methodology's own worked example.
- **C11 (Trade governance) and C12 (Environmental and climate governance) - relevance 0.5.** Half relevance (locked 2026-07-21): real but secondary dimensions of their categories' governance core. Their measurement-quality is left at 1.0 DELIBERATELY - stacking an MQ downgrade on the halved relevance would near-zero them (0.5 x 0.75 = 0.375), which the methodology warns against; neither has a severe enough construct gap to justify it (both carry direct, construct-valid metrics).

- **Weighting scheme.** Resolved 2026-07-21 (working session; full spec `metric_methodology.md` §7): the **5 categories are equal-weighted**; concept weights within category are **equal except Trade (11) and Environmental (12) at half** — the half-weights are the implicit low-relevance judgment, and the earlier four-level annotation exercise was superseded (worksheet retired). Two further mechanisms are locked with parameters set at Step-1 metric selection: a coarse concept-level **measurement-quality multiplier** (1.0/0.75/0.5) for concepts with a genuine CONSTRUCT gap (even the best available metric misses the true construct, e.g. C9 financial supervision: de-jure/AML sources only, no effectiveness measure) - default 1.0, downgrade the exception; thinness alone is NOT a downgrade (few-but-solid metrics stay 1.0) and within-concept weak metrics are handled by tiering, not this multiplier (no double-penalty) [application principle 2026-08-10], and a **missingness penalty** (latest slice only; per-source endogenous/exogenous tags; full / capped-partial / no-penalty regimes) applied after §6 renormalization.
- **Concept 25 (Government transparency and openness) reconsideration.** Significant indicator overlap with other concepts (only the IDEA Political Finance Database and Global Data Barometer are unique to it). **Decision (revisited 2026-06-18): KEEP as own concept.** "Government transparency and openness" is a coherent, investor-legible dimension; overlap tracked under the repetition rule. The Global Data Barometer is deprioritized as its open-data source (thin, edition-unstable, duplicates ODIN). Still flagged to revisit with the full framework view before finalising. See changelog and `framework_decisions.md`.

### Future enhancements (post-v1)

Items identified as v1 measurement gaps or quality limitations, to be addressed in subsequent framework iterations. Many depend on external data sources expanding coverage or methodology over time.

- SOE governance measurement — OECD SOE Guidelines reviews, iSOEF expansion, OECD Corporate Governance Factbook (currently fail coverage); IMF Article IV systematic extraction.
- **State economic control — now measured (2026-07-21):** V-Dem v2clstown provides universal-coverage (179/179) state ownership/control data; the state-control dimension of former Concept 10 is now scored in v1. **SOE governance quality** (how well the state governs its enterprises) remains deferred to v2 — no good universal-coverage source (best is OECD ~50 countries).
- Political settlement direct measurement — possible commissioned country-expert survey along ESID lines for the specific sample.
- PFM coverage expansion — depends on PEFA assessment frequency increasing; IMF FTE coverage expansion if it occurs.
- Statistical infrastructure data integrity / manipulation measurement — currently a documented gap with no standardised cross-country source.
- B-READY rollout tracking — currently ~50 countries, targeting 180. When expanded, strengthens measurement for procedural regulatory quality, trade governance, property rights operational efficiency.
- OECD TFI sub-indicator (A–K) breakdown — v1 uses the composite average (sufficient given admin triangulation: LPI built + TFI built; WTO TFA designed-in but not yet built). Expanding to the 11 sub-indicators is a possible enhancement IF metric-pass introduces per-area weighting (e.g. isolating "transparency of trade rules"); blocked on acquisition (CYC = one sub-metric per download; publication-PDF annex the likely route). Not a to-do.
- Non-tariff barriers measurement — UNCTAD NTM dropped on currency (latest 2012-2017, ~76 countries). WITS bulk-download route is accessible and would work if UNCTAD publishes a refreshed, broader NTM round; revisit then. Currently the one openness gap in Trade governance.
- Bureaucratic feature measurement for non-OECD-non-BTI countries — currently QoG Expert Survey is borderline; could commission expanded coverage.
- Education quality measurement — PISA/PIRLS/TIMSS fails coverage; better universal learning-outcome measurement would strengthen service delivery scoring.
- IMF Article IV systematic extraction — major operational investment benefiting Macroeconomic framework, PFM, SOE governance, and other concepts.
- Subscription source evaluation revisit — EIU at $2k or ICRG at $7k, when cumulative case becomes stronger or when sources change in their coverage of governance content.
- Custom expert survey approaches — for concepts where third-party measurement is structurally thin (notably political settlement).
- World Bank Country Climate and Development Reports (CCDRs) — track as coverage expands.
- CCPI / Climate Action Tracker methodology extension — if methodologies are extended to broader country sample.
- Dedicated environmental institutional capacity measurement — currently a real gap.
- NDC implementation tracking — currently captured only de jure; de facto implementation measurement weak.
- Cross-country extractive capacity measurement — surviving the S/N filter; current proxies (tax/GDP) excluded on noise grounds.
- Cross-country audit institution effectiveness measurement — INTOSAI data fragmentary; better measurement needed.
- Cross-country ombudsman institution measurement — weak cross-country measurement currently.
- Internet / digital media freedom universal-coverage measurement — Freedom on the Net fails coverage at ~70 countries.
- Media ownership concentration cross-country measurement — Media Ownership Monitor covers only ~20 countries.
- Minority rights dimension dedicated measurement — currently captured indirectly through general civil liberties measures.
- Cross-country CSO sector size and capacity measurement — Johns Hopkins Nonprofit Sector Project defunct; replacement needed.
- Cross-country open data measurement — current sources defunct (Open Data Barometer) or borderline (Global Data Barometer).
- Procurement transparency cross-country measurement — sector-specific sources fail coverage.
- Lobbying transparency cross-country measurement — currently very thin globally.
- De facto vs de jure transparency implementation tracking — RTI laws measured; actual disclosure practice less measured. (RTI implementation: rti-evaluation.org assessed and deprioritized — too thin/heterogeneous; partial V-Dem coverage. See changelog.)
- Transparency / RTI trajectory (direction of travel) — RTI Rating history exists but is sticky; a direction-of-travel dimension applicable to several de jure sources could use it later.

---

## Per-concept source-level decisions

The following sections cover all concepts in framework order. Each section provides: conceptual scope; measurement challenge specific to the concept; a source-level decision table listing all sources considered with tier assignment and rationale; and notes on the state of measurement for the concept.

**Tier conventions:** Tier 1 = workhorse primary source; Tier 2 = supporting primary source; Supplementary = useful for cross-check or partial coverage at lower weight; Cross-check = used at category roll-up rather than concept score; Dropped = excluded with reason.

---

### Concept 1: Political settlement

**Category:** Political foundations
**Scope:** the underlying distribution of power among elite factions (horizontal) and between elites and broader social groups (vertical) that produces and constrains formal institutions. Captures configuration of power rather than observable institutional features.
**Measurement challenge:** probably the hardest of the concepts to measure with third-party quantitative sources. Direct measurement in the academic literature uses qualitative case studies and country-expert surveys (ESID, Khan, Kelsall) with limited cross-country coverage. Cross-country quantitative work relies on proxies that capture aspects of the underlying construct.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem power-distribution indicators (v2pepwrses, v2pepwrsoc, v2x_egal, v2psoppaut, factionalism) | Primary tier 1 | Direct fit for vertical power distribution and horizontal factionalism dimensions. Expert coding, ~180 countries, annual. |
| FSI Factionalized Elites (P1) | Primary tier 1 | Direct conceptual match for elite fragmentation. 179 countries, annual. Placed here (not in Stability) to maintain conceptual separation. |
| FSI Group Grievance (S1) | Primary tier 1 | Captures vertical fragmentation/social cohesion. Same source family as P1. Placed here for the same reason. |
| DPI (Database of Political Institutions) | EXCLUDED - validity (2026-07-24) | Was selected Primary tier 2 (party fragmentation as elite-organisation proxy). NOT scored: DPI data and pipeline are CORRECT, but DPI Frac measures seat-dispersion across party LABELS and conflates genuine pluralism with managed-autocracy pseudo-pluralism (Belarus 0.994 = many toothless regime-permitted parties, same as a real multiparty democracy; Barbados one-party = 0.0). Confounded by the very regime type C1 assesses, so an invalid proxy. C1 keeps FSI Factionalized Elites (P1, expert-coded actual elite fragmentation). See metric_selection dpi_total_fragmentation why= and decisions log. |
| Powell-Thyne coups | Supplementary | Revealed measure of settlement instability through realised regime breakdown. Universal, 1950–present. |
| ESID political settlements typology | Dropped — coverage | Conceptually most direct match but ~40 developing countries only. Fails coverage threshold. Added to future enhancements as candidate for commissioned expert survey. |
| BTI stateness component | Dropped — coverage | ~140 transformation countries; excludes most developed economies. |
| WGI Political Stability | Dropped — placement | Outcome measure of stability, not configuration of settlement. Primary in Political stability concept instead. |

**State of measurement:** proxy-based composite from V-Dem and FSI is workable but documents a real limitation: the informal power configurations central to political settlements theory aren't fully captured by available third-party sources. Honest framing recommended in reporting.

---

### Concept 2: Political stability and regime durability

**Category:** Political foundations
**Scope:** durability of the political order, absence of unconstitutional change (coups, revolutions, mass political violence), absence of terrorism, low risk of large-scale political violence. Outcome-focused — what actually happens, not configuration of power (which is Political settlement).
**Measurement challenge:** stability is ambiguous — high stability can reflect either healthy institutions or successful repression. Pairing stability with regime quality content (covered in Accountability category) helps interpretation. Backward-looking and forward-looking measures are both relevant.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| WGI Political Stability and Absence of Violence/Terrorism | Primary tier 1 | Canonical aggregate stability score. ~215 countries, annual. Aggregator nature creates implicit reliance on underlying sources. |
| V-Dem regime duration | Primary tier 1 | Direct measure of regime continuity using V-Dem's own regime classification. Replaces Polity Durable as primary on methodological consistency and currency grounds. |
| Powell-Thyne coups database | Primary tier 1 | Direct measure of realised unconstitutional change events. Universal coverage 1950–present. |
| UCDP (Uppsala Conflict Data Program) | Primary tier 1 | Gold-standard academic source for armed conflict; battle deaths, one-sided violence. Universal. |
| ACLED | Primary tier 1 | Real-time event data; covers more event types than UCDP (protests, riots, civilian violence). ~250 countries/territories. Complement to UCDP. |
| Global Peace Index (IEP) | Primary tier 2 | Composite of 23 indicators; useful as cross-check at concept level. 163 countries, annual. |
| WJP Factor 5 (Order and Security) | Primary tier 2 | Direct fit for stability outcomes. Note: also primary in Personal security and order. 142 countries borderline. |
| Polity Durable | Supplementary | Classic regime durability measure. Used as cross-check rather than primary due to V-Dem supersession and Polity update reliability concerns. |
| Global Terrorism Database (START) | Supplementary | Best historical terrorism source but currency uncertain (funding disruption). Verify status at metric pass. |
| Mass Mobilization Project | Supplementary | Protest event data; update status uncertain post-2020. |
| PRS ICRG, EIU Country Risk | Optional paid | Forward-looking risk content adds value but subscription cost is the question. Considered as supplementary if cumulative case justifies. |
| FSI Factionalized Elites, Group Grievance | Dropped — placement | Moved to Political settlement to maintain conceptual separation between configuration (settlement) and outcomes (stability). |

**State of measurement:** strong. Multiple methodologically distinct sources cover stability outcomes well. Triangulation across WGI aggregate, V-Dem expert coding, and event-based data (UCDP, ACLED, Powell-Thyne) is robust.

---

### Concept 3: Statistical and informational infrastructure

**Category:** State capacity AND Accountability (vertical) — multi-placed
**Scope:** capacity, integrity, and accessibility of official statistics. The standing data and information apparatus of the state — statistical agency independence and resources, statistical laws and methodology quality, and the actual public availability and timeliness of data. Multi-placed because it operates both as a state capability and as accountability infrastructure (citizens, journalists, opposition need data to evaluate government).
**Measurement challenge:** three distinct sub-dimensions — production capacity, accessibility, and integrity. Production and accessibility are well-measured; integrity (resistance to manipulation) has no good standardised cross-country source and is documented as a gap.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| World Bank Statistical Performance Indicators (SPI) | Primary tier 1 | Comprehensive: data infrastructure, sources, products, services, use. 174 countries, annual, World Bank API. |
| Open Data Inventory (ODIN, Open Data Watch) | Primary tier 1 | Best-in-class for accessibility/openness sub-dimension. 195 countries, biennial. Methodologically distinct from SPI. |
| IMF Data Standards subscriptions (SDDS / SDDS Plus / eGDDS) | Primary tier 2 — **Dropped (v1)** | De jure standards-compliance signal (4-level ordinal: SDDS Plus / SDDS / e-GDDS / non-participating). Dropped on construct redundancy: SPI (continuous statistical capacity, likely already incorporating dissemination-standard adherence) and ODIN (continuous coverage+openness, independently audited) measure the same dissemination/transparency facet with more resolution; SDDS is coarse and partly self-reported, and where it discriminates (frontier/low-income floor) SPI already discriminates continuously. Not access, not licence (IMF data freely usable). Re-entry: cheap public DSBB source if a distinct de jure commitment signal is later wanted. |
| V-Dem media corruption / transparent laws indicators | Dropped — precision | Variables initially considered (v2mecorrpt, v2cltrnslw) don't directly measure statistical infrastructure. Stretches that wouldn't pass precision-of-fit. Dropped. |
| PARIS21 reports and assessments | Dropped — currency/structure | Qualitative country reports; not standardised cross-country dataset. Useful for deep dives only. |
| WGI Government Effectiveness | Dropped — precision | Too broad. Aggregates content captured elsewhere. |
| Academic data manipulation work (Martinez, Wallace, others) | Dropped — currency/structure | Specific country cases rather than standardised cross-country index. Real gap; added to future enhancements. |

**State of measurement:** good for production and accessibility (SPI, ODIN; IMF SDDS dropped v1 as redundant). Data integrity / manipulation resistance is a documented measurement gap with no honest universal-coverage solution. Best practice: score the concept on production and accessibility, note integrity dimension as a known limitation rather than force a loose proxy. THIN-FLAG DISPOSITION (2026-07-24): C3 is INTRINSICALLY THIN but adequately measured - 2 independent P1 sources (ODIN openness, IMF SPI performance) covering a coherent narrow concept (does the state produce good, open statistics). Not a fixable gap: the obvious third candidate (WB Statistical Capacity Indicator) was SUPERSEDED by SPI - same lineage, not independent. No action; documented as intrinsically-thin.

---

### Concept 4: Government effectiveness and administrative quality

**Category:** State capacity
**Scope:** the merged concept (former Government Effectiveness + Public Administration Quality). Captures both how well current government formulates and implements coherent policy and standing civil service quality (Weberian features: merit recruitment, professional norms, security of tenure, impartiality).
**Measurement challenge:** heavily measured space, but most indicators are perception-based and correlated. Disciplined selection avoids both over-relying on one source and double-counting through WGI's underlying inputs.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| WGI Government Effectiveness | Primary tier 1 | Canonical aggregate. Direct concept fit (GE is literally what it measures). ~215 countries, annual, API. |
| V-Dem Rigorous and Impartial Public Administration (v2clrspct) | Primary tier 1 | Direct fit for PAQ-side content (impartiality of public admin). Expert coding, ~180 countries. |
| WJP Regulatory Enforcement (Factor 6) | Borderline — keep for metric pass | Captures administrative-procedure quality. 142 countries (borderline coverage). Also a candidate for Regulatory Quality concept; need to disambiguate at metric pass. |
| QoG Expert Survey impartiality and Weberianism measures | Borderline — keep for metric pass | Direct fit for Weberian features (closed Weberianism, politicisation, professionalism). ~135 countries. Coverage borderline against the specific framework sample. |
| BTI Steering Capability and Resource Efficiency | Dropped — coverage | Methodologically strong but ~140 transformation countries only; excludes developed economies. |
| Mo Ibrahim IIAG Public Administration | Dropped — coverage | 54 African countries only. |
| OECD Government at a Glance | Dropped — coverage | ~40 OECD members plus partners; insufficient for broad sample. |
| CPIA Public Sector Management | Dropped — coverage | ~75 IDA-eligible countries only. |
| Evans-Rauch Weberianness Scale | Dropped — currency/coverage | Foundational academic measure but 35 countries and not regularly updated. |

**State of measurement:** headline measurement is strong (WGI + V-Dem). PAQ-side content is well-covered by V-Dem but supplementary depth from QoG / BTI / OECD GaG is lost on coverage grounds. The framework will be thinner on Weberian features for non-OECD-non-BTI countries than ideal; added to future enhancements.

---

### Concept 5: Service delivery and provision of public goods

**Category:** State capacity
**Scope:** actual delivery of education, health, infrastructure, social protection, and other public goods to the population. Outcome-focused — what citizens receive from the state. Distinct from Government effectiveness (use of capacity) and State capacity (structural ability).
**Measurement challenge:** service delivery is unusual among governance concepts in being measured largely through sectoral outcome indicators (school enrollment, vaccination coverage, infrastructure access) rather than governance-specific instruments. Disciplined source selection avoids the temptation of overly broad composites.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| World Bank WDI sector indicators | Primary tier 1 | Curated indicators on education enrollment/completion, health outcomes, infrastructure access. Use specific indicators, not composites. Universal coverage, API access. |
| WHO Global Health Observatory | Primary tier 1 | Health-specific direct outputs: immunisation, mortality, workforce density. Universal coverage, API. |
| UNESCO Institute for Statistics (UIS) | Primary tier 1 — **subsumed by WDI** | The v1 indicators (education expenditure %GDP/govt, pupil-teacher ratios) are delivered via WDI series (`SE.XPD.*`, `SE.*.ENRL.TC.ZS`). UNESCO's native database holds deeper learning-outcome data WDI lacks — a possible future enhancement, not a v1 gap. |
| UNDP HDI sub-indicators (life expectancy, schooling years — not composite) | Primary tier 1 — **subsumed by WDI** | Life expectancy (`SP.DYN.LE00.IN`) and GNI per capita PPP (`NY.GNP.PCAP.PP.CD`) are core WDI series. Use sub-indicators, not composite HDI. No standalone build needed. |
| World Bank Human Capital Index | Primary tier 2 | Synthetic measure: survival, schooling, learning, adult survival. ~170 countries. Useful as composite cross-check. |
| FSI Public Services (P2) | Primary tier 2 | Direct composite of basic service provision. 179 countries. |
| WGI Government Effectiveness | Dropped — precision | Too broad — measures overall governance not service outputs specifically. Primary in GE+AQ concept; using here too broad. |
| Worldwide Bureaucracy Indicators | Dropped — precision | Measures public sector employment/wages, not service outputs. |
| Sustainable Development Report (Sachs et al.) | Dropped — precision | Composite SDG implementation score; far broader than service delivery (climate, gender, partnerships). |
| PISA, PIRLS, TIMSS | Dropped — coverage | Quality measurement but mostly OECD + self-selecting participants. Real gap on education quality dimension. |
| Mo Ibrahim IIAG Human Development | Dropped — coverage | 54 African countries only. |

**State of measurement (build-verified):** build-complete via WDI + HCI + FSI. The three sector sources originally listed separately — WHO GHO, UNESCO UIS, UNDP HDI sub-indicators — are all **subsumed by WDI** (their v1 indicators are WDI series; WHO GHO's own OData API is deprecated). So no standalone WHO/UNESCO/UNDP pipelines are needed for v1. Strong on coverage of services delivered; weaker on quality dimensions (esp. education learning quality, where universal-coverage assessment fails — UNESCO's deeper learning data is a possible future enhancement).

---

### Concept 6: Regulatory quality

**Category:** Economic and fiscal governance AND State capacity — multi-placed
**Scope:** quality of regulation governing private economic activity — well-designed, predictable, proportionate, consistently enforced. Multi-placed because it reflects both state capability to design and implement regulation (State capacity) and the regulatory environment for economic activity (Economic and fiscal governance).
**Measurement challenge:** Doing Business discontinuation (2021) removed a major data source; B-READY is replacement but coverage currently inadequate. Procedural quality (RIA, consultation, transparency in rulemaking) has weak universal-coverage measurement.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| WGI Regulatory Quality | Primary tier 1 | Direct concept match. Universal coverage (~215). The aggregate is literally about regulatory quality. |
| WJP Rule of Law Index — Regulatory Enforcement (Factor 6) | Primary tier 1 | Direct fit for procedural and enforcement quality. 142 countries (borderline). |
| Heritage Business Freedom | ~~Primary tier 2~~ → **superseded by Fraser Regulation** | Same dimension as Fraser Regulation (both tier-2, regulatory environment as firms experience it). House overlap rule prefers Fraser (peer-reviewed, transparent weights) over Heritage (advocacy framing) — as already applied to Heritage Trade and Heritage Property. Tier-1 (WGI + WJP F6) already covers the concept; a second overlapping tier-2 adds no marginal value. Not built. |
| Fraser Regulation area | Primary tier 2 | Similar to Heritage Business Freedom. Same framing caveats. |
| World Bank B-READY | Track for future | Direct fit but ~50 countries currently. Targeting 180. Future enhancement item. |
| OECD iREG (Indicators of Regulatory Policy and Governance) | Dropped — coverage | ~40 OECD + partners. Strong for procedural quality but fails threshold. |
| PRS ICRG / EIU Operational Risk | Dropped — precision | Bundled risk products; regulatory content embedded in broader risk frame. |

**State of measurement:** headline regulatory quality is well-measured; procedural quality dimension is weakly measured universally (OECD iREG fails coverage). B-READY rollout will eventually help.

---

### Concept 7: Public financial management (PFM) — RETIRED / FOLDED INTO CONCEPT 8

**Status (2026-07-24):** Concept 7 has been **folded into Concept 8 (Macroeconomic and financial policy framework)** and retired as a standalone concept. Concept NUMBER 7 is now a vacant stable ID — C8–C25 keep their numbers; the inventory drops from 25 to 24 unique concepts. PFM content (budget credibility, execution controls, procurement, accounting, external audit) is now scored under Concept 8, rescoped to cover the **design AND management** of macro-policy institutions (see C8).

**Rationale:** PFM is thematically closer to macroeconomic/fiscal policy than to general administrative capacity (C4) — the budget is the central instrument of fiscal policy, so managing public money belongs with fiscal-policy institutions rather than general bureaucratic competence. Folding also resolved C7's standalone thinness structurally (it held only OBS scored, with PEFA pipelined but unscored). The C4 overlap (PFM as administrative competence) is acknowledged; the fiscal-policy theme was judged to dominate. Full options analysis (fold-C8 vs fold-C4 vs keep-separate) in framework_decisions changelog.

**Sources folded into C8:** PEFA (Primary tier 1, BUILT `33_pefa_pipeline`, scoring into C8 pending) and Open Budget Survey (already scored, moved C7→C8).

---

### Concept 8: Macroeconomic and financial policy framework

**Category:** Economic and fiscal governance
**Scope:** the **design and management** of macroeconomic and fiscal-policy institutions. Two levels: (1) POLICY-FRAMEWORK DESIGN — fiscal rules and fiscal council design, monetary policy framework, central bank independence and credibility, macroprudential institutional setup, exchange rate regime governance; and (2) PUBLIC FINANCIAL MANAGEMENT (former Concept 7, folded 2026-07-24) — budget credibility and execution, spending controls, procurement, accounting and reporting, external audit. Distinct from macroeconomic OUTCOMES (inflation, realised fiscal balance, debt path), which are deliberately out of scope (governance quality, not outcomes; outcomes live in the sibling sovereign-credit / macro-vulnerability modules). **v2 to-do:** no outcome/execution legs yet (budget-execution-vs-plan, inflation-target-hit-rate) — deferred to v2 pending the governance-vs-outcome boundary decision (see to-do list).
**Measurement challenge:** strong temptation to use macro outcomes (inflation, fiscal balance) as proxies; these have low S/N for framework quality given exogenous drivers. Direct institutional measures (CBI indices, fiscal rules databases) are higher S/N and should drive scoring.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| Romelli (2022) Central Bank Independence Index | Primary tier 1 | Current state-of-the-art for CBI. Updates and broadens Cukierman. ~155 countries. Direct fit, high S/N. |
| IMF Fiscal Rules Database (with compliance tracking) | Primary tier 1 | Existence, design, and compliance of fiscal rules. Direct governance measure (not just outcomes). |
| IMF AREAER — FARI (Financial Account Restrictiveness Index) | Primary tier 1 | Capital-account restrictiveness, de jure. IMF-native authoritative source. 194 countries, 1999–2024. **Manual** (portal WAF-blocked); FARI aggregate + FDI sub-index. See changelog. |
| Chinn-Ito KAOPEN | Primary tier 1 (derivative) | Most-cited academic capital-account-openness index, derived from AREAER. Automated, 182 countries 1970–2023. Broad time-series complement / cross-check to FARI; not more authoritative than AREAER. |
| IMF iMaPP (Integrated Macroprudential Policy Database) | Primary tier 1 | Macroprudential measure adoption. ~130 countries. |
| PEFA (Public Expenditure and Financial Accountability) — *PFM leg, folded from C7* | Primary tier 1 | Gold-standard PFM assessment, 31 indicators. BUILT (`33_pefa_pipeline`), 2016 framework, national, latest per country: 85 countries 2017–2026 (median 2022). Scoring into C8 pending (pillar-aggregate metric selection). Donor-driven coverage skews developing — reference-class caveat at scaling. |
| Open Budget Survey (IBP) — *PFM leg, folded from C7* | Primary tier 1 | Budget transparency and participation. 120 countries (2023 ed.), biennial. Scored (moved C7→C8). Broader coverage than PEFA but transparency-scope only. |
| IMF AREAER — de facto exchange-rate classification | Primary tier 1 (**built**) | The exchange-rate-regime dimension. IMF-native de facto classification (as-of April 30 2025, 195 jurisdictions); supersedes Reinhart-Rogoff as the current-state primary. **BUILT** — hand-transcribed from the borderless matrix (IMF Annual Report Appendix II.9) and validated against the PDF's row + column country-count checksums; pipeline `37_areaer_defacto_er_pipeline.ipynb` → `areaer_er_clean.csv` (arrangement + flexibility ordinal + IMF group + monetary-policy framework incl. inflation-targeting flag + anchor + reclassification recency). See changelog. |
| Reinhart-Rogoff exchange rate classifications | Supplementary (demoted) | De facto regime, methodologically independent (parallel-market-aware) cross-check + deep history (1946–). Demoted from primary: data ends ~2019 (≈7-yr stale, worst in stressed EMs); superseded as current-state primary by AREAER's own de facto classification. |
| Dincer-Eichengreen Central Bank Transparency Index | Deprioritized | Complementary CB transparency dimension (~120 countries) but stale; Romelli CBI covers the concept more currently. |
| Heritage Monetary Freedom / Fraser Sound Money | Supplementary | Monetary stability outcomes — lower ideological loading than other Heritage/Fraser components. Use monetary components only. |
| EIU Country Risk Service (macroeconomic component) | Optional paid | $2k/year. Forward-looking expert assessment. Worth considering if cumulative case across concepts justifies. |
| Cukierman / GMT central bank independence | Dropped — currency/supersession | Superseded by Romelli for current data. |
| EPU index (Baker-Bloom-Davis) | Dropped — coverage | ~30 countries (mostly developed). |
| World Uncertainty Index (Ahir-Bloom-Furceri) | Moved to cross-cutting | Better as cross-cutting predictability composite than primary for this concept. |
| Heritage Fiscal Freedom and Government Size / Fraser Government Size | Dropped — ideological loading | Higher loading than other Heritage/Fraser components. Conflate policy stance (size of state) with governance quality. |
| IMF WEO macro outcomes (inflation, fiscal balance, debt) | Supplementary, low weight if used | Low S/N for framework quality. Cross-check at low weight only. |

**Sub-dimension weighting (LOCKED 2026-07-24; IMPLEMENTED in D4, `src/build_concept_scores.py`).** C8 spans distinct sub-dimensions whose relative weight must be set INTENTIONALLY, not driven by how many metrics each happens to have (central bank independence is one excellent metric, Romelli, while fiscal is spread across ~7). Under naive equal-weight-within-tier monetary would fall to ~9% of C8 on metric count alone - not a considered judgment. Locked bucket weights: **Fiscal 40 / Monetary 40 / External 20.** FISCAL = fiscal rules (fr_num_rule_types, fr_max_legal_basis, fr_any_enforcement, fr_compliance_mean) + PFM (obs_open_budget_index, pefa_core_management, pefa_accountability). MONETARY = central bank independence (romelli_cbi_index, P1) + macroprudential-framework breadth (imapp_breadth_total, P2 - conceptually Monetary as financial-stability policy; P2 keeps romelli the dominant monetary signal at 2/3 vs 1/3 within the bucket). EXTERNAL = capital account (fari_aggregate, fari_fdi_aggregate, fari_fdi_inflow, kaopen_norm). *(areaer_er is NOT in External - the ER-regime metrics are excluded framework-wide: regime type is a policy choice not a quality ordering; the earlier bucket text listing areaer_er predated that exclusion.)* Rationale: fiscal and monetary are co-equal macro-policy pillars (40 each); external lower (20) as capital-account openness is partly a policy STANCE not governance quality, and the bucket is metric-heavy relative to its weight. Within a bucket, metrics share the bucket weight by tier - adding/removing a metric changes resolution WITHIN a bucket, not the bucket share. This dissolves C8's OVER flag: 13 metrics is fine once buckets carry fixed weight. Implemented in D4: C8 uses bucket-then-tier aggregation (within-bucket tier-weighted mean, buckets combined 40/40/20 renormalized over present buckets).

**State of measurement:** strong. Multiple direct institutional measures across all sub-dimensions (central bank, fiscal framework, exchange regime, macroprudential). Capital-account governance is triangulated across IMF-native (AREAER FARI) and academic derivative (Chinn-Ito). Exchange-rate-regime governance: current-state primary is the IMF AREAER de facto classification (**built** — nb 37, checksum-validated transcription); Reinhart-Rogoff retained as a supplementary independent cross-check (data ends ~2019).

---

### Concept 9: Financial sector regulatory and supervisory quality

**Category:** Economic and fiscal governance
**Scope:** quality of regulation and supervision of banks, securities markets, insurance, plus the AML/CFT framework. Includes legal/regulatory framework (what rules exist) and supervisory effectiveness (whether supervisors have powers, resources, independence, and actually use them).
**Measurement challenge:** FSAP (gold standard) happens every 5-10 years per country, voluntary for non-systemically-important. FATF has better timing but is AML/CFT-specific. Financial outcomes (NPL, capital adequacy) have low S/N for supervisory quality (cyclically driven).

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| IMF/WB FSAP — comprehensive financial sector assessment | Primary tier 1 — **deferred to PDF batch (scouted)** | Gold standard, but verified PDF-only: outputs are narrative per-country reports (FSSA / WB FSA / Technical Notes / Detailed Assessment Reports) — **no structured cross-country dataset** (unlike FATF's ratings .xlsx). Publication is voluntary/presumed and irregular (5–10yr cycles for ~47 mandated; voluntary elsewhere), so coverage is patchy even when extracted. The BCP/IOSCO/IAIS gradings are the banking/securities/insurance Detailed Assessment Reports **inside** an FSAP — not separate sources. Genuinely PDF-extraction work; deferred to the Category-1 PDF batch. |
| FATF Mutual Evaluations and compliance ratings | Primary tier 1 | **Built** — `fatf_clean.csv` (nb 35). 199 countries. 11 Immediate Outcomes (effectiveness HE/SE/ME/LE) + 40 Recommendations (technical compliance C/LC/PC/NC), raw + numeric (0-3). One row per country, newer methodology round wins (2013 4th-round vs 2022 5th-round), `methodology_round` flag retained. MANUAL download (fatf-gafi.org Cloudflare-gated; both methodology .xlsx by hand). 2013-vs-2022 scale comparability deferred to metric pass (only 7 countries on 2022 scale; flag enables filter/down-weight). |
| Basel AML Index (Basel Institute on Governance) | Primary tier 1 | AML/CFT risk composite. ~205 countries, annual, free. Synthesises FATF and other sources — saves extraction labor. *(Access note: Expert Edition requires institutional affiliation; see status table.)* |
| Basel Core Principles (BCP) assessments | Primary tier 1 | Banking supervision specifically. Embedded within FSAP. |
| IOSCO Principles assessments | Primary tier 1 | Securities regulation specifically. Embedded within FSAP. |
| IAIS Insurance Core Principles assessments | Primary tier 1 | Insurance regulation specifically. Embedded within FSAP. |
| Barth-Caprio-Levine (World Bank) Bank Regulation and Supervision Survey (BRSS) | Supplementary — **Built (nb 38)** | `wb_brss_clean.csv`. Bespoke construct-aligned **de jure** regulatory-stringency across 9 sub-constructs (supervisory power, independence, capital stringency, private monitoring, resolution, provisioning, liquidity, macroprudential, capacity); NOT the published BCL indices (2019 question-to-index mappings unavailable). Activity Restrictions excluded (contested directionality); provisioning/macropru trimmed of items penalizing IFRS-9. 5th wave (2019 survey; reference year 2016), 161 juris (155 reliable). Rules-on-paper, NOT supervisory effectiveness — advanced economies mid-pack is correct, validated vs Anginer et al. (2019). Currency cap real (frozen irregular survey). Auto-discover fetch; CC-BY-4.0. |
| IMF Financial Soundness Indicators (FSI) | Supplementary, low weight | Outcome data (NPL, capital adequacy). Low S/N for supervisory quality specifically. Cyclical. |
| FSB jurisdictional implementation monitoring | Dropped — coverage | ~24 FSB jurisdictions only. |
| IMF Financial Development Index, WB GFDD | Dropped — precision | Measure financial development, not regulation/supervision. |
| WGI Regulatory Quality | Dropped — precision | Too broad. Primary in Regulatory quality concept. |
| Heritage Financial Freedom | Dropped — ideological loading | Equates lower regulation with more freedom — loaded framing for financial regulation specifically. |
| PRS ICRG Financial Risk | Dropped — precision | Bundled with macroeconomic risk; not financial-supervision-specific. |

**State of measurement (build-verified):** the AML/CFT workhorse — **FATF Mutual Evaluation ratings — is now built** (`fatf_clean.csv`, 199 countries), covering the concept's most accessible and timely dimension. The `classified scrape` access verdict proved wrong on inspection (clean .xlsx download behind Cloudflare), like TFI/NTM. Remaining primaries are unbuilt: FSAP (gold-standard but PDF-batch, access unprobed), Basel AML (affiliation-blocked — though it largely synthesises FATF, now partly redundant), and BCP/IOSCO/IAIS (embedded in FSAP, unexamined). Broader prudential-supervision measurement (banking/securities/insurance) requires FSAP extraction — and FSAP was **scouted and confirmed PDF-only** (narrative reports, no structured dataset, voluntary/irregular publication), with BCP/IOSCO/IAIS being the Detailed Assessment Reports embedded *within* FSAP rather than separate sources. So FSAP + its three embedded assessments collapse into one item, deferred to the PDF-extraction batch. Unlike FATF/TFI/NTM, the 'hard' verdict here held up on inspection. AML/CFT is covered (FATF), and the **banking-regulation de jure leg is now built** via the WB BRSS (Barth-Caprio-Levine, nb 38; 161 juris, 155 reliable) — a rules-on-paper stringency measure that does NOT capture supervisory *effectiveness*. This remains among the thinnest concepts, but no longer substantially-unbuilt: FSAP's residual marginal value now concentrates on securities (IOSCO), insurance (IAIS), and supervisory effectiveness across all three, deferred to the deliberate Category-1 PDF batch. THIN-FLAG DISPOSITION (2026-07-24): sharper than 'thin' - because BRSS is Supplementary (weight 0), C9's SCORED content is entirely FATF, i.e. a single source measuring only the AML/CFT slice standing in for all of financial-sector regulatory/supervisory quality. This is the C19 single-source problem but narrower (one source AND one narrow dimension); AML compliance is a weak proxy for banking-prudential or securities/insurance regulation. Known v1 limitation, not an unaddressed oversight: the source that fills it (FSAP + embedded BCP/IOSCO/IAIS) is confirmed PDF-only and deferred to the Category-1 PDF-extraction batch. No metric action now; documented as thin-with-known-gap-pending-FSAP.

---

### Concept 10: State control over the economy

**Category:** Economic and fiscal governance
**Status:** LIVE in v1 (partial un-deferral, 2026-07-21). Previously deferred as the bundled "SOE governance and state control over the economy"; the **state-control dimension is now scored**, while **SOE governance quality is split out and remains deferred to v2** (see below and the future-enhancements list).
**Scope:** the degree of state ownership and direct control over important sectors of the economy — the state’s economic footprint. Does NOT cover SOE governance quality (board independence, hard budget constraints, competitive neutrality, transparency), which is a distinct, still-deferred concept.
**Primary source:** V-Dem **v2clstown** ("State ownership of economy": does the state own or directly control important sectors of the economy?). Coverage **179/179** in the latest year, complete and annual; interval-scored via the V-Dem measurement model. This clears the coverage threshold that the OECD SOE sources (~50 countries) failed — the original deferral reason no longer holds for the state-control dimension.
**Single-indicator flag:** scored on one indicator; trips the <3-indicator weight-review trigger (§8 reliability flag / D5). May be paired at Step-1 with a second state-footprint source (e.g. IMF GFS Public Corporations, Fraser "government enterprises and investment") for triangulation, coverage permitting.
**Directionality [evidence-resolved 2026-07-21; folds into D3 sign-pass]:** more state control = worse governance, scored **monotonically and linearly — no threshold/non-monotonic transform.** The earlier "likely non-monotonic" hypothesis was tested and rejected: against the WGI 6-dimension governance composite (latest year, n=166), Pearson +0.42 vs Spearman +0.41 (near-identical) and a quadratic fit adds negligible R² (+0.005), so the relationship is monotonic-linear with no threshold or U-shape. **Signal strength moderate** (r ≈ 0.42, R² ≈ 0.18): a valid but noisy governance signal — reinforces the single-indicator reliability flag and argues for modest weight. **Wealth-loading low** (r ≈ 0.25 with log GDP/capita USD): not a wealth proxy, low priority for the wealth-adjustment audit. Sign/shape now settled; still folded into the framework-wide D3 sign-pass for consistency.

**SOE governance quality — SPLIT OUT, DEFERRED TO V2.** How well the state governs the enterprises it owns (board independence, hard budget constraints, transparency, competitive neutrality). Split from the state-control dimension 2026-07-21 because v2clstown measures the *extent* of state control, not the *quality* of SOE governance — keeping them merged would make the concept score misrepresent what it measures. Remains deferred: best dedicated measurement (OECD SOE Guidelines reviews, OECD Corporate Governance Factbook, iSOEF) covers ~50 countries, failing the coverage threshold. PEFA Pillar 3 captures fiscal-risk-from-SOE content where assessments exist (~150 countries, timing variable). IMF Article IV staff reports have rich SOE content annually but require Tier 3 extraction. Future enhancement path: (1) OECD assessment coverage expansion; (2) iSOEF expansion; (3) IMF Article IV systematic extraction (also benefits Macro/PFM); (4) custom country-by-country research for major SOE economies (China, Russia, Gulf, Vietnam, etc.).

---

### Concept 11: Trade governance

**Category:** Economic and fiscal governance
**Scope:** combined trade administration (customs efficiency, trade procedure predictability, transparency of trade rules, anti-dumping process integrity) and trade openness (tariff levels, non-tariff barriers, FTA participation, trade defense). Weighted toward administration over openness per framework design decision.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| World Bank Logistics Performance Index (LPI) | Primary tier 1 | **Built** — `wdi_lpi_overall` in `wdi_clean.csv` (WDI series `LP.LPI.OVRL.XQ`, via the WDI pipeline). Survey-wave, not annual: 2007/10/12/14/16/18/22, 217 countries (186 in latest 2022 wave). Direct measure of trade administration quality. |
| OECD Trade Facilitation Indicators (TFI) | Primary tier 1 | **Built** (`34_tfi_pipeline`, `tfi_clean.csv`) — **composite average** (0–2), 164 countries, 2017/2019/2022. The composite is sufficient for the concept: administration is triangulated with LPI + WTO TFA, and TFI enters the concept as a blended admin signal under the admin weighting (the OECD composite already encodes the A–K weighting). The **11 sub-indicators (A–K)** are a possible future enhancement, not built — CYC exports only one sub-metric at a time (50+ downloads); would require the publication-PDF annex. Manual download from Compare Your Country (Overview table). |
| WTO Trade Facilitation Agreement (TFA) implementation tracking | **Dropped — licence** | **DROPPED (2026-07-09) — licence, not access.** A bulk Notifications Matrix XLSX now exists (tfadatabase.org/en/excel/excel/notifications-matrix; all members × 36 measures × Cat A/B/C), so the per-member-export barrier described below is obsolete. The blocker is licence: WTO material requires **written permission for commercial use** (no open dataset licence found), conflicting with the framework's commercial/investment purpose — the IPU-Parline test. TFA is self-reported *commitment*, not de facto performance (LPI + TFI cover that). Revisitable only via a WTO permission request. _Original access assessment retained below:_ **Not built — deferred to web scrape.** tfadatabase.org "implementation progress" tool gives a clean per-member rate (% TFA commitments implemented, e.g. Global 89.2%; Cat A/B/C split), current, ~164 members — good data. BUT the tool exports **one member at a time** (no batch/select-all; grouping filters return group aggregates, not member breakouts), so ~164 manual exports — not a maintainable manual route. Deferred to a web scrape (or the tool's backing API). NOT urgent: admin dimension already triangulable via LPI ✅ + TFI ✅; TFA adds robustness, not coverage. (Contrast NTM: that was dropped on currency; TFA is deferred on access — good data, awkward delivery.) |
| KOF Globalisation Index — Trade Globalization subindex | Primary tier 1 | **Proxied** — covered via QoG `dr_eg` (KOF *Economic* Globalisation = trade+financial combined) in `qog_clean.csv`. ⚠️ Mismatch vs the intended *Trade* subindex; pending decision (dedicated KOF pipeline vs accept proxy) at metric pass. De jure and de facto openness. ~200 countries. Annual. |
| World Bank tariff data (WITS / WDI) | Primary tier 1 | **Built** — `wdi_tariff_rate_simple_mean` + `wdi_tariff_rate_weighted_mean` in `wdi_clean.csv` (WITS via WDI). 189 countries, 1990-2022. Simple and trade-weighted average tariffs. |
| Heritage Trade Freedom → Fraser Area 4 (Trade) | Primary tier 1 | **Built (via Fraser)** — Heritage Trade Freedom deprioritized (policy-advocacy); superseded by Fraser Area 4, `fraser_trade_freedom` in `fraser_clean.csv` (peer-reviewed, transparent weights). 5-yr steps from 1990 then annual; partial in early years. Trade-openness index leg. |
| UNCTAD Non-Tariff Measures (NTM) database | Dropped — currency | The only cross-country NTM source, but its latest vintage is too stale to use. WITS bulk download is accessible (wits.worldbank.org NTM Data Download), but the data is a staggered single-vintage assessment from **2012-2017** (9-14 yr old, per-country) covering only **~76 countries** at the frequency/coverage-ratio level — well below the sample and badly stale. Dropped on currency (joins Doing Business / Trade Restrictiveness Index). NTBs are an accepted v1 measurement gap; revisit if UNCTAD refreshes (WITS route would then work). See changelog. |
| WTO Trade Policy Reviews (TPRs) | Supplementary | Rich country-specific content. Tier 3 PDFs. Cycle 2-7 years. |
| WTO RTA Database | Supplementary | FTA participation tracking. All WTO members. |
| World Customs Organization (WCO) data | Supplementary | Customs administration practices. Coverage and accessibility vary. |
| Fraser Freedom to Trade Internationally | Dropped — overlap | Overlaps Heritage Trade Freedom too closely. |
| Doing Business Trading Across Borders | Dropped — currency | Discontinued 2021. |
| B-READY trade content | Track for future | Coverage currently ~50 countries; track as expands. |
| Trade Restrictiveness Index (Kee-Nicita-Olarreaga) | Dropped — currency | Updates irregular. |
| WGI Regulatory Quality | Dropped — precision | Too broad for trade specifically; in Regulatory Quality concept. |
| PRS ICRG / EIU Country Risk | Dropped — precision/cost | Bundled in broader risk products. |

**State of measurement (build-verified):** mostly built. **Administration:** LPI ✅ (`wdi_clean.csv`) + TFI ✅ (`tfi_clean.csv`) built; WTO TFA ❌ **dropped on licence** (bulk XLSX now exists at tfadatabase.org, so access is solved; but WTO commercial use requires written permission — IPU-Parline precedent — and TFA is self-reported commitment, not de facto performance). So 2 of 3 admin primaries built and already triangulable; TFA would add robustness, not coverage. **Openness:** tariffs ✅ (`wdi_clean.csv`) + Fraser Trade ✅ (`fraser_clean.csv`) built; KOF proxied via QoG `dr_eg` (⚠️ mismatch, metric-pass decision); **non-tariff barriers are an accepted v1 gap** — UNCTAD NTM dropped on currency (2012-2017, ~76 countries). TFI built at **composite-average** level (sufficient — admin triangulation is real, not just designed); A–K breakdown a possible enhancement, not a v1 requirement. Net: with WTO TFA dropped, only the KOF proxy-vs-dedicated call (metric pass) remains.

---

### Concept 12: Environmental and climate governance

**Category:** Economic and fiscal governance
**Scope:** combined environmental governance (institutional capacity to regulate: ministry capacity, enforcement of environmental regulation, EIA processes, environmental data transparency, regulatory capture by polluting industries) and climate/renewables policy stance (with renewables policy as dominant policy-stance content). Weighted toward governance over policy stance per framework design decision.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| Yale Environmental Performance Index (EPI) — policy and institutional sub-components | Primary tier 1 | Workhorse for environmental governance content. 180 countries, biennial. Use sub-components selectively, not headline composite. |
| LSE Grantham Climate Laws Database | Primary tier 1 | De jure environmental and climate framework. Universal coverage. Continuously updated. *(Built national-only cumulative stock + flow.)* |
| ASCOR (TPI Centre / LSE) sovereign climate assessment | Primary tier 2 | Investor-led sovereign climate-*policy* assessment (legislation, carbon pricing, targets, just transition). ~85 countries, EM/frontier-oriented, income-group-exempted by design. Added at source level 2026-07-21; scored on 5 universally-answered areas. See `framework_decisions.md`. |
| ND-GAIN governance and readiness sub-scores | **Dropped at Step-1** | Construct validity: readiness is fundamentally an adaptive-capacity / development measure (wealth, infrastructure), governance at most a weak distal factor; governance-readiness is WGI-repackaged. See `framework_decisions.md`. |
| IRENA Renewables Capacity Statistics | Primary tier 1 | Workhorse for renewables outcomes. ~200 countries, annual. High S/N for renewables specifically. |
| World Bank Carbon Pricing Dashboard | Primary tier 1 | Direct fit for carbon pricing existence and design. Universal coverage. *(Built; 71 countries — thin, flagged.)* |
| IRENA Renewable Energy Policies Database | Deprioritized | No clean downloadable renewable-policy dataset exists; IRENA's policy work is report-based, and the joint IEA/IRENA Policies DB has no clean renewable filter and would duplicate Climate Laws. See changelog. |
| IEA energy data and Policies Database | Supplementary | Best for OECD/IEA members; uneven for non-OECD. Free portion partial; full database paid. |
| BNEF Climatescope | Supplementary | Emerging market climate policy detail. ~140 countries (borderline). |
| WEF Energy Transition Index | Supplementary | ~115 countries. Borderline coverage; partial fit. |
| UNFCCC NDC Registry | Dropped — user direction | De jure climate commitments. Doesn't measure implementation. Dropped per user preference for narrower policy stance content. |
| IMF Fossil Fuel Subsidy estimates | Dropped — user direction | Direct fit for subsidy reform dimension. Dropped per user preference for narrower content focused on renewables policy. |
| CCPI (Climate Change Performance Index) | Dropped — coverage | ~60 countries. Strong methodology but fails threshold. |
| OECD Environmental Policy Stringency Index | Dropped — coverage | ~35 countries. |
| Climate Action Tracker | Dropped — coverage | ~40 major emitters. |
| IMF C-PIMA | Dropped — coverage | Very limited country coverage. |
| World Bank CCDRs | Track for future | Expanding. ~50 countries currently. |
| WGI components | Dropped — precision | Too broad for environmental governance specifically. |
| EDGAR emissions data | Dropped — S/N | Outcomes heavily driven by economic structure, not governance. |
| Sustainalytics / MSCI sovereign ESG | Dropped — cost | Tier 4 paid, proprietary methodology. |

**State of measurement:** reasonable with the broad-coverage tools (Yale EPI, Climate Laws DB, ND-GAIN) providing direct environmental governance content. Renewables outcomes well-measured (IRENA). Implementation of NDCs and dedicated environmental institutional capacity are real measurement gaps — added to future enhancements.

---

### Concept 13: State capacity (structural core)

**Category:** State capacity
**Scope:** the structural ability of the state — extractive capacity (taxation), coercive capacity (monopoly on legitimate force, maintaining order), administrative capacity (functioning bureaucracy with territorial reach). Pure capability question — what the state CAN do, not how well it uses what it has or what it produces.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem state authority indicators (v2svstterr, v2svdomaut, related) | Primary tier 1 | Direct fit for administrative/territorial reach. ~180 countries, annual. Workhorse. |
| FSI Security Apparatus (C1) | Primary tier 1 | Direct measure of coercive capacity (state monopoly on force, competing armed actors). 179 countries, annual. |
| World Bank Informal Economy Database | **Dropped at Step-1** | 0% current sovereign coverage (series ends 2020, fails recency). Informality-as-state-reach was the rationale; no current data. See `framework_decisions.md`. |
| ILO social security coverage | Primary tier 2 | Formality via state administrative systems. ~150 countries. Direct measure of state reach. |
| Hanson-Sigman state capacity index | **Dropped at Step-1** | Series ends 2015, fails the 4-year recency window (the "last update 2021" note referred to the dataset release, not the data's latest year). See `framework_decisions.md`. |
| Hendrix state capacity measures | Dropped — supersession | Foundational paper (2010); subsequent update thin. Superseded by Hanson-Sigman. |
| Tax revenue / GDP (ICTD-UNU-WIDER, IMF GFS) | Dropped — S/N | Variation driven heavily by economic structure, tax base, political choices, informality. Low S/N for state extractive capacity proper. |
| WGI Government Effectiveness | Dropped — precision | Too broad. Used in GE+AQ concept. |
| Worldwide Bureaucracy Indicators | Dropped — precision | Measures bureaucracy size, not capacity. |
| FSI Public Services (P2) | Dropped — placement | In Service Delivery concept (output, not capability). |
| WB Statistical Performance Indicators | Dropped — placement | In Statistical Infrastructure concept. |
| Bockstette-Chanda-Putterman State Antiquity | Dropped — currency | Largely static historical measure. |
| SIPRI / IISS military personnel | Dropped — precision | Military size ≠ coercive capacity quality. FSI C1 captures concept more directly. IISS also paid. |
| Polity executive recruitment | Dropped — placement | Better placed in Legislative and constitutional checks. |
| QoG Expert Survey | Dropped — coverage/placement | Borderline coverage, content closer to admin quality than structural capacity. |
| PRS ICRG Bureaucracy Quality, Government Stability | Dropped — cost | Bundled risk product. |

**State of measurement:** good. V-Dem state authority + FSI C1 cover administrative reach and coercive capacity directly. Formality proxies (WB Informal Economy, ILO social security) cover state reach into economy and society. Extractive capacity has a documented measurement gap (no good cross-country measure surviving S/N filter) — added to future enhancements.

---

### Concept 14: Legal quality and predictability

**Category:** Rule of law
**Scope:** the narrowed residual rule-of-law concept after constituent concepts (judicial independence, personal security, property rights, corruption, legislative/constitutional checks) were separated. Captures: quality of the law itself (clarity, coherence, accessibility), equal treatment in non-judicial administrative contexts, congruence between formal law and actual practice, predictability of legal application beyond courts.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem v2cltrnslw (Transparent laws with predictable enforcement) | Primary tier 1 | Most direct single measure of the concept. Expert coding, ~180 countries, annual. |
| V-Dem v2clacjstw (Access to justice) - COLLAPSED from 2 to 1 (2026-07-24) | Primary tier 1 | Access-to-justice for women, kept. The men/women pair (v2clacjstm/v2clacjstw) was collapsed to one under the within-source collapse rule (methodology S6): they correlate r=0.96 - near-identical twins, the highest redundancy in any collapse. Unlike C17 property rights (where the gender split diverged interpretably via discriminatory inheritance law), physical/procedural access to justice is barely gender-differentiated, so the men metric added no distinct signal. Kept v2clacjstw (marginally the more binding constraint). ~180 countries. |
| V-Dem v2xeg_eqaccess (Equality before law) | Primary tier 1 | Direct fit for equality dimension. ~180 countries. |
| WJP Rule of Law — Factor 4 (Fundamental Rights) | Primary tier 1 | Direct fit for equal-treatment content. 142 countries (borderline). |
| WJP Rule of Law — Factor 3 (Open Government) | Primary tier 1 | Direct fit for accessibility of law dimension. 142 countries. |
| Comparative Constitutions Project — legal features | Primary tier 1 | De jure constitutional framework. Universal coverage. |
| WGI Rule of Law | Category-level cross-check | Too broad as concept primary (aggregates content split across constituent concepts). Used at Rule of Law category roll-up. |
| WJP Factor 2 (Corruption), Factor 6 (Regulatory Enforcement), Factor 7 (Civil Justice) | Dropped — placement | Each placed in dedicated primary concept (Corruption, Regulatory Quality, Judicial Independence). |
| V-Dem v2clrspct (Rigorous and impartial public admin) | Dropped — placement | In GE+AQ concept. |
| Freedom House Rule of Law sub-component | Dropped — placement | In Civil Liberties concept. |
| Mo Ibrahim IIAG, BTI, Bingham Centre | Dropped — coverage | Region or country-type specific. |
| PRS ICRG Law and Order | Dropped — cost | Cumulative subscription case weak. |

**State of measurement:** moderate. The narrowed residual is harder to isolate measurement-wise than the constituent concepts. V-Dem v2cltrnslw is the strongest single measure; selective WJP factor use rounds out. Score variation may be modest given high correlation between V-Dem indicators and WJP factors.

---

### Concept 15: Judicial independence and quality

**Category:** Rule of law AND Accountability (horizontal) — multi-placed
**Scope:** structural independence of the judiciary (appointment, tenure, budget, freedom from interference); quality of judicial functioning (competence, accessibility, timeliness, enforcement, impartiality); independence of prosecutors. Multi-placed: rule-of-law foundation AND horizontal accountability mechanism (judicial review).

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem judicial indicators (v2juhcind, v2juncind, v2jucomp, v2jupack, v2jupurge) | Primary tier 1 | Multiple direct precise measures of judicial independence across dimensions. Workhorse. ~180 countries, annual. |
| WJP Factor 7 (Civil Justice) | Primary tier 1 | Direct fit for judicial quality dimension. 142 countries (borderline). Full Factor 7 placed here per disciplined factor allocation. |
| WJP Factor 8 (Criminal Justice) | Primary tier 1 | Direct fit for criminal judicial quality. 142 countries. |
| Comparative Constitutions Project — judicial independence features | Primary tier 1 | De jure constitutional framework: appointment, tenure, salary protection, judicial review powers. Universal. |
| Linzer-Staton judicial independence latent variable | Supplementary | Methodologically sophisticated cross-check. Update frequency to verify at metric pass. *(Note: deprioritized elsewhere as stale; V-Dem supersedes.)* |
| Henisz Political Constraints Index (POLCON) | Supplementary | Captures judicial constraints on executive. Update concerns. |
| Polity5 components | Dropped — supersession | Largely superseded by V-Dem for current measurement. |
| WGI Rule of Law | Category-level cross-check | Used at Rule of Law category roll-up. |
| Freedom House Rule of Law sub-component | Dropped — placement | In Civil Liberties concept. |
| BTI, Mo Ibrahim, OECD/CEPEJ | Dropped — coverage | Region or country-type specific. |
| Doing Business Enforcing Contracts | Dropped — currency | Discontinued 2021. |
| CIRI Independence of Judiciary | Dropped — currency | Defunct since 2011. |
| Howard-Carey judicial independence | Dropped — currency | Not regularly updated since 2000s. |
| PRS ICRG, EIU | Dropped — cost | Bundled subscription products. |

**State of measurement:** strong. Among the better-measured concepts. Triangulation of de jure (CCP), expert-coded de facto (V-Dem), and survey-experienced (WJP) covers concept from multiple methodological angles.

---

### Concept 16: Personal security and order

**Category:** Rule of law
**Scope:** physical safety of persons and property in daily life; effectiveness of law enforcement; absence of pervasive crime and disorder; freedom from arbitrary state violence. Outcome-side dominated. Distinct from Political stability (regime-level disruption) and from State capacity coercive dimension (state ability to use force, not its restraint).

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| UNODC Homicide Statistics | Primary tier 1 | Gold standard cross-country violent crime measure. ~200 countries, annual. High S/N. |
| V-Dem physical violence and integrity indicators (v2cltort, v2clkill, v2clrgunev) | Primary tier 1 | Direct fit for state violence and physical integrity dimensions. ~180 countries, annual. |
| Political Terror Scale (PTS) | Primary tier 1 | State violence dimension: torture, political imprisonment, extrajudicial killings. ~190 countries since 1976. Also tier 2 in Civil Liberties (repetition tracked). |
| WJP Factor 5 (Order and Security) | Primary tier 1 | Direct fit; population polls + expert. 142 countries (borderline). |
| Global Peace Index — societal safety and security domain | Primary tier 2 | Pre-aggregated composite covering broader safety dimensions including terrorism. 163 countries, annual. |
| WGI Rule of Law | Category-level cross-check | Used at Rule of Law category roll-up. |
| FSI Security Apparatus (C1) | Dropped — placement | In State capacity (coercive dimension). Cleaner separation. |
| ACLED civilian violence, UCDP one-sided violence | Dropped — placement | Conflict event data; primary in Political Stability. |
| Numbeo Crime Index | Dropped — methodology | Crowdsourced; unreliable representativeness. |
| CIRI | Dropped — currency | Defunct. |
| UNODC Crime Victims Survey | Dropped — currency | Cross-country program discontinued. |
| Global Terrorism Database | Dropped — currency | Status uncertain post-2020. |
| Gallup Law and Order Index | Dropped — cost | Tier 4 paid. |
| PRS ICRG / EIU | Dropped — cost | Bundled. |

**State of measurement:** strong. UNODC homicide is the gold standard outcome measure with near-universal coverage. PTS and V-Dem physical integrity indicators are direct measures of state violence. Triangulation across observed outcomes, documentary review, expert coding, and population polls is methodologically diverse.

---

### Concept 17: Property rights and contract enforcement

**Category:** Rule of law
**Scope:** legal protection of property (physical, intellectual, financial) from arbitrary expropriation by state or seizure by private actors; effectiveness and predictability of contract enforcement; security of property registration and titling. Single-placed in Rule of law (dual placement with Economic and fiscal governance removed in framework refinement).

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem property rights - COLLAPSED 3 to 1 (2026-07-24) | Primary tier 1 | Kept the composite v2xcl_prpty only. Dropped the gendered components v2clprptym (men) and v2clprptyw (women) under the within-source collapse rule (methodology S6): both r>0.93 with the composite (Gate 1). Men's divergences are extreme-low-tail wobble (no decision-relevant distinction). Women's divergences ARE interpretable (Jordan/Cuba - women's rights lagging the general environment via discriminatory inheritance/marital law) - but that property-rights GENDER-GAP signal belongs in C22 (Civil liberties / gender, which already carries WB Women Business and the Law), not in C17's investor-facing expropriation/contract-enforcement scope (option (c): keep C17 focused on the general property environment). C17 stays adequately measured: composite + WJP no-expropriation + Fraser legal system, 3 independent sources. |
| Heritage Property Rights (Index of Economic Freedom component) | Primary tier 1 | Direct fit. ~180 countries, annual. Lower ideological loading than other Heritage components for this dimension. |
| Comparative Constitutions Project — property provisions | Primary tier 1 | De jure constitutional protections for property, expropriation rules, IP. Universal. |
| WJP Factor 6 sub-component 6.5 (No expropriation) | Primary tier 1 | Pulled specifically for this concept. Full Factor 6 stays in Regulatory Quality. |
| Fraser Legal System and Property Rights area — property sub-components only | Primary tier 2 | Selective use; judicial independence content stays in Judicial Independence concept. |
| WIPO IP data | Primary tier 2 | IP protection dimension specifically. ~190 countries. |
| WGI Rule of Law | Category-level cross-check | Used at Rule of Law category roll-up. |
| Doing Business Registering Property, Enforcing Contracts | Dropped — currency | Discontinued 2021. Historical reference. |
| B-READY property/enforcement content | Track for future | ~50 countries currently. |
| International Property Rights Index (IPRI) | Dropped — coverage/framing | 125 countries; below threshold. Hernando de Soto Institute framing. |
| BTI Property Rights | Dropped — coverage | Transformation countries. |
| PRS ICRG Investment Profile, EIU, Coface | Dropped — cost | Tier 4 subscription products. |
| Global Innovation Index Institutions sub-pillar | Dropped — precision | Broader composite. |

**State of measurement:** strong despite Doing Business discontinuation. V-Dem + Heritage + CCP triangulation works well. Operational/transactional data on property registration efficiency (Doing Business's strength) is genuinely lost; B-READY will eventually fill this. Captured structurally but thinner on operational dimensions.

---

### Concept 18: Control of corruption

**Category:** Rule of law
**Scope:** prevention of public power being exercised for private gain — grand corruption, petty corruption, state capture, illicit enrichment, conflict of interest violations, plus institutional infrastructure that prevents and addresses these (anti-corruption agencies, asset declaration regimes, prosecution effectiveness).

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem corruption indicators - COLLAPSED 5 to 3 (2026-07-24) | Primary tier 1 | Kept v2x_corr (composite), v2lgcrrpt (legislative corruption), v2jucorrdc (judicial corruption). Dropped v2excrptps (exec bribery) and v2exembez (exec embezzlement) under the within-source collapse rule (methodology S6). Rationale: EXECUTIVE corruption is the most-measured dimension in C18 already - it is what TI CPI, BCI, and WJP predominantly capture, plus it sits in the V-Dem composite - so the two V-Dem executive sub-metrics (r=0.89 with each other) add no distinct signal (Gate 2 fail). The legislative and judicial components were KEPT because they carry decision-relevant branch distinctions the composite blends away: countries split sharply on where corruption concentrates (Burkina Faso/Ghana corrupt-courts-clean-legislature vs PNG/Sri Lanka the reverse), and judicial corruption specifically threatens contract enforcement. This is the first collapse that KEEPS components over composite-only, because branch-specific corruption is genuinely distinct - the two-gate test protecting distinctive metrics as designed. |
| Transparency International Corruption Perceptions Index (CPI) | Primary tier 1 | Standard cross-country corruption measure. ~180 countries, annual. Aggregator of 13 sources of expert assessment and business surveys. |
| WJP Factor 2 (Absence of Corruption) | Primary tier 1 | Direct fit. Methodologically distinct (population polls + expert surveys, not aggregator). 142 countries (borderline). |
| Bayesian Corruption Indicator (BCI) | Primary tier 2 | Latent-variable cross-check using Bayesian item response model. ~190 countries. Update currency to verify. |
| WGI Control of Corruption | Category-level cross-check | Aggregator sharing many underlying sources with CPI. Used at Rule of Law category roll-up to avoid double-counting. |
| UNCAC review content | Supplementary | Tier 3 PDFs where extractable. |
| Basel AML Index, FATF compliance ratings | Dropped — placement | Primary in Financial Sector concept. Repetition would create double-counting. |
| Open Budget Survey | Dropped — placement | Primary in PFM. Indirect corruption relevance. |
| WEF Executive Opinion Survey | Dropped — double-counting | Input to CPI; using both creates redundancy. |
| Heritage Government Integrity | Dropped — redundancy | Largely derivative of CPI; not ideologically loaded but adds little marginal information. |
| BTI, Mo Ibrahim, OECD Anti-Corruption Convention, Global Corruption Barometer (borderline), regional barometers | Dropped — coverage | Region or country-type specific. |
| PRS ICRG, EIU | Dropped — cost | Bundled. |

**State of measurement:** very strong. Among the most heavily measured governance concepts. Triangulation of aggregator perception (CPI), expert coding (V-Dem), and population polls + expert surveys (WJP) provides methodologically distinct approaches. Perception endogeneity is partially mitigated by V-Dem's expert coding.

> *Note: the IDEA Political Finance Database (political-party and campaign-finance transparency, de jure, ~180 countries, built this cycle) is currently homed in Concept 25 but is also a natural anti-corruption transparency measure; flagged for possible cross-reference at metric pass.*

---

### Concept 19: Legislative and constitutional checks

**Category:** Accountability (horizontal) AND Rule of law — multi-placed
**Scope:** narrowed concept covering: legislative checks on executive (oversight powers, budget approval, ability to constrain executive action); constitutional architecture (separation of powers as designed); and non-corruption-focused independent oversight bodies (audit institutions, ombudsman offices — central bank independence is in Macro Framework; EMBs moved to Electoral Process per vertical accountability fit). Excludes judicial constraints (Judicial Independence) and corruption-focused oversight (Corruption).

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem legislative and executive constraint indicators (v2xlg_legcon and components: v2lgoppart, v2lgqstexp, v2lginvstp, v2lgotovst) | Primary tier 1 | Multiple direct precise measures of legislative oversight. Plus v2x_horacc (broader horizontal accountability index). ~180 countries, annual. |
| Comparative Constitutions Project — separation of powers and checks features | Primary tier 1 | De jure constitutional architecture. Universal coverage. |
| IPU Parline | ~~Primary tier 1~~ → **dropped from v1** | Scouted: **free** data via open REST API (`api.data.ipu.org`, 193 countries, daily, 500+ fields) — clean, automatable access. BUT licensed **CC BY-NC-SA (non-commercial)**, conflicting with the framework's commercial/investment purpose. Also largely redundant for legislative *checks*: V-Dem `v2xlg_legcon` + CCP + Polity cover the construct directly; Parline is structural/descriptive (chamber structure, oversight bodies), not a checks-strength index. Dropped on licence + redundancy; access route recorded if a non-commercial use or licence change ever reopens it. |
| Polity5 Executive Constraints (XCONST) | **Dropped at Step-1** | Series ends 2018, fails the 4-year recency window; V-Dem supersedes. (XCONST was never in the QoG extract regardless.) C19 is now single-source V-Dem. See `framework_decisions.md`. |
| WGI Voice and Accountability | Category-level cross-check | Aggregate; used at Accountability category roll-up rather than concept primary. |
| IDEA EMB Database | Dropped — placement | Moved to Electoral Process and Competition per vertical accountability fit. |
| INTOSAI audit institution data | Supplementary | Tier 3 fragmentary cross-country dataset. Use selectively where extractable. |
| Henisz POLCON | Dropped — precision | Partial fit for veto players. Cleaner direct measures available (V-Dem, IPU). |
| Database of Political Institutions (DPI) | Dropped — precision | Indirect fit. Captures institutional configuration rather than constraint strength. |
| Freedom House Government Functioning | Dropped — placement | Bundled in FH Political Rights. Used in Civil Liberties / Electoral Process via other sub-components. |
| BTI Separation of Powers | Dropped — coverage | Transformation countries only. |
| OECD Independent Fiscal Institutions Database | Dropped — coverage | ~50 countries. |
| ICRG | Dropped — cost | Bundled subscription. |

**State of measurement:** strong for legislative oversight and constitutional architecture dimensions. The independent oversight bodies dimension is leaner — covered mainly via V-Dem horizontal accountability indicators and (where extractable) INTOSAI fragmentary data. Future enhancement: cross-country audit institution and ombudsman effectiveness measurement.

---

### Concept 20: Electoral process and competition

**Category:** Accountability (vertical)
**Scope:** quality and integrity of electoral processes — free and fair elections, universal and effective suffrage, secret ballot, accurate vote tabulation; meaningful electoral competition (multiple viable parties, freedom to form parties, level playing field, peaceful transfer of power); electoral administration quality (EMB independence and capability).

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem electoral democracy and integrity indicators (v2x_polyarchy, v2elfrfair, v2elirreg, v2elintim, v2elvotbuy, v2elaccept) | Primary tier 1 | Multiple direct precise measures across electoral sub-dimensions. Workhorse. ~180 countries, annual. |
| Freedom House Electoral Process sub-component (FIW Political Rights A) | Primary tier 1 | Direct fit, broad coverage (~210 countries), annual. Disciplined extraction of just the Electoral Process sub-component. |
| Electoral Integrity Project (PEI) — Perceptions of Electoral Integrity | Primary tier 1 | Methodologically distinct expert survey covering 49 indicators across 11 dimensions. ~170 countries covered through past elections. Per-election cadence. |
| IDEA EMB Database | **Deprioritized — superseded** | EMB **independence/capability** dimension now filled by V-Dem **v2elembaut** (autonomy) + **v2elembcap** (capacity), added to the V-Dem pull (nb 03) — functional, ordinal, clean directionality. IDEA EMB's unique content is a **de jure model taxonomy** (Independent/Governmental/Mixed) with contested directionality (Independent ≠ better; Germany/Nordics/Switzerland run excellent elections on governmental/mixed models), not worth a bespoke contested-scoring build. Note: IDEA's own GSoD EMB-autonomy indicator is V-Dem v2elembaut re-served. |
| NELDA (National Elections Across Democracy and Autocracy) | SCORED - Supplementary (2026-07-24) | 5 binary election-quality flags scored into C20: concerns-not-free-fair (NELDA11), media-bias-incumbent (NELDA16), riots-protests-after, violence-deaths-before (NELDA33) all direction NEGATIVE; opposition-allowed direction POSITIVE. Tier revised from the source-level 'Primary tier 2' DOWN to Supplementary during scoring: C20 already has 10 P1 metrics, and NELDA is sparse (event-level, ~24.5% of country-years, one obs per country-year) and systematically ABSENT for ~21 consolidated democracies excluded by NELDA's design (absence implies established-democracy = implicitly clean - a coverage bias for scaling). IMPORTANT: the QoG pipeline's original NELDA renames were WRONG (e.g. mbbe mislabeled 'multiple_parties' but is media bias; rpae mislabeled 'ruling_party_advantage' but is post-election riots; fme direction-inverted) - corrected in nb 14 against the NELDA/QoG codebook, with raw 99 (unclear) -> NaN. Excluded: mtop (near-zero discrimination 0.964 vs 1.000), election-type descriptors (type-not-quality). |
| IDEA Voter Turnout Database | Keep for metric pass | Compulsion adjustment not made by IDEA. Metric-level decision: either adjust manually or accept noise. Kept on table. |
| Polity5 electoral indicators | Supplementary | Largely superseded by V-Dem for current measurement. |
| Comparative Constitutions Project — electoral provisions | Supplementary | De jure framework reference. |
| Database of Political Institutions (DPI) | Supplementary | Institutional context. |
| WGI Voice and Accountability | Category-level cross-check | Used at Accountability category roll-up. |
| OSCE/ODIHR election observation | Dropped — coverage | OSCE region only (~57 countries). |
| EU EOMs, OAS, Carter Center, NDI, IRI observation | Dropped — coverage | Selective per-election; not standardised cross-country dataset. |
| BTI Stateness / Political Participation | Dropped — coverage | Transformation countries. |
| EIU Democracy Index — Electoral Process component | Dropped — cost/borderline | Borderline coverage plus paid. |

**State of measurement:** very strong. Among the best-measured concepts. Triangulation across V-Dem (incl. EMB autonomy/capacity, nb 03), PEI, FH, and NELDA provides methodologically diverse measurement with broad coverage; the electoral-administration (EMB) leg is covered by V-Dem, with the standalone IDEA EMB Database deprioritized.

---

### Concept 21: Political participation beyond voting

**Category:** Accountability (vertical)
**Scope:** forms of political engagement beyond electoral voting — protest participation, civic engagement, deliberative participation, party and association membership, contacting officials, signing petitions, online political activity. Earlier flagged as having thin economic relevance among the concepts.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem participation indicators (v2x_partip, v2psprlnks, v2pscohesv, v2cseeorgs, v2dlconslt, v2csreprss) | Primary tier 1 | Multiple direct precise measures, broad coverage (~180 countries), annual. Workhorse. |
| CIVICUS Monitor | Primary tier 1 | Civic space conditions (whether participation is possible). 197 countries/territories. Annual. Categorical scoring. |
| IDEA Global State of Democracy - Participation attribute | SCORED (2026-07-24): composite P1 + local-democracy P2 | Scored 2 metrics into C21: idea_participation (the Participation attribute, 0-1, 174 countries 1990-2025) at P1, and idea_local_democracy at P2. **P1 placement** (revised UP from the source-level 'Primary tier 2') because C21 is otherwise V-Dem-dominated - 6 of 7 existing metrics are V-Dem (its v2x_partip composite plus 5 facets) and CIVICUS covers only 2022+, so GSoD is the main INDEPENDENT full-history participation measure. local_democracy added at P2 as the sharpest democracy/autocracy discriminator in the cluster (gap 0.85) and only moderately correlated with the composite (r=0.744). Excluded: civil_society (r=0.98 redundant), civic_engagement (r=0.83 redundant), electoral_participation (weak discriminator gap 0.21; duplicates C20), direct_democracy (degenerate, mean 0.089). Validated: Denmark 0.96 to North Korea 0.03. |
| World Values Survey (WVS) | Dropped — coverage/currency | Gold-standard methodology but borderline coverage (~100 cumulative) and wave-based timing creates currency issues. |
| WGI Voice and Accountability | Category-level cross-check | Used at Accountability category roll-up. |
| ACLED protest event data, Mass Mobilization Project | Dropped — precision | Measure events not engagement. Used in Political Stability instead. High event count can reflect engaged citizenry OR dysfunctional governance. |
| Freedom House Associational and Organizational Rights | Dropped — placement | In Civil Society Space concept. |
| IDEA Voter Turnout | Dropped — concept fit | Voting, not non-voting participation. Plus compulsion adjustment issue. |
| Regional barometers (Afrobarometer, Latinobarómetro, Asian Barometer, etc.) | Dropped — coverage | Region-only individually. |
| BTI Political and Social Integration | Dropped — coverage | Transformation countries. |
| EIU Democracy Index — Political Participation | Dropped — cost | Tier 4 paid. |

**State of measurement:** moderate. Limited methodological diversity in primary measurement (V-Dem with CIVICUS as secondary). The score will be driven largely by V-Dem. Combined with the previously flagged thin economic relevance of this concept, weighting in the framework should reflect both factors.

---

### Concept 22: Civil liberties

**Category:** Accountability (vertical)
**Scope:** residual civil liberties concept after Media freedom and Civil society space are split out. Covers freedom of expression (non-media), freedom of religion, personal autonomy and privacy, freedom of movement, freedom from arbitrary detention, LGBTQ+ rights, women's rights and gender equality, minority rights.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| Freedom House Freedom in the World — Civil Liberties sub-categories D and G (disciplined extraction) | Primary tier 1 | D (Freedom of Expression and Belief), G (Personal Autonomy and Individual Rights). Direct fit with disciplined extraction. ~210 countries, annual. E reserved for Civil Society Space; F (Rule of Law) overlaps with Rule of Law cluster. |
| V-Dem civil liberties indicators - COLLAPSED 7 to 6 (2026-07-24) | Primary tier 1 | Kept v2x_civlib (broad CL index matching the concept scope), v2clrelig (religion), v2cldmovem + v2cldmovew (movement, men and women), v2clsocgrp (social group equality), v2clslavef (freedom from forced labour). Dropped v2x_clpriv, the SECOND index (r=0.96 with v2x_civlib) - the concept was scoring the same aggregate twice, and v2x_clpriv is an aggregate of exactly the components retained individually, so keeping both double-counts. NOTE the components here are the most DISTINCT of any V-Dem cluster examined: v2clsocgrp r 0.59-0.69, v2clslavef r 0.59-0.75, and the movement gender pair r=0.81 (real signal, unlike C14's r=0.96 access-to-justice twins - legal restrictions on women's movement genuinely diverge from men's in some jurisdictions). |
| Pew Government Restrictions Index (GRI) and Social Hostilities Index (SHI) | Primary tier 2 | Religious freedom dimension specifically. ~200 countries, annual. Tier 2 rather than tier 1 because religious freedom is less central to political accountability than political expression/dissent (centrality principle). |
| Political Terror Scale (PTS) | Primary tier 2 | State violence dimension — state political imprisonment etc. as civil liberties violations. Also primary in Personal Security (repetition tracked, not prohibited). |
| World Bank Women, Business and the Law | Primary tier 2 | Gender equality dimension. 190 countries, annual. Direct legal protections measurement. High S/N. |
| US State Department Country Reports on Human Rights Practices | Supplementary | Rich content; Tier 3 extraction cost real. |
| WGI Voice and Accountability | Category-level cross-check | Used at Accountability category roll-up. |
| ILGA-World Sexual Orientation Laws Map | Dropped — user direction | Generally captured by FH and V-Dem at concept level; user preferred to drop dimension-specific source for LGBTQ+ rights. |
| Equaldex Equality Index | Dropped — methodology/user direction | Less established methodology. Dropped. |
| OECD SIGI | Dropped — user direction | Extending logic from WB WBL decision; though SIGI is gender-broader, kept lean per user preference. |
| Freedom House Associational Rights (sub-category E) | Dropped — placement | In Civil Society Space concept. |
| Freedom House Rule of Law (sub-category F) | Dropped — placement | Rule of Law cluster. |
| Freedom on the Net | Dropped — coverage | ~70 countries. Future enhancement. |
| CIRI | Dropped — currency | Defunct. |
| Amnesty / HRW reports | Dropped — currency/structure | Tier 3 unstructured. |
| BTI Civil Liberties content | Dropped — coverage | Transformation countries. |
| USCIRF religious freedom | Dropped — coverage | Country-selective focus. |
| EIU Democracy Index Civil Liberties | Dropped — cost | Tier 4 paid. |

**State of measurement:** strong. Multiple methodologically distinct sources with broad coverage. Disciplined sub-component extraction from FH addresses the bundling issue cleanly. Internet/digital freedom dimension is under-measured cross-country (Freedom on the Net fails coverage); future enhancement. OVER-FLAG DISPOSITION (2026-07-24): C22 remains flagged OVER at 14 metrics, but this is LEGITIMATE BREADTH, not redundancy - 14 metrics across 5 genuinely different sources (V-Dem, Pew religious-freedom, WB Women Business and the Law, PTS, Freedom House) measuring distinct civil-liberties facets. The collapse pass found only ONE redundant metric here (the duplicate index). The residual is a Step-4 weighting matter, like C8, not a trimming one. Related: C17's collapse left open whether the property-rights gender gap should move here - resolved NO, the gender dimension is already well covered by WB WBL (3 metrics) plus the movement gender pair; adding it would duplicate WBL legal-framework content.

---

### Concept 23: Media freedom and pluralism

**Category:** Accountability (vertical)
**Scope:** freedom of media to operate without state interference; journalist safety; independence of broadcast and print media from political and economic capture; pluralism of media voices; freedom of internet/digital media; access to information.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| Reporters Without Borders (RSF) — World Press Freedom Index | Primary tier 1 | Standard cross-country press freedom measure. 180 countries, annual. Pluralism, independence, environment/self-censorship, legislative framework, transparency, safety, plus quantitative abuses indicator. |
| V-Dem media indicators - COLLAPSED 8 to 5 (2026-07-24) | Primary tier 1 | Kept: v2x_freexp_altinf (composite), v2mecorrpt (media corruption channel), v2merange (range of perspectives / pluralism), v2mecenefm (censorship channel), v2mebias (bias / propaganda channel). Dropped 3 as redundant under the within-source collapse rule (methodology S6, two-gate test): v2meharjrn (harassment), v2meslfcen (self-censorship), v2mecrit (critical coverage) - each highly correlated with the composite (Gate 1) AND their divergences from it are clean-end scale/ceiling noise, not material distinctions (Gate 2 failed). The 5 kept were each retained for distinct decision-relevant signal despite high correlation - e.g. media corruption isolates bribery-vs-state-control (Vietnam/HK controlled not corrupt), range isolates pluralism (Iraq dangerous-but-plural). |
| Committee to Protect Journalists (CPJ) — journalist safety data | Primary tier 1 — **Built** (`cpj_clean.csv`, nb 36) | AUTOMATED via CPJ public REST API. Three per-country measures: journalists imprisoned (live census snapshot), journalists murdered (3-yr rolling window, motive=Murder, derived from CURRENT_YEAR), and unsolved/Complete-Impunity murders (same window). 50 countries with ≥1 incident; all other framework countries are true zeros (tail-severity signal capturing two distinct repression modes — detention vs lethal violence). ISO2 from API, ISO3 via pycountry. Israel/OPT lumped under ISR by CPJ (flag for metric pass). Impunity is slow-moving / ~collinear with murdered over a short window. |
| Freedom House Freedom in the World — Civil Liberties sub-category D | Primary tier 2 | Disciplined extraction. Repetition with Civil Liberties tracked. |
| Centre for Law and Democracy / Access Info Europe — RTI Rating | Primary tier 2 | RTI legislation quality. 138 countries (borderline coverage). Also used in Government Transparency. **Built** (automated, 196 countries incl. no-law). |
| UNESCO Journalist Killings Observatory | Supplementary | Overlaps CPJ; adds prosecution dimension. |
| Article 19 Global Expression Report | Supplementary | Composite drawing on V-Dem (double-counting concern). Use as cross-check only. |
| WGI Voice and Accountability | Category-level cross-check | Used at Accountability category roll-up. |
| Freedom House Freedom of the Press | Dropped — currency | Discontinued in 2017. Media content moved to FIW sub-category D. |
| Freedom on the Net | Dropped — coverage | ~70 countries. Internet/digital freedom dimension under-measured cross-country. |
| Media Ownership Monitor (RSF/Global Media Registry) | Dropped — coverage | ~20 countries with completed monitors. |
| CIRI Freedom of Speech | Dropped — currency | Defunct. |
| BTI Media | Dropped — coverage | Transformation countries. |
| EIU Democracy Index Civil Liberties | Dropped — cost | Tier 4 paid. |

**State of measurement (build-verified):** strong, build-complete. Methodologically distinct primary sources triangulate: V-Dem (expert-coded latent press-freedom climate), FH-FIW CL-D (analyst-coded), RTI Rating (de jure legal framework), and CPJ (objective verified event-counts of journalist imprisonment/murder/impunity). CPJ's construct is largely unique — the expert/legal indices do not produce hard counts of jailed/killed journalists — so it adds distinct measurement rather than redundancy. Main gap: internet/digital media freedom universal-coverage measurement and media ownership concentration cross-country measurement. Future enhancements. NOTE: V-Dem media collapsed 8->5 metrics (2026-07-24) to remove redundancy; residual V-Dem weight vs the independent sources (CPJ x2, FH, RTI) is a deliberate Step-4 weighting item - V-Dem is the higher-quality comprehensive source and may carry more weight by design, but via deliberate weight, not metric count.

---

### Concept 24: Civil society space and vitality

**Category:** Accountability (vertical)
**Scope:** the space within which civil society operates (freedom to form associations, NGOs, trade unions, advocacy groups; freedom from harassment and restriction) and the vitality of that civil society sector (active presence of CSOs, breadth of engagement, capacity, independence from state and corporate capture). Distinct from Political participation beyond voting (engagement levels) and Media freedom.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem CSO indicators (v2cseeorgs, v2csreprss, v2cscnsult, v2csprtcpt) | Primary tier 1 | Multiple direct precise measures across CSO dimensions. ~180 countries, annual. |
| CIVICUS Monitor | Primary tier 1 | Standard civic space measure. 197 countries/territories. Direct fit. Categorical scoring (5 levels). |
| Freedom House Freedom in the World — Civil Liberties sub-category E (Associational and Organizational Rights) | Primary tier 1 | Direct fit, broad coverage. Per disciplined FH sub-component extraction, the natural home for E. |
| ICNL Civic Freedom Monitor | Supplementary | De jure legal framework reference. Uneven coverage. |
| ILO CEACR | Supplementary | Trade union dimension compliance. Tier 3 access. |
| WGI Voice and Accountability | Category-level cross-check | Used at Accountability category roll-up. |
| ITUC Global Rights Index | Dropped — ideological framing | Workers' rights ratings. ITUC is an interest group rather than neutral observer. Trade union dimension captured via ILO CEACR supplementary instead. |
| CIVICUS Civil Society Index (separate from Monitor) | Dropped — coverage/currency | ~70 countries historically; discontinued/irregular. |
| Johns Hopkins Comparative Nonprofit Sector Project | Dropped — currency | ~45 countries historically; updates ceased ~2013. CSO sector size measurement is a real gap. |
| WJP Rule of Law Index | Dropped — precision | Less direct fit than dedicated civic space sources. |
| BTI Stateness / Political and Social Integration | Dropped — coverage | Transformation countries only. |
| EIU Democracy Index | Dropped — cost | Tier 4 paid. |

**State of measurement:** strong on civic space dimension. Weaker on CSO vitality (size, capacity, sectoral breadth) — Johns Hopkins data defunct, no good universal replacement. Vitality measurement is captured indirectly through V-Dem participatory environment indicators. Future enhancement: cross-country CSO sector size and capacity measurement.

---

### Concept 25: Government transparency and openness

**Category:** Accountability (vertical)
**Scope:** transparency of government operations and decision-making; openness of government information to citizens; access to information (FOI/RTI laws and effective implementation); proactive disclosure; transparency in public procurement, lobbying, party finance; open government data initiatives.
**Note on concept status:** significant indicator overlap with other concepts (only the IDEA Political Finance Database and Global Data Barometer are unique to this concept; the rest are also used elsewhere). **Decision (revisited 2026-06-18): KEEP as its own concept** — coherent, investor-legible dimension; overlap tracked under the repetition rule. Still flagged to revisit with the full framework view before finalising.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem transparency-relevant indicators (v2cltrnslw, v2dlconslt, related) | Primary tier 1 | Multiple direct measures. v2cltrnslw also primary in Legal Quality; v2dlconslt also in Political Participation. Repetition tracked. |
| WJP Rule of Law Index — Factor 3 (Open Government) | Primary tier 1 | Direct fit for FOI/RTI/civic participation/complaint mechanisms. Also primary in Legal Quality (repetition tracked). |
| Centre for Law and Democracy / Access Info Europe — RTI Rating | Primary tier 1 | FOI/RTI legislation quality. Also used in Media Freedom. **Built** (automated; 142 rated + 54 no-law = 196 countries; de jure only). |
| Open Budget Survey (IBP) | Primary tier 2 | Budget transparency dimension. Also primary in PFM (repetition tracked). |
| IDEA Political Finance Database | Primary tier 2 | Political party and campaign finance transparency. ~180 countries. Unique to this concept. **Built** (automated; de jure; 20 directionally-curated questions → polfin_transparency_integrity 0–1). *(Source originally listed as "TI Political Finance"; the structured data is International IDEA's; retained source-id TI_POLFINANCE for continuity.)* |
| Open Data Inventory (ODIN) | Supplementary | Primary in Statistical Infrastructure. Useful cross-reference here; covers the open-data dimension. **Built.** |
| Global Data Barometer | **Deprioritized — not built** | Listed in the May version as the open-data supplementary (successor to defunct Open Data Barometer). On review: thin (~43–109 countries, edition-unstable, not a panel), duplicates ODIN's open-data coverage, and does not fill this concept's real gaps (procurement, lobbying, de facto practice). Deliberate departure; see changelog. |
| WGI Voice and Accountability | Category-level cross-check | Used at Accountability category roll-up. |
| Open Government Partnership (OGP) — IRM data | Dropped — coverage | 75 OGP members only; non-OGP systematically missing. |
| Open Data Barometer (Web Foundation) | Dropped — currency | Defunct. |
| Construction Sector Transparency Initiative (CoST) | Dropped — coverage | ~20 member countries; sector-specific. |
| EITI (Extractive Industries Transparency Initiative) | Dropped — coverage | 56 implementing countries; sector-specific. |
| TI Government Defence Integrity Index | Dropped — coverage | 87 countries (borderline); sector-specific. |
| WB Open Data Readiness Assessment | Dropped — coverage | ~50 countries. |
| BTI, SGI | Dropped — coverage | Region or country-type specific. |
| EIU Democracy Index | Dropped — cost | Tier 4 paid. |

**State of measurement:** mixed. Legal-framework legs are well-measured (RTI Rating, Open Budget Survey, IDEA Political Finance, V-Dem disclosure). Open government / open data dimension is thinner cross-country with currency issues (served adequately by ODIN). Sector-specific transparency (procurement, lobbying, defence, extractives) and de facto vs de jure implementation have real measurement gaps. De facto RTI implementation (rti-evaluation.org) assessed and deprioritized — too thin/heterogeneous; partial V-Dem coverage. Future enhancements: cross-country open data, procurement transparency, lobbying transparency, de facto vs de jure implementation.

---

## Changelog — design-level changes since the May 2026 master

> **This changelog is FROZEN (2026-07-24).** It recorded the May-to-July 2026 migration from the original PDF. The `.md` is now the living master, edited directly, with **git history as the record of subsequent changes**. New design decisions are made in place in the sections above, not appended here. The entries below are retained as the historical migration record.

This section records substantive design-level decisions made after the May 2026 PDF version. Build mechanics (notebooks, file paths, access methods, data currency) live in `docs/framework_decisions.md`, `data/processed/source_registry.csv`, and the download log; only decisions that affect the framework's *design* (concepts, source roles, source dispositions) are recorded here.

**2026-07-10**

- **Coverage characterized + reliability approach locked (Step 0.5).** Per-country coverage tabulated (`country_coverage.csv`): sovereigns carry 84–385 metrics (median ~358), the sparse tail is exclusively territories. Metric inclusion rule (§4) and D7 reliability flags (§8, per-concept, <50% present = low-confidence, a revisitable default) locked in `metric_methodology.md`. Coverage tables are tracked data, not embedded here.
- **Framework scope revised — country spine locked at ALL economies (213; 21 territories flagged).** The original target universe (~150–160 countries, population >2M, excluding closed regimes) is replaced by the full spine of all economies with WDI population data, excluding only PRK/ERI/TKM; non-sovereign territories (HKG, PRI, etc.) are included and flagged (`is_territory`). Rationale: the 2M line cut through investable sovereigns (Latvia, Estonia, Guyana, Suriname, Brunei, Iceland), and thin coverage is carried by reliability flags (option A) rather than exclusion. Spine: `data/processed/country_spine.csv` (nb 39); harmonization layer: `src/country_harmonization.py`; methodology detail: `docs/metric_methodology.md` §2. Source-selection coverage judgments (working principle 1) remain benchmarked to the ~150–160 sovereign core, not the full spine.

**2026-07-09**

- **Concept 9 (Financial-sector regulatory & supervisory quality) — banking de jure leg BUILT (WB BRSS, nb 38).** The Barth-Caprio-Levine Bank Regulation and Supervision Survey — the master's planned supplementary banking source — is now built (`wb_brss_clean.csv`). Bespoke construct-aligned **de jure** regulatory-stringency score (9 sub-constructs, 56 scored items, 5 reverse-coded; NOT the published BCL indices, whose 2019 question-to-index mappings are unavailable); Activity Restrictions excluded (contested directionality); provisioning/macropru trimmed of prescriptive items penalizing IFRS-9. 161 jurisdictions (155 reliable); rules-on-paper, NOT supervisory effectiveness (validated vs Anginer et al. 2019). Frozen irregular survey → manual 6th-wave check (see instructions_data_maintenance.md). **Effect on Concept 9 disposition:** AML/CFT (FATF) and banking-regulation de jure (BRSS) now built; FSAP's residual marginal value concentrates on securities (IOSCO), insurance (IAIS), and supervisory effectiveness, still deferred to the Category-1 PDF batch.
- **WTO TFA (Concept 11) — DROPPED on licence.** Access is now solved (a bulk Notifications Matrix XLSX exists at tfadatabase.org — all members × 36 measures × Cat A/B/C), overturning the earlier "deferred to scrape" assessment. But WTO material requires written permission for commercial use (no open dataset licence), conflicting with the framework's commercial/investment purpose — the same test that dropped IPU Parline. Admin dimension already triangulated via LPI + TFI; TFA is self-reported *commitment*, not de facto performance. Revisitable only via a WTO permission request.
- **IDEA EMB Database (Concept 20) — DEPRIORITIZED; EMB leg closed via V-Dem.** The electoral-administration (EMB independence/capability) sub-dimension named in C20 scope is now filled by V-Dem v2elembaut (autonomy) + v2elembcap (capacity), added to the V-Dem pull (nb 03): functional, ordinal, clean-directional. The standalone IDEA EMB Database (a designated primary) is deprioritized — its unique content is a de jure model taxonomy with contested directionality, not worth a bespoke build, and IDEA's own GSoD EMB-autonomy indicator is itself V-Dem v2elembaut re-served.

**2026-06-18**

- **Concept 25 (Government transparency and openness) — KEEP.** The May version flagged this concept for reconsideration due to heavy overlap. Decision: keep as a standalone concept (coherent, investor-legible; overlap tracked under the repetition rule). The architectural argument for absorption (it is thematically rather than functionally defined) was considered and not adopted; still flagged to revisit before finalising.
- **Global Data Barometer — DEPRIORITIZED.** Previously the designated open-data supplementary for Concept 25. On review: thin (~43–109 countries, edition-unstable, not a panel), duplicates ODIN's coverage, and does not fill the concept's real gaps (procurement, lobbying, de facto practice). Open-data leg now served by ODIN. Deliberate departure from the May spec.
- **AREAER capital-account dimension — RESOLVED with three complementary sources.** The IMF AREAER portal was confirmed WAF-blocked and JS-gated (not automatable). Resolution: (1) **IMF AREAER FARI** — capital-account restrictiveness, de jure, IMF-native, obtained by manual export (194 countries, 1999–2024; FARI aggregate + FDI sub-index); (2) **Chinn-Ito KAOPEN** — the most-cited academic derivative of AREAER, automated, broad time series (cross-check, not more authoritative than AREAER); (3) **exchange-rate regime** — sourced from the IMF AREAER *de facto* classification (IMF-native, current to April 2025, ~195 jurisdictions), which supersedes Reinhart-Rogoff as the current-state primary; **Reinhart-Rogoff demoted to supplementary** (independent parallel-market-aware cross-check, data ends ~2019). The AREAER de-facto table is a borderless PDF matrix (IMF Annual Report Appendix II.9 p20; programmatic fetch WAF-blocked, `extract_tables` finds no grid) → **hand-transcribed and validated against the PDF's row + column count checksums → BUILT** (`37_areaer_defacto_er_pipeline.ipynb` → `areaer_er_clean.csv`, 195 jurisdictions, as-of 2025-04-30; annual refresh edits only the source CSV — see instructions_data_maintenance.md). The AREAER Change Index (ACI) was obtained but not built (measures policy change, not level; deferred supplementary).
- **IRENA Renewable Energy Policies Database — DEPRIORITIZED.** No clean downloadable renewable-policy dataset exists; IRENA's policy work is report-based, and the joint IEA/IRENA Policies DB has no clean renewable filter and would duplicate Climate Laws. Renewable deployment covered by IRENA capacity statistics; energy/climate policy by Climate Laws; carbon pricing by WB Carbon.
- **rti-evaluation.org (de facto RTI implementation) — DEPRIORITIZED.** Bespoke per-country reports, handful of countries, heterogeneous — not a comparable cross-country panel. De facto RTI implementation remains a known v1 gap, partially covered by V-Dem transparency/disclosure practice measures. Flagged as a watch item.
- **Concept count.** Working inventory updated from 25 to 26 unique concepts (Concept 11 trade/state-control refinement); SOE governance remains deferred to v2.
- **2026-07-21 — D6 weighting resolved.** Categories equal-weighted; concept weights equal within category with Trade (11) and Environmental (12) at half; measurement-quality multiplier and missingness penalty locked as mechanisms (parameters at Step 1); relevance-annotation worksheet retired. Full spec: `metric_methodology.md` §7.
- **2026-07-21 — Concept 10 split; state control un-deferred into v1.** The *state control over the economy* dimension is now LIVE, scored via V-Dem v2clstown (own-or-control of important economic sectors; 179/179 coverage, interval-scored) — the ~50-country OECD coverage gap that forced deferral does not apply to v2clstown. *SOE governance quality* is split out and remains deferred to v2 (still only ~50-country OECD sources; v2clstown measures extent of control, not SOE-governance quality). Directionality (more control = worse, likely non-monotonic/threshold) deferred to D3. Single-indicator concept → flagged for §8 weight-review; may pair a second state-footprint source at Step 1. Headline inventory unchanged (25 unique / 29 instances), but all 25 now scored. Full record: `framework_decisions.md`.
- **2026-07-17 — concept-count recount + C10 broadened + relevance-annotation status corrected.** Inventory reconciled to **25 unique / 29 instances** (the 26 count never accounted for the GE+PAQ merge). Concept 10 broadened to **“SOE governance and state control over the economy”** (deferred v2; state-control folded in after being dropped from v1 on measurement grounds; split-vs-merge is an open v2 question). Corrected the false claim that economic-relevance annotations exist for concepts 1–9: verified they were never systematically done; annotation worksheet `economic_relevance_worksheet.md` created as the Step-1 input to D6.
- **Sources confirmed stale/superseded:** Dincer-Eichengreen CB Transparency (Romelli CBI supersedes), Linzer-Staton (V-Dem judicial indicators supersede).
- **PEFA — BUILT as a structured pipeline (not PDF); scope locked to 2016/national.** PEFA was slated for the Category-1 PDF-extraction batch, but its "Scores Downloads" facility exports A–D indicator/dimension scores as a CSV — so it is a structured manual-download pipeline (`33_pefa_pipeline`), not PDF parsing. Scope decided on evidence: **core = 2016 framework, national, latest assessment per country (85 countries, median assessment year 2022, all ≤9 yrs old)**. The 2011-framework backfill (35 additional national countries) was **deferred** because its investment-relevant names (Brazil 2009, India 2010, Norway 2008) are 16–18 years stale — current 55% coverage judged better than stale 77%. `assessment_year` is carried as a recency flag; the framework version is a single documented knob (`PEFA_FRAMEWORK`). The 2011 backfill is revisitable — narrowly and flagged — at PFM-concept assembly.
- **ICNL — dropped from the PDF batch, retained as supplementary.** The Civic Freedom Monitor is HTML qualitative country notes (de jure CSO law, ~50 countries), not PDF and not a scored dataset; redundant-for-scoring with the automated CIVICUS Monitor (de facto, ~197 countries) plus V-Dem civil-society indices. Stays registered as `tier3_web`, supplementary; no pipeline built.

> **Note on numbering.** Several concept numbers in this document differ from the May version because the working inventory expanded to 26 and some concepts were reordered. The category assignments and source decisions are the authoritative content; numbering is a navigational convenience.

