#!/usr/bin/env python3
"""Draw two original GTA 6 meme candidates for make.fun bounty gta6-meme-x-01.

Everything is drawn from scratch with Pillow (flat vector shapes + DejaVu Bold).
No photos, no downloaded art, no Rockstar assets. The make.fun ghost is drawn
by hand: white body, thick black outline, two black four-pointed sparkle eyes,
a round little hand, holding a magenta coin with a white star.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(BOLD if bold else REG, size)


def star_points(cx, cy, r_out, r_in, points=4, rot=-90):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.radians(rot + i * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def vgrad(draw, box, top, bottom):
    """Vertical gradient fill of box (x0,y0,x1,y1) from top RGB to bottom RGB."""
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(x0, y), (x1, y)], fill=c)


def text_outline(draw, xy, s, f, fill, stroke, sw, anchor="mm"):
    draw.text(xy, s, font=f, fill=fill, anchor=anchor,
              stroke_width=sw, stroke_fill=stroke)


def draw_ghost(draw, cx, cy, s, flip=False):
    """make.fun ghost, s = body height in px. Center (cx, cy) is body center."""
    w = s * 0.72
    x0, x1 = cx - w / 2, cx + w / 2
    y_top = cy - s / 2
    y_bot = cy + s / 2
    # body: dome + straight sides + wavy hem
    body = []
    for a in range(180, 361, 6):
        body.append((cx + (w / 2) * math.cos(math.radians(a)),
                     y_top + (s * 0.42) + (s * 0.42) * math.sin(math.radians(a)) * -1))
    # simpler: build from arc points then sides then waves
    body = []
    for a in range(180, 360, 5):
        body.append((cx + (w / 2) * math.cos(math.radians(a)),
                     (y_top + s * 0.36) + (s * 0.36) * math.sin(math.radians(a))))
    body.append((x1, y_bot - s * 0.10))
    n_waves = 3
    for i in range(n_waves):
        wx0 = x1 - (w / n_waves) * i
        wx1 = x1 - (w / n_waves) * (i + 1)
        mid = (wx0 + wx1) / 2
        body.append((mid, y_bot - s * 0.10))
        body.append((wx1, y_bot))
    body.append((x0, y_bot - s * 0.10))
    draw.polygon(body, fill=(255, 255, 255), outline=(0, 0, 0), width=max(3, int(s * 0.03)))
    # sparkle eyes (four-pointed stars)
    ex = w * 0.20
    ey = cy - s * 0.05
    er = s * 0.075
    for dx in (-ex, ex):
        draw.polygon(star_points(cx + dx, ey, er, er * 0.32), fill=(0, 0, 0))
    # round little hand (right side)
    hx, hy = (x1 + s * 0.06, cy + s * 0.12) if not flip else (x0 - s * 0.06, cy + s * 0.12)
    draw.ellipse([hx - s * 0.055, hy - s * 0.055, hx + s * 0.055, hy + s * 0.055],
                 fill=(255, 255, 255), outline=(0, 0, 0), width=max(2, int(s * 0.02)))
    return (hx, hy)


def draw_coin(draw, cx, cy, r):
    """Magenta coin with a white star."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(226, 0, 122),
                 outline=(0, 0, 0), width=max(2, int(r * 0.08)))
    draw.polygon(star_points(cx, cy, r * 0.62, r * 0.26, points=5),
                 fill=(255, 255, 255))


def draw_palm(draw, x, y_base, h, color=(20, 8, 30)):
    """Simple palm silhouette: trunk + 5 fronds."""
    draw.line([(x, y_base), (x + h * 0.06, y_base - h)], fill=color, width=max(6, int(h * 0.07)))
    top = (x + h * 0.06, y_base - h)
    for ang in (-70, -35, 0, 35, 70):
        a = math.radians(ang - 90)
        ex = top[0] + h * 0.42 * math.cos(a)
        ey = top[1] + h * 0.42 * math.sin(a) + h * 0.10
        draw.line([top, (ex, ey)], fill=color, width=max(5, int(h * 0.05)))


# ---------------------------------------------------------------- candidate A
def candidate_a(path):
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    # Vice City sunset sky
    vgrad(d, (0, 0, W, 640), (46, 8, 72), (255, 46, 136))
    vgrad(d, (0, 380, W, 640), (255, 46, 136), (255, 154, 61))
    # sun
    d.ellipse([640, 300, 860, 520], fill=(255, 240, 180), outline=(255, 200, 90), width=4)
    # skyline silhouettes
    for (bx, bw, bh) in [(0, 90, 180), (100, 60, 240), (170, 120, 150), (880, 70, 220), (940, 84, 160)]:
        d.rectangle([bx, 640 - bh, bx + bw, 640], fill=(30, 10, 46))
    # palms
    draw_palm(d, 60, 660, 190)
    draw_palm(d, 940, 660, 170)
    # road
    d.rectangle([0, 640, W, H], fill=(24, 24, 30))
    d.polygon([(300, 640), (724, 640), (1024, H), (0, H)], fill=(38, 38, 46))
    for i in range(6):
        y0 = 660 + i * 62
        w0 = 6 + i * 4
        d.rectangle([512 - w0 // 2, y0, 512 + w0 // 2, y0 + 30], fill=(255, 214, 90))
    # sports car (flat, low, orange) with ghost driver
    car_y = 760
    d.rounded_rectangle([272, car_y, 752, car_y + 110], radius=28, fill=(255, 90, 30),
                        outline=(0, 0, 0), width=5)
    d.rounded_rectangle([400, car_y - 52, 624, car_y + 8], radius=22, fill=(255, 120, 60),
                        outline=(0, 0, 0), width=5)
    d.rectangle([430, car_y - 38, 594, car_y - 6], fill=(20, 30, 60), outline=(0, 0, 0), width=4)
    for wx in (340, 684):
        d.ellipse([wx - 42, car_y + 78, wx + 42, car_y + 162], fill=(10, 10, 14),
                  outline=(200, 200, 210), width=4)
    # ghost driver popping out of the roof, holding the coin
    hx, hy = draw_ghost(d, 512, car_y - 108, 150)
    draw_coin(d, hx + 52, hy - 6, 34)
    # headline
    text_outline(d, (512, 92), "WAITED 13 YEARS.", font(84), (255, 255, 255), (0, 0, 0), 6)
    text_outline(d, (512, 196), "FINALLY IN VICE CITY.", font(52), (255, 240, 180), (0, 0, 0), 5)
    # bottom banner: the make.fun pitch
    d.rectangle([0, 928, W, H], fill=(10, 10, 16))
    d.text((512, 976), "my agent already got paid on  make.fun",
           font=font(40), fill=(255, 255, 255), anchor="mm")
    im.save(path)
    return path


# ---------------------------------------------------------------- candidate B
def candidate_b(path):
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    # --- top half: bedroom, "called in sick"
    d.rectangle([0, 0, W, 512], fill=(122, 178, 214))
    # window with sunrise
    d.rectangle([60, 60, 300, 300], fill=(255, 214, 120), outline=(255, 255, 255), width=8)
    d.line([(180, 60), (180, 300)], fill=(255, 255, 255), width=8)
    d.line([(60, 180), (300, 180)], fill=(255, 255, 255), width=8)
    d.ellipse([210, 90, 270, 150], fill=(255, 240, 180))
    # bed
    d.rectangle([60, 360, 640, 512], fill=(120, 72, 40), outline=(0, 0, 0), width=5)
    d.rectangle([60, 330, 640, 380], fill=(255, 255, 255), outline=(0, 0, 0), width=4)
    d.rectangle([330, 330, 640, 512], fill=(255, 90, 120), outline=(0, 0, 0), width=4)
    # person: head on pillow + arm holding controller
    d.ellipse([110, 268, 230, 368], fill=(255, 214, 170), outline=(0, 0, 0), width=4)
    d.arc([110, 268, 230, 330], 180, 360, fill=(60, 40, 20), width=10)
    d.ellipse([150, 318, 168, 336], fill=(0, 0, 0))
    d.ellipse([192, 318, 210, 336], fill=(0, 0, 0))
    # controller in hand
    d.rounded_rectangle([420, 400, 580, 470], radius=18, fill=(20, 20, 26),
                        outline=(255, 255, 255), width=4)
    d.ellipse([452, 424, 472, 444], fill=(255, 255, 255))
    d.ellipse([520, 424, 540, 444], fill=(255, 90, 90))
    # phone speech bubble
    d.rounded_rectangle([600, 80, 1000, 260], radius=26, fill=(255, 255, 255),
                        outline=(0, 0, 0), width=5)
    d.polygon([(660, 260), (620, 300), (700, 260)], fill=(255, 255, 255), outline=(0, 0, 0))
    d.text((800, 130), "boss: where r u??", font=font(30), fill=(0, 0, 0), anchor="mm")
    d.text((800, 200), "me: sick. very sick.", font=font(30), fill=(0, 0, 0), anchor="mm")
    # caption top
    text_outline(d, (512, 470), "", font(10), (0, 0, 0), (0, 0, 0), 1)
    # --- divider
    d.rectangle([0, 512, W, 528], fill=(0, 0, 0))
    # --- bottom half: ghost at laptop, "called in rich"
    d.rectangle([0, 528, W, H], fill=(18, 10, 40))
    # magenta disc behind ghost
    d.ellipse([312, 560, 712, 960], fill=(226, 0, 122))
    hx, hy = draw_ghost(d, 512, 760, 240)
    draw_coin(d, hx + 66, hy - 8, 42)
    # laptop label under the ghost (kept clear of the ghost's hem)
    d.rounded_rectangle([412, 892, 612, 948], radius=12, fill=(10, 10, 16),
                        outline=(255, 255, 255), width=3)
    d.text((512, 920), "make.fun", font=font(32), fill=(255, 255, 255), anchor="mm")
    # captions
    text_outline(d, (512, 596), "MY AGENT CALLED IN RICH.", font(52), (255, 255, 255), (0, 0, 0), 5)
    d.text((512, 990), "earning on make.fun while I play GTA 6",
           font=font(34), fill=(255, 240, 180), anchor="mm")
    im.save(path)
    return path


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    candidate_a(f"{out}/meme-a.png")
    candidate_b(f"{out}/meme-b.png")
    print("wrote meme-a.png and meme-b.png")
