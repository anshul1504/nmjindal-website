"""Fill the database with the site's starting content (idempotent).

Each table is only filled while it is empty, so content edited or deleted in the
admin is never overwritten.   Usage:  python manage.py seed_content
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from core import catalog
from core.models import (FAQ, ContentItem, HeroSlide, Incoterm, Insight, InsightSection, Page, Product,
                         ProductCategory, Region, Service, SiteSettings)

PHOTOS = Path(settings.BASE_DIR) / "core" / "static" / "core" / "img" / "photos"

MISSION = [
    "Deliver quality products from trusted sources to buyers worldwide",
    "Make cross-border trade smooth, transparent and hassle-free",
    "Build long-term partnerships based on honesty and reliability",
    "Follow all international trade regulations and quality standards",
    "Provide competitive pricing and on-time delivery",
]
STRENGTHS = [
    ("Global network", "A wide supplier and buyer network across markets."),
    ("Strict quality control", "Every order inspected before it ships."),
    ("Transparent pricing", "Clear, honest numbers. No surprises."),
    ("Efficient logistics", "Timely shipments, coordinated by sea, air and land."),
    ("Dedicated contact", "One accountable person for every client."),
    ("Flexible terms", "Built for bulk and recurring orders."),
]
WHY_US = [
    "Experienced trade professionals", "Verified suppliers and quality-checked goods", "Honest, transparent dealings",
    "Competitive pricing", "Full documentation and compliance support", "On-time delivery, every time",
]
PROCESS = [
    ("Brief", "Tell us the product, quantity, destination and budget."),
    ("Source", "We shortlist suppliers against your specification."),
    ("Verify", "Supplier verification and quality checks before dispatch."),
    ("Document", "Invoices, packing lists, certificates and customs papers."),
    ("Ship", "Sea, air or land freight, coordinated and cleared."),
    ("Support", "We stay with you after delivery."),
]
FAQS = [
    ("What do you import and export?", "We import goods such as machinery, raw materials and electronics, and export products such as agricultural products, textiles, metals and spices. We also handle custom sourcing for specific requirements."),
    ("Which agricultural products do you export?", "Rice (basmati and non-basmati), wheat and cereals, pulses, spices, oilseeds, tea, fresh fruit and vegetables, and cashew and dry fruits. Each product page lists specifications, packing options and sourcing season."),
    ("Can I get a sample before placing an order?", "Yes. We can arrange samples for your approval against the agreed specification, and keep a sealed counter-sample for reference."),
    ("Do you handle domestic trade as well?", "Yes. We make international as well as domestic trade simple, transparent and profitable for our partners."),
    ("Can you source a product to my specification?", "Yes. Specialised sourcing is built around your specifications, quantity and budget, with supplier verification and quality checks."),
    ("Which documents do you support?", "Invoices, packing lists, certificates of origin and customs paperwork, in line with international trade regulations."),
    ("How are shipments sent?", "We coordinate sea, air and land freight, and support customs clearance so shipments arrive on time."),
    ("Do you support bulk and recurring orders?", "Yes. We offer flexible terms for bulk and recurring orders, with a dedicated point of contact for every client."),
]
PRIVACY = """## What we collect
When you submit the enquiry form we collect the details you enter: your name, company, email address, phone number, area of interest and message.

## How we use it
We use this information only to respond to your enquiry and to deliver the trade services you ask about. We do not sell your information.

## Storage and access
Enquiries are stored securely and are visible only to authorised members of the NM Jindal Global team.

## Your choices
You can ask us to correct or delete the information you have sent by contacting us through the [contact page](/contact/).

This is a general policy. Have it reviewed against the laws that apply to your business before relying on it."""
TERMS = """## Using this website
This website provides general information about NM Jindal Global and its import-export services. Content is for information only and does not by itself form a contract.

## Enquiries and orders
Submitting an enquiry does not create an obligation for either party. Prices, quantities, delivery timelines and terms are agreed in writing for each order.

## Accuracy
We aim to keep the information here accurate and current, but it may change without notice.

## Contact
Questions about these terms can be sent through the [contact page](/contact/).

This is a general template. Have it reviewed against the laws that apply to your business before relying on it."""


def _attach(instance, field, filename):
    """Copy a bundled photo into the model's ImageField (media storage)."""
    path = PHOTOS / filename
    if path.exists():
        with open(path, "rb") as fh:
            getattr(instance, field).save(filename, File(fh), save=False)


def _static_name(path_or_class):
    name = path_or_class.rsplit("/", 1)[-1]
    return name if name.endswith(".jpg") else name + ".jpg"


class Command(BaseCommand):
    help = "Seed the starting site content (only fills empty tables)."

    def handle(self, *args, **opts):
        site = SiteSettings.load()
        defaults = {"phone": "+91 88787 09000", "email": "contact@nmjindalglobal.com", "email2": "info@nmjindalglobal.com",
                    "website": "nmjindalglobal.com", "notify_email": "info@nmjindalglobal.com"}
        changed = [k for k, v in defaults.items() if not getattr(site, k)]
        for k in changed:
            setattr(site, k, defaults[k])
        if changed:
            site.save()

        if not HeroSlide.objects.exists():
            for i, (img, cap) in enumerate([("hero-rice.jpg", "Basmati & paddy rice"), ("hero-port.jpg", "Port & container freight"), ("hero-wheat.jpg", "Wheat & cereals")]):
                s = HeroSlide(caption=cap, order=i)
                _attach(s, "image", img)
                s.save()

        if not Product.objects.exists():
            cats = {n: ProductCategory.objects.get_or_create(name=n, defaults={"order": i})[0] for i, n in enumerate(catalog.PRODUCT_CATEGORIES)}
            for i, p in enumerate(catalog.PRODUCTS):
                obj = Product(
                    name=p["name"], slug=p["slug"], kicker=p["kicker"], icon=p["icon"], category=cats[p["category"]],
                    summary=p["summary"], about_text="\n\n".join(p["about"]), varieties_text="\n".join(p["varieties"]),
                    specs_text="\n".join(f"{k} | {v}" for k, v in p["specs"]), packing_text="\n".join(p["packing"]),
                    uses_text="\n".join(p["uses"]), season_months=",".join(str(m) for m in p["season"]), order=i)
                _attach(obj, "image", _static_name(p["img"]))
                _attach(obj, "banner", _static_name(p["bg"]))
                obj.save()

        if not Service.objects.exists():
            for i, s in enumerate(catalog.SERVICE_DETAILS):
                obj = Service(
                    name=s["name"], slug=s["slug"], icon=s["icon"], summary=s["summary"], lead=s["lead"],
                    body_text="\n\n".join(s["body"]), includes_text="\n".join(s["includes"]),
                    outcomes_text="\n".join(f"{t} | {d}" for t, d in s["outcomes"]), order=i)
                _attach(obj, "image", _static_name(s["img"]))
                _attach(obj, "banner", _static_name(s["bg"]))
                obj.save()

        if not Insight.objects.exists():
            for i, a in enumerate(catalog.INSIGHTS):
                obj = Insight(title=a["title"], slug=a["slug"], tag=a["tag"], read_minutes=a["read"], excerpt=a["excerpt"], order=i)
                _attach(obj, "image", _static_name(a["img"]))
                obj.save()
                for j, (h, t) in enumerate(a["body"]):
                    InsightSection.objects.create(insight=obj, heading=h, text=t, order=j)

        if not Region.objects.exists():
            for i, r in enumerate(catalog.REGIONS):
                Region.objects.create(name=r["name"], note=r["note"], icon=r["icon"], products_text="\n".join(r["products"]), order=i)

        if not Incoterm.objects.exists():
            for i, (code, name, text) in enumerate(catalog.INCOTERMS):
                Incoterm.objects.create(code=code, name=name, description=text, order=i)

        if not FAQ.objects.exists():
            for i, (q, a) in enumerate(FAQS):
                FAQ.objects.create(question=q, answer=a, order=i)

        def fill(group, rows):
            if ContentItem.objects.filter(group=group).exists():
                return
            for i, row in enumerate(rows):
                ContentItem.objects.create(group=group, order=i, **row)

        fill(ContentItem.MISSION, [{"text": t} for t in MISSION])
        fill(ContentItem.STRENGTH, [{"title": t, "text": d} for t, d in STRENGTHS])
        fill(ContentItem.WHY, [{"text": t} for t in WHY_US])
        fill(ContentItem.PROCESS, [{"title": t, "text": d} for t, d in PROCESS])
        fill(ContentItem.QUALITY, [{"title": t, "text": d, "icon": ic} for t, d, ic in catalog.QUALITY_STAGES])
        fill(ContentItem.DOC, [{"title": name, "icon": ic} for ic, name in catalog.DOCS])

        if not Page.objects.exists():
            Page.objects.create(key=Page.PRIVACY, title="Privacy", accent="Policy", subtitle="How NM Jindal Global handles the information you send us.", body=PRIVACY)
            Page.objects.create(key=Page.TERMS, title="Terms of", accent="Use", subtitle="The basis on which this website is provided.", body=TERMS)

        self.stdout.write(self.style.SUCCESS("Content seeded."))
