import re
from urllib.parse import quote

from django.conf import settings

SOCIAL_META = [
    ('facebook', 'Facebook', 'bi-facebook'),
    ('instagram', 'Instagram', 'bi-instagram'),
    ('tiktok', 'TikTok', 'bi-tiktok'),
    ('x', 'X (Twitter)', 'bi-twitter-x'),
    ('youtube', 'YouTube', 'bi-youtube'),
    ('linkedin', 'LinkedIn', 'bi-linkedin'),
]


def _whatsapp_chat():
    """Return (display number, wa.me chat URL) for the configured WhatsApp Business number."""
    digits = re.sub(r'\D', '', getattr(settings, 'WHATSAPP_NUMBER', '') or '')
    if digits.startswith('0') and len(digits) == 11:  # local Nigerian format 080...
        digits = '234' + digits[1:]
    if len(digits) < 10:
        return '', ''
    display = f'+{digits[:3]} {digits[3:6]} {digits[6:9]} {digits[9:]}' if digits.startswith('234') else f'+{digits}'
    url = f"https://wa.me/{digits}?text={quote('Hello RedCart, I need help with')}"
    return display, url


def cart_context(request):
    cart = request.session.get('cart', {}) if request else {}
    total_quantity = 0

    if isinstance(cart, dict):
        for item_data in cart.values():
            if isinstance(item_data, dict):
                quantity = item_data.get('quantity', 1)
            else:
                try:
                    quantity = int(item_data)
                except (TypeError, ValueError):
                    quantity = 1

            total_quantity += max(0, int(quantity))

    links = getattr(settings, 'SOCIAL_LINKS', {}) or {}
    social_links = [
        {'key': key, 'label': label, 'icon': icon, 'url': links[key]}
        for key, label, icon in SOCIAL_META
        if links.get(key)
    ]
    whatsapp_display, whatsapp_chat_url = _whatsapp_chat()

    return {
        'cart_item_count': total_quantity,
        'whatsapp_channel_url': getattr(settings, 'WHATSAPP_CHANNEL_URL', ''),
        'whatsapp_number_display': whatsapp_display,
        'whatsapp_chat_url': whatsapp_chat_url,
        'social_links': social_links,
        'support_email': getattr(settings, 'SUPPORT_EMAIL', ''),
    }
