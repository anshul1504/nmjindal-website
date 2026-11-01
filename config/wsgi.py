"""WSGI config. Also serves uploaded media files (WhiteNoise handles static files)."""

import os

from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()

if not settings.DEBUG:
    from whitenoise import WhiteNoise

    settings.MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    application = WhiteNoise(application, root=str(settings.MEDIA_ROOT), prefix="media/", autorefresh=True)
