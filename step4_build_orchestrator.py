"""
STEP 4 — Build the Orchestrator
================================
The orchestrator is the Claude Opus agent that:
  1. Receives a deal brief
  2. Routes it to the correct fund via the sourcing agent
  3. Sequences DD research + financial modelling (in parallel conceptually)
  4. Triggers IC memo drafting
  5. Runs the outcomes grader
  6. Loops back if grader fails (max 2 retries)
  7. Fires Slack webhook when memo is partner-ready
  8. Writes full audit trail to DealCloud

Usage:
    python3 step4_build_orchestrator.py
    # Runs a full end-to-end workflow on a test deal

Import:
    from step4_build_orchestrator import NIIFLOrchestrator
    result = NIIFLOrchestrator().run_deal(deal_name, deal_brief, financials, deal_terms)
"""

import os, sys, json, datetime
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "config"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "mcp_servers"))

from config import (ANTHROPIC_API_KEY, ORCHESTRATOR_MODEL, FUNDS,
                    SKILLS_DIR, OUTPUTS_DIR)
from step3_build_agents import (DealSourcingAgent, DDResearchAgent,
                                 FinancialModellingAgent, ICMemoDraftingAgent,
                                 OutcomesGraderAgent)
import mcp_dealcloud as dealcloud
import anthropic

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

MAX_GRADER_RETRIES = 2

class NIIFLOrchestrator:
    """
    Claude Opus orchestrator for NIIFL's IC workflow.
    Manages the full deal lifecycle from brief to partner-ready IC memo.
    """

    def __init__(self):
        self.sourcing_agent   = DealSourcingAgent()
        self.dd_agent         = DDResearchAgent()
        self.modelling_agent  = FinancialModellingAgent()
        self.memo_agent       = ICMemoDraftingAgent()
        self.grader_agent     = OutcomesGraderAgent()
        self.run_log          = []

    def _log(self, deal_id: str, stage: str, message: str, data: dict = None):
        """Log every orchestrator action — SEBI audit trail."""
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "deal_id": deal_id,
            "stage": stage,
            "message": message,
            "data_summary": str(data)[:200] if data else None,
        }
        self.run_log.append(entry)
        dealcloud.log_agent_action(deal_id, stage, message, agent="orchestrator")
        print(f"  [{stage}] {message}")

    def _decide_fund(self, screening_result: dict) -> str:
        """Extract recommended fund from sourcing agent output."""
        fund = screening_result.get("recommended_fund", "no_fit")
        if fund not in FUNDS:
            return None
        return fund

    def _notify_slack(self, deal_name: str, deal_id: str, quality_score: int):
        """
        In production: POST to Slack webhook URL.
        Replace SLACK_WEBHOOK_URL with your actual webhook.
        """
        payload = {
            "text": (f":white_check_mark: *IC Memo Ready for Partner Review*\n"
                     f"Deal: *{deal_name}* ({deal_id})\n"
                     f"Quality Score: {quality_score}/100\n"
                     f"Action: Open DOCX in Google Drive and review before IC calendar.")
        }
        # Production: requests.post(os.getenv("SLACK_WEBHOOK_URL"), json=payload)
        print(f"  [SLACK] Webhook fired — memo ready for partner review (score: {quality_score})")
        return payload

    def run_deal(self, deal_name: str, deal_brief: str,
                 financials: dict, deal_terms: dict,
                 data_room_summary: str = "") -> dict:
        """
        Full end-to-end orchestration of one deal.
        Returns: final packaged result dict with memo, grader scores, audit log.
        """
        deal_id = f"DC{datetime.datetime.now().strftime('%Y%m%d%H%M')}"
        print(f"\n{'='*60}")
        print(f"NIIFL Orchestrator — Processing: {deal_name}")
        print(f"Deal ID: {deal_id}")
        print(f"{'='*60}")

        # ── Stage 1: Deal screening ──────────────────────────────────────────
        self._log(deal_id, "screening", f"Starting deal screening for: {deal_name}")
        screening = self.sourcing_agent.run(deal_brief)

        if screening.get("parse_error"):
            self._log(deal_id, "screening", "ERROR: Sourcing agent parse failure", screening)
            return {"status": "error", "stage": "screening", "detail": screening}

        fund = self._decide_fund(screening)
        self._log(deal_id, "screening",
                  f"Screen result: pass={screening.get('pass_screen')} fund={fund} "
                  f"score={screening.get('fit_score')}", screening)

        if not screening.get("pass_screen") or not fund:
            dealcloud.update_deal_status(
                deal_id, "rejected",
                f"Screen failed: {screening.get('reject_reason', 'No fund fit')}"
            )
            return {
                "status": "rejected",
                "deal_id": deal_id,
                "reason": screening.get("reject_reason"),
                "screening": screening,
            }

        dealcloud.create_deal(deal_name, deal_terms.get("sector", "infrastructure"),
                              fund, deal_terms.get("ticket_cr", 0), "AI-Orchestrator")
        dealcloud.update_deal_status(deal_id, "dd", "Passed AI screen — entering DD")

        # ── Stage 2: DD Research ─────────────────────────────────────────────
        self._log(deal_id, "dd_research", "Starting DD research agent")
        dd_result = self.dd_agent.run(
            deal_name=deal_name,
            deal_brief=deal_brief,
            sector=deal_terms.get("sector", "infrastructure"),
            fund=fund,
            data_room_summary=data_room_summary,
        )
        self._log(deal_id, "dd_research",
                  f"DD complete — confidence: {dd_result.get('overall_dd_confidence', 'N/A')}")

        # ── Stage 3: Financial Modelling ─────────────────────────────────────
        self._log(deal_id, "financial_modelling", "Starting financial modelling agent")
        model_result = self.modelling_agent.run(
            deal_name=deal_name,
            sector=deal_terms.get("sector", "infrastructure"),
            fund=fund,
            financials=financials,
            deal_terms=deal_terms,
        )
        self._log(deal_id, "financial_modelling",
                  f"Model complete — base IRR: {model_result.get('base_irr', 'N/A')}% "
                  f"MOIC: {model_result.get('base_moic', 'N/A')}x")

        dealcloud.update_deal_status(deal_id, "ic_prep", "DD + modelling complete")

        # ── Stage 4: IC Memo Drafting + Outcomes QA (with retry loop) ────────
        memo_draft = None
        grader_result = None
        attempt = 0

        while attempt <= MAX_GRADER_RETRIES:
            attempt += 1
            self._log(deal_id, "memo_drafting",
                      f"IC memo drafting — attempt {attempt}/{MAX_GRADER_RETRIES+1}")

            memo_draft = self.memo_agent.run(
                deal_name=deal_name,
                fund=fund,
                dd_research=dd_result,
                financial_model=model_result,
                deal_terms=deal_terms,
            )

            self._log(deal_id, "outcomes_grading", "Running outcomes grader")
            grader_result = self.grader_agent.run(memo_draft, fund)

            overall_pass = grader_result.get("overall_pass", False)
            quality_score = grader_result.get("quality_score", 0)
            gaps = grader_result.get("gaps_to_fix", [])

            self._log(deal_id, "outcomes_grading",
                      f"Grader result: pass={overall_pass} score={quality_score} "
                      f"gaps={len(gaps)}", grader_result)

            if overall_pass:
                break
            elif attempt <= MAX_GRADER_RETRIES:
                self._log(deal_id, "memo_revision",
                          f"Memo failed QA. Gaps: {gaps}. Sending back for revision.")
                # Feed gaps back into the next memo attempt via deal_terms
                deal_terms["grader_feedback"] = gaps

        # ── Stage 5: Package output + notify ─────────────────────────────────
        output_path = os.path.join(OUTPUTS_DIR, f"{deal_id}_{deal_name.replace(' ', '_')}.json")
        final_output = {
            "deal_id": deal_id,
            "deal_name": deal_name,
            "fund": fund,
            "status": "ready_for_partner_review" if grader_result.get("overall_pass") else "needs_manual_review",
            "quality_score": grader_result.get("quality_score", 0),
            "screening": screening,
            "dd_research": dd_result,
            "financial_model": model_result,
            "ic_memo_sections": memo_draft,
            "grader_result": grader_result,
            "audit_log": self.run_log,
            "generated_at": datetime.datetime.now().isoformat(),
        }

        with open(output_path, "w") as f:
            json.dump(final_output, f, indent=2)
        self._log(deal_id, "complete", f"Output saved: {output_path}")

        if grader_result.get("overall_pass"):
            self._notify_slack(deal_name, deal_id, grader_result.get("quality_score", 0))
            dealcloud.update_deal_status(deal_id, "partner_review",
                                         "IC memo passed QA — awaiting partner review")
        else:
            self._log(deal_id, "complete",
                      "Memo did not pass QA after retries — flagged for manual review")

        print(f"\n{'='*60}")
        print(f"Orchestration complete for: {deal_name}")
        print(f"Status: {final_output['status']}")
        print(f"Quality Score: {final_output['quality_score']}/100")
        print(f"Output: {output_path}")
        print(f"{'='*60}")

        return final_output


# ─────────────────────────────────────────────────────────────────────────────
# Test run
# ─────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    orchestrator = NIIFLOrchestrator()

    TEST_DEAL_BRIEF = """
    Greenway Highways Limited (GHL) operates a 280 km 4-lane tolled highway on NH-48
    (Bengaluru–Chennai corridor) under a 30-year NHAI concession signed in 2012.
    FY2024 revenue: INR 142 Cr. EBITDA margin: 88%. Traffic CAGR: 7.8% (5-year).
    NIIFL is being offered a 49% equity stake from the current PE sponsor (exit after 8 years).
    Proposed entry EV: INR 4,200 Cr (EV/EBITDA: 14.2x). Ticket size: INR 800 Cr.
    Asset has no construction risk. NHAI step-in rights intact. 22 years concession remaining.
    """

    TEST_FINANCIALS = {
        "revenue_cr": {"FY22": 118, "FY23": 128, "FY24": 142},
        "ebitda_cr":  {"FY22": 102, "FY23": 112, "FY24": 125},
        "pat_cr":     {"FY22": 28,  "FY23": 35,  "FY24": 42},
        "debt_cr":    {"FY24": 1800},
        "net_worth_cr": {"FY24": 620},
    }

    TEST_DEAL_TERMS = {
        "sector": "roads",
        "ticket_cr": 800,
        "stake_pct": 49,
        "entry_ev_cr": 4200,
        "entry_ev_ebitda": 14.2,
        "concession_remaining_yrs": 22,
        "investment_mode": "secondary",
        "board_seats": 2,
    }

    result = orchestrator.run_deal(
        deal_name="Greenway Highways Limited",
        deal_brief=TEST_DEAL_BRIEF,
        financials=TEST_FINANCIALS,
        deal_terms=TEST_DEAL_TERMS,
    )

    print(f"\nFinal status: {result['status']}")
    print(f"Output file: {OUTPUTS_DIR}/")
