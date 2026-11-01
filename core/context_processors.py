import re

from .models import SiteSettings


def site_info(request):
    site = SiteSettings.load()
    digits = re.sub(r"\D", "", site.phone or "")
    contact = {
        "address": site.address, "phone": site.phone, "email": site.email, "email2": site.email2, "website": site.website,
        "whatsapp_url": f"https://wa.me/{digits}" if digits else "",
        "tel_url": f"tel:+{digits}" if digits else "",
    }
    contact["has_any"] = any(contact[k] for k in ("address", "phone", "email", "email2", "website"))
    return {"site": site, "contact": contact}
