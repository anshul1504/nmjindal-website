from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("what-we-trade/", views.trade, name="trade"),
    path("products/", views.products, name="products"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("services/", views.services, name="services"),
    path("services/<slug:slug>/", views.service_detail, name="service_detail"),
    path("markets/", views.markets, name="markets"),
    path("quality/", views.quality, name="quality"),
    path("insights/", views.insights, name="insights"),
    path("insights/<slug:slug>/", views.insight_detail, name="insight_detail"),
    path("robots.txt", views.robots),
    path("sitemap.xml", views.sitemap),
    path("why-choose-us/", views.why_us, name="why"),
    path("contact/", views.contact, name="contact"),
    path("privacy/", views.privacy, name="privacy"),
    path("terms/", views.terms, name="terms"),
]
