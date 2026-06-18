# Governance Framework — Master Document

*Framework architecture, principles, source-level measurement decisions for 26 concepts, future enhancements, and outstanding work.*

> **Document status.** This is the editable Markdown master, reconstructed from the May 2026 PDF and updated to reflect design-level decisions taken since. **As-of: 2026-06-18. MANUAL SNAPSHOT — does not auto-update.** Pipeline build status, data currency, and code are tracked separately in `docs/framework_decisions.md`, `data/processed/source_registry.csv`, and the download log. A dated changelog of substantive changes since the May version appears at the end of this document.

---

## Purpose

This framework provides a structure for assessing governance quality at the national level, oriented to the question of how governance affects economic and development outcomes. It is designed to apply across sovereign jurisdictions (target population >2 million, excluding effectively closed regimes), supporting cross-country comparison and analytical decomposition of governance into substantively meaningful dimensions. The ultimate use case is investment decisions — whether to allocate capital to a country — with this framework providing the governance assessment piece. Sovereign credit, macroeconomic vulnerability, and other risk factors live outside this framework in separate modules.

The framework draws on academic measurement projects (V-Dem, Polity, Quality of Government Institute, others), multilateral institutions (World Bank, IMF, OECD), think tanks and NGOs (Freedom House, Bertelsmann, Mo Ibrahim, World Justice Project, Transparency International, RSF, CIVICUS, IDEA, Pew), and ratings agency methodologies where relevant.

---

## Framework structure and primary measurement sources

The framework organises governance into **5 categories** containing **26 unique concepts** (30 total instances after multi-placement of 4 concepts). The table below summarises categorisation alongside the primary and secondary measurement sources selected for each concept at the source-level pass. Detailed source-by-source rationale (including sources considered but excluded) appears in the per-concept sections.

> **Note on concept count.** The May version described 25 unique concepts (29 instances). Concept 11 (State control over the economy / Trade governance numbering) and subsequent refinements bring the working inventory to 26 concepts; SOE governance remains deferred to v2. Concept numbering in the per-concept sections below follows the current working order.

| Category | Concept | Primary sources | Secondary / supplementary |
|----------|---------|-----------------|---------------------------|
| **1. Political foundations** | Political settlement | V-Dem power-distribution indicators; FSI Factionalized Elites (P1); FSI Group Grievance (S1); DPI party fragmentation; Powell-Thyne coups | (none selected as supplementary tier) |
| | Political stability and regime durability | WGI Political Stability; V-Dem regime duration; Powell-Thyne coups; UCDP and/or ACLED; GPI; WJP Factor 5 | Polity Durable (cross-check); GTD (currency caveat); MMP; ICRG/EIU (optional paid) |
| **2. State capacity** | State capacity | V-Dem state authority indicators; FSI Security Apparatus (C1) | WB Informal Economy Database; ILO social security coverage; Hanson-Sigman state capacity |
| | Statistical and informational infrastructure* | World Bank SPI; Open Data Inventory | IMF SDDS subscriptions |
| | Government effectiveness and admin quality | WGI Government Effectiveness; V-Dem Rigorous and Impartial Public Admin (v2clrspct) | WJP Regulatory Enforcement (borderline); QoG Expert Survey impartiality/Weberianism (borderline) |
| | Service delivery and provision of public goods | WB WDI sector indicators; WHO GHO; UNESCO UIS; UNDP HDI sub-indicators; WB Human Capital Index; FSI Public Services (P2) | (none — concept measured directly from sector-specific sources) |
| | Regulatory quality* | WGI Regulatory Quality; WJP Regulatory Enforcement (Factor 6) | Heritage Business Freedom; Fraser Regulation area (with framing caveats) |
| **3. Accountability (horizontal)** | Legislative and constitutional checks* | V-Dem legislative constraint indicators (v2xlg_legcon and components); CCP separation-of-powers features; IPU Parline | Polity5 XCONST (with supersession caveat) |
| | Judicial independence and quality* | V-Dem judicial indicators; WJP Factors 7 and 8; CCP judicial independence features | Linzer-Staton latent variable; Henisz POLCON |
| **Accountability (vertical)** | Electoral process and competition | V-Dem electoral indicators; FH Electoral Process sub-component; Electoral Integrity Project (PEI); IDEA EMB Database | NELDA; IDEA Voter Turnout (compulsion adjustment needed); Polity electoral indicators; CCP electoral provisions; DPI |
| | Political participation beyond voting | V-Dem participation indicators; CIVICUS Monitor | IDEA Global State of Democracy Participatory Engagement subindex |
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
| | Macroeconomic policy framework quality | Romelli CBI Index; IMF Fiscal Rules Database; IMF AREAER (FARI); Chinn-Ito KAOPEN; IMF iMaPP; IMF AREAER de-facto ER classification (deferred — PDF batch) | Reinhart-Rogoff (de facto regime, supplementary; data ends 2019); Dincer-Eichengreen CB Transparency (deprioritized); Heritage Monetary Freedom / Fraser Sound Money (monetary only); EIU Country Risk macro (optional paid) |
| | Regulatory quality* | *(see State capacity row above — multi-placed)* | |
| | Financial sector regulatory and supervisory quality | FSAP/BCP/IOSCO/IAIS assessments (where available); FATF compliance ratings; Basel AML Index | Barth-Caprio-Levine bank regulation survey (2019); IMF FSI outcomes (low weight, low S/N) |
| | State-owned enterprise governance | *DEFERRED to v2 — see future enhancements list* | |
| | Trade governance | WB Logistics Performance Index; OECD Trade Facilitation Indicators; WTO TFA implementation; KOF Globalisation Index Trade subindex; WB WITS tariff data; Heritage Trade Freedom; UNCTAD NTM database | WTO Trade Policy Reviews (Tier 3); WTO RTA database |
| | Environmental and climate governance | Yale EPI policy/institutional sub-components; LSE Grantham Climate Laws Database; ND-GAIN governance and readiness; IRENA Renewables Capacity Statistics; WB Carbon Pricing Dashboard | IEA energy data and Policies Database (free portions); BNEF Climatescope; WEF Energy Transition Index. *(IRENA Renewable Energy Policies Database deprioritized — see changelog)* |

\* *Concept appears in more than one category. Inventory: 26 unique concepts, 30 instances. WGI Voice and Accountability serves as Accountability category roll-up cross-check; WGI Rule of Law as Rule of Law category cross-check.*

---

## Framework architecture and principles

### Architecture

The framework operates at two structured levels. **Categories** (5 thematic groupings) provide the top-level reporting and communication structure. **Concepts** (26 unique, 30 instances) sit within categories and represent the substantive dimensions of governance that are scored. Within Accountability, concepts are further organised into horizontal accountability (government checks on government) and vertical accountability (government accountability to non-state actors).

Below the concept level, **sources** (datasets and measurement projects) are selected for each concept based on coverage, precision, signal quality, and accessibility. **Metrics** (specific indicators within sources) are selected at the metric-level pass that follows source-level decisions.

### Guiding design principles

- **Substantive categorisation.** Concepts are grouped by what they are about rather than by where they sit in a causal chain or what governance is functionally for. This prioritises navigability and matches how governance is taught and discussed.
- **Multi-placement where genuinely warranted.** A concept is placed in more than one category when it substantively serves more than one categorical function — not merely when it relates to other categories. The operational test: direct dual-function rather than indirect downstream effect. Four concepts qualify.
- **Economic relevance as cross-cutting lens.** Each concept carries an annotation of the strength of evidence linking it to economic and development outcomes. This informs eventual weighting decisions but is not used to exclude concepts at the structural stage.

### Working principles for source and metric selection

The following principles guide source-level and (eventually) metric-level decisions. They were established iteratively through the source-level pass and apply across all concepts.

1. **Country coverage threshold.** Sources should cover the large majority of the framework's country sample (~150–160 countries with population >2M, excluding effectively closed regimes). Sources with systematic regional or income-group exclusions are dropped even when methodologically strong. Borderline-coverage sources (~135–145) are kept on the table at source level with final inclusion decided at metric-level pass against the specific sample.
2. **Precision-of-fit.** Prefer sources that conceptually target the specific concept. Broader aggregate sources can be considered but are excluded where precise concept-specific sources exist. Where broad aggregates duplicate content captured directly by underlying sources we use, the aggregates serve as category-level cross-checks rather than concept primaries.
3. **Signal-to-noise consideration.** Prefer metrics where cross-country and over-time variation is driven primarily by the governance concept rather than by exogenous, cyclical, or confounding factors. Lower-S/N metrics can be supplementary but shouldn't drive scoring. Particularly relevant for outcome metrics (e.g., fiscal outcomes have low S/N for PFM because they're heavily driven by commodity cycles and external conditions).
4. **Outcome metrics OK if signal-rich.** Don't categorically exclude outcome measures. Evaluate by S/N for the specific concept. UNODC homicide is a good outcome measure for personal security (high S/N). Tax-to-GDP is a poor outcome measure for extractive capacity (low S/N due to economic structure confound).
5. **Indicator-level repetition tracked, not prohibited.** Where the same indicator legitimately measures content for multiple concepts, it can appear in both. The discipline is awareness and documentation, not exclusion. Several indicators appear in multiple concepts (e.g., PTS in Personal Security and Civil Liberties).
6. **Conceptual chain awareness within categories.** Concepts within a category often sit on a causal chain (e.g., State capacity → Government effectiveness and administrative quality → Service delivery). The same indicators should not measure structural ability, current use, and realised outputs simultaneously. Disciplined assignment of indicators to specific points on the chain.
7. **Tiering reflects both directness and centrality.** Source tier-1 vs tier-2 placement reflects (a) quality and directness of measurement for the dimension covered, and (b) centrality of that dimension to the concept's role within its category. A direct measure of a peripheral sub-dimension is tier 2 even if methodologically strong.
8. **WGI components as category-level cross-checks.** Where the framework uses WGI components' underlying sources directly (V-Dem, WJP, FH, etc.), the WGI aggregate is treated as a category-level cross-check at roll-up rather than as a concept primary. Avoids double-counting through aggregation.
9. **Ideologically-loaded sources used selectively.** Heritage and Fraser indices have ideological framings of varying intensity across components. Components with low loading and broad expert consensus alignment (e.g., Heritage Trade Freedom for openness; Heritage Property Rights; Heritage Monetary Freedom) are usable. Components with high loading (Heritage Fiscal Freedom, Government Size; Fraser Government Size) are excluded as they conflate policy stance with governance quality.
10. **Subscription sources require cumulative case.** Tier 4 paid sources (EIU at ~$2k/year, ICRG at ~$7k/year, Gallup, MSCI, IISS) are kept off the primary list unless the cumulative case across multiple concepts justifies the cost. To date, neither EIU nor ICRG has earned primary placement across concepts on precision grounds; the cumulative case for paying is weak.

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
- **Weighting scheme using economic relevance annotations.** Per-concept economic relevance annotations (Very strong / Strong / Moderate / Thin) exist for concepts 1–9 and need completion for Trade governance and Environmental and climate governance. Weighting at category and framework levels uses these annotations.
- **Concept 25 (Government transparency and openness) reconsideration.** Significant indicator overlap with other concepts (only the IDEA Political Finance Database and Global Data Barometer are unique to it). **Decision (revisited 2026-06-18): KEEP as own concept.** "Government transparency and openness" is a coherent, investor-legible dimension; overlap tracked under the repetition rule. The Global Data Barometer is deprioritized as its open-data source (thin, edition-unstable, duplicates ODIN). Still flagged to revisit with the full framework view before finalising. See changelog and `framework_decisions.md`.

### Future enhancements (post-v1)

Items identified as v1 measurement gaps or quality limitations, to be addressed in subsequent framework iterations. Many depend on external data sources expanding coverage or methodology over time.

- SOE governance measurement — OECD SOE Guidelines reviews, iSOEF expansion, OECD Corporate Governance Factbook (currently fail coverage); IMF Article IV systematic extraction.
- SOE sector size / state economic control — no good universal-coverage source currently. Concept itself deferred to v2.
- Political settlement direct measurement — possible commissioned country-expert survey along ESID lines for the specific sample.
- PFM coverage expansion — depends on PEFA assessment frequency increasing; IMF FTE coverage expansion if it occurs.
- Statistical infrastructure data integrity / manipulation measurement — currently a documented gap with no standardised cross-country source.
- B-READY rollout tracking — currently ~50 countries, targeting 180. When expanded, strengthens measurement for procedural regulatory quality, trade governance, property rights operational efficiency.
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
| DPI (Database of Political Institutions) | Primary tier 2 | Party fragmentation and government composition as proxies for horizontal elite organisation. ~180 countries. |
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
| IMF Data Standards subscriptions (SDDS / SDDS Plus / eGDDS) | Primary tier 2 | De jure standards compliance signal. Universal but tiered (SDDS Plus for advanced, SDDS for middle, eGDDS for lower-income). |
| V-Dem media corruption / transparent laws indicators | Dropped — precision | Variables initially considered (v2mecorrpt, v2cltrnslw) don't directly measure statistical infrastructure. Stretches that wouldn't pass precision-of-fit. Dropped. |
| PARIS21 reports and assessments | Dropped — currency/structure | Qualitative country reports; not standardised cross-country dataset. Useful for deep dives only. |
| WGI Government Effectiveness | Dropped — precision | Too broad. Aggregates content captured elsewhere. |
| Academic data manipulation work (Martinez, Wallace, others) | Dropped — currency/structure | Specific country cases rather than standardised cross-country index. Real gap; added to future enhancements. |

**State of measurement:** good for production and accessibility (SPI, ODIN, SDDS). Data integrity / manipulation resistance is a documented measurement gap with no honest universal-coverage solution. Best practice: score the concept on production and accessibility, note integrity dimension as a known limitation rather than force a loose proxy.

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
| UNESCO Institute for Statistics (UIS) | Primary tier 1 | Education-specific direct outputs: enrolment, completion, expenditure, teacher-pupil ratios. Universal coverage. |
| UNDP HDI sub-indicators (life expectancy, schooling years — not composite) | Primary tier 1 | Direct outcome indicators. Use sub-indicators, not composite HDI. |
| World Bank Human Capital Index | Primary tier 2 | Synthetic measure: survival, schooling, learning, adult survival. ~170 countries. Useful as composite cross-check. |
| FSI Public Services (P2) | Primary tier 2 | Direct composite of basic service provision. 179 countries. |
| WGI Government Effectiveness | Dropped — precision | Too broad — measures overall governance not service outputs specifically. Primary in GE+AQ concept; using here too broad. |
| Worldwide Bureaucracy Indicators | Dropped — precision | Measures public sector employment/wages, not service outputs. |
| Sustainable Development Report (Sachs et al.) | Dropped — precision | Composite SDG implementation score; far broader than service delivery (climate, gender, partnerships). |
| PISA, PIRLS, TIMSS | Dropped — coverage | Quality measurement but mostly OECD + self-selecting participants. Real gap on education quality dimension. |
| Mo Ibrahim IIAG Human Development | Dropped — coverage | 54 African countries only. |

**State of measurement:** strong on coverage of services delivered. Weaker on quality dimensions (especially education learning quality where universal-coverage assessment fails). Triangulation across WHO, UNESCO, WDI, and FSI provides robust signal.

---

### Concept 6: Regulatory quality

**Category:** Economic and fiscal governance AND State capacity — multi-placed
**Scope:** quality of regulation governing private economic activity — well-designed, predictable, proportionate, consistently enforced. Multi-placed because it reflects both state capability to design and implement regulation (State capacity) and the regulatory environment for economic activity (Economic and fiscal governance).
**Measurement challenge:** Doing Business discontinuation (2021) removed a major data source; B-READY is replacement but coverage currently inadequate. Procedural quality (RIA, consultation, transparency in rulemaking) has weak universal-coverage measurement.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| WGI Regulatory Quality | Primary tier 1 | Direct concept match. Universal coverage (~215). The aggregate is literally about regulatory quality. |
| WJP Rule of Law Index — Regulatory Enforcement (Factor 6) | Primary tier 1 | Direct fit for procedural and enforcement quality. 142 countries (borderline). |
| Heritage Business Freedom | Primary tier 2 | Direct fit for regulatory environment as experienced by firms. Ideological framing acknowledged but moderate for this dimension. |
| Fraser Regulation area | Primary tier 2 | Similar to Heritage Business Freedom. Same framing caveats. |
| World Bank B-READY | Track for future | Direct fit but ~50 countries currently. Targeting 180. Future enhancement item. |
| OECD iREG (Indicators of Regulatory Policy and Governance) | Dropped — coverage | ~40 OECD + partners. Strong for procedural quality but fails threshold. |
| PRS ICRG / EIU Operational Risk | Dropped — precision | Bundled risk products; regulatory content embedded in broader risk frame. |

**State of measurement:** headline regulatory quality is well-measured; procedural quality dimension is weakly measured universally (OECD iREG fails coverage). B-READY rollout will eventually help.

---

### Concept 7: Public financial management (PFM)

**Category:** Economic and fiscal governance
**Scope:** end-to-end architecture for managing public finances — budget formulation and credibility, policy-based budgeting, predictability of execution, procurement systems, public investment management, accounting and reporting, external audit and legislative scrutiny.
**Measurement challenge:** one of the thinnest concepts for cross-country governance-precise measurement. Best dedicated source (PEFA) has irregular timing per country; OBS has borderline coverage. Countries without recent PEFA or OBS coverage have real measurement gaps.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| PEFA (Public Expenditure and Financial Accountability) | Primary tier 1 | Gold standard PFM assessment across 31 indicators (~150 countries with at least one assessment all-time). **BUILT** (`33_pefa_pipeline`) from PEFA's structured **"Scores Downloads" CSV — not PDF.** Core scope = 2016 framework, national, latest assessment per country: **85 countries, assessment years 2017–2026** (median 2022). 2011-framework backfill deferred (stale — see changelog). |
| Open Budget Survey (IBP) | Primary tier 1 | Direct fit for budget transparency and participation. 120 countries (2023 ed.). Biennial. Strong methodology. |
| IMF Fiscal Transparency Evaluations | Keep for metric pass — coverage verify | Excellent quality. ~50-60 historically; may have expanded. Confirm current count at metric pass. |
| IMF WEO fiscal outcomes | Supplementary, low weight | Universal coverage. Low S/N for PFM specifically (cyclical, exogenous). Cross-check only at low weight. |
| WGI Government Effectiveness | Dropped — precision | Too broad. PFM is one of many things GE captures. Already used in GE+AQ. |
| TADAT, MAPS, DeMPA | Dropped — coverage | Specific assessment tools; each fails coverage individually. Content embedded in PEFA where present. |
| CPIA Public Sector Management | Dropped — coverage | IDA-only. |

**State of measurement:** measurement is genuinely thin and heterogeneous across the sample. Countries with recent PEFA assessments will be well-measured; countries with only OBS will be measured on transparency only; countries with neither have real gaps. Documented limitation in framework reporting recommended.

---

### Concept 8: Macroeconomic policy framework quality

**Category:** Economic and fiscal governance
**Scope:** institutional architecture governing macroeconomic policymaking — fiscal rules and fiscal council design, monetary policy framework, central bank independence and credibility, macroprudential institutional setup, exchange rate regime governance. Distinct from macroeconomic outcomes.
**Measurement challenge:** strong temptation to use macro outcomes (inflation, fiscal balance) as proxies; these have low S/N for framework quality given exogenous drivers. Direct institutional measures (CBI indices, fiscal rules databases) are higher S/N and should drive scoring.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| Romelli (2022) Central Bank Independence Index | Primary tier 1 | Current state-of-the-art for CBI. Updates and broadens Cukierman. ~155 countries. Direct fit, high S/N. |
| IMF Fiscal Rules Database (with compliance tracking) | Primary tier 1 | Existence, design, and compliance of fiscal rules. Direct governance measure (not just outcomes). |
| IMF AREAER — FARI (Financial Account Restrictiveness Index) | Primary tier 1 | Capital-account restrictiveness, de jure. IMF-native authoritative source. 194 countries, 1999–2024. **Manual** (portal WAF-blocked); FARI aggregate + FDI sub-index. See changelog. |
| Chinn-Ito KAOPEN | Primary tier 1 (derivative) | Most-cited academic capital-account-openness index, derived from AREAER. Automated, 182 countries 1970–2023. Broad time-series complement / cross-check to FARI; not more authoritative than AREAER. |
| IMF iMaPP (Integrated Macroprudential Policy Database) | Primary tier 1 | Macroprudential measure adoption. ~130 countries. |
| IMF AREAER — de facto exchange-rate classification | Primary tier 1 (deferred) | The exchange-rate-regime dimension. IMF-native de facto classification (current to April 2025, ~195 jurisdictions); supersedes Reinhart-Rogoff as the current-state primary. **Manual PDF + matrix extraction; deferred to the Category-1 PDF batch** — published as a borderless 2-D matrix (IMF Annual Report Appendix II.9); see changelog. |
| Reinhart-Rogoff exchange rate classifications | Supplementary (demoted) | De facto regime, methodologically independent (parallel-market-aware) cross-check + deep history (1946–). Demoted from primary: data ends ~2019 (≈7-yr stale, worst in stressed EMs); superseded as current-state primary by AREAER's own de facto classification. |
| Dincer-Eichengreen Central Bank Transparency Index | Deprioritized | Complementary CB transparency dimension (~120 countries) but stale; Romelli CBI covers the concept more currently. |
| Heritage Monetary Freedom / Fraser Sound Money | Supplementary | Monetary stability outcomes — lower ideological loading than other Heritage/Fraser components. Use monetary components only. |
| EIU Country Risk Service (macroeconomic component) | Optional paid | $2k/year. Forward-looking expert assessment. Worth considering if cumulative case across concepts justifies. |
| Cukierman / GMT central bank independence | Dropped — currency/supersession | Superseded by Romelli for current data. |
| EPU index (Baker-Bloom-Davis) | Dropped — coverage | ~30 countries (mostly developed). |
| World Uncertainty Index (Ahir-Bloom-Furceri) | Moved to cross-cutting | Better as cross-cutting predictability composite than primary for this concept. |
| Heritage Fiscal Freedom and Government Size / Fraser Government Size | Dropped — ideological loading | Higher loading than other Heritage/Fraser components. Conflate policy stance (size of state) with governance quality. |
| IMF WEO macro outcomes (inflation, fiscal balance, debt) | Supplementary, low weight if used | Low S/N for framework quality. Cross-check at low weight only. |

**State of measurement:** strong. Multiple direct institutional measures across all sub-dimensions (central bank, fiscal framework, exchange regime, macroprudential). Capital-account governance is triangulated across IMF-native (AREAER FARI) and academic derivative (Chinn-Ito). Exchange-rate-regime governance: current-state primary is the IMF AREAER de facto classification (deferred to the Category-1 PDF-extraction batch — documented short-term gap); Reinhart-Rogoff retained as a supplementary independent cross-check (data ends ~2019).

---

### Concept 9: Financial sector regulatory and supervisory quality

**Category:** Economic and fiscal governance
**Scope:** quality of regulation and supervision of banks, securities markets, insurance, plus the AML/CFT framework. Includes legal/regulatory framework (what rules exist) and supervisory effectiveness (whether supervisors have powers, resources, independence, and actually use them).
**Measurement challenge:** FSAP (gold standard) happens every 5-10 years per country, voluntary for non-systemically-important. FATF has better timing but is AML/CFT-specific. Financial outcomes (NPL, capital adequacy) have low S/N for supervisory quality (cyclically driven).

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| IMF/WB FSAP — comprehensive financial sector assessment | Primary tier 1 | Gold standard. Mandatory every 5 years for ~30 systemically important; voluntary for others. ~190 countries with at least one assessment but timing varies. Tier 3 access. |
| FATF Mutual Evaluations and compliance ratings | Primary tier 1 | Direct fit for AML/CFT. ~200 jurisdictions. ~10-year cycle with intermediate follow-ups. Structured ratings via fatf-gafi.org (Tier 2 access for ratings, Tier 3 for full reports). |
| Basel AML Index (Basel Institute on Governance) | Primary tier 1 | AML/CFT risk composite. ~205 countries, annual, free. Synthesises FATF and other sources — saves extraction labor. *(Access note: Expert Edition requires institutional affiliation; see status table.)* |
| Basel Core Principles (BCP) assessments | Primary tier 1 | Banking supervision specifically. Embedded within FSAP. |
| IOSCO Principles assessments | Primary tier 1 | Securities regulation specifically. Embedded within FSAP. |
| IAIS Insurance Core Principles assessments | Primary tier 1 | Insurance regulation specifically. Embedded within FSAP. |
| Barth-Caprio-Levine Bank Regulation and Supervision Survey | Supplementary | Direct fit for banking regulation. Most recent comprehensive wave 2019. Currency cap is real. |
| IMF Financial Soundness Indicators (FSI) | Supplementary, low weight | Outcome data (NPL, capital adequacy). Low S/N for supervisory quality specifically. Cyclical. |
| FSB jurisdictional implementation monitoring | Dropped — coverage | ~24 FSB jurisdictions only. |
| IMF Financial Development Index, WB GFDD | Dropped — precision | Measure financial development, not regulation/supervision. |
| WGI Regulatory Quality | Dropped — precision | Too broad. Primary in Regulatory quality concept. |
| Heritage Financial Freedom | Dropped — ideological loading | Equates lower regulation with more freedom — loaded framing for financial regulation specifically. |
| PRS ICRG Financial Risk | Dropped — precision | Bundled with macroeconomic risk; not financial-supervision-specific. |

**State of measurement:** strong direct measurement (FSAP, FATF, BCP/IOSCO/IAIS) but Tier 3 access cost is real and coverage timing varies. Practical workhorse for AML/CFT is FATF compliance ratings (structured Tier 2). Broader supervisory quality requires FSAP extraction work.

---

### Concept 10: State-owned enterprise governance — DEFERRED TO V2

**Category:** Economic and fiscal governance
**Status:** deferred to v2 framework. The thinnest concept for cross-country governance-precise measurement in the inventory. The best-fit sources fail coverage threshold; broad-coverage alternatives fail precision.
**Decision rationale:** best dedicated measurement (OECD SOE Guidelines reviews, OECD Corporate Governance Factbook, iSOEF) covers ~50 countries — fails the coverage threshold. PEFA Pillar 3 captures fiscal-risk-from-SOE content where assessments exist (~150 countries, timing variable). IMF Article IV staff reports have rich SOE content annually but require Tier 3 extraction. Cross-country SOE sector size measurement is also weakly developed (IMF GFS Public Corporations data has definitional inconsistencies and coverage gaps; OECD PMR State Control fails coverage).
**Future enhancement path:** (1) OECD assessment coverage expansion if it occurs; (2) iSOEF expansion; (3) IMF Article IV systematic extraction (also benefits Macro framework, PFM); (4) custom country-by-country research for major SOE economies (China, Russia, Gulf, Vietnam, etc.).

---

### Concept 11: Trade governance

**Category:** Economic and fiscal governance
**Scope:** combined trade administration (customs efficiency, trade procedure predictability, transparency of trade rules, anti-dumping process integrity) and trade openness (tariff levels, non-tariff barriers, FTA participation, trade defense). Weighted toward administration over openness per framework design decision.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| World Bank Logistics Performance Index (LPI) | Primary tier 1 | Direct measure of trade administration quality. 139 countries (2023 ed.). 5-year update gap historically; current cadence uncertain. |
| OECD Trade Facilitation Indicators (TFI) | Primary tier 1 | 11 indicators covering administration. 163 countries. Updated every 2-3 years. *(Access: JS simulator, no API; manual route prepared — see status table.)* |
| WTO Trade Facilitation Agreement (TFA) implementation tracking | Primary tier 1 | Country commitments and implementation status. All WTO members. Continuously updated. |
| KOF Globalisation Index — Trade Globalization subindex | Primary tier 1 | De jure and de facto openness measures. ~200 countries. Lower ideological framing than Heritage/Fraser. Annual. |
| World Bank tariff data (WITS / WDI) | Primary tier 1 | Simple and trade-weighted average tariffs. Universal coverage, annual. |
| Heritage Trade Freedom | Primary tier 1 | Direct fit for openness. ~180 countries, annual. Lower ideological loading than other Heritage components for openness measurement specifically. |
| UNCTAD Non-Tariff Measures (NTM) database | Primary tier 1 | Comprehensive NTM coverage. ~110 countries. Borderline coverage but only good source on NTMs. *(Access: bulk API 403, TRAINS JS-gated — see status table.)* |
| WTO Trade Policy Reviews (TPRs) | Supplementary | Rich country-specific content. Tier 3 PDFs. Cycle 2-7 years. |
| WTO RTA Database | Supplementary | FTA participation tracking. All WTO members. |
| World Customs Organization (WCO) data | Supplementary | Customs administration practices. Coverage and accessibility vary. |
| Fraser Freedom to Trade Internationally | Dropped — overlap | Overlaps Heritage Trade Freedom too closely. |
| Doing Business Trading Across Borders | Dropped — currency | Discontinued 2021. |
| B-READY trade content | Track for future | Coverage currently ~50 countries; track as expands. |
| Trade Restrictiveness Index (Kee-Nicita-Olarreaga) | Dropped — currency | Updates irregular. |
| WGI Regulatory Quality | Dropped — precision | Too broad for trade specifically; in Regulatory Quality concept. |
| PRS ICRG / EIU Country Risk | Dropped — precision/cost | Bundled in broader risk products. |

**State of measurement:** strong measurement on both administration and openness dimensions. The weighting toward administration is operationalised through metric selection (LPI/TFI heavier than tariff data and openness indices).

---

### Concept 12: Environmental and climate governance

**Category:** Economic and fiscal governance
**Scope:** combined environmental governance (institutional capacity to regulate: ministry capacity, enforcement of environmental regulation, EIA processes, environmental data transparency, regulatory capture by polluting industries) and climate/renewables policy stance (with renewables policy as dominant policy-stance content). Weighted toward governance over policy stance per framework design decision.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| Yale Environmental Performance Index (EPI) — policy and institutional sub-components | Primary tier 1 | Workhorse for environmental governance content. 180 countries, biennial. Use sub-components selectively, not headline composite. |
| LSE Grantham Climate Laws Database | Primary tier 1 | De jure environmental and climate framework. Universal coverage. Continuously updated. *(Built national-only cumulative stock + flow.)* |
| ND-GAIN governance and readiness sub-scores | Primary tier 1 | Governance and readiness dimensions; 192 countries; annual. Broader governance content with environmental framing. |
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
| World Bank Informal Economy Database | Primary tier 2 | Informality as proxy for state reach into formal economy. ~160 countries. Direct conceptual link via administrative reach. |
| ILO social security coverage | Primary tier 2 | Formality via state administrative systems. ~150 countries. Direct measure of state reach. |
| Hanson-Sigman state capacity index | Supplementary | Multi-dimensional latent variable measure. ~169 countries. Last comprehensive update 2021. Use as cross-check with double-counting caveat (incorporates V-Dem and other sources we use). |
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
| V-Dem v2clacjstm and v2clacjstw (Access to justice) | Primary tier 1 | Direct fit for equal-treatment dimension. ~180 countries. |
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
| V-Dem property rights indicators (v2clprptym, v2clprptyw, v2xcl_prpty) | Primary tier 1 | Direct fit, multiple direct measures of both de jure and de facto property protection. Strong workhorse. |
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
| V-Dem corruption indicators (v2x_corr, v2excrptps, v2exembez, v2lgcrrpt, v2jucorrdc) | Primary tier 1 | Multiple direct precise measures across branches of government. ~180 countries. Methodologically distinct from CPI/WGI aggregators. |
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
| IPU Parline | Primary tier 1 | Legislative structural features and oversight powers. Universal coverage (~190 parliaments). Authoritative source. Continuously updated. |
| Polity5 Executive Constraints (XCONST) | Primary tier 2 | Classic executive constraints measure. Long time series. Update reliability concern; V-Dem supersession ongoing. |
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
| IDEA EMB Database | Primary tier 1 | EMB design and independence dimension. ~220 jurisdictions. Moved here per vertical accountability fit. |
| NELDA (National Elections Across Democracy and Autocracy) | Primary tier 2 | Event-level data: opposition allowed, harassment, fraud, post-election violence. Universal where elections occur. |
| IDEA Voter Turnout Database | Keep for metric pass | Compulsion adjustment not made by IDEA. Metric-level decision: either adjust manually or accept noise. Kept on table. |
| Polity5 electoral indicators | Supplementary | Largely superseded by V-Dem for current measurement. |
| Comparative Constitutions Project — electoral provisions | Supplementary | De jure framework reference. |
| Database of Political Institutions (DPI) | Supplementary | Institutional context. |
| WGI Voice and Accountability | Category-level cross-check | Used at Accountability category roll-up. |
| OSCE/ODIHR election observation | Dropped — coverage | OSCE region only (~57 countries). |
| EU EOMs, OAS, Carter Center, NDI, IRI observation | Dropped — coverage | Selective per-election; not standardised cross-country dataset. |
| BTI Stateness / Political Participation | Dropped — coverage | Transformation countries. |
| EIU Democracy Index — Electoral Process component | Dropped — cost/borderline | Borderline coverage plus paid. |

**State of measurement:** very strong. Among the best-measured concepts. Triangulation across V-Dem, PEI, FH, and IDEA provides methodologically diverse measurement with broad coverage.

---

### Concept 21: Political participation beyond voting

**Category:** Accountability (vertical)
**Scope:** forms of political engagement beyond electoral voting — protest participation, civic engagement, deliberative participation, party and association membership, contacting officials, signing petitions, online political activity. Earlier flagged as having thin economic relevance among the concepts.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| V-Dem participation indicators (v2x_partip, v2psprlnks, v2pscohesv, v2cseeorgs, v2dlconslt, v2csreprss) | Primary tier 1 | Multiple direct precise measures, broad coverage (~180 countries), annual. Workhorse. |
| CIVICUS Monitor | Primary tier 1 | Civic space conditions (whether participation is possible). 197 countries/territories. Annual. Categorical scoring. |
| IDEA Global State of Democracy — Participatory Engagement subindex | Primary tier 2 | Composite with broad coverage (~173 countries). Some V-Dem double-counting given underlying sources. |
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
| V-Dem civil liberties indicators (v2x_civlib, v2x_clpriv, v2clrelig, v2clpriv, v2cldmovem/w, v2clsocgrp, v2clslavef) | Primary tier 1 | Multiple direct precise measures across civil liberties sub-dimensions. Workhorse. |
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

**State of measurement:** strong. Multiple methodologically distinct sources with broad coverage. Disciplined sub-component extraction from FH addresses the bundling issue cleanly. Internet/digital freedom dimension is under-measured cross-country (Freedom on the Net fails coverage); future enhancement.

---

### Concept 23: Media freedom and pluralism

**Category:** Accountability (vertical)
**Scope:** freedom of media to operate without state interference; journalist safety; independence of broadcast and print media from political and economic capture; pluralism of media voices; freedom of internet/digital media; access to information.

| Source | Decision | Rationale / notes |
|--------|----------|-------------------|
| Reporters Without Borders (RSF) — World Press Freedom Index | Primary tier 1 | Standard cross-country press freedom measure. 180 countries, annual. Pluralism, independence, environment/self-censorship, legislative framework, transparency, safety, plus quantitative abuses indicator. |
| V-Dem media indicators (v2x_freexp_altinf, v2mecenefm, v2meharjrn, v2mecorrpt, v2meslfcen, v2merange, v2mebias, v2mecrit) | Primary tier 1 | Multiple direct precise measures. ~180 countries, annual. |
| Committee to Protect Journalists (CPJ) — journalist safety data | Primary tier 1 | Direct outcome measure for journalist safety dimension. Universal (CPJ tracks all reported cases). Continuous. |
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

**State of measurement:** strong. Multiple methodologically distinct primary sources (RSF expert+quantitative, V-Dem expert coding, CPJ outcome data) provide robust triangulation. Main gap: internet/digital media freedom universal-coverage measurement and media ownership concentration cross-country measurement. Future enhancements.

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

This section records substantive design-level decisions made after the May 2026 PDF version. Build mechanics (notebooks, file paths, access methods, data currency) live in `docs/framework_decisions.md`, `data/processed/source_registry.csv`, and the download log; only decisions that affect the framework's *design* (concepts, source roles, source dispositions) are recorded here.

**2026-06-18**

- **Concept 25 (Government transparency and openness) — KEEP.** The May version flagged this concept for reconsideration due to heavy overlap. Decision: keep as a standalone concept (coherent, investor-legible; overlap tracked under the repetition rule). The architectural argument for absorption (it is thematically rather than functionally defined) was considered and not adopted; still flagged to revisit before finalising.
- **Global Data Barometer — DEPRIORITIZED.** Previously the designated open-data supplementary for Concept 25. On review: thin (~43–109 countries, edition-unstable, not a panel), duplicates ODIN's coverage, and does not fill the concept's real gaps (procurement, lobbying, de facto practice). Open-data leg now served by ODIN. Deliberate departure from the May spec.
- **AREAER capital-account dimension — RESOLVED with three complementary sources.** The IMF AREAER portal was confirmed WAF-blocked and JS-gated (not automatable). Resolution: (1) **IMF AREAER FARI** — capital-account restrictiveness, de jure, IMF-native, obtained by manual export (194 countries, 1999–2024; FARI aggregate + FDI sub-index); (2) **Chinn-Ito KAOPEN** — the most-cited academic derivative of AREAER, automated, broad time series (cross-check, not more authoritative than AREAER); (3) **exchange-rate regime** — sourced from the IMF AREAER *de facto* classification (IMF-native, current to April 2025, ~195 jurisdictions), which supersedes Reinhart-Rogoff as the current-state primary; **Reinhart-Rogoff demoted to supplementary** (independent parallel-market-aware cross-check, data ends ~2019). The AREAER de-facto table is a borderless PDF matrix (IMF Annual Report Appendix II.9 p20; programmatic fetch WAF-blocked, `extract_tables` finds no grid) → **deferred to the Category-1 PDF-extraction batch**; ER-regime is a documented short-term gap until then. The AREAER Change Index (ACI) was obtained but not built (measures policy change, not level; deferred supplementary).
- **IRENA Renewable Energy Policies Database — DEPRIORITIZED.** No clean downloadable renewable-policy dataset exists; IRENA's policy work is report-based, and the joint IEA/IRENA Policies DB has no clean renewable filter and would duplicate Climate Laws. Renewable deployment covered by IRENA capacity statistics; energy/climate policy by Climate Laws; carbon pricing by WB Carbon.
- **rti-evaluation.org (de facto RTI implementation) — DEPRIORITIZED.** Bespoke per-country reports, handful of countries, heterogeneous — not a comparable cross-country panel. De facto RTI implementation remains a known v1 gap, partially covered by V-Dem transparency/disclosure practice measures. Flagged as a watch item.
- **Concept count.** Working inventory updated from 25 to 26 unique concepts (Concept 11 trade/state-control refinement); SOE governance remains deferred to v2.
- **Sources confirmed stale/superseded:** Dincer-Eichengreen CB Transparency (Romelli CBI supersedes), Linzer-Staton (V-Dem judicial indicators supersede).
- **PEFA — BUILT as a structured pipeline (not PDF); scope locked to 2016/national.** PEFA was slated for the Category-1 PDF-extraction batch, but its "Scores Downloads" facility exports A–D indicator/dimension scores as a CSV — so it is a structured manual-download pipeline (`33_pefa_pipeline`), not PDF parsing. Scope decided on evidence: **core = 2016 framework, national, latest assessment per country (85 countries, median assessment year 2022, all ≤9 yrs old)**. The 2011-framework backfill (35 additional national countries) was **deferred** because its investment-relevant names (Brazil 2009, India 2010, Norway 2008) are 16–18 years stale — current 55% coverage judged better than stale 77%. `assessment_year` is carried as a recency flag; the framework version is a single documented knob (`PEFA_FRAMEWORK`). The 2011 backfill is revisitable — narrowly and flagged — at PFM-concept assembly.
- **ICNL — dropped from the PDF batch, retained as supplementary.** The Civic Freedom Monitor is HTML qualitative country notes (de jure CSO law, ~50 countries), not PDF and not a scored dataset; redundant-for-scoring with the automated CIVICUS Monitor (de facto, ~197 countries) plus V-Dem civil-society indices. Stays registered as `tier3_web`, supplementary; no pipeline built.

> **Note on numbering.** Several concept numbers in this document differ from the May version because the working inventory expanded to 26 and some concepts were reordered. The category assignments and source decisions are the authoritative content; numbering is a navigational convenience.

