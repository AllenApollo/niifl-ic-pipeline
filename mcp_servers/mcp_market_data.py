"""
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