# NIIFL AI Engine — Claude Code Instructions

## What this project is
A FastAPI web application that exposes NIIFL's AI pipeline agents through a browser UI.
Investment team members open the web app in their browser to submit deals, run agents,
review IC memos, and monitor agent status — no terminal knowledge needed.

## Project structure
```
niifl_ai/
├── CLAUDE.md                  ← You are here. Read this first.
├── config/config.py           ← Central config: models, funds, paths
├── skills/                    ← NIIFL domain knowledge packs (built by step1)
├── mcp_servers/               ← Data connectors (built by step2)
├── outputs/                   ← Deal JSON + IC Memo DOCX output here
├── web/
│   ├── main.py                ← FastAPI backend (START HERE to run the server)
│   ├── static/
│   │   └── index.html         ← Frontend UI (served by FastAPI)
├── step1_build_skills.py      ← Build skills (run first time only)
├── step2_build_mcp_servers.py ← Build MCP stubs (run first time only)
├── step3_build_agents.py      ← Agent class definitions
├── step4_build_orchestrator.py← NIIFLOrchestrator class
├── step5_format_memo.py       ← DOCX formatter
├── step6_portfolio_monitor.py ← Portfolio monitoring agent
└── step7_run_pipeline.py      ← Master runner (for CLI use)
```

## How to run the web server

### First time setup (run once):
```bash
cd niifl_ai
python3 step1_build_skills.py
python3 step2_build_mcp_servers.py
pip install fastapi uvicorn python-multipart anthropic --break-system-packages
npm install -g docx
export ANTHROPIC_API_KEY=sk-ant-...
```

### Start the web server:
```bash
cd niifl_ai
python3 web/main.py
```
Then open: http://localhost:8000

### The server runs on port 8000 by default.
If port 8000 is busy, change PORT in web/main.py to 8001 or 8080.

## API endpoints (for Claude Code to understand)
- GET  /             → serves index.html
- GET  /api/deals    → list all deals from DealCloud
- POST /api/deals    → submit new deal, starts AI pipeline async
- GET  /api/deals/{id} → get single deal + memo status
- GET  /api/deals/{id}/memo → get IC memo sections JSON
- GET  /api/deals/{id}/memo/download → download IC Memo DOCX
- GET  /api/agents   → get agent status (running/idle)
- GET  /api/system   → system health (API key, ZDR, costs)
- POST /api/pipeline/run → manually trigger pipeline for a deal_id
- GET  /api/outputs  → list files in outputs/

## Environment variables needed
```
ANTHROPIC_API_KEY=sk-ant-api03-...     (required)
SLACK_WEBHOOK_URL=https://hooks.slack.com/...  (optional, for notifications)
PORT=8000                               (optional, default 8000)
```

## Common tasks for Claude Code

### "Run the server"
```bash
cd niifl_ai && python3 web/main.py
```

### "The server crashed, fix it"
Read web/main.py, identify the error, fix it, restart.

### "Add a new field to the deal submission form"
1. Add field to web/static/index.html form
2. Add field to /api/deals POST handler in web/main.py
3. Pass field into NIIFLOrchestrator.run_deal() call

### "Connect to real DealCloud API"
Edit mcp_servers/mcp_dealcloud.py — replace stub functions with
real HTTP calls to https://dealcloud.com/api/v1 using the API key
stored in environment variable DEALCLOUD_API_KEY.

### "The IC memo download isn't working"
Check: does outputs/{deal_id}_IC_Memo.docx exist?
If not, run step5_format_memo.py on the deal's JSON file.
If yes, check the /api/deals/{id}/memo/download route in web/main.py.

### "Add authentication / login"
Install: pip install python-jose passlib[bcrypt]
Add OAuth2 password flow to web/main.py using FastAPI's built-in security.
For Azure AD SSO: use msal library.

## Important notes
- ANTHROPIC_API_KEY must be set before starting the server
- skills/ must exist (run step1 first) — agents load skills at startup
- mcp_servers/ must exist (run step2 first)
- outputs/ is created automatically
- The pipeline runs asynchronously — deal status updates via /api/deals/{id}
- All deal data stays local; ZDR means Anthropic doesn't store API call data
