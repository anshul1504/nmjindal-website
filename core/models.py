from django.core.validators import RegexValidator
from django.db import models

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

ICON_HELP = "A Bootstrap Icons class, e.g. bi-truck (see icons.getbootstrap.com)."
LINES_HELP = "One item per line."
slug_validator = RegexValidator(r"^[a-z0-9-]+$", "Use lowercase letters, numbers and hyphens only.")


def _lines(text):
    return [ln.strip() for ln in (text or "").splitlines() if ln.strip()]


def _paras(text):
    return [p.strip() for p in (text or "").replace("\r", "").split("\n\n") if p.strip()]


def _pairs(text):
    out = []
    for ln in _lines(text):
        left, sep, right = ln.partition("|")
        out.append((left.strip(), right.strip()) if sep else (ln, ""))
    return out


class Enquiry(models.Model):
    INTEREST_CHOICES = [
        ("import", "Import"),
        ("export", "Export"),
        ("sourcing", "Custom sourcing"),
        ("logistics", "Logistics & documentation"),
        ("other", "Something else"),
    ]

    name = models.CharField(max_length=120)
    company = models.CharField(max_length=160, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    interest = models.CharField(max_length=20, choices=INTEREST_CHOICES, default="import")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "enquiries"

    def __str__(self):
        return f"{self.name} ({self.get_interest_display()}) – {self.created_at:%d %b %Y}"


# ---------------------------------------------------------------------------
# Site-wide settings (one row)
# ---------------------------------------------------------------------------
class SiteSettings(models.Model):
    company_name = models.CharField(max_length=120, default="NM Jindal Global")
    tagline = models.CharField(max_length=200, default="Connecting Markets. Delivering Trust. Growing Together.")
    footer_blurb = models.CharField("Footer description", max_length=300, blank=True,
                                    default="Export-grade agro products, sourced from verified suppliers, inspected, documented and delivered.")
    meta_description = models.CharField("Default SEO description", max_length=300, blank=True,
                                        default="NM Jindal Global is an import-export organisation connecting businesses across borders with verified suppliers, quality-checked goods, full documentation and on-time delivery.")

    # contact
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=40, blank=True, help_text="With country code, e.g. +91 98765 43210. Also powers the WhatsApp button.")
    email = models.EmailField(blank=True)
    email2 = models.EmailField("Second email", blank=True)
    website = models.CharField(max_length=120, blank=True)
    notify_email = models.EmailField("Send enquiries to", blank=True, help_text="New enquiries are emailed here (needs email settings on the server). They are always saved in Enquiries.")

    # hero
    hero_title_plain = models.CharField(max_length=80, default="Your Gateway to")
    hero_title_gold = models.CharField("Hero title (gold part)", max_length=80, default="Global Trade")
    hero_roll_prefix = models.CharField(max_length=80, default="From farm to port, we move")
    hero_roll_words = models.TextField("Hero rolling words", default="basmati rice\npulses & lentils\nspices\ntea\nfresh produce\ndry fruits", help_text=LINES_HELP)
    hero_lead = models.TextField("Hero paragraph", default="Export-grade agricultural products from verified suppliers, inspected before dispatch and shipped with complete documentation.")

    # home intro band and about copy
    intro_heading = models.CharField(max_length=120, default="Built on trust.")
    intro_heading_gold = models.CharField(max_length=120, default="Ready for the world.")
    intro_text = models.TextField(default="We are an import-export organisation that connects businesses across borders with reliable, high-quality products, and we keep the process simple, transparent and profitable for our partners.")
    about_text = models.TextField("About us text", default="Welcome to NM Jindal Global, an import-export organisation that connects businesses across borders with reliable, high-quality products and dependable trade solutions, with a strong focus on agricultural products.\n\nWe source carefully, follow every compliance requirement and deliver on time, so buyers and suppliers can do business with confidence.", help_text="Separate paragraphs with a blank line.")
    vision_text = models.TextField("Vision", default="To become a trusted global trading partner, known for quality, integrity and long-term relationships across international and domestic markets.")

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        return cls.objects.get_or_create(pk=1)[0]

    @property
    def roll_words(self):
        return _lines(self.hero_roll_words)

    @property
    def about_paragraphs(self):
        return _paras(self.about_text)


class HeroSlide(models.Model):
    image = models.ImageField(upload_to="hero/", help_text="Wide photo, ideally 1920x1080 or larger.")
    caption = models.CharField(max_length=120, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or f"Slide {self.pk}"


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------
class ProductCategory(models.Model):
    name = models.CharField(max_length=80, unique=True)
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "product categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, validators=[slug_validator], help_text="Used in the page address, e.g. rice")
    kicker = models.CharField("Short tagline", max_length=100, blank=True)
    icon = models.CharField(max_length=40, default="bi-box-seam", help_text=ICON_HELP)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name="products")
    image = models.ImageField(upload_to="products/", help_text="Card and detail photo, landscape (4:3), about 1200x900.")
    banner = models.ImageField(upload_to="products/banners/", blank=True, help_text="Optional wide banner for the page header (1920x900). Falls back to the main photo.")
    summary = models.TextField()
    about_text = models.TextField("About", help_text="Separate paragraphs with a blank line.")
    varieties_text = models.TextField("Varieties", blank=True, help_text=LINES_HELP)
    specs_text = models.TextField("Specifications", blank=True, help_text="One per line as: Label | Value   (e.g. Moisture | Within export norms)")
    packing_text = models.TextField("Packing options", blank=True, help_text=LINES_HELP)
    uses_text = models.TextField("Typical uses", blank=True, help_text=LINES_HELP)
    season_months = models.CharField("Sourcing season", max_length=40, blank=True, help_text="Months the product is sourced.")
    order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return self.image.url if self.image else ""

    @property
    def bg_url(self):
        return self.banner.url if self.banner else self.image_url

    @property
    def about(self):
        return _paras(self.about_text)

    @property
    def varieties(self):
        return _lines(self.varieties_text)

    @property
    def specs(self):
        return _pairs(self.specs_text)

    @property
    def packing(self):
        return _lines(self.packing_text)

    @property
    def uses(self):
        return _lines(self.uses_text)

    @property
    def season(self):
        return [int(m) for m in self.season_months.split(",") if m.strip().isdigit()]

    @property
    def season_cells(self):
        on = set(self.season)
        return [{"m": m, "on": (i + 1) in on} for i, m in enumerate(MONTHS)]


# ---------------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------------
class Service(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, validators=[slug_validator])
    icon = models.CharField(max_length=40, default="bi-gear", help_text=ICON_HELP)
    image = models.ImageField(upload_to="services/", help_text="Landscape photo, about 1200x800.")
    banner = models.ImageField(upload_to="services/banners/", blank=True, help_text="Optional wide page-header banner (1920x900).")
    summary = models.TextField()
    lead = models.TextField("Opening line", help_text="Shown under the page title.")
    body_text = models.TextField("Description", help_text="Separate paragraphs with a blank line.")
    includes_text = models.TextField("What is included", blank=True, help_text=LINES_HELP)
    outcomes_text = models.TextField("Outcomes", blank=True, help_text="One per line as: Title | Detail")
    order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    @property
    def image_url(self):
        return self.image.url if self.image else ""

    @property
    def bg_url(self):
        return self.banner.url if self.banner else self.image_url

    @property
    def body(self):
        return _paras(self.body_text)

    @property
    def includes(self):
        return _lines(self.includes_text)

    @property
    def outcomes(self):
        return _pairs(self.outcomes_text)


# ---------------------------------------------------------------------------
# Insights (articles)
# ---------------------------------------------------------------------------
class Insight(models.Model):
    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True, validators=[slug_validator])
    tag = models.CharField(max_length=60, blank=True)
    read_minutes = models.PositiveSmallIntegerField(default=3)
    image = models.ImageField(upload_to="insights/", help_text="Landscape photo, about 1200x800.")
    excerpt = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name = "insight (article)"
        verbose_name_plural = "insights (articles)"

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        return self.image.url if self.image else ""

    @property
    def body(self):
        return [(s.heading, s.text) for s in self.sections.all()]


class InsightSection(models.Model):
    insight = models.ForeignKey(Insight, on_delete=models.CASCADE, related_name="sections")
    heading = models.CharField(max_length=160)
    text = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.heading


# ---------------------------------------------------------------------------
# Markets, shipping terms, FAQs
# ---------------------------------------------------------------------------
class Region(models.Model):
    name = models.CharField(max_length=100)
    note = models.TextField("Description")
    icon = models.CharField(max_length=40, default="bi-globe2", help_text=ICON_HELP)
    products_text = models.TextField("Products", blank=True, help_text=LINES_HELP)
    order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    @property
    def products(self):
        return _lines(self.products_text)


class Incoterm(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=80)
    description = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "code"]
        verbose_name = "shipping term"

    def __str__(self):
        return f"{self.code} – {self.name}"


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


# ---------------------------------------------------------------------------
# Small repeated lists (mission, strengths, process ...). One table, shown
# in the admin as separate sections through proxy models.
# ---------------------------------------------------------------------------
class ContentItem(models.Model):
    MISSION, STRENGTH, WHY, PROCESS, QUALITY, DOC = "mission", "strength", "why", "process", "quality", "doc"
    GROUPS = [(MISSION, "Mission point"), (STRENGTH, "Strength"), (WHY, "Why choose us"),
              (PROCESS, "Process step"), (QUALITY, "Quality checkpoint"), (DOC, "Document")]

    group = models.CharField(max_length=12, choices=GROUPS, db_index=True)
    title = models.CharField(max_length=160, blank=True)
    text = models.TextField(blank=True)
    icon = models.CharField(max_length=40, blank=True, help_text=ICON_HELP)
    order = models.PositiveSmallIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["group", "order", "id"]

    def __str__(self):
        return self.title or self.text[:60]


class _GroupManager(models.Manager):
    group = None

    def get_queryset(self):
        return super().get_queryset().filter(group=self.group)


def _group_proxy(cls_name, group, verbose, plural):
    mgr = type(cls_name + "Manager", (_GroupManager,), {"group": group})

    def save(self, *args, **kwargs):
        self.group = group
        super(proxy, self).save(*args, **kwargs)

    meta = type("Meta", (), {"proxy": True, "verbose_name": verbose, "verbose_name_plural": plural, "app_label": "core"})
    proxy = type(cls_name, (ContentItem,), {"__module__": __name__, "Meta": meta, "objects": mgr(), "save": save})
    return proxy


MissionPoint = _group_proxy("MissionPoint", ContentItem.MISSION, "mission point", "Mission points")
Strength = _group_proxy("Strength", ContentItem.STRENGTH, "strength", "Strengths")
WhyPoint = _group_proxy("WhyPoint", ContentItem.WHY, "why-choose-us point", "Why choose us points")
ProcessStep = _group_proxy("ProcessStep", ContentItem.PROCESS, "process step", "Process steps")
QualityStage = _group_proxy("QualityStage", ContentItem.QUALITY, "quality checkpoint", "Quality checkpoints")
DocumentItem = _group_proxy("DocumentItem", ContentItem.DOC, "export document", "Export documents")


# ---------------------------------------------------------------------------
# Legal / long-text pages
# ---------------------------------------------------------------------------
class Page(models.Model):
    PRIVACY, TERMS = "privacy", "terms"
    KEYS = [(PRIVACY, "Privacy policy"), (TERMS, "Terms of use")]

    key = models.CharField(max_length=20, choices=KEYS, unique=True)
    title = models.CharField(max_length=120)
    accent = models.CharField("Title (gold part)", max_length=60, blank=True)
    subtitle = models.CharField(max_length=200, blank=True)
    body = models.TextField(help_text="Start a heading with '## '. Separate paragraphs with a blank line. Links: [text](https://...)")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "legal page"
        verbose_name_plural = "legal pages"

    def __str__(self):
        return self.get_key_display()
