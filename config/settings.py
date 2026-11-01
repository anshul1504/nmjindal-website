"""
Django settings for the NM Jindal Global website.

Local development works with no configuration. On the server, put the secrets
in a `.env` file next to manage.py (see `.env.example`); it is never committed.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_env_file(path):
    """Tiny KEY=VALUE loader so no extra package is needed."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_env_file(BASE_DIR / ".env")


def env(name, default=""):
    return os.environ.get(name, default)


def env_list(name, default=""):
    return [x.strip() for x in env(name, default).split(",") if x.strip()]


DEBUG = env("DJANGO_DEBUG", "1") == "1"

SECRET_KEY = env("DJANGO_SECRET_KEY") or "django-insecure-dev-only-key-change-in-production"
if not DEBUG and SECRET_KEY.startswith("django-insecure"):
    raise RuntimeError("Set DJANGO_SECRET_KEY in .env before running with DJANGO_DEBUG=0.")

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "[::1]"] + env_list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")


INSTALLED_APPS = [
    "jazzmin",
    "core",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_info",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": env("DJANGO_DB_PATH") or BASE_DIR / "db.sqlite3",
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
USE_I18N = True
USE_TZ = True

# Static and uploaded (media) files
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}
MEDIA_URL = "/media/"
MEDIA_ROOT = Path(env("DJANGO_MEDIA_ROOT") or BASE_DIR / "media")
DATA_UPLOAD_MAX_MEMORY_SIZE = 15 * 1024 * 1024
FILE_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email (enquiry notifications). Console backend until SMTP details are set in .env.
EMAIL_BACKEND = env("DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = int(env("EMAIL_PORT", "587") or 587)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = env("EMAIL_USE_SSL", "0") == "1"          # port 465
EMAIL_USE_TLS = env("EMAIL_USE_TLS", "0" if EMAIL_USE_SSL else "1") == "1"  # port 587
EMAIL_TIMEOUT = 12
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL") or EMAIL_HOST_USER or "noreply@localhost"

# Production hardening (only when DEBUG is off)
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"
    if env("DJANGO_HTTPS", "0") == "1":
        # The http -> https redirect itself is done in .htaccess on the server.
        SESSION_COOKIE_SECURE = True
        CSRF_COOKIE_SECURE = True
        SECURE_HSTS_SECONDS = 3600
    LOGGING = {
        "version": 1, "disable_existing_loggers": False,
        "handlers": {"file": {"class": "logging.FileHandler", "filename": str(BASE_DIR / "django-errors.log")}},
        "loggers": {"django": {"handlers": ["file"], "level": "WARNING", "propagate": True}},
    }

# ---------------------------------------------------------------------------
# Admin look (django-jazzmin)
# ---------------------------------------------------------------------------
JAZZMIN_SETTINGS = {
    "site_title": "NM Jindal Global",
    "site_header": "NM Jindal Global",
    "site_brand": "NM Jindal Global",
    "site_logo": "core/img/logo-mark.png",
    "login_logo": "core/img/logo.png",
    "login_logo_dark": "core/img/logo.png",
    "site_icon": "core/img/logo-mark.png",
    "welcome_sign": "Sign in to manage your website",
    "copyright": "NM Jindal Global",
    "search_model": ["core.Product", "core.Enquiry"],
    "topmenu_links": [
        {"name": "View website", "url": "/", "new_window": True, "icon": "fas fa-globe"},
        {"name": "Enquiries", "model": "core.Enquiry"},
        {"name": "Site settings", "url": "admin:core_sitesettings_changelist", "permissions": ["core.change_sitesettings"]},
    ],
    "usermenu_links": [{"name": "View website", "url": "/", "new_window": True, "icon": "fas fa-globe"}],
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_models": ["core.ContentItem"],
    "order_with_respect_to": [
        "core.Enquiry", "core.SiteSettings", "core.HeroSlide",
        "core.Product", "core.ProductCategory", "core.Service", "core.Insight",
        "core.Region", "core.Incoterm", "core.FAQ",
        "core.MissionPoint", "core.Strength", "core.WhyPoint", "core.ProcessStep", "core.QualityStage", "core.DocumentItem",
        "core.Page", "auth",
    ],
    "icons": {
        "auth": "fas fa-users-cog", "auth.user": "fas fa-user", "auth.Group": "fas fa-users",
        "core.Enquiry": "fas fa-envelope-open-text", "core.SiteSettings": "fas fa-sliders-h",
        "core.HeroSlide": "fas fa-images", "core.Product": "fas fa-seedling", "core.ProductCategory": "fas fa-tags",
        "core.Service": "fas fa-concierge-bell", "core.Insight": "fas fa-newspaper",
        "core.Region": "fas fa-globe-asia", "core.Incoterm": "fas fa-ship", "core.FAQ": "fas fa-question-circle",
        "core.MissionPoint": "fas fa-bullseye", "core.Strength": "fas fa-dumbbell", "core.WhyPoint": "fas fa-check-circle",
        "core.ProcessStep": "fas fa-stream", "core.QualityStage": "fas fa-clipboard-check", "core.DocumentItem": "fas fa-file-alt",
        "core.Page": "fas fa-file-contract",
    },
    "default_icon_parents": "fas fa-folder",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": True,
    "custom_css": "core/css/admin.css",
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {"core.sitesettings": "collapsible", "core.insight": "collapsible"},
    "show_ui_builder": False,
}

JAZZMIN_UI_TWEAKS = {
    "theme": "darkly",
    "default_theme_mode": "dark",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "sidebar": "sidebar-dark-warning",
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "button_classes": {
        "primary": "btn-warning", "secondary": "btn-outline-secondary", "info": "btn-outline-info",
        "warning": "btn-warning", "danger": "btn-danger", "success": "btn-success",
    },
    "sidebar_nav_small_text": False,
    "sidebar_nav_flat_style": True,
    "sidebar_nav_child_indent": True,
    "actions_sticky_top": True,
}
