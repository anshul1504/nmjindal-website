"""Generates the site's imagery (gold-on-black, matched to the NM Jindal Global logo).

Run from the project root:  python tools/make_images.py
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "core" / "static" / "core" / "img"
SS = 2  # supersampling factor for smooth edges

GOLD = (232, 184, 84)
GOLD_LIGHT = (255, 224, 140)
GOLD_DARK = (150, 108, 36)
BG = (8, 8, 10)


# ---------------------------------------------------------------- helpers
def canvas(w, h):
    return Image.new("RGB", (w * SS, h * SS), BG)


def glow(img, layer, radius, strength=1.0):
    """Add a blurred copy of `layer` (an RGB image on black) onto img."""
    blurred = layer.filter(ImageFilter.GaussianBlur(radius * SS))
    if strength != 1.0:
        blurred = blurred.point(lambda v: min(255, int(v * strength)))
    return ImageChops.add(img, blurred)


def vignette(img, strength=0.75):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse((-w * 0.25, -h * 0.35, w * 1.25, h * 1.35), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(min(w, h) * 0.18))
    dark = Image.new("RGB", (w, h), BG)
    return Image.composite(img, dark, mask.point(lambda v: int(v * strength + 255 * (1 - strength))))


def finish(img, name, size, quality=88):
    w, h = size
    img = vignette(img).resize((w, h), Image.LANCZOS)
    # subtle film grain keeps gradients from banding
    rnd = random.Random(7)
    noise = Image.effect_noise((w, h), 10).convert("RGB")
    img = Image.blend(img, ImageChops.add(img, noise.point(lambda v: v // 14)), 0.5)
    img.save(IMG / name, quality=quality, optimize=True)
    print("wrote", name)


def mix(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def line_glow(img, pts, color, width, glow_r=6, strength=1.0):
    layer = Image.new("RGB", img.size, (0, 0, 0))
    ImageDraw.Draw(layer).line(pts, fill=color, width=int(width * SS), joint="curve")
    img = glow(img, layer, glow_r, strength)
    ImageDraw.Draw(img).line(pts, fill=color, width=int(width * SS), joint="curve")
    return img


def arc_points(p0, p1, lift, steps=80):
    (x0, y0), (x1, y1) = p0, p1
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2 - lift
    pts = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t ** 2 * x1
        y = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t ** 2 * y1
        pts.append((x, y))
    return pts


def background_grid(img, step=60, alpha=14):
    d = ImageDraw.Draw(img)
    w, h = img.size
    c = (alpha + 6, alpha + 5, alpha)
    for x in range(0, w, step * SS):
        d.line((x, 0, x, h), fill=c, width=1)
    for y in range(0, h, step * SS):
        d.line((0, y, w, y), fill=c, width=1)


def radial_glow(img, center, radius, color, strength=0.35):
    layer = Image.new("RGB", img.size, (0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = center
    for i in range(24, 0, -1):
        t = i / 24
        r = radius * t
        d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=tuple(int(v * strength * (1 - t) ** 1.6) for v in color))
    return ImageChops.add(img, layer.filter(ImageFilter.GaussianBlur(radius * 0.08)))


# ---------------------------------------------------------------- logo
def make_logo():
    src = Image.open(IMG / "logo-source.png").convert("RGB")
    # black background -> transparency (alpha from brightest channel)
    r, g, b = src.split()
    alpha = ImageChops.lighter(ImageChops.lighter(r, g), b).point(lambda v: min(255, int(max(0, v - 6) * 1.12)))
    rgba = Image.merge("RGBA", (r, g, b, alpha))
    # un-premultiply so edges stay gold, not grey
    px = rgba.load()
    for y in range(rgba.height):
        for x in range(rgba.width):
            R, G, B, A = px[x, y]
            if 0 < A < 255:
                k = 255 / max(R, G, B, 1)
                px[x, y] = (min(255, int(R * k)), min(255, int(G * k)), min(255, int(B * k)), A)
    box = alpha.point(lambda v: 255 if v > 24 else 0).getbbox()
    pad = 24
    box = (box[0] - pad, box[1] - pad, box[2] + pad, box[3] + pad)
    full = rgba.crop(box)
    full.save(IMG / "logo.png", optimize=True)

    # NM mark only (top part of the lockup, above the wordmark) for favicon / navbar
    mark_box = (box[0], box[1], box[2], 790)
    mark = rgba.crop(mark_box)
    bb = mark.split()[3].point(lambda v: 255 if v > 24 else 0).getbbox()
    mark = mark.crop(bb)
    side = max(mark.size) + 40
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.paste(mark, ((side - mark.width) // 2, (side - mark.height) // 2))
    sq.resize((256, 256), Image.LANCZOS).save(IMG / "logo-mark.png", optimize=True)
    fav = Image.new("RGBA", (256, 256), BG + (255,))
    fav.alpha_composite(sq.resize((220, 220), Image.LANCZOS), (18, 18))
    fav.save(IMG / "favicon.png")
    fav.resize((64, 64), Image.LANCZOS).save(IMG / "favicon.ico", sizes=[(64, 64), (32, 32), (16, 16)])
    print("wrote logo.png, logo-mark.png, favicon")


# ---------------------------------------------------------------- globe
def land_dots(rnd, n):
    """Rough continent blobs as (lon, lat) clusters, used to dot the globe."""
    blobs = [  # lon, lat, radius(deg), weight
        (-100, 45, 24, 3), (-98, 30, 12, 1), (-60, -12, 18, 3), (-65, -38, 8, 1),
        (10, 50, 14, 2), (20, 5, 20, 3), (25, -20, 12, 2), (50, 28, 14, 2),
        (80, 22, 14, 3), (100, 55, 30, 3), (105, 30, 16, 3), (120, 8, 12, 2),
        (135, 35, 7, 1), (135, -25, 14, 2), (-45, 72, 12, 1),
    ]
    pts = []
    total = sum(b[3] for b in blobs)
    for lon0, lat0, rad, wgt in blobs:
        for _ in range(int(n * wgt / total)):
            a = rnd.uniform(0, math.tau)
            r = rad * math.sqrt(rnd.random())
            pts.append((lon0 + r * math.cos(a) * 1.3, lat0 + r * math.sin(a)))
    return pts


def project(lon, lat, rot, cx, cy, R):
    lam, phi = math.radians(lon + rot), math.radians(lat)
    x = math.cos(phi) * math.sin(lam)
    y = math.sin(phi)
    z = math.cos(phi) * math.cos(lam)
    tilt = math.radians(-18)
    y2 = y * math.cos(tilt) - z * math.sin(tilt)
    z2 = y * math.sin(tilt) + z * math.cos(tilt)
    return cx + x * R, cy - y2 * R, z2


def make_globe(name, size, center, R, rot=-20, hubs=None, density=9000, seed=3):
    rnd = random.Random(seed)
    w, h = size
    img = canvas(w, h)
    cx, cy, R = center[0] * SS, center[1] * SS, R * SS
    img = radial_glow(img, (cx, cy), R * 1.6, GOLD, 0.22)
    d = ImageDraw.Draw(img)
    # sphere body
    d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(14, 12, 10), outline=(70, 55, 28), width=2 * SS)
    # graticule
    for lat in range(-60, 90, 30):
        pts = [project(lon, lat, rot, cx, cy, R) for lon in range(-180, 181, 4)]
        seg = []
        for x, y, z in pts:
            if z > 0:
                seg.append((x, y))
            elif len(seg) > 1:
                d.line(seg, fill=(46, 38, 22), width=SS)
                seg = []
            else:
                seg = []
        if len(seg) > 1:
            d.line(seg, fill=(46, 38, 22), width=SS)
    for lon in range(-180, 180, 30):
        seg = []
        for lat in range(-90, 91, 4):
            x, y, z = project(lon, lat, rot, cx, cy, R)
            if z > 0:
                seg.append((x, y))
            elif len(seg) > 1:
                d.line(seg, fill=(46, 38, 22), width=SS)
                seg = []
            else:
                seg = []
        if len(seg) > 1:
            d.line(seg, fill=(46, 38, 22), width=SS)
    # land dots
    dots = Image.new("RGB", img.size, (0, 0, 0))
    dd = ImageDraw.Draw(dots)
    for lon, lat in land_dots(rnd, density):
        x, y, z = project(lon, lat, rot, cx, cy, R)
        if z > 0.02:
            c = mix(GOLD_DARK, GOLD_LIGHT, min(1, z * 1.1))
            r = (0.9 + 0.9 * z) * SS
            dd.ellipse((x - r, y - r, x + r, y + r), fill=c)
    img = glow(img, dots, 3, 0.8)
    img = ImageChops.add(img, dots)
    # trade arcs between hubs
    hubs = hubs or [(-74, 40), (-0, 51), (77, 28), (121, 31), (28, -26), (-46, -23), (139, 35), (55, 25)]
    screen = []
    for lon, lat in hubs:
        x, y, z = project(lon, lat, rot, cx, cy, R)
        if z > 0.1:
            screen.append((x, y))
    arcs = Image.new("RGB", img.size, (0, 0, 0))
    for i in range(len(screen)):
        for j in range(i + 1, len(screen)):
            if (i * 7 + j * 3) % 3 == 0:
                p0, p1 = screen[i], screen[j]
                dist = math.dist(p0, p1)
                pts = arc_points(p0, p1, dist * 0.35)
                ImageDraw.Draw(arcs).line(pts, fill=GOLD, width=2 * SS, joint="curve")
    img = glow(img, arcs, 8, 1.2)
    img = ImageChops.add(img, arcs.point(lambda v: int(v * 0.9)))
    dots2 = ImageDraw.Draw(img)
    for x, y in screen:
        for r, c in ((9, (90, 66, 20)), (5, GOLD), (2.5, (255, 245, 210))):
            dots2.ellipse((x - r * SS, y - r * SS, x + r * SS, y + r * SS), fill=c)
    # atmosphere rim
    rim = Image.new("RGB", img.size, (0, 0, 0))
    ImageDraw.Draw(rim).ellipse((cx - R, cy - R, cx + R, cy + R), outline=GOLD, width=3 * SS)
    img = glow(img, rim, 14, 0.9)
    # stars / particles
    sd = ImageDraw.Draw(img)
    for _ in range(140):
        x, y = rnd.randint(0, img.width), rnd.randint(0, img.height)
        if math.dist((x, y), (cx, cy)) > R * 1.05:
            v = rnd.randint(50, 130)
            sd.ellipse((x, y, x + SS * 1.6, y + SS * 1.6), fill=(v, int(v * 0.85), int(v * 0.5)))
    finish(img, name, size)


# ---------------------------------------------------------------- scene art
def draw_container_stack(d, x, y, cols, rows, cw, ch, rnd, flat=False):
    pal = [(160, 112, 38), (194, 144, 56), (120, 84, 30), (214, 168, 74), (88, 62, 24)]
    for r in range(rows):
        for c in range(cols):
            x0 = x + c * (cw + 2 * SS)
            y0 = y - (r + 1) * (ch + 2 * SS)
            col = rnd.choice(pal)
            d.rectangle((x0, y0, x0 + cw, y0 + ch), fill=col)
            for k in range(1, 7):
                xx = x0 + k * cw / 7
                d.line((xx, y0 + 2 * SS, xx, y0 + ch - 2 * SS), fill=mix(col, (0, 0, 0), 0.35), width=SS)
            d.rectangle((x0, y0, x0 + cw, y0 + 3 * SS), fill=mix(col, (255, 240, 190), 0.25))


def sea(img, y0, h, t=0.0):
    d = ImageDraw.Draw(img)
    w = img.width
    for i in range(26):
        yy = y0 + i * (h / 26)
        a = i / 26
        col = mix((22, 18, 10), (8, 8, 10), a)
        d.rectangle((0, yy, w, yy + h / 26 + 1), fill=col)
    for i in range(70):
        yy = y0 + 8 * SS + (i / 70) * (h - 12 * SS)
        amp = (3 + 6 * i / 70) * SS
        pts = [(x, yy + math.sin(x / (80 * SS) + i * 1.7) * amp) for x in range(0, w + 20, 20)]
        d.line(pts, fill=mix((38, 30, 16), GOLD_DARK, i / 70 * 0.7), width=SS)


def make_ship(name, size):
    w, h = size
    rnd = random.Random(11)
    img = canvas(w, h)
    img = radial_glow(img, (w * SS * 0.5, h * SS * 0.45), w * SS * 0.7, GOLD, 0.18)
    sea(img, h * SS * 0.68, h * SS * 0.32)
    d = ImageDraw.Draw(img)
    hy = h * SS * 0.7
    x0, x1 = w * SS * 0.07, w * SS * 0.95
    # hull
    hull = [(x0, hy - 70 * SS), (x1 - 40 * SS, hy - 70 * SS), (x1, hy - 100 * SS), (x1 - 30 * SS, hy), (x0 + 60 * SS, hy)]
    d.polygon(hull, fill=(36, 28, 16), outline=GOLD_DARK)
    d.polygon([(x0 + 10 * SS, hy - 12 * SS), (x1 - 45 * SS, hy - 12 * SS), (x1 - 30 * SS, hy), (x0 + 60 * SS, hy)], fill=(120, 40, 24))
    # containers
    cw, ch = 46 * SS, 28 * SS
    cols = int((x1 - x0 - 330 * SS) / (cw + 2 * SS))
    draw_container_stack(d, x0 + 30 * SS, hy - 70 * SS, cols, 5, cw, ch, rnd)
    # bridge
    bx = x1 - 280 * SS
    d.rectangle((bx, hy - 70 * SS - 150 * SS, bx + 150 * SS, hy - 70 * SS), fill=(210, 205, 195))
    for k in range(5):
        d.rectangle((bx + 14 * SS, hy - 70 * SS - 140 * SS + k * 27 * SS, bx + 136 * SS, hy - 70 * SS - 125 * SS + k * 27 * SS), fill=(26, 26, 30))
    d.rectangle((bx + 30 * SS, hy - 70 * SS - 190 * SS, bx + 120 * SS, hy - 70 * SS - 150 * SS), fill=(190, 186, 176))
    d.rectangle((bx + 40 * SS, hy - 70 * SS - 182 * SS, bx + 110 * SS, hy - 70 * SS - 166 * SS), fill=(24, 30, 36))
    d.line((bx + 75 * SS, hy - 70 * SS - 190 * SS, bx + 75 * SS, hy - 70 * SS - 235 * SS), fill=GOLD, width=2 * SS)
    # reflection
    refl = img.crop((0, int(hy - 230 * SS), img.width, int(hy))).transpose(Image.FLIP_TOP_BOTTOM)
    refl = refl.point(lambda v: int(v * 0.22)).filter(ImageFilter.GaussianBlur(3 * SS))
    img.paste(ImageChops.add(img.crop((0, int(hy), img.width, int(hy) + refl.height)), refl), (0, int(hy)))
    # horizon glow
    hz = Image.new("RGB", img.size, (0, 0, 0))
    ImageDraw.Draw(hz).line((0, h * SS * 0.68, w * SS, h * SS * 0.68), fill=GOLD, width=2 * SS)
    img = glow(img, hz, 10, 0.9)
    finish(img, name, size)


def make_air(name, size):
    w, h = size
    img = canvas(w, h)
    img = radial_glow(img, (w * SS * 0.6, h * SS * 0.4), w * SS * 0.6, GOLD, 0.2)
    background_grid(img)
    # routes
    rnd = random.Random(2)
    routes = Image.new("RGB", img.size, (0, 0, 0))
    rd = ImageDraw.Draw(routes)
    for i in range(7):
        p0 = (rnd.randint(0, w // 3) * SS, rnd.randint(h // 2, h) * SS)
        p1 = (rnd.randint(2 * w // 3, w) * SS, rnd.randint(0, h // 2) * SS)
        pts = arc_points(p0, p1, rnd.randint(60, 200) * SS)
        for k in range(0, len(pts) - 3, 4):
            rd.line(pts[k:k + 3], fill=GOLD_DARK, width=2 * SS)
    img = glow(img, routes, 3, 0.8)
    img = ImageChops.add(img, routes)
    # airplane (top-down silhouette)
    cx, cy = w * SS * 0.52, h * SS * 0.5
    s = h * SS / 520
    def P(x, y):
        a = math.radians(-28)
        xr, yr = x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)
        return (cx + xr * s, cy + yr * s)
    body = [P(-20, -230), P(0, -250), P(20, -230), P(26, 120), P(8, 250), P(-8, 250), P(-26, 120)]
    wingL = [P(-20, -20), P(-260, 100), P(-250, 130), P(-20, 70)]
    wingR = [P(20, -20), P(260, 100), P(250, 130), P(20, 70)]
    tailL = [P(-10, 190), P(-90, 245), P(-85, 262), P(-8, 235)]
    tailR = [P(10, 190), P(90, 245), P(85, 262), P(8, 235)]
    shape = Image.new("RGB", img.size, (0, 0, 0))
    sd = ImageDraw.Draw(shape)
    for poly in (wingL, wingR, tailL, tailR, body):
        sd.polygon(poly, fill=GOLD)
    img = glow(img, shape, 24, 0.9)
    d = ImageDraw.Draw(img)
    for poly, col in ((wingL, GOLD_DARK), (wingR, GOLD), (tailL, GOLD_DARK), (tailR, GOLD), (body, GOLD_LIGHT)):
        d.polygon(poly, fill=col)
    # engines
    for ex, ey in ((-95, 20), (95, 20), (-165, 60), (165, 60)):
        x, y = P(ex, ey)
        d.ellipse((x - 11 * s, y - 11 * s, x + 11 * s, y + 11 * s), fill=(60, 44, 18))
    finish(img, name, size)


def make_truck_port(name, size):
    w, h = size
    rnd = random.Random(5)
    img = canvas(w, h)
    img = radial_glow(img, (w * SS * 0.3, h * SS * 0.35), w * SS * 0.6, GOLD, 0.2)
    d = ImageDraw.Draw(img)
    gy = h * SS * 0.8
    d.rectangle((0, gy, w * SS, h * SS), fill=(14, 13, 12))
    d.line((0, gy, w * SS, gy), fill=GOLD_DARK, width=2 * SS)
    # gantry crane
    cx0 = w * SS * 0.14
    crane = Image.new("RGB", img.size, (0, 0, 0))
    cd = ImageDraw.Draw(crane)
    for lx in (cx0, cx0 + 120 * SS):
        cd.line((lx, gy, lx, gy - 330 * SS), fill=GOLD, width=7 * SS)
    cd.line((cx0 - 100 * SS, gy - 330 * SS, cx0 + 380 * SS, gy - 330 * SS), fill=GOLD, width=9 * SS)
    cd.line((cx0 - 100 * SS, gy - 330 * SS, cx0 + 60 * SS, gy - 400 * SS), fill=GOLD, width=4 * SS)
    cd.line((cx0 + 60 * SS, gy - 400 * SS, cx0 + 380 * SS, gy - 330 * SS), fill=GOLD, width=4 * SS)
    for k in range(7):
        cd.line((cx0, gy - 40 * SS - k * 45 * SS, cx0 + 120 * SS, gy - 85 * SS - k * 45 * SS), fill=GOLD_DARK, width=2 * SS)
    cd.line((cx0 + 280 * SS, gy - 330 * SS, cx0 + 280 * SS, gy - 200 * SS), fill=GOLD_LIGHT, width=2 * SS)
    cd.rectangle((cx0 + 245 * SS, gy - 200 * SS, cx0 + 315 * SS, gy - 170 * SS), fill=GOLD)
    img = glow(img, crane, 8, 0.7)
    img = ImageChops.add(img, crane)
    d = ImageDraw.Draw(img)
    # container yard
    draw_container_stack(d, w * SS * 0.45, gy, 5, 4, 56 * SS, 34 * SS, rnd)
    draw_container_stack(d, w * SS * 0.7, gy, 4, 3, 56 * SS, 34 * SS, rnd)
    # truck
    tx = w * SS * 0.1
    ty = gy
    d.rectangle((tx, ty - 120 * SS, tx + 260 * SS, ty - 28 * SS), fill=(168, 120, 42))
    for k in range(1, 9):
        d.line((tx + k * 29 * SS, ty - 114 * SS, tx + k * 29 * SS, ty - 34 * SS), fill=(110, 76, 26), width=SS)
    d.polygon([(tx + 268 * SS, ty - 110 * SS), (tx + 330 * SS, ty - 110 * SS), (tx + 360 * SS, ty - 62 * SS), (tx + 360 * SS, ty - 28 * SS), (tx + 268 * SS, ty - 28 * SS)], fill=(210, 205, 195))
    d.polygon([(tx + 280 * SS, ty - 100 * SS), (tx + 322 * SS, ty - 100 * SS), (tx + 344 * SS, ty - 66 * SS), (tx + 280 * SS, ty - 66 * SS)], fill=(24, 30, 36))
    for wx in (tx + 50 * SS, tx + 110 * SS, tx + 300 * SS):
        d.ellipse((wx - 22 * SS, ty - 44 * SS, wx + 22 * SS, ty), fill=(18, 18, 18), outline=GOLD_DARK, width=3 * SS)
    finish(img, name, size)


def make_check(name, size):
    """Quality & compliance: shield + check, document stack."""
    w, h = size
    img = canvas(w, h)
    img = radial_glow(img, (w * SS * 0.5, h * SS * 0.5), w * SS * 0.55, GOLD, 0.26)
    background_grid(img, 50)
    cx, cy = w * SS / 2, h * SS / 2
    s = h * SS / 560
    # documents behind
    docs = Image.new("RGB", img.size, (0, 0, 0))
    dd = ImageDraw.Draw(docs)
    for dx, dy, ang in ((-230, 20, -9), (230, 30, 8)):
        pts = []
        for px, py in ((-120, -150), (120, -150), (120, 150), (-120, 150)):
            a = math.radians(ang)
            pts.append((cx + (dx + px * math.cos(a) - py * math.sin(a)) * s, cy + (dy + px * math.sin(a) + py * math.cos(a)) * s))
        dd.polygon(pts, fill=(34, 28, 16), outline=GOLD_DARK)
        for k in range(7):
            a = math.radians(ang)
            def Q(px, py):
                return (cx + (dx + px * math.cos(a) - py * math.sin(a)) * s, cy + (dy + px * math.sin(a) + py * math.cos(a)) * s)
            dd.line((Q(-90, -100 + k * 28), Q(90 if k % 3 else 40, -100 + k * 28)), fill=GOLD_DARK, width=3 * SS)
    img = ImageChops.add(img, docs)
    # shield
    shield = [(0, -190), (150, -140), (150, 20), (0, 200), (-150, 20), (-150, -140)]
    pts = [(cx + x * s, cy + y * s) for x, y in shield]
    layer = Image.new("RGB", img.size, (0, 0, 0))
    ImageDraw.Draw(layer).polygon(pts, fill=GOLD)
    img = glow(img, layer, 26, 0.9)
    d = ImageDraw.Draw(img)
    d.polygon(pts, fill=(20, 17, 11), outline=GOLD, width=5 * SS)
    inner = [(cx + x * 0.86 * s, cy + y * 0.86 * s) for x, y in shield]
    d.polygon(inner, outline=GOLD_DARK, width=2 * SS)
    chk = [(cx - 70 * s, cy - 5 * s), (cx - 20 * s, cy + 50 * s), (cx + 75 * s, cy - 60 * s)]
    img = line_glow(img, chk, GOLD_LIGHT, 16, 10, 1.0)
    finish(img, name, size)


def make_handshake_network(name, size):
    """Partnerships: network of nodes around a central ring."""
    w, h = size
    rnd = random.Random(21)
    img = canvas(w, h)
    img = radial_glow(img, (w * SS / 2, h * SS / 2), w * SS * 0.55, GOLD, 0.24)
    background_grid(img)
    cx, cy = w * SS / 2, h * SS / 2
    nodes = []
    for ring, count, rr in ((1, 8, 150), (2, 14, 250)):
        for i in range(count):
            a = i / count * math.tau + ring * 0.4
            nodes.append((cx + math.cos(a) * rr * SS * 1.4, cy + math.sin(a) * rr * SS * 0.95))
    net = Image.new("RGB", img.size, (0, 0, 0))
    nd = ImageDraw.Draw(net)
    for n in nodes:
        nd.line((cx, cy, n[0], n[1]), fill=GOLD_DARK, width=SS)
    for i, a in enumerate(nodes):
        for b in nodes[i + 1:]:
            if math.dist(a, b) < 230 * SS:
                nd.line((a, b), fill=(90, 66, 24), width=SS)
    img = glow(img, net, 3, 0.9)
    img = ImageChops.add(img, net)
    d = ImageDraw.Draw(img)
    for x, y in nodes:
        r = rnd.choice((6, 8, 10)) * SS
        d.ellipse((x - r * 2, y - r * 2, x + r * 2, y + r * 2), fill=(30, 24, 12))
        d.ellipse((x - r, y - r, x + r, y + r), fill=GOLD)
    for r, wd in ((110, 3), (80, 2), (50, 2)):
        ring = Image.new("RGB", img.size, (0, 0, 0))
        ImageDraw.Draw(ring).ellipse((cx - r * SS, cy - r * SS, cx + r * SS, cy + r * SS), outline=GOLD, width=wd * SS)
        img = glow(img, ring, 10, 1.0)
        ImageDraw.Draw(img).ellipse((cx - r * SS, cy - r * SS, cx + r * SS, cy + r * SS), outline=GOLD_LIGHT if r == 50 else GOLD, width=wd * SS)
    d = ImageDraw.Draw(img)
    d.ellipse((cx - 22 * SS, cy - 22 * SS, cx + 22 * SS, cy + 22 * SS), fill=GOLD_LIGHT)
    finish(img, name, size)


# ---------------------------------------------------------------- icon-style cards (service imagery)
def icon_canvas(name, size, painter):
    w, h = size
    img = canvas(w, h)
    img = radial_glow(img, (w * SS * 0.5, h * SS * 0.55), w * SS * 0.6, GOLD, 0.25)
    background_grid(img, 40)
    img = painter(img, w * SS, h * SS)
    finish(img, name, size)


def gold_layer(img, draw_fn, glow_r=14, strength=0.9):
    layer = Image.new("RGB", img.size, (0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    img = glow(img, layer, glow_r, strength)
    draw_fn(ImageDraw.Draw(img))
    return img


def p_sourcing(img, W, H):
    cx, cy, s = W / 2, H / 2, H / 400
    def f(d):
        r = 95 * s
        d.ellipse((cx - 30 * s - r, cy - 30 * s - r, cx - 30 * s + r, cy - 30 * s + r), outline=GOLD, width=int(14 * s))
        d.line((cx + 40 * s, cy + 40 * s, cx + 130 * s, cy + 130 * s), fill=GOLD, width=int(26 * s))
        d.ellipse((cx - 30 * s - 50 * s, cy - 30 * s - 50 * s, cx - 30 * s + 50 * s, cy - 30 * s + 50 * s), outline=GOLD_DARK, width=int(4 * s))
        for ang in range(0, 360, 60):
            a = math.radians(ang)
            d.line((cx - 30 * s, cy - 30 * s, cx - 30 * s + math.cos(a) * 50 * s, cy - 30 * s + math.sin(a) * 50 * s), fill=GOLD_DARK, width=int(3 * s))
    return gold_layer(img, f)


def p_inspect(img, W, H):
    cx, cy, s = W / 2, H / 2, H / 400
    def f(d):
        d.rounded_rectangle((cx - 110 * s, cy - 130 * s, cx + 110 * s, cy + 130 * s), radius=int(14 * s), outline=GOLD, width=int(8 * s))
        for k in range(4):
            y = cy - 80 * s + k * 55 * s
            d.line((cx - 40 * s, y, cx + 70 * s, y), fill=GOLD_DARK, width=int(8 * s))
            d.line((cx - 80 * s, y, cx - 55 * s, y + 8 * s), fill=GOLD_LIGHT, width=int(8 * s))
    return gold_layer(img, f)


def p_docs(img, W, H):
    cx, cy, s = W / 2, H / 2, H / 400
    def f(d):
        for dx, dy in ((-50, 20), (0, 0), (50, -20)):
            d.rounded_rectangle((cx + (dx - 85) * s, cy + (dy - 115) * s, cx + (dx + 85) * s, cy + (dy + 115) * s), radius=int(10 * s), outline=GOLD if dx == 50 else GOLD_DARK, width=int(6 * s))
        for k in range(5):
            d.line((cx + 5 * s, cy - 80 * s + k * 34 * s, cx + (95 if k % 2 else 70) * s, cy - 80 * s + k * 34 * s), fill=GOLD, width=int(6 * s))
        d.ellipse((cx + 70 * s, cy + 60 * s, cx + 130 * s, cy + 120 * s), outline=GOLD_LIGHT, width=int(6 * s))
    return gold_layer(img, f)


def p_logistics(img, W, H):
    cx, cy, s = W / 2, H / 2, H / 400
    def f(d):
        d.polygon([(cx - 140 * s, cy + 30 * s), (cx + 140 * s, cy + 30 * s), (cx + 110 * s, cy + 90 * s), (cx - 100 * s, cy + 90 * s)], outline=GOLD, width=int(7 * s))
        for k in range(3):
            d.rectangle((cx - 100 * s + k * 62 * s, cy - 30 * s, cx - 48 * s + k * 62 * s, cy + 24 * s), outline=GOLD_LIGHT, width=int(5 * s))
        d.line((cx + 80 * s, cy - 30 * s, cx + 80 * s, cy - 100 * s), fill=GOLD, width=int(6 * s))
        d.polygon([(cx + 80 * s, cy - 100 * s), (cx + 130 * s, cy - 82 * s), (cx + 80 * s, cy - 64 * s)], fill=GOLD)
        for k in range(3):
            pts = [(cx - 160 * s + x * s, cy + 125 * s + math.sin(x / 22 + k) * 6 * s + k * 14 * s) for x in range(0, 330, 8)]
            d.line(pts, fill=GOLD_DARK, width=int(4 * s))
    return gold_layer(img, f)


def p_customs(img, W, H):
    cx, cy, s = W / 2, H / 2, H / 400
    def f(d):
        d.rectangle((cx - 130 * s, cy - 110 * s, cx + 130 * s, cy + 110 * s), outline=GOLD_DARK, width=int(6 * s))
        d.ellipse((cx - 70 * s, cy - 70 * s, cx + 70 * s, cy + 70 * s), outline=GOLD, width=int(9 * s))
        d.ellipse((cx - 40 * s, cy - 40 * s, cx + 40 * s, cy + 40 * s), outline=GOLD_DARK, width=int(4 * s))
        d.ellipse((cx - 70 * s, cy - 18 * s, cx + 70 * s, cy + 18 * s), outline=GOLD, width=int(4 * s))
        d.line((cx, cy - 70 * s, cx, cy + 70 * s), fill=GOLD, width=int(4 * s))
        d.line((cx - 38 * s, cy + 124 * s, cx - 8 * s, cy + 154 * s), fill=GOLD_LIGHT, width=int(10 * s))
        d.line((cx - 8 * s, cy + 154 * s, cx + 52 * s, cy + 98 * s), fill=GOLD_LIGHT, width=int(10 * s))
    return gold_layer(img, f)


def p_support(img, W, H):
    cx, cy, s = W / 2, H / 2, H / 400
    def f(d):
        d.arc((cx - 100 * s, cy - 120 * s, cx + 100 * s, cy + 80 * s), 180, 360, fill=GOLD, width=int(12 * s))
        d.rounded_rectangle((cx - 128 * s, cy - 40 * s, cx - 86 * s, cy + 30 * s), radius=int(12 * s), fill=GOLD)
        d.rounded_rectangle((cx + 86 * s, cy - 40 * s, cx + 128 * s, cy + 30 * s), radius=int(12 * s), fill=GOLD)
        d.arc((cx - 110 * s, cy - 40 * s, cx + 80 * s, cy + 120 * s), 20, 100, fill=GOLD_DARK, width=int(8 * s))
        d.ellipse((cx + 40 * s, cy + 90 * s, cx + 80 * s, cy + 124 * s), fill=GOLD_LIGHT)
    return gold_layer(img, f)


def p_import(img, W, H):
    cx, cy, s = W / 2, H / 2, H / 400
    def f(d):
        # box with arrow in
        d.polygon([(cx - 110 * s, cy - 20 * s), (cx, cy - 75 * s), (cx + 110 * s, cy - 20 * s), (cx, cy + 35 * s)], outline=GOLD, width=int(6 * s))
        d.line((cx - 110 * s, cy - 20 * s, cx - 110 * s, cy + 80 * s), fill=GOLD, width=int(6 * s))
        d.line((cx + 110 * s, cy - 20 * s, cx + 110 * s, cy + 80 * s), fill=GOLD, width=int(6 * s))
        d.line((cx, cy + 35 * s, cx, cy + 135 * s), fill=GOLD, width=int(6 * s))
        d.line((cx - 110 * s, cy + 80 * s, cx, cy + 135 * s), fill=GOLD, width=int(6 * s))
        d.line((cx + 110 * s, cy + 80 * s, cx, cy + 135 * s), fill=GOLD, width=int(6 * s))
        d.line((cx, cy - 170 * s, cx, cy - 90 * s), fill=GOLD_LIGHT, width=int(12 * s))
        d.polygon([(cx - 30 * s, cy - 110 * s), (cx + 30 * s, cy - 110 * s), (cx, cy - 70 * s)], fill=GOLD_LIGHT)
    return gold_layer(img, f)


def p_export(img, W, H):
    cx, cy, s = W / 2, H / 2, H / 400
    def f(d):
        d.polygon([(cx - 110 * s, cy - 10 * s), (cx, cy - 65 * s), (cx + 110 * s, cy - 10 * s), (cx, cy + 45 * s)], outline=GOLD, width=int(6 * s))
        d.line((cx - 110 * s, cy - 10 * s, cx - 110 * s, cy + 90 * s), fill=GOLD, width=int(6 * s))
        d.line((cx + 110 * s, cy - 10 * s, cx + 110 * s, cy + 90 * s), fill=GOLD, width=int(6 * s))
        d.line((cx, cy + 45 * s, cx, cy + 145 * s), fill=GOLD, width=int(6 * s))
        d.line((cx - 110 * s, cy + 90 * s, cx, cy + 145 * s), fill=GOLD, width=int(6 * s))
        d.line((cx + 110 * s, cy + 90 * s, cx, cy + 145 * s), fill=GOLD, width=int(6 * s))
        d.line((cx, cy - 80 * s, cx, cy - 165 * s), fill=GOLD_LIGHT, width=int(12 * s))
        d.polygon([(cx - 30 * s, cy - 140 * s), (cx + 30 * s, cy - 140 * s), (cx, cy - 180 * s)], fill=GOLD_LIGHT)
    return gold_layer(img, f)


def p_custom(img, W, H):
    cx, cy, s = W / 2, H / 2, H / 400
    def f(d):
        d.ellipse((cx - 110 * s, cy - 110 * s, cx + 110 * s, cy + 110 * s), outline=GOLD, width=int(7 * s))
        d.ellipse((cx - 60 * s, cy - 60 * s, cx + 60 * s, cy + 60 * s), outline=GOLD_DARK, width=int(5 * s))
        d.ellipse((cx - 14 * s, cy - 14 * s, cx + 14 * s, cy + 14 * s), fill=GOLD_LIGHT)
        for ang in range(0, 360, 90):
            a = math.radians(ang)
            d.line((cx + math.cos(a) * 110 * s, cy + math.sin(a) * 110 * s, cx + math.cos(a) * 150 * s, cy + math.sin(a) * 150 * s), fill=GOLD, width=int(7 * s))
    return gold_layer(img, f)


def main():
    """Only the logo cut-out is generated now; site imagery uses real photos (tools/build_photos.py)."""
    IMG.mkdir(parents=True, exist_ok=True)
    make_logo()


if __name__ == "__main__":
    main()
