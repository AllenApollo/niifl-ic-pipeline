"""
STEP 1 — Build NIIFL Custom Skills
===================================
Skills are domain knowledge packs loaded into agent context.
Each skill is a plain-text prompt block stored as a .txt file.
Run this script first — agents load skills at startup.

Usage:
    python3 step1_build_skills.py
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "config"))
from config import FUNDS, ESG_PILLARS, POLICY_FRAMEWORKS, SKILLS_DIR

os.makedirs(SKILLS_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# SKILL 1 — Fund Mandate Skill
# ─────────────────────────────────────────────────────────────────────────────
fund_mandate_skill = """
# NIIFL Fund Mandate Skill
# Loaded by: Orchestrator, Deal Sourcing Agent, IC Memo Agent

## NIIFL Overview
National Investment and Infrastructure Fund Limited (NIIFL) is India's sovereign-anchored
alternative asset manager. Government of India holds 49% in each fund. Registered with SEBI
as Category II Alternative Investment Fund. Governing Council chaired by Finance Minister.

## Fund 1 — NIIF Master Fund
- Strategy: Operating assets in core infrastructure
- Sectors: Roads, ports, airports, energy, utilities, urban infrastructure
- Ticket size: INR 500 Cr minimum
- Asset type: Mature operating assets with long track record
- Return hurdle: 12%+ net IRR, 1.8x+ MOIC
- Target: Regulated environments or concession/PPA structures
- Key LPs: ADIA, Temasek, CPP Investments, Ontario Teachers', AustralianSuper, PSP Investments

## Fund 2 — NIIF Strategic Opportunities Fund (SOF)
- Strategy: Growth equity — building domestic champions
- Sectors: Digital infrastructure, manufacturing, financial services, healthcare, housing
- Ticket size: INR 100–500 Cr
- Asset type: Growth equity, minority or majority stakes
- Return hurdle: 18%+ net IRR, 2.5x+ MOIC
- Target: Established Indian businesses with scale potential
- Key LPs: Temasek, Padmanabh Sinha (CIO-Growth Equity)

## Fund 3 — NIIF Private Markets Fund (PMF)
- Strategy: Fund of funds — mid-market Indian fund managers
- Sectors: Climate, healthcare, affordable housing, manufacturing, fintech, agri
- Ticket size: INR 50–200 Cr per fund commitment
- Asset type: Primary fund commitments, selective co-investments
- Return hurdle: 15%+ net IRR, 2.0x+ MOIC
- Target: Best-in-class domestic fund managers, India-focused strategies

## Fund 4 — India-Japan Fund (IJF)
- Strategy: Bilateral infrastructure — Japan nexus required
- Sectors: Clean energy, mobility (EVs, last-mile), logistics, smart cities
- Ticket size: INR 200–1000 Cr
- Asset type: Operating assets and growth equity with Japan partnership
- Return hurdle: 14%+ net IRR, 2.0x+ MOIC
- Bilateral partner: Japan Bank for International Cooperation (JBIC)
- JBIC criteria: Japanese technology, capital, or partnership required
- Fund size: INR 49 billion target; GoI 49%, JBIC 51%

## Mandatory Exclusions (All Funds)
- Weapons, tobacco, gambling, alcohol
- Projects with unresolved land acquisition disputes
- Companies under SEBI/SFIO investigation
- Entities with adverse environmental court orders

## NIIFL Investment Principles
1. Long-term, patient capital — economic cycles perspective
2. Sustainable investing — ESG integrated in every decision
3. Commercial returns — IC decisions made independently of government
4. Portfolio concentration limits — max 25% in any single sector
5. Co-investment encouraged — LP co-invest rights on deals >INR 1000 Cr
"""

# ─────────────────────────────────────────────────────────────────────────────
# SKILL 2 — IC Memo Template Skill
# ─────────────────────────────────────────────────────────────────────────────
ic_memo_template_skill = """
# NIIFL IC Memo Template Skill
# Loaded by: IC Memo Drafting Agent

## IC Memo — Standard Structure (All Funds)
Every IC memo must contain exactly these 8 sections in this order:

### Section 1 — Investment Thesis
- Why this deal: core value proposition in 2–3 sentences
- Why NIIFL: strategic fit with fund mandate, additionality
- Why now: market timing, deal dynamics, competitive tension
- Value creation plan: operational improvements, capacity expansion, re-rating catalysts
- Exit strategy: strategic buyer, IPO, secondary — with timeline and comparable exits

### Section 2 — Market & Competitive Position
- Total Addressable Market (TAM) — size, growth rate, data source
- Regulatory environment: concession terms, tariff regime, regulator track record
- Competitive landscape: market share, barriers to entry, key competitors
- Company positioning: differentiation, moats, customer concentration
- India macro tailwinds: GDP growth, infrastructure spend, policy support

### Section 3 — Financial Returns
- Entry valuation: EV, EV/EBITDA multiple, rationale for multiple
- Base case IRR and MOIC (clearly state vs fund hurdle)
- Bull case and bear case IRR with assumption changes
- Sensitivity table: minimum 2 variables (e.g. traffic/tariff for roads, PLF/tariff for power)
- Historical financial summary: Revenue, EBITDA, PAT — last 3 years
- Projected financials: Revenue, EBITDA, FCF — next 5 years
- Debt structure: leverage ratio, DSCR, covenant headroom

### Section 4 — Key Risks & Mitigants
Format each risk as: [Risk Category] → [Specific Risk] → [Mitigant] → [Residual Risk: High/Med/Low]
Required risk categories:
- Regulatory risk
- Construction / execution risk (if applicable)
- Revenue / demand risk
- Management / key person risk
- Environmental / social risk
- Exit risk

### Section 5 — ESG & Impact Score
NIIFL ESG Framework — score each pillar 1–5:
- Environment: carbon footprint, renewable content, waste management practices
- Ease of Living: jobs created, communities impacted, service accessibility
- Economic Growth: GDP contribution, exports, MSME linkages, tax generation
State alignment with NIIFL's three ESG pillars and UN SDGs.

### Section 6 — Policy Alignment
- NIP (National Infrastructure Pipeline): state whether project is in NIP
- PLI scheme: relevance to applicable PLI sector
- NMP (National Monetisation Pipeline): if asset is NMP candidate
- PM GatiShakti: multimodal logistics integration
- State government support: clearances, incentives, land status

### Section 7 — Deal Structure & Terms
- Proposed equity stake: % ownership, board seats, governance rights
- Entry mechanism: primary / secondary / mix
- Shareholder agreement key terms: tag, drag, ROFR, anti-dilution
- Debt structure: senior, mezzanine, project finance — key covenants
- Escrow / holdback arrangements
- Conditions precedent: regulatory approvals required

### Section 8 — Recommendation
- Proposed action: INVEST / PASS / DEFER
- Proposed ticket size: INR X Cr from [Fund Name]
- IC approval sought: Term sheet authorisation / exclusivity / final investment
- Dissenting views (if any)
- Next steps if approved: milestones and timeline

## Fund-Specific Additions

### Master Fund Memos — Additional Requirements
- Concession agreement summary: tenure, authority, step-in rights, termination triggers
- Traffic/capacity projections: source, methodology, independent traffic study reference
- O&M structure: in-house vs outsourced, key contracts
- Regulatory asset base analysis (for regulated utilities)

### IJF Memos — Additional Requirements
- Japan nexus statement: nature of Japanese involvement (technology/capital/partnership)
- JBIC criteria compliance: checklist confirmation
- Cross-currency analysis: JPY/INR assumptions, hedging strategy
- JBIC environmental and social standards: compliance confirmation
"""

# ─────────────────────────────────────────────────────────────────────────────
# SKILL 3 — India Infrastructure Skill
# ─────────────────────────────────────────────────────────────────────────────
india_infra_skill = """
# India Infrastructure Skill
# Loaded by: Financial Modelling Agent, DD Research Agent

## Financial Modelling Frameworks

### Roads (NHAI Concessions)
- Model type: Concession DCF
- Key revenue driver: PCU traffic × toll rate
- Toll escalation: Typically WPI-linked, annual
- Concession period: 20–30 years from COD
- Key risks: Traffic underperformance (use NHAI traffic studies), toll collection efficiency
- Benchmark EBITDA margin: 85–92% (toll collection is high margin)
- Exit: EV/EBITDA 12–18x for operational highway assets (2024–25 benchmarks)
- Reference: NHAI ATVM data, MoRTH annual report

### Ports (Major Port Trusts / PPP)
- Model type: Concession DCF
- Key revenue driver: Cargo volume (MTPA) × tariff
- Tariff: TAMP-regulated or market-determined (non-major ports)
- Key metrics: Berth occupancy, turnaround time, market share by commodity
- Benchmark EBITDA margin: 55–70%
- Exit: EV/EBITDA 14–20x for operating port assets
- Reference: IPA (Indian Ports Association) statistics, MoPSW data

### Power / Renewable Energy
- Model type: Project finance DCF
- Key revenue driver: Units generated (PLF × capacity) × tariff
- Tariff: PPA-backed (fixed) or merchant (variable)
- PLF benchmarks: Solar 20–26%, Wind 28–35%, Hydro site-specific
- Key risks: Grid curtailment, PPA counterparty (DISCOM) credit quality
- Benchmark EBITDA margin: 88–94% for renewable assets
- Exit: EV/MW 4–7 Cr for solar; EV/MW 5–9 Cr for wind (2024–25)
- Reference: CEA monthly generation reports, MNRE data

### Airports
- Model type: Concession DCF with aeronautical + non-aeronautical split
- Aeronautical: AERA-regulated UDF, landing charges
- Non-aeronautical: Retail, cargo, real estate — typically 30–40% of revenue
- Key driver: Passenger throughput (domestic + international)
- Reference: AAI traffic statistics, DGCA monthly data

## Key India Macro Assumptions (Update Annually)
- GDP growth: 6.5–7.5% (FY26 IMF/RBI estimates)
- CPI inflation: 4.5–5.5%
- WPI inflation: 3.5–4.5% (used for toll escalation)
- 10-year G-sec yield: 6.5–7.2% (use as risk-free rate)
- India equity risk premium: 6–8%
- INR/USD long-term: 85–90 (use for cross-currency deals)

## Regulatory Bodies Quick Reference
| Sector | Regulator | Key Portal |
|--------|-----------|------------|
| Roads | NHAI / MoRTH | nhai.gov.in |
| Ports | MoPSW / TAMP | shipping.gov.in |
| Power | CERC / SERC | cercind.gov.in |
| Airports | AERA / DGCA | aera.gov.in |
| Telecom | TRAI | trai.gov.in |
| Water | No central regulator | State govts |

## National Infrastructure Pipeline (NIP) — Key Stats
- Total NIP outlay: INR 111 lakh crore (2019–2025)
- Top sectors: Energy (24%), Roads (19%), Urban (16%), Railways (13%)
- Implementation gap: ~35–40% underfunded — opportunity for private capital
- Source: NITI Aayog NIP dashboard (niti.gov.in)
"""

# ─────────────────────────────────────────────────────────────────────────────
# SKILL 4 — ESG & Impact Skill
# ─────────────────────────────────────────────────────────────────────────────
esg_skill = """
# NIIFL ESG & Impact Skill
# Loaded by: IC Memo Drafting Agent, Outcomes Grader Agent

## NIIFL ESG Framework — Three Pillars

### Pillar 1 — Environment
Score 1–5 on each sub-dimension:
- Carbon footprint: Net GHG emissions, reduction commitments, offset quality
- Renewable energy content: % of operations powered by renewables
- Water stewardship: Water intensity, recycling, watershed impact
- Biodiversity: Land use, habitat impact, environmental clearance status
- Waste management: Hazardous waste handling, circular economy practices

### Pillar 2 — Ease of Living
Score 1–5 on each sub-dimension:
- Energy access: Rural electrification, energy poverty reduction
- Healthcare: Hospital beds, diagnostic centres, healthcare access created
- Affordable housing: Units created, affordability metrics (EMI/income ratio)
- Digital inclusion: Broadband connectivity, digital literacy programs
- Mobility: Public transport, last-mile connectivity, accessibility

### Pillar 3 — Economic Growth
Score 1–5 on each sub-dimension:
- Job creation: Direct jobs, indirect/induced employment (use multipliers)
- Tax generation: GST, corporate tax, customs — annual contribution
- Export facilitation: Forex earnings, export infrastructure
- MSME linkages: Local supply chain, vendor development programs
- Skill development: Training programs, apprenticeships

## ESG Scoring Rubric (for Outcomes Grader)
- Total ESG score: Sum of all sub-dimension scores / max possible × 100
- Minimum score to proceed: 50/100
- Flagged for board attention: Any sub-dimension scoring 1 (critical concern)
- Best practice threshold: 75+ overall score

## LP ESG Reporting Requirements
- ADIA: TCFD-aligned climate disclosure required
- CPP Investments: Net-zero portfolio commitment — scope 3 emissions required
- Temasek: TotalValue framework — financial + social + environmental value
- Ontario Teachers': Responsible investing integration — voting rights disclosure
- AustralianSuper: Paris Agreement alignment — stranded asset risk assessment

## UN SDG Mapping (Required in IC Memo)
Map every investment to relevant UN SDGs. Most common for NIIFL:
- SDG 7 (Affordable Clean Energy): Renewable power, energy access
- SDG 9 (Infrastructure & Innovation): Roads, ports, airports, digital
- SDG 11 (Sustainable Cities): Urban infrastructure, affordable housing
- SDG 13 (Climate Action): Emission reduction, climate resilience

## SEBI ESG Disclosure Requirements (AIF Category II)
- Annual ESG report to SEBI with portfolio-level metrics
- Board-level ESG committee or designated ESG officer required
- Incident reporting: Material ESG events within 30 days
"""

# ─────────────────────────────────────────────────────────────────────────────
# SKILL 5 — Outcomes Rubric Skill (used by the grader agent)
# ─────────────────────────────────────────────────────────────────────────────
outcomes_rubric_skill = """
# NIIFL IC Memo Outcomes Rubric
# Loaded by: Outcomes Grader Agent ONLY
# This skill defines what a PASS looks like for every section of the IC memo.

## Section Scoring Rules

### Section 1 — Investment Thesis (PASS criteria)
- PASS: Thesis is 2–4 sentences, clearly states why NIIFL specifically, mentions exit strategy
- FAIL: Vague thesis, no exit strategy, no mention of fund mandate fit

### Section 2 — Market & Competitive Position (PASS criteria)
- PASS: TAM stated with source, competitive landscape has 3+ named competitors, regulatory status confirmed
- FAIL: No TAM, no competitor names, regulatory status unclear

### Section 3 — Financial Returns (PASS criteria)
- PASS: Base case IRR stated vs fund hurdle, MOIC stated, sensitivity table present, 3 scenarios shown
- FAIL: IRR not compared to hurdle, single scenario only, no sensitivity analysis

### Section 4 — Risks & Mitigants (PASS criteria)
- PASS: Minimum 4 risk categories covered, each has a named mitigant and residual risk rating
- FAIL: Fewer than 4 risks, risks listed without mitigants, no residual risk rating

### Section 5 — ESG & Impact (PASS criteria)
- PASS: All 3 NIIFL pillars scored, minimum ESG score ≥ 50/100, UN SDG mapping present
- FAIL: Any pillar missing, no SDG mapping, score below 50

### Section 6 — Policy Alignment (PASS criteria)
- PASS: NIP inclusion stated (yes/no with reason), at least 1 policy framework cited with evidence
- FAIL: No NIP reference, no policy framework cited

### Section 7 — Deal Structure (PASS criteria)
- PASS: Equity stake % stated, board seats stated, key SHA terms listed, CPs listed
- FAIL: Equity % missing, no governance terms, no CPs

### Section 8 — Recommendation (PASS criteria)
- PASS: Clear INVEST/PASS/DEFER stated, ticket size in INR Cr from named fund, next steps listed
- FAIL: Ambiguous recommendation, no ticket size, no next steps

## Overall Pass Criteria
- All 8 sections must individually PASS
- ESG score must be ≥ 50
- IRR must meet or exceed fund hurdle (stated in fund mandate skill)
- If any section FAILS → return to IC memo agent with specific gap description

## Common Failure Patterns (from past memos)
1. Section 3 failure: IRR shown but not compared to hurdle rate — always state "X% vs Y% hurdle"
2. Section 5 failure: ESG section pasted from company CSR report — must be NIIFL's own assessment
3. Section 6 failure: Policy section is 1 sentence — must have specific NIP project code or PLI tranche reference
4. Section 4 failure: Exit risk not addressed — always include "exit risk" even for operating assets
"""

# ─────────────────────────────────────────────────────────────────────────────
# Write all skills to disk
# ─────────────────────────────────────────────────────────────────────────────
skills = {
    "skill_fund_mandate.txt":     fund_mandate_skill,
    "skill_ic_memo_template.txt": ic_memo_template_skill,
    "skill_india_infra.txt":      india_infra_skill,
    "skill_esg_impact.txt":       esg_skill,
    "skill_outcomes_rubric.txt":  outcomes_rubric_skill,
}

for filename, content in skills.items():
    path = os.path.join(SKILLS_DIR, filename)
    with open(path, "w") as f:
        f.write(content.strip())
    print(f"  Created: {path}")

print(f"\nStep 1 complete — {len(skills)} skills written to {SKILLS_DIR}/")
