"""
STEP 2 — Build MCP Servers (Data Connectors)
=============================================
MCP servers expose external data sources as tools Claude can call.
Each server is a Python class with tool methods.
In production, these become actual HTTP/SSE MCP servers.
For local dev, they run as in-process stubs you wire into agents.

Usage:
    python3 step2_build_mcp_servers.py   # validates all servers start correctly

Real deployment: each class becomes a FastMCP or mcp-python server.
"""

import os, sys, json, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "config"))
from config import MCP_DIR

os.makedirs(MCP_DIR, exist_ok=True)

# ─────────────────────────────────────────────────────────────────────────────
# MCP SERVER 1 — DealCloud CRM
# ─────────────────────────────────────────────────────────────────────────────
dealcloud_mcp = '''"""
MCP Server: DealCloud CRM
Tools exposed to Claude agents:
  - search_deals        : search pipeline by keyword, sector, fund, status
  - get_deal            : fetch a single deal record by ID
  - create_deal         : add new deal to pipeline
  - update_deal_status  : update status (screening / dd / ic_prep / approved / passed)
  - log_agent_action    : write agent audit log entry (SEBI compliance)

Production: Replace stub data with real DealCloud API calls.
DealCloud API docs: https://dealcloud.com/api/v1
"""

import json
from datetime import datetime

DEALS_DB = {
    "DC001": {
        "id": "DC001", "name": "Greenway Highways Ltd",
        "sector": "roads", "fund": "master_fund",
        "ticket_cr": 800, "status": "ic_prep",
        "irr_base": 13.2, "moic": 2.1,
        "entry_date": "2025-01-15", "deal_lead": "Rajiv Sharma",
    },
    "DC002": {
        "id": "DC002", "name": "SunGrid Renewables Pvt Ltd",
        "sector": "energy", "fund": "india_japan_fund",
        "ticket_cr": 650, "status": "dd",
        "irr_base": 14.8, "moic": 2.3,
        "entry_date": "2025-02-01", "deal_lead": "Priya Nair",
    },
}
AUDIT_LOG = []

def search_deals(keyword: str = "", fund: str = "", sector: str = "", status: str = "") -> dict:
    """Search DealCloud pipeline. Returns list of matching deals."""
    results = []
    for deal in DEALS_DB.values():
        if keyword and keyword.lower() not in deal["name"].lower():
            continue
        if fund and deal["fund"] != fund:
            continue
        if sector and deal["sector"] != sector:
            continue
        if status and deal["status"] != status:
            continue
        results.append(deal)
    return {"deals": results, "count": len(results)}

def get_deal(deal_id: str) -> dict:
    """Fetch full deal record by ID."""
    deal = DEALS_DB.get(deal_id)
    if not deal:
        return {"error": f"Deal {deal_id} not found"}
    return deal

def create_deal(name: str, sector: str, fund: str, ticket_cr: float, deal_lead: str) -> dict:
    """Create new deal record in DealCloud."""
    new_id = f"DC{len(DEALS_DB)+1:03d}"
    DEALS_DB[new_id] = {
        "id": new_id, "name": name, "sector": sector,
        "fund": fund, "ticket_cr": ticket_cr,
        "status": "screening", "deal_lead": deal_lead,
        "entry_date": datetime.now().strftime("%Y-%m-%d"),
    }
    return {"created": True, "deal_id": new_id}

def update_deal_status(deal_id: str, status: str, notes: str = "") -> dict:
    """Update deal status and log the change."""
    if deal_id not in DEALS_DB:
        return {"error": f"Deal {deal_id} not found"}
    DEALS_DB[deal_id]["status"] = status
    log_agent_action(deal_id, "status_update", f"Status -> {status}. {notes}")
    return {"updated": True, "deal_id": deal_id, "new_status": status}

def log_agent_action(deal_id: str, action_type: str, description: str, agent: str = "system") -> dict:
    """Write to SEBI-compliant audit log. Every agent action must call this."""
    entry = {
        "timestamp": datetime.now().isoformat(),
        "deal_id": deal_id,
        "agent": agent,
        "action_type": action_type,
        "description": description,
    }
    AUDIT_LOG.append(entry)
    return {"logged": True, "entry": entry}

if __name__ == "__main__":
    print("DealCloud MCP — tool test:")
    print(json.dumps(search_deals(fund="master_fund"), indent=2))
    print(json.dumps(get_deal("DC001"), indent=2))
'''

# ─────────────────────────────────────────────────────────────────────────────
# MCP SERVER 2 — PitchBook / Capital IQ (Market Data)
# ─────────────────────────────────────────────────────────────────────────────
pitchbook_mcp = '''"""
MCP Server: Market Data (PitchBook + Capital IQ)
Tools exposed:
  - search_companies     : search by sector, geography, revenue range
  - get_company_profile  : full company profile with financials
  - get_deal_comps       : recent comparable transactions in sector
  - get_public_comps     : public company trading multiples for benchmarking
  - get_fund_benchmarks  : PE/infra fund return benchmarks by vintage year

Production: Replace stubs with PitchBook API (api.pitchbook.com) and 
            Capital IQ API (capitaliq.spglobal.com) calls.
"""

import json

def search_companies(sector: str, country: str = "India", min_revenue_cr: float = 0) -> dict:
    """Search for companies matching criteria."""
    stub = [
        {"name": "Greenway Highways Ltd", "sector": sector, "revenue_cr": 850, "ebitda_margin": 88},
        {"name": "SunGrid Power Pvt Ltd", "sector": sector, "revenue_cr": 420, "ebitda_margin": 91},
    ]
    return {"companies": stub, "source": "PitchBook", "as_of": "2025-Q1"}

def get_company_profile(company_name: str) -> dict:
    """Full company profile including ownership, financials, key management."""
    return {
        "name": company_name,
        "founded": 2012,
        "hq": "Mumbai, India",
        "employees": 1240,
        "revenue_cr": 850,
        "ebitda_cr": 748,
        "ebitda_margin_pct": 88.0,
        "debt_cr": 2100,
        "net_debt_ebitda": 2.8,
        "shareholders": [{"name": "Promoter Group", "pct": 65}, {"name": "PE Fund", "pct": 35}],
        "source": "PitchBook",
    }

def get_deal_comps(sector: str, asset_type: str = "operating", num_comps: int = 5) -> dict:
    """Recent comparable M&A transactions for valuation benchmarking."""
    comps = [
        {"target": "Highway Asset Alpha", "sector": sector, "ev_cr": 4200, "ev_ebitda": 14.2, "date": "2024-11"},
        {"target": "Port Terminal Beta",  "sector": sector, "ev_cr": 3800, "ev_ebitda": 16.8, "date": "2024-09"},
        {"target": "Road Concession Co",  "sector": sector, "ev_cr": 2900, "ev_ebitda": 13.5, "date": "2024-06"},
    ]
    return {"comps": comps[:num_comps], "source": "PitchBook + Capital IQ", "asset_type": asset_type}

def get_public_comps(sector: str) -> dict:
    """Public company trading multiples for the sector."""
    return {
        "sector": sector,
        "companies": [
            {"name": "IRB Infrastructure", "ev_ebitda": 12.4, "pe": 18.2, "mktcap_cr": 14200},
            {"name": "Adani Ports", "ev_ebitda": 17.8, "pe": 24.1, "mktcap_cr": 195000},
        ],
        "median_ev_ebitda": 15.1,
        "source": "Capital IQ",
        "as_of": "2025-05",
    }

def get_fund_benchmarks(fund_type: str = "infrastructure", vintage_year: int = 2020) -> dict:
    """PE/infrastructure fund return benchmarks by vintage year."""
    return {
        "fund_type": fund_type,
        "vintage": vintage_year,
        "top_quartile_irr": 16.2,
        "median_irr": 12.8,
        "bottom_quartile_irr": 9.1,
        "top_quartile_moic": 2.4,
        "median_moic": 1.9,
        "source": "PitchBook Benchmarks",
    }

if __name__ == "__main__":
    print(json.dumps(get_deal_comps("roads"), indent=2))
'''

# ─────────────────────────────────────────────────────────────────────────────
# MCP SERVER 3 — India Government Data (NITI Aayog, MCA21, CEA)
# ─────────────────────────────────────────────────────────────────────────────
india_gov_mcp = '''"""
MCP Server: India Government Data Sources
Tools exposed:
  - search_nip_projects   : search National Infrastructure Pipeline
  - get_mca21_filing      : company registrar filings from MCA21
  - get_cea_power_data    : Central Electricity Authority generation data
  - get_nhai_traffic_data : NHAI ATVM traffic statistics for toll roads
  - get_sebi_aif_data     : SEBI AIF disclosure data for benchmarking

Production: 
  - NIP: NITI Aayog API / web scraper (niti.gov.in)
  - MCA21: Ministry of Corporate Affairs API (api.mca.gov.in)
  - CEA: Central Electricity Authority data portal (cea.nic.in)
  - NHAI: NHAI FASTag data (ihmcl.com)
  - SEBI: SEBI data portal (sebi.gov.in)
"""

import json

def search_nip_projects(sector: str, state: str = "", min_size_cr: float = 0) -> dict:
    """Search National Infrastructure Pipeline projects."""
    projects = [
        {
            "project_id": "NIP-RD-2024-1823",
            "name": "4-laning of NH-48 Bengaluru–Chennai",
            "sector": "roads", "state": "Karnataka/Tamil Nadu",
            "total_cost_cr": 12400, "mode": "HAM",
            "status": "Under Implementation",
            "private_investment_cr": 8200,
        },
        {
            "project_id": "NIP-EN-2024-0912",
            "name": "5 GW Solar Park — Rajasthan",
            "sector": "energy", "state": "Rajasthan",
            "total_cost_cr": 22000, "mode": "PPP",
            "status": "Tendering",
            "private_investment_cr": 22000,
        },
    ]
    filtered = [p for p in projects if sector.lower() in p["sector"].lower()]
    return {"projects": filtered, "source": "NITI Aayog NIP Dashboard", "total_nip_outlay_lakh_cr": 111}

def get_mca21_filing(company_cin: str) -> dict:
    """Fetch company registration, directors, charges from MCA21."""
    return {
        "cin": company_cin,
        "company_name": "Greenway Highways Limited",
        "date_of_incorporation": "2012-03-15",
        "registered_office": "Mumbai, Maharashtra",
        "authorized_capital_cr": 500,
        "paid_up_capital_cr": 320,
        "directors": [
            {"name": "Arun Mehta", "din": "00123456", "designation": "MD & CEO"},
            {"name": "Sunita Rao",  "din": "00234567", "designation": "Independent Director"},
        ],
        "charges": [
            {"charge_id": "10045678", "charge_holder": "SBI", "amount_cr": 1800, "status": "Subsisting"},
        ],
        "source": "MCA21",
        "last_filing_date": "2024-10-31",
    }

def get_cea_power_data(state: str = "", fuel_type: str = "") -> dict:
    """Power generation statistics from Central Electricity Authority."""
    return {
        "installed_capacity_gw": {"total": 442, "renewable": 203, "thermal": 211, "hydro": 28},
        "generation_twh_fy24": 1736,
        "renewable_share_pct": 23.4,
        "avg_plf_thermal_pct": 65.2,
        "solar_plf_pct": 21.8,
        "wind_plf_pct": 31.4,
        "peak_demand_gw": 243,
        "t&d_losses_pct": 18.2,
        "source": "CEA Monthly Generation Report, April 2025",
    }

def get_nhai_traffic_data(highway_code: str) -> dict:
    """NHAI ATVM FASTag traffic statistics for toll roads."""
    return {
        "highway": highway_code,
        "pcus_daily_avg": 28400,
        "yoy_growth_pct": 7.8,
        "toll_collection_cr_fy24": 142,
        "top_vehicle_category": "LCV",
        "peak_month": "December",
        "source": "NHAI FASTag ATVM Data",
    }

def get_sebi_aif_data(category: str = "II", strategy: str = "infrastructure") -> dict:
    """SEBI AIF industry data for benchmarking."""
    return {
        "aif_category": category,
        "total_aum_cr": 842000,
        "num_funds": 1284,
        "infrastructure_aif_aum_cr": 186000,
        "avg_fund_size_cr": 1420,
        "top_quartile_irr": 17.2,
        "median_irr": 13.1,
        "source": "SEBI AIF Industry Report Q3 FY25",
    }

if __name__ == "__main__":
    print(json.dumps(search_nip_projects("roads"), indent=2))
    print(json.dumps(get_mca21_filing("U45203MH2012PLC123456"), indent=2))
'''

# ─────────────────────────────────────────────────────────────────────────────
# Write MCP server files
# ─────────────────────────────────────────────────────────────────────────────
mcp_servers = {
    "mcp_dealcloud.py":    dealcloud_mcp,
    "mcp_market_data.py":  pitchbook_mcp,
    "mcp_india_gov.py":    india_gov_mcp,
}

for filename, content in mcp_servers.items():
    path = os.path.join(MCP_DIR, filename)
    with open(path, "w") as f:
        f.write(content.strip())
    print(f"  Created: {path}")

# ── Validation: import and basic test ────────────────────────────────────────
print("\nValidating MCP servers...")
sys.path.insert(0, MCP_DIR)

import importlib, importlib.util

for filename in mcp_servers.keys():
    mod_name = filename.replace(".py", "")
    spec = importlib.util.spec_from_file_location(mod_name, os.path.join(MCP_DIR, filename))
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    print(f"  OK: {mod_name}")

print(f"\nStep 2 complete — {len(mcp_servers)} MCP servers written and validated.")
