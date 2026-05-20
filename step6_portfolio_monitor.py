"""
STEP 6 — Portfolio Monitoring Agent
=====================================
Runs post-investment: monitors KPIs, flags underperformance,
prepares board pack summaries, tracks exit readiness.

Usage:
    python3 step6_portfolio_monitor.py
"""

import os, sys, json, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "config"))
from config import ANTHROPIC_API_KEY, SUBAGENT_MODEL, SKILLS_DIR
import anthropic

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def load_skill(f):
    p = os.path.join(SKILLS_DIR, f)
    return open(p).read() if os.path.exists(p) else f"[{f} not found]"

PORTFOLIO_SYSTEM = """You are NIIFL's portfolio monitoring agent. You track
post-investment KPIs for infrastructure and growth equity assets.

Your job for each portfolio company:
1. Compare actual KPIs vs IC memo projections
2. Flag any metric that is >15% below projection as a RED flag
3. Identify early warning signals (debt covenant breaches, management changes, regulatory risks)
4. Assess exit readiness (Is the company ready for IPO / strategic sale / secondary?)
5. Draft board pack talking points for the quarterly portfolio review

{india_infra_skill}

Output as JSON:
{{
  "company": "...",
  "period": "...",
  "kpi_vs_plan": {{
    "revenue": {{"actual": 0, "plan": 0, "variance_pct": 0, "flag": "green|amber|red"}},
    "ebitda":  {{"actual": 0, "plan": 0, "variance_pct": 0, "flag": "green|amber|red"}},
    "traffic_pcus": {{"actual": 0, "plan": 0, "variance_pct": 0, "flag": "green|amber|red"}}
  }},
  "early_warnings": ["Warning 1", "Warning 2"],
  "exit_readiness": "ready|12_months|24_months|not_ready",
  "exit_rationale": "...",
  "board_pack_points": ["Point 1", "Point 2", "Point 3"],
  "recommended_action": "monitor|engage_management|escalate_to_ic|initiate_exit_process"
}}"""

class PortfolioMonitoringAgent:
    def run(self, company_name: str, period: str,
            actuals: dict, ic_projections: dict) -> dict:
        system = PORTFOLIO_SYSTEM.format(
            india_infra_skill=load_skill("skill_india_infra.txt")
        )
        user = f"""
Portfolio Company: {company_name}
Period: {period}

Actual KPIs:
{json.dumps(actuals, indent=2)}

IC Memo Projections (at time of investment):
{json.dumps(ic_projections, indent=2)}

Analyse performance and return the structured monitoring report.
"""
        resp = client.messages.create(
            model=SUBAGENT_MODEL, max_tokens=3000,
            system=system,
            messages=[{"role": "user", "content": user}]
        )
        raw = resp.content[0].text
        try:
            return json.loads(raw.strip().strip("```json").strip("```").strip())
        except json.JSONDecodeError:
            return {"raw_response": raw, "parse_error": True}


if __name__ == "__main__":
    agent = PortfolioMonitoringAgent()
    result = agent.run(
        company_name="Greenway Highways Limited",
        period="Q3 FY2026",
        actuals={
            "revenue_cr": 38.2,
            "ebitda_cr": 33.8,
            "ebitda_margin_pct": 88.5,
            "traffic_pcus_daily": 27800,
            "toll_collection_efficiency_pct": 97.2,
        },
        ic_projections={
            "revenue_cr": 40.0,
            "ebitda_cr": 35.2,
            "ebitda_margin_pct": 88.0,
            "traffic_pcus_daily": 29000,
            "toll_collection_efficiency_pct": 97.5,
        }
    )
    print(json.dumps(result, indent=2))
    print("\nStep 6 complete — Portfolio monitoring agent ready.")
