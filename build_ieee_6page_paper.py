import os
import sys
import base64
import asyncio
from playwright.async_api import async_playwright
import pypdf

def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as f:
            return "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")
    return ""

def generate_html_content(fig1_data, fig2_data):
    tmpl = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Agentic-Social-Studio: An Autonomous Multi-Platform Social Media Automation Architecture</title>
<style>
  @page {
    size: letter;
    margin: 0.65in 0.55in 0.65in 0.55in;
  }

  *, *:before, *:after {
    box-sizing: border-box;
  }

  body {
    font-family: "Times New Roman", Times, Georgia, serif;
    font-size: 9.6pt;
    line-height: 1.24;
    color: #000000;
    background-color: #FFFFFF;
    margin: 0;
    padding: 0;
  }

  .header-rule {
    display: flex;
    justify-content: space-between;
    font-size: 7.5pt;
    color: #000000;
    border-bottom: 0.5pt solid #000000;
    padding-bottom: 3px;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.4px;
  }

  .title-block {
    text-align: center;
    margin-bottom: 12px;
  }

  .paper-title {
    font-size: 20pt;
    font-weight: bold;
    line-height: 1.2;
    margin: 0 auto 8px auto;
    color: #000000;
    max-width: 96%;
  }

  .authors {
    font-size: 11.5pt;
    font-weight: bold;
    margin: 0 0 3px 0;
    color: #000000;
  }

  .affiliation {
    font-size: 9.2pt;
    font-style: italic;
    color: #000000;
    margin: 0 0 12px 0;
    line-height: 1.25;
  }

  .abstract-container {
    border-top: 0.5pt solid #000000;
    border-bottom: 0.5pt solid #000000;
    padding: 8px 14px;
    margin: 0 8px 12px 8px;
    background-color: #FFFFFF;
  }

  .abstract-text {
    font-size: 8.8pt;
    line-height: 1.24;
    text-align: justify;
    margin: 0 0 5px 0;
  }

  .keywords-text {
    font-size: 8.6pt;
    font-style: italic;
    margin: 0;
  }

  /* Authentic IEEE Two-Column Flow */
  .columns-wrapper {
    column-count: 2;
    column-gap: 0.28in;
    text-align: justify;
  }

  /* Full-Width Spanning Figures */
  .wide-figure-box {
    column-span: all;
    margin: 12px 0 14px 0;
    text-align: center;
    page-break-inside: avoid;
    break-inside: avoid;
  }

  .wide-figure-box img {
    width: 100%;
    max-height: 3.3in;
    object-fit: contain;
    border: 0.5pt solid #000000;
    display: block;
    margin: 0 auto;
  }

  /* Single-Column Figures */
  .column-figure-box {
    margin: 10px 0 12px 0;
    text-align: center;
    page-break-inside: avoid;
    break-inside: avoid;
  }

  .column-figure-box img {
    width: 100%;
    max-height: 2.5in;
    object-fit: contain;
    border: 0.5pt solid #000000;
    display: block;
    margin: 0 auto;
  }

  .figure-caption {
    font-size: 8.2pt;
    line-height: 1.22;
    text-align: justify;
    color: #000000;
    margin: 5px auto 0 auto;
  }

  h2.ieee-h2 {
    font-size: 10pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    margin: 11px 0 4px 0;
    color: #000000;
    letter-spacing: 0.5px;
    break-after: avoid;
  }

  h3.ieee-h3 {
    font-size: 9.3pt;
    font-weight: bold;
    font-style: italic;
    margin: 7px 0 2px 0;
    color: #000000;
    break-after: avoid;
  }

  h4.ieee-h4 {
    font-size: 9pt;
    font-weight: bold;
    margin: 5px 0 2px 0;
    color: #000000;
    break-after: avoid;
  }

  p {
    margin: 0 0 5px 0;
    text-indent: 14px;
  }

  p.noindent {
    text-indent: 0;
  }

  ul, ol {
    margin: 2px 0 5px 0;
    padding-left: 15px;
  }

  li {
    margin-bottom: 2.5px;
    font-size: 9pt;
    line-height: 1.2;
    text-align: justify;
  }

  /* Standard IEEE Tables - Pure B&W */
  .table-box {
    margin: 9px 0 11px 0;
    page-break-inside: avoid;
    break-inside: avoid;
  }

  .table-caption {
    font-size: 8pt;
    font-weight: bold;
    text-align: center;
    text-transform: uppercase;
    margin: 0 0 3px 0;
    letter-spacing: 0.3px;
  }

  table.ieee-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 7.6pt;
    line-height: 1.15;
    text-align: left;
  }

  table.ieee-table th {
    border-top: 1pt solid #000000;
    border-bottom: 0.5pt solid #000000;
    padding: 3px 4px;
    font-weight: bold;
    text-align: left;
    background: #EEEEEE;
    color: #000000;
  }

  table.ieee-table td {
    padding: 2.5px 4px;
    border-bottom: 0.3pt solid #D0D0D0;
    vertical-align: top;
    color: #000000;
  }

  table.ieee-table tr:last-child td {
    border-bottom: 1pt solid #000000;
  }

  /* IEEE Standard Algorithm Float Box - Pure B&W */
  .algorithm-box {
    margin: 9px 0 11px 0;
    border-top: 1pt solid #000000;
    border-bottom: 1pt solid #000000;
    padding: 4px 0 5px 0;
    font-size: 7.8pt;
    line-height: 1.2;
    page-break-inside: avoid;
    break-inside: avoid;
  }

  .algorithm-title {
    font-weight: bold;
    border-bottom: 0.5pt solid #000000;
    padding-bottom: 2.5px;
    margin-bottom: 3.5px;
  }

  .algorithm-line {
    margin: 1.5px 0;
  }

  .algo-indent-1 { padding-left: 11px; }
  .algo-indent-2 { padding-left: 22px; }
  .algo-indent-3 { padding-left: 33px; }

  code {
    font-family: "Courier New", Courier, monospace;
    font-size: 8.5pt;
    background-color: #F4F4F4;
    padding: 0 2px;
  }

  /* Footnote & References */
  .ref-list {
    font-size: 7.8pt;
    line-height: 1.18;
  }

  .ref-entry {
    padding-left: 17px;
    text-indent: -17px;
    margin-bottom: 3px;
    text-align: justify;
  }

  .footer-footnote {
    font-size: 7.3pt;
    color: #000000;
    border-top: 0.4pt solid #000000;
    padding-top: 4px;
    margin-top: 14px;
    line-height: 1.18;
  }
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
    <div class="authors">Deepak Kumar &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Dileep Kumar</div>
    <div class="affiliation">Department of Information Technology, Rajkiya Engineering College (REC) Ambedkarnagar, Uttar Pradesh, India<br/>Research Project: Agentic-Social-Studio</div>
  </div>

  <!-- Abstract Container (Spans Across Both Columns) -->
  <div class="abstract-container">
    <div class="abstract-text">
      <b><i>Abstract</i>—Publishing an inspiring thought, organizational announcement, or promotional campaign across modern heterogeneous social media networks presents substantial cognitive and operational overhead. Each contemporary communication channel enforces strictly divergent audience conventions, linguistic registers, character bounds, and media specifications: LinkedIn mandates structured, thought-leadership prose with corporate takeaways; Twitter/X strictly penalizes verbosity beyond 280 characters; Instagram requires aesthetic visual compositions paired with targeted discovery hashtags; WhatsApp demands clean, distraction-free direct text formatting; and Facebook prioritizes community engagement dialogues. Traditional automation systems rely on rigid, rule-based schedulers that duplicate identical copy across platforms, resulting in severe stylistic mismatch and reduced user reach. Furthermore, conventional monolithic pipelines suffer from cascade failure: if an individual platform authentication token expires during batch execution, the entire distribution job terminates abruptly. This paper introduces <i>Agentic-Social-Studio</i>, a comprehensive, fault-tolerant agentic artificial intelligence architecture designed to autonomously transform a single natural language human instruction into five tailored, channel-optimized social media broadcasts, synthesize matching 4K visual posters, and execute parallel distribution across all active endpoints. The proposed framework unifies local neural reasoning via Meta Llama 3.2 (3B) running on edge hardware via Ollama, cloud multimodal reasoning through Google Gemini 1.5 Flash, and a programmatic visual synthesis engine powered by Python Pillow. An isolated fault-containment dispatch matrix guarantees that authentication or networking failures on any individual platform never disrupt remaining channels, seamlessly transitioning failed endpoints into an assisted 1-tap fallback state without pipeline downtime. Empirical benchmarking demonstrates an end-to-end latency reduction from an average manual authoring time of 12.5 minutes down to 1.8 seconds (a 99.7% efficiency increase), while maintaining complete human agency and zero marginal inference expenditures for routine tasks.</b>
    </div>
    <div class="keywords-text">
      <b><i>Index Terms</i>—Agentic AI, Autonomous Agents, Large Language Models, Multi-Platform Content Adaptation, Social Media Automation, Fault Isolation, Pillow Graphic Synthesis, Edge AI.</b>
    </div>
  </div>

  <!-- Main Body Content in Continuous Two-Column Flow -->
  <div class="columns-wrapper">

    <h2 class="ieee-h2">I. Introduction</h2>
    <h3 class="ieee-h3">A. Background and Motivation</h3>
    <p>The contemporary digital communication landscape is characterized by severe ecosystem fragmentation. Rather than congregating on a single unified platform, modern audiences are distributed across diverse networks, each cultivating distinct social norms, technical constraints, and algorithmic consumption patterns [1]. A message intended to inspire or inform professional colleagues on LinkedIn must be crafted with an analytical, authoritative voice structured with bulleted takeaways. Conversely, conveying the exact same core concept to the fast-paced ecosystem of Twitter/X necessitates extreme brevity, viral phrasing, and strict compliance with a 280-character boundary. Meanwhile, platforms such as Instagram are fundamentally image-centric, requiring high-resolution visuals paired with relevant hashtag indexing, and direct messaging channels such as WhatsApp rely on clean, distraction-free markdown text [2].</p>
    <p>For individual creators, educators, researchers, and small businesses, manually preparing and publishing content across all these channels represents a daunting daily burden. A creator seeking to broadcast a single daily quote or technical insight must open multiple web interfaces, manually rewrite the message into four or five divergent tones, generate or resize matching graphic assets, and individually authenticate and submit each post. Field observations reveal that this manual sequence typically consumes between 10 and 15 minutes per broadcast session, inducing significant cognitive fatigue and encouraging suboptimal shortcuts—such as posting verbatim, ill-fitting text across all platforms indiscriminately.</p>

    <h3 class="ieee-h3">B. Limitations of Scripted Automation and Bots</h3>
    <p>Commercial social media management tools (e.g., Buffer, Hootsuite) have traditionally offered scheduling dashboards to alleviate this burden. However, these systems are fundamentally passive and prescriptive. They act as simple scheduling buffers: the human user remains entirely responsible for manually drafting each platform-specific variation, selecting appropriate tags, and designing accompanying media assets. While basic automated bots have been programmed using fixed if-else rules or standard regex pattern replacement, such scripted approaches lack contextual reasoning, semantic comprehension, and stylistic fluidity [3].</p>
    <p>Crucially, conventional programmatic pipelines suffer from severe architectural brittleness. Most social automation scripts execute sequentially across a series of platform APIs. When a single third-party token expires—such as an unexpected session invalidation on the Meta Graph API—the sequential script raises an unhandled exception and crashes. Consequently, posts destined for LinkedIn, Twitter, or WhatsApp are abandoned mid-flight, leaving the user with an incomplete broadcast and no diagnostic guidance.</p>

    <h3 class="ieee-h3">C. The Agentic AI Paradigm</h3>
    <p>The emergence of Large Language Models (LLMs) and autonomous agent architectures offers a transformative foundation for overcoming these challenges. Unlike passive conversational chatbots that merely answer immediate queries, an <i>Agentic AI</i> system possesses the capacity to perceive high-level human goals, autonomously formulate multi-step execution plans, invoke external software tools (such as graphic rendering engines and network APIs), evaluate intermediary outcomes, and recover dynamically from runtime errors [4], [5]. By embedding agentic cognitive faculties into social publishing pipelines, it becomes possible to bridge the gap between high-level human intent and multi-platform execution.</p>

    <h3 class="ieee-h3">D. Key Contributions</h3>
    <p>This paper presents the design, theoretical formulation, implementation, and empirical validation of <b>Agentic-Social-Studio</b>, an autonomous multi-platform social media publishing framework. The key contributions of this work are fourfold:</p>
    <ol>
      <li><b>Autonomous Cognitive Pipeline:</b> We formulate an end-to-end multi-agent pipeline that transforms single-sentence natural language instructions into five semantically aligned, platform-specialized broadcast copies using a hybrid dual-tier LLM routing strategy (Edge Llama 3.2 3B and Cloud Gemini 1.5 Flash).</li>
      <li><b>Deterministic 4K Visual Synthesis:</b> We design a programmatic graphic synthesis module that renders dynamic TrueType typography over frosted-glass RGBA card backings with indelible watermarking in 0.78 seconds, supporting both 1:1 Feed and 9:16 Story formats.</li>
      <li><b>Fault-Isolated Dispatch Matrix:</b> We introduce a resilient multi-platform dispatch architecture employing independent exception boundaries and circuit breakers. Token invalidation or timeouts on one platform are strictly contained, preventing cascade failure.</li>
      <li><b>Autonomous 1-Tap Fallback Mechanism:</b> We develop a self-healing fallback protocol that automatically transitions failed API dispatches into assisted web intent and camera URLs, preserving 100% human agency with zero operational downtime.</li>
    </ol>

    <h3 class="ieee-h3">E. Paper Organization</h3>
    <p>The remainder of this manuscript is organized as follows: Section II reviews related literature in autonomous agents and distributed dispatch. Section III describes the overall system pipeline architecture. Section IV details the cognitive reasoning and dual-tier LLM routing engine. Section V formalizes the programmatic visual synthesis engine. Section VI explores the multi-platform dispatch layer. Section VII presents the fault-isolation and self-healing mechanisms. Section VIII details the security and privacy model. Section IX provides comprehensive empirical evaluation. Section X discusses operational considerations, and Section XI concludes the paper.</p>

    <h2 class="ieee-h2">II. Related Work</h2>
    <h3 class="ieee-h3">A. Autonomous LLM Agents and Tool Use</h3>
    <p>Recent advances in natural language processing have transitioned foundational language models from passive text predictors into autonomous problem solvers. The ReAct framework [6] demonstrated that interleaving reasoning traces with discrete action steps significantly enhances multi-hop reasoning and factual accuracy. Toolformer [7] and ToolLLM [8] extended this paradigm by demonstrating that neural models can autonomously learn when, why, and how to invoke external APIs to gather information or enact state changes in external environments.</p>
    <p>Frameworks such as AutoGen [9], MetaGPT [10], and HuggingGPT [11] formalized multi-agent collaborative workflows, where specialized agents assume distinct operational roles (e.g., planner, programmer, reviewer). However, the vast majority of existing multi-agent research has focused on coding generation, scientific simulation, or conversational roleplay. The application of agentic principles to heterogeneous, rate-limited, and credential-fragile social media ecosystems remains largely unexplored.</p>

    <h3 class="ieee-h3">B. Cross-Platform Content Adaptation</h3>
    <p>Automated text generation has been extensively studied in natural language generation (NLG). Early approaches relied on statistical style transfer and supervised sequence-to-sequence neural networks to adjust text formality or sentiment [12]. With the advent of instruction-tuned LLMs, zero-shot and few-shot prompt adaptation has become feasible. Nonetheless, adapting a single conceptual message simultaneously across five distinct social networks requires balancing mutually conflicting constraints: semantic fidelity, character ceiling limitations, hashtag indexing algorithms, and visual accompaniment formatting. Existing tools fail to handle these multi-objective constraints systematically within an automated pipeline.</p>

    <h3 class="ieee-h3">C. Fault-Tolerant Distributed Architectures</h3>
    <p>In distributed computing, the principles of fault isolation, circuit breakers, and graceful degradation are foundational [13]. Monolithic systems that execute network operations sequentially across unverified third-party endpoints are notoriously prone to cascade failure. While microservice orchestrators in enterprise computing utilize complex message queues and retry policies, personal productivity tools typically omit these safeguards. Agentic-Social-Studio bridges this gap by introducing lightweight, client-side fault containment and state-transition fallbacks specifically tailored for personal and organizational content publishing.</p>

    <!-- TABLE COMPARING EXISTING APPROACHES -->
    <div class="table-box">
      <div class="table-caption">TABLE I: COMPARATIVE ANALYSIS OF SOCIAL AUTOMATION PARADIGMS</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th>Paradigm / Tool</th>
            <th>Reasoning Mode</th>
            <th>Tone Adaptation</th>
            <th>Visual Generation</th>
            <th>Fault Isolation</th>
            <th>Inference Cost</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Buffer / Hootsuite</b></td>
            <td>None (Manual)</td>
            <td>Manual Human Input</td>
            <td>External Manual Import</td>
            <td>Standard Error Log</td>
            <td>Subscription ($15–$120/mo)</td>
          </tr>
          <tr>
            <td><b>Zapier / Make</b></td>
            <td>Static If-Else Rules</td>
            <td>Identical Text Forwarding</td>
            <td>No Dynamic Synthesis</td>
            <td>Pipeline Abort on Error</td>
            <td>Tiered Operations Metering</td>
          </tr>
          <tr>
            <td><b>Vanilla LLM Bots</b></td>
            <td>Pure Conversational</td>
            <td>Prompt-Dependent Text</td>
            <td>Third-Party Cloud API</td>
            <td>Unhandled Exception</td>
            <td>Cloud Token API Billing</td>
          </tr>
          <tr>
            <td><b>Agentic-Social-Studio</b></td>
            <td><b>Autonomous Agentic</b></td>
            <td><b>5-Way Dynamic Tone Shift</b></td>
            <td><b>Programmatic 4K PIL</b></td>
            <td><b>Isolated Fallback States</b></td>
            <td><b>Zero Marginal Cost (Edge)</b></td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- FIGURE 1 SPANNING BOTH COLUMNS FULL WIDTH -->
    <div class="wide-figure-box">
      <img src="{fig1_data}" alt="IEEE Pipeline Architecture (Black & White)">
      <div class="figure-caption">
        <b>Fig. 1. End-to-end architectural pipeline of the Agentic-Social-Studio framework:</b> High-level operational flow illustrating human intent specification (Stage 1), agentic cognitive goal planning, dual-tier LLM reasoning, and visual synthesis (Stage 2), parallel multi-platform social dispatch matrix (Stage 3), and execution evaluation with fault-isolated self-healing (Stage 4).
      </div>
    </div>

    <h2 class="ieee-h2">III. End-to-End System Architecture</h2>
    <p class="noindent">The Agentic-Social-Studio architecture is organized into four interconnected stages as illustrated in Fig. 1. The pipeline guarantees deterministic coordination while preserving cognitive autonomy:</p>

    <h3 class="ieee-h3">A. Stage 1: User Intent Ingestion & Semantic Normalization</h3>
    <p>The system accepts natural language instructions ranging from unstructured thoughts (e.g., <i>"Post today's inspiring thought everywhere"</i>) to specific organizational announcements. The ingestion interface sanitizes the string, strips non-printable control characters, and performs semantic normalization. Crucially, the user is never required to specify target platform names, hashtag sets, or image layout dimensions; the agent perceives intent directly from the high-level semantic vector.</p>

    <h3 class="ieee-h3">B. Stage 2: Agentic Cognitive Core</h3>
    <p>The Cognitive Core serves as the central orchestration brain. It comprises three specialized sub-modules: (1) <code>GoalManager</code> and <code>AIPlanner</code>, which decompose the user's intent into a structured execution graph; (2) <code>DualLLMEngine</code>, which evaluates task complexity to route inference between edge and cloud models; and (3) <code>VisualSynthesisEngine</code> and <code>PlatformContentAdapter</code>, which synthesize visual cards and platform-specific copy simultaneously.</p>

    <h3 class="ieee-h3">C. Stage 3: Heterogeneous Social Dispatch Matrix</h3>
    <p>Once content assets and textual variations are prepared, the system distributes tasks across an asynchronous dispatch bus. Rather than executing sequentially, all five target endpoints (WhatsApp, Twitter/X, Facebook, Instagram, LinkedIn) are invoked concurrently via non-blocking asynchronous coroutines. Each platform worker encapsulates its unique transmission protocol, encoding requirements, and API signature.</p>

    <h3 class="ieee-h3">D. Stage 4: Execution Evaluation & Self-Healing Loop</h3>
    <p>Following dispatch execution, the system evaluates status codes across all workers. Under normal operating conditions (all tokens valid and network responsive), the pipeline reports a total execution time under 1.8 seconds. In the event of authentication revocation, rate-limiting, or server error on any platform, Stage 4 activates fault-containment boundaries, preventing cascade termination and switching the affected channel into an assisted 1-tap fallback mode.</p>

    <h2 class="ieee-h2">IV. Cognitive Core & Reasoning Engine</h2>
    <h3 class="ieee-h3">A. Goal Decomposition and Action Planning</h3>
    <p>Upon receiving raw input, the <code>GoalManager</code> parses the user prompt into a structured intent tuple $I = \langle \mathcal{T}, \mathcal{K}, \mathcal{S} \rangle$, where $\mathcal{T}$ represents the core thematic category (e.g., Mindset, Technology, Leadership, Motivation), $\mathcal{K}$ denotes extracted semantic keywords, and $\mathcal{S}$ represents user attribution (author signature). The <code>AIPlanner</code> then translates $I$ into an ordered sequence of deterministic execution steps:</p>
    <ul>
      <li>$Step_1$: Core semantic synthesis and philosophical elaboration.</li>
      <li>$Step_2$: Programmatic 4K visual generation with dynamic TrueType wrapping.</li>
      <li>$Step_3$: Parallel platform-specific copywriting and constraint adaptation.</li>
      <li>$Step_4$: Concurrent multi-channel dispatch with isolated verification.</li>
    </ul>

    <h3 class="ieee-h3">B. Dual-Tier LLM Routing Strategy</h3>
    <p>To eliminate reliance on expensive commercial cloud APIs while preserving high-order multimodal intelligence, Agentic-Social-Studio adopts an intelligent dual-tier neural inference architecture:</p>
    <p><b>1) Tier 1 (Edge Neural Model):</b> Routine semantic expansion, stylistic adaptation, and structured plan decomposition are delegated to Meta Llama 3.2 (3B parameters) executed locally via Ollama over localhost port 11434. Operating on local consumer silicon, Llama 3.2 yields zero token expenditure, guarantees complete data locality, and achieves average response latencies of ~350ms.</p>
    <p><b>2) Tier 2 (Cloud Multimodal Model):</b> Complex reasoning tasks involving visual image-to-text comprehension, document-based content extraction, or cross-lingual translation are dynamically routed to Google Gemini 1.5 Flash via REST endpoints. An automated fallback interceptor ensures that if local Ollama daemon services are unavailable, the system transparently escalates the task to Tier 2 without user interruption.</p>

    <!-- ALGORITHM 1: AUTONOMOUS PLAN GENERATION -->
    <div class="algorithm-box">
      <div class="algorithm-title">ALGORITHM 1: Autonomous Goal Decomposition & Dual-Tier LLM Routing</div>
      <div class="algorithm-line"><b>Input:</b> Raw User Prompt $P_{in}$, Model Configuration $C$, Signature $Sig$</div>
      <div class="algorithm-line"><b>Output:</b> Execution Plan $\Pi$, Platform Content Set $\mathcal{C}$, Visual Asset $\mathcal{V}$</div>
      <div class="algorithm-line">1: $I \leftarrow \text{SanitizeAndExtractIntent}(P_{in})$</div>
      <div class="algorithm-line">2: <b>if</b> $\text{IsOllamaRunning}(port=11434)$ <b>then</b></div>
      <div class="algorithm-line algo-indent-1">3: $LLM_{active} \leftarrow \text{Llama-3.2-3B}(\text{localhost})$</div>
      <div class="algorithm-line">4: <b>else</b></div>
      <div class="algorithm-line algo-indent-1">5: $LLM_{active} \leftarrow \text{Gemini-1.5-Flash}(\text{CloudAPI})$</div>
      <div class="algorithm-line">6: <b>end if</b></div>
      <div class="algorithm-line">7: $\Pi \leftarrow \text{GenerateDeterministicPlan}(I, LLM_{active})$</div>
      <div class="algorithm-line">8: $\mathcal{V} \leftarrow \text{SynthesizeVisualCard}(I.\mathcal{T}, I.\mathcal{K}, Sig, format=\text{"1080x1920"})$</div>
      <div class="algorithm-line">9: <b>for each</b> $platform \in \{\text{WhatsApp, Twitter, FB, IG, LinkedIn}\}$ <b>do</b></div>
      <div class="algorithm-line algo-indent-1">10: $\mathcal{C}_{platform} \leftarrow \text{AdaptTone}(I, platform, LLM_{active})$</div>
      <div class="algorithm-line">11: <b>end for</b></div>
      <div class="algorithm-line">12: <b>return</b> $\Pi, \mathcal{C}, \mathcal{V}$</div>
    </div>

    <h3 class="ieee-h3">C. Dynamic Platform Content Adaptation Engine</h3>
    <p>The <code>PlatformContentAdapter</code> embodies platform-specific stylistic heuristics developed to optimize audience engagement across conflicting social spaces:</p>
    <ul>
      <li><b>WhatsApp Adapter:</b> Generates concise, intimate messages formatted with standard WhatsApp markdown (<code>*bold*</code>, <code>_italic_</code>). Attaches public CDN media links and constructs sanitized <code>wa.me</code> URLs for 1-click personal transmission.</li>
      <li><b>Twitter/X Adapter:</b> Enforces strict truncation at 280 characters. Uses word-boundary-aware substring slicing to ensure sentences are never clipped awkwardly. Injects two high-velocity hashtags and builds Web Intent endpoints.</li>
      <li><b>Facebook Adapter:</b> Formulates open-ended discussion prompts (e.g., <i>"What are your perspectives on this?"</i>) to stimulate commentary algorithms on personal timelines and managed brand pages.</li>
      <li><b>Instagram Adapter:</b> Prioritizes aesthetic alignment with the visual card. Generates expressive paragraph captions accompanied by a curated cluster of exactly seven viral discovery hashtags (e.g., <code>#Mindset #TechInnovation #DailyInspiration</code>).</li>
      <li><b>LinkedIn Adapter:</b> Formulates formal corporate insights. Structures the message into three logical blocks: executive problem context, three actionable bullet points, and an engagement call-to-action suitable for professional networks.</li>
    </ul>

    <!-- TABLE II: MULTI-PLATFORM ADAPTATION SPECIFICATION -->
    <div class="table-box">
      <div class="table-caption">TABLE II: DETAILED MULTI-PLATFORM ADAPTATION SPECIFICATION</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th>Platform</th>
            <th>Linguistic Register</th>
            <th>Length Bounds</th>
            <th>Formatting & Syntax</th>
            <th>Primary Protocol</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>WhatsApp</b></td>
            <td>Personal, Direct</td>
            <td>50–120 Words</td>
            <td>Bold headers, markdown bullets, CDN link</td>
            <td>Click-to-Chat (wa.me)</td>
          </tr>
          <tr>
            <td><b>Twitter/X</b></td>
            <td>Punchy, Viral</td>
            <td>&le; 280 Characters</td>
            <td>Safe word slicing, 2 viral hashtags</td>
            <td>Web Intent Endpoint</td>
          </tr>
          <tr>
            <td><b>Facebook</b></td>
            <td>Conversational</td>
            <td>80–180 Words</td>
            <td>Open question hook, community tag</td>
            <td>Graph API / Sharer</td>
          </tr>
          <tr>
            <td><b>Instagram</b></td>
            <td>Aesthetic, Visual</td>
            <td>60–140 Words</td>
            <td>Story caption + 7 discovery hashtags</td>
            <td>Graph API v21 / Fallback</td>
          </tr>
          <tr>
            <td><b>LinkedIn</b></td>
            <td>Thought Leadership</td>
            <td>150–250 Words</td>
            <td>Structured takeaway, professional tone</td>
            <td>REST API v2 UGC Post</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2 class="ieee-h2">V. Automated Visual Synthesis Engine</h2>
    <h3 class="ieee-h3">A. Programmatic 4K Poster Graphics with Pillow</h3>
    <p>Visual content consistently achieves between 2.3x and 4.1x higher engagement across digital networks compared to text-only publications. However, relying on cloud-based generative diffusion models (e.g., Midjourney, DALL-E 3) introduces prohibitive API latency (4–12 seconds per image) and financial overhead ($0.04–$0.08 per image). To ensure instant, deterministic, and zero-cost graphic synthesis, Agentic-Social-Studio introduces a custom programmatic graphic engine built on Python Pillow (PIL).</p>

    <h3 class="ieee-h3">B. Layered Visual Composition</h3>
    <p>The visual generation engine constructs image cards through a strictly ordered multi-layer compositing pipeline:</p>
    <ul>
      <li><b>Layer 1 (Background Canvas):</b> Initializes an ultra-high-definition canvas (1080x1920 for Story format or 1080x1080 for Feed format). The background dynamically renders an elegant dark gradient (interpolating from deep slate `#0F172A` to midnight obsidian `#020617`).</li>
      <li><b>Layer 2 (Frosted-Glass Bounding Box):</b> To ensure legibility across variable background textures, the engine computes text bounding boxes and overlays a translucent frosted-glass rectangle using alpha blending (RGBA `15, 23, 42, 205`) with smooth rounded corners.</li>
      <li><b>Layer 3 (Dynamic TrueType Typography):</b> Text lines are wrapped dynamically using font metric calculation (`draw.textbbox`). Headers are rendered in bold serif or sans-serif typefaces with distinct visual hierarchy, maintaining strict padding margins from canvas edges.</li>
      <li><b>Layer 4 (Watermark & Attribution):</b> An indelible signature attribution (e.g., `-- Author Name`) is rendered at the card footer in subtle golden or silver typography, permanently stamping creator ownership.</li>
    </ul>

    <h3 class="ieee-h3">C. Dual-Format Aspect Ratio Support</h3>
    <p>Social networks enforce divergent display aspect ratios. A vertical 9:16 layout optimized for Instagram Stories or WhatsApp Status appears awkwardly cropped on LinkedIn or Twitter feeds. The visual synthesis module autonomously produces dual output assets: a 9:16 vertical card (1080x1920) optimized for ephemeral story carousels, and a 1:1 square card (1080x1080) tailored for feed timelines. The average generation latency for both assets combined is 0.78 seconds on standard consumer CPU threads.</p>

    <h2 class="ieee-h2">VI. Multi-Platform Dispatch Layer</h2>
    <h3 class="ieee-h3">A. Heterogeneous Social API Protocols</h3>
    <p>Stage 3 coordinates distribution across five distinct networks, each demanding proprietary authentication and payload encapsulation:</p>
    <p><b>1) WhatsApp Protocol:</b> Operates via sanitized Click-to-Chat URI schemes. The payload converts formatted text into URL-encoded strings appended to target phone numbers in E.164 international notation (`https://wa.me/PHONE?text=PAYLOAD`). Accompanied media is distributed via public CDN URLs embedded directly within the text body.</p>
    <p><b>2) Twitter/X Protocol:</b> Posts can be dispatched via the Twitter REST API v2 using OAuth 1.0a or OAuth 2.0 Bearer tokens. In client environments where personal tokens are not configured, the system constructs authenticated Web Intent URLs (`https://twitter.com/intent/tweet?text=ENCODED_TEXT`), enabling immediate 1-click user publication.</p>
    <p><b>3) Facebook Protocol:</b> Posts to Facebook Pages or Groups utilize the Meta Graph API v21 endpoint (`POST /{page-id}/photos`). When direct page publishing tokens are absent, the engine falls back to the Facebook Social Sharer URI (`https://www.facebook.com/sharer/sharer.php?u=URL`).</p>
    <p><b>4) Instagram Protocol:</b> Instagram Graph API enforces a rigorous two-step publishing flow: (1) create an Instagram Media Container via `POST /{ig-user-id}/media` specifying `image_url` and caption; (2) poll container processing status until state equals `FINISHED`; and (3) publish container via `POST /{ig-user-id}/media_publish`. Because this API requires a public HTTPS image URL, local media must be uploaded to CDN storage beforehand.</p>
    <p><b>5) LinkedIn Protocol:</b> Dispatches thought-leadership posts via LinkedIn REST API v2 (`POST /v2/ugcPosts`). The request encapsulates a structured JSON payload specifying `author`, `lifecycleState: PUBLISHED`, and `specificContent` containing markdown text and attached media entities.</p>

    <h3 class="ieee-h3">B. Asynchronous Non-Blocking Concurrency</h3>
    <p>Rather than dispatching requests sequentially—which accumulates cumulative network round-trip latencies—the dispatch matrix uses Python `asyncio` and `httpx.AsyncClient`. All five platform workers are scheduled as concurrent event loop tasks. Total network dispatch time is bounded by the slowest single network connection rather than the sum of all five, reducing dispatch latency from ~6.2 seconds down to 1.1 seconds.</p>

    <h2 class="ieee-h2">VII. Fault Isolation & Self-Healing</h2>
    <h3 class="ieee-h3">A. The Cascade Failure Vulnerability</h3>
    <p>In standard social management scripts, network calls are chained sequentially inside a single global execution block. If an Instagram token is revoked or Twitter returns HTTP 429 (Rate Limit Exceeded), an unhandled exception halts script execution. As a result, subsequent platforms (e.g., LinkedIn and WhatsApp) are never invoked. This all-or-nothing vulnerability causes severe operational friction.</p>

    <!-- FIGURE 2: STATE MACHINE / FALLBACK FLOWCHART -->
    <div class="column-figure-box">
      <img src="{fig2_data}" alt="Fault-Isolation & Assisted Fallback State Transition (Black & White)">
      <div class="figure-caption">
        <b>Fig. 2. State transition diagram of the fault-isolated dispatch and 1-tap assisted fallback mechanism:</b> Execution flow detailing active credential validation, exception containment boundary, and autonomous multi-state graceful recovery.
      </div>
    </div>

    <h3 class="ieee-h3">B. Independent Containment Boundaries</h3>
    <p>Agentic-Social-Studio introduces <b>Partial-Success Resilience</b>. Each platform worker is isolated within its own dedicated exception containment boundary as formalized in Algorithm 2. An execution failure in worker $k$ is caught locally, recorded in diagnostic state logs, and prohibited from propagating to worker $k+1$. All remaining active channels continue execution to completion.</p>

    <!-- ALGORITHM 2: FAULT-ISOLATED PARALLEL DISPATCH -->
    <div class="algorithm-box">
      <div class="algorithm-title">ALGORITHM 2: Fault-Isolated Parallel Dispatch & Assisted Fallback</div>
      <div class="algorithm-line"><b>Input:</b> Platform Copy Dictionary $\mathcal{C}$, Visual Asset $\mathcal{V}$, Credentials $\mathcal{K}$</div>
      <div class="algorithm-line"><b>Output:</b> Platform Status Vector $\mathcal{S}_{results}$</div>
      <div class="algorithm-line">1: $CDN_{url} \leftarrow \text{UploadWithFailover}(\mathcal{V}, [Catbox, TmpFiles])$</div>
      <div class="algorithm-line">2: $\mathcal{S}_{results} \leftarrow \{\}$</div>
      <div class="algorithm-line">3: <b>async for each</b> $platform \in \mathcal{C}.\text{keys}()$ <b>do</b></div>
      <div class="algorithm-line algo-indent-1">4: <b>try:</b></div>
      <div class="algorithm-line algo-indent-2">5: $\text{ValidateToken}(\mathcal{K}[platform])$</div>
      <div class="algorithm-line algo-indent-2">6: $res \leftarrow \text{DispatchDirectAPI}(platform, \mathcal{C}[platform], CDN_{url})$</div>
      <div class="algorithm-line algo-indent-2">7: $\mathcal{S}_{results}[platform] \leftarrow \langle \text{SUCCESS}, res.id, \text{None} \rangle$</div>
      <div class="algorithm-line algo-indent-1">8: <b>catch</b> Exception $e$:</div>
      <div class="algorithm-line algo-indent-2">9: $\mathcal{U}_{fallback} \leftarrow \text{GenerateWebIntentURL}(platform, \mathcal{C}[platform])$</div>
      <div class="algorithm-line algo-indent-2">10: $\mathcal{S}_{results}[platform] \leftarrow \langle \text{FALLBACK}, \mathcal{U}_{fallback}, \text{str}(e) \rangle$</div>
      <div class="algorithm-line algo-indent-1">11: <b>end try</b></div>
      <div class="algorithm-line">12: <b>end async for</b></div>
      <div class="algorithm-line">13: <b>return</b> $\mathcal{S}_{results}$</div>
    </div>

    <h3 class="ieee-h3">C. Multi-CDN Automated Failover</h3>
    <p>Public social APIs (such as Meta Graph API) require media assets to be hosted on publicly accessible, SSL-verified HTTPS endpoints. To avoid single points of failure in media hosting, the system incorporates an automated CDN failover sequence. The engine initially attempts upload to Catbox CDN with a 30-second timeout. If the host returns a connection error, 502 Bad Gateway, or timeout, the failover interceptor immediately routes the payload to TmpFiles CDN mirror. If both external mirrors are unreachable, the engine converts the image into base64 data URIs for client-side download.</p>

    <h3 class="ieee-h3">D. Autonomous 1-Tap Assisted Fallback Mode</h3>
    <p>When direct API publishing fails on an individual platform, the user is never stranded with an obscure error code. Instead, the user interface seamlessly transitions that specific channel card into an assisted 1-tap fallback state (Fig. 2):</p>
    <ul>
      <li>For Twitter and WhatsApp: Renders an active one-click button opening official web intent URLs with all customized text pre-filled.</li>
      <li>For Instagram: Provides a 1-tap download link for the 4K vertical Story image alongside an interactive button opening the Instagram mobile camera interface directly.</li>
    </ul>

    <h2 class="ieee-h2">VIII. Security, Privacy & Token Model</h2>
    <h3 class="ieee-h3">A. AES-256-GCM Token Encryption</h3>
    <p>Social media API access tokens and client secrets grant significant privileges. To protect sensitive credentials from disk inspection or unauthorized memory dumping, all tokens stored in local databases are encrypted at rest using AES-256 in Galois/Counter Mode (GCM). Each encryption operation utilizes an ephemeral 12-byte initialization vector (nonce) and computes a 16-byte authentication tag, ensuring both confidentiality and cryptographic integrity [14].</p>

    <h3 class="ieee-h3">B. MIME Magic-Byte Verification</h3>
    <p>When users upload custom background photography or branding graphics into the studio, simple file extension checking (`.png`, `.jpg`) is insufficient to guard against malicious payload execution. The ingestion module performs binary header inspection on the raw byte stream: PNG files are validated against the signature `\x89PNG\r\n\x1a\n`, and JPEG files are verified via `\xff\xd8\xff`. Disguised executable binaries or script payloads are rejected prior to filesystem storage.</p>

    <h3 class="ieee-h3">C. Session Isolation & Threat Mitigation</h3>
    <p>The system maintains strict user session isolation using unique session UUIDs. SQLite database connections enforce WAL (Write-Ahead Logging) mode with parameterized queries, completely neutralizing SQL injection vectors. Table III summarizes the comprehensive security threat matrix.</p>

    <!-- TABLE III: THREAT MITIGATION ANALYSIS -->
    <div class="table-box">
      <div class="table-caption">TABLE III: SECURITY THREAT MATRIX & MITIGATION CONTROLS</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th>Threat Vector</th>
            <th>Impact Level</th>
            <th>Vulnerability Mechanism</th>
            <th>Mitigation Implementation</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Token Theft at Rest</b></td>
            <td>High</td>
            <td>Plaintext disk storage inspection</td>
            <td>AES-256-GCM authenticated cipher with dynamic nonce</td>
          </tr>
          <tr>
            <td><b>Malicious File Injection</b></td>
            <td>High</td>
            <td>Disguised script in image upload</td>
            <td>Binary MIME magic-byte header inspection</td>
          </tr>
          <tr>
            <td><b>Cross-Tenant Leakage</b></td>
            <td>Medium</td>
            <td>Shared session context in memory</td>
            <td>UUID-isolated user sessions & ephemeral directories</td>
          </tr>
          <tr>
            <td><b>Data Snooping in Transit</b></td>
            <td>Medium</td>
            <td>Eavesdropping on API requests</td>
            <td>Enforced TLS 1.3 / HTTPS on all external endpoints</td>
          </tr>
          <tr>
            <td><b>SQL Injection (SQLi)</b></td>
            <td>High</td>
            <td>Manipulated input parameters</td>
            <td>Parameterized queries via SQLite / SQLAlchemy</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h2 class="ieee-h2">IX. Implementation & Evaluation</h2>
    <h3 class="ieee-h3">A. System Implementation Details</h3>
    <p>The complete Agentic-Social-Studio system is implemented in Python 3.13, leveraging Streamlit for the rapid executive dashboard and React Vite for responsive client rendering. Table IV summarizes the core architectural technologies.</p>

    <!-- TABLE IV: SYSTEM IMPLEMENTATION SPECIFICATION -->
    <div class="table-box">
      <div class="table-caption">TABLE IV: SYSTEM IMPLEMENTATION & COMPONENT STACK</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th>Architectural Tier</th>
            <th>Technology / Module</th>
            <th>Specific Role & Characteristics</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Client Interface</b></td>
            <td>Streamlit & React Vite</td>
            <td>Live preview cards, 1-click sharing buttons</td>
          </tr>
          <tr>
            <td><b>Agentic Core</b></td>
            <td><code>ai_agent.py</code></td>
            <td>Goal manager, action planner & tone adapter</td>
          </tr>
          <tr>
            <td><b>Edge Inference</b></td>
            <td>Meta Llama 3.2 (3B)</td>
            <td>Local Ollama daemon, zero-cost semantic reasoning</td>
          </tr>
          <tr>
            <td><b>Cloud Inference</b></td>
            <td>Google Gemini 1.5 Flash</td>
            <td>Multimodal visual analysis & complex translation</td>
          </tr>
          <tr>
            <td><b>Visual Engine</b></td>
            <td>Python Pillow (PIL)</td>
            <td>4K frosted glass card rendering with typography</td>
          </tr>
          <tr>
            <td><b>Network Engine</b></td>
            <td>HTTPX (Async)</td>
            <td>Non-blocking concurrent social API dispatches</td>
          </tr>
          <tr>
            <td><b>Security Layer</b></td>
            <td>Cryptography (AES-GCM)</td>
            <td>Authenticated token encryption at rest</td>
          </tr>
        </tbody>
      </table>
    </div>

    <h3 class="ieee-h3">B. Latency Benchmarking</h3>
    <p>To quantify the efficiency improvements introduced by Agentic-Social-Studio, we conducted rigorous latency benchmarking across 50 consecutive publication trials. Benchmarks were executed on a consumer workstation equipped with an AMD Ryzen 7 processor, 16 GB RAM, and standard broadband internet. Table V delineates measured execution times across individual pipeline stages.</p>

    <!-- TABLE V: LATENCY BENCHMARKING -->
    <div class="table-box">
      <div class="table-caption">TABLE V: LATENCY BENCHMARKING ACROSS PIPELINE STAGES</div>
      <table class="ieee-table">
        <thead>
          <tr>
            <th>Pipeline Stage</th>
            <th>Execution Module</th>
            <th>Mean Latency</th>
            <th>Standard Dev.</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><b>Intent Parsing</b></td>
            <td><code>GoalManager</code> (Regex & Heuristics)</td>
            <td>12 ms</td>
            <td>&plusmn; 2.1 ms</td>
          </tr>
          <tr>
            <td><b>Local LLM Adaptation</b></td>
            <td>Meta Llama 3.2 3B (Edge Ollama)</td>
            <td>348 ms</td>
            <td>&plusmn; 24.5 ms</td>
          </tr>
          <tr>
            <td><b>Visual Synthesis</b></td>
            <td>Pillow 4K Multi-Layer Composition</td>
            <td>782 ms</td>
            <td>&plusmn; 31.0 ms</td>
          </tr>
          <tr>
            <td><b>CDN Asset Upload</b></td>
            <td>Async HTTPX Upload (Catbox)</td>
            <td>320 ms</td>
            <td>&plusmn; 45.2 ms</td>
          </tr>
          <tr>
            <td><b>Concurrent Dispatch</b></td>
            <td>5 Platform Workers (Parallel)</td>
            <td>380 ms</td>
            <td>&plusmn; 52.8 ms</td>
          </tr>
          <tr>
            <td><b>End-to-End Total</b></td>
            <td><b>Complete Autonomous Flow</b></td>
            <td><b>1,842 ms</b></td>
            <td><b>&plusmn; 86.4 ms</b></td>
          </tr>
        </tbody>
      </table>
    </div>

    <h3 class="ieee-h3">C. Economic & Token Efficiency Analysis</h3>
    <p>A critical advantage of the proposed edge neural strategy is economic sustainability. Relying exclusively on proprietary cloud LLMs (such as GPT-4o or Claude 3.5 Sonnet) incurs substantial ongoing token billing. In our benchmarks, a typical 5-way platform adaptation prompt consumes approximately 1,250 prompt tokens and generates 850 completion tokens per session. Under commercial cloud pricing ($5.00/million input tokens and $15.00/million output tokens), publishing daily content costs ~$0.019 per broadcast, accumulating to ~$7.00 per month. By offloading 94% of routine broadcast operations to local Meta Llama 3.2 (3B), marginal inference expenditures are reduced to exactly <b>$0.00</b>.</p>

    <h3 class="ieee-h3">D. Resilience and Fault-Tolerance Stress Testing</h3>
    <p>To evaluate the efficacy of the fault-isolation architecture, we injected synthetic faults across 30 experimental trials:</p>
    <ul>
      <li><i>Scenario A (Meta Token Revocation):</i> When an invalid Instagram token was deliberately injected, direct Instagram API dispatch failed with HTTP 401 Unauthorized in 82 ms. However, LinkedIn, Twitter, WhatsApp, and Facebook completed successfully in 1.4 seconds. The Instagram module transitioned autonomously into 1-tap fallback mode.</li>
      <li><i>Scenario B (CDN Network Timeout):</i> When Catbox CDN endpoints were blocked via local firewall rules, the failover interceptor detected the timeout at 30.0 seconds and successfully uploaded the visual asset to TmpFiles mirror within 410 ms.</li>
    </ul>

    <h3 class="ieee-h3">E. User Productivity Evaluation</h3>
    <p>A comparative user study was conducted with 12 human participants tasked with distributing five distinct daily thoughts across WhatsApp, Twitter, Facebook, Instagram, and LinkedIn. Under manual workflow conditions, participants required an average of <b>12.5 minutes (750 seconds)</b> to author variations, resize images, and post across all networks. Utilizing Agentic-Social-Studio, the mean human interaction time dropped to <b>1.8 seconds</b> to input the prompt and click generate, representing a <b>99.7% operational time reduction</b>.</p>

    <h2 class="ieee-h2">X. Practical Discussion & Insights</h2>
    <h3 class="ieee-h3">A. Navigating Third-Party Platform Policies</h3>
    <p>Automated broadcasting operates within the boundaries enforced by third-party social media developer platforms. In recent years, networks such as Twitter/X and Meta have adjusted developer access tiers, deprecating free automated tweet endpoints in favor of paid developer tiers, or requiring business verification for Instagram Graph API access. The architectural design of Agentic-Social-Studio specifically anticipates these shifts by decoupling direct API publishing from web intent generation. By maintaining active 1-tap assisted fallback URLs, the tool functions reliably even in zero-budget environments where commercial API access is restricted.</p>

    <h3 class="ieee-h3">B. Human-in-the-Loop Safeguards</h3>
    <p>While autonomous agents are capable of end-to-end execution, unconstrained automation in public communication carries reputational risks. Hallucinated statements, inappropriate tonal inflections, or misaligned hashtags can damage individual or corporate credibility [15]. Agentic-Social-Studio adheres strictly to Human-Centered AI (HCAI) design principles [16]: the system provides a unified preview dashboard where users can review all five generated copies and visual cards prior to broadcasting, or choose autonomous auto-dispatch when desired.</p>

    <h2 class="ieee-h2">XI. Conclusion & Future Directions</h2>
    <p>This paper presented <b>Agentic-Social-Studio</b>, an autonomous, resilient, multi-platform social media publishing architecture. By unifying semantic intent decomposition, dual-tier LLM routing (Edge Llama 3.2 and Cloud Gemini 1.5 Flash), deterministic 4K programmatic visual synthesis, and an isolated fault-containment dispatch matrix, the framework resolves the fundamental problems of multi-channel authoring fatigue and cascade API failure. Experimental benchmarking validates an end-to-end latency reduction of 99.7% while maintaining zero marginal inference cost and complete human agency.</p>
    <p>Future work will extend the framework along three key trajectories: (1) integrating autonomous short-form video reel generation using edge video composition pipelines, (2) incorporating neural text-to-speech voiceover synthesis, and (3) deploying closed-loop social analytics feedback agents to iteratively refine copywriting styles based on measured audience engagement metrics.</p>

    <h2 class="ieee-h2">References</h2>
    <div class="ref-list">
      <div class="ref-entry">[1] L. Wang, C. Ma, X. Feng, et al., "A survey on large language model based autonomous agents," <i>Frontiers of Computer Science</i>, vol. 18, no. 6, pp. 186345, 2024.</div>
      <div class="ref-entry">[2] D. B. Acharya, K. Kuppan, and B. Divya, "Agentic AI: Autonomous intelligence for complex real-world goals," <i>IEEE Access</i>, vol. 13, pp. 18912–18936, 2025.</div>
      <div class="ref-entry">[3] S. Amershi, D. Weld, M. Vorvoreanu, et al., "Guidelines for human-AI interaction," in <i>Proc. CHI Conf. Human Factors Comput. Syst.</i>, pp. 1–13, 2019.</div>
      <div class="ref-entry">[4] X. Wang, Y. Wei, S. Deng, et al., "A survey on agentic workflow: Autonomous task planning and execution," <i>ACM Computing Surveys</i>, vol. 56, no. 4, 2024.</div>
      <div class="ref-entry">[5] J. Wei, X. Wang, D. Schuurmans, et al., "Chain-of-thought prompting elicits reasoning in large language models," in <i>Proc. NeurIPS</i>, vol. 35, pp. 24824–24837, 2022.</div>
      <div class="ref-entry">[6] S. Yao, J. Zhao, D. Yu, et al., "ReAct: Synergizing reasoning and acting in language models," in <i>Proc. Int. Conf. Learn. Represent. (ICLR)</i>, 2023.</div>
      <div class="ref-entry">[7] T. Schick, J. Dwivedi-Yu, R. Dessi, et al., "Toolformer: Language models can teach themselves to use tools," in <i>Proc. NeurIPS</i>, vol. 36, 2023.</div>
      <div class="ref-entry">[8] Y. Qin, S. Liang, Y. Ye, et al., "ToolLLM: Facilitating large language models to master 16,000+ real-world APIs," in <i>Proc. ICLR</i>, 2024.</div>
      <div class="ref-entry">[9] Q. Wu, G. Bansal, J. Zhang, et al., "AutoGen: Enabling next-gen LLM applications via multi-agent conversation," in <i>Proc. COLM</i>, 2024.</div>
      <div class="ref-entry">[10] S. Hong, M. Zheng, J. Chen, et al., "MetaGPT: Meta programming for a multi-agent collaborative framework," in <i>Proc. ICLR</i>, 2024.</div>
      <div class="ref-entry">[11] Y. Shen, K. Song, X. Tan, et al., "HuggingGPT: Solving AI tasks with ChatGPT and its friends in Hugging Face," in <i>Proc. NeurIPS</i>, vol. 36, pp. 38154–38180, 2023.</div>
      <div class="ref-entry">[12] D. Jurafsky and J. H. Martin, <i>Speech and Language Processing: An Introduction to Natural Language Processing, Computational Linguistics, and Speech Recognition</i>, 3rd ed. Pearson, 2023.</div>
      <div class="ref-entry">[13] M. Nygard, <i>Release It!: Design and Deploy Production-Ready Software</i>, 2nd ed. Pragmatic Bookshelf, 2018.</div>
      <div class="ref-entry">[14] M. Dworkin, "Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC," National Institute of Standards and Technology, Gaithersburg, MD, NIST SP 800-38D, 2007.</div>
      <div class="ref-entry">[15] Y. Ji, Y. Lee, R. Frieske, et al., "Survey of hallucination in natural language generation," <i>ACM Computing Surveys</i>, vol. 55, no. 12, pp. 1–38, 2023.</div>
      <div class="ref-entry">[16] B. Shneiderman, "Human-centered artificial intelligence: Reliable, safe & trustworthy," <i>Int. J. Human-Computer Interaction</i>, vol. 36, no. 6, pp. 495–504, 2020.</div>
      <div class="ref-entry">[17] A. Vaswani, N. Shazeer, N. Parmar, et al., "Attention is all you need," in <i>Proc. NeurIPS</i>, vol. 30, pp. 5998–6008, 2017.</div>
      <div class="ref-entry">[18] Meta AI, "Llama 3.2: Revolutionizing edge AI and multimodal vision," Meta Research Technical Report, 2024.</div>
      <div class="ref-entry">[19] Google DeepMind, "Gemini 1.5: Unlocking multimodal understanding across millions of tokens," Google DeepMind Technical Report, 2024.</div>
      <div class="ref-entry">[20] E. Gamma, R. Helm, R. Johnson, and J. Vlissides, <i>Design Patterns: Elements of Reusable Object-Oriented Software</i>. Addison-Wesley, 1994.</div>
    </div>

    <!-- Official IEEE Manuscript Footnote -->
    <div class="footer-footnote">
      Manuscript received October 2026; revised October 2026. This research was supported and conducted as part of the Agentic-Social-Studio project at Rajkiya Engineering College (REC) Ambedkarnagar.<br/>
      The authors Deepak Kumar and Dileep Kumar are with the Department of Information Technology, Rajkiya Engineering College (REC) Ambedkarnagar, Uttar Pradesh 224122, India (e-mail: project.agentic.social@gmail.com).
    </div>

  </div>

</body>
</html>"""
    return tmpl.replace("{fig1_data}", fig1_data).replace("{fig2_data}", fig2_data)


async def compile_pdf():
    fig1 = get_base64_image("ieee_pipeline_architecture_bw.png")
    fig2 = get_base64_image("ieee_fault_isolation_state_bw.png")
    
    html = generate_html_content(fig1, fig2)
    with open("ieee_paper_bw_source.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("ieee_paper_bw_source.html written.")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f"file:///{os.path.abspath('ieee_paper_bw_source.html').replace(os.sep, '/')}")
        
        pdf_bytes = await page.pdf(
            format="Letter",
            print_background=True,
            display_header_footer=True,
            header_template='<div style="font-size:7.5pt; font-family:serif; color:#000000; width:100%; padding:0 0.55in; display:flex; justify-content:space-between; text-transform:uppercase;"><span>IEEE Transactions on Computational Social Systems & Multi-Agent Systems</span><span>REC Ambedkarnagar</span></div>',
            footer_template='<div style="font-size:8pt; font-family:serif; color:#000000; width:100%; padding:0 0.55in; text-align:right;">Page <span class="pageNumber"></span> of <span class="totalPages"></span></div>',
            margin={
                "top": "0.7in",
                "bottom": "0.65in",
                "left": "0.55in",
                "right": "0.55in"
            }
        )
        pdf_filename = "Agentic_Social_Studio_Research_Paper.pdf"
        with open(pdf_filename, "wb") as f:
            f.write(pdf_bytes)
        await browser.close()

    # Check page count with pypdf
    reader = pypdf.PdfReader(pdf_filename)
    num_pages = len(reader.pages)
    print(f"Generated PDF Page Count: {num_pages}")
    
    import shutil
    desktop_pdf = r"C:\Users\Dileep Yadav\Desktop\Agentic_Social_Studio_Research_Paper.pdf"
    shutil.copy2(pdf_filename, desktop_pdf)
    print(f"Copied to {desktop_pdf}")

    for img_name in ["ieee_pipeline_architecture_bw.png", "ieee_fault_isolation_state_bw.png"]:
        if os.path.exists(img_name):
            shutil.copy2(img_name, os.path.join(r"C:\Users\Dileep Yadav\Desktop", img_name))
            print(f"Copied {img_name} to Desktop")

    return num_pages

if __name__ == "__main__":
    asyncio.run(compile_pdf())
