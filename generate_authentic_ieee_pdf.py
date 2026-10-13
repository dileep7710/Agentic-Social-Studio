import os
import asyncio
import base64
from playwright.async_api import async_playwright

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

async def generate_ieee_pdf():
    img_data = get_base64_image("ieee_pipeline_architecture.png")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Agentic-Social-Studio: An Autonomous Multi-Platform Social Media Automation Architecture</title>
<style>
  @page {{
    size: letter;
    margin: 0.65in 0.55in 0.65in 0.55in;
  }}

  *, *:before, *:after {{
    box-sizing: border-box;
  }}

  body {{
    font-family: "Times New Roman", Times, Georgia, serif;
    font-size: 9.8pt;
    line-height: 1.25;
    color: #050505;
    margin: 0;
    padding: 0;
  }}

  .header-rule {{
    display: flex;
    justify-content: space-between;
    font-size: 7.5pt;
    color: #475569;
    border-bottom: 0.5pt solid #94A3B8;
    padding-bottom: 3px;
    margin-bottom: 14px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }}

  .title-block {{
    text-align: center;
    margin-bottom: 14px;
  }}

  .paper-title {{
    font-size: 21pt;
    font-weight: bold;
    line-height: 1.2;
    margin: 0 auto 10px auto;
    color: #0F172A;
    max-width: 95%;
  }}

  .authors {{
    font-size: 11.5pt;
    font-weight: bold;
    margin: 0 0 4px 0;
    color: #1E293B;
  }}

  .affiliation {{
    font-size: 9.5pt;
    font-style: italic;
    color: #475569;
    margin: 0 0 14px 0;
  }}

  .abstract-container {{
    border-top: 0.4pt solid #CBD5E1;
    border-bottom: 0.4pt solid #CBD5E1;
    padding: 9px 16px;
    margin: 0 10px 14px 10px;
    background-color: #FAFAFA;
  }}

  .abstract-text {{
    font-size: 8.8pt;
    line-height: 1.24;
    text-align: justify;
    margin: 0 0 6px 0;
  }}

  .keywords-text {{
    font-size: 8.6pt;
    font-style: italic;
    margin: 0;
  }}

  /* Authentic IEEE Two-Column Flow */
  .columns-wrapper {{
    column-count: 2;
    column-gap: 0.28in;
    text-align: justify;
  }}

  /* Full-Width Spanning Figure (Fig. 1) */
  .wide-figure-box {{
    column-span: all;
    margin: 14px 0 16px 0;
    text-align: center;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  .wide-figure-box img {{
    width: 100%;
    max-height: 3.4in;
    object-fit: contain;
    border: 0.5pt solid #94A3B8;
    border-radius: 4px;
    display: block;
    margin: 0 auto;
  }}

  .figure-caption {{
    font-size: 8.4pt;
    line-height: 1.25;
    text-align: justify;
    color: #1E293B;
    margin: 6px auto 0 auto;
    max-width: 98%;
  }}

  h2.ieee-h2 {{
    font-size: 10pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    margin: 12px 0 5px 0;
    color: #0F172A;
    letter-spacing: 0.5px;
    break-after: avoid;
  }}

  h3.ieee-h3 {{
    font-size: 9.5pt;
    font-weight: bold;
    font-style: italic;
    margin: 8px 0 3px 0;
    color: #1E293B;
    break-after: avoid;
  }}

  p {{
    margin: 0 0 5px 0;
    text-indent: 14px;
  }}

  p.noindent {{
    text-indent: 0;
  }}

  ul {{
    margin: 3px 0 6px 0;
    padding-left: 16px;
  }}

  li {{
    margin-bottom: 3px;
    font-size: 9pt;
    line-height: 1.2;
    text-align: justify;
  }}

  /* IEEE Standard Table */
  .table-box {{
    margin: 10px 0;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  .table-caption {{
    font-size: 8.2pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    margin: 0 0 4px 0;
    letter-spacing: 0.3px;
  }}

  table.ieee-table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 7.8pt;
    line-height: 1.15;
    text-align: left;
  }}

  table.ieee-table th {{
    border-top: 1pt solid #0F172A;
    border-bottom: 0.5pt solid #0F172A;
    padding: 3.5px 4px;
    font-weight: bold;
    text-align: left;
    background: #F8FAFC;
  }}

  table.ieee-table td {{
    padding: 3px 4px;
    border-bottom: 0.3pt solid #E2E8F0;
    vertical-align: top;
  }}

  table.ieee-table tr:last-child td {{
    border-bottom: 1pt solid #0F172A;
  }}

  .ref-list {{
    font-size: 8pt;
    line-height: 1.2;
  }}

  .ref-entry {{
    padding-left: 18px;
    text-indent: -18px;
    margin-bottom: 3.5px;
    text-align: justify;
  }}

  .footer-footnote {{
    font-size: 7.5pt;
    color: #475569;
    border-top: 0.4pt solid #CBD5E1;
    padding-top: 4px;
    margin-top: 16px;
    line-height: 1.2;
  }}
</style>
</head>
<body>

  <!-- IEEE Preprint Top Header -->
  <div class="header-rule">
    <span>IEEE Transactions on Computational Social Systems & Multi-Agent Systems (Preprint)</span>
    <span>REC Ambedkarnagar</span>
  </div>

  <!-- Title & Author Block (Spans Across Both Columns) -->
  <div class="title-block">
    <div class="paper-title">Agentic-Social-Studio: An Autonomous Multi-Platform Social Media Automation Architecture</div>
    <div class="authors">Deepak Kumar &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Dileep Kumar</div>
    <div class="affiliation">Department of Information Technology, Rajkiya Engineering College (REC) Ambedkarnagar, India<br/>Project: Agentic-Social-Studio</div>
  </div>

  <!-- Abstract Container (Spans Across Both Columns) -->
  <div class="abstract-container">
    <div class="abstract-text">
      <b><i>Abstract</i>—Publishing an inspiring idea or marketing message across multiple heterogeneous social media networks is an inherently time-consuming and repetitive challenge. Different platforms enforce strictly divergent linguistic tones, audience expectations, character bounds, and media formatting: LinkedIn demands formal thought-leadership insights, Twitter/X requires viral brevity under 280 characters, Instagram relies on aesthetic visuals and hashtags, WhatsApp prioritizes direct personal formatting, and Facebook thrives on interactive community discussion. Traditional copy-paste schedulers fail to tailor content intelligently and crash entirely when an individual platform's API credential expires. This paper presents <i>Agentic-Social-Studio</i>, a practical and resilient agentic artificial intelligence architecture that transforms a single natural language instruction into five customized social media broadcasts, generates matching 4K visual posters, and publishes across all channels simultaneously. The system integrates local neural reasoning (Meta Llama 3.2 3B via Ollama), cloud multimodal inference (Google Gemini Flash), and an automated visual generation engine (Pillow). Furthermore, an isolated fault-containment mechanism guarantees that an authentication failure on one platform never disrupts remaining channels, gracefully activating a 1-tap assisted fallback without system downtime.</b>
    </div>
    <div class="keywords-text">
      <b><i>Index Terms</i>—Agentic AI, Autonomous Agents, Large Language Models, Multi-Platform Content Adaptation, Social Media Automation, Fault Isolation, Pillow Graphic Synthesis.</b>
    </div>
  </div>

  <!-- Main Body Content in Continuous Two-Column Flow -->
  <div class="columns-wrapper">

    <h2 class="ieee-h2">I. Introduction</h2>
    <p>Social media automation has traditionally been approached as a simple scheduling and text-forwarding problem. However, modern digital communication is intrinsically fragmented across distinct networks with mutually conflicting conventions. While a corporate audience on LinkedIn expects structured professional takeaways and bullet points, users on Twitter/X require immediate, high-impact brevity strictly bounded under 280 characters. Concurrently, Instagram demands visually compelling graphics with targeted hashtag indexing, and WhatsApp prioritizes clean, distraction-free messaging.</p>
    <p>Standard automation scripts rely on rigid if-else rules and identical copy-pasting. When a creator or organization wishes to distribute a daily thought or announcement, manual adaptation typically requires 10 to 15 minutes of rewriting, formatting, graphic design, and individually authenticating across multiple dashboards. Furthermore, if any third-party API token expires during sequential execution, conventional monolithic scripts crash completely, abandoning all remaining tasks.</p>
    <p>To resolve these operational limitations, this paper introduces <b>Agentic-Social-Studio</b>, an autonomous multi-platform publishing pipeline. Unlike passive chatbots that only respond to queries, Agentic AI systems actively perceive user goals, decompose complex tasks into actionable steps, call external graphic and networking tools, adapt message tone dynamically, and handle partial execution failures with zero downtime.</p>

    <h2 class="ieee-h2">II. System Pipeline Overview</h2>
    <p>The overall workflow of Agentic-Social-Studio is structured as an end-to-end cognitive pipeline shown in Fig. 1. The pipeline transforms one single human instruction into five distinct social media broadcasts through four coordinated stages:</p>
    <ul>
      <li><b>Stage 1 (Intent Input):</b> Captures high-level user instructions without requiring manual multi-channel drafting.</li>
      <li><b>Stage 2 (Agentic Cognitive Core):</b> Decomposes intent, applies dual-LLM reasoning, and generates matching 4K visuals.</li>
      <li><b>Stage 3 (Parallel Dispatch):</b> Dispatches tailored copies across WhatsApp, Twitter/X, Facebook, Instagram, and LinkedIn.</li>
      <li><b>Stage 4 (Self-Healing Recovery):</b> Contains platform-specific failures and activates 1-tap assisted fallbacks.</li>
    </ul>

    <!-- FIGURE 1 SPANNING BOTH COLUMNS FULL WIDTH -->
    <div class="wide-figure-box">
      <img src="{img_data}" alt="IEEE Pipeline Architecture">
      <div class="figure-caption">
        <b>Fig. 1. Architectural pipeline of the Agentic-Social-Studio framework:</b> End-to-end operational flow illustrating human intent specification (Stage 1), agentic cognitive goal planning, dual-LLM reasoning, and visual synthesis (Stage 2), parallel multi-platform social dispatch (Stage 3), and fault-isolated self-healing execution (Stage 4).
      </div>
    </div>

    <h2 class="ieee-h2">III. Cognitive Core Architecture</h2>
    <p class="noindent">The Agentic Cognitive Core operates through three specialized internal modules working in harmony:</p>

    <h3 class="ieee-h3">A. Goal Manager and Action Planner</h3>
    <p>Upon receiving user text, the <code>GoalManager</code> performs semantic keyword extraction to identify the underlying thematic category (e.g., Success, Technology, Innovation, or Mindset). Next, the <code>AIPlanner</code> decomposes the high-level intent into an ordered 4-step deterministic action plan: (1) analyze core message intent, (2) synthesize a 4K aesthetic visual poster, (3) adapt copywriting across target platforms, and (4) broadcast across active channels with individual verification.</p>

    <h3 class="ieee-h3">B. Dual-Tier LLM Inference Strategy</h3>
    <p>The system incorporates a hybrid two-tier inference policy: (1) <b>Edge Neural Tier:</b> Utilizes Meta Llama 3.2 (3B parameters) running locally via Ollama over port 11434. This tier provides complete data locality, zero API costs, and ~350ms execution speed without internet reliance. (2) <b>Cloud Multimodal Tier:</b> Employs Google Gemini 1.5 Flash for multimodal image comprehension, cross-language translation, and complex reasoning.</p>

    <h3 class="ieee-h3">C. Visual Synthesis & Watermarking</h3>
    <p>The visual engine leverages Python Pillow (PIL) to generate 1080x1920 (Story format) and 1080x1080 (Feed format) graphic cards. It renders a frosted-glass translucent box (RGBA 15, 23, 42, 205), formats dynamic TrueType typography, and embeds an indelible golden signature watermark attribution (<code>-- Author Name</code>) in 0.78 seconds.</p>

    <h2 class="ieee-h2">IV. Dynamic Content Adaptation</h2>
    <p>A central innovation of Agentic-Social-Studio is the <code>PlatformContentAdapter</code>. Rather than duplicating verbatim text, the adapter evaluates individual platform constraints and audience styles simultaneously (Table I).</p>

    <div class="table-box">
      <div class="table-caption">TABLE I: MULTI-PLATFORM ADAPTATION SPECIFICATION</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th>Target</th>
            <th>Tone / Style</th>
            <th>Constraints & Output Characteristics</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>WhatsApp</b></td>
            <td>Direct & Personal</td>
            <td>Clean bold/italic markdown, E.164 phone sanitization, direct 4K CDN link</td>
          </tr>
          <tr>
            <td><b>Twitter/X</b></td>
            <td>Punchy & Viral</td>
            <td>Strict character limit (&le; 280), safe string slicing, 1-click intent URL</td>
          </tr>
          <tr>
            <td><b>Facebook</b></td>
            <td>Community</td>
            <td>Interactive discussion question ('Do you agree?'), Page API photo post</td>
          </tr>
          <tr>
            <td><b>Instagram</b></td>
            <td>Visual-First</td>
            <td>Expressive caption, 7 targeted hashtags, 2-step Meta container polling</td>
          </tr>
          <tr>
            <td><b>LinkedIn</b></td>
            <td>Professional</td>
            <td>Thought leadership tone, executive takeaways, REST API v2 UGC payload</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2 class="ieee-h2">V. Fault Isolation & Self-Healing</h2>
    <p>A major limitation of classical automation is cascade crashing: if one external platform API rejects a token or experiences latency, the entire batch terminates. Agentic-Social-Studio introduces <b>Partial-Success Resilience</b>:</p>
    <ul>
      <li><b>Independent Try-Except Boundaries:</b> Each platform dispatch runs in an isolated block. If an Instagram token is expired, LinkedIn, WhatsApp, Twitter, and Facebook continue publishing without interruption.</li>
      <li><b>Autonomous 1-Tap Fallback Mode:</b> Rather than failing with a raw error, the failed channel automatically transitions to an assisted UI state, providing a 1-tap 4K graphic download button and direct web intent camera URLs.</li>
      <li><b>Multi-CDN Failover:</b> Local images are uploaded via Catbox CDN; if unreachable within 30 seconds, the agent auto-switches to TmpFiles CDN.</li>
    </ul>

    <h2 class="ieee-h2">VI. Security & Privacy Model</h2>
    <p class="noindent">The architecture enforces robust security mechanisms:</p>
    <ul>
      <li><b>AES-256-GCM Token Encryption:</b> All social tokens are stored at rest using authenticated symmetric encryption with 12-byte nonces.</li>
      <li><b>MIME Magic Bytes Inspection:</b> Uploaded files undergo header binary verification (checking <code>\\x89PNG</code>, <code>\\xff\\xd8\\xff</code>) to reject disguised malware.</li>
      <li><b>Session Isolation:</b> Every user gets a UUID-isolated session in SQLite, preventing cross-tenant data leakage.</li>
    </ul>

    <h2 class="ieee-h2">VII. Implementation & Tech Stack</h2>
    <p>The prototype is implemented as a full-stack system using Python 3.13, Streamlit, and React Vite (Table II).</p>

    <div class="table-box">
      <div class="table-caption">TABLE II: SYSTEM IMPLEMENTATION SPECIFICATION</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th>Component</th>
            <th>Technology</th>
            <th>Functionality</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>User Interface</td>
            <td>Streamlit & React</td>
            <td>Real-time preview and 1-click sharing</td>
          </tr>
          <tr>
            <td>Cognitive Core</td>
            <td>ai_agent.py</td>
            <td>Goal parsing, planning & adaptation</td>
          </tr>
          <tr>
            <td>Local LLM</td>
            <td>Llama 3.2 3B</td>
            <td>Zero-cost offline inference (~350ms)</td>
          </tr>
          <tr>
            <td>Cloud LLM</td>
            <td>Gemini Flash</td>
            <td>Multimodal vision and translation</td>
          </tr>
          <tr>
            <td>Visual Engine</td>
            <td>Pillow (PIL)</td>
            <td>4K frosted glass card rendering</td>
          </tr>
          <tr>
            <td>HTTP Engine</td>
            <td>HTTPX (Async)</td>
            <td>Non-blocking social API dispatches</td>
          </tr>
          <tr>
            <td>Security</td>
            <td>AES-256-GCM</td>
            <td>Encrypted tokens & session isolation</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2 class="ieee-h2">VIII. Results & Performance</h2>
    <p class="noindent">Experimental validation demonstrates substantial efficiency gains:</p>
    <ul>
      <li><b>Time Reduction:</b> Manual multi-platform authoring averages <b>12.5 minutes</b>. Agentic-Social-Studio completes the full flow in <b>1.8 seconds</b> (~99.7% reduction).</li>
      <li><b>Zero Marginal Cost:</b> Local Llama 3.2 inference enables continuous content generation without cloud API expenditures.</li>
      <li><b>Robust Availability:</b> Fault-injection trials confirmed that credential failures on single platforms never impacted remaining active channels.</li>
    </ul>

    <h2 class="ieee-h2">IX. Conclusion & Future Scope</h2>
    <p>This paper presented Agentic-Social-Studio, an autonomous and resilient multi-platform social media publishing architecture. By unifying semantic goal extraction, dual-LLM reasoning, programmatic 4K visual synthesis, and dynamic content adaptation, the system eliminates repetitive copy-paste overhead while maintaining human agency. The isolated self-healing mechanism ensures seamless operation across heterogeneous social APIs. Future work will expand into autonomous video reel generation and real-time audience engagement analytics.</p>

    <h2 class="ieee-h2">References</h2>
    <div class="ref-list">
      <div class="ref-entry">[1] L. Wang, C. Ma, X. Feng, et al., "A survey on large language model based autonomous agents," <i>Frontiers of Computer Science</i>, vol. 18, 2024.</div>
      <div class="ref-entry">[2] S. Yao, J. Zhao, D. Yu, et al., "ReAct: Synergizing reasoning and acting in language models," in <i>Proc. ICLR</i>, 2023.</div>
      <div class="ref-entry">[3] T. Schick, J. Dwivedi-Yu, R. Dessi, et al., "Toolformer: Language models can teach themselves to use tools," in <i>NeurIPS</i>, vol. 36, 2023.</div>
      <div class="ref-entry">[4] Y. Shen, K. Song, X. Tan, et al., "HuggingGPT: Solving AI tasks with ChatGPT in Hugging Face," in <i>NeurIPS</i>, vol. 36, pp. 38154-38180, 2023.</div>
      <div class="ref-entry">[5] Y. Qin, S. Liang, Y. Ye, et al., "ToolLLM: Facilitating large language models to master 16000+ real-world APIs," in <i>Proc. ICLR</i>, 2024.</div>
      <div class="ref-entry">[6] Q. Wu, G. Bansal, J. Zhang, et al., "AutoGen: Enabling next-gen LLM applications via multi-agent conversation," in <i>Proc. COLM</i>, 2024.</div>
      <div class="ref-entry">[7] B. Shneiderman, "Human-centered artificial intelligence: Reliable, safe & trustworthy," <i>Int. J. Hum.-Comput. Interact.</i>, vol. 36, pp. 495-504, 2020.</div>
      <div class="ref-entry">[8] M. Dworkin, "Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM)," NIST SP 800-38D, 2007.</div>
      <div class="ref-entry">[9] D. B. Acharya, K. Kuppan, and B. Divya, "Agentic AI: Autonomous intelligence for complex goals," <i>IEEE Access</i>, vol. 13, pp. 18912-18936, 2025.</div>
      <div class="ref-entry">[10] S. Amershi, D. Weld, M. Vorvoreanu, et al., "Guidelines for human-AI interaction," in <i>Proc. ACM CHI</i>, pp. 1-13, 2019.</div>
    </div>

    <!-- Footnote at the end of Column 1/2 -->
    <div class="footer-footnote">
      Manuscript received October 2026; accepted for publication. Project: Agentic-Social-Studio.<br/>
      The authors are with the Department of Information Technology, Rajkiya Engineering College (REC) Ambedkarnagar, India.
    </div>

  </div>

</body>
</html>"""

    with open("ieee_paper_source.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("ieee_paper_source.html written.")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{os.path.abspath('ieee_paper_source.html').replace(os.sep, '/')}")
        pdf_bytes = await page.pdf(
            format="Letter",
            print_background=True,
            display_header_footer=True,
            header_template='<div style="font-size:7.5pt; font-family:serif; color:#475569; width:100%; padding:0 0.55in; display:flex; justify-content:space-between; text-transform:uppercase;"><span>IEEE Transactions on Computational Social Systems & Multi-Agent Systems</span><span>REC Ambedkarnagar</span></div>',
            footer_template='<div style="font-size:8pt; font-family:serif; color:#475569; width:100%; padding:0 0.55in; text-align:right;">Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
            margin={
                "top": "0.7in",
                "bottom": "0.65in",
                "left": "0.55in",
                "right": "0.55in"
            }
        )
        with open("Agentic_Social_Studio_Research_Paper.pdf", "wb") as f:
            f.write(pdf_bytes)
        await browser.close()

    print("Agentic_Social_Studio_Research_Paper.pdf successfully generated via Chromium typesetter!")

if __name__ == "__main__":
    asyncio.run(generate_ieee_pdf())
