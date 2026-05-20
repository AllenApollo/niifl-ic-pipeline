"""
STEP 3 — Build Specialised Subagents
=====================================
Four Claude-powered agents, each with:
  - A focused system prompt
  - Access to specific skills and MCP tools
  - A structured run() method returning typed output

Usage:
    python3 step3_build_agents.py        # runs a smoke test on each agent
    from step3_build_agents import *     # import agents into orchestrator

All agents use the Anthropic Messages API directly.
In production, wire MCP tool calls to actual server responses.
"""

import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "config"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "mcp_servers"))

from config import (ANTHROPIC_API_KEY, SUBAGENT_MODEL, ORCHESTRATOR_MODEL,
                    SKILLS_DIR, OUTPUTS_DIR, FUNDS)
import anthropic

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

# ── Skill loader ──────────────────────────────────────────────────────────────
def load_skill(skill_file: str) -> str:
    path = os.path.join(SKILLS_DIR, skill_file)
    if not os.path.exists(path):
        return f"[Skill file {skill_file} not found — run step1_build_skills.py first]"
    with open(path) as f:
        return f.read()

def call_claude(system: str, user: str, model: str = SUBAGENT_MODEL,
                max_tokens: int = 4096) -> str:
    """Minimal wrapper around the Anthropic Messages API."""
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    return response.content[0].text


# ═════════════════════════════════════════════════════════════════════════════
# AGENT 1 — Deal Sourcing Agent
# ═════════════════════════════════════════════════════════════════════════════
class DealSourcingAgent:
    """
    Scans market data and inbound deal flow to identify and score opportunities
    against NIIFL's four fund mandates.
    MCP tools used: PitchBook/Capital IQ, NITI Aayog NIP, DealCloud (write)
    """

    SYSTEM = """You are NIIFL's deal sourcing agent. Your job is to evaluate whether
an inbound deal opportunity fits one of NIIFL's four fund mandates, and to score it.

{fund_mandate_skill}

## Your Output Format
Always respond with a valid JSON object:
{{
  "deal_name": "...",
  "recommended_fund": "master_fund|strategic_opportunities_fund|private_markets_fund|india_japan_fund|no_fit",
  "fit_score": 0-100,
  "fit_rationale": "...",
  "pass_screen": true|false,
  "reject_reason": "... (only if pass_screen=false)",
  "suggested_ticket_cr": 0,
  "key_questions": ["Question 1 for DD team", "Question 2"],
  "nip_project_relevant": true|false
}}

Be strict. If the deal does not clearly fit a fund mandate, recommend no_fit and pass_screen=false.
Never approve a deal that violates mandatory exclusions."""

    def run(self, deal_brief: str) -> dict:
        """
        Args:
            deal_brief: Free-text description of the deal opportunity
        Returns:
            Structured screening result dict
        """
        system = self.SYSTEM.format(
            fund_mandate_skill=load_skill("skill_fund_mandate.txt")
        )
        raw = call_claude(system, f"Evaluate this deal:\n\n{deal_brief}")
        try:
            # Strip markdown code fences if present
            clean = raw.strip().strip("```json").strip("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            return {"raw_response": raw, "parse_error": True}


# ═════════════════════════════════════════════════════════════════════════════
# AGENT 2 — DD Research Agent
# ═════════════════════════════════════════════════════════════════════════════
class DDResearchAgent:
    """
    Conducts market, competitive, regulatory, and management due diligence.
    Synthesises data room documents, expert call transcripts, and public sources.
    MCP tools used: Google Drive, MCA21, CEA, PitchBook, web search
    """

    SYSTEM = """You are NIIFL's due diligence research agent. You are conducting DD on
an infrastructure or growth equity investment opportunity for NIIFL.

{india_infra_skill}
{esg_skill}

## Your Task
Produce a structured DD research summary covering:
1. Market analysis (TAM, growth, regulation)
2. Competitive landscape (named competitors, market share, barriers to entry)
3. Management background (promoter track record, key person risks)
4. Regulatory and legal risks (clearances, litigation, SEBI/regulatory issues)
5. ESG preliminary assessment (score each NIIFL pillar 1-5 with rationale)
6. Policy alignment (NIP, PLI, NMP relevance)
7. Key red flags (anything that could be a deal-stopper)
8. Recommended follow-up questions for management

## Output Format
Respond as a JSON object with keys:
market_analysis, competitive_landscape, management_assessment,
regulatory_risks, esg_preliminary, policy_alignment, red_flags,
follow_up_questions, overall_dd_confidence (High/Medium/Low)"""

    def run(self, deal_name: str, deal_brief: str, sector: str,
            fund: str, data_room_summary: str = "") -> dict:
        system = self.SYSTEM.format(
            india_infra_skill=load_skill("skill_india_infra.txt"),
            esg_skill=load_skill("skill_esg_impact.txt"),
        )
        user = f"""
Deal: {deal_name}
Sector: {sector}
Fund: {fund}
Brief: {deal_brief}
Data room summary: {data_room_summary or 'Not yet available — use market knowledge.'}

Conduct comprehensive DD research and return the structured JSON summary.
"""
        raw = call_claude(system, user, max_tokens=6000)
        try:
            clean = raw.strip().strip("```json").strip("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            return {"raw_response": raw, "parse_error": True}


# ═════════════════════════════════════════════════════════════════════════════
# AGENT 3 — Financial Modelling Agent
# ═════════════════════════════════════════════════════════════════════════════
class FinancialModellingAgent:
    """
    Builds and stress-tests financial models. Uses concession DCF for Master Fund
    assets, growth equity DCF for SOF, cross-currency DCF for IJF.
    MCP tools used: Capital IQ (comps), Excel skill (output), code execution
    """

    SYSTEM = """You are NIIFL's financial modelling agent. You build infrastructure
and growth equity financial models to evaluate investment returns.

{india_infra_skill}

## Your Task
Given deal parameters, produce:
1. Base case financial model (5-year projection + terminal value)
2. Bull and bear case sensitivity
3. Entry valuation and implied multiples
4. Returns analysis: Gross IRR, Net IRR (after 2% mgmt fee + 20% carry), MOIC
5. Sensitivity table: 2 key variables, 3 scenarios each
6. Comparable transaction multiples for entry/exit benchmarking

## Model Type Selection
- Sector = roads/ports/airports/energy → Concession DCF model
- Sector = digital_infra/manufacturing/healthcare → Growth equity DCF
- Fund = india_japan_fund → Add cross-currency analysis (JPY/INR)
- Fund = private_markets_fund → IRR attribution model (DPI, TVPI, RVPI)

## Output Format
Return a JSON object with:
model_type, key_assumptions, revenue_projections (5yr array),
ebitda_projections (5yr array), fcf_projections (5yr array),
entry_ev_cr, entry_ev_ebitda, exit_ev_ebitda,
base_irr, bull_irr, bear_irr, base_moic,
net_irr_after_fees, sensitivity_table,
comparable_transactions (list), model_confidence (High/Medium/Low),
key_model_risks"""

    def run(self, deal_name: str, sector: str, fund: str,
            financials: dict, deal_terms: dict) -> dict:
        system = self.SYSTEM.format(
            india_infra_skill=load_skill("skill_india_infra.txt")
        )
        user = f"""
Deal: {deal_name}
Sector: {sector}
Fund: {fund}

Historical Financials:
{json.dumps(financials, indent=2)}

Proposed Deal Terms:
{json.dumps(deal_terms, indent=2)}

Build the financial model and return the complete JSON output.
Use India infrastructure benchmarks from your skill knowledge.
"""
        raw = call_claude(system, user, max_tokens=6000)
        try:
            clean = raw.strip().strip("```json").strip("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            return {"raw_response": raw, "parse_error": True}


# ═════════════════════════════════════════════════════════════════════════════
# AGENT 4 — IC Memo Drafting Agent  (uses Opus — highest quality)
# ═════════════════════════════════════════════════════════════════════════════
class ICMemoDraftingAgent:
    """
    Drafts the full IC memo from DD research + financial model outputs.
    Uses Claude Opus for highest quality output.
    MCP tools used: Google Drive (read past memos), DOCX skill (output)
    """

    SYSTEM = """You are NIIFL's IC memo drafting agent. You write professional,
partner-ready Investment Committee memoranda for India's premier sovereign-anchored
infrastructure fund. Every memo must be precise, evidence-based, and ready for
presentation to NIIFL's IC without further editing of facts.

{ic_memo_template}
{esg_skill}

## Writing Standards
- Use formal but clear language — no jargon without explanation
- Every financial figure must have a source or calculation basis stated
- Every risk must have a named mitigant
- IRR must always be stated vs fund hurdle rate
- ESG section must be NIIFL's own assessment — not the company's CSR report
- Section 8 (Recommendation) must be unambiguous: INVEST / PASS / DEFER

## Output Format
Return a JSON object where each key is a section name and value is the
fully drafted section text (in professional memo prose, not bullet points).
Keys: thesis, market_analysis, financial_returns, risks_mitigants,
esg_impact, policy_alignment, deal_structure, recommendation"""

    def run(self, deal_name: str, fund: str,
            dd_research: dict, financial_model: dict,
            deal_terms: dict) -> dict:
        system = self.SYSTEM.format(
            ic_memo_template=load_skill("skill_ic_memo_template.txt"),
            esg_skill=load_skill("skill_esg_impact.txt"),
        )
        user = f"""
Deal: {deal_name}
Fund: {fund}
Fund hurdle IRR: {FUNDS[fund]['return_hurdle_irr']}%
Fund hurdle MOIC: {FUNDS[fund]['return_hurdle_moic']}x

DD Research Summary:
{json.dumps(dd_research, indent=2)}

Financial Model:
{json.dumps(financial_model, indent=2)}

Deal Terms:
{json.dumps(deal_terms, indent=2)}

Draft the complete IC memo. Each section must be substantive prose ready
for IC presentation. Do not use placeholder text.
"""
        raw = call_claude(system, user, model=ORCHESTRATOR_MODEL, max_tokens=8000)
        try:
            clean = raw.strip().strip("```json").strip("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            return {"raw_response": raw, "parse_error": True}


# ═════════════════════════════════════════════════════════════════════════════
# AGENT 5 — Outcomes Grader Agent
# ═════════════════════════════════════════════════════════════════════════════
class OutcomesGraderAgent:
    """
    QA agent that scores the IC memo draft against NIIFL's outcomes rubric.
    Runs automatically after IC memo draft — before human review.
    Sends memo back to IC memo agent if any section fails.
    """

    SYSTEM = """You are NIIFL's outcomes grader agent. Your only job is to
evaluate an IC memo draft against NIIFL's quality rubric and return a
structured pass/fail assessment.

{outcomes_rubric}

## Grading Rules
- Score each of the 8 sections as PASS or FAIL with a specific reason
- Identify any data gaps or factual inconsistencies across sections
- Check IRR vs fund hurdle (stated in the memo)
- Check ESG score ≥ 50 (stated in the memo)
- If ANY section fails → overall_pass = false
- List all gaps that must be fixed before human review

## Output Format
Return a JSON object:
{{
  "overall_pass": true|false,
  "section_results": {{
    "thesis": {{"pass": true|false, "reason": "..."}},
    "market_analysis": {{"pass": true|false, "reason": "..."}},
    "financial_returns": {{"pass": true|false, "reason": "..."}},
    "risks_mitigants": {{"pass": true|false, "reason": "..."}},
    "esg_impact": {{"pass": true|false, "reason": "..."}},
    "policy_alignment": {{"pass": true|false, "reason": "..."}},
    "deal_structure": {{"pass": true|false, "reason": "..."}},
    "recommendation": {{"pass": true|false, "reason": "..."}}
  }},
  "gaps_to_fix": ["Gap 1 description", "Gap 2 description"],
  "quality_score": 0-100,
  "grader_notes": "Overall assessment in 2 sentences"
}}"""

    def run(self, memo_sections: dict, fund: str) -> dict:
        system = self.SYSTEM.format(
            outcomes_rubric=load_skill("skill_outcomes_rubric.txt")
        )
        user = f"""
Fund: {fund}
Fund hurdle IRR: {FUNDS[fund]['return_hurdle_irr']}%

IC Memo Draft to Grade:
{json.dumps(memo_sections, indent=2)}

Grade every section strictly against the rubric. Be precise about failures.
"""
        raw = call_claude(system, user, max_tokens=3000)
        try:
            clean = raw.strip().strip("```json").strip("```").strip()
            return json.loads(clean)
        except json.JSONDecodeError:
            return {"raw_response": raw, "parse_error": True}


# ─────────────────────────────────────────────────────────────────────────────
# Smoke test
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("Step 3 — Agent smoke test")
    print("=" * 60)

    test_deal = """
    Greenway Highways Limited operates a 280 km 4-lane tolled highway 
    on NH-48 under a 30-year NHAI concession. Revenue INR 142 Cr FY24,
    EBITDA margin 88%. Traffic CAGR 8% over last 5 years. NIIFL would
    acquire a 49% stake for INR 800 Cr implying EV of ~INR 4,200 Cr.
    """

    print("\n[1] Deal Sourcing Agent")
    sourcing = DealSourcingAgent()
    result = sourcing.run(test_deal)
    print(json.dumps(result, indent=2))

    print("\nStep 3 complete — all 5 agent classes defined and importable.")
    print("Agents: DealSourcingAgent, DDResearchAgent, FinancialModellingAgent,")
    print("        ICMemoDraftingAgent, OutcomesGraderAgent")
