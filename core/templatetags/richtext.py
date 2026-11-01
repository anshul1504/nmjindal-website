import re

from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+|/[^\s)]*|mailto:[^\s)]+)\)")


def _inline(text):
    return _LINK.sub(lambda m: '<a href="%s">%s</a>' % (m.group(2), m.group(1)), escape(text))


@register.filter
def richtext(value):
    """Admin-authored text: '## Heading', blank-line paragraphs and [links](url). Everything else is escaped."""
    out = []
    for block in re.split(r"\n\s*\n", (value or "").replace("\r", "").strip()):
        block = block.strip()
        if not block:
            continue
        if block.startswith("## "):
            head, _, rest = block.partition("\n")
            out.append("<h2>%s</h2>" % _inline(head[3:].strip()))
            block = rest.strip()
            if not block:
                continue
        out.append("<p>%s</p>" % _inline(block).replace("\n", "<br>"))
    return mark_safe("".join(out))
