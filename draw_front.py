#!/usr/bin/env python3
"""Draw the front page of 'The Day in the World' for 25 November 2026.

Run: python3 draw_front.py  -> writes entry.png (1024x1024) next to this file.
Only Pillow is needed at build time; main.py (the graded entrypoint) only
copies the finished entry.png with the standard library.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
INK = (18, 18, 18)
PAPER = (247, 243, 234)
RED = (158, 28, 28)
BLUE = (28, 62, 110)
GREY = (96, 92, 84)
RULE = (60, 58, 52)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap returning a list of lines that fit `width` px."""
    lines = []
    for para in text.split("\n"):
        line = ""
        for word in para.split():
            trial = (line + " " + word).strip()
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=1.28, max_lines=None):
    """Draw wrapped text, return y just below the last line."""
    lines = wrap(draw, text, fnt, width)
    if max_lines is not None and len(lines) > max_lines:
        lines = lines[:max_lines]
        # mark the cut so nothing reads as a dangling half-sentence
        lines[-1] = lines[-1].rstrip(" .,;") + "…"
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def hline(draw, x0, x1, y, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def icon(draw, kind, x, y, s=44):
    """Tiny pictogram drawn from basic shapes, top-left at (x, y)."""
    if kind == "refinery":  # factory + flame
        draw.rectangle([x, y + 22, x + s, y + s], fill=GREY)
        draw.rectangle([x + 6, y + 6, x + 12, y + 22], fill=GREY)
        draw.rectangle([x + 18, y + 2, x + 24, y + 22], fill=GREY)
        draw.polygon([(x + 30, y + 14), (x + 38, y + 2),
                      (x + 42, y + 14)], fill=RED)
    elif kind == "chart":  # bars rising then falling
        bw = s // 4
        heights = [12, 22, 32, 18]
        for i, hh in enumerate(heights):
            draw.rectangle([x + i * (bw + 2), y + s - hh,
                            x + i * (bw + 2) + bw, y + s], fill=BLUE)
    elif kind == "flame":
        draw.polygon([(x + s // 2, y), (x + s, y + s // 2),
                      (x + s * 3 // 4, y + s), (x + s // 4, y + s),
                      (x, y + s // 2)], fill=RED)
        draw.polygon([(x + s // 2, y + 14), (x + s * 3 // 4, y + s - 6),
                      (x + s // 4, y + s - 6)], fill=(232, 140, 40))
    elif kind == "building":
        draw.rectangle([x + 4, y + 8, x + s - 4, y + s], fill=GREY)
        for r in range(2):
            for c in range(3):
                draw.rectangle([x + 9 + c * 12, y + 14 + r * 14,
                                x + 15 + c * 12, y + 22 + r * 14],
                               fill=PAPER)
    elif kind == "market":  # falling line chart
        draw.line([(x, y + 8), (x + s // 3, y + 18),
                   (x + 2 * s // 3, y + 16), (x + s, y + s - 4)],
                  fill=RED, width=4)
        draw.polygon([(x + s - 10, y + s - 4), (x + s, y + s - 14),
                      (x + s, y + s - 4)], fill=RED)
    elif kind == "gavel":
        draw.rectangle([x + 6, y + 6, x + s - 6, y + 16], fill=GREY)
        draw.line([(x + s // 2, y + 16), (x + s // 2, y + s)],
                  fill=GREY, width=5)
        draw.rectangle([x + 4, y + s - 6, x + s - 4, y + s], fill=GREY)
    elif kind == "rocket":
        draw.polygon([(x + s // 2, y), (x + s - 6, y + s - 14),
                      (x + s // 2, y + s - 6), (x + 6, y + s - 14)],
                     fill=BLUE)
        draw.ellipse([x + s // 2 - 5, y + 14, x + s // 2 + 5, y + 24],
                     fill=PAPER)
        draw.polygon([(x + s // 2 - 4, y + s - 8), (x + s // 2 + 4, y + s - 8),
                      (x + s // 2, y + s)], fill=RED)
    elif kind == "flags":
        draw.line([(x + 8, y), (x + 8, y + s)], fill=INK, width=3)
        draw.line([(x + s - 8, y), (x + s - 8, y + s)], fill=INK, width=3)
        draw.polygon([(x + 8, y), (x + 26, y + 5), (x + 8, y + 12)],
                     fill=BLUE)
        draw.polygon([(x + s - 8, y), (x + s - 26, y + 5),
                      (x + s - 8, y + 12)], fill=RED)
    elif kind == "globe":
        draw.ellipse([x, y, x + s, y + s], outline=BLUE, width=3)
        draw.arc([x + 8, y, x + s - 8, y + s], 200, 340, fill=BLUE, width=2)
        draw.line([(x, y + s // 2), (x + s, y + s // 2)], fill=BLUE, width=2)
        draw.polygon([(x + s // 2 - 6, y + s - 2), (x + s // 2 + 6, y + s - 2),
                      (x + s // 2, y + s // 2 + 4)], fill=(60, 140, 70))


def draw_lead_art(draw, x0, y0, x1, y1):
    """Strait of Hormuz: dark sea, tanker, mine blast and fire."""
    # sky and sea
    draw.rectangle([x0, y0, x1, y0 + (y1 - y0) // 2], fill=(214, 226, 238))
    draw.rectangle([x0, y0 + (y1 - y0) // 2, x1, y1], fill=(38, 78, 110))
    # sun
    draw.ellipse([x1 - 62, y0 + 14, x1 - 22, y0 + 54], fill=(240, 190, 90))
    # tanker hull
    hy = y0 + (y1 - y0) // 2 + 26
    draw.rectangle([x0 + 18, hy, x1 - 30, hy + 34], fill=(120, 30, 26))
    draw.rectangle([x0 + 18, hy, x1 - 30, hy + 8], fill=(178, 52, 40))
    # bridge tower
    draw.rectangle([x1 - 92, hy - 34, x1 - 52, hy], fill=(232, 232, 224))
    draw.rectangle([x1 - 92, hy - 34, x1 - 52, hy - 26], fill=(40, 60, 80))
    # funnel with smoke
    draw.rectangle([x0 + 34, hy - 26, x0 + 58, hy], fill=(232, 200, 60))
    for i, (cx, cy, r) in enumerate([(x0 + 46, hy - 44, 12),
                                     (x0 + 58, hy - 62, 16),
                                     (x0 + 76, hy - 78, 20)]):
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 88, 84))
    # explosion: orange flames + black smoke above the bow
    ex, ey = x0 + 210, hy - 6
    draw.polygon([(ex - 46, ey), (ex - 20, ey - 58), (ex, ey - 26),
                  (ex + 22, ey - 64), (ex + 48, ey)],
                 fill=(232, 120, 30))
    draw.polygon([(ex - 26, ey), (ex - 8, ey - 34), (ex + 8, ey - 12),
                  (ex + 26, ey - 38), (ex + 30, ey)],
                 fill=(245, 190, 60))
    draw.ellipse([ex - 52, ey - 84, ex - 16, ey - 48], fill=(60, 58, 54))
    draw.ellipse([ex + 8, ey - 92, ex + 48, ey - 52], fill=(80, 78, 74))
    # sea mines: spiked circles
    for mx, my in [(x0 + 96, y1 - 22), (x1 - 78, y1 - 16)]:
        draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], fill=INK)
        for ang in range(0, 360, 45):
            import math
            dx = int(13 * math.cos(math.radians(ang)))
            dy = int(13 * math.sin(math.radians(ang)))
            draw.line([(mx, my), (mx + dx, my + dy)], fill=INK, width=2)
    # waves
    for wx in range(x0 + 6, x1 - 10, 26):
        draw.arc([wx, y1 - 12, wx + 24, y1 + 2], 180, 360,
                 fill=(200, 215, 230), width=2)
    # caption
    draw.text((x0 + 4, y1 - 2), "A tanker burns in the Strait of Hormuz.",
              font=font(SANS, 12), fill=GREY)


TILES = [
    ("UKRAINE STRIKES", "refinery",
     "Ukraine hits Russian refineries and air base",
     "Ukraine says its drones struck two Rosneft refineries in Samara — "
     "Syzran and Kuibyshev — both on fire; one person killed. Kyiv also "
     "claims 3 MiG-31s and 2 Su-34s damaged at Savasleyka."),
    ("THE TOLL", "chart",
     "Leak: nearly 500,000 Russian soldiers killed",
     "Leaked Rosstat data analysed by the BBC put Russian military deaths "
     "since 2022 at at least 490,334. Mediazona estimates the true figure "
     "could be near 700,000. The Kremlin declined to comment."),
    ("THE GULF", "flame",
     "Houthis claim strike on Saudi refinery",
     "Yemen's Houthis claim they hit the Ras Tanura refinery. Saudi "
     "Arabia says air defences destroyed four drones above it, with no "
     "early casualties. A day earlier, a Houthi drone attack in Riyadh "
     "injured 11."),
    ("GAZA", "building",
     "Israel kills Hamas security chief in Gaza",
     "An Israeli strike on Shati refugee camp killed Hamas's head of "
     "internal security for northern Gaza, with his wife and two "
     "daughters, Gaza's Hamas-run ministry and medics say."),
    ("MARKETS", "market",
     "Asia shares plunge; Dow tops 50,000",
     "South Korea's KOSPI fell 6.16%; Japan's Nikkei fell 2.78%. On Wall "
     "Street, the Nasdaq fell 1.5% and the S&P 500 0.5%, while the Dow "
     "rose 0.9% to 50,018.70 — its first close above 50,000."),
    ("TECH", "gavel",
     "Huawei found guilty in US trial",
     "A Brooklyn federal jury found China's Huawei guilty on 10 of 12 "
     "counts, including conspiracy to steal trade secrets and bank fraud, "
     "after a trial of more than two months. It was cleared of "
     "racketeering."),
    ("SPACE", "rocket",
     "China flies Pakistan's first astronaut",
     "Shenzhou-24 docked at China's Tiangong space station carrying "
     "Muhammad Zeeshan Ali, Pakistan's first astronaut, with two Chinese "
     "crew. A historic first for Pakistan's space programme."),
    ("THE PACIFIC", "flags",
     "Australia–Solomon Islands security pact",
     "Australia and Solomon Islands signed a pact in Canberra barring any "
     "foreign military or security base in Solomon Islands — a major "
     "Canberra move in the Pacific."),
    ("CLIMATE", "globe",
     "Pope dismayed as COP31 ends without deal",
     "Pope Leo XIV voiced concern that the COP31 climate talks failed to "
     "reach an agreement, saying extreme weather events linked to the "
     "climate crisis are \"increasingly frequent\"."),
]

WIRE = [
    ("SUDAN", "RSF drone strikes killed 19 civilians and injured 20 in two cities, Emergency Lawyers say."),
    ("COLOMBIA", "Security forces stormed an Éxito supermarket in Cartagena, freeing all hostages; one kidnapper killed."),
    ("POLAND", "To set up a no-fly zone on the Ukraine border after Russian drones entered its airspace; seeks a permanent US military presence."),
    ("EGYPT", "A fuel tanker crash sparked a huge fire on a road near Cairo; at least 31 killed."),
    ("UNITED STATES", "Trump proposed new tariffs on 14 trading partners (20–40%); hearing set for 25 January."),
    ("NEW YORK", "The 100th Macy's Thanksgiving Parade is delayed to Saturday as a major storm is forecast."),
    ("DELL", "Record Q3 revenue of $54.9 billion (+103%); AI servers $22.0 billion (+291%)."),
    ("DYMER", "The death toll rose to 12, RTE reports."),
    ("UKRAINE", "Trump ruled out US troops and bases in post-war Ukraine, sources say."),
]


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin
    X1 = W - M

    # ---------- Masthead ----------
    title = "The Day in the World"
    tf = font(SERIF_B, 62)
    tw = d.textlength(title, font=tf)
    d.text(((W - tw) / 2, 18), title, font=tf, fill=INK)
    date = "WEDNESDAY, 25 NOVEMBER 2026"
    df = font(SANS_B, 20)
    dw = d.textlength(date, font=df)
    d.text(((W - dw) / 2, 92), date, font=df, fill=RED)
    hline(d, M, X1, 122, 3)
    hline(d, M, X1, 128, 1)

    # ---------- Lead ----------
    ly = 142
    lead_head = "TANKERS HIT BY MINES\nIN THE STRAIT OF HORMUZ"
    hf = font(SERIF_B, 33)
    for ln in lead_head.split("\n"):
        d.text((M, ly), ln, font=hf, fill=INK)
        ly += 40
    ly += 4
    ly = para(d, M, ly,
              "Iran says two oil tankers struck sea mines and caught fire "
              "in the Strait of Hormuz after trying to use an unauthorised "
              "route. UKMTO reported three vessels attacked near Hormuz, "
              "and the US is investigating a possible Iranian link to the "
              "hacking of up to 50 merchant ships.",
              font(SERIF, 16), 590, leading=1.3)
    draw_lead_art(d, 648, 142, X1, 322)
    hline(d, M, X1, 340, 2)

    # ---------- Section header ----------
    d.text((M, 352), "AROUND THE WORLD",
           font=font(SANS_B, 17), fill=RED)
    hline(d, M, X1, 378, 1)

    # ---------- Tile grid: 3 columns x 3 rows ----------
    cols, rows = 3, 3
    gap = 14
    tw_ = (X1 - M - (cols - 1) * gap) // cols
    th = 150
    gy = 390
    for i, (kicker, kind, head, body) in enumerate(TILES):
        r, c = divmod(i, cols)
        x0 = M + c * (tw_ + gap)
        y0 = gy + r * (th + 12)
        d.rectangle([x0, y0, x0 + tw_, y0 + th], outline=(190, 186, 176),
                    width=1)
        icon(d, kind, x0 + 10, y0 + 10, 40)
        d.text((x0 + 58, y0 + 12), kicker, font=font(SANS_B, 12), fill=RED)
        y = para(d, x0 + 10, y0 + 54, head, font(SERIF_B, 15), tw_ - 20,
                 leading=1.12)
        para(d, x0 + 10, y + 2, body, font(SERIF, 11), tw_ - 20,
             leading=1.25, max_lines=4)

    # ---------- Wire strip ----------
    wy = gy + rows * (th + 12) + 6
    hline(d, M, X1, wy, 2)
    d.text((M, wy + 8), "THE WIRE", font=font(SANS_B, 15), fill=RED)
    wy += 34
    col_w = (X1 - M - 2 * 20) // 3
    for i, (place, text) in enumerate(WIRE):
        c = i % 3
        r = i // 3
        x0 = M + c * (col_w + 20)
        y0 = wy + r * 30
        d.text((x0, y0), place + " — ", font=font(SANS_B, 12), fill=INK)
        pw = d.textlength(place + " — ", font=font(SANS_B, 12))
        lines = wrap(d, text, font(SANS, 12), col_w - pw)
        yy = y0
        for j, ln in enumerate(lines[:2]):
            xx = x0 + (pw if j == 0 else 0)
            d.text((xx, yy), ln, font=font(SANS, 12), fill=INK)
            yy += 15

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
