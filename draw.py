#!/usr/bin/env python3
"""news-image-20261122 v3 — front page of THE WORLD, Sunday 22 November 2026.
Draws a 1024x1024 newspaper front page with PIL only. No network access.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

PAGE = 1024
MARGIN = 34
CW = PAGE - 2 * MARGIN          # 956 content width
INK = (26, 22, 18)
RED = (158, 24, 24)
PAPER = (247, 241, 222)
PANEL = (252, 248, 235)
SKY = (178, 214, 235)
NIGHT = (24, 34, 66)
SAND = (226, 205, 150)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def load_font(name, size):
    path = os.path.join(FONT_DIR, name)
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: load_font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: load_font("DejaVuSerif.ttf", s)
SANS_B = lambda s: load_font("DejaVuSans-Bold.ttf", s)


def fit_words(text, font, max_w, draw):
    """Greedy word wrap; returns list of lines that fit inside max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, font, max_w, leading, color=INK):
    """Draw a wrapped paragraph; returns y just below the last line."""
    for line in fit_words(text, font, max_w, draw):
        draw.text((x, y), line, font=font, fill=color)
        y += leading
    return y


def hline(draw, x0, x1, y, w=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=w)


def double_rule(draw, y, gap=5):
    hline(draw, MARGIN, PAGE - MARGIN, y, 3)
    hline(draw, MARGIN, PAGE - MARGIN, y + gap, 1)


def box(draw, rect, outline=INK, width=2, fill=None):
    draw.rectangle(rect, outline=outline, width=width, fill=fill)


def flag(draw, x, y, color, h=34):
    """A small pennant on a pole, top-left at (x, y)."""
    draw.line([(x, y), (x, y + h)], fill=INK, width=2)
    draw.polygon([(x, y), (x + 26, y + 6), (x, y + 13)], fill=color)


def globe(draw, cx, cy, r):
    """A simple globe: blue disc, green land blobs, meridian arcs."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(112, 178, 214),
                 outline=INK, width=3)
    draw.ellipse([cx - r * 0.55, cy - r * 0.6, cx - r * 0.05, cy - r * 0.1],
                 fill=(96, 160, 90))
    draw.ellipse([cx + r * 0.1, cy + r * 0.05, cx + r * 0.6, cy + r * 0.55],
                 fill=(96, 160, 90))
    draw.ellipse([cx - r * 0.75, cy + r * 0.15, cx - r * 0.35, cy + r * 0.5],
                 fill=(120, 175, 105))
    draw.arc([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], 270, 90,
             fill=INK, width=2)
    draw.arc([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r], 90, 270,
             fill=INK, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=INK, width=1)


def lead_art(draw, x0, y0, x1, y1):
    """Richer lead illustration: summit flags over a globe, table, NO DEAL."""
    draw.rectangle([x0, y0, x1, y1], fill=SKY, outline=INK, width=2)
    # sun + rays
    sx, sy = x1 - 52, y0 + 40
    draw.ellipse([sx - 22, sy - 22, sx + 22, sy + 22], fill=(245, 176, 66),
                 outline=INK, width=2)
    for ang in range(0, 360, 45):
        dx, dy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
        draw.line([(sx + dx * 28, sy + dy * 28), (sx + dx * 38, sy + dy * 38)],
                  fill=(245, 176, 66), width=3)
    # row of five summit flags
    cols = [(158, 24, 24), (24, 72, 158), (34, 120, 60), (220, 130, 30),
            (120, 60, 160)]
    fx = x0 + 22
    for c in cols:
        flag(draw, fx, y0 + 14, c)
        fx += 48
    # globe, centre-left
    globe(draw, x0 + 92, y0 + 118, 52)
    # conference table + chairs
    tx0, tx1 = x0 + 168, x1 - 22
    ty = y1 - 58
    draw.rectangle([tx0, ty, tx1, ty + 12], fill=(122, 82, 52), outline=INK, width=2)
    draw.line([(tx0 + 10, ty + 12), (tx0 + 10, y1 - 8)], fill=INK, width=3)
    draw.line([(tx1 - 10, ty + 12), (tx1 - 10, y1 - 8)], fill=INK, width=3)
    draw.rectangle([tx0 + 16, ty - 26, tx0 + 62, ty - 4], fill=(150, 110, 70),
                   outline=INK, width=2)
    draw.rectangle([tx1 - 62, ty - 26, tx1 - 16, ty - 4], fill=(150, 110, 70),
                   outline=INK, width=2)
    # papers on the table
    draw.rectangle([tx0 + 88, ty - 8, tx0 + 128, ty - 1], fill=(255, 255, 255),
                   outline=INK, width=1)
    draw.rectangle([tx1 - 128, ty - 8, tx1 - 88, ty - 1], fill=(255, 255, 255),
                   outline=INK, width=1)
    # sandy ground strip
    draw.rectangle([x0, y1 - 26, x1, y1], fill=SAND)
    draw.line([(x0, y1 - 26), (x1, y1 - 26)], fill=INK, width=2)
    # NO DEAL banner
    banner = "NO DEAL"
    bf = SANS_B(22)
    bw = draw.textlength(banner, font=bf) + 22
    bx = x1 - bw - 12
    by = y1 - 62
    draw.rectangle([bx, by, bx + bw, by + 30], fill=RED, outline=INK, width=2)
    draw.text((bx + 11, by + 4), banner, font=bf, fill=(255, 255, 255))


def strip_sea(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=SKY, outline=INK, width=1)
    draw.ellipse([x1 - 42, y0 + 6, x1 - 14, y0 + 34], fill=(245, 176, 66),
                 outline=INK, width=1)
    for wx in range(x0 + 8, x1 - 8, 26):
        draw.arc([wx, y1 - 16, wx + 22, y1 - 2], 180, 360, fill=(24, 72, 158),
                 width=2)
    # corvette silhouette
    draw.polygon([(x0 + 60, y1 - 14), (x0 + 200, y1 - 14), (x0 + 188, y1 - 30),
                  (x0 + 96, y1 - 30)], fill=(52, 52, 58))
    draw.rectangle([x0 + 108, y1 - 44, x0 + 150, y1 - 30], fill=(52, 52, 58))
    draw.line([(x0 + 128, y1 - 44), (x0 + 128, y1 - 56)], fill=INK, width=2)


def strip_night(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=NIGHT, outline=INK, width=1)
    rnd = random.Random(7)
    for _ in range(14):
        px, py = rnd.randint(x0 + 6, x1 - 6), rnd.randint(y0 + 5, y1 - 14)
        draw.ellipse([px, py, px + 2, py + 2], fill=(255, 255, 255))
    for i in range(3):
        sx = x0 + 40 + i * 78
        draw.ellipse([sx, y0 + 12, sx + 7, y0 + 19], fill=(245, 120, 40))
        draw.line([(sx + 7, y0 + 16), (sx + 34, y0 + 30)], fill=(245, 120, 40),
                  width=2)
    draw.rectangle([x0 + 30, y1 - 18, x0 + 120, y1 - 6], fill=(120, 130, 150),
                   outline=INK, width=1)
    for wx in range(x0 + 36, x0 + 116, 14):
        draw.rectangle([wx, y1 - 16, wx + 7, y1 - 9], fill=(245, 200, 80))


def strip_gulf(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y0 + 22], fill=(245, 196, 120), outline=INK,
                   width=1)
    draw.rectangle([x0, y0 + 22, x1, y1], fill=(70, 130, 190), outline=INK,
                   width=1)
    draw.rectangle([x0 + 150, y0 + 8, x1 - 30, y0 + 20], fill=(158, 24, 24))
    draw.line([(x0 + 34, y0 + 32), (x0 + 122, y0 + 10)], fill=(255, 255, 255),
              width=3)
    draw.ellipse([x0 + 118, y0 + 2, x0 + 126, y0 + 10], fill=(255, 255, 255))
    for wx in range(x0 + 8, x1 - 8, 24):
        draw.arc([wx, y1 - 12, wx + 20, y1 - 2], 180, 360, fill=(255, 255, 255),
                 width=2)


def strip_sudan(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(232, 214, 170), outline=INK, width=1)
    for i, bh in enumerate([30, 44, 26]):
        bx = x0 + 24 + i * 74
        draw.rectangle([bx, y1 - bh, bx + 56, y1], fill=(168, 150, 118),
                       outline=INK, width=1)
        for wy in range(y1 - bh + 6, y1 - 6, 12):
            for wx in range(bx + 7, bx + 50, 14):
                draw.rectangle([wx, wy, wx + 7, wy + 7], fill=(90, 110, 150))
    draw.ellipse([x0 + 210, y0 + 4, x0 + 250, y0 + 30], fill=(120, 120, 120))
    draw.ellipse([x0 + 228, y0 + 16, x0 + 262, y0 + 38], fill=(150, 150, 150))


def strip_tennis(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(46, 139, 87), outline=INK, width=1)
    draw.line([(x0, (y0 + y1) // 2), (x1, (y0 + y1) // 2)], fill=(255, 255, 255),
              width=2)
    draw.line([((x0 + x1) // 2, y0), ((x0 + x1) // 2, y1)], fill=(255, 255, 255),
              width=2)
    draw.rectangle([x0 + 18, y0 + 8, x0 + 66, y0 + 22], fill=(245, 200, 80),
                   outline=INK, width=1)
    draw.ellipse([x1 - 46, y0 + 12, x1 - 22, y0 + 36], fill=(220, 230, 60),
                 outline=INK, width=2)


def strip_house(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(214, 228, 244), outline=INK, width=1)
    cx = (x0 + x1) // 2
    draw.polygon([(cx - 52, y0 + 30), (cx, y0 + 6), (cx + 52, y0 + 30)],
                 fill=(255, 255, 255), outline=INK)
    draw.rectangle([cx - 66, y0 + 32, cx + 66, y1 - 8], fill=(255, 255, 255),
                   outline=INK, width=2)
    for i in range(5):
        px = cx - 56 + i * 24
        draw.line([(px, y0 + 40), (px, y1 - 12)], fill=INK, width=2)
    bf = SANS_B(15)
    tag = "258 SEATS"
    tw = draw.textlength(tag, font=bf)
    draw.rectangle([cx - tw / 2 - 10, y1 - 22, cx + tw / 2 + 10, y1 - 4],
                   fill=(24, 72, 158))
    draw.text((cx - tw / 2, y1 - 21), tag, font=bf, fill=(255, 255, 255))


STRIPS = [strip_sea, strip_night, strip_gulf, strip_sudan, strip_tennis,
          strip_house]

CARDS = [
    ("UKRAINE  •  MEDITERRANEAN",
     "Ukraine sinks Russian corvette at Benghazi",
     "Seven Ukrainian sea drones struck the corvette Merkury at Benghazi "
     "naval base, Zelensky confirmed."),
    ("UKRAINE  •  KYIV REGION",
     "186 drones rain on Ukraine overnight",
     "Russia launched 186 drones overnight; Ukraine downed 161. A strike "
     "hit a block in Dymer: 11 killed, 14 missing."),
    ("GULF  •  BAHRAIN & HORMUZ",
     "Missiles over Bahrain as Hormuz simmers",
     "Iran struck US bases in Bahrain; a civilian facility was hit, two "
     "hurt. Tehran claims two Patriot radars destroyed."),
    ("SUDAN  •  KHARTOUM",
     "Drone strikes hit Khartoum, UN building",
     "Early-Sunday drone strikes hit homes and a UN building in Khartoum "
     "and Omdurman — four killed."),
    ("SPORT  •  TURIN",
     "Alcaraz conquers Turin at last",
     "Carlos Alcaraz beat world No. 1 Alexander Zverev 6–2, 7–6 (9–7) in "
     "Turin for his first ATP Finals title."),
    ("USA  •  WASHINGTON",
     "Democrats' biggest House win since 1992",
     "Democrats secured at least 258 House seats — their largest majority "
     "since 1992, redrawing power in Washington."),
]

BRIEFS = [
    ("MARKETS SLIDE",
     "S&P 500 −3.7%, Nikkei −5.1% in the AI sell-off; Nvidia faces an SEC "
     "inquiry as CEO Huang resigns."),
    ("TRUMP vs IRAN",
     "Trump dares Iran to break the US port blockade; Iran moves 14 tankers "
     "to Kharg Island."),
    ("WEST BANK",
     "Settlers torch vehicles and homes near Ramallah; Eisenkot calls it "
     "\u201cJewish terrorism\u201d."),
    ("ISRAEL POLITICS",
     "Likud and Yashar end coalition talks with no deal; Eisenkot has "
     "until 6 Dec."),
    ("HOUTHIS",
     "Houthis say they hit the Rabigh refinery; the coalition says it "
     "stopped a drone and a missile."),
    ("SOUTH KOREA",
     "Education minister Choi Kyo-jin resigns over an AI cheating scandal "
     "in an exam."),
    ("INDONESIA",
     "Candy factory fire in Banten leaves 3 dead and dozens missing."),
    ("SPARTA II",
     "Russian cargo ship still burning off Finland; being towed out of "
     "Finnish waters."),
    ("NATO SCRAMBLE",
     "Polish F-16s and Swedish Gripens scramble over south-eastern Poland."),
    ("F-16 CLAIM",
     "US denies Iran's account that a missile damaged an F-16 over the Gulf."),
]


def render():
    img = Image.new("RGB", (PAGE, PAGE), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    title = "THE WORLD"
    tf = SERIF_B(84)
    tw = d.textlength(title, font=tf)
    d.text(((PAGE - tw) / 2, 8), title, font=tf, fill=INK)
    sub = "SUNDAY 22 NOVEMBER 2026  •  17 STORIES  •  7 REGIONS"
    sf = SANS_B(19)
    sw = d.textlength(sub, font=sf)
    d.text(((PAGE - sw) / 2, 100), sub, font=sf, fill=RED)
    double_rule(d, 126)

    # ---- lead story ----------------------------------------------------
    ly0, ly1 = 138, 340
    box(d, (MARGIN, ly0, PAGE - MARGIN, ly1), width=2, fill=PANEL)
    lx0, lx1 = MARGIN + 16, MARGIN + 566
    ax0, ax1 = MARGIN + 582, PAGE - MARGIN - 14
    d.text((lx0, ly0 + 10), "CLIMATE  •  ANTALYA, TÜRKIYE", font=SANS_B(16),
           fill=RED)
    hf = SERIF_B(32)
    y = para(d, lx0, ly0 + 34, "COP31 collapses in Antalya", hf, lx1 - lx0, 40)
    y = para(d, lx0, y + 6,
             "After 18 days and 48 hours of overtime — the longest climate "
             "summit ever — the UN talks ended on Sunday with no agreement. "
             "The EU, Britain and some 90 countries rejected the draft for "
             "leaving out fossil fuels; the $120bn finance target was "
             "dropped. Core decisions move to COP32 in Addis Ababa, "
             "November 2027.",
             SERIF(16), lx1 - lx0, 22)
    lead_art(d, ax0, ly0 + 12, ax1, ly1 - 14)

    # ---- six story cards, 3 x 2 ----------------------------------------
    gap = 12
    cw = (CW - 2 * gap) // 3
    ch, strip_h = 172, 42
    gy0 = 352
    for row in range(2):
        for col in range(3):
            i = row * 3 + col
            kicker, head, body = CARDS[i]
            x0 = MARGIN + col * (cw + gap)
            y0 = gy0 + row * (ch + gap)
            x1, y1 = x0 + cw, y0 + ch
            box(d, (x0, y0, x1, y1), width=2, fill=PANEL)
            STRIPS[i](d, x0 + 8, y0 + 8, x1 - 8, y0 + 8 + strip_h)
            ky = y0 + 8 + strip_h + 6
            d.text((x0 + 10, ky), kicker, font=SANS_B(13), fill=RED)
            hy = ky + 17
            hy = para(d, x0 + 10, hy, head, SERIF_B(19), cw - 20, 23)
            para(d, x0 + 10, hy + 2, body, SERIF(14), cw - 20, 17)

    # ---- the day in brief ----------------------------------------------
    by0 = gy0 + 2 * ch + gap + 12
    d.text((MARGIN, by0), "THE DAY IN BRIEF", font=SERIF_B(26), fill=INK)
    rf = SANS_B(14)
    rtxt = "TEN MORE STORIES  •  SUNDAY 22 NOVEMBER 2026"
    rw = d.textlength(rtxt, font=rf)
    d.text((PAGE - MARGIN - rw, by0 + 6), rtxt, font=rf, fill=RED)
    hline(d, MARGIN, PAGE - MARGIN, by0 + 36, 2)
    col_w = (CW - 30) // 2
    yy = by0 + 46
    for side in range(2):
        xx = MARGIN + side * (col_w + 30)
        y = yy
        for j in range(5):
            tag, text = BRIEFS[side * 5 + j]
            d.rectangle([xx, y + 4, xx + 8, y + 12], fill=RED)
            full = tag + " — " + text
            y = para(d, xx + 16, y, full, SERIF(14), col_w - 16, 18)
            y += 5
    # ---- footer --------------------------------------------------------
    fy = PAGE - 42
    double_rule(d, fy)
    ff = SANS_B(14)
    ftxt = "THE WORLD  •  SUNDAY 22 NOVEMBER 2026  •  CLIMATE  •  WAR  •  " \
           "GULF  •  SPORT  •  POLITICS"
    fw = d.textlength(ftxt, font=ff)
    d.text(((PAGE - fw) / 2, fy + 9), ftxt, font=ff, fill=INK)

    img.save(OUT)
    print("wrote", OUT, img.size)


if __name__ == "__main__":
    render()
