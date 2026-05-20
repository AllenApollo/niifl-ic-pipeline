"""
STEP 5 — IC Memo → DOCX Formatter
====================================
Converts the orchestrator's JSON memo output into a formatted
partner-ready Word document using the docx npm package.

Usage:
    python3 step5_format_memo.py <path_to_deal_json>
    python3 step5_format_memo.py outputs/DC202505_Greenway_Highways.json

Output:
    outputs/<deal_id>_IC_Memo.docx
"""

import os, sys, json, subprocess, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "config"))
from config import OUTPUTS_DIR

def generate_memo_docx(deal_output: dict) -> str:
    """
    Takes orchestrator output dict, generates formatted IC memo DOCX.
    Returns path to output file.
    """
    deal_id   = deal_output.get("deal_id", "DEAL")
    deal_name = deal_output.get("deal_name", "Deal")
    fund_key  = deal_output.get("fund", "master_fund")
    memo      = deal_output.get("ic_memo_sections", {})
    model     = deal_output.get("financial_model", {})
    grader    = deal_output.get("grader_result", {})
    score     = grader.get("quality_score", 0)

    fund_display = {
        "master_fund":                  "NIIF Master Fund",
        "strategic_opportunities_fund": "NIIF Strategic Opportunities Fund",
        "private_markets_fund":         "NIIF Private Markets Fund",
        "india_japan_fund":             "NIIF India-Japan Fund",
    }.get(fund_key, fund_key)

    def safe(key, fallback="[To be completed]"):
        val = memo.get(key, fallback)
        if isinstance(val, dict):
            return json.dumps(val, indent=2)
        return str(val) if val else fallback

    # Escape for JS template literal
    def esc(s):
        return (str(s)
                .replace("\\", "\\\\")
                .replace("`", "\\`")
                .replace("${", "\\${"))

    js = f"""
const {{ Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
         HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
         LevelFormat, VerticalAlign, PageBreak }} = require('docx');
const fs = require('fs');

const border  = {{ style: BorderStyle.SINGLE, size: 1, color: "CCCCCC" }};
const borders = {{ top: border, bottom: border, left: border, right: border }};
const hBorder = {{ style: BorderStyle.SINGLE, size: 1, color: "1F3864" }};
const hBorders= {{ top: hBorder, bottom: hBorder, left: hBorder, right: hBorder }};
const cm = {{ top: 80, bottom: 80, left: 120, right: 120 }};

function h1(t) {{
  return new Paragraph({{ heading: HeadingLevel.HEADING_1, spacing:{{before:360,after:120}},
    children:[new TextRun({{text:t, bold:true, size:32, font:"Arial", color:"1F3864"}})] }});
}}
function h2(t) {{
  return new Paragraph({{ heading: HeadingLevel.HEADING_2, spacing:{{before:240,after:80}},
    children:[new TextRun({{text:t, bold:true, size:26, font:"Arial", color:"2E74B5"}})] }});
}}
function para(t, opts={{}}) {{
  return new Paragraph({{ spacing:{{before:60,after:80}},
    children:[new TextRun({{text:t, size:22, font:"Arial", ...opts}})] }});
}}
function bullet(t) {{
  return new Paragraph({{ numbering:{{reference:"bullets",level:0}}, spacing:{{before:40,after:40}},
    children:[new TextRun({{text:t, size:22, font:"Arial"}})] }});
}}
function divider() {{
  return new Paragraph({{ spacing:{{before:100,after:100}},
    border:{{bottom:{{style:BorderStyle.SINGLE,size:6,color:"2E74B5",space:1}}}},
    children:[] }});
}}
function kv(label, value) {{
  return new Paragraph({{ spacing:{{before:40,after:40}},
    children:[
      new TextRun({{text: label + ": ", bold:true, size:22, font:"Arial"}}),
      new TextRun({{text: value, size:22, font:"Arial"}})
    ] }});
}}

function hdrRow(cells, widths) {{
  return new TableRow({{ tableHeader:true, children: cells.map((t,i) =>
    new TableCell({{ borders:hBorders, width:{{size:widths[i],type:WidthType.DXA}},
      shading:{{fill:"1F3864",type:ShadingType.CLEAR}}, margins:cm,
      children:[new Paragraph({{children:[new TextRun({{text:t,bold:true,size:20,font:"Arial",color:"FFFFFF"}})]}})]
    }})
  )}});
}}
function row(cells, widths, shade=false) {{
  return new TableRow({{ children: cells.map((t,i) =>
    new TableCell({{ borders, width:{{size:widths[i],type:WidthType.DXA}},
      shading:{{fill:shade?"EEF3FB":"FFFFFF",type:ShadingType.CLEAR}}, margins:cm,
      children:[new Paragraph({{children:[new TextRun({{text:t,size:20,font:"Arial"}})]}})]
    }})
  )}});
}}

const doc = new Document({{
  numbering: {{ config: [{{ reference:"bullets",
    levels:[{{level:0,format:LevelFormat.BULLET,text:"\\u2022",alignment:AlignmentType.LEFT,
      style:{{paragraph:{{indent:{{left:720,hanging:360}}}}}}}}] }}] }},
  styles: {{
    default: {{ document: {{ run: {{ font:"Arial", size:22 }} }} }},
    paragraphStyles: [
      {{ id:"Heading1",name:"Heading 1",basedOn:"Normal",next:"Normal",quickFormat:true,
         run:{{size:32,bold:true,font:"Arial",color:"1F3864"}},
         paragraph:{{spacing:{{before:360,after:120}},outlineLevel:0}} }},
      {{ id:"Heading2",name:"Heading 2",basedOn:"Normal",next:"Normal",quickFormat:true,
         run:{{size:26,bold:true,font:"Arial",color:"2E74B5"}},
         paragraph:{{spacing:{{before:240,after:80}},outlineLevel:1}} }},
    ]
  }},
  sections: [{{
    properties: {{ page: {{ size:{{width:12240,height:15840}},
      margin:{{top:1440,right:1440,bottom:1440,left:1440}} }} }},
    children: [
      // ── COVER ──
      new Paragraph({{ spacing:{{before:1440,after:120}},
        children:[new TextRun({{text:"CONFIDENTIAL",bold:true,size:24,font:"Arial",color:"C00000"}})] }}),
      new Paragraph({{ spacing:{{before:120,after:120}},
        children:[new TextRun({{text:"Investment Committee Memorandum",bold:true,size:52,font:"Arial",color:"1F3864"}})] }}),
      divider(),
      kv("Company", `{esc(deal_name)}`),
      kv("Fund",    `{esc(fund_display)}`),
      kv("Deal ID", `{esc(deal_id)}`),
      kv("Date",    new Date().toLocaleDateString('en-IN',{{day:'2-digit',month:'long',year:'numeric'}})),
      kv("AI Quality Score", `{score}/100`),
      new Paragraph({{ children:[new PageBreak()] }}),

      // ── SECTION 1 — THESIS ──
      h1("1. Investment Thesis"),
      para(`{esc(safe('thesis'))}`),
      divider(),

      // ── SECTION 2 — MARKET ──
      h1("2. Market & Competitive Position"),
      para(`{esc(safe('market_analysis'))}`),
      divider(),

      // ── SECTION 3 — FINANCIALS ──
      h1("3. Financial Returns"),
      para(`{esc(safe('financial_returns'))}`),
      h2("3.1 Returns Summary"),
      new Table({{
        width:{{size:9360,type:WidthType.DXA}}, columnWidths:[3120,3120,3120],
        rows:[
          hdrRow(["Scenario","IRR (Gross)","MOIC"],[3120,3120,3120]),
          row(["Base case",`{esc(str(model.get('base_irr','—')))}%`,`{esc(str(model.get('base_moic','—')))}x`],[3120,3120,3120],false),
          row(["Bull case",`{esc(str(model.get('bull_irr','—')))}%`,"—"],[3120,3120,3120],true),
          row(["Bear case",`{esc(str(model.get('bear_irr','—')))}%`,"—"],[3120,3120,3120],false),
        ]
      }}),
      divider(),

      // ── SECTION 4 — RISKS ──
      h1("4. Key Risks & Mitigants"),
      para(`{esc(safe('risks_mitigants'))}`),
      divider(),

      // ── SECTION 5 — ESG ──
      h1("5. ESG & Impact"),
      para(`{esc(safe('esg_impact'))}`),
      divider(),

      // ── SECTION 6 — POLICY ──
      h1("6. Policy Alignment"),
      para(`{esc(safe('policy_alignment'))}`),
      divider(),

      // ── SECTION 7 — DEAL STRUCTURE ──
      h1("7. Deal Structure & Terms"),
      para(`{esc(safe('deal_structure'))}`),
      divider(),

      // ── SECTION 8 — RECOMMENDATION ──
      h1("8. Recommendation"),
      para(`{esc(safe('recommendation'))}`),
      divider(),

      // ── QA GRADER SUMMARY ──
      h1("Appendix — AI Quality Assurance Summary"),
      kv("Overall Pass", `{str(grader.get('overall_pass', False))}`),
      kv("Quality Score", `{score}/100`),
      kv("Grader Notes", `{esc(grader.get('grader_notes',''))}`),
      new Paragraph({{ spacing:{{before:480}},
        children:[new TextRun({{text:"— This memo was drafted by NIIFL's AI engine and reviewed by a qualified investment professional before IC presentation. —",
          size:18,font:"Arial",color:"595959",italics:true}})] }}),
    ]
  }}]
}});

Packer.toBuffer(doc).then(buf => {{
  fs.writeFileSync("{esc(os.path.join(OUTPUTS_DIR, f'{deal_id}_IC_Memo.docx'))}", buf);
  console.log("DOCX written");
}});
"""

    # Write temp JS and run
    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False) as tmp:
        tmp.write(js)
        tmp_path = tmp.name

    result = subprocess.run(["node", tmp_path], capture_output=True, text=True)
    os.unlink(tmp_path)

    if result.returncode != 0:
        raise RuntimeError(f"DOCX generation failed:\n{result.stderr}")

    out_path = os.path.join(OUTPUTS_DIR, f"{deal_id}_IC_Memo.docx")
    print(f"  IC Memo DOCX written: {out_path}")
    return out_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        # Use latest output file for demo
        files = sorted([f for f in os.listdir(OUTPUTS_DIR) if f.endswith(".json")])
        if not files:
            print("No output JSON files found. Run step4_build_orchestrator.py first.")
            sys.exit(1)
        json_path = os.path.join(OUTPUTS_DIR, files[-1])
    else:
        json_path = sys.argv[1]

    print(f"Formatting memo from: {json_path}")
    with open(json_path) as f:
        deal_output = json.load(f)

    docx_path = generate_memo_docx(deal_output)
    print(f"\nStep 5 complete — IC Memo DOCX ready: {docx_path}")
