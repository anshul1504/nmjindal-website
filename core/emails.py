"""Enquiry emails: one to the team, one acknowledgement to the person who wrote in."""
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import SiteSettings

log = logging.getLogger(__name__)


def _send(subject, template, ctx, to, reply_to=None):
    text = render_to_string(f"core/email/{template}.txt", ctx)
    html = render_to_string(f"core/email/{template}.html", ctx)
    sender = f"{ctx['site'].company_name} <{settings.DEFAULT_FROM_EMAIL}>"
    msg = EmailMultiAlternatives(subject, text, sender, to, reply_to=reply_to or [])
    msg.attach_alternative(html, "text/html")
    msg.send()


def send_enquiry_emails(enquiry, request):
    """Never raises: a mail problem must not lose the enquiry (it is already saved)."""
    site = SiteSettings.load()
    base = request.build_absolute_uri("/")
    ctx = {"enquiry": enquiry, "site": site, "base": base,
           "admin_url": request.build_absolute_uri(f"/admin/core/enquiry/{enquiry.pk}/change/"),
           "wa": "".join(ch for ch in site.phone if ch.isdigit())}
    ref = f"NMJ-{enquiry.pk:05d}"
    ctx["ref"] = ref

    if site.notify_email:
        try:
            _send(f"New enquiry {ref}: {enquiry.name} ({enquiry.get_interest_display()})", "enquiry_team", ctx,
                  [site.notify_email], reply_to=[f"{enquiry.name} <{enquiry.email}>"])
        except Exception:
            log.exception("Could not send the team notification for enquiry %s", enquiry.pk)

    try:
        _send(f"We have received your enquiry ({ref}) | {site.company_name}", "enquiry_thanks", ctx, [enquiry.email],
              reply_to=[site.email or settings.DEFAULT_FROM_EMAIL])
    except Exception:
        log.exception("Could not send the acknowledgement for enquiry %s", enquiry.pk)
