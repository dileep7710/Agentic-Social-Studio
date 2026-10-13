import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# ==========================================
# NUMBERED CANVAS (PAGE X OF Y + IEEE HEADERS)
# ==========================================
class IEEENumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(IEEENumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(IEEENumberedCanvas, self).showPage()
        super(IEEENumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#475569"))

        # Running Header (Pages 2+)
        if self._pageNumber > 1:
            self.drawString(
                36, 756,
                "AGENTIC-SOCIAL-STUDIO: RESILIENT MULTI-PLATFORM AUTOMATION"
            )
            self.drawRightString(576, 756, "RESEARCH PAPER SPECIFICATION")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(36, 750, 576, 750)

        # Running Footer (All Pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(36, 42, 576, 42)

        self.drawString(36, 30, "Deepak Kumar, Dileep Kumar | Department of Information Technology, REC Ambedkarnagar")
        self.drawRightString(576, 30, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf():
    pdf_filename = "Agentic_Social_Studio_Research_Paper.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()

    # Typography Styles
    title_style = ParagraphStyle(
        'PaperTitle',
        fontName='Helvetica-Bold',
        fontSize=17,
        leading=21,
        alignment=1, # Center
        textColor=colors.HexColor("#0F172A"),
        spaceAfter=8
    )

    authors_style = ParagraphStyle(
        'Authors',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        alignment=1,
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=3
    )

    affil_style = ParagraphStyle(
        'Affiliation',
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        alignment=1,
        textColor=colors.HexColor("#475569"),
        spaceAfter=12
    )

    abstract_heading = ParagraphStyle(
        'AbstractHeading',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#0F172A")
    )

    abstract_text = ParagraphStyle(
        'AbstractText',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        alignment=4, # Justified
        textColor=colors.HexColor("#1E293B"),
        leftIndent=15,
        rightIndent=15,
        spaceAfter=6
    )

    index_terms_style = ParagraphStyle(
        'IndexTerms',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#334155"),
        leftIndent=15,
        rightIndent=15,
        spaceAfter=12
    )

    sec_heading = ParagraphStyle(
        'SectionHeading',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    subsec_heading = ParagraphStyle(
        'SubSectionHeading',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B"),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body = ParagraphStyle(
        'Body',
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        alignment=4, # Justified
        textColor=colors.HexColor("#1E293B"),
        spaceAfter=5
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#0F172A")
    )

    math_block = ParagraphStyle(
        'MathBlock',
        fontName='Courier-Bold',
        fontSize=9,
        leading=12,
        alignment=1, # Center
        textColor=colors.HexColor("#0F172A"),
        spaceBefore=3,
        spaceAfter=5
    )

    table_header = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.5,
        textColor=colors.HexColor("#0F172A")
    )

    table_cell = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1E293B")
    )

    caption_style = ParagraphStyle(
        'Caption',
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        alignment=1, # Center
        textColor=colors.HexColor("#334155"),
        spaceBefore=4,
        spaceAfter=8
    )

    algo_style = ParagraphStyle(
        'AlgorithmText',
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    ref_style = ParagraphStyle(
        'RefStyle',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.8,
        textColor=colors.HexColor("#334155"),
        leftIndent=16,
        firstLineIndent=-16,
        spaceAfter=3
    )

    story = []

    # ==========================================
    # HEADER & TITLE BLOCK
    # ==========================================
    story.append(Paragraph("Agentic-Social-Studio: A Human-Centered Agentic Architecture for Resilient Multi-Platform Social Media Automation", title_style))
    story.append(Paragraph("Deepak Kumar &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Dileep Kumar", authors_style))
    story.append(Paragraph("Department of Information Technology, Rajkiya Engineering College (REC) Ambedkarnagar, India<br/>Project: Agentic-Social-Studio", affil_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#94A3B8"), spaceBefore=0, spaceAfter=8))

    # ==========================================
    # ABSTRACT & INDEX TERMS
    # ==========================================
    abstract_html = (
        "<b><i>Abstract</i>—Publishing a single idea across several social-media platforms is not merely a text-generation problem: "
        "the workflow must interpret intent, plan work, adapt content to different platform conventions, create or host media, "
        "select appropriate publishing tools, handle partial failures, and preserve meaningful human control over external actions. "
        "This paper presents Agentic-Social-Studio, a bounded agentic architecture for multi-platform content preparation and dispatch. "
        "The design separates probabilistic language-model functions from deterministic application logic. Eight functional modules—Goal Manager, "
        "Planner, Platform Content Adapter, Agent Orchestrator, Visual Generator, Media Upload Layer, Dispatch Engine, and Evaluator/Fallback "
        "Layer—operate under a cross-cutting control plane for validation, permissions, logging, timeouts, and reviewer approval. "
        "A three-level inference policy prefers a local language model, can use an optional cloud provider when explicitly configured, and falls "
        "back to deterministic templates when model services are unavailable. Per-platform execution is isolated so that a failure on one "
        "destination does not erase successful outcomes on others. The paper also specifies a security model for credentials, media, untrusted "
        "retrieved text, and irreversible publishing actions. Because the prototype has not yet undergone controlled experimentation, no accuracy, "
        "reliability, latency, or engagement improvements are claimed. Instead, we provide formal execution semantics, measurable failure states, "
        "a human-authority policy, and a preregisterable evaluation protocol covering content quality, fault recovery, workload, latency, cost, security, and reproducibility.</b>"
    )
    story.append(Paragraph(abstract_html, abstract_text))
    story.append(Paragraph("<b><i>Index Terms</i>—agentic AI, autonomous agents, human-in-the-loop, social media automation, tool use, fault isolation, hybrid inference, large language models, AI safety.</b>", index_terms_style))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#CBD5E1"), spaceBefore=0, spaceAfter=8))

    # ==========================================
    # I. INTRODUCTION
    # ==========================================
    story.append(Paragraph("I. INTRODUCTION", sec_heading))
    story.append(Paragraph(
        "Social-media automation often begins as a formatting problem but quickly becomes a systems problem. A user may want one campaign idea "
        "transformed into suitable content for Instagram, LinkedIn, Facebook, WhatsApp, and X. Each destination differs in presentation norms, "
        "interaction patterns, media requirements, authentication, and failure modes. Classical schedulers and copy-paste pipelines can automate "
        "repetition, but they are poorly suited to tasks in which a system must interpret a goal, choose among tools, react to observations, and "
        "degrade safely when an API, credential, model, or media host is unavailable.",
        body
    ))
    story.append(Paragraph(
        "Recent work characterizes LLM-based agents as systems that combine language-model reasoning with planning, memory, tool invocation, and "
        "environmental feedback [1], [2]. Tool-oriented systems such as Toolformer, HuggingGPT, and ToolLLM illustrate different mechanisms for selecting "
        "or coordinating external capabilities [3]-[5]; the broader augmented-language-model literature similarly treats reasoning and external modules as "
        "complementary extensions to language generation [27]. At the same time, AgentBench and WebArena show that long-horizon agent behavior remains "
        "difficult and that evaluation must consider complete task execution rather than isolated model responses [6], [7]. These observations motivate a "
        "conservative architecture in which language models propose or generate, while deterministic software controls permissions, state, and failure handling.",
        body
    ))
    story.append(Paragraph(
        "Agentic-Social-Studio applies this pattern to multi-platform publishing. The research problem is: <i>How can an agentic workflow transform one human intent "
        "into platform-aware content and execute or prepare actions across heterogeneous social platforms while containing failures and preserving human authority over irreversible actions?</i>",
        body
    ))
    story.append(Paragraph(
        "The paper makes four systems contributions. <b>First</b>, it defines a modular end-to-end architecture that separates interpretation, generation, tool selection, "
        "execution, and evaluation. <b>Second</b>, it formalizes partial-success execution and a tri-tier inference policy without treating language models as sole planners; "
        "this is consistent with work advocating structured or verifier-assisted planning [10], [11]. <b>Third</b>, it introduces a human-authority boundary in which content "
        "creation and previewing may be automated, while real-account publication is treated as an approval-gated action, following human-centered AI guidance [16]-[18]. "
        "<b>Fourth</b>, it specifies a reproducible evaluation design rather than reporting unmeasured performance claims.",
        body
    ))

    # ==========================================
    # II. RELATED WORK
    # ==========================================
    story.append(Paragraph("II. RELATED WORK", sec_heading))
    story.append(Paragraph("<b>A. Agent Planning and Tool Use</b>", subsec_heading))
    story.append(Paragraph(
        "LLM-agent research commonly decomposes agent behavior into perception, reasoning or planning, action, and feedback [1]. ReAct explicitly interleaves reasoning "
        "and environment actions [2]; Toolformer studies learned API use [3]; HuggingGPT uses a language model as a controller over specialized models [4]; and ToolLLM "
        "evaluates large-scale real-world API use [5]. Multi-agent frameworks such as AutoGen and MetaGPT emphasize structured coordination and role decomposition [8], [9]. "
        "Reflexion and Tree of Thoughts explore feedback-driven revision and deliberate search, respectively [28], [29]. These systems motivate richer orchestration, but they do not remove the need for deterministic constraints around external actions.",
        body
    ))
    story.append(Paragraph(
        "Planning reliability is particularly relevant. LLM+P combines language models with a classical planner rather than assuming that free-form model output is always a valid plan [11]. "
        "Kapoor et al. argue that useful agent evaluation should include cost, reproducibility, and downstream utility rather than accuracy alone [10]. Accordingly, Agentic-Social-Studio uses bounded workflows and explicit metrics for tool calls, time, failure, and human intervention.",
        body
    ))

    story.append(Paragraph("<b>B. Platform-Aware Content and Personalization</b>", subsec_heading))
    story.append(Paragraph(
        "Social-media platforms differ in the functions they emphasize, including identity, conversation, sharing, relationships, and reputation [14]; more broadly, social media encompasses heterogeneous forms of user-generated interaction rather than a single communication channel [13]. Empirical marketing research also shows that post characteristics such as vividness, interactivity, and informational or entertaining content can influence audience reactions [15]. These studies do not prescribe fixed templates for modern platforms, but they support treating platform adaptation as a first-class design concern rather than duplicating one message verbatim. Research on LLM personalization further shows that generating context-sensitive outputs is a distinct evaluation problem [12].",
        body
    ))

    story.append(Paragraph("<b>C. Human Oversight, Security, and Evaluation</b>", subsec_heading))
    story.append(Paragraph(
        "Human-centered AI literature argues that high automation and meaningful human control are compatible design goals, especially when systems operate under uncertainty [16]. "
        "Earlier automation research likewise emphasizes choosing different levels of automation for information acquisition, analysis, decision selection, and action implementation, rather than treating autonomy as a single all-or-nothing variable [30]; calibrated trust is important because both over-reliance and under-reliance can reduce human performance [31]. "
        "General human-AI interaction guidelines recommend making system capabilities visible, supporting efficient correction, and providing appropriate control [17]; human-in-the-loop literature similarly distinguishes multiple ways in which people can supervise or shape machine behavior [18]. "
        "More recent agent-interface research explores action approval, co-planning, and verification as concrete mechanisms for human involvement [24]. NIST's Generative AI Profile emphasizes governance, measurement, and risk management across the AI lifecycle [19].",
        body
    ))
    story.append(Paragraph(
        "Security is also central for agents that consume untrusted text and invoke tools. Indirect prompt injection can cause retrieved data to be interpreted as instructions [20], while AgentDojo demonstrates the difficulty of simultaneously maintaining task utility and security under adversarial tool outputs [21]. These findings motivate treating retrieved text as data, limiting tool authority, and placing irreversible publishing behind an explicit reviewer gate.",
        body
    ))

    # TABLE I: POSITIONING
    t1_data = [
        [Paragraph("<b>Work</b>", table_header), Paragraph("<b>LLM agent</b>", table_header), Paragraph("<b>External tools</b>", table_header), Paragraph("<b>Multi-platform adaptation</b>", table_header), Paragraph("<b>Failure containment</b>", table_header), Paragraph("<b>Human action gate</b>", table_header), Paragraph("<b>Security evaluation</b>", table_header)],
        [Paragraph("ReAct [2]", table_cell), Paragraph("Yes", table_cell), Paragraph("Yes", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell)],
        [Paragraph("ToolLLM [5]", table_cell), Paragraph("Yes", table_cell), Paragraph("Yes", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell)],
        [Paragraph("WebArena [7]", table_cell), Paragraph("Yes", table_cell), Paragraph("Yes", table_cell), Paragraph("No", table_cell), Paragraph("Evaluation focus", table_cell), Paragraph("No", table_cell), Paragraph("No", table_cell)],
        [Paragraph("AutoGen [8]", table_cell), Paragraph("Yes", table_cell), Paragraph("Yes", table_cell), Paragraph("Not specific", table_cell), Paragraph("Framework-dependent", table_cell), Paragraph("Supports human input", table_cell), Paragraph("Not primary focus", table_cell)],
        [Paragraph("Magentic-UI [24]", table_cell), Paragraph("Yes", table_cell), Paragraph("Yes", table_cell), Paragraph("No", table_cell), Paragraph("Yes", table_cell), Paragraph("Yes", table_cell), Paragraph("Targeted safety", table_cell)],
        [Paragraph("<b>Agentic-Social-Studio (this work)</b>", table_header), Paragraph("<b>Yes</b>", table_header), Paragraph("<b>Yes</b>", table_header), Paragraph("<b>Yes</b>", table_header), Paragraph("<b>Yes</b>", table_header), Paragraph("<b>Yes</b>", table_header), Paragraph("<b>Explicit threat model</b>", table_header)],
    ]
    t1 = Table(t1_data, colWidths=[105, 50, 60, 95, 85, 80, 65])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor("#EFF6FF")),
    ]))
    story.append(Spacer(1, 4))
    story.append(Paragraph("<b>TABLE I: POSITIONING AGAINST REPRESENTATIVE PRIOR WORK</b>", caption_style))
    story.append(t1)
    story.append(Paragraph("<i>Entries summarize the primary scope described by each cited work; 'No' means not a reported focus of that study.</i>", caption_style))
    story.append(Spacer(1, 6))

    # ==========================================
    # III. PROBLEM FORMULATION AND DESIGN PRINCIPLES
    # ==========================================
    story.append(Paragraph("III. PROBLEM FORMULATION AND DESIGN PRINCIPLES", sec_heading))
    story.append(Paragraph(
        "Let a session begin with user intent <i>u</i>, author or account context <i>a</i>, and target-platform set <i>P</i>. The Goal Manager produces structured goal:",
        body
    ))
    story.append(Paragraph("g = (&theta;, m, P, t) &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(1)", math_block))
    story.append(Paragraph(
        "where &theta; is the theme or communication objective, <i>m</i> is optional contextual metadata, and <i>t</i> is the request time. A planning policy produces ordered plan &pi;. A base content object <i>c</i> and visual asset <i>v</i> are generated or selected, after which an adapter creates platform variants <i>c_p</i> for each <i>p &isin; P</i>. The dispatch stage returns an outcome:",
        body
    ))
    story.append(Paragraph("o_p &isin; { SUCCESS, ASSISTED, FAILURE, BLOCKED } &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(2)", math_block))
    story.append(Paragraph(
        "<b>ASSISTED</b> means that automation prepared a user-completable action (for example, a prefilled share surface) rather than publishing directly. <b>BLOCKED</b> means execution was intentionally prevented by a policy, validation, or approval gate.",
        body
    ))
    story.append(Paragraph(
        "The design follows five principles: <b>(i) bounded autonomy:</b> models can only invoke registered operations through validated arguments; "
        "<b>(ii) failure locality:</b> a platform-specific failure must not overwrite outcomes already achieved elsewhere; "
        "<b>(iii) progressive degradation:</b> unavailable model or infrastructure dependencies fall back to lower-dependency alternatives; "
        "<b>(iv) human authority:</b> external publication is an irreversible action and requires explicit authorization in real-account evaluation; and "
        "<b>(v) observability:</b> each state transition, tool call, duration, and error class is recorded without storing private model chain-of-thought.",
        body
    ))

    # ==========================================
    # IV. ARCHITECTURE
    # ==========================================
    story.append(Paragraph("IV. ARCHITECTURE", sec_heading))
    story.append(Paragraph(
        "Fig. 1 shows the system architecture. The eight functional modules are surrounded by a deterministic control plane rather than counted as additional agents.",
        body
    ))

    # EMBED FIGURE 1
    if os.path.exists("fig1_architecture.png"):
        story.append(Spacer(1, 4))
        story.append(RLImage("fig1_architecture.png", width=7.2*inch, height=2.85*inch))
        story.append(Paragraph("<b>Fig. 1. Agentic-Social-Studio architecture.</b> Probabilistic generation is separated from deterministic validation, authorization, state, and failure handling. The reviewer gate is a control boundary rather than an autonomous module.", caption_style))
        story.append(Spacer(1, 4))

    story.append(Paragraph("<b>A. Functional Modules</b>", subsec_heading))
    story.append(Paragraph(
        "The <b>Goal Manager</b> converts raw text into a small typed representation and should prefer explicit user constraints over inferred preferences. "
        "The <b>Planner</b> creates a short ordered plan and exposes the selected inference tier. "
        "The <b>Agent Orchestrator</b> advances the session state, applies execution budgets, and never bypasses tool permissions. "
        "The <b>Platform Content Adapter</b> produces independent variants for each requested platform. "
        "The <b>Visual Generator</b> renders reusable story/feed assets from validated text and layout parameters. "
        "The <b>Media Upload Layer</b> publishes media to an approved host and can try a secondary provider within a fixed retry budget. "
        "The <b>Dispatch Engine</b> maps each platform to an allowed API action or user-assisted share mechanism. "
        "The <b>Evaluator/Fallback Layer</b> classifies results and selects a bounded recovery action based on structured error codes.",
        body
    ))
    story.append(Paragraph(
        "The original prototype uses Python, Streamlit, Pillow, asynchronous HTTP requests, and Ollama-backed local inference. The reference build described in the source material uses a local Llama 3.2 3B model plus deterministic fallback; the cloud tier is therefore treated as an optional provider interface rather than an experimentally validated dependency.",
        body
    ))

    story.append(Paragraph("<b>B. Human Authority Matrix</b>", subsec_heading))
    story.append(Paragraph("Table II makes authority allocation explicit. The main human-centered constraint is that preparing content is different from committing content to an external account.", body))

    # TABLE II: HUMAN AUTHORITY
    t2_data = [
        [Paragraph("<b>Stage</b>", table_header), Paragraph("<b>System may do automatically</b>", table_header), Paragraph("<b>Human role</b>", table_header)],
        [Paragraph("Interpret", table_cell), Paragraph("Structure intent; flag ambiguity", table_cell), Paragraph("Correct", table_cell)],
        [Paragraph("Generate", table_cell), Paragraph("Draft text/visual variants", table_cell), Paragraph("Edit/reject", table_cell)],
        [Paragraph("Validate", table_cell), Paragraph("Check schema, length, media, links", table_cell), Paragraph("Review", table_cell)],
        [Paragraph("Preview", table_cell), Paragraph("Render final per-platform package", table_cell), Paragraph("Inspect", table_cell)],
        [Paragraph("Publish", table_cell), Paragraph("Prepare tool call or share action", table_cell), Paragraph("Approve", table_cell)],
        [Paragraph("Recover", table_cell), Paragraph("Suggest retry/fallback", table_cell), Paragraph("Approve fallback", table_cell)],
    ]
    t2 = Table(t2_data, colWidths=[90, 290, 160])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>TABLE II: HUMAN AUTHORITY AND AUTOMATION BOUNDARY</b>", caption_style))
    story.append(t2)
    story.append(Spacer(1, 6))

    # ==========================================
    # V. AGENTIC EXECUTION AND PLATFORM ADAPTATION
    # ==========================================
    story.append(Paragraph("V. AGENTIC EXECUTION AND PLATFORM ADAPTATION", sec_heading))
    story.append(Paragraph(
        "Algorithm 1 is expressed as typed control flow rather than hidden model reasoning. The model may propose content or a plan, but ordinary software determines whether an action is valid and authorized. For platform <i>p</i>, the adapter can be written as <i>c_p = A_p(c, g)</i>, where <i>A_p</i> is a deterministic template, an LLM-conditioned transformation, or a hybrid. Platform rules are operational constraints that can be tested (Table III).",
        body
    ))

    # ALGORITHM 1 BOX
    algo_content = [
        [Paragraph("<b>Algorithm 1: Bounded Multi-Platform Execution</b>", table_header)],
        [Paragraph(
            "1) <b>g</b> &larr; GoalManager.parse(u, P)<br/>"
            "2) (<b>&pi;</b>, tier) &larr; PlanWithFallback(g)<br/>"
            "3) (<b>c</b>, <b>v</b>) &larr; generate draft content and visual; validate types, lengths, and media signature<br/>"
            "4) {<b>c_p</b>} &larr; Adapter.adapt(c, P)<br/>"
            "5) Build a preview package and request approval for direct publishing<br/>"
            "6) <b>For each</b> p &isin; P independently: select permitted tool; execute under timeout/retry limits; classify the result; if recoverable, invoke at most the configured fallback path<br/>"
            "7) Aggregate per-platform outcomes and return session telemetry.",
            algo_style
        )]
    ]
    t_algo = Table(algo_content, colWidths=[540])
    t_algo.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F8FAFC")),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#FFFFFF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#64748B")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(Spacer(1, 2))
    story.append(t_algo)
    story.append(Spacer(1, 6))

    # TABLE III: ADAPTATION INTENT
    t3_data = [
        [Paragraph("<b>Target</b>", table_header), Paragraph("<b>Intended Register</b>", table_header), Paragraph("<b>Adapter Behavior</b>", table_header)],
        [Paragraph("Instagram", table_cell), Paragraph("expressive", table_cell), Paragraph("visual-first caption; compact hashtags (#Motivation #DailyWisdom)", table_cell)],
        [Paragraph("LinkedIn", table_cell), Paragraph("professional", table_cell), Paragraph("context, takeaway, restrained formatting, corporate hashtags", table_cell)],
        [Paragraph("Facebook", table_cell), Paragraph("conversational", table_cell), Paragraph("community-oriented prompt/question ('Do you agree with this?')", table_cell)],
        [Paragraph("WhatsApp", table_cell), Paragraph("direct", table_cell), Paragraph("clean markdown bold/italic, direct CDN media link handoff", table_cell)],
        [Paragraph("X (Twitter)", table_cell), Paragraph("concise", table_cell), Paragraph("configurable character budget &le; 275 and safe truncation", table_cell)],
    ]
    t3 = Table(t3_data, colWidths=[90, 100, 350])
    t3.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(Paragraph("<b>TABLE III: PROTOTYPE PLATFORM-ADAPTATION INTENT</b>", caption_style))
    story.append(t3)
    story.append(Spacer(1, 6))

    # ==========================================
    # VI. TRI-TIER INFERENCE AND RESILIENCE
    # ==========================================
    story.append(Paragraph("VI. TRI-TIER INFERENCE AND RESILIENCE", sec_heading))
    story.append(Paragraph(
        "The inference policy selects the first permitted and available tier:",
        body
    ))
    story.append(Paragraph("T(g) = { T_L(g) if local model succeeds within &tau;_L; T_C(g) if cloud enabled &amp; succeeds within &tau;_C; T_H(g) otherwise } &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(3)", math_block))
    story.append(Paragraph(
        "where <i>T_H</i> is a deterministic heuristic/template path. The important guarantee is not 'zero latency' or globally bounded end-to-end execution. The defensible guarantee is that tier selection can be bounded by configured timeouts, while total workflow latency is bounded only if every external operation also has explicit timeout and retry budgets.",
        body
    ))

    # EMBED FIGURE 2
    if os.path.exists("fig2_tritier.png"):
        story.append(Spacer(1, 3))
        story.append(RLImage("fig2_tritier.png", width=4.5*inch, height=3.6*inch))
        story.append(Paragraph("<b>Fig. 2. Tri-tier inference policy.</b> The cloud tier is optional; deterministic fallback remains available even when both model providers are unavailable.", caption_style))
        story.append(Spacer(1, 4))

    story.append(Paragraph("<b>A. Failure Semantics</b>", subsec_heading))
    story.append(Paragraph(
        "Failures are classified as either shared-stage failures (e.g., no valid content package exists) or platform-local failures (e.g., one platform rejects authentication). Only the latter are promised to be isolated. This distinction closes an ambiguity: an invalid shared visual can legitimately block all media-dependent destinations, whereas an expired token for one platform must not erase a successful result elsewhere. For <i>n = |P|</i> target platforms, define normalized platform completion:",
        body
    ))
    story.append(Paragraph("C = (1 / n) &sum;_{p &isin; P} I[ o_p &isin; { SUCCESS, ASSISTED } ] &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(4)", math_block))
    story.append(Paragraph(
        "A session is 'full' only when all required outcomes satisfy the experiment's success definition; otherwise the vector of per-platform outcomes is retained instead of collapsing every mixed run into a single binary label.",
        body
    ))

    # ==========================================
    # VII. SECURITY, PRIVACY, AND RESPONSIBLE ACTION
    # ==========================================
    story.append(Paragraph("VII. SECURITY, PRIVACY, AND RESPONSIBLE ACTION", sec_heading))
    story.append(Paragraph(
        "The security boundary is wider than credential encryption. A production-capable agent can receive adversarial user text, retrieve untrusted web content, manipulate files, and act on external accounts. The revised threat model therefore covers data, model instructions, tools, and irreversible actions. "
        "AES-GCM is an authenticated-encryption mode standardized by NIST [22]; encryption is therefore appropriate for recoverable access tokens, whereas hashing alone is not. Encryption does not solve authorization, key management, transport, or logging risks, so those controls are specified separately. For the broader generative-AI risk process, the evaluation should record intended context, system limits, incidents, and human overrides as recommended by risk-management guidance [19].",
        body
    ))

    # ==========================================
    # VIII. IMPLEMENTATION METHODOLOGY
    # ==========================================
    story.append(Paragraph("VIII. IMPLEMENTATION METHODOLOGY", sec_heading))
    story.append(Paragraph(
        "The prototype described in the supplied implementation uses Python with a Streamlit interface. Pillow generates 1080x1920 story assets and 1080x1080 feed assets; referring to these as '4K' would be inaccurate and is avoided here. HTTP clients handle platform and media-host interactions; URI construction supports user-assisted share paths where appropriate. Local generation runs through Ollama with Meta Llama 3.2 3B. The system should pin model identifier, prompt version, decoding parameters, Python/package versions, and platform-adapter configuration for every experiment. "
        "Each tool is represented by a name, typed input schema, typed output schema, permission level, timeout, and implementation. A tool call that fails validation is not executed. Platform dispatch occurs in isolated blocks, and the orchestrator persists a concise event record containing session ID, stage, tool, status, duration, error class, and non-secret metadata.",
        body
    ))

    # ==========================================
    # IX. EVALUATION METHODOLOGY
    # ==========================================
    story.append(Paragraph("IX. EVALUATION METHODOLOGY", sec_heading))
    story.append(Paragraph("<b>A. Research Questions</b>", subsec_heading))
    story.append(Paragraph(
        "• <b>RQ1:</b> How reliably does the workflow complete a multi-platform preparation/publishing task under nominal conditions?<br/>"
        "• <b>RQ2:</b> Do platform-specific variants receive higher blinded appropriateness ratings than a single copied post?<br/>"
        "• <b>RQ3:</b> How effectively are platform-local faults contained and recovered without reducing success on unaffected platforms?<br/>"
        "• <b>RQ4:</b> What quality, latency, availability, privacy, and cost trade-offs arise across local, cloud, and heuristic inference tiers?<br/>"
        "• <b>RQ5:</b> How does the agentic workflow change human effort, edit count, approval time, and perceived control compared with a manual/template workflow?<br/>"
        "• <b>RQ6:</b> How robust are the policy and tool boundaries to adversarial or malformed inputs, including prompt injection and media-validation failures?",
        body
    ))

    # TABLE IV: THREAT MODEL
    t4_data = [
        [Paragraph("<b>Threat</b>", table_header), Paragraph("<b>Example consequence</b>", table_header), Paragraph("<b>Control in the revised design</b>", table_header), Paragraph("<b>Residual risk / validation need</b>", table_header)],
        [Paragraph("Credential compromise", table_cell), Paragraph("Unauthorized account actions", table_cell), Paragraph("AES-256-GCM at rest; fresh nonce per encryption; key kept outside db", table_cell), Paragraph("Host or key-store compromise can still expose tokens", table_cell)],
        [Paragraph("Untrusted retrieved text", table_cell), Paragraph("Prompt injection changes tool behavior", table_cell), Paragraph("Treat retrieved text as data; allow-listed tools; schema validation", table_cell), Paragraph("Semantic attacks may still influence generated content [20], [21]", table_cell)],
        [Paragraph("Malicious media", table_cell), Paragraph("Parser abuse or disguised payload", table_cell), Paragraph("MIME/header signature validation, size limits, generated allow-list", table_cell), Paragraph("Valid-but-malicious media requires deeper scanning", table_cell)],
        [Paragraph("Token/log leakage", table_cell), Paragraph("Secrets retained in telemetry", table_cell), Paragraph("Redact authorization headers; do not place secrets in prompts", table_cell), Paragraph("Misconfigured logging or external SDKs may leak metadata", table_cell)],
        [Paragraph("Unauthorized publication", table_cell), Paragraph("Content posted without intended consent", table_cell), Paragraph("Reviewer approval before direct dispatch; immutable audit record", table_cell), Paragraph("Compromised reviewer session or social engineering", table_cell)],
        [Paragraph("Runaway retries / cost", table_cell), Paragraph("Excess API calls or delayed completion", table_cell), Paragraph("Per-tool timeout, retry, tool-call, and session budgets", table_cell), Paragraph("Provider-side retries may be opaque", table_cell)],
    ]
    t4 = Table(t4_data, colWidths=[100, 110, 185, 145])
    t4.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(Spacer(1, 2))
    story.append(Paragraph("<b>TABLE IV: THREAT MODEL AND REQUIRED CONTROLS</b>", caption_style))
    story.append(t4)
    story.append(Spacer(1, 6))

    # TABLE V: PLANNED EXPERIMENTS
    t5_data = [
        [Paragraph("<b>ID</b>", table_header), Paragraph("<b>Objective</b>", table_header), Paragraph("<b>Primary measures</b>", table_header)],
        [Paragraph("E1", table_cell), Paragraph("Nominal completion", table_cell), Paragraph("C, full/partial/failed sessions, tool errors", table_cell)],
        [Paragraph("E2", table_cell), Paragraph("Adaptation quality", table_cell), Paragraph("blinded 5-point ratings; inter-rater agreement (Krippendorff's alpha)", table_cell)],
        [Paragraph("E3", table_cell), Paragraph("Fault injection", table_cell), Paragraph("containment, recovery rate, recovery latency", table_cell)],
        [Paragraph("E4", table_cell), Paragraph("Inference tiers", table_cell), Paragraph("latency, availability, rated quality, cost", table_cell)],
        [Paragraph("E5", table_cell), Paragraph("Human workload", table_cell), Paragraph("time, edits, interventions, rejection/approval rate", table_cell)],
        [Paragraph("E6", table_cell), Paragraph("Manual vs. agentic", table_cell), Paragraph("paired completion time and action count", table_cell)],
        [Paragraph("E7", table_cell), Paragraph("Security tests", table_cell), Paragraph("blocked unsafe actions, injection/tool-policy failures", table_cell)],
        [Paragraph("E8", table_cell), Paragraph("Load/repeatability", table_cell), Paragraph("variance across repeats; concurrency failures", table_cell)],
    ]
    t5 = Table(t5_data, colWidths=[40, 180, 320])
    t5.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 2.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(Paragraph("<b>TABLE V: PLANNED EXPERIMENTS (NO RESULTS CLAIMED)</b>", caption_style))
    story.append(t5)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>B. Experiments, Baselines, and Measures</b>", subsec_heading))
    story.append(Paragraph(
        "E2 should randomize and blind the presentation of adapted and non-adapted posts so raters do not know which condition produced each item. Raters score relevance, platform fit, readability, factual fidelity, and overall usefulness; Krippendorff's alpha or an equivalently justified inter-rater statistic should be reported. E3 injects one fault at a time—expired credential, unavailable primary media host, stopped local LLM, cloud timeout, malformed upload, or platform API failure—and records whether unrelated platforms retain their nominal outcomes. E4 compares identical prompts and task sets across enabled tiers. E5/E6 use the same participants and tasks across conditions where practical, with order counterbalancing to reduce learning effects.",
        body
    ))
    story.append(Paragraph(
        "Binary rates should include Wilson 95% confidence intervals. Paired continuous or ordinal comparisons should report effect sizes and use a paired t-test only when assumptions are defensible; otherwise a Wilcoxon signed-rank test is appropriate. Sample size should be selected by prospective power analysis rather than choosing N after results are seen. All failures, retries, and reviewer rejections remain in the dataset.",
        body
    ))

    # ==========================================
    # X. THREATS TO VALIDITY AND LIMITATIONS
    # ==========================================
    story.append(Paragraph("X. THREATS TO VALIDITY AND LIMITATIONS", sec_heading))
    story.append(Paragraph(
        "<b>Construct validity:</b> 'Platform appropriateness' is subjective and cannot be established by template conformance alone; human ratings therefore complement deterministic checks. Engagement metrics are not used as a proxy for content quality because they depend on audience size, timing, recommendation systems, and account history.<br/>"
        "<b>Internal validity:</b> LLM outputs are nondeterministic, and external APIs vary over time. Repeated runs, pinned configurations, fixed task sets, and preserved failures are required.<br/>"
        "<b>External validity:</b> Results from five selected platforms, one local model, and a small prototype should not be generalized to all social networks, languages, or organization types.<br/>"
        "<b>Security scope:</b> AES-GCM and file-signature checks cover only narrow risks. They do not by themselves solve prompt injection, compromised hosts, malicious but valid media, account takeover, platform-policy compliance, or moderation.<br/>"
        "<b>Ethical scope:</b> Automated generation can amplify misinformation, impersonation, or unwanted bulk posting. The system should not infer permission to publish from credential availability alone. A human reviewer remains responsible for factual claims, rights to media, audience suitability, and the decision to publish.",
        body
    ))

    # ==========================================
    # XI. DISCUSSION & XII. CONCLUSION
    # ==========================================
    story.append(Paragraph("XI. DISCUSSION", sec_heading))
    story.append(Paragraph(
        "The architectural contribution is integration rather than a new foundation model or planning algorithm. The system combines established ideas—goal decomposition, tool use, platform adaptation, deterministic validation, fallback, and human oversight—into a workflow in which success can be measured at each stage. This framing avoids two common overclaims. First, graceful degradation is not the same as self-healing: the prototype can select an alternate path but does not autonomously repair expired credentials or third-party outages. Second, partial success is not equivalent to reliability; it is an execution semantic that must be evaluated under controlled fault injection.",
        body
    ))

    story.append(Paragraph("XII. CONCLUSION", sec_heading))
    story.append(Paragraph(
        "This paper presented Agentic-Social-Studio, a bounded, human-centered agentic architecture for preparing and coordinating social-media content across multiple platforms. The framework separates model-driven interpretation and generation from deterministic orchestration, validation, permission checks, state, and logging; it supports local/cloud/heuristic inference fallback; isolates platform-local failures; and distinguishes autonomous preparation from approval-gated external publication. The paper intentionally reports no unmeasured performance claims. Its main deliverables are a coherent architecture, formal outcome semantics, a security and human-authority model, and an eight-experiment evaluation plan that can test quality, reliability, workload, latency, cost, security, and reproducibility.",
        body
    ))

    # ==========================================
    # REFERENCES [1] TO [31]
    # ==========================================
    story.append(Spacer(1, 4))
    story.append(Paragraph("REFERENCES", sec_heading))
    refs = [
        "[1] L. Wang, C. Ma, X. Feng, et al., 'A survey on large language model based autonomous agents,' Frontiers of Computer Science, vol. 18, Art. no. 186345, 2024.",
        "[2] S. Yao, J. Zhao, D. Yu, N. Du, I. Shafran, K. R. Narasimhan, and Y. Cao, 'ReAct: Synergizing reasoning and acting in language models,' in Proc. ICLR, 2023.",
        "[3] T. Schick, J. Dwivedi-Yu, R. Dessi, et al., 'Toolformer: Language models can teach themselves to use tools,' in NeurIPS, vol. 36, pp. 68539-68551, 2023.",
        "[4] Y. Shen, K. Song, X. Tan, D. Li, W. Lu, and Y. Zhuang, 'HuggingGPT: Solving AI tasks with ChatGPT and its friends in Hugging Face,' in NeurIPS, vol. 36, pp. 38154-38180, 2023.",
        "[5] Y. Qin, S. Liang, Y. Ye, et al., 'ToolLLM: Facilitating large language models to master 16000+ real-world APIs,' in Proc. ICLR, 2024.",
        "[6] X. Liu, H. Yu, H. Zhang, et al., 'AgentBench: Evaluating LLMs as agents,' in Proc. ICLR, 2024.",
        "[7] S. Zhou, F. F. Xu, H. Zhu, et al., 'WebArena: A realistic web environment for building autonomous agents,' in Proc. ICLR, 2024.",
        "[8] Q. Wu, G. Bansal, J. Zhang, et al., 'AutoGen: Enabling next-gen LLM applications via multi-agent conversation,' in Proc. COLM, 2024.",
        "[9] S. Hong, M. Zhuge, J. Chen, et al., 'MetaGPT: Meta programming for a multi-agent collaborative framework,' in Proc. ICLR, 2024.",
        "[10] S. Kapoor, B. Stroebl, Z. S. Siegel, N. Nadgir, and A. Narayanan, 'AI agents that matter,' arXiv:2407.01502, 2024.",
        "[11] B. Liu, Y. Jiang, X. Zhang, Q. Liu, S. Zhang, J. Biswas, and P. Stone, 'LLM+P: Empowering large language models with optimal planning proficiency,' arXiv:2304.11477, 2023.",
        "[12] A. Salemi, S. Mysore, M. Bendersky, and H. Zamani, 'LaMP: When large language models meet personalization,' in Proc. ACL, pp. 7370-7392, 2024.",
        "[13] A. M. Kaplan and M. Haenlein, 'Users of the world, unite! The challenges and opportunities of social media,' Business Horizons, vol. 53, no. 1, pp. 59-68, 2010.",
        "[14] J. H. Kietzmann, K. Hermkens, I. P. McCarthy, and B. S. Silvestre, 'Social media? Get serious! Understanding the functional building blocks of social media,' Business Horizons, vol. 54, no. 3, pp. 241-251, 2011.",
        "[15] L. de Vries, S. Gensler, and P. S. H. Leeflang, 'Popularity of brand posts on brand fan pages: An investigation of the effects of social media marketing,' Journal of Interactive Marketing, vol. 26, no. 2, pp. 83-91, 2012.",
        "[16] B. Shneiderman, 'Human-centered artificial intelligence: Reliable, safe & trustworthy,' International Journal of Human-Computer Interaction, vol. 36, no. 6, pp. 495-504, 2020.",
        "[17] S. Amershi, D. Weld, M. Vorvoreanu, et al., 'Guidelines for human-AI interaction,' in Proc. CHI, pp. 1-13, 2019.",
        "[18] E. Mosqueira-Rey, E. Hernandez-Pereira, D. Alonso-Rios, et al., 'Human-in-the-loop machine learning: A state of the art,' Artificial Intelligence Review, vol. 56, pp. 3005-3054, 2023.",
        "[19] C. Autio, R. Schwartz, J. Dunietz, et al., Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile, NIST AI 600-1, 2024.",
        "[20] K. Greshake, S. Abdelnabi, S. Mishra, et al., 'Not what you've signed up for: Compromising real-world LLM-integrated applications with indirect prompt injection,' in Proc. ACM AISec, pp. 79-90, 2023.",
        "[21] E. Debenedetti, J. Zhang, M. Balunovic, et al., 'AgentDojo: A dynamic environment to evaluate prompt injection attacks and defenses for LLM agents,' in NeurIPS, vol. 37, 2024.",
        "[22] M. Dworkin, Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC, NIST SP 800-38D, 2007.",
        "[23] M. Zhang, J. Cao, X. Shen, and Z. Cui, 'EdgeShard: Efficient LLM inference via collaborative edge computing,' IEEE Internet of Things Journal, vol. 12, no. 10, pp. 13119-13131, 2025.",
        "[24] H. Mozannar, G. Bansal, C. Tan, et al., 'Magentic-UI: Towards human-in-the-loop agentic systems,' Microsoft Research Technical Report MSR-TR-2025-40, 2025.",
        "[25] Z. Xi, W. Chen, X. Guo, et al., 'The rise and potential of large language model based agents: A survey,' arXiv:2309.07864, 2023.",
        "[26] D. B. Acharya, K. Kuppan, and B. Divya, 'Agentic AI: Autonomous intelligence for complex goals-A comprehensive survey,' IEEE Access, vol. 13, pp. 18912-18936, 2025.",
        "[27] G. Mialon, R. Dessi, M. Lomeli, et al., 'Augmented language models: A survey,' Transactions on Machine Learning Research, 2023.",
        "[28] N. Shinn, F. Cassano, A. Gopinath, K. Narasimhan, and S. Yao, 'Reflexion: Language agents with verbal reinforcement learning,' in NeurIPS, vol. 36, 2023.",
        "[29] S. Yao, D. Yu, J. Zhao, I. Shafran, T. Griffiths, Y. Cao, and K. Narasimhan, 'Tree of Thoughts: Deliberate problem solving with large language models,' in NeurIPS, vol. 36, 2023.",
        "[30] R. Parasuraman, T. B. Sheridan, and C. D. Wickens, 'A model for types and levels of human interaction with automation,' IEEE Trans. Syst., Man, Cybern. A, vol. 30, no. 3, pp. 286-297, 2000.",
        "[31] J. D. Lee and K. A. See, 'Trust in automation: Designing for appropriate reliance,' Human Factors, vol. 46, no. 1, pp. 50-80, 2004."
    ]
    for r in refs:
        story.append(Paragraph(r, ref_style))

    doc.build(story, canvasmaker=IEEENumberedCanvas)
    print(f"Publication-grade PDF successfully compiled: {pdf_filename}")

if __name__ == "__main__":
    build_pdf()
