import os
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
        "seguisb.ttf" if bold else "segoeui.ttf",
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_arrow(draw, start, end, fill="#334155", width=4, arrow_size=12):
    import math
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - arrow_size * math.cos(angle - math.pi / 6), y2 - arrow_size * math.sin(angle - math.pi / 6))
    p2 = (x2 - arrow_size * math.cos(angle + math.pi / 6), y2 - arrow_size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=fill)

def create_super_simple_diagram():
    W, H = 2400, 1500
    img = Image.new("RGBA", (W, H), (248, 250, 252, 255)) # Soft crisp background
    draw = ImageDraw.Draw(img)

    f_title = get_font(52, bold=True)
    f_sub = get_font(26, bold=False)
    f_card_title = get_font(32, bold=True)
    f_card_sub = get_font(22, bold=False)
    f_badge = get_font(20, bold=True)
    f_plat_title = get_font(28, bold=True)
    f_plat_desc = get_font(19, bold=False)

    # 1. HEADER
    title_text = "HOW AGENTIC AI & LLM WORK (SIMPLIFIED ARCHITECTURE)"
    sub_text = "1 Simple Input -> Autonomous Thinking & Planning -> Custom Content for 5 Social Media Platforms"
    
    bb_t = draw.textbbox((0, 0), title_text, font=f_title)
    draw.text(((W - (bb_t[2] - bb_t[0])) // 2, 50), title_text, fill="#0F172A", font=f_title)
    
    bb_s = draw.textbbox((0, 0), sub_text, font=f_sub)
    draw.text(((W - (bb_s[2] - bb_s[0])) // 2, 120), sub_text, fill="#64748B", font=f_sub)

    # 2. LEVEL 1: USER INPUT (Top)
    # Box: (750, 190, 1650, 290)
    draw.rounded_rectangle([750, 190, 1650, 290], radius=24, fill="#EFF6FF", outline="#3B82F6", width=4)
    u_title = "USER INPUT (YOU)"
    u_desc = "\"Post today's inspiring thought everywhere\""
    bbu_t = draw.textbbox((0, 0), u_title, font=f_card_title)
    bbu_d = draw.textbbox((0, 0), u_desc, font=f_card_sub)
    draw.text((750 + (900 - (bbu_t[2] - bbu_t[0])) // 2, 208), u_title, fill="#1D4ED8", font=f_card_title)
    draw.text((750 + (900 - (bbu_d[2] - bbu_d[0])) // 2, 250), u_desc, fill="#1E293B", font=f_card_sub)

    # Arrow Down from Input to Brain
    draw_arrow(draw, (1200, 290), (1200, 360), fill="#2563EB", width=5, arrow_size=16)

    # 3. LEVEL 2: THE AGENTIC AI CORE BRAIN
    # Big Parent Container: (350, 360, 2050, 680)
    draw.rounded_rectangle([350, 360, 2050, 680], radius=30, fill="#FFFFFF", outline="#6366F1", width=4)
    # Inner Header Badge
    brain_badge = "AGENTIC AI SYSTEM (THE MASTER BRAIN)"
    bb_bb = draw.textbbox((0, 0), brain_badge, font=f_badge)
    draw.rounded_rectangle([1200 - (bb_bb[2] - bb_bb[0])//2 - 24, 380, 1200 + (bb_bb[2] - bb_bb[0])//2 + 24, 424], radius=14, fill="#EEF2FF", outline="#818CF8", width=2)
    draw.text((1200 - (bb_bb[2] - bb_bb[0])//2, 392), brain_badge, fill="#4338CA", font=f_badge)

    # 3 Sub-Blocks inside the Agentic Brain:
    # A. Goal Manager & Planner
    draw.rounded_rectangle([400, 450, 870, 640], radius=18, fill="#F8FAFC", outline="#94A3B8", width=2)
    draw.text((430, 475), "1. Goal & Planner", fill="#0F172A", font=f_card_title)
    draw.text((430, 525), "- Understands Theme (Success, Tech)", fill="#475569", font=f_card_sub)
    draw.text((430, 560), "- Makes 4-step action plan", fill="#475569", font=f_card_sub)
    draw.text((430, 595), "- Sets execution order", fill="#475569", font=f_card_sub)

    # Arrow A -> B
    draw_arrow(draw, (870, 545), (940, 545), fill="#64748B", width=4, arrow_size=12)

    # B. LLM Engine (Llama 3.2 / Gemini)
    draw.rounded_rectangle([940, 450, 1460, 640], radius=18, fill="#F5F3FF", outline="#8B5CF6", width=3)
    draw.text((970, 475), "2. LLM Engine (Brain)", fill="#6D28D9", font=f_card_title)
    draw.text((970, 525), "- Meta Llama 3.2 (Local 3B)", fill="#5B21B6", font=f_card_sub)
    draw.text((970, 560), "- Google Gemini (Cloud Flash)", fill="#5B21B6", font=f_card_sub)
    draw.text((970, 595), "- Generates & rewrites content", fill="#5B21B6", font=f_card_sub)

    # Arrow B -> C
    draw_arrow(draw, (1460, 545), (1530, 545), fill="#64748B", width=4, arrow_size=12)

    # C. Visual Generator & Adapter
    draw.rounded_rectangle([1530, 450, 2000, 640], radius=18, fill="#FFFBEB", outline="#F59E0B", width=2)
    draw.text((1560, 475), "3. Visual & Adapter", fill="#B45309", font=f_card_title)
    draw.text((1560, 525), "- Pillow 4K Graphic Generator", fill="#78350F", font=f_card_sub)
    draw.text((1560, 560), "- Adds Signature Watermark", fill="#78350F", font=f_card_sub)
    draw.text((1560, 595), "- Customizes for each platform", fill="#78350F", font=f_card_sub)

    # 4. BRANCHING ARROWS DOWN TO 5 SOCIAL MEDIA PLATFORMS
    # Central junction point at (1200, 680)
    # Down to Y=740
    draw.line([(1200, 680), (1200, 740)], fill="#4F46E5", width=5)
    # Horizontal bus bar from X=240 to X=2160
    draw.line([(240, 740), (2160, 740)], fill="#4F46E5", width=5)

    # 5 Branch Positions (Centers):
    # 1. WhatsApp: X=240
    # 2. Twitter / X: X=720
    # 3. Facebook: X=1200
    # 4. Instagram: X=1680
    # 5. LinkedIn: X=2160
    
    platforms = [
        ("WhatsApp", 240, "#25D366", "#F0FDF4", "#15803D", [
            "- Direct 1-Click Message",
            "- Bold / Italic formatting",
            "- Direct 4K CDN Photo link",
            "- E.164 Clean phone target"
        ]),
        ("Twitter / X", 720, "#0F172A", "#F8FAFC", "#0F172A", [
            "- Short & Viral Tweet",
            "- Max 280 character limit",
            "- Safe text truncation",
            "- 1-Click Tweet Intent"
        ]),
        ("Facebook", 1200, "#1877F2", "#EFF6FF", "#1D4ED8", [
            "- Community Discussion",
            "- Question-style caption",
            "- Page API / Feed Timeline",
            "- High audience engagement"
        ]),
        ("Instagram", 1680, "#E1306C", "#FDF2F8", "#BE185D", [
            "- 24h Story & Feed Post",
            "- Visual-first layout",
            "- 7 Targeted Viral Hashtags",
            "- 1-Tap Story Camera flow"
        ]),
        ("LinkedIn", 2160, "#0A66C2", "#F0F9FF", "#0369A1", [
            "- Thought Leadership Tone",
            "- Professional Bullet Points",
            "- Executive takeaways",
            "- Corporate Growth Hashtags"
        ])
    ]

    card_w = 400
    card_h = 360
    card_top = 800

    for name, cx, brand_color, bg_card, text_dark, bullet_points in platforms:
        # Arrow down from bus bar to card
        draw_arrow(draw, (cx, 740), (cx, card_top), fill=brand_color, width=4, arrow_size=14)

        # Draw Card
        x1 = cx - card_w // 2
        x2 = cx + card_w // 2
        y1 = card_top
        y2 = card_top + card_h

        draw.rounded_rectangle([x1, y1, x2, y2], radius=20, fill=bg_card, outline=brand_color, width=3)

        # Card Title Header
        draw.rounded_rectangle([x1, y1, x2, y1 + 75], radius=20, fill=brand_color)
        # Fix top radius / fill
        draw.rectangle([x1, y1 + 45, x2, y1 + 75], fill=brand_color)
        
        bb_pt = draw.textbbox((0, 0), name, font=f_plat_title)
        draw.text((x1 + (card_w - (bb_pt[2] - bb_pt[0])) // 2, y1 + 22), name, fill="#FFFFFF", font=f_plat_title)

        # Bullet Points
        by = y1 + 105
        for bp in bullet_points:
            draw.text((x1 + 24, by), bp, fill=text_dark, font=f_plat_desc)
            by += 55

    # 5. BOTTOM SUMMARY BANNER (Self-Healing & Result)
    # Box: (300, 1220, 2100, 1340)
    draw.rounded_rectangle([300, 1220, 2100, 1340], radius=22, fill="#0F172A")
    sum_title = "RESULT: 1 Instruction -> 5 Tailored Posts Broadcasted Everywhere!"
    sum_desc = "Resilience: If any platform API fails, the Agent never crashes -> automatically switches to 1-Tap Fallback!"
    bbs_t = draw.textbbox((0, 0), sum_title, font=f_card_title)
    bbs_d = draw.textbbox((0, 0), sum_desc, font=f_card_sub)
    draw.text((300 + (1800 - (bbs_t[2] - bbs_t[0])) // 2, 1238), sum_title, fill="#38BDF8", font=f_card_title)
    draw.text((300 + (1800 - (bbs_d[2] - bbs_d[0])) // 2, 1285), sum_desc, fill="#94A3B8", font=f_card_sub)

    out_file = "simple_agentic_workflow.png"
    img.save(out_file, dpi=(300, 300))
    print(f"{out_file} successfully generated!")

if __name__ == "__main__":
    create_super_simple_diagram()
