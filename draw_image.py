"""Draw the 20 November 2026 world-news image.

Run once, locally, to produce entry.png (1024x1024, PNG):
    python3 draw_image.py

The entry program itself is main.py, which only copies entry.png
to the output directory using the standard library, so the graded
run needs no network and no third-party package. This script is
kept in the repo so anyone can see exactly how the image was made
and re-draw it byte-for-byte: same inputs, same fonts, same layout,
no clock, no randomness, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 232)
NAVY = (15, 42, 68)
NAVY_LIGHT = (27, 68, 102)
RED = (178, 34, 34)
DARK = (24, 24, 24)
GREY = (90, 90, 90)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)
TEAL = (0, 128, 128)
GREEN = (34, 120, 60)
ORANGE = (200, 100, 0)
PURPLE = (90, 60, 140)


def font(name, size):
    paths = [
        f"/usr/share/fonts/truetype/dejavu/{name}.ttf",
        f"/usr/share/fonts/truetype/liberation/{name}.ttf",
    ]
    for path in paths:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


BOLD = lambda s: font("DejaVuSans-Bold", s)
REG = lambda s: font("DejaVuSans", s)
SERIF_BOLD = lambda s: font("DejaVuSerif-Bold", s)


def wrap(draw, text, fnt, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_width, leading=6):
    """Draw wrapped text, return the y just below it."""
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def flag_us(draw, x, y, w, h):
    for i in range(7):
        draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                       fill=(178, 34, 52) if i % 2 == 0 else WHITE)
    draw.rectangle([x, y, x + w * 0.4, y + h * 4 / 7], fill=NAVY)
    for r in range(3):
        for c in range(4):
            cx = x + 12 + c * 22
            cy = y + 10 + r * 14
            draw.ellipse([cx, cy, cx + 6, cy + 6], fill=WHITE)


def flag_cn(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    for cx, cy, r in [(x + 20, y + 14, 8), (x + 42, y + 10, 4),
                      (x + 50, y + 22, 4), (x + 44, y + 34, 4)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 222, 0))


def flag_ru(draw, x, y, w, h):
    for i, colour in enumerate([WHITE, (0, 57, 166), (213, 0, 50)]):
        draw.rectangle([x, y + i * h / 3, x + w, y + (i + 1) * h / 3],
                       fill=colour)


def icon_scales(draw, cx, cy, colour):
    draw.line([cx, cy - 26, cx, cy + 26], fill=colour, width=5)
    draw.line([cx - 26, cy - 18, cx + 26, cy - 18], fill=colour, width=5)
    draw.line([cx - 26, cy - 18, cx - 34, cy + 6], fill=colour, width=4)
    draw.line([cx - 26, cy - 18, cx - 18, cy + 6], fill=colour, width=4)
    draw.line([cx + 26, cy - 18, cx + 18, cy + 6], fill=colour, width=4)
    draw.line([cx + 26, cy - 18, cx + 34, cy + 6], fill=colour, width=4)
    draw.arc([cx - 38, cy + 2, cx - 14, cy + 20], 0, 180, fill=colour, width=4)
    draw.arc([cx + 14, cy + 2, cx + 38, cy + 20], 0, 180, fill=colour, width=4)
    draw.line([cx - 22, cy + 26, cx + 22, cy + 26], fill=colour, width=5)


def icon_rocket(draw, cx, cy, colour):
    draw.polygon([(cx, cy - 30), (cx + 14, cy + 6), (cx, cy + 16),
                  (cx - 14, cy + 6)], fill=colour)
    draw.ellipse([cx - 8, cy - 12, cx + 8, cy + 4], fill=WHITE)
    draw.polygon([(cx - 14, cy + 6), (cx - 24, cy + 22), (cx - 8, cy + 14)],
                 fill=colour)
    draw.polygon([(cx + 14, cy + 6), (cx + 24, cy + 22), (cx + 8, cy + 14)],
                 fill=colour)
    draw.polygon([(cx - 6, cy + 16), (cx + 6, cy + 16), (cx, cy + 32)],
                 fill=(255, 170, 0))


def icon_chart_down(draw, cx, cy, colour):
    draw.line([cx - 30, cy + 26, cx + 30, cy + 26], fill=colour, width=4)
    draw.line([cx - 30, cy - 20, cx - 8, cy - 2, cx + 8, cy - 12,
               cx + 30, cy + 14], fill=colour, width=6)
    draw.polygon([(cx + 30, cy + 14), (cx + 14, cy + 12), (cx + 28, cy + 28)],
                 fill=colour)


def icon_drone(draw, cx, cy, colour):
    for dx, dy in [(-24, -18), (24, -18), (-24, 18), (24, 18)]:
        draw.ellipse([cx + dx - 9, cy + dy - 9, cx + dx + 9, cy + dy + 9],
                     outline=colour, width=4)
        draw.line([cx, cy, cx + dx, cy + dy], fill=colour, width=4)
    draw.rectangle([cx - 14, cy - 9, cx + 14, cy + 9], fill=colour)


def icon_leaf(draw, cx, cy, colour):
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], outline=colour,
                 width=5)
    draw.line([cx, cy - 26, cx, cy + 26], fill=colour, width=4)
    draw.arc([cx - 26, cy - 26, cx + 26, cy + 26], 300, 60, fill=colour,
             width=4)


def icon_tower(draw, cx, cy, colour):
    draw.polygon([(cx - 12, cy + 28), (cx - 6, cy - 28), (cx + 6, cy - 28),
                  (cx + 12, cy + 28)], fill=colour)
    draw.line([cx - 22, cy + 28, cx + 22, cy + 28], fill=colour, width=5)
    for wy in (-14, 0, 14):
        draw.rectangle([cx - 4, cy + wy, cx + 4, cy + wy + 6], fill=WHITE)


ICONS = {
    "scales": icon_scales,
    "rocket": icon_rocket,
    "chart": icon_chart_down,
    "drone": icon_drone,
    "leaf": icon_leaf,
    "tower": icon_tower,
}


def draw_card(draw, x, y, w, h, colour, kicker, title, body, icon):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=CARD,
                           outline=(210, 205, 190), width=2)
    draw.rounded_rectangle([x, y, x + w, y + 8], radius=4, fill=colour)
    draw.ellipse([x + 18, y + 26, x + 98, y + 106], outline=colour, width=3)
    ICONS[icon](draw, x + 58, y + 66, colour)
    tx = x + 116
    draw.text((tx, y + 16), kicker, font=BOLD(19), fill=colour)
    text_block(draw, tx, y + 42, title, BOLD(26), DARK, w - 132, leading=2)
    text_block(draw, tx, y + 104, body, REG(20), GREY, w - 132, leading=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Header band.
    draw.rectangle([0, 0, W, 148], fill=NAVY)
    draw.rectangle([0, 148, W, 154], fill=RED)
    draw.text((24, 14), "THE WORLD IN ONE IMAGE", font=BOLD(24),
              fill=(180, 210, 235))
    date = "FRIDAY  20  NOVEMBER  2026"
    draw.text((24, 44), date, font=SERIF_BOLD(52), fill=WHITE)
    draw.text((24, 108), "Six stories that defined the day, from Shenzhen to The Hague.",
              font=REG(25), fill=(200, 215, 230))

    # Lead story.
    lx, ly, lw, lh = 24, 170, 976, 240
    draw.rounded_rectangle([lx, ly, lx + lw, ly + lh], radius=12, fill=CARD,
                           outline=(210, 205, 190), width=2)
    draw.rectangle([lx, ly + 12, lx + 8, ly + lh - 12], fill=RED)
    draw.text((lx + 28, ly + 16), "LEAD STORY  •  SHENZHEN, CHINA",
              font=BOLD(22), fill=RED)
    text_block(draw, lx + 28, ly + 48,
               "Trump, Xi and Putin sign a 'Declaration toward Peace'",
               SERIF_BOLD(36), DARK, 920, leading=2)
    text_block(draw, lx + 28, ly + 132,
               "First-ever trilateral summit ends with a four-point pact: "
               "UN reform, energy cooperation, official immunity and "
               "nuclear-risk dialogue.",
               REG(23), GREY, 920, leading=3)

    # Flags row inside the lead card, bottom right.
    fy = ly + 188
    for i, (fn, label) in enumerate([(flag_us, "USA"), (flag_cn, "CHINA"),
                                     (flag_ru, "RUSSIA")]):
        fx = lx + 28 + i * 180
        fn(draw, fx, fy, 95, 44)
        draw.rectangle([fx, fy, fx + 95, fy + 44], outline=DARK, width=2)
        draw.text((fx + 103, fy + 10), label, font=BOLD(19), fill=DARK)
    draw.text((lx + 620, fy + 8), "Zelensky: no deal",
              font=BOLD(21), fill=NAVY)
    draw.text((lx + 620, fy + 34), "without Kyiv.",
              font=REG(20), fill=GREY)

    # Six-story grid.
    stories = [
        (NAVY, "JUSTICE  •  THE HAGUE", "ICJ: Myanmar committed genocide",
         "World Court rules 9-6: the 2017 crackdown was genocide.",
         "scales"),
        (GREEN, "MARKETS  •  NEW YORK", "Anthropic's IPO soars",
         "First frontier AI firm lists on Nasdaq (ANT); shares up 17% on debut.",
         "rocket"),
        (RED, "MARKETS  •  WORLD", "Stocks tumble on AI fears",
         "Dow below 50,000; S&P -2.0%, Nasdaq -2.3%; Asia plunges.",
         "chart"),
        (NAVY_LIGHT, "UKRAINE  •  KYIV", "UK sends 1,000+ drones",
         "GBP 260m package for Kyiv; Europe ready for talks with Russia.",
         "drone"),
        (TEAL, "CLIMATE  •  COP31", "COP31 drops fossil-fuel phase-out",
         "Draft deal drops the call; Africa seeks tripled climate finance.",
         "leaf"),
        (ORANGE, "MIDDLE EAST  •  RIYADH", "Houthi strike hits Riyadh tower",
         "Attack damages Saudi Arabia's tallest tower; Gaza strains ceasefire.",
         "tower"),
    ]
    gx, gy = 24, 426
    cw, ch, gap = 482, 170, 12
    for i, (colour, kicker, title, body, icon) in enumerate(stories):
        x = gx + (i % 2) * (cw + gap)
        y = gy + (i // 2) * (ch + gap)
        draw_card(draw, x, y, cw, ch, colour, kicker, title, body, icon)

    # Footer band.
    draw.rectangle([0, 968, W, H], fill=NAVY)
    draw.text((24, 982), "20 NOVEMBER 2026  •  SHENZHEN  •  THE HAGUE  •  NEW YORK  •  KYIV  •  RIYADH",
              font=BOLD(21), fill=WHITE)
    draw.text((24, 1010), "", font=REG(10), fill=WHITE)
    img.save(OUT, format="PNG", optimize=True)
    print(f"wrote {OUT} {W}x{H} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
