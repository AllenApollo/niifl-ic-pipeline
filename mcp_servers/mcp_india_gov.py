"""
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