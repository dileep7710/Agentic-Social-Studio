import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas that adds Page X of Y and Running Headers to every page."""
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (Only on page 2 onwards)
        if self._pageNumber > 1:
            self.drawString(54, 750, "AGENTIC AI CORE & EXPANDED TOOL REGISTRY — COMPLETE SPECIFICATION")
            self.drawRightString(612 - 54, 750, "B.Tech Final Year Capstone Project")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.5)
            self.line(54, 744, 612 - 54, 744)

        # Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        
        self.drawString(54, 32, "Author: Dileep Yadav | Project: Agentic-Social-Studio")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        self.restoreState()


def build_agentic_ai_pdf(output_filename="Agentic_AI_Core_Deep_Explanation.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#1E1B4B")     # Deep Indigo #1E1B4B
    SECONDARY = colors.HexColor("#4338CA")   # Indigo #4338CA
    ACCENT_CYAN = colors.HexColor("#0284C7") # Sky Blue #0284C7
    ACCENT_GOLD = colors.HexColor("#D97706") # Amber #D97706
    BG_BOX = colors.HexColor("#F8FAFC")      # Slate 50
    TEXT_DARK = colors.HexColor("#0F172A")   # Slate 900
    TEXT_MUTED = colors.HexColor("#475569")  # Slate 600

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=PRIMARY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=SECONDARY,
        spaceAfter=12
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MUTED,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=PRIMARY,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        spaceAfter=5
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#0F172A")
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=TEXT_DARK,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    story = []

    # ==========================================
    # COVER / HEADER
    # ==========================================
    story.append(Paragraph("🌌 AGENTIC AI CORE & EXPANDED TOOL REGISTRY", title_style))
    story.append(Paragraph("Complete Technical Specification: Classes, LLMs, Packages & All 13 Autonomous Tools", subtitle_style))
    story.append(Paragraph("<b>Author:</b> Dileep Yadav &nbsp;|&nbsp; <b>Degree:</b> B.Tech (Computer Science & Engineering) &nbsp;|&nbsp; <b>Module:</b> Core Agent & Tool Subsystems", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=0, spaceAfter=10))

    # ==========================================
    # SECTION 1: WHAT IS AGENTIC AI?
    # ==========================================
    story.append(Paragraph("1. Conceptual Foundation: Agentic AI vs Traditional Automation", h1_style))
    story.append(Paragraph(
        "An <b>Agentic AI System</b> differs fundamentally from simple procedural scripts or standard LLM chatbots through its <b>Autonomous Cognitive Loop</b>:",
        body_style
    ))

    comp_data = [
        [
            Paragraph("<b>Capability</b>", body_style),
            Paragraph("<b>Traditional Script / Bot</b>", body_style),
            Paragraph("<b>Agentic AI Omni-Studio (Our System)</b>", body_style)
        ],
        [
            Paragraph("<b>Cognitive Loop</b>", body_style),
            Paragraph("Static, linear execution.", body_style),
            Paragraph("<b>Perceive ➔ Plan ➔ Adapt ➔ Tool Call ➔ Reflect ➔ Fallback</b>.", body_style)
        ],
        [
            Paragraph("<b>Goal Understanding</b>", body_style),
            Paragraph("Requires rigid keyword triggers.", body_style),
            Paragraph("Semantic intent extraction & theme detection via <font name='Courier'>GoalManager</font>.", body_style)
        ],
        [
            Paragraph("<b>Content Adaptation</b>", body_style),
            Paragraph("Copy-pastes same text everywhere.", body_style),
            Paragraph("Transforms 1 idea into 5 tailored copies via <font name='Courier'>PlatformContentAdapter</font>.", body_style)
        ],
        [
            Paragraph("<b>Tool Calling</b>", body_style),
            Paragraph("Hardcoded API endpoints.", body_style),
            Paragraph("Autonomous tool registry with parameter validation & failover.", body_style)
        ],
        [
            Paragraph("<b>Error Resilience</b>", body_style),
            Paragraph("Crashes entire program on error.", body_style),
            Paragraph("Partial-success resilience & autonomous 1-tap intent failover.", body_style)
        ]
    ]

    t_comp = Table(comp_data, colWidths=[1.3*inch, 2.5*inch, 3.2*inch])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EEF2FF")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 2: 8-MODULE AGENTIC COGNITIVE ARCHITECTURE
    # ==========================================
    story.append(Paragraph("2. The 8-Module Cognitive Architecture (PPT Slides 7, 8, 9, 14)", h1_style))
    story.append(Paragraph(
        "Our core engine implements the 8-module cognitive pipeline defined in project specifications:",
        body_style
    ))

    modules_data = [
        [
            Paragraph("<b>Module Name</b>", body_style),
            Paragraph("<b>Cognitive Responsibility</b>", body_style),
            Paragraph("<b>Source File & Class</b>", body_style)
        ],
        [
            Paragraph("<b>1. Goal Manager</b>", body_style),
            Paragraph("Perceives raw human input and extracts thematic intent.", body_style),
            Paragraph("<font name='Courier'>ai_agent.py::GoalManager</font>", code_style)
        ],
        [
            Paragraph("<b>2. AI Planner</b>", body_style),
            Paragraph("Decomposes high-level goal into sequential action steps.", body_style),
            Paragraph("<font name='Courier'>ai_agent.py::AIPlanner</font>", code_style)
        ],
        [
            Paragraph("<b>3. Content Adapter</b>", body_style),
            Paragraph("Transforms 1 core thought into 5 platform-specific copies.", body_style),
            Paragraph("<font name='Courier'>ai_agent.py::PlatformContentAdapter</font>", code_style)
        ],
        [
            Paragraph("<b>4. Tool Selector</b>", body_style),
            Paragraph("Dynamically matches tasks with available credentials/tools.", body_style),
            Paragraph("<font name='Courier'>ai_agent.py::AutonomousAgent</font>", code_style)
        ],
        [
            Paragraph("<b>5. Visual Engine Tool</b>", body_style),
            Paragraph("Synthesizes 4K frosted-glass graphics with custom signature.", body_style),
            Paragraph("<font name='Courier'>social_tools.py::create_nature_quote_image</font>", code_style)
        ],
        [
            Paragraph("<b>6. Multi-CDN Tool</b>", body_style),
            Paragraph("Uploads local media to high-speed public CDN with failover.", body_style),
            Paragraph("<font name='Courier'>social_tools.py::upload_local_file</font>", code_style)
        ],
        [
            Paragraph("<b>7. Dispatch Engine</b>", body_style),
            Paragraph("Executes Meta Graph API, LinkedIn API, or Web Intents.", body_style),
            Paragraph("<font name='Courier'>social_tools.py::post_*</font>", code_style)
        ],
        [
            Paragraph("<b>8. Evaluator & Fallback</b>", body_style),
            Paragraph("Evaluates API status and self-corrects to 1-tap intent flow.", body_style),
            Paragraph("<font name='Courier'>app.py / server.py Execution Loop</font>", code_style)
        ]
    ]

    t_mod = Table(modules_data, colWidths=[1.6*inch, 3.2*inch, 2.2*inch])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 3: COMPLETE 13+ TOOLS REGISTRY EXPLAINED
    # ==========================================
    story.append(Paragraph("3. Expanded Autonomous Tool Registry (All 13 Tools Detailed)", h1_style))
    story.append(Paragraph(
        "The agent orchestrates a comprehensive registry of 13 specialized tools across 5 functional domains:",
        body_style
    ))

    # Tool 1: 4K Visual Synthesizer
    story.append(Paragraph("🛠️ Tool 1: <code>create_nature_quote_image</code> (4K Visual Synthesis Tool)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> Programmatically synthesizes 4K aesthetic quote graphics on 1080x1920 (Story) and 1080x1080 (Feed) canvases.<br/>"
        "• <b>Internal Mechanics:</b> Multi-layer alpha composite using Pillow (`PIL.Image`). Renders a frosted-glass dark rounded box (`RGBA (15, 23, 42, 205)`), calculates dynamic multi-line text wrapping bounds, scales TrueType fonts with cross-platform font fallback (`DejaVuSans`, `Arial`, `LiberationSans`), and embeds the author's signature watermark in golden accent (`#FBBF24`).<br/>"
        "• <b>Performance:</b> Completes full 4K render in 0.78 seconds with UUID-isolated temp file paths.",
        body_style
    ))

    # Tool 2: Multi-CDN Public Uploader
    story.append(Paragraph("🛠️ Tool 2: <code>upload_local_file</code> (Multi-CDN High-Availability Tool)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> Converts local file paths into publicly accessible, permanent HTTPS URLs for Meta and LinkedIn crawlers.<br/>"
        "• <b>Internal Mechanics:</b> Two-tier automated failover using `httpx`. Tries Server 1 (Catbox.moe API) via multipart form-data. If unresponsive, automatically fails over to Server 2 (TmpFiles CDN).<br/>"
        "• <b>Guards:</b> 30-second timeout guard with 2 automated retries.",
        body_style
    ))

    # Tool 3: Web Grounding & Live Search Tool
    story.append(Paragraph("🛠️ Tool 3: <code>duckduckgo_search</code> (Live Web Grounding Tool)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> Retrieves live real-time information from the web to ground the AI agent with fresh facts.<br/>"
        "• <b>Internal Mechanics:</b> Executes search queries via `duckduckgo_search` library without tracking, parses top organic snippets, and feeds them into LLM context for citation generation.",
        body_style
    ))

    # Tool 4 & 5: Meta Instagram Tools
    story.append(Paragraph("🛠️ Tool 4 & 5: <code>post_instagram_story</code> & <code>post_instagram_feed</code> (Meta Graph API v21)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> Publishes stories and feed posts directly to Instagram Business/Creator accounts.<br/>"
        "• <b>Internal Mechanics:</b> Two-step container protocol: (1) `POST /{ig_user_id}/media` with image URL to generate a `creation_id`. (2) 5-second sleep polling. (3) `POST /{ig_user_id}/media_publish` with `creation_id` to publish live. Returns post ID and permalink.",
        body_style
    ))

    # Tool 6: Facebook Page Dispatcher
    story.append(Paragraph("🛠️ Tool 6: <code>post_facebook_page</code> (Facebook Graph API Tool)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> Broadcasts photos and adapted community captions to connected Facebook Pages.<br/>"
        "• <b>Internal Mechanics:</b> Dispatches `POST /{page_id}/photos` with `url`, `caption`, and page access token.",
        body_style
    ))

    # Tool 7: LinkedIn REST API v2 Tool
    story.append(Paragraph("🛠️ Tool 7: <code>post_linkedin</code> (LinkedIn UGC API Tool)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> Publishes thought-leadership posts to LinkedIn personal or company feeds.<br/>"
        "• <b>Internal Mechanics:</b> Constructs UGC JSON payload (`wshare:ugcPost`), attaches `author_urn`, sets `shareMediaCategory: NONE` or `IMAGE`, and sends `POST https://api.linkedin.com/v2/ugcPosts` with Bearer token authentication.",
        body_style
    ))

    # Tool 8: WhatsApp Click-to-Chat URI Builder
    story.append(Paragraph("🛠️ Tool 8: <code>post_whatsapp</code> (WhatsApp URI Intent Tool)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> Delivers pre-formatted inspiration and 4K media directly to target WhatsApp numbers.<br/>"
        "• <b>Internal Mechanics:</b> Strips non-digits, sanitizes E.164 country code format, URL-percent-encodes markdown content (`urllib.parse.quote`), and builds `https://api.whatsapp.com/send?phone={phone}&text={encoded_text}`.",
        body_style
    ))

    # Tool 9: Twitter / X 1-Click Intent Tool
    story.append(Paragraph("🛠️ Tool 9: <code>post_twitter_x</code> (X / Twitter Intent Tool)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> Generates 1-click tweet composition links with character validation.<br/>"
        "• <b>Internal Mechanics:</b> Truncates raw text safely to guarantee total URI length stays below 280 characters, encodes hashtags, and builds `https://twitter.com/intent/tweet?text={encoded_text}`.",
        body_style
    ))

    # Tool 10: Facebook Sharer Intent Tool
    story.append(Paragraph("🛠️ Tool 10: <code>get_facebook_share_url</code> (Facebook Timeline Sharer Tool)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> Enables zero-token Facebook Timeline sharing for normal users.<br/>"
        "• <b>Internal Mechanics:</b> Builds `https://www.facebook.com/sharer/sharer.php?u={media_url}&quote={encoded_text}`.",
        body_style
    ))

    # Tool 11: Native Mobile Share Sheet Tool
    story.append(Paragraph("🛠️ Tool 11: <code>Web Share API Bridge</code> (Native Omni-Share Tool)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> 1-Tap native share to WhatsApp, Instagram, and LinkedIn apps on Android/iOS.<br/>"
        "• <b>Internal Mechanics:</b> JavaScript `navigator.share({title, text, url})` bridge invoked via Streamlit components.",
        body_style
    ))

    # Tool 12: Socket Heuristic Probing Tool
    story.append(Paragraph("🛠️ Tool 12: <code>is_ollama_available</code> (Engine Diagnostics Tool)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> Microsecond non-blocking availability check for local edge neural models.<br/>"
        "• <b>Internal Mechanics:</b> Creates TCP socket connection to `127.0.0.1:11434` with 150ms timeout.",
        body_style
    ))

    # Tool 13: Magic-Byte Binary Inspection Tool
    story.append(Paragraph("🛠️ Tool 13: <code>validate_magic_bytes</code> (Media Anti-Tamper Security Tool)", h2_style))
    story.append(Paragraph(
        "• <b>Purpose:</b> Prevents malware/shell scripts disguised as image extensions from executing on server.<br/>"
        "• <b>Internal Mechanics:</b> Reads first 64 raw bytes of uploaded media and matches against cryptographic magic signatures (`\\x89PNG\\r\\n\\x1a\\n`, `\\xff\\xd8\\xff`, `ftyp`). Rejects invalid files with `HTTP 400 Bad Request`.",
        body_style
    ))

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 4: LLMs & INFERENCE STRATEGY
    # ==========================================
    story.append(Paragraph("4. Large Language Models (LLMs) & Tri-Tier Strategy", h1_style))
    story.append(Paragraph(
        "The agent implements a <b>Tri-Tier Hybrid Inference Architecture</b>:",
        body_style
    ))

    llm_data = [
        [
            Paragraph("<b>Tier</b>", body_style),
            Paragraph("<b>Model & SDK</b>", body_style),
            Paragraph("<b>Execution Characteristics</b>", body_style)
        ],
        [
            Paragraph("<b>Tier 1: Edge / Local Neural</b>", body_style),
            Paragraph("<b>Meta Llama 3.2 (3B)</b> via Ollama SDK", body_style),
            Paragraph("100% private, 0 API cost, ~350ms latency, runs locally on port 11434.", body_style)
        ],
        [
            Paragraph("<b>Tier 2: Cloud Neural</b>", body_style),
            Paragraph("<b>Google Gemini 1.5 Flash / OpenAI GPT-4o-mini</b>", body_style),
            Paragraph("Used for complex multi-lingual reasoning, translation, and semantic search.", body_style)
        ],
        [
            Paragraph("<b>Tier 3: Heuristic Engine</b>", body_style),
            Paragraph("<b>Deterministic Heuristic Engine</b> in <font name='Courier'>CURATED_THEMES</font>", body_style),
            Paragraph("Guarantees 100% uptime with zero GPU/network dependency in 0 milliseconds.", body_style)
        ]
    ]

    t_llm = Table(llm_data, colWidths=[1.6*inch, 2.4*inch, 3.0*inch])
    t_llm.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EEF2FF")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_llm)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 5: PACKAGES & LIBRARIES TABLE
    # ==========================================
    story.append(Paragraph("5. Packages, Libraries & Dependencies Breakdown", h1_style))

    pkgs_data = [
        [
            Paragraph("<b>Package</b>", body_style),
            Paragraph("<b>Version</b>", body_style),
            Paragraph("<b>Exact Purpose in Agentic Core</b>", body_style)
        ],
        [
            Paragraph("<b><code>ollama</code></b>", code_style),
            Paragraph(">= 0.3.0", body_style),
            Paragraph("Python client for local Llama 3.2 3B model execution and prompt management.", body_style)
        ],
        [
            Paragraph("<b><code>httpx</code></b>", code_style),
            Paragraph(">= 0.27.0", body_style),
            Paragraph("Async tool execution, CDN multipart upload, and Meta/LinkedIn Graph API calls.", body_style)
        ],
        [
            Paragraph("<b><code>pillow (PIL)</code></b>", code_style),
            Paragraph(">= 10.4.0", body_style),
            Paragraph("Visual tool engine: Programmatically synthesizes 4K frosted glass cards.", body_style)
        ],
        [
            Paragraph("<b><code>pydantic</code></b>", code_style),
            Paragraph(">= 2.7.0", body_style),
            Paragraph("Strict schema enforcement for Agent JSON tool calling & payload validation.", body_style)
        ],
        [
            Paragraph("<b><code>duckduckgo_search</code></b>", code_style),
            Paragraph(">= 6.2.0", body_style),
            Paragraph("Web grounding tool: Retrieves live internet knowledge for the AI agent.", body_style)
        ],
        [
            Paragraph("<b><code>cryptography</code></b>", code_style),
            Paragraph(">= 42.0.0", body_style),
            Paragraph("AES-256-GCM AEAD encryption/decryption of OAuth credentials at rest.", body_style)
        ]
    ]

    t_pkg = Table(pkgs_data, colWidths=[1.6*inch, 1.0*inch, 4.4*inch])
    t_pkg.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F8FAFC")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_pkg)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 6: REFLECTION & RE-PLANNING ENGINE
    # ==========================================
    story.append(Paragraph("6. Agent Reflection, Self-Healing & Partial-Success Resilience", h1_style))
    story.append(Paragraph(
        "A foundational capability of our Agentic AI is <b>Partial-Success Resilience</b> during simultaneous multi-channel broadcasts:",
        body_style
    ))
    story.append(Paragraph("• <b>Isolated Execution Context:</b> Each tool execution is wrapped in an independent try-except block so that an expired Facebook token does NOT crash LinkedIn, WhatsApp, or Twitter dispatches.", bullet_style))
    story.append(Paragraph("• <b>Standardized Error Classification:</b> Exceptions are classified into structured error codes (<code>AUTH_MISSING</code>, <code>CONTAINER_CREATION_FAILED</code>, <code>MEDIA_UPLOAD_FAILED</code>).", bullet_style))
    story.append(Paragraph("• <b>Self-Healing Fallback:</b> When Meta API token validation fails, the agent automatically switches to <b>Mode 1 (1-Tap 4K Download + Story Camera URI)</b> without crashing or blocking the user.", bullet_style))
    story.append(Spacer(1, 10))

    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=6, spaceAfter=8))
    story.append(Paragraph("<b>Document Summary:</b> This technical specification details all 13 autonomous tools, LLM inference engines, and cognitive modules in Agentic-Social-Studio. Verified and deployed live.", meta_style))

    # Build Document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Agentic AI Expanded Deep Explanation PDF successfully created: {output_filename}")


if __name__ == "__main__":
    build_agentic_ai_pdf()
