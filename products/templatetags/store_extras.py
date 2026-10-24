from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

register = template.Library()

BULLET_PREFIXES = ('• ', '- ', '* ')


@register.filter(name='format_description')
def format_description(value):
    """Render plain-text product copy as paragraphs, short headings and bullet lists.

    A short line directly followed by bullet lines (e.g. "Highlights") becomes a
    heading. All text is escaped, so this is safe for admin-entered content.
    """
    lines = [line.strip() for line in str(value or '').splitlines()]
    html = []
    bullets = []

    def flush_bullets():
        if bullets:
            html.append('<ul>' + ''.join(f'<li>{escape(item)}</li>' for item in bullets) + '</ul>')
            bullets.clear()

    for index, line in enumerate(lines):
        if not line:
            flush_bullets()
            continue
        if line.startswith(BULLET_PREFIXES):
            bullets.append(line[2:].strip())
            continue
        flush_bullets()
        next_line = lines[index + 1] if index + 1 < len(lines) else ''
        if len(line) <= 40 and next_line.startswith(BULLET_PREFIXES):
            html.append(f'<h3>{escape(line)}</h3>')
        else:
            html.append(f'<p>{escape(line)}</p>')
    flush_bullets()
    return mark_safe(''.join(html))


@register.filter(name='description_summary')
def description_summary(value):
    """Return the first paragraph of the description, without bullets or headings."""
    for line in str(value or '').splitlines():
        line = line.strip()
        if line and not line.startswith(BULLET_PREFIXES) and line.lower() != 'product overview':
            return line
    return ''


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """Rebuild the current query string with some parameters replaced (used by pagination)."""
    params = context['request'].GET.copy()
    for key, val in kwargs.items():
        if val in (None, ''):
            params.pop(key, None)
        else:
            params[key] = val
    return params.urlencode()
