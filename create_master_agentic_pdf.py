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

class MasterNumberedCanvas(canvas.Canvas):
    """Canvas that adds Page X of Y and formal running headers/footers to every page."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Running Header (Page 2 onwards)
        if self._pageNumber > 1:
            self.drawString(54, 752, "AGENTIC AI OMNI-STUDIO — MASTER THESIS & PRESENTATION GUIDE")
            self.drawRightString(612 - 54, 752, "B.Tech Final Year Capstone Project")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 746, 612 - 54, 746)

        # Running Footer (All pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(54, 45, 612 - 54, 45)
        
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Author: Dileep Yadav  |  Department: Computer Science & Engineering  |  Project: Agentic-Social-Studio")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(612 - 54, 32, page_str)
        self.restoreState()


def build_master_agentic_pdf(output_filename="Agentic_AI_Core_Deep_Explanation.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Elegant Color Palette
    PRIMARY = colors.HexColor("#0F172A")    # Slate 900 (Deep Navy/Black)
    SECONDARY = colors.HexColor("#312E81")  # Indigo 900
    ACCENT_BLUE = colors.HexColor("#1D4ED8")# Blue 700
    ACCENT_GOLD = colors.HexColor("#B45309")# Amber 700
    TEXT_DARK = colors.HexColor("#1E293B")  # Slate 800
    TEXT_MUTED = colors.HexColor("#475569") # Slate 600
    BG_CARD = colors.HexColor("#F8FAFC")    # Slate 50

    # Custom Typography Styles (No unicode emojis to prevent black box glitch)
    title_style = ParagraphStyle(
        'DocTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=ACCENT_BLUE,
        spaceAfter=8
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=TEXT_MUTED,
        spaceAfter=12
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=SECONDARY,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=ACCENT_BLUE,
        spaceBefore=9,
        spaceAfter=4,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'Heading3_Custom',
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=13,
        textColor=ACCENT_GOLD,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
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
        leading=13.5,
        textColor=TEXT_DARK,
        leftIndent=14,
        firstLineIndent=-9,
        spaceAfter=3
    )

    callout_style = ParagraphStyle(
        'Callout_Custom',
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor("#1E293B")
    )

    story = []

    # ==========================================
    # COVER / HEADER
    # ==========================================
    story.append(Paragraph("AGENTIC AI CORE ENGINE — MASTER HINGLISH EXPLANATION", title_style))
    story.append(Paragraph("Complete Technical Architecture: Cognitive Loop, Codebase Walkthrough, LLMs, 13 Tools & Viva Defense", subtitle_style))
    story.append(Paragraph("<b>Author:</b> Dileep Yadav &nbsp;|&nbsp; <b>Degree:</b> B.Tech (Computer Science & Engineering) &nbsp;|&nbsp; <b>Project:</b> Agentic-Social-Studio", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=0, spaceAfter=10))

    # ==========================================
    # SECTION 1: AGENTIC AI DEFINITION & ANALOGIES
    # ==========================================
    story.append(Paragraph("SECTION 1: Agentic AI Kya Hota Hai? (Asli Zindagi Ke 3 Udaharan)", h1_style))
    story.append(Paragraph(
        "Agentic AI ka seedha matlab hai ek aisa Artificial Intelligence system jo sirf sawalon ke jawab nahi deta, balki <b>ek insaan ki tarah khud soch kar, planning karke aur alag-alag tools ko use karke poora kaam complete karta hai</b>.",
        body_style
    ))

    story.append(Paragraph("<b>[Udaharan 1] Smart Executive Manager vs Simple Calculator:</b>", h2_style))
    story.append(Paragraph(
        "• <b>Simple Script / Chatbot:</b> Agar aap chatbot se kahenge '50 * 20 kitna hota hai', toh woh 1000 bata dega. Lekin agar aap use kahenge 'mere liye 5 social media par post daal do', toh woh crash ho jayega kyunki use tool chalana nahi aata.<br/>"
        "• <b>Hamara Agentic AI Assistant:</b> Yeh ek expert digital manager ki tarah hai. Aap use sirf ek line bolte hain: <i>'Aaj ka inspiring thought sabhi jagah broadcast kar do'</i> — toh woh pehle thought ka theme pehchanta hai, 4K graphic poster design karta hai, LinkedIn ke liye corporate English likhta hai, WhatsApp ke liye friendly message banata hai, aur bina aapke haath lagaye har jagah publish kar deta hai!",
        body_style
    ))

    story.append(Paragraph("<b>[Udaharan 2] Dynamic Copy Adaptation (Slide 8 Concept):</b>", h2_style))
    story.append(Paragraph(
        "Maan lijiye aapko ek khabar sunani hai. Jab aap apne <b>College Principal ya Boss</b> se baat karte hain, toh formal language bolte hain (LinkedIn). Jab aap <b>Friends Group</b> me baat karte hain, toh casual bolte hain (WhatsApp). Aur jab aap <b>Public Notice Board</b> par likhte hain, toh short bullet points likhte hain (Twitter/X). Hamara Agentic AI theek yahi kaam automatically karta hai — 1 single thought ko 5 alag-alag tones me convert karta hai taaki kahi par bhi copy-paste na lage!",
        body_style
    ))

    story.append(Paragraph("<b>[Udaharan 3] Self-Healing (Rasta Badal Kar Kaam Poora Karna):</b>", h2_style))
    story.append(Paragraph(
        "Agar aapko Delhi se Mumbai jana hai aur flight cancel ho jaye, toh ek samajhdaar insaan ghar wapas aane ke bajaye Train ya Cab pakad kar Mumbai pahuchta hai. Theek waise hi, agar Meta API ka token expire ho jaye, toh hamara AI agent crash hone ke bajaye turant <b>1-Tap 4K Download + Story Camera flow</b> par switch kar deta hai!",
        body_style
    ))

    story.append(Spacer(1, 8))

    # ==========================================
    # COMPARISON TABLE
    # ==========================================
    comp_data = [
        [
            Paragraph("<b>Paimana (Dimension)</b>", body_style),
            Paragraph("<b>Sadharan Script / Chatbot</b>", body_style),
            Paragraph("<b>Hamara Agentic AI Omni-Studio</b>", body_style)
        ],
        [
            Paragraph("<b>Kaam Ka Tareeqa</b>", body_style),
            Paragraph("Sirf fix if-else rules par chalta hai.", body_style),
            Paragraph("<b>Perceive -> Plan -> Adapt -> Tool Call -> Reflect -> Fallback</b>", body_style)
        ],
        [
            Paragraph("<b>Vichar Samajhna (Goal)</b>", body_style),
            Paragraph("Sirf fix exact keyword par chalta hai.", body_style),
            Paragraph("Semantic intent aur theme (Success, Tech, Mindset) khud pehchanta hai.", body_style)
        ],
        [
            Paragraph("<b>Content Formatting</b>", body_style),
            Paragraph("Ek hi same text har jagah copy-paste.", body_style),
            Paragraph("1 quote se 5 distinct copy banata hai (Slide 8 Concept).", body_style)
        ],
        [
            Paragraph("<b>Tools Ka Istemal</b>", body_style),
            Paragraph("Tools use karne ki shamta nahi hoti.", body_style),
            Paragraph("Pillow 4K, Multi-CDN, Meta API, LinkedIn API, WhatsApp ko autonomously call karta hai.", body_style)
        ],
        [
            Paragraph("<b>Galti Aane Par (Resilience)</b>", body_style),
            Paragraph("Ek error aate hi poora program crash.", body_style),
            Paragraph("Partial-success resilience aur automatic 1-tap mode failover.", body_style)
        ]
    ]

    t_comp = Table(comp_data, colWidths=[1.4*inch, 2.4*inch, 3.2*inch])
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
    # SECTION 2: 8 COGNITIVE MODULES
    # ==========================================
    story.append(Paragraph("SECTION 2: Agentic AI Ke 8 Dimagi Modules (PPT Slides 7, 8, 9, 14)", h1_style))
    story.append(Paragraph(
        "Hamara Agentic Core 8 interconnected cognitive modules par bana hai jo aapas me milkar kaam karte hain:",
        body_style
    ))

    modules_data = [
        [Paragraph("<b>Module Ka Naam</b>", body_style), Paragraph("<b>Aam Bhasha Me Iska Kaam</b>", body_style), Paragraph("<b>Source File & Class</b>", body_style)],
        [Paragraph("<b>1. Goal Manager</b>", body_style), Paragraph("User ke vichar ka core theme (Success, Innovation, Mindset) pehchanna.", body_style), Paragraph("<font name='Courier'>ai_agent.py::GoalManager</font>", code_style)],
        [Paragraph("<b>2. AI Planner</b>", body_style), Paragraph("Goal ko 4 sequential steps me todna (Plan banana).", body_style), Paragraph("<font name='Courier'>ai_agent.py::AIPlanner</font>", code_style)],
        [Paragraph("<b>3. Content Adapter</b>", body_style), Paragraph("1 quote ko 5 platform-tailored copies me badalna (Slide 8).", body_style), Paragraph("<font name='Courier'>ai_agent.py::PlatformContentAdapter</font>", code_style)],
        [Paragraph("<b>4. Tool Selector</b>", body_style), Paragraph("Decide karna ki kaunsa tool (API ya 1-Tap) chalana hai.", body_style), Paragraph("<font name='Courier'>ai_agent.py::AutonomousAgent</font>", code_style)],
        [Paragraph("<b>5. Visual Engine Tool</b>", body_style), Paragraph("4K frosted-glass graphic card aur custom signature watermark render karna.", body_style), Paragraph("<font name='Courier'>social_tools.py::create_nature_quote_image</font>", code_style)],
        [Paragraph("<b>6. Multi-CDN Tool</b>", body_style), Paragraph("Local photo ko high-speed public HTTPS URL me convert karna.", body_style), Paragraph("<font name='Courier'>social_tools.py::upload_local_file</font>", code_style)],
        [Paragraph("<b>7. Dispatch Engine</b>", body_style), Paragraph("Meta API, LinkedIn API ya Web Intents se live broadcast karna.", body_style), Paragraph("<font name='Courier'>social_tools.py::post_*</font>", code_style)],
        [Paragraph("<b>8. Evaluator & Fallback</b>", body_style), Paragraph("Post status evaluate karna aur token fail hone par 1-tap me switch karna.", body_style), Paragraph("<font name='Courier'>app.py Execution Loop</font>", code_style)]
    ]

    t_mod = Table(modules_data, colWidths=[1.5*inch, 3.2*inch, 2.3*inch])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 3: CODEBASE WALKTHROUGH
    # ==========================================
    story.append(Paragraph("SECTION 3: Codebase Walkthrough (Har Ek Class Aur Function Ka Deep Breakdown)", h1_style))

    # Class 1
    story.append(Paragraph("Class 1: <code>GoalManager</code> (Vichar Samajhne Ka Engine)", h2_style))
    story.append(Paragraph("• <b>Function:</b> <font name='Courier'>understand_goal(raw_input: str) -> Dict[str, Any]</font>", body_style))
    story.append(Paragraph("• <b>Yeh Kaise Kaam Karta Hai:</b> Jab user koi text likhta hai ya blank chhodta hai, yeh function unhe clean karta hai. Uske baad semantic keyword scan karta hai: agar words me <i>'tech', 'ai', 'innovat', 'future', 'code'</i> mile toh theme <b>'innovation'</b> banti hai; agar <i>'mind', 'dream', 'focus', 'peace'</i> mile toh <b>'mindset'</b> banti hai; aur default <b>'success'</b> banti hai. Iske sath yeh UTC timestamp aur 5 target platforms attach karke ek structured dictionary return karta hai.", body_style))

    # Class 2
    story.append(Paragraph("Class 2: <code>AIPlanner</code> (Task Plan Banane Ka Engine)", h2_style))
    story.append(Paragraph("• <b>Function:</b> <font name='Courier'>create_plan(goal_obj: Dict[str, Any]) -> str</font>", body_style))
    story.append(Paragraph("• <b>Yeh Kaise Kaam Karta Hai:</b> Yeh pehle check karta hai ki local LLM (Meta Llama 3.2 3B) available hai ya nahi (<font name='Courier'>is_ollama_available()</font>). Agar LLM available hai, toh system prompt dekar 4 numbered steps banwata hai. Agar LLM offline ho, toh hamara <b>Deterministic Heuristic Planner</b> 0 millisecond me fallback karke yeh 4 steps return karta hai:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1. Analyze core message intent & extract theme.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;2. Generate 4K aesthetic visual poster with custom signature.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;3. Adapt message copy for Instagram, LinkedIn, Facebook, WhatsApp & Twitter.<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;4. Broadcast across active channels with individual platform confirmation.", body_style))

    # Class 3
    story.append(Paragraph("Class 3: <code>PlatformContentAdapter</code> (5 Alag Posts Banane Ka Engine - Slide 8)", h2_style))
    story.append(Paragraph("• <b>Function:</b> <font name='Courier'>adapt_all_platforms(content, author, media_url) -> Dict[str, str]</font>", body_style))
    story.append(Paragraph("• <b>Har Platform Ka Rule:</b><br/>"
        "&nbsp;&nbsp;• <b>Instagram Copy:</b> Quotes text with decorative markers, motivational encouragement, and 7 targeted hashtags (<code>#Motivation #DailyWisdom #GrowthMindset #AgenticAI</code>).<br/>"
        "&nbsp;&nbsp;• <b>LinkedIn Copy:</b> Formal thought-leadership tone, executive takeaway context, signature attribution, and corporate growth hashtags (<code>#Leadership #Productivity #FutureOfWork</code>).<br/>"
        "&nbsp;&nbsp;• <b>Facebook Copy:</b> Relatable community discussion prompt (<i>'Do you agree with this? Share your thoughts below!'</i>).<br/>"
        "&nbsp;&nbsp;• <b>WhatsApp Copy:</b> Clean bold/italic markdown (<code>*Daily Inspiration*</code>, <code>_-- Author_</code>) with direct 4K CDN link.<br/>"
        "&nbsp;&nbsp;• <b>Twitter / X Copy:</b> Punchy, high-impact tweet strictly bounded under 275 characters with safe truncation.", body_style))

    # Class 4
    story.append(Paragraph("Class 4: <code>AutonomousAgent</code> (Master Cognitive Orchestrator)", h2_style))
    story.append(Paragraph("• <b>Function 1:</b> <font name='Courier'>process(user_text, author, media_url)</font> ➔ Goal, Plan aur Content Adaptation ko unroll karke final execution packet banata hai.<br/>"
        "• <b>Function 2:</b> <font name='Courier'>generate_fresh_quote(theme)</font> ➔ Local Llama 3.2 ya curated high-impact wisdom library (<font name='Courier'>CURATED_THEMES</font>) se naya thought nikalta hai.", body_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 4: ALL 13 TOOLS FULLY EXPLAINED
    # ==========================================
    story.append(Paragraph("SECTION 4: System Ke Sabhi 13 Tools Ka Complete Technical Breakdown", h1_style))
    story.append(Paragraph("Hamara AI Agent niche diye gaye 13 tools ko autonomously execute karta hai:", body_style))

    tools_deep = [
        ("Tool 1: create_nature_quote_image() (4K Visual Synthesis Tool)",
         "social_tools.py", "Pillow (PIL)",
         "Yeh tool code ke through 1080x1920 (Story - 9:16) aur 1080x1080 (Feed - 1:1) 4K canvas render karta hai. Isme Frosted Glass Box (RGBA 15,23,42,205) lagata hai, dynamic text width measure karke words ko 2-4 lines me wrap karta hai, scalable TrueType fonts (DejaVuSans, Arial) render karta hai, aur golden accent (#FBBF24) me user ka signature watermark (-- Dileep Yadav) embed karta hai (0.78 seconds me complete)."),

        ("Tool 2: upload_local_file() (Multi-CDN High-Availability Tool)",
         "social_tools.py", "httpx",
         "Meta aur LinkedIn local C:\\ paths ko accept nahi karte, unhe public HTTPS URL chahiye. Yeh tool photo ko Catbox.moe API par multipart upload karta hai. Agar Catbox busy ho, toh auto-failover karke TmpFiles CDN par upload karta hai (30s timeout guard aur 2 retries ke sath)."),

        ("Tool 3: validate_magic_bytes() (Media Anti-Tamper Security Tool)",
         "backend/server.py", "Python Built-in",
         "Hacker virus scripts (.exe ya .sh) ka naam badal kar .png na upload karein, isliye yeh tool file ke starting 64 raw bytes (Magic Bytes) check karta hai (PNG: \\x89PNG\\r\\n\\x1a\\n, JPEG: \\xff\\xd8\\xff, MP4: ftyp). Fake file ko HTTP 400 Bad Request se drop karta hai."),

        ("Tool 4: post_instagram_feed() & post_instagram_story() (Meta Graph API v21)",
         "social_tools.py", "httpx",
         "Meta Graph API v21 ke sath 2-step container flow execute karta hai: (1) POST /{ig_id}/media se image URL bhej kar creation_id leta hai, (2) 5s sleep polling karta hai, (3) POST /{ig_id}/media_publish se creation_id bhej kar live post kar deta hai."),

        ("Tool 5: post_facebook_page() (Facebook Graph API Tool)",
         "social_tools.py", "httpx",
         "Connected Facebook Page par live photo aur community discussion caption publish karta hai (POST /{page_id}/photos)."),

        ("Tool 6: post_linkedin() (LinkedIn REST API v2 Tool)",
         "social_tools.py", "httpx",
         "LinkedIn ke new UGC Post API (wshare:ugcPost) me JSON payload banata hai, author URN attach karta hai aur Bearer OAuth token ke sath live feed par send karta hai."),

        ("Tool 7: post_whatsapp() (WhatsApp URI Intent Tool)",
         "social_tools.py", "urllib.parse",
         "Phone number ko E.164 (+91...) format me clean karta hai, text ko percent-encode karta hai aur https://api.whatsapp.com/send?phone=... link banata hai."),

        ("Tool 8: post_twitter_x() (X / Twitter Intent Tool)",
         "social_tools.py", "urllib.parse",
         "280-character boundary check karta hai, safe string slicing karta hai aur 1-click tweet URL (twitter.com/intent/tweet?text=...) banata hai."),

        ("Tool 9: get_facebook_share_url() & get_linkedin_share_url() (Web Sharer)",
         "social_tools.py", "urllib.parse",
         "Bina developer token ke normal users ke liye 1-click Facebook Sharer aur LinkedIn Offsite Sharer links create karta hai."),

        ("Tool 10: Web Share API Bridge (Native Mobile Share Sheet)",
         "app.py", "JavaScript / Streamlit",
         "Mobile browser ke native navigator.share() ko call karta hai jisse phone ke bottom se direct WhatsApp, Instagram, FB share tray open hoti hai."),

        ("Tool 11: duckduckgo_search (Live Web Grounding Tool)",
         "ai_agent.py", "duckduckgo_search",
         "Internet se live taza information search karke AI agent ko latest facts se ground karta hai."),

        ("Tool 12: is_ollama_available() (Socket Diagnostics Tool)",
         "ai_agent.py", "socket (stdlib)",
         "150 milliseconds me TCP socket connect karke check karta hai ki local Llama 3.2 AI model port 11434 par chal raha hai ya nahi."),

        ("Tool 13: AES-256-GCM Cryptographic Tool (Token Security)",
         "backend/crypto.py", "cryptography",
         "Database me sabhi social media access tokens ko 12-byte nonce aur 16-byte auth tag ke sath AES-256-GCM se encrypt karta hai (Zero Plaintext Token).")
    ]

    for t_name, t_file, t_lib, t_desc in tools_deep:
        story.append(Paragraph(f"<b>[Tool] {t_name}</b>", h2_style))
        story.append(Paragraph(f"<b>File:</b> <font name='Courier'>{t_file}</font> &nbsp;|&nbsp; <b>Library:</b> <font name='Courier'>{t_lib}</font>", h3_style))
        story.append(Paragraph(t_desc, body_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))

    # ==========================================
    # SECTION 5: LLM INFERENCE STRATEGY
    # ==========================================
    story.append(Paragraph("SECTION 5: LLM Models & Tri-Tier Inference Strategy", h1_style))
    story.append(Paragraph("Hamara AI Agent ek <b>Tri-Tier Hybrid LLM Strategy</b> par chalta hai:", body_style))

    llm_data = [
        [Paragraph("<b>Tier</b>", body_style), Paragraph("<b>Model & SDK</b>", body_style), Paragraph("<b>Kaam Aur Khasiyat</b>", body_style)],
        [
            Paragraph("<b>Tier 1: Edge / Local Neural</b>", body_style),
            Paragraph("<b>Meta Llama 3.2 (3B)</b> via Ollama", body_style),
            Paragraph("100% private, 0 API cost, ~350ms latency. Local machine par bina internet chalta hai.", body_style)
        ],
        [
            Paragraph("<b>Tier 2: Cloud Neural</b>", body_style),
            Paragraph("<b>Google Gemini 1.5 / GPT-4o-mini</b>", body_style),
            Paragraph("Complex reasoning, multi-language translation aur deep semantic search ke liye.", body_style)
        ],
        [
            Paragraph("<b>Tier 3: Heuristic Engine</b>", body_style),
            Paragraph("<b>Deterministic Fallback</b> in <font name='Courier'>CURATED_THEMES</font>", body_style),
            Paragraph("100% Uptime guarantee. Internet ya GPU band hone par bhi 0 millisecond me kaam karta hai.", body_style)
        ]
    ]

    t_llm = Table(llm_data, colWidths=[1.6*inch, 2.3*inch, 3.1*inch])
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
    # SECTION 6: SELF-HEALING & RESILIENCE
    # ==========================================
    story.append(Paragraph("SECTION 6: Self-Healing & Partial-Success Resilience (Crash-Proof Architecture)", h1_style))
    story.append(Paragraph(
        "Jab ek sath 5 platforms par post kiya jata hai, toh hamara AI system <b>Partial-Success Resilience</b> follow karta hai:<br/>"
        "1. <b>Isolated Try-Except Blocks:</b> Har platform ka code alag block me wrapped hai. Agar Facebook ka token expire ho jaye, toh yeh LinkedIn, WhatsApp ya Twitter ko block ya crash nahi karta.<br/>"
        "2. <b>Standardized Error Codes:</b> Errors ko structured code me classify karta hai (<code>AUTH_MISSING</code>, <code>CONTAINER_CREATION_FAILED</code>, <code>MEDIA_UPLOAD_FAILED</code>).<br/>"
        "3. <b>Autonomous 1-Tap Fallback:</b> Token fail hone par screen par user ke liye <b>1-Tap 4K Download + Direct Story Camera flow</b> automatically open kar deta hai!",
        body_style
    ))
    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 7: VIVA Q&A DEFENSE
    # ==========================================
    story.append(Paragraph("SECTION 7: Top 10 Viva Questions & Hinglish Model Answers (Examiner Defense)", h1_style))

    viva_qa = [
        ("Q1: Is project ko 'Agentic AI' kyu kehte hain, yeh simple script se alag kaise hai?",
         "Sir, normal script linear hoti hai aur hardcoded rules par chalti hai. Agentic AI ek cognitive loop follow karta hai: yeh goal samajhta hai (Perceive), plan banata hai (Plan), platform ke hisaab se copy adapt karta hai (Adapt), available credentials dekh kar tool select karta hai (Tool Selection), aur error aane par khud 1-tap intent me failover karta hai (Self-Correction & Fallback)."),

        ("Q2: Content Adaptation Engine (Slide 8 Concept) kyu banaya gaya?",
         "Sir, har social media ka algorithm aur audience alag hai. LinkedIn par corporate bullet points chalte hain, Instagram par emojis aur hashtags chalte hain, aur Twitter par 280 character limit hoti hai. Hamara adapter 1 raw quote se 5 distinct copy banata hai taaki kahi par bhi copy-paste na lage."),

        ("Q3: AES-256-GCM encryption kyu use kiya, hashing kyu nahi ki?",
         "Sir, Hashing one-way hoti hai jisse original token wapas nahi mil sakta aur Meta/LinkedIn API call nahi ho payegi. AES-256-GCM authenticated symmetric encryption hai jo 12-byte nonce aur 16-byte auth tag ke sath data encrypt karta hai, jisse database chori hone par bhi token 100% safe rehte hain."),

        ("Q4: Multi-CDN uploader ki kya zaroorat thi?",
         "Sir, Meta Graph API aur LinkedIn API local C:\\ file paths accept nahi karte; unhe publicly accessible HTTPS link chahiye hota hai. Hamara uploader local 4K image ko 1.2s me Catbox/TmpFiles par upload karke live HTTPS URL generate karta hai."),

        ("Q5: Magic Bytes validation file extension se behtar kyu hai?",
         "Sir, koi bhi attacker script.sh ya malware.exe ka naam badal kar image.png kar sakta hai. Hamara server file ke starting 64 raw bytes (Magic Bytes) check karta hai, isliye fake files execute nahi ho sakti.")
    ]

    for q, a in viva_qa:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(f"<b>Answer:</b> {a}", body_style))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=4, spaceAfter=6))
    story.append(Paragraph("<b>Document Summary:</b> Complete Hinglish technical specification of Agentic-Social-Studio. Formatted for B.Tech Thesis, Project Reports, and Presentation Defense. Verified and Deployed Live.", meta_style))

    # Build Document using MasterNumberedCanvas
    doc.build(story, canvasmaker=MasterNumberedCanvas)
    print(f"Master Hinglish Deep Explanation PDF successfully created: {output_filename}")


if __name__ == "__main__":
    build_master_agentic_pdf()
