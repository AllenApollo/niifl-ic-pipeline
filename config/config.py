"""
NIIFL AI Engine — Central Configuration
All agents, MCP servers, and skills reference this file.
"""

import os

# ── API ───────────────────────────────────────────────────────────────────────
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "YOUR_API_KEY_HERE")

# ── Models ────────────────────────────────────────────────────────────────────
ORCHESTRATOR_MODEL  = "claude-opus-4-6"   # Highest reasoning — orchestrator + IC memo
SUBAGENT_MODEL      = "claude-sonnet-4-6" # Speed + cost — DD research, sourcing, modelling
GRADER_MODEL        = "claude-sonnet-4-6" # QA / outcomes grader

# ── Fund definitions ──────────────────────────────────────────────────────────
FUNDS = {
    "master_fund": {
        "name": "NIIF Master Fund",
        "strategy": "Operating assets in core infrastructure",
        "min_ticket_cr": 500,
        "sectors": ["roads", "ports", "airports", "energy", "utilities"],
        "return_hurdle_irr": 12.0,   # % net IRR threshold
        "return_hurdle_moic": 1.8,
        "asset_type": "operating",   # operating | greenfield | growth_equity
        "bilateral": False,
    },
    "strategic_opportunities_fund": {
        "name": "NIIF Strategic Opportunities Fund",
        "strategy": "Growth equity — domestic champions",
        "min_ticket_cr": 100,
        "sectors": ["digital_infra", "manufacturing", "financial_services", "healthcare", "housing"],
        "return_hurdle_irr": 18.0,
        "return_hurdle_moic": 2.5,
        "asset_type": "growth_equity",
        "bilateral": False,
    },
    "private_markets_fund": {
        "name": "NIIF Private Markets Fund",
        "strategy": "Fund of funds — mid-market India managers",
        "min_ticket_cr": 50,
        "sectors": ["climate", "healthcare", "housing", "fintech", "agri"],
        "return_hurdle_irr": 15.0,
        "return_hurdle_moic": 2.0,
        "asset_type": "fund_of_funds",
        "bilateral": False,
    },
    "india_japan_fund": {
        "name": "NIIF India-Japan Fund",
        "strategy": "Bilateral — Japan nexus required",
        "min_ticket_cr": 200,
        "sectors": ["clean_energy", "mobility", "logistics", "smart_cities"],
        "return_hurdle_irr": 14.0,
        "return_hurdle_moic": 2.0,
        "asset_type": "operating",
        "bilateral": True,
        "bilateral_partner": "JBIC",
    },
}

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR        = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS_DIR      = os.path.join(BASE_DIR, "skills")
MCP_DIR         = os.path.join(BASE_DIR, "mcp_servers")
AGENTS_DIR      = os.path.join(BASE_DIR, "agents")
OUTPUTS_DIR     = os.path.join(BASE_DIR, "outputs")

# ── ESG pillars (NIIFL-specific) ──────────────────────────────────────────────
ESG_PILLARS = {
    "environment":    ["renewable_energy", "ev_mobility", "waste_management", "green_buildings"],
    "ease_of_living": ["energy_access", "healthcare", "affordable_housing", "digital_infra"],
    "economic_growth":["job_creation", "export_promotion", "msme_support", "skilling"],
}

# ── Policy frameworks ─────────────────────────────────────────────────────────
POLICY_FRAMEWORKS = [
    "National Infrastructure Pipeline (NIP)",
    "Production Linked Incentive (PLI)",
    "National Monetisation Pipeline (NMP)",
    "PM GatiShakti",
    "Make in India",
]
