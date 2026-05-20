"""
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