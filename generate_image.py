import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BG = '#F7F1E3'
INK = '#14213D'
RED = '#C1272D'
NAVY = '#1B2A4A'
TEAL = '#0E7C7B'
GOLD = '#D9A441'

FNT_BOLD_44 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 44)
FNT_BOLD_36 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 36)
FNT_BOLD_30 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 30)
FNT_REG_24 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 24)
FNT_REG_22 = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 22)

def wrap_text(draw, text, font, max_w):
    words = text.split()
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if draw.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def draw_wrapped(draw, xy, lines, font, fill, leading=6):
    x, y = xy
    for line in lines:
        draw.text((int(x), int(y)), line, font=font, fill=fill)
        y += font.size + leading

def draw_globe(draw, cx, cy, r):
    draw.ellipse([int(cx-r), int(cy-r), int(cx+r), int(cy+r)], fill=TEAL, outline=NAVY, width=3)
    for lat in range(-60, 61, 30):
        yy = int(cy + r * 0.6 * (lat/90))
        draw.arc([int(cx-r), yy-int(r*0.1), int(cx+r), yy+int(r*0.1)], 0, 180, fill=NAVY, width=2)
    for lon in range(-150, 151, 60):
        xx = int(cx + r * 0.6 * (lon/180))
        draw.arc([xx-int(r*0.1), int(cy-r), xx+int(r*0.1), int(cy+r)], 90, 270, fill=NAVY, width=2)
    draw.ellipse([int(cx-r*0.15), int(cy-r*0.15), int(cx+r*0.15), int(cy+r*0.15)], fill=GOLD)

def draw_flames(draw, x, y, h, color=RED):
    for i in range(5):
        fx = x + (i-2)*8
        draw.polygon([(int(fx), int(y)), (int(fx-10), int(y-h)), (int(fx+10), int(y-h))], fill=color)
        draw.polygon([(int(fx), int(y-h//2)), (int(fx-6), int(y-h)), (int(fx+6), int(y-h))], fill=GOLD)

def draw_tanker(draw, x, y):
    draw.rectangle([int(x-40), int(y-15), int(x+40), int(y+10)], fill='#3A3A3A')
    draw.rectangle([int(x-30), int(y-35), int(x+30), int(y-15)], fill='#555')
    draw.ellipse([int(x-35), int(y+5), int(x-15), int(y+25)], fill='#222')
    draw.ellipse([int(x+15), int(y+5), int(x+35), int(y+25)], fill='#222')
    draw.rectangle([int(x-10), int(y-40), int(x+10), int(y-35)], fill=RED)

def draw_rocket_station(draw, x, y):
    draw.rectangle([int(x-15), int(y-60), int(x+15), int(y)], fill='#CCC')
    draw.polygon([(int(x-15), int(y-60)), (int(x), int(y-80)), (int(x+15), int(y-60))], fill=RED)
    draw.ellipse([int(x-50), int(y-20), int(x+50), int(y+20)], outline=TEAL, width=4)
    draw.ellipse([int(x-60), int(y-30), int(x+60), int(y+30)], outline=TEAL, width=2)
    for sx, sy in [(x-80, y-70), (x+80, y-70), (x-90, y+40), (x+90, y+40), (x, y-100)]:
        draw.ellipse([int(sx-3), int(sy-3), int(sx+3), int(sy+3)], fill=GOLD)

def draw_building_flags(draw, x, y):
    draw.rectangle([int(x-50), int(y-60), int(x+50), int(y+20)], fill='#DDD', outline=NAVY, width=2)
    draw.rectangle([int(x-40), int(y-80), int(x+40), int(y-60)], fill='#BBB', outline=NAVY, width=2)
    draw.polygon([(int(x-40), int(y-80)), (int(x), int(y-100)), (int(x+40), int(y-80))], fill=NAVY)
    for i, fx in enumerate([x-60, x, x+60]):
        draw.rectangle([int(fx-15), int(y-120), int(fx+15), int(y-90)], fill=[NAVY, TEAL, GOLD][i])
        draw.line([(int(fx), int(y-120)), (int(fx), int(y-140))], fill=INK, width=2)

def draw_chess_cricket(draw, x, y):
    for i in range(4):
        for j in range(4):
            c = INK if (i+j)%2 else '#FFF'
            draw.rectangle([int(x-60+i*30), int(y-60+j*30), int(x-30+i*30), int(y-30+j*30)], fill=c)
    draw.ellipse([int(x-10), int(y-10), int(x+10), int(y+10)], fill=GOLD)
    draw.rectangle([int(x+40), int(y-40), int(x+45), int(y+40)], fill='#8B4513')
    draw.ellipse([int(x+55), int(y-10), int(x+75), int(y+10)], fill=RED)

def draw_asteroid(draw, x, y):
    pts = [(int(x+40*0.8*__import__('math').cos(a)), int(y+40*0.8*__import__('math').sin(a))) for a in [i*0.5 for i in range(13)]]
    draw.polygon(pts, fill='#666', outline='#444', width=2)
    draw.ellipse([int(x-10), int(y-10), int(x+10), int(y+10)], fill='#333')
    draw.polygon([(int(x+30), int(y)), (int(x+50), int(y-20)), (int(x+50), int(y+20))], fill='#AAA')

def draw_parliament(draw, x, y):
    draw.ellipse([int(x-50), int(y-30), int(x+50), int(y+30)], fill='#EEE', outline=NAVY, width=3)
    draw.rectangle([int(x-40), int(y+30), int(x+40), int(y+60)], fill='#DDD', outline=NAVY, width=2)
    draw.polygon([(int(x-20), int(y-30)), (int(x), int(y-60)), (int(x+20), int(y-30))], fill=GOLD)
    draw.line([(int(x-30), int(y+80)), (int(x+30), int(y+80))], fill=INK, width=3)
    draw.polygon([(int(x-30), int(y+80)), (int(x), int(y+100)), (int(x+30), int(y+80))], fill=TEAL)

def draw_supermarket(draw, x, y):
    draw.rectangle([int(x-50), int(y-40), int(x+50), int(y+20)], fill='#DDD', outline=NAVY, width=2)
    draw.rectangle([int(x-40), int(y-60), int(x+40), int(y-40)], fill=RED)
    draw.text((int(x-20), int(y-55)), 'MARKET', font=FNT_BOLD_30, fill='#FFF')
    draw.rectangle([int(x-10), int(y-10), int(x+10), int(y+10)], fill=TEAL, outline=NAVY, width=2)

def draw_oil_derrick(draw, x, y):
    draw.line([(int(x), int(y+40)), (int(x), int(y-60))], fill='#555', width=6)
    for yy in range(-50, 40, 20):
        draw.line([(int(x-20), int(y+yy)), (int(x+20), int(y+yy))], fill='#555', width=3)
    draw_flames(draw, x, y-70, 30)
    draw.rectangle([int(x-30), int(y+30), int(x+30), int(y+50)], fill='#333')

def draw_variant1():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    
    d.rectangle([0, 0, W, int(H*0.14)], fill=NAVY)
    draw_wrapped(d, (int(W*0.05), int(H*0.01)), ['THURSDAY 26 NOVEMBER 2026'], FNT_BOLD_44, '#FFF')
    draw_wrapped(d, (int(W*0.05), int(H*0.07)), ['THE WORLD IN ONE IMAGE'], FNT_BOLD_36, GOLD)
    
    draw_globe(d, W//2, int(H*0.35), int(W*0.22))
    
    panels = [
        (int(W*0.04), int(H*0.58), int(W*0.3), int(H*0.18), 'EGYPT: TANKER FIRE KILLS 30+ ON CAIRO RING ROAD', draw_tanker, (int(W*0.19), int(H*0.68))),
        (int(W*0.36), int(H*0.58), int(W*0.3), int(H*0.18), 'GULF: HOUTHIS STRIKE SAUDI PORTS INCL RAS TANURA', draw_oil_derrick, (int(W*0.51), int(H*0.68))),
        (int(W*0.68), int(H*0.58), int(W*0.3), int(H*0.18), 'EUROPE: EU LEADERS MEET IN BRUSSELS FOR SPECIAL COUNCIL', draw_building_flags, (int(W*0.83), int(H*0.68))),
        (int(W*0.04), int(H*0.78), int(W*0.3), int(H*0.18), 'SPACE: PAKISTAN ASTRONAUT DOCKS AT TIANGONG', draw_rocket_station, (int(W*0.19), int(H*0.88))),
        (int(W*0.36), int(H*0.78), int(W*0.3), int(H*0.18), 'COLOMBIA: POLICE FREE 20 HOSTAGES IN CARTAGENA', draw_supermarket, (int(W*0.51), int(H*0.88))),
        (int(W*0.68), int(H*0.78), int(W*0.3), int(H*0.18), 'SPORT: GUKESH DRAWS; 15YO SMASHES 204 OFF 53', draw_chess_cricket, (int(W*0.83), int(H*0.88))),
    ]
    for px, py, pw, ph, headline, pic_fn, pic_xy in panels:
        d.rectangle([px, py, px+pw, py+ph], fill='#FFF', outline=NAVY, width=2)
        pic_fn(d, pic_xy[0], pic_xy[1])
        lines = wrap_text(d, headline, FNT_BOLD_30, pw - 20)
        draw_wrapped(d, (px+10, py+int(ph*0.55)), lines[:2], FNT_BOLD_30, INK)
    
    d.rectangle([0, int(H*0.86), W, H], fill=NAVY)
    bot_panels = [
        (int(W*0.05), int(H*0.87), int(W*0.44), int(H*0.11), 'INDIA: CONSTITUTION DAY & 26/11; IITS ADD 6K SEATS; RS 15K CR NEPAL PACKAGE', draw_parliament, (int(W*0.22), int(H*0.93))),
        (int(W*0.52), int(H*0.87), int(W*0.44), int(H*0.11), 'SCIENCE: CLOSE-UP OF ASTEROID HIT IN PLANETARY DEFENCE TEST', draw_asteroid, (int(W*0.74), int(H*0.93))),
    ]
    for px, py, pw, ph, headline, pic_fn, pic_xy in bot_panels:
        d.rectangle([px, py, px+pw, py+ph], fill='#FFF', outline=TEAL, width=2)
        pic_fn(d, pic_xy[0], pic_xy[1])
        lines = wrap_text(d, headline, FNT_BOLD_30, pw - 20)
        draw_wrapped(d, (px+10, py+int(ph*0.55)), lines[:2], FNT_BOLD_30, INK)
    
    return img

def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else '1'
    fn = globals().get('draw_variant' + variant)
    if not fn:
        print(f'Unknown variant {variant}')
        sys.exit(1)
    img = fn()
    fname = f'variant_{variant}.png'
    img.save(fname)
    print(f'wrote {fname} 1024x1024 bytes {len(img.tobytes())}')

def draw_variant2():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    
    # Top date banner
    d.rectangle([0, 0, W, 100], fill=NAVY)
    draw_wrapped(d, (40, 15), ['THURSDAY 26 NOVEMBER 2026'], FNT_BOLD_44, '#FFF')
    
    # 2x2 big panels
    pad, gap = 20, 15
    pw = (W - 2*pad - gap) // 2
    ph = (H - 110 - 2*pad - gap - 100) // 2
    positions = [
        (pad, 110), (pad + pw + gap, 110),
        (pad, 110 + ph + gap), (pad + pw + gap, 110 + ph + gap)
    ]
    panels = [
        ('CAIRO TANKER FIRE KILLS 30', draw_tanker, (positions[0][0]+pw//2, positions[0][1]+ph//2)),
        ('PAKISTAN ASTRONAUT DOCKS AT TIANGONG', draw_rocket_station, (positions[1][0]+pw//2, positions[1][1]+ph//2)),
        ('EU LEADERS MEET IN BRUSSELS', draw_building_flags, (positions[2][0]+pw//2, positions[2][1]+ph//2)),
        ('GUKESH DRAWS; TEEN SMASHES 204', draw_chess_cricket, (positions[3][0]+pw//2, positions[3][1]+ph//2)),
    ]
    for i, (px, py) in enumerate(positions):
        d.rectangle([px, py, px+pw, py+ph], fill='#FFF', outline=NAVY, width=3)
        headline, pic_fn, pic_xy = panels[i]
        pic_fn(d, pic_xy[0], pic_xy[1])
        lines = wrap_text(d, headline, FNT_BOLD_36, pw - 30)
        draw_wrapped(d, (px+15, py+ph-100), lines[:2], FNT_BOLD_36, INK)
    
    # Bottom four chips
    by = H - 100
    chip_w = (W - 5*pad) // 4
    chips = [
        ('GULF', draw_oil_derrick),
        ('COLOMBIA', draw_supermarket),
        ('INDIA', draw_parliament),
        ('SCIENCE', draw_asteroid),
    ]
    for i, (label, pic_fn) in enumerate(chips):
        cx = pad + i*(chip_w + pad)
        d.rectangle([cx, by, cx+chip_w, by+90], fill='#FFF', outline=TEAL, width=2)
        draw_wrapped(d, (cx+10, by+28), [label], FNT_BOLD_30, INK)
    return img

def draw_variant3():
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    
    # Masthead
    d.rectangle([0, 0, W, 120], fill=NAVY)
    draw_wrapped(d, (40, 10), ['THE WORLD IN ONE IMAGE'], FNT_BOLD_44, '#FFF')
    draw_wrapped(d, (40, 65), ['THURSDAY 26 NOVEMBER 2026'], FNT_BOLD_30, GOLD)
    
    # Lead panel - Cairo tanker fire large
    lx, ly, lw, lh = 30, 140, 600, 380
    d.rectangle([lx, ly, lx+lw, ly+lh], fill='#FFF', outline=NAVY, width=3)
    draw_tanker(d, lx+lw//2, ly+lh//2)
    draw_flames(d, lx+lw//2+30, ly+lh//2-20, 60)
    lines = wrap_text(d, 'CAIRO TANKER FIRE KILLS 30+ ON RING ROAD', FNT_BOLD_36, lw - 40)
    draw_wrapped(d, (lx+20, ly+20), lines[:2], FNT_BOLD_36, RED)
    
    # Four horizontal brief rows (stories 2-5)
    rows = [
        ('HOUTHIS STRIKE SAUDI PORTS INCL RAS TANURA', draw_oil_derrick),
        ('EU LEADERS MEET IN BRUSSELS FOR SPECIAL COUNCIL', draw_building_flags),
        ('PAKISTAN ASTRONAUT DOCKS AT TIANGONG', draw_rocket_station),
        ('POLICE FREE 20 HOSTAGES IN CARTAGENA', draw_supermarket),
    ]
    ry = ly + lh + 20
    for headline, pic_fn in rows:
        d.rectangle([30, ry, W-30, ry+90], fill='#FFF', outline=NAVY, width=2)
        pic_fn(d, 70, ry+45)
        lines = wrap_text(d, headline, FNT_BOLD_30, W - 220)
        draw_wrapped(d, (140, ry+15), lines[:1], FNT_BOLD_30, INK)
        ry += 100
    
    # Bottom three chips: sport, India, science
    by = H - 100
    cw = (W - 4*30) // 3
    chips = [
        ('SPORT', draw_chess_cricket),
        ('INDIA', draw_parliament),
        ('SCIENCE', draw_asteroid),
    ]
    for i, (label, pic_fn) in enumerate(chips):
        cx = 30 + i*(cw + 30)
        d.rectangle([cx, by, cx+cw, by+90], fill='#FFF', outline=TEAL, width=2)
        pic_fn(d, cx+cw//2, by+45)
        draw_wrapped(d, (cx+15, by+10), [label], FNT_BOLD_30, INK)
    return img
if __name__ == "__main__":
    main()