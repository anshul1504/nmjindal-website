"""Crops/optimises the downloaded Unsplash photos (tools/photos_raw) into the site.

Run from the project root:  python tools/build_photos.py
"""
from pathlib import Path

from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "tools" / "photos_raw"
OUT = ROOT / "core" / "static" / "core" / "img" / "photos"

# name -> (source, (w, h), focus_x, focus_y)
JOBS = {
    # hero + page backgrounds (wide)
    "hero-port":       ("port_cranes", (1920, 1080), .5, .5),
    "bg-night-port":   ("port_night", (1920, 900), .5, .55),
    "bg-warehouse":    ("wh2", (1920, 900), .5, .5),
    "bg-containers":   ("cont2", (1920, 900), .5, .5),
    "bg-air":          ("air6", (1920, 900), .5, .55),
    "bg-sea":          ("ship4", (1920, 900), .5, .55),
    "bg-quality":      ("qc3", (1920, 900), .5, .4),
    "bg-meeting":      ("biz3", (1920, 900), .5, .45),
    # freight
    "sea-freight":     ("ship3", (1600, 760), .5, .5),
    "air-freight":     ("air6", (1200, 800), .5, .5),
    "land-freight":    ("truck2", (1200, 800), .5, .55),
    # trade
    "trade-import":    ("machine", (1200, 800), .5, .5),
    "trade-electro":   ("circuit1", (1200, 800), .5, .5),
    "trade-export":    ("spice1", (1200, 800), .5, .55),
    "trade-textile":   ("textile", (1200, 800), .5, .5),
    "trade-custom":    ("wh2", (1200, 800), .5, .5),
    # services
    "svc-sourcing":    ("wh3", (1200, 800), .5, .55),
    "svc-inspection":  ("qc2", (1200, 800), .5, .5),
    "svc-docs":        ("qc1", (1200, 800), .5, .5),
    "svc-logistics":   ("ship4", (1200, 800), .5, .5),
    "svc-customs":     ("cont2", (1200, 800), .5, .5),
    "svc-support":     ("biz3", (1200, 800), .5, .5),
    # editorial
    "about-warehouse": ("wh3", (1000, 1300), .5, .5),
    "about-ship":      ("ship_aerial", (1000, 1300), .45, .5),
    "partnership":     ("biz2", (1200, 900), .5, .5),
    "quality":         ("qc3", (1200, 900), .55, .4),
    "containers":      ("cont1", (1200, 900), .5, .5),
    "spices":          ("spice1", (900, 1200), .5, .5),
    # agro products (cards 4:3, detail heroes wide)
    "prod-rice":       ("rice_grain", (1200, 900), .5, .5),
    "prod-wheat":      ("wheat_field", (1200, 900), .5, .5),
    "prod-pulses":     ("chickpea_macro", (1200, 900), .5, .5),
    "prod-spices":     ("spice_market", (1200, 900), .6, .6),
    "prod-oilseeds":   ("sesame", (1200, 900), .5, .5),
    "prod-tea":        ("tea_hill", (1200, 900), .5, .5),
    "prod-fruits":     ("mango", (1200, 900), .5, .5),
    "prod-veg":        ("veg_crates", (1200, 900), .5, .5),
    "prod-nuts":       ("nuts1", (1200, 900), .5, .5),
    "bg-prod-rice":    ("rice_harvest", (1920, 900), .5, .4),
    "bg-prod-wheat":   ("wheat_combine", (1920, 900), .5, .5),
    "bg-prod-pulses":  ("chickpea_pot", (1920, 900), .5, .5),
    "bg-prod-spices":  ("spice_market", (1920, 900), .5, .6),
    "bg-prod-oilseeds": ("sesame", (1920, 900), .5, .5),
    "bg-prod-tea":     ("tea_hill", (1920, 900), .5, .6),
    "bg-prod-fruits":  ("veg_market", (1920, 900), .5, .5),
    "bg-prod-veg":     ("veg_crates", (1920, 900), .5, .5),
    "bg-prod-nuts":    ("nuts1", (1920, 900), .5, .5),
    "bg-farm":         ("paddy_farmer", (1920, 900), .5, .55),
    "bg-harvest":      ("wheat_combine", (1920, 900), .5, .5),
    "hero-rice":       ("rice_harvest", (1920, 1080), .5, .4),
    "hero-wheat":      ("wheat_combine", (1920, 1080), .5, .5),
    "farm-story":      ("rice_harvest", (1000, 1300), .5, .4),
    "farm-peas":       ("peas_bowl", (1000, 1000), .5, .5),
    "agro-jars":       ("spice_jars", (1200, 900), .5, .5),
    # hero visual slides (portrait)
    "hv-rice":         ("rice_harvest", (1000, 1250), .42, .4),
    "hv-port":         ("port_cranes", (1000, 1250), .55, .5),
    "hv-wheat":        ("wheat_combine", (1000, 1250), .5, .5),
    "hv-spice":        ("spice_market", (1000, 1250), .62, .6),
    "agro-warehouse":  ("sacks_wh", (1200, 900), .5, .5),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (src, size, fx, fy) in JOBS.items():
        im = Image.open(RAW / f"{src}.jpg").convert("RGB")
        im = ImageOps.fit(im, size, Image.LANCZOS, centering=(fx, fy))
        # slight warm/contrast grade so the set feels consistent with the gold brand
        im = ImageEnhance.Contrast(im).enhance(1.06)
        im = ImageEnhance.Color(im).enhance(0.92)
        im.save(OUT / f"{name}.jpg", quality=80, optimize=True, progressive=True)
        print("wrote", name)


if __name__ == "__main__":
    main()
