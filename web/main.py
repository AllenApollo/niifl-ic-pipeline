"""
NIIFL AI Engine — FastAPI Backend
===================================
Runs the web server that the investment team uses.

Start with:
    python3 web/main.py

Then open: http://localhost:8000

All pipeline steps (agents, orchestrator, memo formatter) are
called from here as async background tasks so the UI stays
responsive while agents run.
"""

import os
import sys
import json
import uuid
import time
import asyncio
import datetime
from pathlib import Path
from typing import Optional

# ── Path setup so we can import from parent directory ────────────────────────
WEB_DIR    = Path(__file__).parent
ROOT_DIR   = WEB_DIR.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(ROOT_DIR / "config"))
sys.path.insert(0, str(ROOT_DIR / "mcp_servers"))

from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ── In-memory deal store (replace with DB in production) ─────────────────────
# Structure: { deal_id: { ...deal_data, status, memo, grader } }
DEALS: dict = {}
AGENT_STATUS: dict = {
    "orchestrator":         {"status": "idle", "current_deal": None, "completed_at": None},
    "deal_sourcing":        {"status": "idle", "current_deal": None, "completed_at": None},
    "dd_research":          {"status": "idle", "current_deal": None, "completed_at": None},
    "financial_modelling":  {"status": "idle", "current_deal": None, "completed_at": None},
    "ic_memo_drafting":     {"status": "idle", "current_deal": None, "completed_at": None},
    "outcomes_grader":      {"status": "idle", "current_deal": None, "completed_at": None},
}
ACTIVITY_LOG: list = [
    {"type": "grading",   "text": "IC memo ready — Greenway Highways passed QA (84/100). Partner review required.", "icon": "ti-check",     "bg": "var(--green-bg)",  "color": "var(--green)",  "agent": "Outcomes grader",           "ts": time.time() - 120},
    {"type": "memo",      "text": "Memo drafted — SunGrid Renewables 8-section memo complete. ESG 81/100.",         "icon": "ti-file-text", "bg": "var(--purple-bg)", "color": "var(--purple)", "agent": "IC memo agent",             "ts": time.time() - 1080},
    {"type": "modelling", "text": "Model complete — SunGrid base IRR 14.8% vs 14% IJF hurdle.",                     "icon": "ti-chart-bar", "bg": "#dbeafe",          "color": "#1e40af",       "agent": "Financial modelling agent", "ts": time.time() - 2040},
]

# ── Seed demo deals so the UI isn't empty on first load ──────────────────────
DEALS["DC001"] = {
    "deal_id": "DC001", "name": "Greenway Highways Ltd",
    "sector": "roads", "fund": "master_fund", "ticket_cr": 800,
    "stake_pct": 49, "entry_ev_cr": 4200, "deal_lead": "Rajiv Sharma",
    "status": "partner_review", "quality_score": 84,
    "irr_base": 13.2, "moic": 2.1,
    "submitted_at": "2026-05-05T09:14:00",
    "brief": "280km NH-48 tolled highway under 30-yr NHAI concession.",
    "memo_ready": True,
    "memo_sections": {
        "thesis": "Greenway Highways offers high-quality exposure to India's tolled road infrastructure with 22 years concession remaining and resilient WPI-linked revenue.",
        "market_analysis": "NH-48 corridor serves the Bengaluru–Chennai industrial belt. Traffic CAGR 7.8% over 5 years; NHAI ATVM data confirms consistent growth.",
        "financial_returns": "Base IRR 13.2% vs 12.0% hurdle. MOIC 2.1x. Bull 16.8%, Bear 10.1%. Entry 14.2x EV/EBITDA.",
        "risks_mitigants": "Traffic risk: mitigated by diversified vehicle mix and growing corridor demand. Regulatory: NHAI step-in rights intact.",
        "esg_impact": "ESG score 74/100. SDG 9 and 11 aligned. 1,240 direct jobs. INR 18Cr annual GST contribution.",
        "policy_alignment": "Confirmed in NIP (NIP-RD-2024-1823). PM GatiShakti multimodal node designation pending.",
        "deal_structure": "49% equity stake. 2 board seats. Tag/drag/ROFR in SHA. Senior debt INR 1,800Cr at 8.4% p.a.",
        "recommendation": "INVEST — INR 800 Cr from NIIF Master Fund. Authorise term sheet and exclusivity.",
    },
    "grader": {"overall_pass": True, "quality_score": 84, "grader_notes": "All 8 sections pass. Minor gap in exit risk section — add secondary buyer universe."},
}
DEALS["DC002"] = {
    "deal_id": "DC002", "name": "SunGrid Renewables Pvt Ltd",
    "sector": "energy", "fund": "india_japan_fund", "ticket_cr": 650,
    "stake_pct": 51, "entry_ev_cr": 3800, "deal_lead": "Priya Nair",
    "status": "ic_prep", "quality_score": 76,
    "irr_base": 14.8, "moic": 2.3,
    "submitted_at": "2026-05-06T11:30:00",
    "brief": "5GW solar platform with Nippon Electric as Japan technology partner.",
    "memo_ready": True,
    "memo_sections": {
        "thesis": "SunGrid is India's fastest-growing utility-scale solar platform, offering IJF exposure to clean energy with a credible Japanese technology partnership.",
        "market_analysis": "Indian solar market 203GW installed; SunGrid holds 2.4% share. PPA-backed revenue provides visibility.",
        "financial_returns": "Base IRR 14.8% vs 14.0% IJF hurdle. MOIC 2.3x. Cross-currency hedge adds 40bps net IRR.",
        "risks_mitigants": "DISCOM payment risk: mitigated by payment security mechanism and letter of credit. Grid curtailment: <3% historically.",
        "esg_impact": "ESG score 81/100. 890MW renewable capacity displacing 680kt CO2/year. SDG 7 and 13 aligned.",
        "policy_alignment": "NIP-EN-2024-0912. PLI solar manufacturing component eligible. PM-KUSUM alignment for rural solar.",
        "deal_structure": "51% equity. 3 board seats. JBIC co-invest 30% on same terms. Anti-dilution ratchet if IRR <12%.",
        "recommendation": "INVEST — INR 650 Cr from NIIF India-Japan Fund. Proceed to final IC with JBIC confirmation.",
    },
    "grader": {"overall_pass": True, "quality_score": 76, "grader_notes": "Policy section thin — NMP alignment not stated. ESG good. Recommend adding JBIC environmental checklist."},
}
DEALS["DC003"] = {
    "deal_id": "DC003", "name": "IndiaStack Digital Infra",
    "sector": "digital_infra", "fund": "strategic_opportunities_fund", "ticket_cr": 320,
    "stake_pct": 35, "entry_ev_cr": 1800, "deal_lead": "Amit Verma",
    "status": "dd", "quality_score": None,
    "submitted_at": "2026-05-07T08:00:00",
    "brief": "B2B digital infrastructure SaaS platform serving 400+ enterprise clients.",
    "memo_ready": False, "memo_sections": {}, "grader": None,
}

app = FastAPI(title="NIIFL AI Engine", version="1.0.0")

app.add_middleware(CORSMiddleware,
    allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Serve static files
app.mount("/static", StaticFiles(directory=str(WEB_DIR / "static")), name="static")

# ── Request models ────────────────────────────────────────────────────────────
class DealSubmission(BaseModel):
    name: str
    fund: str
    sector: str
    ticket_cr: float
    stake_pct: float
    entry_ev_cr: float
    deal_lead: str
    brief: str
    revenue_fy22: Optional[float] = 0
    revenue_fy23: Optional[float] = 0
    revenue_fy24: Optional[float] = 0
    ebitda_fy22:  Optional[float] = 0
    ebitda_fy23:  Optional[float] = 0
    ebitda_fy24:  Optional[float] = 0
    net_debt_fy24: Optional[float] = 0
    net_worth_fy24: Optional[float] = 0

class ActivityEvent(BaseModel):
    type: str
    text: str
    icon: Optional[str] = "ti-check"
    bg: Optional[str] = "var(--green-bg)"
    color: Optional[str] = "var(--green)"
    agent: Optional[str] = ""

# ── Background pipeline runner ────────────────────────────────────────────────
async def run_pipeline_background(deal_id: str, submission: DealSubmission):
    """Runs the full AI pipeline in the background. Updates DEALS[deal_id] as stages complete."""
    deal = DEALS[deal_id]
    AGENT_STATUS["orchestrator"]["status"] = "running"
    AGENT_STATUS["orchestrator"]["current_deal"] = deal["name"]

    try:
        # Stage 1: Screening
        deal["status"] = "screening"
        AGENT_STATUS["deal_sourcing"]["status"] = "running"
        AGENT_STATUS["deal_sourcing"]["current_deal"] = deal["name"]
        await asyncio.sleep(0.1)  # yield to event loop

        from step3_build_agents import DealSourcingAgent
        sourcing = DealSourcingAgent()
        screen = sourcing.run(submission.brief)
        AGENT_STATUS["deal_sourcing"]["status"] = "idle"

        if not screen.get("pass_screen"):
            deal["status"] = "rejected"
            deal["reject_reason"] = screen.get("reject_reason", "Did not pass AI screen")
            return

        # Stage 2: DD Research
        deal["status"] = "dd"
        AGENT_STATUS["dd_research"]["status"] = "running"
        AGENT_STATUS["dd_research"]["current_deal"] = deal["name"]

        from step3_build_agents import DDResearchAgent
        dd = DDResearchAgent()
        dd_result = dd.run(
            deal_name=submission.name,
            deal_brief=submission.brief,
            sector=submission.sector,
            fund=submission.fund,
        )
        deal["dd_result"] = dd_result
        AGENT_STATUS["dd_research"]["status"] = "idle"

        # Stage 3: Financial Modelling
        AGENT_STATUS["financial_modelling"]["status"] = "running"
        AGENT_STATUS["financial_modelling"]["current_deal"] = deal["name"]

        from step3_build_agents import FinancialModellingAgent
        modelling = FinancialModellingAgent()
        financials = {
            "revenue_cr": {"FY22": submission.revenue_fy22, "FY23": submission.revenue_fy23, "FY24": submission.revenue_fy24},
            "ebitda_cr":  {"FY22": submission.ebitda_fy22,  "FY23": submission.ebitda_fy23,  "FY24": submission.ebitda_fy24},
            "net_debt_cr": {"FY24": submission.net_debt_fy24},
            "net_worth_cr": {"FY24": submission.net_worth_fy24},
        }
        deal_terms = {
            "sector": submission.sector, "ticket_cr": submission.ticket_cr,
            "stake_pct": submission.stake_pct, "entry_ev_cr": submission.entry_ev_cr,
        }
        model_result = modelling.run(submission.name, submission.sector, submission.fund, financials, deal_terms)
        deal["model_result"] = model_result
        deal["irr_base"] = model_result.get("base_irr")
        deal["moic"] = model_result.get("base_moic")
        AGENT_STATUS["financial_modelling"]["status"] = "idle"

        # Stage 4: IC Memo
        deal["status"] = "ic_prep"
        AGENT_STATUS["ic_memo_drafting"]["status"] = "running"
        AGENT_STATUS["ic_memo_drafting"]["current_deal"] = deal["name"]

        from step3_build_agents import ICMemoDraftingAgent, OutcomesGraderAgent
        memo_agent = ICMemoDraftingAgent()
        grader_agent = OutcomesGraderAgent()

        memo_sections = None
        grader_result = None
        for attempt in range(3):
            memo_sections = memo_agent.run(
                deal_name=submission.name, fund=submission.fund,
                dd_research=dd_result, financial_model=model_result,
                deal_terms=deal_terms,
            )
            AGENT_STATUS["ic_memo_drafting"]["status"] = "idle"
            AGENT_STATUS["outcomes_grader"]["status"] = "running"
            grader_result = grader_agent.run(memo_sections, submission.fund)
            AGENT_STATUS["outcomes_grader"]["status"] = "idle"
            if grader_result.get("overall_pass"):
                break

        deal["memo_sections"] = memo_sections if not isinstance(memo_sections, dict) or not memo_sections.get("parse_error") else {}
        deal["memo_ready"] = bool(grader_result and grader_result.get("overall_pass"))
        deal["grader"] = grader_result
        deal["quality_score"] = grader_result.get("quality_score") if grader_result else None

        # Stage 5: DOCX
        deal["status"] = "partner_review" if deal["memo_ready"] else "needs_manual_review"
        try:
            from step5_format_memo import generate_memo_docx
            full_output = {
                "deal_id": deal_id, "deal_name": submission.name,
                "fund": submission.fund, "ic_memo_sections": memo_sections,
                "financial_model": model_result, "grader_result": grader_result,
            }
            docx_path = generate_memo_docx(full_output)
            deal["docx_path"] = str(docx_path)
        except Exception as e:
            deal["docx_error"] = str(e)

        # Save JSON output
        out = ROOT_DIR / "outputs" / f"{deal_id}_result.json"
        out.parent.mkdir(exist_ok=True)
        with open(out, "w") as f:
            json.dump({k: v for k, v in deal.items() if isinstance(v, (str, int, float, bool, dict, list, type(None)))}, f, indent=2, default=str)

    except Exception as e:
        deal["status"] = "error"
        deal["error"] = str(e)
    finally:
        AGENT_STATUS["orchestrator"]["status"] = "idle"
        AGENT_STATUS["orchestrator"]["current_deal"] = None

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/")
async def serve_ui():
    return FileResponse(str(WEB_DIR / "static" / "index.html"))

@app.get("/api/deals")
async def list_deals():
    return JSONResponse([
        {k: v for k, v in d.items() if k not in ("memo_sections", "dd_result", "model_result")}
        for d in DEALS.values()
    ])

@app.post("/api/deals")
async def submit_deal(submission: DealSubmission, background_tasks: BackgroundTasks):
    deal_id = f"DC{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
    DEALS[deal_id] = {
        "deal_id": deal_id,
        "name": submission.name,
        "fund": submission.fund,
        "sector": submission.sector,
        "ticket_cr": submission.ticket_cr,
        "stake_pct": submission.stake_pct,
        "entry_ev_cr": submission.entry_ev_cr,
        "deal_lead": submission.deal_lead,
        "brief": submission.brief,
        "status": "queued",
        "quality_score": None,
        "irr_base": None,
        "moic": None,
        "memo_ready": False,
        "memo_sections": {},
        "grader": None,
        "submitted_at": datetime.datetime.now().isoformat(),
        "pipeline_stages": {
            "screening": {"status": "pending", "started_at": None, "completed_at": None, "duration_s": None, "msg": ""},
            "modelling": {"status": "pending", "started_at": None, "completed_at": None, "duration_s": None, "msg": ""},
            "memo":      {"status": "pending", "started_at": None, "completed_at": None, "duration_s": None, "msg": ""},
            "grading":   {"status": "pending", "started_at": None, "completed_at": None, "duration_s": None, "msg": ""},
        },
    }
    background_tasks.add_task(run_pipeline_background, deal_id, submission)
    return JSONResponse({"deal_id": deal_id, "status": "pipeline_started"})

@app.get("/api/deals/{deal_id}")
async def get_deal(deal_id: str):
    if deal_id not in DEALS:
        raise HTTPException(404, "Deal not found")
    d = DEALS[deal_id]
    return JSONResponse({k: v for k, v in d.items() if k not in ("dd_result", "model_result")})

@app.get("/api/deals/{deal_id}/memo")
async def get_memo(deal_id: str):
    if deal_id not in DEALS:
        raise HTTPException(404, "Deal not found")
    d = DEALS[deal_id]
    return JSONResponse({
        "deal_id": deal_id,
        "name": d["name"],
        "fund": d["fund"],
        "memo_ready": d.get("memo_ready", False),
        "quality_score": d.get("quality_score"),
        "memo_sections": d.get("memo_sections", {}),
        "grader": d.get("grader", {}),
        "irr_base": d.get("irr_base"),
        "moic": d.get("moic"),
    })

@app.get("/api/deals/{deal_id}/memo/download")
async def download_memo(deal_id: str):
    if deal_id not in DEALS:
        raise HTTPException(404, "Deal not found")
    d = DEALS[deal_id]
    docx_path = d.get("docx_path")
    if not docx_path or not Path(docx_path).exists():
        # Try finding it in outputs
        name = d["name"].replace(" ", "_")
        candidate = ROOT_DIR / "outputs" / f"{deal_id}_IC_Memo.docx"
        if candidate.exists():
            docx_path = str(candidate)
        else:
            raise HTTPException(404, "DOCX not yet generated — wait for pipeline to complete")
    return FileResponse(docx_path, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        filename=f"IC_Memo_{d['name'].replace(' ','_')}.docx")

@app.get("/api/agents")
async def get_agents():
    return JSONResponse(AGENT_STATUS)

@app.get("/api/activity")
async def get_activity():
    return JSONResponse(list(reversed(ACTIVITY_LOG[-10:])))

@app.post("/api/activity")
async def add_activity(event: ActivityEvent):
    ACTIVITY_LOG.append({**event.dict(), "ts": time.time()})
    return JSONResponse({"ok": True})

@app.get("/api/system")
async def system_health():
    api_key = os.getenv("ANTHROPIC_API_KEY", "")
    skills_ok = (ROOT_DIR / "skills" / "skill_fund_mandate.txt").exists()
    mcp_ok = (ROOT_DIR / "mcp_servers" / "mcp_dealcloud.py").exists()
    outputs = list((ROOT_DIR / "outputs").glob("*.json")) if (ROOT_DIR / "outputs").exists() else []
    return JSONResponse({
        "api_key_set": bool(api_key) and api_key != "YOUR_API_KEY_HERE",
        "api_key_preview": f"{api_key[:12]}...{api_key[-4:]}" if len(api_key) > 16 else "not set",
        "skills_ready": skills_ok,
        "mcp_ready": mcp_ok,
        "zdr_note": "Enable ZDR at console.anthropic.com/settings",
        "data_residency": "Local — configure Azure Central India for production",
        "deals_in_memory": len(DEALS),
        "output_files": len(outputs),
        "model_orchestrator": "claude-opus-4-6",
        "model_subagent": "claude-sonnet-4-6",
    })

@app.get("/api/outputs")
async def list_outputs():
    out_dir = ROOT_DIR / "outputs"
    if not out_dir.exists():
        return JSONResponse([])
    files = []
    for f in sorted(out_dir.iterdir()):
        files.append({"name": f.name, "size_kb": round(f.stat().st_size / 1024, 1),
                      "modified": datetime.datetime.fromtimestamp(f.stat().st_mtime).isoformat()})
    return JSONResponse(files)

# ── Start server ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"\n{'='*50}")
    print(f"  NIIFL AI Engine — Web Server")
    print(f"  Open: http://localhost:{port}")
    print(f"  API docs: http://localhost:{port}/docs")
    print(f"{'='*50}\n")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True, app_dir=str(WEB_DIR))
