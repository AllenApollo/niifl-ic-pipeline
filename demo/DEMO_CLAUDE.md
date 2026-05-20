# NIIFL AI Engine — Demo Build (Option B Hybrid)
# Claude Code reads this file first every session

## What this demo is
Option B hybrid demo:
- Pre-run deal (Greenway Highways) loaded and polished — appears instantly
- Live pipeline triggered for second deal (Sunrise Port Terminal) during demo
- Everything runs on Claude Agents (Opus 4.6 orchestrator + Sonnet 4.6 subagents)
- Single command to start — no setup steps needed on demo day

## Demo day — ONE command to run everything:
```bash
cd niifl_ai
python3 demo/demo_runner.py
```
Then open: http://localhost:8000
That's it. Server starts, pre-loaded deal is ready, live pipeline available.

## Files in this demo build
```
niifl_ai/
├── demo/
│   ├── demo_runner.py        ← START HERE — runs everything
│   ├── demo_data.py          ← Pre-polished Greenway Highways deal data
│   ├── demo_agent.py         ← Streamlined Claude agent for live demo call
│   └── DEMO_SCRIPT.md        ← 20-min presenter script with talking points
├── web/
│   ├── main.py               ← FastAPI backend (used by demo_runner)
│   └── static/
│       └── index.html        ← Frontend UI
├── skills/                   ← NIIFL knowledge packs
├── config/config.py          ← Fund definitions
```

## What Claude Code should do if asked

### "Start the demo server"
```bash
cd niifl_ai && python3 demo/demo_runner.py
```

### "The server crashed"
Read the error, fix it in the relevant file, restart with demo/demo_runner.py

### "Polish the Greenway memo — section X looks weak"
Edit demo/demo_data.py → find the memo_sections dict → update the relevant section text

### "The live demo deal isn't producing a good memo"
Edit demo/demo_agent.py → update the DEMO_SYSTEM_PROMPT with more specific NIIFL context

### "Add a third pre-loaded deal to the pipeline"
Edit demo/demo_data.py → add new entry to DEMO_DEALS dict following the same pattern

### "Change the demo deal from Sunrise Port to something else"
Edit demo/demo_data.py → update LIVE_DEMO_BRIEF with new deal details

### "The DOCX download isn't working"
Run: python3 demo/demo_runner.py --pregenerate-docx
This pre-generates the DOCX before the demo starts.

## Environment needed
```
ANTHROPIC_API_KEY=sk-ant-api03-...   (required for live agent call)
PORT=8000                             (optional)
```

## Demo script location
See demo/DEMO_SCRIPT.md for full 20-minute presenter script with talking points.
```
