#!/usr/bin/env python3
"""THE WORLD — front page for Sunday 22 November 2026.
Draws a 1024x1024 newspaper front page with PIL only. No network, no files
beyond the DejaVu fonts shipped with the system.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 28  # page margin
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (248, 244, 233)
INK = (26, 26, 26)
RED = (164, 31, 31)
BLUE = (31, 78, 121)
GREY = (110, 105, 92)
LIGHT = (238, 231, 214)
SKY = (214, 230, 240)
SEA = (178, 205, 222)
SAND = (232, 214, 170)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw a wrapped paragraph; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def rule(draw, x0, x1, y, width=2, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=width)


def double_rule(draw, x0, x1, y, color=INK):
    draw.line([(x0, y), (x1, y)], fill=color, width=3)
    draw.line([(x0, y + 5), (x1, y + 5)], fill=color, width=1)


# ---------------------------------------------------------------- illustrations
def draw_lead_art(d, x, y, w, h):
    """Summit hall: cracked globe on a stage, row of flags, a gavel."""
    d.rectangle([x, y, x + w, y + h], fill=SKY, outline=INK, width=2)
    # stage floor band at the bottom
    d.rectangle([x, y + h - 40, x + w, y + h], fill=(196, 178, 142))
    # flag row along the top
    cols = [(164, 31, 31), (31, 78, 121), (46, 125, 50), (212, 160, 32),
            (120, 60, 140), (31, 78, 121)]
    for i, c in enumerate(cols):
        fx = x + 26 + i * 70
        d.line([(fx, y + 10), (fx, y + 52)], fill=INK, width=2)
        d.polygon([(fx, y + 10), (fx + 34, y + 20), (fx, y + 32)], fill=c)
    # cracked globe, centre-left, resting on the floor
    cx, cy, r = x + 140, y + 118, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 150, 190),
              outline=INK, width=3)
    # land blobs
    d.ellipse([cx - 38, cy - 36, cx - 6, cy - 8], fill=(74, 140, 74))
    d.ellipse([cx + 8, cy + 6, cx + 40, cy + 38], fill=(74, 140, 74))
    d.ellipse([cx - 10, cy - 44, cx + 22, cy - 22], fill=(74, 140, 74))
    # the crack: jagged black line across the globe
    pts = [(cx - 44, cy - 26), (cx - 24, cy - 4), (cx - 34, cy + 16),
           (cx - 6, cy + 30), (cx + 6, cy + 44), (cx + 26, cy + 38)]
    d.line(pts, fill=(20, 20, 20), width=5, joint="curve")
    d.line([(cx - 24, cy - 4), (cx - 2, cy - 18)], fill=(20, 20, 20), width=3)
    # gavel on the stage, right of the globe
    gx, gy = x + 312, y + 122
    d.rectangle([gx - 8, gy + 26, gx + 96, gy + 34], fill=(120, 82, 40))
    d.rectangle([gx + 18, gy - 6, gx + 70, gy + 22], fill=(146, 100, 52),
                outline=INK, width=2)
    d.line([(gx + 44, gy - 6), (gx + 44, gy + 26)], fill=INK, width=2)
    d.text((gx + 8, gy + 40), "NO DEAL", font=font(SANS_B, 14), fill=RED)


def draw_ship_art(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=INK, width=2)
    # sky + sea
    d.rectangle([x, y, x + w, y + 62], fill=(226, 236, 242))
    d.rectangle([x, y + 62, x + w, y + h], fill=SEA)
    for wy in (y + 78, y + 100, y + 122):
        for wx in range(x + 8, x + w - 20, 34):
            d.arc([wx, wy, wx + 26, wy + 10], 0, 180, fill=(255, 255, 255),
                  width=2)
    # corvette silhouette
    d.polygon([(x + 18, y + 96), (x + 108, y + 96), (x + 96, y + 76),
               (x + 30, y + 76)], fill=(52, 58, 64))
    d.rectangle([x + 44, y + 60, x + 78, y + 76], fill=(52, 58, 64))
    d.line([(x + 60, y + 60), (x + 60, y + 44)], fill=(52, 58, 64), width=3)
    # explosion starburst over the stern
    import math
    ex, ey = x + 96, y + 48
    burst = []
    for i in range(16):
        ang = math.pi * i / 8
        rr = 20 if i % 2 == 0 else 9
        burst.append((ex + rr * math.cos(ang), ey + rr * math.sin(ang)))
    d.polygon(burst, fill=(240, 140, 40), outline=(200, 60, 20))
    d.ellipse([ex - 7, ey - 7, ex + 7, ey + 7], fill=(255, 220, 90))
    # sea drone approaching
    d.ellipse([x + 8, y + 112, x + 30, y + 122], fill=(30, 30, 30))
    d.line([(x + 30, y + 117), (x + 46, y + 108)], fill=(30, 30, 30), width=2)


def draw_drones_art(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 54), outline=INK, width=2)
    # stars
    for sx, sy in [(14, 14), (44, 30), (80, 12), (104, 34), (30, 52),
                   (66, 48), (118, 16)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=(255, 255, 255))
    # apartment block, damaged corner
    d.rectangle([x + 14, y + 58, x + 92, y + h - 8], fill=(150, 140, 120),
                outline=INK, width=2)
    for fy in range(y + 66, y + h - 14, 16):
        for fx in range(x + 22, x + 86, 16):
            d.rectangle([fx, fy, fx + 9, fy + 9], fill=(240, 200, 90))
    # collapsed corner (dark rubble)
    d.polygon([(x + 72, y + 58), (x + 92, y + 58), (x + 92, y + 96),
               (x + 80, y + 108), (x + 66, y + 88)], fill=(40, 36, 30))
    d.polygon([(x + 66, y + 108), (x + 92, y + 108), (x + 92, y + 96),
               (x + 80, y + 108)], fill=(70, 64, 54))
    # drones with trails
    for dx, dy in [(x + 100, y + 20), (x + 116, y + 40), (x + 98, y + 58)]:
        d.line([(dx - 22, dy + 14), (dx, dy)], fill=(240, 140, 40), width=2)
        d.ellipse([dx - 4, dy - 3, dx + 4, dy + 3], fill=(255, 200, 80))
        d.line([(dx - 7, dy), (dx + 7, dy)], fill=(255, 200, 80), width=2)


def draw_gulf_art(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 200), outline=INK,
                width=2)
    # dusk sky
    d.rectangle([x, y, x + w, y + 66], fill=(240, 180, 120))
    d.ellipse([x + 96, y + 12, x + 120, y + 36], fill=(255, 230, 160))
    # missile flying left to right with a broken smoke trail
    mx, my = x + 78, y + 30
    for sx0, sx1 in [(x + 8, x + 24), (x + 30, x + 46), (x + 52, x + 64)]:
        d.line([(sx0, my + 8), (sx1, my + 2)], fill=(120, 110, 100), width=3)
    d.polygon([(mx, my - 9), (mx + 18, my), (mx, my + 9), (mx + 4, my)],
              fill=(60, 60, 60))
    d.ellipse([mx + 12, my - 4, mx + 20, my + 4], fill=(240, 140, 40))
    # radar dish
    d.arc([x + 12, y + 66, x + 52, y + 106], 180, 360, fill=(60, 60, 60),
          width=3)
    d.line([(x + 32, y + 86), (x + 32, y + 116)], fill=(60, 60, 60), width=3)
    d.line([(x + 32, y + 86), (x + 52, y + 66)], fill=(200, 60, 20), width=2)
    # supertanker on the water
    d.rectangle([x, y + 100, x + w, y + h], fill=(120, 160, 190))
    d.rectangle([x + 56, y + 108, x + 122, y + 122], fill=(140, 40, 40),
                outline=INK, width=1)
    d.rectangle([x + 100, y + 96, x + 116, y + 108], fill=(220, 220, 220),
                outline=INK, width=1)


def draw_sudan_art(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SAND, outline=INK, width=2)
    # UN building
    d.rectangle([x + 18, y + 52, x + 96, y + h - 10], fill=(240, 236, 220),
                outline=INK, width=2)
    for fy in range(y + 60, y + h - 16, 15):
        for fx in range(x + 26, x + 90, 15):
            d.rectangle([fx, fy, fx + 8, fy + 8], fill=(90, 120, 160))
    # UN flag
    d.line([(x + 57, y + 52), (x + 57, y + 22)], fill=INK, width=2)
    d.rectangle([x + 57, y + 22, x + 92, y + 40], fill=(70, 120, 190),
                outline=INK, width=1)
    d.ellipse([x + 66, y + 25, x + 82, y + 37], outline=(255, 255, 255),
              width=1)
    # smoke + drone
    d.ellipse([x + 96, y + 30, x + 118, y + 48], fill=(120, 110, 100))
    d.ellipse([x + 104, y + 22, x + 120, y + 38], fill=(150, 140, 128))
    d.ellipse([x + 8, y + 16, x + 26, y + 24], fill=(30, 30, 30))
    d.line([(x + 26, y + 20), (x + 40, y + 26)], fill=(30, 30, 30), width=2)


def draw_tennis_art(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 140, 90), outline=INK, width=2)
    # court lines
    d.rectangle([x + 14, y + 18, x + w - 14, y + h - 18], outline=(255, 255, 255),
                width=2)
    d.line([(x + w // 2, y + 18), (x + w // 2, y + h - 18)],
           fill=(255, 255, 255), width=2)
    d.line([(x + 14, y + h // 2), (x + w - 14, y + h // 2)],
           fill=(255, 255, 255), width=3)
    # net
    d.rectangle([x + 14, y + h // 2 - 4, x + w - 14, y + h // 2 + 4],
                fill=(40, 40, 40))
    # ball + trophy
    d.ellipse([x + 88, y + 26, x + 106, y + 44], fill=(220, 230, 60),
              outline=INK, width=1)
    d.arc([x + 88, y + 26, x + 106, y + 44], 200, 340, fill=(255, 255, 255),
          width=2)
    # trophy
    tx, ty = x + 34, y + h - 52
    d.polygon([(tx, ty), (tx + 34, ty), (tx + 30, ty + 22), (tx + 4, ty + 22)],
              fill=(220, 180, 40), outline=INK, width=1)
    d.arc([tx - 8, ty + 2, tx + 6, ty + 16], 90, 270, fill=(220, 180, 40),
          width=3)
    d.arc([tx + 28, ty + 2, tx + 42, ty + 16], 270, 90, fill=(220, 180, 40),
          width=3)
    d.rectangle([tx + 12, ty + 22, tx + 22, ty + 30], fill=(220, 180, 40),
                outline=INK, width=1)
    d.rectangle([tx + 6, ty + 30, tx + 28, ty + 35], fill=(220, 180, 40),
                outline=INK, width=1)


def draw_capitol_art(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 240), outline=INK,
                width=2)
    # stars
    for sx, sy in [(16, 14), (46, 10), (112, 12), (96, 30), (28, 30)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1],
                  fill=RED)
    # capitol dome
    d.rectangle([x + 16, y + h - 34, x + w - 16, y + h - 10], fill=(240, 240, 235),
                outline=INK, width=2)
    d.rectangle([x + 30, y + h - 58, x + w - 30, y + h - 34], fill=(240, 240, 235),
                outline=INK, width=2)
    d.pieslice([x + 40, y + 22, x + w - 40, y + h - 40], 180, 360,
               fill=(240, 240, 235), outline=INK, width=2)
    d.line([(x + w // 2, y + 22), (x + w // 2, y + 10)], fill=INK, width=2)
    d.ellipse([x + w // 2 - 3, y + 6, x + w // 2 + 3, y + 12], fill=RED)
    # columns
    for cx in range(x + 36, x + w - 36, 18):
        d.line([(cx, y + h - 58), (cx, y + h - 34)], fill=INK, width=2)
    # "258" banner, full width of the panel, text centred
    d.rectangle([x + 12, y + h - 30, x + w - 12, y + h - 12], fill=BLUE)
    banner = "258 SEATS"
    bf = font(SANS_B, 11)
    bw = d.textlength(banner, font=bf)
    d.text((x + (w - bw) / 2, y + h - 29), banner, font=bf,
           fill=(255, 255, 255))


# ------------------------------------------------------------------- stories
CARDS = [
    dict(tag="UKRAINE  •  MEDITERRANEAN", art=draw_ship_art,
         head="Ukraine sinks Russian corvette at Benghazi",
         body="Seven Ukrainian sea drones struck the corvette Merkury docked "
              "at Benghazi naval base, Zelensky confirmed. A second vessel "
              "was also hit — the war reaches the Mediterranean."),
    dict(tag="UKRAINE  •  KYIV REGION", art=draw_drones_art,
         head="186 drones rain on Ukraine overnight",
         body="Russia launched 186 drones; Ukraine says it downed 161. A "
              "strike partly collapsed a five-storey block in Dymer, north "
              "of Kyiv — at least 11 killed, 14 missing."),
    dict(tag="GULF  •  BAHRAIN & HORMUZ", art=draw_gulf_art,
         head="Missiles over Bahrain as Hormuz simmers",
         body="Iran struck US bases in Bahrain; a civilian industrial site "
              "was hit and two people hurt. Tehran claims two US Patriot "
              "radars destroyed, and says two tankers hit mines off Hormuz."),
    dict(tag="SUDAN  •  KHARTOUM", art=draw_sudan_art,
         head="Drone strikes hit Khartoum and a UN building",
         body="Early-Sunday drone strikes hit homes and a UN facility in "
              "Khartoum, Omdurman and Jebel Aulia — at least four killed, "
              "the UN building damaged while staff were inside."),
    dict(tag="SPORT  •  TURIN", art=draw_tennis_art,
         head="Alcaraz conquers Turin at last",
         body="Carlos Alcaraz beat world No. 1 Alexander Zverev 6–2, 7–6 "
              "(9–7) for his first ATP Finals title — a 14-match win "
              "streak, and only the fourth man to hold all four Slams plus "
              "the Finals."),
    dict(tag="USA  •  WASHINGTON", art=draw_capitol_art,
         head="Democrats' biggest House win since 1992",
         body="Democrats secured at least 258 House seats — their largest "
              "majority since 1992, redrawing the balance of power in "
              "Washington."),
]

LEAD_BODY = (
    "After 18 days and 48 hours of overtime — the longest climate summit "
    "ever — the UN talks ended on Sunday with no agreement. The EU, "
    "Britain, Panama, the Marshall Islands and some 90 countries rejected "
    "the final draft because it left out fossil fuels. The $120bn "
    "adaptation-finance target was dropped; only a pledge to triple "
    "funding survived. Core decisions move to COP32 in Addis Ababa, "
    "November 2027."
)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead
    title = "THE WORLD"
    tf = font(SERIF_B, 82)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 14), title, font=tf, fill=INK)
    sub = "SUNDAY 22 NOVEMBER 2026  •  SEVEN REGIONS  •  ONE DAY"
    sf = font(SANS_B, 17)
    sw = d.textlength(sub, font=sf)
    d.text(((W - sw) / 2, 106), sub, font=sf, fill=RED)
    double_rule(d, M, W - M, 132)

    # ---- lead story
    y = 146
    d.text((M, y), "CLIMATE  •  ANTALYA, TURKIYE", font=font(SANS_B, 15),
           fill=RED)
    y += 22
    head_f = font(SERIF_B, 40)
    head = "COP31 TALKS COLLAPSE IN ANTALYA"
    hw = d.textlength(head, font=head_f)
    d.text((M, y), head, font=head_f, fill=INK)
    y += 52
    art_x, art_y, art_w, art_h = M, y, 452, 196
    draw_lead_art(d, art_x, art_y, art_w, art_h)
    body_x = art_x + art_w + 18
    body_w = W - M - body_x
    para(d, body_x, art_y + 2, LEAD_BODY, font(SANS, 15), body_w, 20)
    y = art_y + art_h + 14
    rule(d, M, W - M, y, width=2)

    # ---- six smaller stories: 2 columns x 3 rows
    col_w = (W - 2 * M - 16) // 2
    row_h = 162
    gx0, gy0 = M, y + 12
    for i, c in enumerate(CARDS):
        cx = gx0 + (i % 2) * (col_w + 16)
        cy = gy0 + (i // 2) * (row_h + 14)
        d.rectangle([cx, cy, cx + col_w, cy + row_h], outline=GREY, width=1)
        ax, ay, aw, ah = cx + 8, cy + 8, 128, row_h - 16
        c["art"](d, ax, ay, aw, ah)
        tx = ax + aw + 10
        tw_ = cx + col_w - 10 - tx
        ty = cy + 8
        d.text((tx, ty), c["tag"], font=font(SANS_B, 11), fill=RED)
        ty += 17
        ty = para(d, tx, ty, c["head"], font(SERIF_B, 18), tw_, 21)
        ty += 3
        para(d, tx, ty, c["body"], font(SANS, 12), tw_, 15)

    # ---- footer strip
    fy = gy0 + 3 * row_h + 2 * 14 + 10
    rule(d, M, W - M, fy, width=2)
    foot = "THE WORLD  •  SUNDAY 22 NOVEMBER 2026  •  CLIMATE  •  WAR  •  GULF  •  SPORT  •  POLITICS"
    ff = font(SANS_B, 13)
    fw = d.textlength(foot, font=ff)
    d.text(((W - fw) / 2, fy + 8), foot, font=ff, fill=INK)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out)
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
