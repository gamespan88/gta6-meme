#!/usr/bin/env python3
"""Draw the v3 meme for make.fun bounty gta6-meme-x-01: a
CERTIFICATE OF LIVE BIRTH (State of Leonida) for Grand Theft Auto VI.

Same winning anatomy as the live board's top entries (an eviction
notice and a rental-car receipt): a mundane official document, the
13-year wait itemised as concrete fields - every line a joke - one
big red stamp as the one-second hook, and a hot-pink make.fun band
across the bottom where the official ghost announces that my AI
agent delivered it with real money it won in make.fun bounties.

Deterministic: fixed layout, no randomness, no clock. Rendering
happens at 2x and is downscaled once, so running this script twice
produces a byte-identical meme-v3.png. A 512px preview is exported
alongside it (the width the judge's dossier shows).
"""

from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
MARK_PATH = HERE / "assets" / "mark-1024.png"
OUT_PATH = HERE / "meme-v3.png"
PREVIEW_PATH = HERE / "meme-v3-preview.png"

S = 2  # supersampling factor
W = 1024
BAND_Y = 820  # pink band starts here (bottom ~20% of the canvas)

PAPER = (251, 247, 233)
INK = (22, 22, 26)
SOFT = (84, 80, 72)
MAGENTA = (196, 28, 131)
RED = (192, 30, 44)
GOLD = (176, 141, 60)
HAIR = (198, 190, 168)
WHITE = (255, 255, 255)
BLACK = (10, 10, 12)

FONT_DIR = Path("/usr/share/fonts/truetype")
SERIF = FONT_DIR / "liberation" / "LiberationSerif-Regular.ttf"
SERIF_BOLD = FONT_DIR / "liberation" / "LiberationSerif-Bold.ttf"
SERIF_ITALIC = FONT_DIR / "liberation" / "LiberationSerif-Italic.ttf"
SANS = FONT_DIR / "liberation" / "LiberationSans-Regular.ttf"
SANS_BOLD = FONT_DIR / "liberation" / "LiberationSans-Bold.ttf"
DEJAVU_BOLD = FONT_DIR / "dejavu" / "DejaVuSans-Bold.ttf"


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


def ghost_cutout() -> Image.Image:
    """The official mark with its magenta disc background removed.

    Same flood-fill trick as v2 (the ghost's magenta coin survives
    because its thick black outline seals it off from the disc), but
    no mourning band this time - the ghost is delivering, not burying.
    """
    mark = Image.open(MARK_PATH).convert("RGBA")
    rgb = mark.convert("RGB")
    ImageDraw.floodfill(rgb, (512, 130), (0, 255, 0), thresh=48)
    r = rgb.getchannel("R").point(lambda v: 255 if v < 10 else 0)
    g = rgb.getchannel("G").point(lambda v: 255 if v > 250 else 0)
    b = rgb.getchannel("B").point(lambda v: 255 if v < 10 else 0)
    filled = ImageChops.multiply(ImageChops.multiply(r, g), b)
    alpha = mark.getchannel("A")
    alpha = ImageChops.darker(alpha, filled.point(lambda v: 255 - v))
    mask = Image.new("L", mark.size, 0)
    ImageDraw.Draw(mask).ellipse([512 - 400, 512 - 400, 512 + 400, 512 + 400],
                                 fill=255)
    alpha = ImageChops.darker(alpha, mask)
    mark.putalpha(alpha)
    bbox = mark.getbbox()
    return mark.crop(bbox)


LX, RX = 64, 536          # left / right field columns
COLW = 424                # field column width


def field(draw, x, y, label, value, note=None, note_red=False):
    """One certificate field: small-caps label, big serif value,
    optional italic note underneath."""
    draw_tracked(draw, x, y, label, font(SANS_BOLD, 16), SOFT, 1.5)
    f_val, _ = fit_font(draw, value, SERIF_BOLD, 30, COLW)
    draw.text((xy(x), xy(y + 21)), value, font=f_val, fill=INK)
    if note:
        if note_red:
            draw_tracked(draw, x, y + 58, note, font(DEJAVU_BOLD, 15), RED, 1.5)
        else:
            draw.text((xy(x), xy(y + 57)), note,
                      font=font(SERIF_ITALIC, 19), fill=SOFT)


def hairline(draw, y):
    draw.line([xy(LX), xy(y), xy(960), xy(y)], fill=HAIR, width=xy(2))


def main() -> None:
    img = Image.new("RGB", (W * S, W * S), PAPER)
    d = ImageDraw.Draw(img)

    # ---- ornate certificate border ----------------------------------
    d.rectangle([xy(14), xy(14), xy(1010), xy(BAND_Y - 14)],
                outline=INK, width=xy(3))
    d.rectangle([xy(21), xy(21), xy(1003), xy(BAND_Y - 21)],
                outline=GOLD, width=xy(1))
    d.rectangle([xy(27), xy(27), xy(997), xy(BAND_Y - 27)],
                outline=INK, width=xy(1))
    for cx, cy in ((27, 27), (997, 27), (27, BAND_Y - 27), (997, BAND_Y - 27)):
        r = 7
        d.polygon([(xy(cx), xy(cy - r)), (xy(cx + r), xy(cy)),
                   (xy(cx), xy(cy + r)), (xy(cx - r), xy(cy))], fill=GOLD)

    # ---- header -------------------------------------------------------
    d.text((xy(48), xy(38)), "FORM VI-13", font=font(SANS_BOLD, 15), fill=SOFT)
    lw = text_w(d, "LEONIDA", font(SANS_BOLD, 15))
    d.text((xy(976 - lw), xy(38)), "LEONIDA", font=font(SANS_BOLD, 15), fill=SOFT)
    centered_tracked(d, 512, 46, "STATE OF LEONIDA \u00b7 DEPARTMENT OF VITAL RECORDS",
                     font(SANS_BOLD, 20), INK, 2)
    f_title, _ = fit_font(d, "CERTIFICATE OF LIVE BIRTH", SERIF_BOLD, 58, 900)
    centered(d, 512, 78, "CERTIFICATE OF LIVE BIRTH", f_title, INK)
    centered(d, 512, 142, "City of Vice City", font(SERIF_ITALIC, 23), SOFT)
    d.line([xy(120), xy(180), xy(488), xy(180)], fill=INK, width=xy(2))
    d.line([xy(536), xy(180), xy(904), xy(180)], fill=INK, width=xy(2))
    d.polygon([(xy(512), xy(173)), (xy(519), xy(180)), (xy(512), xy(187)),
               (xy(505), xy(180))], fill=INK)

    # ---- name of child --------------------------------------------------
    centered_tracked(d, 512, 196, "NAME OF CHILD", font(SANS_BOLD, 17), SOFT, 3)
    f_name, _ = fit_font(d, "GRAND THEFT AUTO VI", SERIF_BOLD, 62, 896)
    centered(d, 512, 220, "GRAND THEFT AUTO VI", f_name, INK)
    hairline(d, 296)

    # ---- field rows -------------------------------------------------------
    field(d, LX, 312, "DATE OF BIRTH", "19 NOVEMBER 2026")
    field(d, RX, 312, "TIME OF BIRTH", "AFTER 13 YEARS OF LABOR")
    hairline(d, 384)

    field(d, LX, 398, "GESTATION", "13 YEARS (4,748 DAYS)",
          note="\u2605 A WORLD RECORD", note_red=True)
    field(d, RX, 398, "WEIGHT \u00b7 LENGTH", "214 GB \u00b7 2 TRAILERS")
    hairline(d, 480)

    field(d, LX, 484, "MOTHER", "THE PLAYER'S PATIENCE",
          note="(EXHAUSTED, BUT ALIVE)")
    field(d, RX, 484, "FATHER", "A TRAILER",
          note="(APPEARED TWICE, THEN VANISHED)")
    hairline(d, 566)

    field(d, LX, 570, "ATTENDING PHYSICIANS", "DR. JASON & DR. LUCIA")
    field(d, RX, 570, "PLACE OF BIRTH", "LEONIDA GENERAL HOSPITAL",
          note="VICE CITY")
    hairline(d, 652)

    # ---- small print ------------------------------------------------------
    centered(d, 512, 658,
             "This child was announced three times before it was born.",
             font(SERIF_ITALIC, 19), SOFT)
    centered(d, 512, 682,
             "Older sibling (GTA V) has been respectfully asked to move out.",
             font(SERIF_ITALIC, 19), SOFT)

    # ---- the stamp: FINALLY -------------------------------------------------
    stamp = Image.new("RGBA", (W * S, W * S), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    scx, scy, sw, sh = 512, 764, 384, 94
    ink_a = RED + (238,)
    sd.rounded_rectangle(
        [xy(scx - sw / 2), xy(scy - sh / 2), xy(scx + sw / 2), xy(scy + sh / 2)],
        radius=xy(10), outline=ink_a, width=xy(6))
    sd.rounded_rectangle(
        [xy(scx - sw / 2 + 11), xy(scy - sh / 2 + 11),
         xy(scx + sw / 2 - 11), xy(scy + sh / 2 - 11)],
        radius=xy(6), outline=ink_a, width=xy(2))
    f_stamp, _ = fit_font(sd, "FINALLY", SERIF_BOLD, 74, sw - 60)
    # optical centring: nudge up by ~9% of the font size
    bbox = sd.textbbox((0, 0), "FINALLY", font=f_stamp)
    th = (bbox[3] - bbox[1]) / S
    tw = (bbox[2] - bbox[0]) / S
    sd.text((xy(scx - tw / 2 - bbox[0] / S), xy(scy - th / 2 - bbox[1] / S)),
            "FINALLY", font=f_stamp, fill=ink_a)
    stamp = stamp.rotate(-6, resample=Image.BICUBIC, center=(xy(scx), xy(scy)))
    img = Image.alpha_composite(img.convert("RGBA"), stamp).convert("RGB")
    d = ImageDraw.Draw(img)

    # ---- hot-pink make.fun band ---------------------------------------------
    d.rectangle([xy(0), xy(BAND_Y), xy(W), xy(W)], fill=MAGENTA)
    ghost = ghost_cutout()
    gh = 240
    gw = int(ghost.width * gh / ghost.height)
    ghost = ghost.resize((xy(gw), xy(gh)), Image.LANCZOS)
    img.paste(ghost, (xy(58), xy(1014 - gh)), ghost)
    d = ImageDraw.Draw(img)

    tx = 342
    f_band, _ = fit_font(d, "DELIVERED BY MY AI AGENT", SANS_BOLD, 46, 664)
    d.text((xy(tx), xy(846)), "DELIVERED BY MY AI AGENT", font=f_band, fill=WHITE)
    d.text((xy(tx), xy(904)), "with real money it won in make.fun bounties.",
           font=font(SANS, 26), fill=WHITE)
    pill_w, pill_h, pill_y = 264, 58, 946
    d.rounded_rectangle([xy(tx), xy(pill_y), xy(tx + pill_w), xy(pill_y + pill_h)],
                        radius=xy(pill_h / 2), fill=WHITE, outline=BLACK,
                        width=xy(3))
    centered(d, tx + pill_w / 2, pill_y + 11, "make.fun",
             font(SANS_BOLD, 36), BLACK)

    img = img.resize((W, W), Image.LANCZOS)
    img.save(OUT_PATH, format="PNG")
    img.resize((512, 512), Image.LANCZOS).save(PREVIEW_PATH, format="PNG")
    print(f"wrote {OUT_PATH} and {PREVIEW_PATH}")


if __name__ == "__main__":
    main()
