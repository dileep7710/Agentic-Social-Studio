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

def draw_arrow(draw, start, end, fill="#1E293B", width=3, arrow_size=10):
    x1, y1 = start
    x2, y2 = end
    draw.line([start, end], fill=fill, width=width)
    import math
    angle = math.atan2(y2 - y1, x2 - x1)
    # Arrow head
    p1 = (x2 - arrow_size * math.cos(angle - math.pi / 6), y2 - arrow_size * math.sin(angle - math.pi / 6))
    p2 = (x2 - arrow_size * math.cos(angle + math.pi / 6), y2 - arrow_size * math.sin(angle + math.pi / 6))
    draw.polygon([end, p1, p2], fill=fill)

def create_fig1():
    W, H = 2400, 950
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_title = get_font(34, bold=True)
    f_box = get_font(30, bold=True)
    f_sub = get_font(22, bold=False)
    f_control = get_font(26, bold=True)

    # Outer Control Plane Bounding Box (Dashed style)
    cp_x1, cp_y1, cp_x2, cp_y2 = 50, 40, 2350, 850
    # Draw dashed rectangle
    dash_len = 16
    for x in range(cp_x1, cp_x2, dash_len * 2):
        draw.line([(x, cp_y1), (min(x + dash_len, cp_x2), cp_y1)], fill="#94A3B8", width=3)
        draw.line([(x, cp_y2), (min(x + dash_len, cp_x2), cp_y2)], fill="#94A3B8", width=3)
    for y in range(cp_y1, cp_y2, dash_len * 2):
        draw.line([(cp_x1, y), (cp_x1, min(y + dash_len, cp_y2))], fill="#94A3B8", width=3)
        draw.line([(cp_x2, y), (cp_x2, min(y + dash_len, cp_y2))], fill="#94A3B8", width=3)

    # Top Row Components
    boxes_row1 = [
        ("Human\nIntent", 120, 110, 320, 250, "#F1F5F9", "#0F172A", False, True),
        ("Goal\nManager", 410, 110, 710, 250, "#F8FAFC", "#0F172A", False, False),
        ("Planner", 800, 110, 1100, 250, "#F8FAFC", "#0F172A", False, False),
        ("Agent\nOrchestrator", 1190, 110, 1530, 250, "#EFF6FF", "#1D4ED8", False, False),
        ("Platform\nAdapter", 1620, 110, 1940, 250, "#F8FAFC", "#0F172A", False, False),
    ]

    # Row 2 Components
    boxes_row2 = [
        ("Visual\nGenerator", 410, 480, 710, 620, "#F8FAFC", "#0F172A", False, False),
        ("Media Upload\nLayer", 800, 480, 1100, 620, "#F8FAFC", "#0F172A", False, False),
        ("Reviewer\nApproval Gate", 1190, 480, 1530, 620, "#FEF3C7", "#B45309", True, False),
        ("Dispatch\nEngine", 1620, 480, 1940, 620, "#F0FDF4", "#15803D", True, False),
        ("Evaluator /\nFallback", 2020, 480, 2300, 620, "#FEF2F2", "#B91C1C", True, False),
    ]

    all_boxes = boxes_row1 + boxes_row2

    for text, x1, y1, x2, y2, bg_col, border_col, is_dashed, is_pill in all_boxes:
        # Fill
        draw.rounded_rectangle([x1, y1, x2, y2], radius=18, fill=bg_col)
        # Border
        if is_dashed:
            # dashed border
            d = 10
            for bx in range(x1, x2, d * 2):
                draw.line([(bx, y1), (min(bx + d, x2), y1)], fill=border_col, width=3)
                draw.line([(bx, y2), (min(bx + d, x2), y2)], fill=border_col, width=3)
            for by in range(y1, y2, d * 2):
                draw.line([(x1, by), (x1, min(by + d, y2))], fill=border_col, width=3)
                draw.line([(x2, by), (x2, min(by + d, y2))], fill=border_col, width=3)
        else:
            draw.rounded_rectangle([x1, y1, x2, y2], radius=18, outline=border_col, width=3)

        # Draw Multiline Text Centered
        lines = text.split("\n")
        total_text_h = len(lines) * 36
        start_y = y1 + (y2 - y1 - total_text_h) // 2
        for i, line in enumerate(lines):
            bbox = draw.textbbox((0, 0), line, font=f_box)
            tw = bbox[2] - bbox[0]
            tx = x1 + (x2 - x1 - tw) // 2
            ty = start_y + i * 36
            draw.text((tx, ty), line, fill="#0F172A", font=f_box)

    # Arrows Row 1
    draw_arrow(draw, (320, 180), (410, 180), fill="#334155", width=4)
    draw_arrow(draw, (710, 180), (800, 180), fill="#334155", width=4)
    draw_arrow(draw, (1100, 180), (1190, 180), fill="#334155", width=4)
    draw_arrow(draw, (1530, 180), (1620, 180), fill="#334155", width=4)

    # Orchestrator to Row 2 / Platform Adapter to Visual
    # Orchestrator down to Row 2:
    draw.line([(1360, 250), (1360, 360)], fill="#334155", width=4)
    draw.line([(1360, 360), (560, 360)], fill="#334155", width=4)
    draw_arrow(draw, (560, 360), (560, 480), fill="#334155", width=4)

    # Arrows Row 2
    draw_arrow(draw, (710, 550), (800, 550), fill="#334155", width=4)
    draw_arrow(draw, (1100, 550), (1190, 550), fill="#334155", width=4)
    draw_arrow(draw, (1530, 550), (1620, 550), fill="#334155", width=4)
    draw_arrow(draw, (1940, 550), (2020, 550), fill="#334155", width=4)

    # Control Plane Label
    cp_text = "Control plane: schemas, permissions, timeouts, retries, state, logging, secrets policy"
    bbox_cp = draw.textbbox((0, 0), cp_text, font=f_control)
    cp_w = bbox_cp[2] - bbox_cp[0]
    draw.text(((W - cp_w) // 2, 730), cp_text, fill="#475569", font=f_control)

    img.save("fig1_architecture.png", dpi=(300, 300))
    print("fig1_architecture.png created successfully!")

def create_fig2():
    W, H = 1400, 1200
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    draw = ImageDraw.Draw(img)

    f_box = get_font(34, bold=True)
    f_sub = get_font(26, bold=False)
    f_lbl = get_font(24, bold=True)

    # Component 1: Top Pill
    # Planning / generation request
    draw.rounded_rectangle([300, 60, 1100, 160], radius=50, fill="#F1F5F9", outline="#334155", width=3)
    text1 = "Planning / generation request"
    bb1 = draw.textbbox((0, 0), text1, font=f_box)
    draw.text((300 + (800 - (bb1[2] - bb1[0])) // 2, 88), text1, fill="#0F172A", font=f_box)

    # Arrow 1 down
    draw_arrow(draw, (700, 160), (700, 260), fill="#334155", width=4)

    # Component 2: Tier 1: local LLM
    draw.rounded_rectangle([320, 260, 1080, 420], radius=16, fill="#EFF6FF", outline="#1D4ED8", width=3)
    t2_a = "Tier 1: local LLM"
    t2_b = "timeout  \u03c4_L"
    bb2a = draw.textbbox((0, 0), t2_a, font=f_box)
    bb2b = draw.textbbox((0, 0), t2_b, font=f_sub)
    draw.text((320 + (760 - (bb2a[2] - bb2a[0])) // 2, 290), t2_a, fill="#1E3A8A", font=f_box)
    draw.text((320 + (760 - (bb2b[2] - bb2b[0])) // 2, 350), t2_b, fill="#3B82F6", font=f_sub)

    # Arrow 2 down with label: fail / timeout
    draw_arrow(draw, (700, 420), (700, 580), fill="#DC2626", width=4)
    lbl1 = "fail / timeout"
    bbl1 = draw.textbbox((0, 0), lbl1, font=f_lbl)
    # Background for label
    draw.rectangle([720, 480, 720 + (bbl1[2] - bbl1[0]) + 20, 520], fill="#FFFFFF")
    draw.text((730, 485), lbl1, fill="#DC2626", font=f_lbl)

    # Component 3: Tier 2: optional cloud LLM
    draw.rounded_rectangle([320, 580, 1080, 740], radius=16, fill="#FDF4FF", outline="#A855F7", width=3)
    t3_a = "Tier 2: optional cloud LLM"
    t3_b = "timeout  \u03c4_C"
    bb3a = draw.textbbox((0, 0), t3_a, font=f_box)
    bb3b = draw.textbbox((0, 0), t3_b, font=f_sub)
    draw.text((320 + (760 - (bb3a[2] - bb3a[0])) // 2, 610), t3_a, fill="#581C87", font=f_box)
    draw.text((320 + (760 - (bb3b[2] - bb3b[0])) // 2, 670), t3_b, fill="#9333EA", font=f_sub)

    # Arrow 3 down with label: fail / disabled
    draw_arrow(draw, (700, 740), (700, 900), fill="#DC2626", width=4)
    lbl2 = "fail / disabled"
    bbl2 = draw.textbbox((0, 0), lbl2, font=f_lbl)
    draw.rectangle([720, 800, 720 + (bbl2[2] - bbl2[0]) + 20, 840], fill="#FFFFFF")
    draw.text((730, 805), lbl2, fill="#DC2626", font=f_lbl)

    # Component 4: Tier 3: deterministic heuristic/template
    draw.rounded_rectangle([260, 900, 1140, 1060], radius=16, fill="#F0FDF4", outline="#16A34A", width=3)
    t4_a = "Tier 3: deterministic heuristic / template"
    t4_b = "100% Uptime Guarantee (0ms Fallback)"
    bb4a = draw.textbbox((0, 0), t4_a, font=f_box)
    bb4b = draw.textbbox((0, 0), t4_b, font=f_sub)
    draw.text((260 + (880 - (bb4a[2] - bb4a[0])) // 2, 930), t4_a, fill="#14532D", font=f_box)
    draw.text((260 + (880 - (bb4b[2] - bb4b[0])) // 2, 990), t4_b, fill="#16A34A", font=f_sub)

    img.save("fig2_tritier.png", dpi=(300, 300))
    print("fig2_tritier.png created successfully!")

if __name__ == "__main__":
    create_fig1()
    create_fig2()
