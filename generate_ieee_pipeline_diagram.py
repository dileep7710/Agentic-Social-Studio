import os
import math
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    font_names = [
        "arialbd.ttf" if bold else "arial.ttf",
        "timesbd.ttf" if bold else "times.ttf",
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

def draw_arrow(draw, start, end, fill="#1E293B", width=3, arrow_size=10):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - arrow_size * math.cos(angle - math.pi / 6), y2 - arrow_size * math.sin(angle - math.pi / 6))
    p2 = (x2 - arrow_size * math.cos(angle + math.pi / 6), y2 - arrow_size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=fill)

def generate_ieee_diagram():
    # IEEE publication width format (aspect ratio ~ 1.9 : 1 for full width span)
    W, H = 2400, 1260
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(34, bold=True)
    f_sub = get_font(21, bold=False)
    f_box_title = get_font(26, bold=True)
    f_box_text = get_font(20, bold=False)
    f_badge = get_font(18, bold=True)
    f_tag = get_font(17, bold=True)
    f_plat = get_font(23, bold=True)
    f_plat_det = get_font(17, bold=False)

    # 1. OUTER IEEE BOUNDARY (Subtle clean border)
    draw.rectangle([15, 15, W - 15, H - 15], outline="#CBD5E1", width=2)

    # Header / Title Bar
    draw.rectangle([15, 15, W - 15, 75], fill="#F8FAFC", outline="#CBD5E1", width=2)
    t_text = "AGENTIC-SOCIAL-STUDIO: END-TO-END SYSTEM PIPELINE ARCHITECTURE"
    bb_t = draw.textbbox((0, 0), t_text, font=f_title)
    draw.text(((W - (bb_t[2] - bb_t[0])) // 2, 28), t_text, fill="#0F172A", font=f_title)

    # ==========================================
    # LEVEL 1: USER INPUT & GOAL SPECIFICATION
    # ==========================================
    # Box: (60, 160, 480, 445) - Perfectly aligned vertically with Stage 2 modules!
    draw.rounded_rectangle([60, 160, 480, 445], radius=10, fill="#FFFFFF", outline="#475569", width=2)
    # Header tab
    draw.rounded_rectangle([60, 160, 480, 200], radius=10, fill="#E2E8F0")
    draw.rectangle([60, 185, 480, 200], fill="#E2E8F0")
    draw.text((75, 168), "Stage 1: User Intent Input", fill="#0F172A", font=f_box_title)
    
    draw.text((80, 230), "High-Level User Instruction:", fill="#334155", font=f_box_text)
    draw.text((80, 270), "\"Post today's inspiring", fill="#1E293B", font=f_box_title)
    draw.text((80, 310), "thought everywhere\"", fill="#1E293B", font=f_box_title)
    draw.text((80, 385), "[1-Click Natural Intent]", fill="#475569", font=f_tag)

    # Arrow Stage 1 -> Stage 2
    draw_arrow(draw, (480, 300), (550, 300), fill="#1E293B", width=3, arrow_size=12)

    # ==========================================
    # LEVEL 2: AGENTIC AI COGNITIVE CORE
    # ==========================================
    # Big Container: (550, 95, 2340, 480)
    draw.rounded_rectangle([550, 95, 2340, 480], radius=14, fill="#FAFAFA", outline="#2563EB", width=2)
    
    # Subsystem Badge
    core_lbl = "STAGE 2: AGENTIC COGNITIVE CORE (PERCEIVE -> PLAN -> ADAPT -> SYNTHESIZE)"
    draw.rectangle([550, 95, 2340, 135], fill="#EFF6FF", outline="#2563EB", width=2)
    draw.text((575, 104), core_lbl, fill="#1D4ED8", font=f_badge)

    # 3 Parallel Functional Modules in Cognitive Core
    # Module 1: Goal Manager & Action Planner
    draw.rounded_rectangle([580, 160, 1120, 445], radius=10, fill="#FFFFFF", outline="#64748B", width=2)
    draw.rounded_rectangle([580, 160, 1120, 200], radius=10, fill="#F1F5F9")
    draw.rectangle([580, 185, 1120, 200], fill="#F1F5F9")
    draw.text((595, 168), "Module 1: Goal Manager & Planner", fill="#0F172A", font=f_box_title)
    draw.text((600, 220), "- Semantic intent & theme extraction", fill="#334155", font=f_box_text)
    draw.text((600, 260), "- Keywords: Success, Tech, Mindset", fill="#334155", font=f_box_text)
    draw.text((600, 300), "- Deterministic 4-step action plan", fill="#334155", font=f_box_text)
    draw.text((600, 340), "- Execution dependency ordering", fill="#334155", font=f_box_text)
    draw.text((600, 385), "[ai_agent.py :: GoalManager & Planner]", fill="#2563EB", font=f_tag)

    # Arrow Mod 1 -> Mod 2
    draw_arrow(draw, (1120, 300), (1220, 300), fill="#1E293B", width=3, arrow_size=10)
    draw.text((1150, 275), "Plan", fill="#64748B", font=f_tag)

    # Module 2: Dual-Tier LLM Engine
    draw.rounded_rectangle([1220, 160, 1730, 445], radius=10, fill="#FFFFFF", outline="#64748B", width=2)
    draw.rounded_rectangle([1220, 160, 1730, 200], radius=10, fill="#F5F3FF")
    draw.rectangle([1220, 185, 1730, 200], fill="#F5F3FF")
    draw.text((1235, 168), "Module 2: Dual LLM Engine", fill="#581C87", font=f_box_title)
    draw.text((1240, 220), "- Tier 1 (Edge): Meta Llama 3.2 (3B)", fill="#334155", font=f_box_text)
    draw.text((1240, 260), "  Private, zero-cost, 350ms latency", fill="#475569", font=f_box_text)
    draw.text((1240, 300), "- Tier 2 (Cloud): Google Gemini Flash", fill="#334155", font=f_box_text)
    draw.text((1240, 340), "  Multimodal image-to-text & translation", fill="#475569", font=f_box_text)
    draw.text((1240, 385), "[Socket Port 11434 & Gemini API]", fill="#7C3AED", font=f_tag)

    # Arrow Mod 2 -> Mod 3
    draw_arrow(draw, (1730, 300), (1810, 300), fill="#1E293B", width=3, arrow_size=10)
    draw.text((1740, 275), "Content", fill="#64748B", font=f_tag)

    # Module 3: Visual Synthesis & Platform Content Adapter
    draw.rounded_rectangle([1810, 160, 2300, 445], radius=10, fill="#FFFFFF", outline="#64748B", width=2)
    draw.rounded_rectangle([1810, 160, 2300, 200], radius=10, fill="#FFFBEB")
    draw.rectangle([1810, 185, 2300, 200], fill="#FFFBEB")
    draw.text((1825, 168), "Module 3: Visual & Adapter", fill="#92400E", font=f_box_title)
    draw.text((1830, 220), "- Pillow 4K Poster Graphic Engine", fill="#334155", font=f_box_text)
    draw.text((1830, 260), "  Frosted-glass RGBA box & typography", fill="#475569", font=f_box_text)
    draw.text((1830, 300), "- Embeds custom signature watermark", fill="#334155", font=f_box_text)
    draw.text((1830, 340), "- 5 Distinct platform-tailored copies", fill="#334155", font=f_box_text)
    draw.text((1830, 385), "[social_tools.py :: create_image & adapt]", fill="#D97706", font=f_tag)

    # ==========================================
    # BUS BAR TO DISPATCH LAYER (STAGE 3)
    # ==========================================
    # Central trunk line down from Module 3
    draw.line([(2055, 445), (2055, 520)], fill="#1E3A8A", width=3)
    draw.line([(2055, 520), (1200, 520)], fill="#1E3A8A", width=3)
    draw.line([(1200, 520), (1200, 560)], fill="#1E3A8A", width=3)

    # Big Stage 3 Container: (70, 560, 2330, 1020)
    draw.rounded_rectangle([70, 560, 2330, 1020], radius=14, fill="#F8FAFC", outline="#475569", width=2)
    
    # Stage 3 Header
    draw.rectangle([70, 560, 2330, 600], fill="#F1F5F9", outline="#475569", width=2)
    stage3_lbl = "STAGE 3: PARALLEL MULTI-PLATFORM SOCIAL DISPATCH LAYER (WITH FAULT ISOLATION)"
    draw.text((95, 570), stage3_lbl, fill="#0F172A", font=f_badge)

    # Distribution Bus
    draw.line([(240, 630), (2160, 630)], fill="#0F172A", width=3)
    draw_arrow(draw, (1200, 600), (1200, 630), fill="#0F172A", width=3, arrow_size=8)

    # 5 Platform Cards
    platform_nodes = [
        ("WhatsApp", 240, "#15803D", "#F0FDF4", "#14532D", [
            "Protocol: Click-to-Chat URI",
            "Payload: Clean Markdown Text",
            "Media: Public CDN HTTPS link",
            "Target: E.164 sanitized phone"
        ]),
        ("Twitter / X", 720, "#0F172A", "#F8FAFC", "#0F172A", [
            "Protocol: Web Intent Tweet",
            "Constraint: <= 280 Characters",
            "Payload: Punchy viral message",
            "Engine: Safe string truncation"
        ]),
        ("Facebook", 1200, "#1D4ED8", "#EFF6FF", "#1E3A8A", [
            "Protocol: Graph API / Sharer",
            "Payload: Community question",
            "Target: Timeline & Connected Page",
            "Engine: Discussion engagement"
        ]),
        ("Instagram", 1680, "#BE185D", "#FDF2F8", "#831843", [
            "Protocol: Meta Graph API v21",
            "Formats: 9:16 Story & 1:1 Feed",
            "Payload: Visual + 7 viral hashtags",
            "Fallback: 1-Tap Story Camera"
        ]),
        ("LinkedIn", 2160, "#0369A1", "#F0F9FF", "#075985", [
            "Protocol: REST API v2 UGC Post",
            "Payload: Thought leadership",
            "Structure: Context + Bullet points",
            "Security: Bearer OAuth token"
        ]),
    ]

    card_w = 400
    card_h = 320
    card_top = 670

    for name, cx, b_col, bg_col, t_col, bullets in platform_nodes:
        # Arrow down from bus bar
        draw_arrow(draw, (cx, 630), (cx, card_top), fill=b_col, width=3, arrow_size=10)

        x1 = cx - card_w // 2
        x2 = cx + card_w // 2
        y1 = card_top
        y2 = card_top + card_h

        # Card container
        draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=bg_col, outline=b_col, width=2)
        # Header banner
        draw.rounded_rectangle([x1, y1, x2, y1 + 55], radius=10, fill=b_col)
        draw.rectangle([x1, y1 + 35, x2, y1 + 55], fill=b_col)
        
        bb_pn = draw.textbbox((0, 0), name, font=f_plat)
        draw.text((x1 + (card_w - (bb_pn[2] - bb_pn[0])) // 2, y1 + 14), name, fill="#FFFFFF", font=f_plat)

        # Bullets
        cur_y = y1 + 75
        for b in bullets:
            draw.text((x1 + 18, cur_y), b, fill=t_col, font=f_plat_det)
            cur_y += 54

    # ==========================================
    # LEVEL 4: STAGE 4: FAULT ISOLATION & RESULTS
    # ==========================================
    # Box: (70, 1050, 2330, 1220)
    draw.rounded_rectangle([70, 1050, 2330, 1220], radius=10, fill="#0F172A")
    
    r_title = "STAGE 4: EXECUTION EVALUATION & FAULT-ISOLATED SELF-HEALING"
    r_sub1 = "Normal State: All 5 platforms broadcast simultaneously within 1.8 seconds (SUCCESS state)."
    r_sub2 = "Fault State: If an API token expires (e.g., Meta session invalid), unaffected platforms succeed -> failed platform auto-switches to 1-Tap Fallback."
    
    bb_rt = draw.textbbox((0, 0), r_title, font=f_box_title)
    draw.text((70 + (2260 - (bb_rt[2] - bb_rt[0])) // 2, 1065), r_title, fill="#38BDF8", font=f_box_title)
    
    draw.text((120, 1118), r_sub1, fill="#E2E8F0", font=f_box_text)
    draw.text((120, 1162), r_sub2, fill="#94A3B8", font=f_box_text)

    out_file = "ieee_pipeline_architecture.png"
    img.save(out_file, dpi=(300, 300))
    print(f"{out_file} successfully generated with publication-grade IEEE standards!")

if __name__ == "__main__":
    generate_ieee_diagram()
