"""
NIIFL Demo Data
================
Pre-polished deal data seeded into the server at startup.
This is what appears instantly when the demo opens —
no waiting, no API calls needed for the pre-loaded deals.

To update memo sections: edit the memo_sections dict below.
To add a new pre-loaded deal: copy the DEALS["DC001"] pattern.
"""

# ── Pre-written demo deal brief for the LIVE pipeline submission ──────────────
# Paste this into the New Deal form during the demo
LIVE_DEMO_BRIEF = {
    "name": "Sunrise Port Terminal Ltd",
    "fund": "master_fund",
    "sector": "ports",
    "ticket_cr": 900,
    "stake_pct": 74,
    "entry_ev_cr": 5400,
    "deal_lead": "Priya Nair",
    "brief": """Sunrise Port Terminal Ltd (SPTL) operates Container Terminal 3 at
Jawaharlal Nehru Port Trust (JNPT) under a 30-year concession signed
in 2009, with 18 years remaining. FY2024 revenue INR 380 Cr, EBITDA
margin 62%, throughput 1.2 million TEUs growing at 9% CAGR over 5 years.
NIIFL is acquiring 74% equity from the promoter group at an EV of
INR 5,400 Cr (EV/EBITDA 14.2x FY24). No construction risk — fully
operational. TAMP-regulated tariffs with annual escalation. Strategic
position: only private container terminal in the Mumbai port cluster.
Government of Maharashtra has committed to road and rail connectivity
upgrades in the hinterland. Confirmed in National Infrastructure Pipeline
(NIP-PT-2024-0447). Potential for adjacent terminal expansion (CT4)
under NMP. No material litigation; all environmental clearances in place.""",
    "revenue_fy22": 312,
    "revenue_fy23": 348,
    "revenue_fy24": 380,
    "ebitda_fy22": 187,
    "ebitda_fy23": 212,
    "ebitda_fy24": 236,
    "net_debt_fy24": 1800,
    "net_worth_fy24": 740,
}

# ── Pre-loaded demo deals (appear instantly in pipeline on server start) ───────
DEMO_DEALS = {

    "DC001": {
        "deal_id": "DC001",
        "name": "Greenway Highways Ltd",
        "sector": "roads",
        "fund": "master_fund",
        "ticket_cr": 800,
        "stake_pct": 49,
        "entry_ev_cr": 4200,
        "entry_ev_ebitda": 14.2,
        "deal_lead": "Rajiv Sharma",
        "status": "partner_review",
        "quality_score": 84,
        "irr_base": 13.2,
        "irr_bull": 16.8,
        "irr_bear": 10.1,
        "irr_net": 11.4,
        "moic": 2.1,
        "submitted_at": "2026-05-05T09:14:00",
        "memo_ready": True,
        "docx_ready": True,
        "brief": "280km NH-48 tolled highway under 30-year NHAI concession, 22 years remaining.",

        "memo_sections": {
            "thesis": (
                "Greenway Highways Limited (GHL) offers NIIFL's Master Fund a "
                "compelling entry into India's tolled road infrastructure — an "
                "operational 280 km 4-lane highway on the NH-48 Bengaluru–Chennai "
                "corridor with 22 years of concession remaining. The investment thesis "
                "rests on three pillars: (i) resilient, inflation-hedged toll revenue "
                "with a 7.8% traffic CAGR over five years, backed by WPI-linked annual "
                "tariff escalation; (ii) regulatory certainty under NHAI's established "
                "concession framework with full step-in rights and zero construction "
                "risk; and (iii) a clear exit path via a strategic infrastructure buyer "
                "or InvIT listing at EV/EBITDA 16–18x in years 7–10. NIIFL's 49% "
                "secondary acquisition at INR 800 Cr (EV INR 4,200 Cr; 14.2x FY24 "
                "EBITDA) represents an attractive entry relative to the precedent "
                "transaction average of 14.8x for operational NHAI concessions. Value "
                "creation will be driven by FASTAG adoption driving collection "
                "efficiency from 94% to 98%, active traffic management to capture "
                "the projected NH-48 corridor volume growth, and a potential toll "
                "plaza modernisation programme."
            ),
            "market_analysis": (
                "The NH-48 Bengaluru–Chennai corridor is one of India's highest-density "
                "national highways, connecting two of South India's largest commercial "
                "and industrial centres. MoRTH ATVM data confirms daily PCU of 28,400 "
                "with consistent growth across all vehicle categories; LCV and multi-axle "
                "vehicles together represent 61% of traffic, providing high per-vehicle "
                "toll revenue. The competitive landscape is limited: GHL holds the only "
                "tolled concession on this 280 km stretch, with no viable parallel route. "
                "NHAI's concession framework provides regulatory certainty — tariffs are "
                "set by NHAI, escalated annually at WPI, and the authority has a strong "
                "track record of honouring concession terms. India's National "
                "Infrastructure Pipeline allocates INR 19 lakh crore to road sector "
                "investment through FY30, underpinning long-term traffic demand. "
                "PM GatiShakti designates the Bengaluru–Chennai corridor as a priority "
                "multimodal logistics spine, with dedicated freight rail running parallel "
                "expected to reduce competing road freight traffic for bulk commodities "
                "while increasing passenger and LCV volumes."
            ),
            "financial_returns": (
                "Base case gross IRR of 13.2% (exceeds the 12.0% Master Fund hurdle "
                "by 120 bps) and 2.1x MOIC over a 7-year hold to exit. Bull case "
                "assumptions — traffic growth +15% above base and toll escalation at "
                "6.0% — deliver 16.8% IRR and 2.6x MOIC. Bear case — traffic flat to "
                "base and escalation capped at 3.5% — returns 10.1% IRR and 1.7x MOIC, "
                "still returning capital above cost. Net IRR (after 2% p.a. management "
                "fee and 20% carried interest) is estimated at 11.4% in the base case. "
                "Entry valuation of 14.2x FY24 EV/EBITDA is benchmarked against five "
                "precedent NHAI toll transactions averaging 14.8x; the 40 bps discount "
                "reflects a secondary purchase from a PE seller seeking a clean exit. "
                "Exit assumption of 16.0x reflects the natural re-rating of operating "
                "assets as concession risk diminishes. Key sensitivity: every 5% traffic "
                "underperformance reduces base IRR by approximately 90 bps; even a 20% "
                "sustained shortfall keeps the asset above the cost of equity."
            ),
            "risks_mitigants": (
                "Traffic risk (MEDIUM): NH-48 serves diverse traffic — passenger, LCV, "
                "and multi-axle — reducing single-category exposure. NHAI independent "
                "traffic study (2024) projects 7.2% CAGR through FY35 even in the "
                "downside scenario. Mitigant: bear case modelled at flat traffic growth. "
                "Residual risk: LOW.\n\n"
                "Regulatory / tariff risk (LOW): NHAI's tariff escalation mechanism is "
                "WPI-linked and contractually embedded. No tariff freeze has been "
                "imposed on this concession in its 14-year history. Mitigant: "
                "concession agreement reviewed by external legal counsel — no "
                "ambiguity in escalation clause. Residual risk: LOW.\n\n"
                "Operational / O&M risk (LOW): GHL has operated the highway since 2012 "
                "with no major outage. O&M contract with Ashoka Buildcon — India's "
                "largest toll operator — with performance penalties. Residual: LOW.\n\n"
                "Exit risk (MEDIUM): InvIT / strategic buyer market has deepened "
                "significantly since 2022 (IRB InvIT, NHAI InvIT, Highway Infrastructure "
                "Trust). Comparable assets have traded in the 16–18x range. Primary "
                "risk is a broad market dislocation. Mitigant: 7-year hold provides "
                "multiple exit windows. Residual: MEDIUM."
            ),
            "esg_impact": (
                "ESG overall score: 74/100 (exceeds NIIFL threshold of 50).\n\n"
                "Environment (3.8/5): GHL has committed to 100% renewable energy for "
                "all toll plazas and administrative offices by FY26 — currently at 68%. "
                "Solar canopy installed at Krishnagiri and Vellore plazas (combined "
                "620 kWp). No adverse environmental court orders; Forest Conservation "
                "Act compliance confirmed. Scope 1 emissions from O&M fleet: 1,840 "
                "tCO2e/year — reduction roadmap to 2030 submitted to NIIFL.\n\n"
                "Ease of Living (4.2/5): NH-48 reduces Bengaluru–Chennai travel time "
                "by 2.1 hours, serving 6 districts with limited alternative "
                "connectivity options. Highway ambulance service (3 vehicles) covers "
                "the full 280 km stretch — 1,240 emergency responses in FY24.\n\n"
                "Economic Growth (4.0/5): 1,240 direct FTEs employed; estimated "
                "3,800 indirect jobs in roadside economy. Annual GST contribution: "
                "INR 18 Cr. Logistics cost reduction along corridor: INR 340 Cr/year "
                "for freight users.\n\n"
                "SDG alignment: SDG 9 (Industry, Innovation and Infrastructure), "
                "SDG 11 (Sustainable Cities and Communities), SDG 8 (Decent Work).\n\n"
                "NIP alignment: confirmed, project code NIP-RD-2024-1823. PM GatiShakti "
                "multimodal node designation in progress."
            ),
            "policy_alignment": (
                "National Infrastructure Pipeline (NIP): GHL's concession is confirmed "
                "in the NIP under project code NIP-RD-2024-1823. The NH-48 corridor "
                "is classified as a priority national corridor under MoRTH's Bharatmala "
                "Phase I programme.\n\n"
                "PM GatiShakti: The Bengaluru–Chennai economic corridor is designated "
                "as a priority spine under PM GatiShakti's multimodal logistics "
                "integration framework. NIIFL's investment supports the government's "
                "goal of reducing logistics costs from 14% to 8% of GDP by 2030.\n\n"
                "National Monetisation Pipeline (NMP): While GHL itself is a private "
                "concession, two adjacent NHAI-operated stretches (Krishnagiri–Vellore, "
                "62 km) are listed in the NMP for PPP monetisation in FY27 — "
                "representing a potential bolt-on acquisition opportunity for NIIFL.\n\n"
                "Make in India: The Krishnagiri–Vellore corridor serves three major "
                "electronics manufacturing clusters (Samsung, Foxconn, Pegatron supply "
                "chain). GHL directly enables Make in India logistics connectivity."
            ),
            "deal_structure": (
                "Proposed stake: 49% equity acquisition (secondary from PE seller). "
                "Board representation: 2 of 5 board seats, including audit committee "
                "chairmanship. Reserved matters include: annual budget approval, "
                "capex above INR 50 Cr, related-party transactions, change of CEO.\n\n"
                "Shareholder Agreement key terms: Tag-along rights on any transfer "
                "above 5%. Drag-along if NIIFL exercises exit after year 5. ROFR on "
                "any primary share issuance. Anti-dilution: weighted average broad-based "
                "protection below INR 4,200 Cr EV.\n\n"
                "Debt structure: INR 1,800 Cr senior project finance from SBI-led "
                "consortium at 8.4% p.a. fixed for 10 years. DSCR covenant 1.25x "
                "(current: 1.68x — significant headroom). Cash waterfall: O&M reserve "
                "(3 months) → debt service → DSRA replenishment → dividend.\n\n"
                "Conditions precedent: NHAI transfer approval (expected 60 days), "
                "no-objection from lenders (expected 30 days), NIIFL Investment "
                "Committee final approval. No regulatory approval from CCI required "
                "(below threshold).\n\n"
                "Exclusivity: 45-day exclusivity requested. LOI to be signed within "
                "5 business days of IC approval."
            ),
            "recommendation": (
                "INVEST — INR 800 Cr from the NIIF Master Fund, acquiring 49% equity "
                "in Greenway Highways Limited.\n\n"
                "IC approval sought for: Term sheet execution and 45-day exclusivity.\n\n"
                "Rationale: The investment delivers 13.2% base case gross IRR (120 bps "
                "above the 12.0% Master Fund hurdle), 2.1x MOIC, at an entry multiple "
                "40 bps below precedent transactions. The asset is operational, "
                "regulatory risk is low, and the exit pathway via InvIT or strategic "
                "buyer is well-established. The NH-48 corridor is strategically "
                "significant to India's logistics infrastructure and directly aligned "
                "with NIIFL's mandate to catalyse private capital into core "
                "infrastructure.\n\n"
                "Next steps if approved: (1) Execute LOI and exclusivity within 5 "
                "business days. (2) Initiate legal due diligence and lender NOC process. "
                "(3) Commission independent traffic study. (4) Return to IC for final "
                "investment approval in 60 days."
            ),
        },

        "grader": {
            "overall_pass": True,
            "quality_score": 84,
            "section_results": {
                "thesis":            {"pass": True,  "reason": "Clear thesis, exit strategy stated, fund mandate fit confirmed"},
                "market_analysis":   {"pass": True,  "reason": "TAM sourced from ATVM data, 3 competitors named, regulatory status confirmed"},
                "financial_returns": {"pass": True,  "reason": "IRR stated vs hurdle, 3 scenarios, sensitivity table present"},
                "risks_mitigants":   {"pass": True,  "reason": "4 risk categories covered, each has mitigant and residual rating"},
                "esg_impact":        {"pass": True,  "reason": "All 3 NIIFL pillars scored, SDG mapping present, score 74/100"},
                "policy_alignment":  {"pass": True,  "reason": "NIP code stated, PM GatiShakti and NMP referenced with evidence"},
                "deal_structure":    {"pass": True,  "reason": "49% stake, board seats, SHA terms, CPs all stated"},
                "recommendation":    {"pass": True,  "reason": "Clear INVEST, INR 800 Cr from Master Fund, next steps listed"},
            },
            "gaps_to_fix": [],
            "grader_notes": (
                "All 8 sections pass the NIIFL quality rubric. Minor enhancement "
                "opportunity: add secondary buyer universe (strategic + InvIT) to "
                "the exit risk section. ESG score 74/100 is solid but could be "
                "improved by including scope 3 emissions from freight users."
            ),
        },
    },

    "DC002": {
        "deal_id": "DC002",
        "name": "SunGrid Renewables Pvt Ltd",
        "sector": "energy",
        "fund": "india_japan_fund",
        "ticket_cr": 650,
        "stake_pct": 51,
        "entry_ev_cr": 3800,
        "entry_ev_ebitda": 16.1,
        "deal_lead": "Priya Nair",
        "status": "ic_prep",
        "quality_score": 76,
        "irr_base": 14.8,
        "irr_bull": 17.2,
        "irr_bear": 11.9,
        "irr_net": 13.1,
        "moic": 2.3,
        "submitted_at": "2026-05-06T11:30:00",
        "memo_ready": True,
        "docx_ready": False,
        "brief": "5 GW solar platform with Nippon Electric as Japan technology partner.",
        "memo_sections": {
            "thesis": (
                "SunGrid Renewables is India's fourth-largest utility-scale solar "
                "developer with a 5 GW operational and under-construction portfolio "
                "across Rajasthan, Gujarat, and Andhra Pradesh. The IJF thesis rests "
                "on three factors: (i) PPA-backed revenue with 18 DISCOMs providing "
                "25-year contracted cashflows; (ii) a genuine Japan nexus through "
                "Nippon Electric's proprietary bifacial panel technology (8% higher "
                "yield than market standard) and an ongoing technology licensing "
                "arrangement; and (iii) India's renewable energy target of 500 GW by "
                "2030 creating structural demand for SunGrid's development pipeline. "
                "NIIFL acquires 51% for INR 650 Cr at EV INR 3,800 Cr."
            ),
            "market_analysis": (
                "India's solar installed capacity reached 85 GW in FY24 with a target "
                "of 280 GW solar by 2030, implying 25 GW+ annual additions. SunGrid "
                "holds a 2.4% market share with a strong development pipeline. SECI "
                "and state DISCOM offtake agreements provide revenue certainty. "
                "Nippon Electric's bifacial technology gives SunGrid a 15-20% cost "
                "advantage in bid submissions, enabling consistent project wins."
            ),
            "financial_returns": (
                "Base IRR 14.8% vs 14.0% IJF hurdle. MOIC 2.3x over 7-year hold. "
                "Bull case (PLF +8%, carbon credit revenue) 17.2% IRR. Bear "
                "case (curtailment 8%, DISCOM payment delays) 11.9% IRR. "
                "Cross-currency JPY/INR hedge adds 40 bps to net IRR. "
                "Net IRR after fees: 13.1%."
            ),
            "risks_mitigants": (
                "DISCOM payment risk (MEDIUM): Payment Security Mechanism and Letter "
                "of Credit from state governments cover 6 months of receivables. "
                "Grid curtailment risk (LOW): <3% historically across SunGrid's "
                "portfolio. Japan nexus risk (LOW): Nippon Electric is a committed "
                "technology partner with a 10-year licensing agreement in place."
            ),
            "esg_impact": (
                "ESG score 81/100. 890 MW operational capacity displacing 680,000 "
                "tCO2e/year. SDG 7 (Affordable Clean Energy) and SDG 13 (Climate "
                "Action) primary alignment. Rural employment: 2,400 construction "
                "jobs and 340 permanent O&M roles across project sites."
            ),
            "policy_alignment": (
                "NIP confirmed: NIP-EN-2024-0912. PLI Solar Manufacturing: SunGrid "
                "qualifies for PLI tranche 2 for domestic cell manufacturing. "
                "PM-KUSUM: Two projects (180 MW combined) supply agricultural "
                "feeders under PM-KUSUM scheme. JBIC environmental and social "
                "standards compliance confirmed."
            ),
            "deal_structure": (
                "51% equity, 3 board seats. JBIC co-invests 30% on identical terms "
                "(NIIFL effective 51%, JBIC 30%, promoter 19%). Anti-dilution ratchet "
                "if gross IRR falls below 12% at exit. Promoter lock-in: 3 years. "
                "Tag/drag/ROFR standard terms."
            ),
            "recommendation": (
                "INVEST — INR 650 Cr from NIIF India-Japan Fund. Proceed to final IC "
                "with JBIC co-investment confirmation. Authorise term sheet and "
                "45-day exclusivity."
            ),
        },
        "grader": {
            "overall_pass": True,
            "quality_score": 76,
            "grader_notes": "Policy section could add NMP reference. JBIC environmental checklist confirmation needed before final IC.",
        },
    },

    "DC003": {
        "deal_id": "DC003",
        "name": "IndiaStack Digital Infra",
        "sector": "digital_infra",
        "fund": "strategic_opportunities_fund",
        "ticket_cr": 320,
        "stake_pct": 35,
        "entry_ev_cr": 1800,
        "entry_ev_ebitda": 22.4,
        "deal_lead": "Amit Verma",
        "status": "ic_prep",
        "quality_score": 71,
        "irr_base": 18.2,
        "irr_bull": 22.4,
        "irr_bear": 13.8,
        "irr_net": 16.1,
        "moic": 2.7,
        "submitted_at": "2026-05-07T08:00:00",
        "memo_ready": True,
        "docx_ready": False,
        "brief": "B2B digital infrastructure SaaS platform serving 400+ enterprise clients.",
        "memo_sections": {
            "thesis": (
                "IndiaStack Digital Infra (ISDI) offers NIIFL's Strategic Opportunities "
                "Fund a differentiated exposure to India's rapidly digitalising enterprise "
                "infrastructure market. ISDI operates a B2B SaaS platform providing "
                "cloud-hosted digital infrastructure services — API gateway management, "
                "identity and access management, and data residency compliance tooling — "
                "to 400+ enterprise clients across BFSI, healthcare, and government. The "
                "investment thesis rests on three pillars: (i) sticky, recurring revenue "
                "with an average contract tenure of 36 months and 94% gross revenue "
                "retention; (ii) a structural tailwind from India's data localisation "
                "regulations and Digital India mandates driving enterprise spend on "
                "compliant infrastructure; and (iii) a clear path to platform expansion "
                "via the National Data Governance Framework (NDGF), which mandates "
                "certified infrastructure providers for public sector data. NIIFL acquires "
                "35% for INR 320 Cr at EV INR 1,800 Cr (22.4x FY24 EBITDA), consistent "
                "with comparable Indian SaaS infrastructure transactions."
            ),
            "market_analysis": (
                "India's enterprise SaaS market reached USD 8.4 billion in FY24 and is "
                "projected to grow at 28% CAGR through FY28, driven by cloud adoption, "
                "data localisation mandates under the Digital Personal Data Protection "
                "Act 2023, and government Digital India procurement. ISDI's addressable "
                "market in compliance-grade digital infrastructure is estimated at "
                "INR 12,000 Cr by FY27. The competitive landscape includes multinational "
                "hyperscalers (AWS, Azure) and domestic players (Zoho, Freshworks); "
                "ISDI's differentiation is sovereign-compliant data residency and "
                "pre-certified integration with IndiaStack APIs (Aadhaar, UPI, DigiLocker), "
                "which international providers cannot replicate without UIDAI certification. "
                "ISDI holds 7 of the 12 available CERT-In certifications for enterprise "
                "cloud infrastructure — a significant regulatory moat."
            ),
            "financial_returns": (
                "Base case gross IRR of 18.2% (exceeds the 16.0% SOF hurdle by 220 bps) "
                "and 2.7x MOIC over a 6-year hold to exit via strategic trade sale or "
                "secondary to a growth PE fund. Bull case — ARR growth +35% above base, "
                "platform expansion into public sector — delivers 22.4% IRR and 3.3x MOIC. "
                "Bear case — enterprise IT spend slowdown, competitive pressure from "
                "hyperscalers — returns 13.8% IRR and 2.0x MOIC, above capital return "
                "threshold. Net IRR after fees: 16.1% base case. Entry multiple of 22.4x "
                "FY24 EBITDA is benchmarked against comparable Indian enterprise SaaS "
                "transactions averaging 24–26x; the 160 bps discount reflects a primary "
                "growth capital raise rather than secondary. Revenue FY24: INR 80 Cr; "
                "EBITDA INR 80 Cr at 100% margin (fully SaaS). CAGR revenue FY22–24: 41%."
            ),
            "risks_mitigants": (
                "Customer concentration risk (MEDIUM): Top 10 clients represent 38% of "
                "ARR. Mitigant: no single client above 6%; ISDI's 400+ client base "
                "provides diversification. Average contract tenure 36 months reduces "
                "churn velocity. Residual: MEDIUM-LOW.\n\n"
                "Technology / platform risk (MEDIUM): Cloud infrastructure is subject to "
                "rapid technology change. Mitigant: ISDI's API-layer architecture is "
                "technology-agnostic — the platform runs on AWS, Azure, and on-premise "
                "depending on client requirements, insulating it from hyperscaler "
                "platform shifts. Residual: LOW.\n\n"
                "Regulatory risk (LOW): DPDP Act 2023 and data localisation mandates "
                "are structural tailwinds, not risks. CERT-In certification creates a "
                "compliance moat that requires 12–18 months to replicate. Residual: LOW.\n\n"
                "Key person risk (MEDIUM): Founder-CEO Rajan Iyer holds key client "
                "relationships. Mitigant: NIIFL to negotiate key-person retention "
                "package and 3-year founder lock-in as condition of investment. "
                "Residual: MEDIUM."
            ),
            "esg_impact": (
                "ESG overall score: 68/100 (above NIIFL SOF threshold of 60).\n\n"
                "Environment (3.2/5): ISDI's data centres run on 62% renewable energy; "
                "commitment to 100% by FY27. PUE ratio 1.48 — below industry average of "
                "1.58. Carbon footprint INR 2,100 tCO2e FY24; verified by Bureau of "
                "Energy Efficiency. Scope 2 reduction roadmap to 2030 submitted.\n\n"
                "Ease of Living (3.8/5): ISDI's platform underpins digital service "
                "delivery for 3 state government health portals serving 14 million "
                "citizens. DigiLocker integration enables document verification for "
                "12 enterprise clients in financial inclusion use cases.\n\n"
                "Economic Growth (4.0/5): 680 direct FTEs; 72% technology roles. "
                "Annual R&D spend INR 18 Cr (22% of revenue) supporting domestic "
                "software IP creation. 140 internships annually from IIT and NIT "
                "campuses. SDG 9 (Innovation and Infrastructure) and SDG 8 (Decent Work) "
                "primary alignment."
            ),
            "policy_alignment": (
                "Digital India: ISDI is a registered Digital India partner and holds "
                "MeitY empanelment for cloud services (Category A). The platform's "
                "IndiaStack API integrations directly enable government digital service "
                "delivery at scale.\n\n"
                "National Data Governance Framework (NDGF): ISDI is one of 4 certified "
                "providers under the draft NDGF, positioning it to capture mandatory "
                "public sector data infrastructure spend estimated at INR 4,200 Cr "
                "over FY26–29.\n\n"
                "DPDP Act 2023: Data localisation mandates under the Act are a structural "
                "revenue driver. ISDI's sovereign-compliant data residency product "
                "directly addresses the enterprise compliance obligation. Regulatory "
                "clarity expected in FY25 will accelerate enterprise migration.\n\n"
                "Make in India (Software): ISDI's platform is built on 100% domestically "
                "developed software IP. Qualifies for PLI IT hardware complement scheme "
                "for data centre infrastructure expansion."
            ),
            "deal_structure": (
                "Proposed stake: 35% primary equity (growth capital). Board representation: "
                "1 of 5 board seats; observer rights with information access to all "
                "committee meetings. Reserved matters: annual budget approval, capex "
                "above INR 15 Cr, any M&A activity, changes to key management.\n\n"
                "SHA key terms: ROFR on any secondary share transfer. Anti-dilution: "
                "broad-based weighted average. Tag-along on any transfer of 20%+. "
                "Founder lock-in: 3 years from closing date as condition of investment. "
                "Key-person retention: Rajan Iyer and CTO Meera Krishnan.\n\n"
                "Valuation: INR 1,800 Cr pre-money EV. INR 320 Cr primary capital to fund "
                "sales team expansion (INR 120 Cr), data centre capacity (INR 110 Cr), "
                "and product R&D (INR 90 Cr). Post-money EV: INR 2,120 Cr.\n\n"
                "Conditions precedent: FIPB/RBI filing (FDI in technology sector — "
                "standard approval, expected 30 days), founder lock-in execution, "
                "CERT-In compliance confirmation, NIIFL IC final approval.\n\n"
                "Exit pathway: Strategic trade sale to a domestic IT conglomerate or "
                "global SaaS infrastructure player (target: FY30–31 at 28–32x EBITDA). "
                "Secondary to growth PE as interim liquidity option from FY28."
            ),
            "recommendation": (
                "INVEST — INR 320 Cr from the NIIF Strategic Opportunities Fund, "
                "acquiring 35% primary equity in IndiaStack Digital Infra.\n\n"
                "IC approval sought for: Term sheet execution, 30-day exclusivity, "
                "and founder retention negotiation.\n\n"
                "Rationale: The investment delivers 18.2% base case gross IRR (220 bps "
                "above the 16.0% SOF hurdle) and 2.7x MOIC, with a structural regulatory "
                "moat that international competitors cannot easily replicate. "
                "ISDI's CERT-In certifications and IndiaStack API integrations position "
                "it as a mandatory infrastructure layer for enterprise digital compliance "
                "under the DPDP Act. The growth capital structure (primary raise) means "
                "NIIFL's capital directly drives expansion, creating alignment with "
                "the revenue growth assumptions in the model.\n\n"
                "Next steps if approved: (1) Execute LOI and 30-day exclusivity. "
                "(2) Initiate technical due diligence on platform architecture and "
                "CERT-In certifications. (3) Negotiate founder lock-in and key-person "
                "retention. (4) Return to IC for final investment approval in 45 days."
            ),
        },
        "grader": {
            "overall_pass": True,
            "quality_score": 71,
            "section_results": {
                "thesis":            {"pass": True,  "reason": "Clear thesis with 3 pillars, fund mandate fit stated, entry multiple justified"},
                "market_analysis":   {"pass": True,  "reason": "TAM quantified, 3 competitors identified, regulatory moat explained"},
                "financial_returns": {"pass": True,  "reason": "IRR stated vs SOF hurdle, 3 scenarios, entry multiple benchmarked"},
                "risks_mitigants":   {"pass": True,  "reason": "4 risk categories, each with mitigant and residual rating"},
                "esg_impact":        {"pass": True,  "reason": "All 3 NIIFL pillars scored, SDG mapping, score 68/100 above threshold"},
                "policy_alignment":  {"pass": True,  "reason": "Digital India, NDGF, DPDP Act all referenced with evidence"},
                "deal_structure":    {"pass": True,  "reason": "35% stake, board seat, SHA terms, CPs, exit pathway stated"},
                "recommendation":    {"pass": True,  "reason": "Clear INVEST, INR 320 Cr from SOF, next steps listed"},
            },
            "gaps_to_fix": [
                "NIP project code not confirmed — request MeitY project registration number before final IC",
                "JBIC/DFI co-investment not explored — consider approaching DEG or IFC for co-invest to reduce ticket",
            ],
            "grader_notes": (
                "7 of 8 sections pass. Policy alignment is solid but lacks an NIP project code — "
                "request confirmation from ISDI management. ESG score 68/100 is above the 60 "
                "SOF threshold but below Master Fund standard of 70 — appropriate for a digital "
                "infra asset. Key person risk is the primary residual concern; founder lock-in "
                "must be executed as a hard condition precedent."
            ),
        },
    },

    "DC004": {
        "deal_id": "DC004",
        "name": "Sunrise Port Terminal Ltd",
        "sector": "ports",
        "fund": "master_fund",
        "ticket_cr": 900,
        "stake_pct": 74,
        "entry_ev_cr": 5400,
        "entry_ev_ebitda": 14.2,
        "deal_lead": "Priya Nair",
        "status": "ic_prep",
        "quality_score": 79,
        "irr_base": 13.8,
        "irr_bull": 17.4,
        "irr_bear": 10.6,
        "irr_net": 12.1,
        "moic": 2.2,
        "submitted_at": "2026-05-09T10:00:00",
        "memo_ready": True,
        "docx_ready": False,
        "brief": "Container Terminal 3 at JNPT under 30-year concession, 18 years remaining. 1.2M TEU capacity.",
        "memo_sections": {
            "thesis": (
                "Sunrise Port Terminal Ltd (SPTL) offers NIIFL's Master Fund a compelling "
                "entry into India's container port infrastructure — the only private container "
                "terminal in the Mumbai port cluster, operating under a 30-year JNPT concession "
                "with 18 years remaining. The thesis rests on: (i) a fully operational, "
                "zero-construction-risk asset with TAMP-regulated, annually escalating tariffs; "
                "(ii) monopoly positioning in India's largest container gateway handling 4.3M "
                "TEUs annually; and (iii) structural volume growth driven by Maharashtra's "
                "committed Sagarmala road and rail hinterland investments (NIP-PT-2024-0447). "
                "NIIFL acquires 74% at EV INR 5,400 Cr (14.2x FY24 EBITDA), at the lower "
                "bound of comparable Indian port transactions (14.5-16x)."
            ),
            "market_analysis": (
                "JNPT handles 56% of India's containerised trade. SPTL's CT3 handled 1.2M TEUs "
                "in FY24 growing at 9% CAGR over 5 years, driven by a deeper berth (14.5m draft "
                "enabling post-Panamax calls) vs JNPT average. Competitive position is "
                "concession-protected: no new competing capacity at JNPT within 8-10 years. "
                "Key demand drivers: India's USD 2 trillion export target by 2030, manufacturing "
                "shift from China, and the logistics cost reduction agenda. TAMP annual "
                "escalation is regulatory and contractually embedded."
            ),
            "financial_returns": (
                "Base IRR 13.8% vs 12.0% Master Fund hurdle (+180 bps). MOIC 2.2x over 7 years. "
                "Bull case (throughput +12%, tariff 6.5%): 17.4% IRR, 2.7x MOIC. "
                "Bear case (flat throughput, tariff 3.5%): 10.6% IRR, 1.8x MOIC. "
                "Net IRR after fees: 12.1%. Entry 14.2x at low end of comparables; "
                "exit at 16.5x reflects stabilised infrastructure re-rating. "
                "Key sensitivity: 10% throughput variance = ~130 bps IRR impact."
            ),
            "risks_mitigants": (
                "Throughput/trade risk (MEDIUM): Diversified cargo mix; no shipper above 8%. "
                "Bear case at flat growth. Residual: MEDIUM-LOW. "
                "Tariff/regulatory risk (LOW): TAMP regulatory escalation; no tariff freeze "
                "in 30-year JNPT history. Residual: LOW. "
                "Concession termination (LOW): Material breach + 90-day cure required; "
                "no breach history in 15 years. Residual: LOW. "
                "CT4 expansion risk (MEDIUM): Competitor CT4 from FY32 possible. "
                "Mitigant: SPTL right of first offer on CT4 under NMP. Residual: MEDIUM."
            ),
            "esg_impact": (
                "ESG score 77/100. Shore power by FY27 (4,200 tCO2e/year reduction). "
                "2.4 MW rooftop solar. Scope 1+2: 8,400 tCO2e FY24. "
                "2,840 direct FTEs; 9,200 indirect jobs. Annual GST: INR 68 Cr. "
                "Container dwell time 3.2 days vs JNPT average 4.1. SDG 9, 8, 17 aligned."
            ),
            "policy_alignment": (
                "NIP-PT-2024-0447 confirmed. Sagarmala Phase II node — Maharashtra committed "
                "INR 2,800 Cr for CT3 road and rail connectivity. NMP: CT4 right of first "
                "offer aligned with container capacity doubling target. Make in India: CT3 "
                "handles 22% of India's electronics exports."
            ),
            "deal_structure": (
                "74% majority equity. 4 of 5 board seats including chairmanship. Full "
                "operational control. Promoter retains 26% with standard minority protections. "
                "Debt: INR 1,800 Cr senior PF at 8.6% p.a. fixed; DSCR covenant 1.30x "
                "(current 1.74x). FY24 dividend: INR 95 Cr. CPs: JNPT authority approval "
                "(45 days), lender NOC (30 days). Exclusivity: 30 days from LOI."
            ),
            "recommendation": (
                "INVEST — INR 900 Cr from NIIF Master Fund, acquiring 74% equity in SPTL. "
                "Base IRR 13.8% (180 bps above hurdle), majority control of a concession-"
                "protected monopoly in India's largest container gateway. Clear exit via "
                "strategic port operator or InvIT. Sagarmala connectivity de-risks throughput. "
                "Note: placeholder memo — re-submit via New Deal form for live Claude Opus memo."
            ),
        },
        "grader": {
            "overall_pass": True,
            "quality_score": 79,
            "section_results": {
                "thesis":            {"pass": True, "reason": "Monopoly positioning, 3 pillars, entry multiple benchmarked"},
                "market_analysis":   {"pass": True, "reason": "JNPT data specific, competitive moat, demand drivers stated"},
                "financial_returns": {"pass": True, "reason": "IRR vs hurdle, 3 scenarios, sensitivity stated"},
                "risks_mitigants":   {"pass": True, "reason": "4 risks with mitigants and residual ratings"},
                "esg_impact":        {"pass": True, "reason": "All 3 NIIFL pillars, SDG mapping, score 77/100"},
                "policy_alignment":  {"pass": True, "reason": "NIP code, Sagarmala and NMP with specifics"},
                "deal_structure":    {"pass": True, "reason": "74% stake, board control, debt structure, CPs"},
                "recommendation":    {"pass": True, "reason": "Clear INVEST, INR 900 Cr, rationale stated"},
            },
            "gaps_to_fix": ["CT4 right of first offer — confirm legal status with JNPT before final IC"],
            "grader_notes": "Placeholder memo — re-submit to generate live Claude Opus version.",
        },
    },
}
