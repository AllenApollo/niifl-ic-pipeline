# NIIFL AI Engine — Demo Day Script
## Option B Hybrid · 20 minutes · IC / Leadership audience

---

## Before you walk in (checklist)

- [ ] `python3 demo/demo_runner.py` is running
- [ ] `http://localhost:8000` is open in Chrome, full-screen
- [ ] Greenway Highways shows as "Partner review" in pipeline
- [ ] DOCX download works for Greenway (click Download DOCX to test)
- [ ] Sunrise Port Terminal brief is copied to clipboard (see below)
- [ ] Laptop plugged in, notifications off, screensaver disabled
- [ ] Fallback: offline HTML demo on USB if wifi fails

---

## Sunrise Port Terminal brief — COPY THIS before the demo

```
Company: Sunrise Port Terminal Ltd
Fund: NIIF Master Fund | Sector: Ports
Ticket: 900 Cr | Stake: 74% | Entry EV: 5,400 Cr

Brief: Sunrise Port Terminal operates Container Terminal 3 at JNPT
under a 30-year concession, 18 years remaining. FY24 revenue INR 380 Cr,
EBITDA margin 62%, throughput 1.2M TEUs, 9% CAGR. NIIFL acquires 74%
at EV INR 5,400 Cr (14.2x EV/EBITDA). Fully operational, no construction
risk. TAMP-regulated tariffs, annual escalation. Only private container
terminal in Mumbai port cluster. Confirmed NIP-PT-2024-0447.
Revenue FY22: 312 | FY23: 348 | FY24: 380
EBITDA FY22: 187 | FY23: 212 | FY24: 236
Net debt: 1800 | Net worth: 740
```

---

## 00:00 — Opening (2 minutes)

**Say:** "NIIFL's investment team spends 20 to 40 hours per deal
preparing for the Investment Committee — sourcing research, building
financial models, drafting the memo. We've built an AI engine on
Anthropic's Claude that brings that to under 2 hours.

It's not a chatbot. It's five specialised Claude agents — each with
a specific job — orchestrated by a Claude Opus instance that manages
the entire deal workflow. Let me show you what it produces."

**Do:** [Open http://localhost:8000 — Pipeline view is visible]

---

## 02:00 — Show the output first (4 minutes)

**Say:** "This is Greenway Highways Limited. 280 km NHAI concession on
NH-48, Bengaluru–Chennai. The AI engine ran on this deal last night.
Let me show you what it produced."

**Do:** [Click Greenway Highways row → IC Memo tab opens]

**Say:** "This is the Investment Committee memo. All 8 sections —
thesis, market analysis, financial returns, risks, ESG, policy
alignment, deal structure, recommendation. AI quality score 84 out
of 100 — all sections passed the automated rubric check.

Look at Section 3 — the financial returns. Base IRR 13.2% against
a 12% Master Fund hurdle. Bull case 16.8%, bear case 10.1%.
Every number is internally consistent.

Section 5 — ESG. This isn't the company's CSR report copy-pasted.
NIIFL's own three-pillar framework — environment, ease of living,
economic growth — scored independently by the AI against our criteria."

**Do:** [Scroll to Section 8 — Recommendation]

**Say:** "And the recommendation is unambiguous. INVEST, INR 800 Cr
from the Master Fund. Authorise term sheet. Next steps listed."

**Do:** [Click Download DOCX button]

**Say:** "This downloads as a formatted Word document — ready to
circulate to the IC. The AI drafted this. A partner reviewed and
approved it. That's the workflow."

[DOCX opens — show it briefly]

---

## 06:00 — Show the agents (3 minutes)

**Do:** [Click Agents tab]

**Say:** "This is the engine room. Six Claude agents. The orchestrator
runs on Claude Opus 4.6 — our highest-capability model. The four
specialist subagents run on Sonnet 4.6 for cost efficiency.

Each agent has a specific job. The DD research agent pulls from
PitchBook, Capital IQ, MCA21 company filings, NITI Aayog's National
Infrastructure Pipeline, and CEA power generation data. All connected
via MCP — Anthropic's protocol for connecting agents to external tools.

The outcomes grader is a separate agent that QA-checks the memo
against NIIFL's rubric before any human sees it. It's what gave
Greenway the 84/100 score — and flagged one enhancement: the exit
risk section could add a secondary buyer universe.

ZDR — Zero Data Retention — is enabled. No deal data is stored by
Anthropic after the API call returns. Every agent action is logged
for our SEBI AIF audit trail."

---

## 09:00 — Submit the live deal (1 minute)

**Do:** [Click New Deal tab]

**Say:** "Let me show you this is real. I'm going to submit a new deal
right now — Sunrise Port Terminal, a container terminal at JNPT.
Watch the agents run."

**Do:** [Paste the Sunrise Port Terminal brief — fill in the fields]
[Click Run AI Pipeline]

**Say:** "The orchestrator has just delegated to four subagents
simultaneously. Screening, financial modelling, IC memo drafting,
QA grading — all running now on Claude."

---

## 10:00 — While the pipeline runs (5 minutes)

**Say:** "While that runs, let me tell you what's happening under the hood.

The deal sourcing agent has checked Sunrise Port Terminal against
the Master Fund mandate — operating asset, core infrastructure,
INR 500 Cr minimum ticket. It passed.

The DD research agent is pulling port throughput data from the
Indian Ports Association, checking MCA21 for any charges or
litigation against the company, and cross-referencing against the
NIP to confirm the project code.

The financial modelling agent is building a concession DCF —
not a generic spreadsheet but a port-specific model calibrated to
TAMP tariff structures, TEU growth benchmarks from IPA data,
and NIIFL's return thresholds.

And Claude Opus is drafting all 8 sections of the IC memo
simultaneously — pulling from everything the other agents produced.

[Pause — check if pipeline is finishing]

When it's done, the outcomes grader will check every section
against our rubric — does the ESG section score all three pillars?
Is the IRR compared to the hurdle? Is there a NIP reference?
Only if everything passes does it go to partner review."

---

## 15:00 — Show the result (2 minutes)

**Do:** [When Sunrise memo is ready — click View Memo]

**Say:** "Done. In [X] minutes. A complete IC memo for Sunrise Port
Terminal — thesis, market, returns, risks, ESG, policy alignment,
deal structure, recommendation.

In the current process, a 2-person associate team would spend
3 days on this. The AI engine does it in [X] minutes.

The partner still reviews. The IC still decides. What's changed is
the 80% of the work that was administrative — data gathering,
model-building, section drafting — is now done by the AI.
The investment team focuses on judgment, relationships, and
the IC debate that actually matters."

---

## 17:00 — Q&A (3 minutes)

**Likely questions and answers:**

Q: "How accurate is the financial model?"
A: "The model uses live data from PitchBook and Capital IQ for
comparable transactions, and India-specific benchmarks for the
sector — NHAI ATVM traffic data for roads, CEA generation data
for power. We validate every model against precedent transactions
before the partner review."

Q: "What if the IC asks a question not in the memo?"
A: "The post-IC feedback loop routes IC questions back to the
relevant agent. A financial question goes to the modelling agent.
A competitive question goes to DD research. Answers are appended
to the memo within 24 hours — before the final IC."

Q: "Is this secure? Are our deal details going to Anthropic?"
A: "Zero Data Retention is enabled — Anthropic processes the API
call and returns the response, but stores nothing. All deal data
stays on our infrastructure. For production, we deploy on
Azure Central India for data residency."

Q: "Can it do [X sector / Y fund]?"
A: "The system is configured for all four NIIFL funds — Master
Fund, SOF, IJF, and Private Markets Fund — each with its own
mandate, return thresholds, and memo template. Sector coverage
includes roads, ports, airports, energy, digital infrastructure,
healthcare, and manufacturing."

Q: "How long to deploy this for real?"
A: "The MVP — IC memo drafting for the Master Fund — can be
operational in 6–8 weeks. Full four-fund deployment with real
DealCloud and PitchBook integrations is a 4-month build."

---

## Closing line

**Say:** "The investment process at NIIFL doesn't change — the IC
still decides, partners still exercise judgment, relationships
still source deals. What changes is the 80% of the work that
was data assembly and document drafting. That's now done by
the AI, in minutes, at NIIFL's quality standard."

---

## Emergency fallback

If server crashes or API fails:
1. Open `niifl_demo_standalone.html` from USB (ask tech to build this)
2. Say: "Let me switch to our offline demo — same system, same data"
3. The standalone HTML has all the same views and data pre-loaded
