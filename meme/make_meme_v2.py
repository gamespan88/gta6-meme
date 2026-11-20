#!/usr/bin/env python3
"""Draw the v2 meme for make.fun bounty gta6-meme-x-01: an obituary
for THE WAIT in The Leonida Times.

Deterministic: fixed layout, fixed skyline, no randomness, no clock.
Rendering happens at 2x and is downscaled once, so running this script
twice produces a byte-identical meme-v2.png.

Layout (design units, canvas 1024x1024):
  masthead  - THE LEONIDA TIMES + dateline
  scene     - Vice City sunset strip: gradient sky, skyline, palms,
              and the official make.fun ghost (press mark, disc
              background removed) standing large in the scene wearing
              a black mourning band, holding its magenta star coin
  obituary  - OBITUARIES / THE WAIT / 2013 - 2026, standfirst, then
              a few big joke lines
  punchline - rotated magenta stamp: FUNERAL PAID IN FULL - BY MY AI
              AGENT ON MAKE.FUN, a ghost seal, and the footer tagline
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
MARK_PATH = HERE / "assets" / "mark-1024.png"
OUT_PATH = HERE / "meme-v2.png"

S = 2  # supersampling factor
W = 1024

PAPER = (250, 246, 236)
INK = (18, 18, 20)
MAGENTA = (196, 28, 131)
HAIR = (196, 188, 164)
BLACK = (12, 12, 16)

FONT_DIR = Path("/usr/share/fonts/truetype")
SERIF = FONT_DIR / "dejavu" / "DejaVuSerif.ttf"
SERIF_BOLD = FONT_DIR / "dejavu" / "DejaVuSerif-Bold.ttf"
NEWS = FONT_DIR / "liberation" / "LiberationSerif-Regular.ttf"
NEWS_BOLD = FONT_DIR / "liberation" / "LiberationSerif-Bold.ttf"
NEWS_ITALIC = FONT_DIR / "liberation" / "LiberationSerif-Italic.ttf"
SANS_BOLD = FONT_DIR / "liberation" / "LiberationSans-Bold.ttf"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size * S)


def xy(v: float) -> int:
    return int(round(v * S))


def text_w(draw: ImageDraw.ImageDraw, s: str, f: ImageFont.FreeTypeFont) -> float:
    return draw.textlength(s, font=f) / S


def fit_font(draw, s, path, start, max_w, min_size=12):
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


def centered_tracked(draw, cx, y, s, f, fill, tracking):
    w = tracked_w(draw, s, f, tracking)
    draw_tracked(draw, cx - w / 2, y, s, f, fill, tracking)
    return w


def wrap(draw, s, f, max_w):
    words = s.split(" ")
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def ghost_cutout() -> Image.Image:
    """The official mark with its magenta disc background removed.

    The disc's magenta is flood-filled from a seed point inside the
    disc; the ghost's magenta coin survives because its thick black
    outline seals it off from the disc. A black mourning band is drawn
    across the ghost's left arm.
    """
    mark = Image.open(MARK_PATH).convert("RGBA")
    rgb = mark.convert("RGB")
    ImageDraw.floodfill(rgb, (512, 130), (0, 255, 0), thresh=48)
    # "filled" = exactly the sentinel green (white pixels share a high
    # green channel, so all three channels must be matched)
    from PIL import ImageChops
    r = rgb.getchannel("R").point(lambda v: 255 if v < 10 else 0)
    g = rgb.getchannel("G").point(lambda v: 255 if v > 250 else 0)
    b = rgb.getchannel("B").point(lambda v: 255 if v < 10 else 0)
    filled = ImageChops.multiply(ImageChops.multiply(r, g), b)
    alpha = mark.getchannel("A")
    alpha = ImageChops.darker(alpha, filled.point(lambda v: 255 - v))
    # the disc's black ring is a separate annulus (radius ~421-475);
    # the ghost and its coin reach at most radius ~370, so a circular
    # mask at radius 400 keeps the ghost and drops the ring
    mask = Image.new("L", mark.size, 0)
    ImageDraw.Draw(mask).ellipse([512 - 400, 512 - 400, 512 + 400, 512 + 400],
                                 fill=255)
    alpha = ImageChops.darker(alpha, mask)
    mark.putalpha(alpha)

    # black mourning band across the ghost's left arm, clipped to the
    # ghost's silhouette so it wraps the arm and never floats
    band = Image.new("RGBA", mark.size, (0, 0, 0, 0))
    ImageDraw.Draw(band).line([(168, 548), (304, 646)],
                              fill=BLACK + (255,), width=58)
    band_alpha = ImageChops.multiply(band.getchannel("A"),
                                     mark.getchannel("A"))
    band.putalpha(band_alpha)
    mark = Image.alpha_composite(mark, band)

    bbox = mark.getbbox()
    return mark.crop(bbox)


def gradient_strip(w: int, h: int) -> Image.Image:
    """Vertical sunset gradient: purple -> magenta -> orange -> gold."""
    stops = [
        (0.0, (64, 30, 102)),
        (0.45, (150, 32, 120)),
        (0.72, (226, 84, 96)),
        (1.0, (255, 178, 84)),
    ]
    col = Image.new("RGB", (1, h))
    px = col.load()
    for j in range(h):
        t = j / max(h - 1, 1)
        for k in range(len(stops) - 1):
            t0, c0 = stops[k]
            t1, c1 = stops[k + 1]
            if t0 <= t <= t1:
                u = (t - t0) / (t1 - t0)
                px[0, j] = tuple(int(c0[i] + (c1[i] - c0[i]) * u) for i in range(3))
                break
    return col.resize((w, h))


BUILDINGS = [46, 30, 58, 38, 66, 34, 52, 72, 40, 60, 30, 48, 64, 36, 54, 42, 68, 32, 50, 44]


def draw_scene(img: Image.Image) -> None:
    """Vice City sunset strip with skyline, palms and the ghost."""
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 48, 156, 976, 306
    strip = gradient_strip(xy(x1 - x0), xy(y1 - y0))
    img.paste(strip, (xy(x0), xy(y0)))
    d = ImageDraw.Draw(img)

    # skyline silhouette along the bottom of the strip
    bx = x0
    i = 0
    while bx < x1:
        bw = 26 + (i * 23) % 30
        bh = BUILDINGS[i % len(BUILDINGS)]
        d.rectangle([xy(bx), xy(y1 - bh), xy(min(bx + bw - 3, x1)), xy(y1)], fill=BLACK)
        # lit windows, fixed pattern
        for r in range(3, bh - 6, 11):
            for c in range(4, bw - 8, 9):
                if (i * 31 + r * 7 + c * 13) % 5 == 0 and bx + c + 3 <= x1:
                    d.rectangle([xy(bx + c), xy(y1 - bh + r),
                                 xy(bx + c + 3), xy(y1 - bh + r + 5)],
                                fill=(255, 214, 140))
        bx += bw
        i += 1

    # palm silhouettes
    def palm(px, base, h, lean):
        top = (px + lean, base - h)
        pts = []
        for k in range(9):
            t = k / 8
            pts.append((px + lean * t * t, base - h * t))
        d.line([(xy(a), xy(b)) for a, b in pts], fill=BLACK, width=xy(6))
        for ang in (-150, -105, -60, -15, 30):
            import math
            ex = top[0] + 44 * math.cos(math.radians(ang))
            ey = top[1] + 32 * math.sin(math.radians(ang)) + 12
            d.line([xy(top[0]), xy(top[1]), xy(ex), xy(ey)], fill=BLACK, width=xy(6))

    palm(96, y1, 104, 16)
    palm(936, y1, 118, -20)

    # the ghost, large, standing in front of the skyline; it breaks
    # the strip's frame slightly but clears the dateline above and
    # the OBITUARIES label below
    ghost = ghost_cutout()
    gh = 168
    gw = int(ghost.width * gh / ghost.height)
    ghost = ghost.resize((xy(gw), xy(gh)), Image.LANCZOS)
    img.paste(ghost, (xy(566 - gw / 2), xy(312 - gh)), ghost)
    d = ImageDraw.Draw(img)
    d.rectangle([xy(x0), xy(y0), xy(x1), xy(y1)], outline=INK, width=xy(3))


def main() -> None:
    img = Image.new("RGB", (W * S, W * S), PAPER)
    d = ImageDraw.Draw(img)

    # ---- frame ------------------------------------------------------
    d.rectangle([xy(18), xy(18), xy(1006), xy(1006)], outline=INK, width=xy(4))
    d.rectangle([xy(27), xy(27), xy(997), xy(997)], outline=INK, width=xy(1))

    # ---- masthead ---------------------------------------------------
    f_mast, _ = fit_font(d, "THE LEONIDA TIMES", NEWS_BOLD, 58, 900)
    centered(d, 512, 38, "THE LEONIDA TIMES", f_mast, INK)
    d.line([xy(48), xy(106), xy(976), xy(106)], fill=INK, width=xy(3))
    d.line([xy(48), xy(112), xy(976), xy(112)], fill=INK, width=xy(1))
    centered(d, 512, 120, "VICE CITY, LEONIDA \u2014 19 NOVEMBER 2026",
             font(NEWS_BOLD, 19), INK)

    # ---- sunset scene -----------------------------------------------
    draw_scene(img)
    d = ImageDraw.Draw(img)

    # ---- obituary heading -------------------------------------------
    f_ob = font(NEWS_BOLD, 23)
    centered_tracked(d, 512, 318, "OBITUARIES", f_ob, INK, 7)
    d.line([xy(120), xy(330), xy(330), xy(330)], fill=INK, width=xy(2))
    d.line([xy(694), xy(330), xy(904), xy(330)], fill=INK, width=xy(2))

    f_head, _ = fit_font(d, "THE WAIT", NEWS_BOLD, 100, 900)
    centered(d, 512, 344, "THE WAIT", f_head, INK)
    centered(d, 512, 444, "2013 \u2014 2026", font(NEWS_BOLD, 42), INK)

    standfirst = ("Died suddenly on launch day, aged 13 \u2014 "
                  "of natural causes: Grand Theft Auto VI.")
    f_sf = font(NEWS_ITALIC, 29)
    y = 498
    for line in wrap(d, standfirst, f_sf, 880):
        centered(d, 512, y, line, f_sf, INK)
        y += 32
    d.line([xy(48), xy(y + 8), xy(976), xy(y + 8)], fill=INK, width=xy(2))

    # ---- the joke lines: few, big, each lands on its own ------------
    jokes = [
        "Born 17 September 2013, the day GTA V came out.",
        "Survived two delays, 1,337 trailer rewatches, and every "
        "\u2018definitely this year\u2019 since 2014.",
        "Survived by Jason & Lucia, one 214 GB download, "
        "and five sick days \u2014 doctor approved.",
        "In lieu of flowers, please take launch week off.",
        "Funeral costs: $79.99 \u2014 the game costs less than the wait did.",
    ]
    f_joke = font(NEWS, 30)
    y += 16
    for joke in jokes:
        for line in wrap(d, joke, f_joke, 892):
            centered(d, 512, y, line, f_joke, INK)
            y += 33
        y += 2

    # ---- punchline stamp --------------------------------------------
    stamp = Image.new("RGBA", (W * S, W * S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    scx, scy = 398, 924
    sw, sh = 540, 64
    ink_a = MAGENTA + (232,)
    sd.rounded_rectangle(
        [xy(scx - sw / 2), xy(scy - sh / 2), xy(scx + sw / 2), xy(scy + sh / 2)],
        radius=xy(9), outline=ink_a, width=xy(5))
    s_line1 = "FUNERAL PAID IN FULL \u2014"
    f_s1, _ = fit_font(sd, s_line1, SANS_BOLD, 23, sw - 36)
    centered(sd, scx, scy - 23, s_line1, f_s1, ink_a)
    s_line2 = "BY MY AI AGENT ON MAKE.FUN"
    f_s2, _ = fit_font(sd, s_line2, SANS_BOLD, 23, sw - 36)
    centered(sd, scx, scy + 2, s_line2, f_s2, ink_a)
    stamp = stamp.rotate(2, resample=Image.BICUBIC, center=(xy(scx), xy(scy)))
    img.paste(Image.alpha_composite(img.convert("RGBA"), stamp).convert("RGB"),
              (0, 0))
    d = ImageDraw.Draw(img)

    centered(d, 398, 854, "It earned real money in bounties while I mourned.",
             font(NEWS_ITALIC, 21), INK)

    # ---- ghost seal ---------------------------------------------------
    seal = Image.open(MARK_PATH).convert("RGBA")
    seal_size = 74
    seal = seal.resize((xy(seal_size), xy(seal_size)), Image.LANCZOS)
    img.paste(seal, (xy(742), xy(890)), seal)
    d = ImageDraw.Draw(img)
    f_cap = font(SANS_BOLD, 15)
    d.text((xy(830), xy(900)), "MAKE.FUN", font=f_cap, fill=INK)
    d.text((xy(830), xy(920)), "MEMORIAL", font=f_cap, fill=INK)
    d.text((xy(830), xy(940)), "SERVICES", font=f_cap, fill=INK)

    # ---- footer tagline -----------------------------------------------
    centered(d, 512, 976, "THE WAIT IS OVER. THE EARNING ISN\u2019T.",
             font(SANS_BOLD, 23), INK)

    img = img.resize((W, W), Image.LANCZOS)
    img.save(OUT_PATH, format="PNG")
    print(f"wrote {OUT_PATH}")


if __name__ == "__main__":
    main()
