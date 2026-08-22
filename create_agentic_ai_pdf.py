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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#475569"))
        
        # Header (Only on page 2 onwards)
        if self._pageNumber > 1:
            self.drawString(54, 750, "AGENTIC AI OMNI-STUDIO — SARAL HINGLISH EXPLANATION GUIDE")
            self.drawRightString(612 - 54, 750, "B.Tech Presentation & Thesis Master Guide")
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


def build_hinglish_agentic_pdf(output_filename="Agentic_AI_Core_Deep_Explanation.pdf"):
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
    PRIMARY = colors.HexColor("#1E1B4B")     # Deep Navy
    SECONDARY = colors.HexColor("#4338CA")   # Indigo
    ACCENT_CYAN = colors.HexColor("#0284C7") # Sky Blue
    ACCENT_GOLD = colors.HexColor("#B45309") # Warm Amber
    TEXT_DARK = colors.HexColor("#0F172A")   # Slate 900
    TEXT_MUTED = colors.HexColor("#475569")  # Slate 600

    # Custom Typography Styles
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
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=SECONDARY,
        spaceAfter=10
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
        fontSize=12.5,
        leading=16,
        textColor=PRIMARY,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=SECONDARY,
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_DARK,
        spaceAfter=4
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        fontName='Courier',
        fontSize=7.5,
        leading=10.5,
        textColor=colors.HexColor("#0F172A")
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=TEXT_DARK,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    story = []

    # ==========================================
    # COVER / HEADER
    # ==========================================
    story.append(Paragraph("🌌 AGENTIC AI CORE ENGINE — COMPLETE HINGLISH GUIDE", title_style))
    story.append(Paragraph("Aam Bhasha Me Deep Technical Explanation: Classes, Functions, LLMs & All 13 Tools", subtitle_style))
    story.append(Paragraph("<b>Author:</b> Dileep Yadav &nbsp;|&nbsp; <b>Degree:</b> B.Tech (Computer Science & Engineering) &nbsp;|&nbsp; <b>Project:</b> Agentic-Social-Studio", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=SECONDARY, spaceBefore=0, spaceAfter=8))

    # ==========================================
    # SECTION 1: AGENTIC AI KYA HOTA HAI?
    # ==========================================
    story.append(Paragraph("1. Agentic AI Kya Hota Hai? (Asli Zindagi Ke Udaharan Se Samjhein)", h1_style))
    story.append(Paragraph(
        "<b>Asan Udaharan:</b> Maan lijiye aapke paas ek <b>Smart Executive Assistant (Manager)</b> hai. Agar aap use sirf itna bolein: <i>'Aaj ka motivation sabhi jagah share kar do'</i> — toh woh khud sochta hai ki kaisa quote chahiye, 4K photo design karta hai, LinkedIn ke liye formal likhta hai, WhatsApp ke liye friendly likhta hai, aur sabhi jagah post kar deta hai. Agar koi website down ho, toh dusra rasta nikalta hai. <b>Isi 'Swatantra Soch aur Kaam Karne Ki Shamta' ko Agentic AI kehte hain!</b>",
        body_style
    ))

    comp_data = [
        [
            Paragraph("<b>Feature</b>", body_style),
            Paragraph("<b>Normal Script / Chatbot</b>", body_style),
            Paragraph("<b>Hamara Agentic AI Engine</b>", body_style)
        ],
        [
            Paragraph("<b>Kaam Ka Tareeqa</b>", body_style),
            Paragraph("Sirf fix rules par chalta hai.", body_style),
            Paragraph("<b>Goal Samajhta hai ➔ Plan banata hai ➔ Copy adapt karta hai ➔ Tool call karta hai ➔ Error aane par Self-Heal karta hai</b>.", body_style)
        ],
        [
            Paragraph("<b>Content Copy-Paste</b>", body_style),
            Paragraph("Wahi same text har jagah daalta hai.", body_style),
            Paragraph("1 quote se 5 alag-alag tone wali post banata hai (Slide 8 Concept).", body_style)
        ],
        [
            Paragraph("<b>Error Handling</b>", body_style),
            Paragraph("Token fail hone par pura program crash.", body_style),
            Paragraph("Khud 1-Tap Intent Mode me switch ho jata hai (Zero Crash).", body_style)
        ]
    ]

    t_comp = Table(comp_data, colWidths=[1.3*inch, 2.5*inch, 3.2*inch])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EEF2FF")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 8))

    # ==========================================
    # SECTION 2: 8 COGNITIVE MODULES
    # ==========================================
    story.append(Paragraph("2. Agentic AI Ke 8 Dimagi Modules (PPT Slides 7, 8, 9, 14)", h1_style))
    story.append(Paragraph("Hamare AI Agent ke andar 8 main hisse kaam karte hain:", body_style))

    modules_data = [
        [Paragraph("<b>Module</b>", body_style), Paragraph("<b>Aam Bhasha Me Kaam</b>", body_style), Paragraph("<b>Code File</b>", body_style)],
        [Paragraph("<b>1. Goal Manager</b>", body_style), Paragraph("User ke vichar ka theme pehchanta hai (Success, Tech, Mindset).", body_style), Paragraph("<font name='Courier'>ai_agent.py::GoalManager</font>", code_style)],
        [Paragraph("<b>2. AI Planner</b>", body_style), Paragraph("Goal ko 4 sequential steps me divide karta hai.", body_style), Paragraph("<font name='Courier'>ai_agent.py::AIPlanner</font>", code_style)],
        [Paragraph("<b>3. Content Adapter</b>", body_style), Paragraph("1 thought ko 5 alag social media formats me badalta hai.", body_style), Paragraph("<font name='Courier'>ai_agent.py::PlatformContentAdapter</font>", code_style)],
        [Paragraph("<b>4. Tool Selector</b>", body_style), Paragraph("Sahi credentials dekh kar decide karta hai ki kaunsa tool chalana hai.", body_style), Paragraph("<font name='Courier'>ai_agent.py::AutonomousAgent</font>", code_style)],
        [Paragraph("<b>5. Visual Engine Tool</b>", body_style), Paragraph("4K frosted-glass graphic card banata hai watermark ke sath.", body_style), Paragraph("<font name='Courier'>social_tools.py::create_nature_quote_image</font>", code_style)],
        [Paragraph("<b>6. Multi-CDN Tool</b>", body_style), Paragraph("Local photo ko public HTTPS link me convert karta hai.", body_style), Paragraph("<font name='Courier'>social_tools.py::upload_local_file</font>", code_style)],
        [Paragraph("<b>7. Dispatch Engine</b>", body_style), Paragraph("Meta API, LinkedIn API ya Web Intents se post karta hai.", body_style), Paragraph("<font name='Courier'>social_tools.py::post_*</font>", code_style)],
        [Paragraph("<b>8. Evaluator & Fallback</b>", body_style), Paragraph("Error aane par khud 1-tap mode me switch karta hai.", body_style), Paragraph("<font name='Courier'>app.py Execution Loop</font>", code_style)]
    ]

    t_mod = Table(modules_data, colWidths=[1.5*inch, 3.3*inch, 2.2*inch])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E1")),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 8))

    # ==========================================
    # SECTION 3: CODE CLASSES & FUNCTIONS
    # ==========================================
    story.append(Paragraph("3. Core Code Classes & Functions Ka Deep Breakdown", h1_style))

    story.append(Paragraph("🔹 <b>Class 1: <code>GoalManager</code> (Vichar Samajhne Ka Engine)</b>", h2_style))
    story.append(Paragraph("• <b>Function:</b> <font name='Courier'>understand_goal(raw_input)</font><br/>• <b>Explanation:</b> Yeh user ke text me se keywords dhoondhta hai. Agar text me 'tech', 'ai', 'innovat' ho toh theme <b>'innovation'</b> banti hai; agar 'mind', 'focus', 'peace' ho toh <b>'mindset'</b>; warna <b>'success'</b> banti hai. Yeh ISO timestamp aur 5 platforms attach karta hai.", body_style))

    story.append(Paragraph("🔹 <b>Class 2: <code>AIPlanner</code> (Task Plan Banane Ka Engine)</b>", h2_style))
    story.append(Paragraph("• <b>Function:</b> <font name='Courier'>create_plan(goal_obj)</font><br/>• <b>Explanation:</b> Yeh pehle check karta hai ki local LLM (Llama 3.2) chal raha hai ya nahi. Agar chal raha hai toh usse 4 steps banwata hai; agar offline ho toh deterministic fallback se 0 millisecond me 4-step plan deta hai.", body_style))

    story.append(Paragraph("🔹 <b>Class 3: <code>PlatformContentAdapter</code> (5 Alag Posts Banane Ka Engine - Slide 8)</b>", h2_style))
    story.append(Paragraph("• <b>Function:</b> <font name='Courier'>adapt_all_platforms(content, author, media_url)</font><br/>• <b>Instagram Copy:</b> Emojis (✨), motivational context aur 7 trending hashtags (#MindsetMatters).<br/>• <b>LinkedIn Copy:</b> Formal corporate tone, leadership context aur professional hashtags (#Leadership).<br/>• <b>Facebook Copy:</b> Community question ('Do you agree with this? Share below! 👇').<br/>• <b>WhatsApp Copy:</b> Bold markdown (*Daily Inspiration*) aur direct 4K CDN link.<br/>• <b>Twitter/X Copy:</b> 280-character limit ke andar bounded crisp tweet.", body_style))

    story.append(Paragraph("🔹 <b>Class 4: <code>AutonomousAgent</code> (Master Orchestrator)</b>", h2_style))
    story.append(Paragraph("• <b>Functions:</b> <font name='Courier'>process()</font> Goal, Plan aur Content ko combine karta hai. <font name='Courier'>generate_fresh_quote()</font> naye inspiring quotes generate karta hai.", body_style))

    story.append(Spacer(1, 8))

    # ==========================================
    # SECTION 4: ALL 13 TOOLS DETAILED IN HINGLISH
    # ==========================================
    story.append(Paragraph("4. System Ke Sabhi 13 Tools Ka Saral Hinglish Explanation", h1_style))

    tools_exp = [
        ("Tool 1: create_nature_quote_image() (4K Visual Generator)",
         "Pillow library se 1080x1920 4K image banata hai. Isme Frosted Glass Box (RGBA 15,23,42,205), scalable TrueType fonts aur niche golden color me user ka signature watermark (-- Dileep Yadav) lagata hai."),
        
        ("Tool 2: upload_local_file() (Multi-CDN High-Speed Uploader)",
         "Meta aur LinkedIn ko image ke liye public link chahiye hota hai. Yeh tool local photo ko Catbox.moe API par upload karke instant HTTPS URL banata hai. Agar Catbox busy ho toh TmpFiles par auto-switch hota hai."),
        
        ("Tool 3: validate_magic_bytes() (Media Anti-Tamper Security Tool)",
         "Hacker virus script ko .png bana kar upload na kare, isliye yeh tool file ke starting 64 raw bytes (Magic Bytes) check karta hai (PNG ke liye \\x89PNG). Fake file hone par HTTP 400 Bad Request se reject karta hai."),
        
        ("Tool 4: post_instagram_story() & post_instagram_feed() (Meta Graph API)",
         "Meta Graph API v21 ke sath 2-step container flow chalata hai: Pehle /{ig_id}/media se creation_id leta hai, 5 second wait karta hai, fir /{ig_id}/media_publish se live Instagram par photo post karta hai."),
        
        ("Tool 5: post_facebook_page() (Facebook Graph API Tool)",
         "Connected Facebook Page par live photo aur community discussion caption post karta hai (POST /{page_id}/photos)."),
        
        ("Tool 6: post_linkedin() (LinkedIn REST API v2 Tool)",
         "LinkedIn ke new UGC Post API (wshare:ugcPost) se Bearer token use karke professional thought leadership post publish karta hai."),
        
        ("Tool 7: post_whatsapp() (WhatsApp URI Intent Tool)",
         "Phone number ko E.164 (+91...) me format karta hai, text ko URL-encode karta hai aur https://api.whatsapp.com/send?phone=... link generate karta hai."),
        
        ("Tool 8: post_twitter_x() (X / Twitter Intent Tool)",
         "Text ko 280 characters ke andar truncate karke 1-click tweet URL (twitter.com/intent/tweet?text=...) banata hai."),
        
        ("Tool 9: get_facebook_share_url() & get_linkedin_share_url() (Web Sharer)",
         "Bina kisi token ke normal users ke liye 1-click Facebook Sharer aur LinkedIn Offsite Sharer links create karta hai."),
        
        ("Tool 10: Web Share API Bridge (Native Mobile Share Sheet)",
         "Mobile phone ke native navigator.share() ko trigger karta hai jisse phone ke niche se direct WhatsApp, Instagram share sheet khul jati hai."),
        
        ("Tool 11: duckduckgo_search (Live Web Grounding Tool)",
         "Internet se live taza information search karke AI agent ko latest facts provide karta hai."),
        
        ("Tool 12: is_ollama_available() (Socket Diagnostics Tool)",
         "150 milliseconds me TCP socket se check karta hai ki local Llama 3.2 AI model available hai ya nahi."),
        
        ("Tool 13: AES-256-GCM Cryptographic Tool (Token Security)",
         "Database me sabhi social media access tokens ko 12-byte nonce aur 16-byte auth tag ke sath AES-256-GCM se encrypt karta hai (Zero Plaintext Token).")
    ]

    for t_title, t_desc in tools_exp:
        story.append(Paragraph(f"<b>🛠️ {t_title}:</b>", h2_style))
        story.append(Paragraph(t_desc, body_style))

    story.append(Spacer(1, 8))

    # ==========================================
    # SECTION 5: LLMS & PACKAGES
    # ==========================================
    story.append(Paragraph("5. LLM Models Aur Packages Ka Complete Breakdown", h1_style))
    story.append(Paragraph("• <b>Meta Llama 3.2 (3B):</b> Local edge model jo bina internet ke computer par chalta hai (100% private, 0 cost).<br/>• <b>Google Gemini / GPT-4o-mini:</b> Cloud AI models jo complex reasoning aur translation ke liye use hote hain.<br/>• <b>Deterministic Heuristic Engine:</b> Offline fallback database jo 100% uptime deta hai.<br/>• <b>Libraries:</b> <code>ollama</code> (Local LLM), <code>httpx</code> (Async API), <code>pillow</code> (4K Graphics), <code>pydantic</code> (Validation), <code>cryptography</code> (AES-256-GCM).", body_style))

    story.append(Spacer(1, 8))

    # ==========================================
    # SECTION 6: SELF-HEALING & RESILIENCE
    # ==========================================
    story.append(Paragraph("6. Self-Healing Aur Partial-Success Resilience (Crash-Proof System)", h1_style))
    story.append(Paragraph(
        "Agar 5 social media par broadcast karte waqt Facebook ka token expire ho jaye, toh <b>hamara AI agent crash nahi hota</b>. Woh Facebook ko <code>ACTION_REQUIRED</code> mark karta hai, baaki LinkedIn, WhatsApp aur Twitter par posting complete karke status <b><code>PARTIAL_SUCCESS</code></b> deta hai, aur user ko 1-Tap 4K Download + Story Camera flow me automatically switch kar deta hai!",
        body_style
    ))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=4, spaceAfter=6))
    story.append(Paragraph("<b>Summary:</b> Yeh complete Agentic AI guide saral Hinglish me tayar ki gayi hai taaki koi bhi aam vyakti ya examiner ise padh kar 100% samajh sake.", meta_style))

    # Build Document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Hinglish Deep Explanation PDF successfully created: {output_filename}")


if __name__ == "__main__":
    build_hinglish_agentic_pdf()
