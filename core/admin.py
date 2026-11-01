from django import forms
from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.html import format_html

from .models import (FAQ, DocumentItem, Enquiry, HeroSlide, Incoterm, Insight, InsightSection, MissionPoint, MONTHS, Page,
                     ProcessStep, Product, ProductCategory, QualityStage, Region, Service, SiteSettings, Strength, WhyPoint)

admin.site.site_header = "NM Jindal Global"
admin.site.site_title = "NM Jindal Global admin"
admin.site.index_title = "Manage your website"


def _thumb(obj, field="image", w=64):
    f = getattr(obj, field, None)
    if f:
        return format_html('<img src="{}" style="width:{}px;height:{}px;object-fit:cover;border-radius:8px">', f.url, w, int(w * .75))
    return "-"


class ThumbMixin:
    @admin.display(description="Photo")
    def thumb(self, obj):
        return _thumb(obj)


# ---------------------------------------------------------------------------
@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "email", "phone", "interest", "created_at", "handled")
    list_filter = ("handled", "interest", "created_at")
    list_editable = ("handled",)
    search_fields = ("name", "company", "email", "phone", "message")
    readonly_fields = ("name", "company", "email", "phone", "interest", "message", "created_at")
    date_hierarchy = "created_at"
    actions = ["mark_handled", "mark_open"]

    def has_add_permission(self, request):
        return False

    @admin.action(description="Mark selected enquiries as handled")
    def mark_handled(self, request, queryset):
        self.message_user(request, f"{queryset.update(handled=True)} enquiries marked as handled.")

    @admin.action(description="Mark selected enquiries as open")
    def mark_open(self, request, queryset):
        self.message_user(request, f"{queryset.update(handled=False)} enquiries re-opened.")


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Company", {"fields": ("company_name", "tagline", "footer_blurb", "meta_description")}),
        ("Contact details", {"description": "Shown in the footer, contact page and enquiry form. Empty fields are hidden. The phone number also drives the WhatsApp button.",
                             "fields": ("address", "phone", "email", "email2", "website", "notify_email")}),
        ("Home page hero", {"fields": ("hero_title_plain", "hero_title_gold", "hero_roll_prefix", "hero_roll_words", "hero_lead")}),
        ("Home page intro", {"fields": ("intro_heading", "intro_heading_gold", "intro_text")}),
        ("About us", {"fields": ("about_text", "vision_text")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        return HttpResponseRedirect(reverse("admin:core_sitesettings_change", args=[obj.pk]))


@admin.register(HeroSlide)
class HeroSlideAdmin(ThumbMixin, admin.ModelAdmin):
    list_display = ("thumb", "caption", "order", "active")
    list_editable = ("order", "active")


# ---------------------------------------------------------------------------
class ProductForm(forms.ModelForm):
    season = forms.MultipleChoiceField(
        label="Sourcing season", required=False, widget=forms.CheckboxSelectMultiple,
        choices=[(str(i + 1), m) for i, m in enumerate(MONTHS)], help_text="Tick the months this product is sourced.")

    class Meta:
        model = Product
        exclude = ("season_months",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["season"].initial = [str(m) for m in self.instance.season]

    def save(self, commit=True):
        self.instance.season_months = ",".join(sorted(self.cleaned_data.get("season", []), key=int))
        return super().save(commit)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)


@admin.register(Product)
class ProductAdmin(ThumbMixin, admin.ModelAdmin):
    form = ProductForm
    list_display = ("thumb", "name", "category", "order", "active")
    list_editable = ("order", "active")
    list_filter = ("category", "active")
    search_fields = ("name", "kicker", "summary")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Basics", {"fields": ("name", "slug", "kicker", "category", "icon", "order", "active")}),
        ("Photos", {"fields": ("image", "banner")}),
        ("Description", {"fields": ("summary", "about_text")}),
        ("Details", {"fields": ("varieties_text", "specs_text", "packing_text", "uses_text", "season")}),
    )


@admin.register(Service)
class ServiceAdmin(ThumbMixin, admin.ModelAdmin):
    list_display = ("thumb", "name", "order", "active")
    list_editable = ("order", "active")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        ("Basics", {"fields": ("name", "slug", "icon", "order", "active")}),
        ("Photos", {"fields": ("image", "banner")}),
        ("Content", {"fields": ("summary", "lead", "body_text", "includes_text", "outcomes_text")}),
    )


class InsightSectionInline(admin.StackedInline):
    model = InsightSection
    extra = 1
    fields = ("heading", "text", "order")


@admin.register(Insight)
class InsightAdmin(ThumbMixin, admin.ModelAdmin):
    list_display = ("thumb", "title", "tag", "read_minutes", "order", "published")
    list_editable = ("order", "published")
    list_filter = ("published", "tag")
    search_fields = ("title", "excerpt")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [InsightSectionInline]
    fields = ("title", "slug", "tag", "read_minutes", "image", "excerpt", "order", "published")


# ---------------------------------------------------------------------------
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "active")
    list_editable = ("order", "active")


@admin.register(Incoterm)
class IncotermAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "order", "active")
    list_editable = ("order", "active")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order", "active")
    list_editable = ("order", "active")
    search_fields = ("question", "answer")


class _ItemAdmin(admin.ModelAdmin):
    list_display = ("__str__", "order", "active")
    list_editable = ("order", "active")


@admin.register(MissionPoint)
class MissionPointAdmin(_ItemAdmin):
    fields = ("text", "order", "active")


@admin.register(WhyPoint)
class WhyPointAdmin(_ItemAdmin):
    fields = ("text", "order", "active")


@admin.register(Strength)
class StrengthAdmin(_ItemAdmin):
    fields = ("title", "text", "order", "active")


@admin.register(ProcessStep)
class ProcessStepAdmin(_ItemAdmin):
    fields = ("title", "text", "order", "active")


@admin.register(QualityStage)
class QualityStageAdmin(_ItemAdmin):
    fields = ("title", "text", "icon", "order", "active")


@admin.register(DocumentItem)
class DocumentItemAdmin(_ItemAdmin):
    fields = ("title", "icon", "order", "active")


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("key", "title", "updated_at")
    fields = ("key", "title", "accent", "subtitle", "body")
