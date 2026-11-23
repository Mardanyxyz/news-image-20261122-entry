#!/usr/bin/env python3
"""THE WORLD — Sunday 22 November 2026 front page, version 2.

Draws a 1024x1024 newspaper front page with PIL only (DejaVu fonts,
no network, no external images). Seven main stories plus a ten-item
"THE DAY IN BRIEF" section: 17 stories across 7 regions.

Run:  python3 draw.py   -> writes entry.png beside this file.
"""

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 240, 220)
INK = (26, 26, 26)
RED = (164, 31, 31)
BLUE = (31, 78, 121)
SKY = (198, 222, 240)
NIGHT = (18, 30, 58)
SAND = (214, 196, 150)
GREEN = (46, 110, 58)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def load(path, size):
    return ImageFont.truetype(path, size)


F = {
    "mast": load(SERIF, 96),
    "dateline": load(SANS_B, 20),
    "kick": load(SANS_B, 14),
    "lead_head": load(SERIF, 33),
    "head": load(SERIF, 21),
    "body": load(SANS, 15),
    "body_sm": load(SANS, 14),
    "card": load(SANS, 13),
    "brief": load(SANS, 13),
    "brief_b": load(SANS_B, 13),
    "foot": load(SANS_B, 14),
    "tag": load(SANS_B, 15),
}

page = Image.new("RGB", (W, H), PAPER)
pen = ImageDraw.Draw(page)


def wrap_text(text, font, width):
    """Greedy word wrap measured in pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if pen.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(x, y, text, font, width, leading, color=INK, limit=None):
    """Draw wrapped paragraph; return y just below the last line."""
    lines = wrap_text(text, font, width)
    if limit:
        lines = lines[:limit]
    for ln in lines:
        pen.text((x, y), ln, font=font, fill=color)
        y += leading
    return y


def rule(y, weight=2, x0=28, x1=996):
    pen.line([(x0, y), (x1, y)], fill=INK, width=weight)


def double_rule(y):
    rule(y, 3)
    rule(y + 5, 1)


def kicker_head(x, y, width, kick, headline, head_font, head_lead=25):
    pen.text((x, y), kick, font=F["kick"], fill=RED)
    y += 20
    lines = wrap_text(headline, head_font, width)
    for ln in lines:
        pen.text((x, y), ln, font=head_font, fill=INK)
        y += head_lead
    return y


# ---------------------------------------------------------------- masthead
pen.text((W // 2, 6), "THE WORLD", font=F["mast"], fill=INK, anchor="ma")
sub = "SUNDAY 22 NOVEMBER 2026  \u2022  17 STORIES  \u2022  7 REGIONS"
pen.text((W // 2, 108), sub, font=F["dateline"], fill=RED, anchor="ma")
double_rule(136)

# ---------------------------------------------------------------- lead story
LX, LY, LW = 28, 148, 968
pen.rectangle([LX, LY, LX + LW, LY + 152], outline=INK, width=2)
pen.text((LX + 14, LY + 8), "CLIMATE  \u2022  ANTALYA, T\u00dcRKIYE", font=F["kick"], fill=RED)
pen.text((LX + 14, LY + 30), "COP31 collapses in Antalya",
         font=F["lead_head"], fill=INK)

lead_body = ("After 18 days and 48 hours of overtime \u2014 the longest climate "
             "summit ever \u2014 the UN talks ended on Sunday with no agreement. "
             "The EU, Britain and some 90 countries rejected the draft for "
             "leaving out fossil fuels; the $120bn finance target was dropped. "
             "Core decisions move to COP32 in Addis Ababa, November 2027.")
para(LX + 14, LY + 72, lead_body, F["body_sm"], 600, 18, limit=4)

# Lead illustration: globe on a cracked shore, flags, NO DEAL ribbon.
IX, IY, IW, IH = 668, LY + 8, 314, 142
pen.rectangle([IX, IY, IX + IW, IY + IH], fill=SKY, outline=INK, width=2)
pen.rectangle([IX, IY + 108, IX + IW, IY + IH], fill=SAND)
flag_cols = [(164, 31, 31), (31, 78, 121), (46, 110, 58),
             (232, 150, 60), (110, 60, 140), (31, 120, 120)]
for i, c in enumerate(flag_cols):
    fx = IX + 18 + i * 50
    pen.line([(fx, IY + 12), (fx, IY + 44)], fill=INK, width=2)
    pen.polygon([(fx, IY + 12), (fx + 26, IY + 19), (fx, IY + 26)], fill=c)
# Globe with a crack.
pen.ellipse([IX + 52, IY + 46, IX + 132, IY + 126], fill=(110, 180, 220),
            outline=INK, width=3)
pen.ellipse([IX + 66, IY + 56, IX + 92, IY + 76], fill=GREEN)
pen.ellipse([IX + 96, IY + 88, IX + 120, IY + 108], fill=GREEN)
pen.line([(IX + 92, IY + 46), (IX + 84, IY + 70), (IX + 100, IY + 92),
          (IX + 88, IY + 126)], fill=INK, width=3)
# Empty chairs / table.
pen.rectangle([IX + 168, IY + 96, IX + 296, IY + 104], fill=(140, 100, 60),
              outline=INK, width=2)
pen.rectangle([IX + 180, IY + 72, IX + 212, IY + 96], fill=(120, 84, 52),
              outline=INK, width=2)
pen.rectangle([IX + 252, IY + 72, IX + 284, IY + 96], fill=(120, 84, 52),
              outline=INK, width=2)
pen.rectangle([IX + 196, IY + 112, IX + 268, IY + 130], fill=RED)
pen.text((IX + 232, IY + 113), "NO DEAL", font=F["tag"], fill=(255, 255, 255),
         anchor="ma")

# ---------------------------------------------------------------- story rows
COL_W = 310
GAP = 19
X0 = 28


def mini_scene(box, kind):
    """Small drawn scene strip at the top of a card."""
    x, y, w, h = box
    if kind == "ship":
        pen.rectangle([x, y, x + w, y + h], fill=SKY, outline=INK, width=1)
        pen.polygon([(x + 90, y + 8), (x + 150, y + 8), (x + 168, y + 30),
                     (x + 72, y + 30)], fill=(60, 60, 60))
        pen.rectangle([x + 108, y - 2, x + 118, y + 10], fill=(60, 60, 60))
        pen.ellipse([x + 176, y + 2, x + 206, y + 32], fill=(255, 170, 40))
        for wx in range(x + 8, x + w - 8, 26):
            pen.arc([wx, y + h - 12, wx + 22, y + h + 2], 180, 360, fill=BLUE, width=2)
    elif kind == "drones":
        pen.rectangle([x, y, x + w, y + h], fill=NIGHT, outline=INK, width=1)
        for sx, sy in [(x + 30, y + 6), (x + 90, y + 14), (x + 200, y + 8),
                       (x + 260, y + 16)]:
            pen.ellipse([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))
        pen.rectangle([x + 40, y + 18, x + 150, y + h], fill=(90, 90, 100),
                      outline=INK, width=1)
        for wy in range(y + 24, y + h - 4, 12):
            for wx in range(x + 46, x + 144, 14):
                pen.rectangle([wx, wy, wx + 7, wy + 6], fill=(255, 210, 90))
        for dx, dy in [(x + 180, y + 10), (x + 220, y + 20), (x + 250, y + 6)]:
            pen.ellipse([dx, dy, dx + 6, dy + 6], fill=(255, 120, 40))
            pen.line([(dx, dy + 3), (dx - 22, dy + 12)], fill=(255, 120, 40), width=2)
    elif kind == "gulf":
        pen.rectangle([x, y, x + w, y + h], fill=(255, 214, 150), outline=INK, width=1)
        pen.ellipse([x + w - 52, y + 4, x + w - 22, y + 34], fill=(255, 220, 120))
        for mx in range(x + 10, x + 150, 42):
            pen.polygon([(mx, y + 22), (mx + 26, y + 16), (mx + 26, y + 28)],
                        fill=(80, 80, 80))
            pen.line([(mx, y + 22), (mx - 14, y + 30)], fill=(120, 120, 120), width=2)
        pen.rectangle([x, y + h - 14, x + w, y + h], fill=(90, 140, 190))
        pen.rectangle([x + 170, y + h - 26, x + 250, y + h - 12], fill=(140, 40, 40))
    elif kind == "sudan":
        pen.rectangle([x, y, x + w, y + h], fill=(240, 225, 190), outline=INK, width=1)
        pen.rectangle([x + 60, y + 6, x + 250, y + h - 6], fill=(210, 200, 170),
                      outline=INK, width=1)
        for wy in range(y + 12, y + h - 10, 12):
            for wx in range(x + 68, x + 244, 16):
                pen.rectangle([wx, wy, wx + 9, wy + 7], fill=(90, 120, 150))
        pen.rectangle([x + 120, y + 2, x + 190, y + 14], fill=(40, 90, 160))
        pen.ellipse([x + 148, y + 5, x + 162, y + 12], fill=(255, 255, 255))
        pen.line([(x + 20, y + 30), (x + 48, y + 8)], fill=(80, 80, 80), width=3)
        pen.ellipse([x + 14, y + 26, x + 28, y + 38], fill=(90, 90, 90))
    elif kind == "tennis":
        pen.rectangle([x, y, x + w, y + h], fill=GREEN, outline=INK, width=1)
        pen.rectangle([x + 10, y + 5, x + w - 10, y + h - 5], outline=(255, 255, 255),
                      width=2)
        pen.line([(x + w // 2, y + 5), (x + w // 2, y + h - 5)], fill=(255, 255, 255),
                 width=2)
        pen.line([(x + 10, y + h // 2), (x + w - 10, y + h // 2)],
                 fill=(255, 255, 255), width=2)
        pen.ellipse([x + w - 62, y + 8, x + w - 40, y + 30], fill=(220, 230, 60),
                    outline=INK, width=1)
        pen.polygon([(x + 24, y + h - 22), (x + 62, y + h - 22), (x + 56, y + h - 6),
                     (x + 30, y + h - 6)], fill=(255, 210, 60), outline=INK, width=1)
    elif kind == "capitol":
        pen.rectangle([x, y, x + w, y + h], fill=(225, 232, 240), outline=INK, width=1)
        pen.pieslice([x + 110, y + 2, x + 200, y + 26], 180, 360, fill=(240, 240, 240),
                     outline=INK, width=2)
        pen.rectangle([x + 96, y + 20, x + 214, y + h - 6], fill=(240, 240, 240),
                      outline=INK, width=1)
        for cx in range(x + 104, x + 208, 26):
            pen.rectangle([cx, y + 24, cx + 8, y + h - 10], fill=(180, 180, 180))
        pen.rectangle([x + 30, y + h - 18, x + w - 30, y + h - 2], fill=BLUE)
        pen.text((x + w // 2, y + h - 17), "258 SEATS", font=F["tag"],
                 fill=(255, 255, 255), anchor="ma")


def story_card(x, y, w, h, scene, kick, headline, body, head_font=F["head"]):
    pen.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    mini_scene((x + 8, y + 8, w - 16, 38), scene)
    ty = kicker_head(x + 10, y + 54, w - 20, kick, headline, head_font, 23)
    para(x + 10, ty + 2, body, F["card"], w - 20, 15, limit=3)


ROW1_Y, ROW1_H = 312, 172
story_card(X0, ROW1_Y, COL_W, ROW1_H, "ship",
           "UKRAINE  \u2022  MEDITERRANEAN",
           "Ukraine sinks Russian corvette at Benghazi",
           "Seven Ukrainian sea drones struck the corvette Merkury at Benghazi "
           "naval base, Zelensky confirmed.")
story_card(X0 + COL_W + GAP, ROW1_Y, COL_W, ROW1_H, "drones",
           "UKRAINE  \u2022  KYIV REGION",
           "186 drones rain on Ukraine overnight",
           "Russia launched 186 drones overnight; Ukraine downed 161. "
           "A strike hit a block in Dymer: 11 killed, 14 missing.")
story_card(X0 + 2 * (COL_W + GAP), ROW1_Y, COL_W, ROW1_H, "gulf",
           "GULF  \u2022  BAHRAIN & HORMUZ",
           "Missiles over Bahrain as Hormuz simmers",
           "Iran struck US bases in Bahrain; a civilian facility was hit, two "
           "hurt. Tehran claims two Patriot radars destroyed.")

ROW2_Y, ROW2_H = 496, 172
story_card(X0, ROW2_Y, COL_W, ROW2_H, "sudan",
           "SUDAN  \u2022  KHARTOUM",
           "Drone strikes hit Khartoum, UN building",
           "Early-Sunday drone strikes hit homes and a UN building in Khartoum, "
           "Omdurman and Jebel Aulia \u2014 at least four killed.")
story_card(X0 + COL_W + GAP, ROW2_Y, COL_W, ROW2_H, "tennis",
           "SPORT  \u2022  TURIN",
           "Alcaraz conquers Turin at last",
           "Carlos Alcaraz beat world No. 1 Alexander Zverev 6\u20132, 7\u20136 (9\u20137) "
           "in Turin for his first ATP Finals title.")
story_card(X0 + 2 * (COL_W + GAP), ROW2_Y, COL_W, ROW2_H, "capitol",
           "USA  \u2022  WASHINGTON",
           "Democrats' biggest House win since 1992",
           "Democrats secured at least 258 House seats \u2014 their largest "
           "majority since 1992, redrawing power in Washington.")

# ---------------------------------------------------------------- the day in brief
BY = 680
pen.text((28, BY), "THE DAY IN BRIEF", font=load(SERIF, 26), fill=INK)
pen.text((996, BY + 6), "TEN MORE STORIES  \u2022  SUNDAY 22 NOVEMBER 2026",
         font=F["kick"], fill=RED, anchor="ra")
double_rule(BY + 36)

BRIEFS = [
    ("MARKETS SLIDE \u2014 ", "S&P 500 \u22123.7%, Nikkei \u22125.1% in the AI sell-off; "
     "Nvidia faces an SEC inquiry as CEO Huang resigns."),
    ("TRUMP vs IRAN \u2014 ", "Trump dares Iran to break the US port blockade; Iran "
     "moves 14 tankers to Kharg Island."),
    ("WEST BANK \u2014 ", "Settlers torch vehicles and homes near Ramallah; Eisenkot "
     "calls it \u201cJewish terrorism\u201d."),
    ("ISRAEL POLITICS \u2014 ", "Likud and Yashar end coalition talks with no deal; "
     "Eisenkot has until 6 Dec."),
    ("HOUTHIS \u2014 ", "Houthis say they hit the Rabigh refinery; the coalition says "
     "it stopped a drone and a missile."),
    ("SOUTH KOREA \u2014 ", "Education minister Choi Kyo-jin resigns over an AI "
     "cheating scandal in an exam."),
    ("INDONESIA \u2014 ", "Candy factory fire in Banten leaves 3 dead and dozens missing."),
    ("SPARTA II \u2014 ", "Russian cargo ship still burning off Finland; being towed "
     "out of Finnish waters."),
    ("NATO SCRAMBLE \u2014 ", "Polish F-16s and Swedish Gripens scramble over "
     "south-eastern Poland."),
    ("F-16 CLAIM \u2014 ", "US denies Iran\u2019s account that a missile damaged an "
     "F-16 over the Gulf."),
]

COL_X = [28, 522]
COL_WB = 462
for i, (lead, rest) in enumerate(BRIEFS):
    col = i // 5
    row = i % 5
    bx = COL_X[col]
    by = BY + 50 + row * 50
    pen.text((bx, by), "\u25aa", font=F["brief_b"], fill=RED)
    lead_w = pen.textlength(lead, font=F["brief_b"])
    pen.text((bx + 16, by), lead, font=F["brief_b"], fill=INK)
    words = rest.split()
    cur = ""
    leftover = []
    stopped = False
    for w in words:
        if stopped:
            leftover.append(w)
            continue
        trial = (cur + " " + w).strip()
        if pen.textlength(trial, font=F["brief"]) + lead_w <= COL_WB - 16:
            cur = trial
        else:
            leftover.append(w)
            stopped = True
    pen.text((bx + 16 + lead_w, by), cur, font=F["brief"], fill=INK)
    if leftover:
        rem = " ".join(leftover)
        rem_lines = wrap_text(rem, F["brief"], COL_WB - 16)
        yy = by + 17
        for ln in rem_lines[:1]:
            pen.text((bx + 16, yy), ln, font=F["brief"], fill=INK)
            yy += 17

# ---------------------------------------------------------------- footer
double_rule(988)
pen.text((W // 2, 1004), "THE WORLD  \u2022  SUNDAY 22 NOVEMBER 2026  \u2022  "
         "CLIMATE  \u2022  WAR  \u2022  GULF  \u2022  SPORT  \u2022  POLITICS",
         font=F["foot"], fill=INK, anchor="ma")

page.save("entry.png")
print("wrote entry.png", page.size)
