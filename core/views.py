from django.contrib import messages
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .emails import send_enquiry_emails
from .forms import EnquiryForm
from .models import (FAQ, MONTHS, ContentItem, HeroSlide, Incoterm, Insight, Page, Product, ProductCategory, Region,
                     Service, SiteSettings)


def _group(group):
    return list(ContentItem.objects.filter(group=group, active=True))


def _ctx(**extra):
    base = {
        "services": list(Service.objects.filter(active=True)),
        "products": list(Product.objects.filter(active=True).select_related("category")),
        "insights": list(Insight.objects.filter(published=True).prefetch_related("sections")),
        "faqs": [(f.question, f.answer) for f in FAQ.objects.filter(active=True)],
        "mission": [m.text for m in _group(ContentItem.MISSION)],
        "strengths": [(s.title, s.text) for s in _group(ContentItem.STRENGTH)],
        "why_us": [w.text for w in _group(ContentItem.WHY)],
        "process": [(p.title, p.text) for p in _group(ContentItem.PROCESS)],
        "hero_slides": list(HeroSlide.objects.filter(active=True)),
    }
    base.update(extra)
    return base


def home(request):
    return render(request, "core/home.html", _ctx())


def products(request):
    ctx = _ctx()
    cal_rows = [{"name": p.name, "cal": p.season_cells} for p in ctx["products"]]
    used = {p.category_id for p in ctx["products"]}
    categories = [c.name for c in ProductCategory.objects.all() if c.pk in used]
    return render(request, "core/products.html", dict(ctx, categories=categories, cal_rows=cal_rows, months_all=MONTHS))


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug, active=True)
    ctx = _ctx()
    others = [p for p in ctx["products"] if p.pk != product.pk]
    same = [p for p in others if p.category_id == product.category_id]
    related = (same + [p for p in others if p not in same])[:3]
    return render(request, "core/product_detail.html", dict(ctx, product=product, related=related, season=product.season_cells, months=MONTHS))


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug, active=True)
    ctx = _ctx()
    return render(request, "core/service_detail.html", dict(ctx, service=service, others=[s for s in ctx["services"] if s.pk != service.pk]))


def markets(request):
    regions = Region.objects.filter(active=True)
    incoterms = [(i.code, i.name, i.description) for i in Incoterm.objects.filter(active=True)]
    return render(request, "core/markets.html", _ctx(regions=regions, incoterms=incoterms))


def quality(request):
    stages = [(s.title, s.text, s.icon) for s in _group(ContentItem.QUALITY)]
    docs = [(d.icon, d.title) for d in _group(ContentItem.DOC)]
    return render(request, "core/quality.html", _ctx(stages=stages, docs=docs))


def insights(request):
    return render(request, "core/insights.html", _ctx())


def insight_detail(request, slug):
    article = get_object_or_404(Insight.objects.prefetch_related("sections"), slug=slug, published=True)
    ctx = _ctx()
    return render(request, "core/insight_detail.html", dict(ctx, article=article, more=[a for a in ctx["insights"] if a.pk != article.pk][:3]))


def robots(request):
    lines = ["User-agent: *", "Allow: /", "Disallow: /admin/", "Sitemap: " + request.build_absolute_uri("/sitemap.xml"), ""]
    return HttpResponse(chr(10).join(lines), content_type="text/plain")


def sitemap(request):
    paths = [reverse(n) for n in ("home", "about", "trade", "products", "services", "markets", "quality", "insights", "why", "contact", "privacy", "terms")]
    paths += [reverse("product_detail", args=[p.slug]) for p in Product.objects.filter(active=True)]
    paths += [reverse("service_detail", args=[s.slug]) for s in Service.objects.filter(active=True)]
    paths += [reverse("insight_detail", args=[a.slug]) for a in Insight.objects.filter(published=True)]
    urls = "".join(f"<url><loc>{request.build_absolute_uri(p)}</loc></url>" for p in paths)
    xml = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return HttpResponse(xml, content_type="application/xml")


def about(request):
    return render(request, "core/about.html", _ctx())


def trade(request):
    return render(request, "core/trade.html", _ctx())


def services(request):
    return render(request, "core/services.html", _ctx())


def why_us(request):
    return render(request, "core/why.html", _ctx())


def _legal(request, key):
    page = get_object_or_404(Page, key=key)
    return render(request, "core/legal.html", _ctx(page=page))


def privacy(request):
    return _legal(request, Page.PRIVACY)


def terms(request):
    return _legal(request, Page.TERMS)


def contact(request):
    if request.method == "POST":
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            send_enquiry_emails(enquiry, request)
            messages.success(request, "Thank you. Your enquiry has been received and our team will respond shortly.")
            return redirect("contact")
        messages.error(request, "Please check the highlighted fields and try again.")
    else:
        initial = {}
        item = (Product.objects.filter(slug=request.GET.get("product", ""), active=True).first()
                or Service.objects.filter(slug=request.GET.get("service", ""), active=True).first())
        if item:
            nl = chr(10)
            initial["message"] = nl.join([f"I'd like a quote for {item.name}.", "", "Quantity:", "Destination port / country:", "Target timeline:", ""])
            if request.GET.get("product"):
                initial["interest"] = "export"
        form = EnquiryForm(initial=initial)
    return render(request, "core/contact.html", _ctx(form=form))
