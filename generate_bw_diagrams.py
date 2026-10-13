import os
import math
from PIL import Image, ImageDraw, ImageFont

def get_font(size, bold=False):
    font_names = [
        "timesbd.ttf" if bold else "times.ttf",
        "arialbd.ttf" if bold else "arial.ttf",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "calibrib.ttf" if bold else "calibri.ttf",
    ]
    for fn in font_names:
        try:
            return ImageFont.truetype(fn, size)
        except Exception:
            continue
    return ImageFont.load_default()

def draw_arrow(draw, start, end, fill="#000000", width=2, arrow_size=10):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=fill, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    p1 = (x2 - arrow_size * math.cos(angle - math.pi / 6), y2 - arrow_size * math.sin(angle - math.pi / 6))
    p2 = (x2 - arrow_size * math.cos(angle + math.pi / 6), y2 - arrow_size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=fill)

def generate_bw_pipeline_diagram():
    # Crisp B&W 300 DPI layout (2400 x 1260)
    W, H = 2400, 1260
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(32, bold=True)
    f_box_title = get_font(25, bold=True)
    f_box_text = get_font(19, bold=False)
    f_badge = get_font(18, bold=True)
    f_tag = get_font(17, bold=True)
    f_plat = get_font(22, bold=True)
    f_plat_det = get_font(17, bold=False)

    # 1. Outer Boundary (Crisp Black Border)
    draw.rectangle([12, 12, W - 12, H - 12], outline="#000000", width=2)

    # Top Header Banner (Subtle Light Gray Fill, Black Text)
    draw.rectangle([12, 12, W - 12, 75], fill="#EEEEEE", outline="#000000", width=2)
    t_text = "AGENTIC-SOCIAL-STUDIO: END-TO-END SYSTEM PIPELINE ARCHITECTURE"
    bb_t = draw.textbbox((0, 0), t_text, font=f_title)
    draw.text(((W - (bb_t[2] - bb_t[0])) // 2, 26), t_text, fill="#000000", font=f_title)

    # ==========================================
    # LEVEL 1: USER INPUT & GOAL SPECIFICATION
    # ==========================================
    draw.rounded_rectangle([50, 160, 470, 445], radius=6, fill="#FFFFFF", outline="#000000", width=2)
    # Header Tab
    draw.rounded_rectangle([50, 160, 470, 205], radius=6, fill="#E0E0E0")
    draw.rectangle([50, 185, 470, 205], fill="#E0E0E0")
    draw.line([(50, 205), (470, 205)], fill="#000000", width=2)
    draw.text((65, 172), "Stage 1: User Intent Input", fill="#000000", font=f_box_title)
    
    draw.text((70, 230), "High-Level User Instruction:", fill="#333333", font=f_box_text)
    draw.text((70, 270), "\"Post today's inspiring", fill="#000000", font=f_box_title)
    draw.text((70, 310), "thought everywhere\"", fill="#000000", font=f_box_title)
    draw.text((70, 385), "[1-Click Natural Intent]", fill="#444444", font=f_tag)

    # Arrow Stage 1 -> Stage 2
    draw_arrow(draw, (470, 300), (540, 300), fill="#000000", width=3, arrow_size=12)

    # ==========================================
    # LEVEL 2: AGENTIC AI COGNITIVE CORE
    # ==========================================
    draw.rounded_rectangle([540, 95, 2350, 480], radius=8, fill="#FAFAFA", outline="#000000", width=2)
    
    # Subsystem Badge
    core_lbl = "STAGE 2: AGENTIC COGNITIVE CORE (PERCEIVE -> PLAN -> ADAPT -> SYNTHESIZE)"
    draw.rectangle([540, 95, 2350, 135], fill="#EAEAEA", outline="#000000", width=2)
    draw.text((565, 106), core_lbl, fill="#000000", font=f_badge)

    # 3 Parallel Functional Modules in Cognitive Core
    # Module 1: Goal Manager & Action Planner
    draw.rounded_rectangle([570, 160, 1110, 445], radius=6, fill="#FFFFFF", outline="#000000", width=2)
    draw.rounded_rectangle([570, 160, 1110, 205], radius=6, fill="#F0F0F0")
    draw.rectangle([570, 185, 1110, 205], fill="#F0F0F0")
    draw.line([(570, 205), (1110, 205)], fill="#000000", width=2)
    draw.text((585, 172), "Module 1: Goal Manager & Planner", fill="#000000", font=f_box_title)
    draw.text((590, 225), "- Semantic intent & theme extraction", fill="#222222", font=f_box_text)
    draw.text((590, 265), "- Keywords: Success, Tech, Mindset", fill="#222222", font=f_box_text)
    draw.text((590, 305), "- Deterministic 4-step action plan", fill="#222222", font=f_box_text)
    draw.text((590, 345), "- Execution dependency ordering", fill="#222222", font=f_box_text)
    draw.text((590, 390), "[ai_agent.py :: GoalManager & Planner]", fill="#444444", font=f_tag)

    # Arrow Mod 1 -> Mod 2
    draw_arrow(draw, (1110, 300), (1200, 300), fill="#000000", width=3, arrow_size=10)
    draw.text((1130, 275), "Plan", fill="#333333", font=f_tag)

    # Module 2: Dual-Tier LLM Engine
    draw.rounded_rectangle([1200, 160, 1730, 445], radius=6, fill="#FFFFFF", outline="#000000", width=2)
    draw.rounded_rectangle([1200, 160, 1730, 205], radius=6, fill="#F0F0F0")
    draw.rectangle([1200, 185, 1730, 205], fill="#F0F0F0")
    draw.line([(1200, 205), (1730, 205)], fill="#000000", width=2)
    draw.text((1215, 172), "Module 2: Dual LLM Engine", fill="#000000", font=f_box_title)
    draw.text((1220, 225), "- Tier 1 (Edge): Meta Llama 3.2 (3B)", fill="#222222", font=f_box_text)
    draw.text((1220, 265), "  Private, zero-cost, 350ms latency", fill="#444444", font=f_box_text)
    draw.text((1220, 305), "- Tier 2 (Cloud): Google Gemini Flash", fill="#222222", font=f_box_text)
    draw.text((1220, 345), "  Multimodal image-to-text & translation", fill="#444444", font=f_box_text)
    draw.text((1220, 390), "[Socket Port 11434 & Gemini API]", fill="#444444", font=f_tag)

    # Arrow Mod 2 -> Mod 3
    draw_arrow(draw, (1730, 300), (1810, 300), fill="#000000", width=3, arrow_size=10)
    draw.text((1740, 275), "Copy", fill="#333333", font=f_tag)

    # Module 3: Visual Synthesis & Multi-Platform Adapter
    draw.rounded_rectangle([1810, 160, 2320, 445], radius=6, fill="#FFFFFF", outline="#000000", width=2)
    draw.rounded_rectangle([1810, 160, 2320, 205], radius=6, fill="#F0F0F0")
    draw.rectangle([1810, 185, 2320, 205], fill="#F0F0F0")
    draw.line([(1810, 205), (2320, 205)], fill="#000000", width=2)
    draw.text((1825, 172), "Module 3: Visual & Adapter", fill="#000000", font=f_box_title)
    draw.text((1830, 225), "- Pillow 4K Poster Graphic Engine", fill="#222222", font=f_box_text)
    draw.text((1830, 265), "  Frosted-glass card & typography", fill="#444444", font=f_box_text)
    draw.text((1830, 305), "- Embeds custom signature watermark", fill="#222222", font=f_box_text)
    draw.text((1830, 345), "- 5 Distinct platform-tailored copies", fill="#222222", font=f_box_text)
    draw.text((1830, 390), "[social_tools.py :: Graphic & Adaptation]", fill="#444444", font=f_tag)

    # ==========================================
    # BUS BAR TO DISPATCH LAYER (STAGE 3)
    # ==========================================
    draw.line([(2065, 445), (2065, 520)], fill="#000000", width=2)
    draw.line([(2065, 520), (1200, 520)], fill="#000000", width=2)
    draw.line([(1200, 520), (1200, 560)], fill="#000000", width=2)

    # Big Stage 3 Container
    draw.rounded_rectangle([50, 560, 2350, 1020], radius=8, fill="#FAFAFA", outline="#000000", width=2)
    draw.rectangle([50, 560, 2350, 600], fill="#EAEAEA", outline="#000000", width=2)
    stage3_lbl = "STAGE 3: PARALLEL MULTI-PLATFORM SOCIAL DISPATCH LAYER (WITH FAULT ISOLATION)"
    draw.text((75, 571), stage3_lbl, fill="#000000", font=f_badge)

    # Distribution Bus
    draw.line([(230, 630), (2170, 630)], fill="#000000", width=2)
    draw_arrow(draw, (1200, 600), (1200, 630), fill="#000000", width=2, arrow_size=8)

    # 5 Platform Cards (Pure B&W / Grayscale Styling)
    platform_nodes = [
        ("WhatsApp", 230, [
            "Protocol: Click-to-Chat URI",
            "Payload: Clean Markdown Text",
            "Media: Public CDN HTTPS link",
            "Target: E.164 sanitized phone"
        ]),
        ("Twitter / X", 715, [
            "Protocol: Web Intent Tweet",
            "Constraint: <= 280 Characters",
            "Payload: Punchy viral message",
            "Engine: Safe string truncation"
        ]),
        ("Facebook", 1200, [
            "Protocol: Graph API / Sharer",
            "Payload: Community question",
            "Target: Timeline & Connected Page",
            "Engine: Discussion engagement"
        ]),
        ("Instagram", 1685, [
            "Protocol: Meta Graph API v21",
            "Formats: 9:16 Story & 1:1 Feed",
            "Payload: Visual + 7 viral hashtags",
            "Fallback: 1-Tap Story Camera"
        ]),
        ("LinkedIn", 2170, [
            "Protocol: REST API v2 UGC Post",
            "Payload: Thought leadership",
            "Structure: Context + Bullet points",
            "Security: Bearer OAuth token"
        ]),
    ]

    card_w = 410
    card_h = 320
    card_top = 670

    for name, cx, bullets in platform_nodes:
        draw_arrow(draw, (cx, 630), (cx, card_top), fill="#000000", width=2, arrow_size=10)

        x1 = cx - card_w // 2
        x2 = cx + card_w // 2
        y1 = card_top
        y2 = card_top + card_h

        # Card container: White fill, black outline
        draw.rounded_rectangle([x1, y1, x2, y2], radius=6, fill="#FFFFFF", outline="#000000", width=2)
        # Header banner: Light gray fill, black outline
        draw.rounded_rectangle([x1, y1, x2, y1 + 55], radius=6, fill="#DCDCDC")
        draw.rectangle([x1, y1 + 35, x2, y1 + 55], fill="#DCDCDC")
        draw.line([(x1, y1 + 55), (x2, y1 + 55)], fill="#000000", width=2)
        
        bb_pn = draw.textbbox((0, 0), name, font=f_plat)
        draw.text((x1 + (card_w - (bb_pn[2] - bb_pn[0])) // 2, y1 + 14), name, fill="#000000", font=f_plat)

        # Bullets
        cur_y = y1 + 75
        for b in bullets:
            draw.text((x1 + 18, cur_y), b, fill="#222222", font=f_plat_det)
            cur_y += 54

    # ==========================================
    # LEVEL 4: STAGE 4: FAULT ISOLATION & RESULTS
    # ==========================================
    draw.rounded_rectangle([50, 1050, 2350, 1220], radius=6, fill="#F2F2F2", outline="#000000", width=2)
    
    r_title = "STAGE 4: EXECUTION EVALUATION & FAULT-ISOLATED SELF-HEALING"
    r_sub1 = "Normal State: All 5 platforms broadcast simultaneously within 1.8 seconds (SUCCESS state)."
    r_sub2 = "Fault State: If an API token expires (e.g., Meta session invalid), unaffected platforms succeed -> failed platform auto-switches to 1-Tap Fallback."
    
    bb_rt = draw.textbbox((0, 0), r_title, font=f_box_title)
    draw.text((50 + (2300 - (bb_rt[2] - bb_rt[0])) // 2, 1065), r_title, fill="#000000", font=f_box_title)
    
    draw.text((100, 1118), r_sub1, fill="#111111", font=f_box_text)
    draw.text((100, 1162), r_sub2, fill="#333333", font=f_box_text)

    out_file = "ieee_pipeline_architecture_bw.png"
    img.save(out_file, dpi=(300, 300))
    print(f"{out_file} successfully generated in pure Black & White!")

def generate_bw_state_diagram():
    # Fig. 2: State transition / decision flowchart in pure B&W (1200 x 750)
    W, H = 1200, 750
    img = Image.new("RGB", (W, H), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_node = get_font(18, bold=True)
    f_desc = get_font(15, bold=False)
    f_edge = get_font(14, bold=True)

    # Outer border
    draw.rectangle([8, 8, W - 8, H - 8], outline="#000000", width=2)
    
    # Title
    t_text = "FAULT-ISOLATION & ASSISTED FALLBACK STATE TRANSITION"
    bb_t = draw.textbbox((0, 0), t_text, font=f_title)
    draw.text(((W - (bb_t[2] - bb_t[0])) // 2, 22), t_text, fill="#000000", font=f_title)
    draw.line([(50, 60), (W - 50, 60)], fill="#000000", width=1)

    # Node 1: Start / Incoming Payload
    draw.rounded_rectangle([60, 100, 360, 180], radius=6, fill="#F0F0F0", outline="#000000", width=2)
    draw.text((80, 115), "1. Prepared Payload", fill="#000000", font=f_node)
    draw.text((80, 142), "Platform copy + 4K poster", fill="#333333", font=f_desc)

    # Arrow 1 -> Decision
    draw_arrow(draw, (360, 140), (460, 140), fill="#000000", width=2)

    # Node 2: Decision Diamond / Box
    draw.rounded_rectangle([460, 95, 780, 185], radius=6, fill="#FFFFFF", outline="#000000", width=2)
    draw.text((480, 112), "2. Validate Credentials", fill="#000000", font=f_node)
    draw.text((480, 138), "Active Bearer Token & Network?", fill="#333333", font=f_desc)

    # Path A: Valid Token (Success)
    draw_arrow(draw, (780, 140), (880, 140), fill="#000000", width=2)
    draw.text((795, 118), "[Token Valid]", fill="#000000", font=f_edge)

    draw.rounded_rectangle([880, 100, 1140, 180], radius=6, fill="#E5E5E5", outline="#000000", width=2)
    draw.text((900, 115), "State: SUCCESS", fill="#000000", font=f_node)
    draw.text((900, 142), "HTTP 200 / Direct Publish", fill="#333333", font=f_desc)

    # Path B: Downward to Token Expired / Network Error
    draw_arrow(draw, (620, 185), (620, 270), fill="#000000", width=2)
    draw.text((630, 220), "[Token Expired / 401 Unauthorized / Timeout]", fill="#000000", font=f_edge)

    # Node 3: Fault Isolation Boundary
    draw.rounded_rectangle([380, 270, 860, 370], radius=6, fill="#FFFFFF", outline="#000000", width=2)
    draw.text((400, 288), "3. Fault Containment Boundary", fill="#000000", font=f_node)
    draw.text((400, 315), "Catch Exception Locally (No Cascade Failure)", fill="#222222", font=f_desc)
    draw.text((400, 338), "Other Channels Continue Execution Uninterrupted", fill="#555555", font=f_desc)

    # Arrow to Fallback Trigger
    draw_arrow(draw, (620, 370), (620, 440), fill="#000000", width=2)

    # Node 4: Autonomous Fallback State Machine
    draw.rounded_rectangle([300, 440, 940, 560], radius=6, fill="#F5F5F5", outline="#000000", width=2)
    draw.text((320, 458), "4. Autonomous 1-Tap Assisted Fallback", fill="#000000", font=f_node)
    draw.text((320, 488), "A. Generate Direct Web Intent URI (Twitter / WhatsApp / FB)", fill="#222222", font=f_desc)
    draw.text((320, 510), "B. Provide 1-Tap 4K Image Download + Instagram Camera Link", fill="#222222", font=f_desc)
    draw.text((320, 532), "C. Switch CDN Mirror (Catbox -> TmpFiles Failover)", fill="#222222", font=f_desc)

    # Arrow to Final Resolved State
    draw_arrow(draw, (620, 560), (620, 630), fill="#000000", width=2)

    # Node 5: Terminal Resolved State
    draw.rounded_rectangle([400, 630, 840, 710], radius=6, fill="#E0E0E0", outline="#000000", width=2)
    draw.text((420, 646), "State: GRACEFULLY RECOVERED", fill="#000000", font=f_node)
    draw.text((420, 674), "Zero Downtime | Complete Human Agency Retained", fill="#333333", font=f_desc)

    out_file = "ieee_fault_isolation_state_bw.png"
    img.save(out_file, dpi=(300, 300))
    print(f"{out_file} successfully generated in pure Black & White!")

if __name__ == "__main__":
    generate_bw_pipeline_diagram()
    generate_bw_state_diagram()
