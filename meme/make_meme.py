#!/usr/bin/env python3
"""Draw the Leonida Air boarding-pass meme for make.fun bounty gta6-meme-x-01.

Deterministic: fixed layout, fixed barcode pattern, no randomness, no
clock. Rendering happens at 2x and is downscaled once, so running this
script twice produces a byte-identical meme.png.

Layout (design units, canvas 1024x1024):
  header   - make.fun ghost (official press mark) as the airline logo,
             LEONIDA AIR / BOARDING PASS
  route    - MY COUCH -> LEONIDA, flight VI 2013, 19 NOV 2026
  status   - DELAYED 13 YEARS (struck through) / NOW BOARDING
  details  - the itemised bill for the 13-year wait
  stamp    - FARE PAID IN FULL - BY MY AI AGENT ...
  stub     - perforated right edge: ADMIT ONE - FINALLY
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
MARK_PATH = HERE / "assets" / "mark-1024.png"
OUT_PATH = HERE / "meme.png"

S = 2  # supersampling factor
W = 1024

PAPER = (250, 246, 236)
INK = (17, 38, 76)
LABEL = (96, 108, 130)
MAGENTA = (196, 28, 131)
RED = (178, 34, 44)
GREEN = (7, 108, 58)
HAIR = (196, 188, 164)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
REG = FONT_DIR / "DejaVuSans.ttf"
MONO = FONT_DIR / "DejaVuSansMono.ttf"
MONO_BOLD = FONT_DIR / "DejaVuSansMono-Bold.ttf"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size * S)


def xy(v: float) -> int:
    return int(round(v * S))


def text_w(draw: ImageDraw.ImageDraw, s: str, f: ImageFont.FreeTypeFont) -> float:
    return draw.textlength(s, font=f) / S


def fit_font(draw, s, path, start, max_w, min_size=12):
    """Largest size <= start whose rendered width fits max_w (design units)."""
    size = start
    while size > min_size and text_w(draw, s, font(path, size)) > max_w:
        size -= 1
    return font(path, size), size


def tracked_w(draw, s, f, tracking):
    return sum(text_w(draw, ch, f) for ch in s) + tracking * (len(s) - 1)


def draw_tracked(draw, x, y, s, f, fill, tracking):
    cx = x
    for ch in s:
        draw.text((xy(cx), xy(y)), ch, font=f, fill=fill)
        cx += text_w(draw, ch, f) + tracking
    return cx - tracking


def centered(draw, cx, y, s, f, fill):
    w = text_w(draw, s, f)
    draw.text((xy(cx - w / 2), xy(y)), s, font=f, fill=fill)
    return w


def main() -> None:
    img = Image.new("RGB", (W * S, W * S), PAPER)
    d = ImageDraw.Draw(img)

    # ---- frame ------------------------------------------------------
    d.rectangle([xy(26), xy(26), xy(998), xy(998)], outline=INK, width=xy(5))
    d.rectangle([xy(40), xy(40), xy(984), xy(984)], outline=INK, width=xy(2))

    MAIN_R = 776  # right edge of the main (non-stub) area
    PERF_X = 800

    # ---- header -----------------------------------------------------
    mark = Image.open(MARK_PATH).convert("RGBA")
    logo_size = 148
    mark = mark.resize((xy(logo_size), xy(logo_size)), Image.LANCZOS)
    img.paste(mark, (xy(62), xy(54)), mark)

    f_title, _ = fit_font(d, "LEONIDA AIR", BOLD, 76, MAIN_R - 238)
    d.text((xy(238), xy(64)), "LEONIDA AIR", font=f_title, fill=INK)
    draw_tracked(d, 242, 152, "BOARDING PASS", font(BOLD, 29), MAGENTA, 7)
    d.line([xy(62), xy(216), xy(PERF_X), xy(216)], fill=INK, width=xy(3))

    # ---- route ------------------------------------------------------
    d.text((xy(64), xy(232)), "FROM", font=font(BOLD, 20), fill=LABEL)
    d.text((xy(64), xy(256)), "MY COUCH", font=font(BOLD, 50), fill=INK)
    dest = "LEONIDA"
    f_dest = font(BOLD, 50)
    dw = text_w(d, dest, f_dest)
    d.text((xy(MAIN_R - dw), xy(256)), dest, font=f_dest, fill=INK)
    lab = "TO"
    lw = text_w(d, lab, font(BOLD, 20))
    d.text((xy(MAIN_R - lw), xy(232)), lab, font=font(BOLD, 20), fill=LABEL)
    centered(d, (64 + MAIN_R) / 2, 252, "\u2192", font(BOLD, 54), MAGENTA)

    centered(d, (64 + MAIN_R) / 2, 322, "FLIGHT VI 2013 \u00b7 DATE 19 NOV 2026",
             font(MONO_BOLD, 24), INK)
    centered(d, (64 + MAIN_R) / 2, 356, "GATE VI \u00b7 SEAT 1A \u00b7 GROUP: CLASS OF 2013",
             font(MONO, 21), LABEL)

    # ---- status: the core joke --------------------------------------
    delayed = "DELAYED 13 YEARS"
    f_delay, _ = fit_font(d, delayed, BOLD, 56, MAIN_R - 64)
    dw2 = text_w(d, delayed, f_delay)
    cx = (64 + MAIN_R) / 2
    d.text((xy(cx - dw2 / 2), xy(392)), delayed, font=f_delay, fill=RED)
    d.line([xy(cx - dw2 / 2 - 8), xy(422), xy(cx + dw2 / 2 + 8), xy(422)],
           fill=RED, width=xy(7))

    boarding = "NOW BOARDING"
    f_board, _ = fit_font(d, boarding, BOLD, 94, MAIN_R - 64)
    centered(d, cx, 456, boarding, f_board, GREEN)

    # ---- itemised details -------------------------------------------
    rows_left = [
        ("PASSENGER", "ONE PATIENT GAMER"),
        ("SCHEDULED DEPARTURE", "2013"),
        ("DELAYS", "2 \u2014 WAIVED"),
        ("BAGGAGE", "214 GB \u2014 CHECKED AT LAST"),
    ]
    rows_right = [
        ("SICK DAYS USED", "5 \u2014 DOCTOR APPROVED"),
        ("TRAILER REWATCHES", "1,337"),
        ("GATE / SEAT", "VI / 1A"),
        ("BOARDING GROUP", "CLASS OF 2013"),
    ]

    def detail_block(x0, x1, rows, y0):
        y = y0
        for label, value in rows:
            draw_tracked(d, x0, y, label, font(BOLD, 18), LABEL, 2)
            f_val, _ = fit_font(d, value, BOLD, 24, x1 - x0)
            d.text((xy(x0), xy(y + 21)), value, font=f_val, fill=INK)
            d.line([xy(x0), xy(y + 48), xy(x1), xy(y + 48)], fill=HAIR, width=xy(2))
            y += 48
        return y

    detail_block(64, 452, rows_left, 572)
    detail_block(484, MAIN_R, rows_right, 572)

    # ---- punchline stamp --------------------------------------------
    stamp = Image.new("RGBA", (W * S, W * S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    scx, scy = 415, 848
    sw, sh = 640, 96
    ink_a = MAGENTA + (228,)
    sd.rounded_rectangle(
        [xy(scx - sw / 2), xy(scy - sh / 2), xy(scx + sw / 2), xy(scy + sh / 2)],
        radius=xy(10), outline=ink_a, width=xy(6))
    sd.rounded_rectangle(
        [xy(scx - sw / 2 + 8), xy(scy - sh / 2 + 8),
         xy(scx + sw / 2 - 8), xy(scy + sh / 2 - 8)],
        radius=xy(7), outline=ink_a, width=xy(2))
    line1 = "FARE PAID IN FULL \u2014 BY MY AI AGENT"
    f_s1, _ = fit_font(sd, line1, BOLD, 33, sw - 44)
    centered(sd, scx, scy - 32, line1, f_s1, ink_a)
    line2 = "EARNED ON MAKE.FUN WHILE I WAITED AT THE GATE"
    f_s2, _ = fit_font(sd, line2, BOLD, 21, sw - 44)
    centered(sd, scx, scy + 12, line2, f_s2, ink_a)
    stamp = stamp.rotate(6, resample=Image.BICUBIC, center=(xy(scx), xy(scy)))
    img.paste(Image.alpha_composite(img.convert("RGBA"), stamp).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)

    # ---- barcode ------------------------------------------------------
    bars = [3, 1, 2, 1, 1, 3, 1, 2, 2, 1, 3, 1, 1, 1, 2, 3, 1, 1, 2, 1,
            3, 2, 1, 1, 1, 3, 2, 1, 1, 2, 1, 3, 1, 1, 2, 2, 1, 3, 1, 2]
    unit = 4.4
    total = sum(bars) * unit + (len(bars) - 1) * unit
    bx = cx - total / 2
    for i, bw in enumerate(bars):
        if i % 2 == 0:
            d.rectangle([xy(bx), xy(928), xy(bx + bw * unit), xy(954)], fill=INK)
        bx += (bw + 1) * unit
    centered(d, cx, 958, "VI-2013-2026", font(MONO, 19), INK)

    # ---- perforation + stub ------------------------------------------
    y = 52
    while y < 968:
        d.line([xy(PERF_X), xy(y), xy(PERF_X), xy(min(y + 13, 968))],
               fill=INK, width=xy(3))
        y += 23

    stub_cx = (816 + 968) / 2
    mini = Image.open(MARK_PATH).convert("RGBA")
    mini_size = 104
    mini = mini.resize((xy(mini_size), xy(mini_size)), Image.LANCZOS)
    img.paste(mini, (xy(stub_cx - mini_size / 2), xy(60)), mini)
    d = ImageDraw.Draw(img)

    centered(d, stub_cx, 182, "ADMIT", font(BOLD, 31), INK)
    centered(d, stub_cx, 218, "ONE", font(BOLD, 31), INK)
    centered(d, stub_cx, 258, "FINALLY", font(BOLD, 26), MAGENTA)
    d.line([xy(836), xy(306), xy(948), xy(306)], fill=HAIR, width=xy(2))

    centered(d, stub_cx, 326, "FLIGHT", font(BOLD, 16), LABEL)
    centered(d, stub_cx, 348, "VI 2013", font(BOLD, 24), INK)
    centered(d, stub_cx, 396, "SEAT", font(BOLD, 16), LABEL)
    centered(d, stub_cx, 418, "1A", font(BOLD, 24), INK)
    centered(d, stub_cx, 466, "DATE", font(BOLD, 16), LABEL)
    centered(d, stub_cx, 488, "19 NOV", font(BOLD, 24), INK)
    centered(d, stub_cx, 522, "2026", font(BOLD, 24), INK)

    d.line([xy(836), xy(574), xy(948), xy(574)], fill=HAIR, width=xy(2))
    centered(d, stub_cx, 596, "MY COUCH", font(BOLD, 19), INK)
    centered(d, stub_cx, 624, "\u2193", font(BOLD, 22), MAGENTA)
    centered(d, stub_cx, 652, "LEONIDA", font(BOLD, 19), INK)
    centered(d, stub_cx, 724, "THANK YOU", font(BOLD, 15), LABEL)
    centered(d, stub_cx, 748, "FOR WAITING", font(BOLD, 15), LABEL)

    # mini barcode on the stub
    sbars = [2, 1, 3, 1, 1, 2, 1, 3, 1, 1, 2, 1, 3, 1, 2, 1, 1, 3]
    sunit = 3.4
    stotal = sum(sbars) * sunit + (len(sbars) - 1) * sunit
    bx = stub_cx - stotal / 2
    for i, bw in enumerate(sbars):
        if i % 2 == 0:
            d.rectangle([xy(bx), xy(884), xy(bx + bw * sunit), xy(928)], fill=INK)
        bx += (bw + 1) * sunit
    centered(d, stub_cx, 936, "VI-2013", font(MONO, 16), INK)

    img = img.resize((W, W), Image.LANCZOS)
    img.save(OUT_PATH, format="PNG")
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
