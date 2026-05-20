# NIIFL AI Engine — Step-by-Step Build Guide

## What This Is
A complete Claude-native AI engine for NIIFL's Investment Committee workflows.
Built entirely on Anthropic's Claude API, Agent SDK, and MCP protocol.

---

## Prerequisites

```bash
# Python 3.10+
pip install anthropic python-dotenv

# Node.js 18+ (for DOCX generation)
npm install -g docx

# Set your Anthropic API key
export ANTHROPIC_API_KEY=sk-ant-api03-...
```

---

## Project Structure

```
niifl_ai/
├── config/
│   └── config.py               # Central config: models, fund definitions, paths
├── skills/                     # Built by Step 1 — NIIFL domain knowledge packs
│   ├── skill_fund_mandate.txt
│   ├── skill_ic_memo_template.txt
│   ├── skill_india_infra.txt
│   ├── skill_esg_impact.txt
│   └── skill_outcomes_rubric.txt
├── mcp_servers/                # Built by Step 2 — data connectors
│   ├── mcp_dealcloud.py        # CRM read/write + audit log
│   ├── mcp_market_data.py      # PitchBook + Capital IQ
│   └── mcp_india_gov.py        # NITI Aayog NIP, MCA21, CEA, NHAI
├── outputs/                    # Deal JSON + IC Memo DOCX output here
├── step1_build_skills.py       # Build all 5 custom skills
├── step2_build_mcp_servers.py  # Build + validate 3 MCP servers
├── step3_build_agents.py       # Define all 5 Claude agents
├── step4_build_orchestrator.py # Claude Opus orchestrator
├── step5_format_memo.py        # JSON memo → DOCX
├── step6_portfolio_monitor.py  # Post-investment monitoring agent
└── step7_run_pipeline.py       # MASTER RUNNER — runs everything end-to-end
```

---

## Step-by-Step Execution

### Step 1 — Build Custom Skills
```bash
python3 step1_build_skills.py
```
Creates 5 skill files in `skills/`:
- `skill_fund_mandate.txt` — NIIFL's 4 fund mandates, return hurdles, exclusions
- `skill_ic_memo_template.txt` — 8-section IC memo template per fund
- `skill_india_infra.txt` — India infra financial modelling frameworks (roads, ports, power)
- `skill_esg_impact.txt` — NIIFL's 3-pillar ESG framework + LP reporting requirements
- `skill_outcomes_rubric.txt` — Pass/fail criteria for IC memo QA grader

---

### Step 2 — Build MCP Servers
```bash
python3 step2_build_mcp_servers.py
```
Creates 3 MCP server modules in `mcp_servers/`:
- `mcp_dealcloud.py` — DealCloud CRM: search, create, update deals, audit log
- `mcp_market_data.py` — PitchBook + Capital IQ: deal comps, public comps, benchmarks
- `mcp_india_gov.py` — NITI Aayog NIP, MCA21 filings, CEA power data, NHAI traffic

**Production note:** Each server is currently a stub.
Replace the stub functions with real API calls:
- DealCloud: `https://dealcloud.com/api/v1`
- PitchBook: `https://api.pitchbook.com`
- MCA21: `https://api.mca.gov.in`

---

### Step 3 — Understand the Agents
```bash
python3 step3_build_agents.py   # runs smoke test on DealSourcingAgent
```
Defines 5 Claude agent classes. Each has a `run()` method returning typed JSON:

| Agent | Model | Job |
|-------|-------|-----|
| `DealSourcingAgent` | Sonnet | Screen deal against fund mandates, score fit |
| `DDResearchAgent` | Sonnet | Market, competitive, regulatory, ESG DD |
| `FinancialModellingAgent` | Sonnet | Concession DCF / growth equity model, IRR, MOIC |
| `ICMemoDraftingAgent` | **Opus** | Draft all 8 IC memo sections from DD + model |
| `OutcomesGraderAgent` | Sonnet | QA every section against NIIFL rubric, pass/fail |

---

### Step 4 — Run the Orchestrator
```bash
python3 step4_build_orchestrator.py
```
`NIIFLOrchestrator.run_deal()` executes the full deal lifecycle:
1. Screen → fund routing → reject if no fit
2. DD research (DDResearchAgent)
3. Financial modelling (FinancialModellingAgent)
4. IC memo draft → outcomes QA → retry loop (max 2x) (ICMemoDraftingAgent + OutcomesGraderAgent)
5. Save JSON output to `outputs/`
6. Fire Slack webhook (configure `SLACK_WEBHOOK_URL` env var)
7. Full audit log written to DealCloud

Output: `outputs/<deal_id>_<deal_name>.json`

---

### Step 5 — Format IC Memo as DOCX
```bash
python3 step5_format_memo.py outputs/<deal_id>_<deal_name>.json
```
Converts JSON memo sections into a formatted Word document with:
- Cover page (Confidential, fund name, quality score)
- All 8 sections with professional formatting
- Returns summary table (base/bull/bear IRR)
- AI QA summary appendix

Output: `outputs/<deal_id>_IC_Memo.docx`

---

### Step 6 — Portfolio Monitoring (Post-Investment)
```bash
python3 step6_portfolio_monitor.py
```
After investment, `PortfolioMonitoringAgent` quarterly:
- Compares actual KPIs vs IC memo projections
- Flags >15% variance as RED
- Assesses exit readiness
- Drafts board pack talking points

---

### Step 7 — Run Everything at Once
```bash
python3 step7_run_pipeline.py
```
Runs Steps 1–5 end-to-end on a test deal (Greenway Highways Limited).

---

## Configuration

Edit `config/config.py` to customise:
- `ORCHESTRATOR_MODEL` / `SUBAGENT_MODEL` — Claude model versions
- `FUNDS` dict — return hurdles, ticket sizes, sector lists per fund
- `ESG_PILLARS` — NIIFL's three-pillar ESG framework
- `POLICY_FRAMEWORKS` — India policy schemes to check alignment against

---

## Production Deployment Checklist

- [ ] Replace stub MCP functions with real API calls (DealCloud, PitchBook, MCA21)
- [ ] Set `SLACK_WEBHOOK_URL` env var for deal team notifications
- [ ] Set `ANTHROPIC_API_KEY` with ZDR (Zero Data Retention) enabled account
- [ ] Upload `skills/*.txt` files as Claude Agent Skills via Anthropic Console
- [ ] Connect Google Drive MCP for data room document access
- [ ] Populate RAG index with past NIIFL IC memos (vector embeddings)
- [ ] Deploy MCP servers as FastMCP HTTP servers on India-region cloud
- [ ] Configure DealCloud API credentials
- [ ] Configure PitchBook + Capital IQ API credentials
- [ ] Set up audit log export to SEBI-compliant storage (90-day retention)
- [ ] Test with a real deal before enabling for investment team

---

## Security Notes

- Never commit `ANTHROPIC_API_KEY` to git — use environment variables or secrets manager
- Enable Zero Data Retention on your Anthropic API account for deal confidentiality
- All deal data should be processed in India-region infrastructure
- DOCX output contains confidential deal information — treat as SEBI Category II AIF material

---

## Support

Built on:
- Anthropic Claude API: https://docs.anthropic.com
- Anthropic Agent SDK: https://github.com/anthropics/claude-agent-sdk-python
- MCP Protocol: https://modelcontextprotocol.io
- docx npm package: https://docx.js.org
