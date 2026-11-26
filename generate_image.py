import sys
from PIL import Image, ImageDraw, ImageFont

S = 1024
PAPER = 0xF7F1E3
INK = 0x14213D
RED = 0xC1272D
NAVY = 0x1B2A4A
TEAL = 0x0E7C7B
GOLD = 0xD9A441

FB_P = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR_P = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_font_cache = {}

def font(size, bold=False):
    size = int(size)
    key = (size, bold)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FB_P if bold else FR_P, size)
    return _font_cache[key]

def wrap_text(draw, text, fnt, maxw):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines if lines else [""]

def draw_wrapped(draw, xy, lines, fnt, fill, leading=None):
    x, y = int(xy[0]), int(xy[1])
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * (1.0 if leading is None else leading))

def rrect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle([int(box[0]), int(box[1]), int(box[2]), int(box[3])],
                           radius=int(radius), fill=fill, outline=outline, width=int(width))

MONTHA = BLUE = TEAL
DAY = GOLD

def chip(draw, xy, label, color):
    f = font(13, True)
    w = int(draw.textlength(label, font=f))
    x, y = int(xy[0]), int(xy[1])
    h = int(f.size * 1.5)
    pad = 6
    rrect(draw, (x, y, x + w + 2 * pad, y + h), h // 2, fill=color)
    draw.text((x + pad, y + (h - f.size)//2), label, font=f, fill=PAPER)
    return x + w + 2 * pad, y + h

def panel_icon(draw, kind, x, y, colors):
    W, H, L, R, A, T, G = [int(v) for v in (15, 12, TEAL, GOLD, RED, NAVY, 0x8A94A6)]
    if kind == "flame":
        pts = [(x + W//2, y), (x + W, y + H), (x, y + H)]
        draw.polygon([tuple(map(int, p)) for p in pts], fill=RED)
        draw.ellipse([x + 4, y + 5, x + W - 4, y + H], fill=GOLD)
    elif kind == "ship":
        rrect(draw, (x, y + 2, x + W, y + 7), 1, fill=T)
        draw.polygon([(x + 7, y), (x + 10, y + 2), (x + 4, y + 2)], fill=T)
        draw.line([(x, y + 9), (x + W, y + 9)], fill=INK, width=1)
    elif kind == "building":
        draw.rectangle([x, y + 2, x + W, y + H], fill=T)
        for i in range(3):
            for j in range(2):
                draw.rectangle([x + 2 + i * 4, y + 4 + j * 3, x + 4 + i * 4, y + 6 + j * 3], fill=PAPER)
    elif kind == "rocket":
        draw.polygon([(x + W//2, y), (x + 11, y + H), (x + W - 11, y + H)], fill=T)
        draw.ellipse([x + W//2 - 2, y + 3, x + W//2 + 2, y + 6], fill=PAPER)
        draw.line([(x + 3, y + H), (x + 7, y + H - 3)], fill=RED, width=1)
    elif kind == "shield":
        draw.polygon([(x + W//2, y), (x + W, y + 3), (x + W//2, y + H), (x, y + 3)], fill=T)
        draw.line([(x + W//2, y + 2), (x + W//2, y + H - 2)], fill=PAPER, width=1)
    elif kind == "flag":
        draw.line([(x + 2, y), (x + 2, y + H)], fill=G, width=1)
        draw.rectangle([x + 2, y + 1, x + 8, y + 6], fill=GOLD)
        draw.rectangle([x + 2, y + 6, x + 8, y + 8], fill=T)
        draw.rectangle([x + 2, y + 8, x + 8, y + 10], fill=T)
    elif kind == "ball":
        draw.ellipse([x, y, x + W, y + H], outline=T, width=2)
        cx, cy = x + W//2, y + H//2
        draw.polygon([(cx, y + 1), (cx + 3, y + 4), (cx, y + 7), (cx - 3, y + 4)], fill=T)

def box(draw, x0, y0, x1, y1, fill=PAPER, outline=NAVY, wd=2):
    draw.rectangle([int(x0), int(y0), int(x1), int(y1)], fill=fill, outline=outline, width=int(wd))

def hline(draw, x0, y, x1, c, wd=2):
    draw.line([(int(x0), int(y)), (int(x1), int(y))], fill=c, width=int(wd))

def news(d, img=None):
    f7 = font(7)
    out = []
    for line, (lead, sub, tag) in [
    ]:
        pass
    return ""

def draw1(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, S], fill=PAPER)
    hline(d, 0, 0, S, INK, 3)
    box(d, 0, 3, W, 84, NAVY, NAVY)
    f_mk = font(34, True)
    d.text((24, 14), "THE WORLD IN ONE IMAGE", font=f_mk, fill=PAPER)
    d.text((S - 300, 20), "NOVEMBER 2026 EDITION", font=font(16, True), fill=GOLD)
    d.line([(24, 78), (S - 24, 78)], fill=GOLD, width=2)
    f_d1 = font(24, True)
    f_d2 = font(20)
    d.text((24, 94), "THURSDAY", font=f_d1, fill=NAVY)
    d.text((24 + d.textlength("THURSDAY", font=f_d1) + 16, 96), "26 NOVEMBER 2026", font=f_d2, fill=RED)
    d.line([(24, 138), (S - 24, 138)], fill=INK, width=2)
    # hero
    hline(d, 24, 150, S - 24, RED, 2)
    f_hl = font(40, True)
    hl = wrap_text(d, "Fuel tanker crash kills 30 on Cairo Ring Road", f_hl, S - 48)
    draw_wrapped(d, (24, 156), hl, f_hl, INK, 1.05)
    yy = 156 + int(len(hl) * 40 * 1.12) + 6
    f_su = font(18)
    su = wrap_text(d, "A fuel tanker crashed and caught fire on Cairo's Ring Road in the Warraq district of Giza, engulfing more than two dozen cars and motorcycles; Egypt's health ministry calls the toll of 30 killed and 25 injured preliminary.", f_su, S - 48 - 70)
    draw_wrapped(d, (94, yy), su, f_su, NAVY, 1.25)
    x0, y0, x1, y1 = 24, yy + 6, S - 24, yy + 6 + 72
    box(d, x0, y0, x1, y1, PAPER, INK, 1)
    panel_icon(d, "flame", x0 + 12, y0 + (72 - 12)//2, None)
    f_big = font(40, True)
    f_lab = font(12, True)
    d.text((x0 + 44, y0 + 8), "30", font=f_big, fill=RED)
    d.text((x0 + 44, y0 + 44), "KILLED", font=f_lab, fill=NAVY)
    d.text((x0 + 140, y0 + 8), "25", font=f_big, fill=TEAL)
    d.text((x0 + 140, y0 + 44), "INJURED", font=f_lab, fill=NAVY)
    d.text((x0 + 270, y0 + 8), "2026", font=f_big, fill=INK)
    d.text((x0 + 270, y0 + 44), "WARQAQ, GIZA", font=f_lab, fill=NAVY)
    d.line([(x0 + 40, y0 + 8), (x0 + 40, y1 - 8)], fill=INK, width=1)
    d.line([(x0 + 130, y0 + 8), (x0 + 130, y1 - 8)], fill=INK, width=1)
    d.line([(x0 + 260, y0 + 8), (x0 + 260, y1 - 8)], fill=INK, width=1)
    d.text((x1 - 100, y0 + 8), "EGYPT", font=f_lab, fill=RED)
    yy = y1 + 12
    # tiles 2x2: stories 2,3,4,5
    f_tit = font(16, True)
    f_sub = font(13)
    f_chip = font(11, True)

def _main():
    print("run generate_image.py with a variant number argument")

def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else "1"
    fn = globals().get("draw_variant" + variant)
    if fn is None:
        print("unknown variant", variant)
        sys.exit(1)
    img = Image.new("RGB", (S, S), PAPER)
    fn(img)
    path = "variant_" + variant + ".png"
    img.save(path, "PNG")
    import os
    sz = os.path.getsize(path)
    print("wrote variant_%s.png 1024x1024 bytes %d" % (variant, sz))

import sys
from PIL import Image, ImageDraw, ImageFont

S = 1024
PAPER = 0xF7F1E3
INK = 0x14213D
RED = 0xC1272D
NAVY = 0x1B2A4A
TEAL = 0x0E7C7B
GOLD = 0xD9A441

FB_P = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR_P = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

_font_cache = {}

def font(size, bold=False):
    size = int(size)
    key = (size, bold)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(FB_P if bold else FR_P, size)
    return _font_cache[key]

def wrap_text(draw, text, fnt, maxw):
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines if lines else [""]

def draw_wrapped(draw, xy, lines, fnt, fill, leading=None):
    x, y = int(xy[0]), int(xy[1])
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += int(fnt.size * (1.0 if leading is None else leading))

def rrect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle([int(box[0]), int(box[1]), int(box[2]), int(box[3])],
                           radius=int(radius), fill=fill, outline=outline, width=int(width))

MONTHA = BLUE = TEAL
DAY = GOLD

def chip(draw, xy, label, color):
    f = font(13, True)
    w = int(draw.textlength(label, font=f))
    x, y = int(xy[0]), int(xy[1])
    h = int(f.size * 1.5)
    pad = 6
    rrect(draw, (x, y, x + w + 2 * pad, y + h), h // 2, fill=color)
    draw.text((x + pad, y + (h - f.size)//2), label, font=f, fill=PAPER)
    return x + w + 2 * pad, y + h

def panel_icon(draw, kind, x, y, colors):
    W, H, L, R, A, T, G = [int(v) for v in (15, 12, TEAL, GOLD, RED, NAVY, 0x8A94A6)]
    if kind == "flame":
        pts = [(x + W//2, y), (x + W, y + H), (x, y + H)]
        draw.polygon([tuple(map(int, p)) for p in pts], fill=RED)
        draw.ellipse([x + 4, y + 5, x + W - 4, y + H], fill=GOLD)
    elif kind == "ship":
        rrect(draw, (x, y + 2, x + W, y + 7), 1, fill=T)
        draw.polygon([(x + 7, y), (x + 10, y + 2), (x + 4, y + 2)], fill=T)
        draw.line([(x, y + 9), (x + W, y + 9)], fill=INK, width=1)
    elif kind == "building":
        draw.rectangle([x, y + 2, x + W, y + H], fill=T)
        for i in range(3):
            for j in range(2):
                draw.rectangle([x + 2 + i * 4, y + 4 + j * 3, x + 4 + i * 4, y + 6 + j * 3], fill=PAPER)
    elif kind == "rocket":
        draw.polygon([(x + W//2, y), (x + 11, y + H), (x + W - 11, y + H)], fill=T)
        draw.ellipse([x + W//2 - 2, y + 3, x + W//2 + 2, y + 6], fill=PAPER)
        draw.line([(x + 3, y + H), (x + 7, y + H - 3)], fill=RED, width=1)
    elif kind == "shield":
        draw.polygon([(x + W//2, y), (x + W, y + 3), (x + W//2, y + H), (x, y + 3)], fill=T)
        draw.line([(x + W//2, y + 2), (x + W//2, y + H - 2)], fill=PAPER, width=1)
    elif kind == "flag":
        draw.line([(x + 2, y), (x + 2, y + H)], fill=G, width=1)
        draw.rectangle([x + 2, y + 1, x + 8, y + 6], fill=GOLD)
        draw.rectangle([x + 2, y + 6, x + 8, y + 8], fill=T)
        draw.rectangle([x + 2, y + 8, x + 8, y + 10], fill=T)
    elif kind == "ball":
        draw.ellipse([x, y, x + W, y + H], outline=T, width=2)
        cx, cy = x + W//2, y + H//2
        draw.polygon([(cx, y + 1), (cx + 3, y + 4), (cx, y + 7), (cx - 3, y + 4)], fill=T)

def box(draw, x0, y0, x1, y1, fill=PAPER, outline=NAVY, wd=2):
    draw.rectangle([int(x0), int(y0), int(x1), int(y1)], fill=fill, outline=outline, width=int(wd))

def hline(draw, x0, y, x1, c, wd=2):
    draw.line([(int(x0), int(y)), (int(x1), int(y))], fill=c, width=int(wd))

def news(d, img=None):
    f7 = font(7)
    out = []
    for line, (lead, sub, tag) in []:
        pass
    return ""

def draw1(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, S], fill=PAPER)
    hline(d, 0, 0, S, INK, 3)
    box(d, 0, 3, W, 84, NAVY, NAVY)
    f_mk = font(34, True)
    d.text((24, 14), "THE WORLD IN ONE IMAGE", font=f_mk, fill=PAPER)
    d.text((S - 300, 20), "NOVEMBER 2026 EDITION", font=font(16, True), fill=GOLD)
    d.line([(24, 78), (S - 24, 78)], fill=GOLD, width=2)
    f_d1 = font(24, True)
    f_d2 = font(20)
    d.text((24, 94), "THURSDAY", font=f_d1, fill=NAVY)
    d.text((24 + d.textlength("THURSDAY", font=f_d1) + 16, 96), "26 NOVEMBER 2026", font=f_d2, fill=RED)
    d.line([(24, 138), (S - 24, 138)], fill=INK, width=2)
    # hero
    hline(d, 24, 150, S - 24, RED, 2)
    f_hl = font(40, True)
    hl = wrap_text(d, "Fuel tanker crash kills 30 on Cairo Ring Road", f_hl, S - 48)
    draw_wrapped(d, (24, 156), hl, f_hl, INK, 1.05)
    yy = 156 + int(len(hl) * 40 * 1.12) + 6
    f_su = font(18)
    su = wrap_text(d, "A fuel tanker crashed and caught fire on Cairo's Ring Road in the Warraq district of Giza, engulfing more than two dozen cars and motorcycles; Egypt's health ministry calls the toll of 30 killed and 25 injured preliminary.", f_su, S - 48 - 70)
    draw_wrapped(d, (94, yy), su, f_su, NAVY, 1.25)
    x0, y0, x1, y1 = 24, yy + 6, S - 24, yy + 6 + 72
    box(d, x0, y0, x1, y1, PAPER, INK, 1)
    panel_icon(d, "flame", x0 + 12, y0 + (72 - 12)//2, None)
    f_big = font(40, True)
    f_lab = font(12, True)
    d.text((x0 + 44, y0 + 8), "30", font=f_big, fill=RED)
    d.text((x0 + 44, y0 + 44), "KILLED", font=f_lab, fill=NAVY)
    d.text((x0 + 140, y0 + 8), "25", font=f_big, fill=TEAL)
    d.text((x0 + 140, y0 + 44), "INJURED", font=f_lab, fill=NAVY)
    d.text((x0 + 270, y0 + 8), "2026", font=f_big, fill=INK)
    d.text((x0 + 270, y0 + 44), "WARQAQ, GIZA", font=f_lab, fill=NAVY)
    d.line([(x0 + 40, y0 + 8), (x0 + 40, y1 - 8)], fill=INK, width=1)
    d.line([(x0 + 130, y0 + 8), (x0 + 130, y1 - 8)], fill=INK, width=1)
    d.line([(x0 + 260, y0 + 8), (x0 + 260, y1 - 8)], fill=INK, width=1)
    d.text((x1 - 100, y0 + 8), "EGYPT", font=f_lab, fill=RED)
    yy = y1 + 12
    # tiles 2x2: stories 2,3,4,5
    f_tit = font(16, True)
    f_sub = font(13)
    f_chip = font(11, True)

def draw_variant2(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, S], fill=PAPER)
    # Top date banner
    banner_h = 80
    rrect(d, (0, 0, S, banner_h), 0, fill=NAVY)
    f_date = font(36, True)
    date_text = "THURSDAY 26 NOVEMBER 2026"
    tw = d.textlength(date_text, font=f_date)
    d.text(((S - tw) // 2, (banner_h - f_date.size) // 2), date_text, font=f_date, fill=PAPER)
    # Gold accent line
    d.line([(60, banner_h), (S - 60, banner_h)], fill=GOLD, width=3)
    
    # 2x3 grid for stories 1-6
    grid_top = banner_h + 10
    grid_h = S - grid_top - 10
    panel_w = (S - 30) // 2  # 2 columns with margins
    panel_h = (grid_h - 20) // 3  # 3 rows with gaps
    
    stories = [
        {"tag": "EGYPT", "color": RED, "headline": "Fuel tanker crash kills 30 on Cairo Ring Road",
         "summary": "Tanker exploded on Ring Road in Warraq district, engulfing 20+ vehicles; health ministry toll preliminary.", "icon": "flame"},
        {"tag": "GULF", "color": TEAL, "headline": "Houthis claim attacks on Saudi ports including Ras Tanura",
         "summary": "Retaliatory strikes hit oil refinery; India condemns after two nationals injured.", "icon": "ship"},
        {"tag": "EUROPE", "color": NAVY, "headline": "EU leaders convene Special Council in Brussels",
         "summary": "London and Brussels agree closer economic ties at 26-27 Nov summit.", "icon": "building"},
        {"tag": "SPACE", "color": GOLD, "headline": "Pakistan's first astronaut docks at Tiangong station",
         "summary": "Muhammad Zeeshan Ali aboard Shenzhou-24, first foreign visitor to Chinese station.", "icon": "rocket"},
        {"tag": "COLOMBIA", "color": RED, "headline": "Police free 20 hostages after 17-hour supermarket siege",
         "summary": "Cartagena standoff ends with one gunman killed; nation marks 10 years since peace accord.", "icon": "shield"},
        {"tag": "INDIA", "color": TEAL, "headline": "Constitution Day and 26/11 anniversary observed",
         "summary": "IITs add 6,000 seats in robotics, AI, space; Rs 15,000 cr Nepal package announced.", "icon": "flag"},
    ]
    
    for idx, s in enumerate(stories):
        col = idx % 2
        row = idx // 2
        x0 = 15 + col * (panel_w + 10)
        y0 = grid_top + 10 + row * (panel_h + 10)
        x1 = x0 + panel_w
        y1 = y0 + panel_h
        
        # Panel background
        box(d, x0, y0, x1, y1, PAPER, NAVY, 1)
        
        # Header chip
        chip_x = x0 + 12
        chip_y = y0 + 12
        chip(d, (chip_x, chip_y), s["tag"], s["color"])
        
        # Headline (up to 2 lines)
        f_hl = font(18, True)
        hl_lines = wrap_text(d, s["headline"], f_hl, panel_w - 40)
        hl_lines = hl_lines[:2]
        hl_y = chip_y + 30
        draw_wrapped(d, (chip_x, hl_y), hl_lines, f_hl, INK, 1.15)
        
        # Summary (one line)
        f_sum = font(13)
        sum_lines = wrap_text(d, s["summary"], f_sum, panel_w - 40)
        sum_y = hl_y + len(hl_lines) * int(f_hl.size * 1.15) + 8
        if sum_lines:
            draw_wrapped(d, (chip_x, sum_y), sum_lines[:1], f_sum, NAVY, 1.2)
        
        # Icon bottom right
        icon_x = x1 - 30
        icon_y = y1 - 25
        panel_icon(d, s["icon"], icon_x, icon_y, None)

def draw_variant3(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, S, S], fill=PAPER)
    
    # Date line at top
    f_date = font(28, True)
    d.text((40, 20), "THURSDAY 26 NOVEMBER 2026", font=f_date, fill=NAVY)
    d.line([(40, 58), (S - 40, 58)], fill=GOLD, width=2)
    
    # Huge headline for story 1
    f_huge = font(42, True)
    hl1 = "Fuel tanker crash kills 30 on Cairo Ring Road"
    hl_lines = wrap_text(d, hl1, f_huge, S - 80)
    draw_wrapped(d, (40, 70), hl_lines, f_huge, INK, 1.1)
    
    # Red rule
    rule_y = 70 + len(hl_lines) * int(f_huge.size * 1.1) + 10
    d.line([(40, rule_y), (S - 40, rule_y)], fill=RED, width=3)
    
    # Five horizontal brief rows for stories 2-6
    briefs = [
        {"tag": "GULF", "color": TEAL, "headline": "Houthis strike Saudi ports, hit Ras Tanura refinery",
         "summary": "India condemns retaliatory attacks after two nationals injured."},
        {"tag": "EUROPE", "color": NAVY, "headline": "EU Special Council in Brussels; UK-Brussels reset agreed",
         "summary": "Leaders meet 26-27 Nov to bring economies closer."},
        {"tag": "SPACE", "color": GOLD, "headline": "Pakistan astronaut Muhammad Zeeshan Ali docks at Tiangong",
         "summary": "First foreign visitor to Chinese station aboard Shenzhou-24."},
        {"tag": "COLOMBIA", "color": RED, "headline": "Cartagena supermarket siege ends; 20 hostages freed after 17 hours",
         "summary": "One gunman killed; Colombia marks decade since peace deal."},
        {"tag": "INDIA", "color": TEAL, "headline": "Constitution Day & 26/11 anniversary; IITs add 6,000 tech seats",
         "summary": "Rs 15,000 cr Nepal package; call for human control of military AI."},
        {"tag": "SPORT", "color": GOLD, "headline": "Gukesh draws Game 2 vs Sindarov; Sooryavanshi 204 off 53 balls",
         "summary": "Chess world championship tied; teen prodigy smashes T20 record."},
        {"tag": "SCIENCE", "color": TEAL, "headline": "Asteroid-defence close-up images show a new crater",
         "summary": "Hera mission captures detailed impact site on Dimorphos."},
    ]
    
    f_brief_h = font(18, True)
    f_brief_s = font(14)
    row_h = 78
    start_y = rule_y + 20
    
    for i, b in enumerate(briefs):
        ry = start_y + i * (row_h + 8)
        # Chip
        chip(d, (40, ry + 8), b["tag"], b["color"])
        # Headline
        chip_w = int(d.textlength(b["tag"], font=font(13, True))) + 12 + 12
        hx = 40 + chip_w + 16
        hl = wrap_text(d, b["headline"], f_brief_h, S - hx - 40)
        draw_wrapped(d, (hx, ry + 4), hl[:1], f_brief_h, INK, 1.1)
        # Summary
        sum_y = ry + 4 + int(f_brief_h.size * 1.1) + 4
        sl = wrap_text(d, b["summary"], f_brief_s, S - hx - 40)
        draw_wrapped(d, (hx, sum_y), sl[:1], f_brief_s, NAVY, 1.2)
        # Divider line
        if i < 6:
            d.line([(40, ry + row_h + 4), (S - 40, ry + row_h + 4)], fill=0xD0C9B8, width=1)
    
    # Bottom strip with two ticker items
    strip_y = S - 100
    rrect(d, (0, strip_y, S, S), 0, fill=NAVY)
    f_tick = font(13, True)
    f_tick_s = font(12)
    tickers = [
        "IPL 2027 auction: 1,220 players registered  |  Russia admits ~500,000 lost in Ukraine war",
        "US readies new global tariffs plan  |  North Korea expels Swiss diplomat  |  6 dead in Mississippi plane crash  |  Flipkart CEO to step down in Dec",
    ]
    for i, t in enumerate(tickers):
        ty = strip_y + 15 + i * 35
        # Bullet
        d.ellipse([25, ty + 5, 31, ty + 11], fill=GOLD)
        draw_wrapped(d, (40, ty), [t], f_tick_s, PAPER, 1.2)

def _main():
    print("run generate_image.py with a variant number argument")

def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else "1"
    fn = globals().get("draw_variant" + variant)
    if fn is None:
        print("unknown variant", variant)
        sys.exit(1)
    img = Image.new("RGB", (S, S), PAPER)
    fn(img)
    path = "variant_" + variant + ".png"
    img.save(path, "PNG")
    import os
    sz = os.path.getsize(path)
    print("wrote variant_%s.png 1024x1024 bytes %d" % (variant, sz))

if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
