"""
STEP 7 — Master Runner (Run Everything End-to-End)
====================================================
Executes all steps in sequence for a given deal.
This is the single entry point for the full NIIFL AI engine.

Usage:
    python3 step7_run_pipeline.py

Steps executed:
    1. Build skills
    2. Validate MCP servers
    3. Run orchestrator (deal sourcing → DD → modelling → IC memo → QA)
    4. Format IC memo as DOCX
    5. Print audit summary

Set ANTHROPIC_API_KEY in environment before running:
    export ANTHROPIC_API_KEY=sk-ant-...
"""

import os, sys, json, subprocess, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "config"))
from config import ANTHROPIC_API_KEY, OUTPUTS_DIR

def banner(msg):
    print(f"\n{'='*60}")
    print(f"  {msg}")
    print(f"{'='*60}")

def check_api_key():
    if ANTHROPIC_API_KEY == "YOUR_API_KEY_HERE" or not ANTHROPIC_API_KEY:
        print("\nERROR: Set your Anthropic API key first:")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)
    print(f"  API key: {ANTHROPIC_API_KEY[:12]}...{ANTHROPIC_API_KEY[-4:]}")

# ─────────────────────────────────────────────────────────────────────────────
# Main pipeline
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    start = datetime.datetime.now()

    banner("NIIFL AI Engine — Full Pipeline")
    print(f"  Started: {start.strftime('%Y-%m-%d %H:%M:%S')}")
    check_api_key()

    # Step 1 — Skills
    banner("Step 1/5 — Building Custom Skills")
    import step1_build_skills
    print("  Skills built OK")

    # Step 2 — MCP Servers
    banner("Step 2/5 — Validating MCP Servers")
    import step2_build_mcp_servers
    print("  MCP servers validated OK")

    # Step 3 — Agents (imported by orchestrator)
    banner("Step 3/5 — Loading Agents")
    from step3_build_agents import (DealSourcingAgent, DDResearchAgent,
                                     FinancialModellingAgent, ICMemoDraftingAgent,
                                     OutcomesGraderAgent)
    print("  All 5 agent classes loaded OK")

    # Step 4 — Orchestrator
    banner("Step 4/5 — Running Orchestrator")
    from step4_build_orchestrator import NIIFLOrchestrator

    orchestrator = NIIFLOrchestrator()
    result = orchestrator.run_deal(
        deal_name="Greenway Highways Limited",
        deal_brief="""
        Greenway Highways Limited (GHL) operates a 280 km 4-lane tolled highway on NH-48
        (Bengaluru–Chennai corridor) under a 30-year NHAI concession signed in 2012.
        FY2024 revenue: INR 142 Cr. EBITDA margin: 88%. Traffic CAGR: 7.8% (5-year).
        NIIFL is being offered a 49% equity stake from the current PE sponsor (exit after 8 years).
        Proposed entry EV: INR 4,200 Cr (EV/EBITDA 14.2x). Ticket: INR 800 Cr.
        Asset has no construction risk. NHAI step-in rights intact. 22 years concession remaining.
        Japan technology partner (Nippon Expressway) involved for traffic management systems.
        """,
        financials={
            "revenue_cr": {"FY22": 118, "FY23": 128, "FY24": 142},
            "ebitda_cr":  {"FY22": 102, "FY23": 112, "FY24": 125},
            "pat_cr":     {"FY22": 28,  "FY23": 35,  "FY24": 42},
            "debt_cr":    {"FY24": 1800},
            "net_worth_cr": {"FY24": 620},
        },
        deal_terms={
            "sector": "roads",
            "ticket_cr": 800,
            "stake_pct": 49,
            "entry_ev_cr": 4200,
            "entry_ev_ebitda": 14.2,
            "concession_remaining_yrs": 22,
            "investment_mode": "secondary",
            "board_seats": 2,
        },
    )

    # Save deal output path for next step
    deal_id   = result.get("deal_id", "DEAL")
    deal_name = result.get("deal_name", "Deal").replace(" ", "_")
    json_path = os.path.join(OUTPUTS_DIR, f"{deal_id}_{deal_name}.json")

    # Step 5 — DOCX
    banner("Step 5/5 — Formatting IC Memo as DOCX")
    from step5_format_memo import generate_memo_docx
    try:
        docx_path = generate_memo_docx(result)
        # Copy to outputs for download
        import shutil
        shutil.copy(docx_path, "/mnt/user-data/outputs/NIIFL_IC_Memo_Greenway.docx")
        print(f"  DOCX ready: {docx_path}")
    except Exception as e:
        print(f"  DOCX generation error: {e}")
        docx_path = None

    # ── Final Summary ────────────────────────────────────────────────────────
    elapsed = (datetime.datetime.now() - start).seconds

    banner("Pipeline Complete — Summary")
    print(f"  Deal:          {result.get('deal_name')}")
    print(f"  Fund:          {result.get('fund')}")
    print(f"  Status:        {result.get('status')}")
    print(f"  Quality score: {result.get('quality_score')}/100")
    print(f"  Audit entries: {len(result.get('audit_log', []))}")
    print(f"  JSON output:   {json_path}")
    print(f"  DOCX output:   {docx_path or 'N/A'}")
    print(f"  Total time:    {elapsed}s")
    print(f"\n  Next step: Open the DOCX, review as the deal partner,")
    print(f"  then schedule for Preliminary IC.")
