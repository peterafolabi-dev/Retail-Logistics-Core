"""
Utility functions for RedCart e-commerce
"""
import json
import os
import re
import requests
from urllib.parse import quote
import time
from functools import wraps

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags
from .models import EmailLog, EmailTemplate, Product
import logging

logger = logging.getLogger(__name__)

# Simple in-memory cache for AI responses
_AI_RESPONSE_CACHE = {}
_CATALOG_CACHE = None
_CATALOG_CACHE_TIME = 0
CATALOG_CACHE_TTL = 300  # 5 minutes


# ============ EMAIL UTILITIES ============

def send_email(user, email_type, context=None, recipient_email=None):
    """
    Send email using templates

    Args:
        user: User object
        email_type: Type of email (e.g., 'order_confirmation')
        context: Dictionary with template context
        recipient_email: Override recipient email (default: user.email)
    """
    if context is None:
        context = {}

    try:
        template = EmailTemplate.objects.filter(email_type=email_type, is_active=True).first()
        if not template:
            logger.warning(f"Email template not found: {email_type}")
            return False

        recipient = recipient_email or user.email

        context['user'] = user
        context['site_name'] = 'RedCart'

        html_message = render_to_string(f'emails/{email_type}.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=template.subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            html_message=html_message,
            fail_silently=False,
        )

        if user is not None:
            EmailLog.objects.create(
                user=user,
                email_type=email_type,
                recipient=recipient,
                subject=template.subject,
                status='sent'
            )

        logger.info(f"Email sent: {email_type} to {recipient}")
        return True

    except Exception as e:
        logger.error(f"Error sending email {email_type}: {str(e)}")

        if user is not None:
            EmailLog.objects.create(
                user=user,
                email_type=email_type,
                recipient=recipient_email or user.email,
                subject='',
                status='failed'
            )
        return False


def send_newsletter_confirmation_email(email):
    """Send a confirmation email to a new newsletter subscriber."""
    try:
        from django.core.mail import send_mail
        from django.conf import settings

        # Try to use template first, if it doesn't exist, use simple HTML
        template = None
        try:
            template = EmailTemplate.objects.filter(email_type='newsletter', is_active=True).first()
        except:
            pass

        unsubscribe_url = f"{settings.SITE_URL.rstrip('/')}/products/newsletter/unsubscribe/?email={quote(email)}"

        if template:
            context = {
                'email': email,
                'site_name': 'RedCart',
                'unsubscribe_url': unsubscribe_url,
            }
            html_message = render_to_string('emails/newsletter.html', context)
            plain_message = strip_tags(html_message)
            subject = template.subject
        else:
            # Fallback HTML if template doesn't exist
            html_message = f'''
            <h2>Welcome to RedCart Newsletter!</h2>
            <p>Hi {email},</p>
            <p>Thank you for subscribing to our newsletter. You'll now receive updates about new products, special offers, and exclusive deals.</p>
            <hr>
            <p><a href="{unsubscribe_url}">Unsubscribe from newsletter</a></p>
            '''
            plain_message = f'Welcome to RedCart Newsletter!\n\nThank you for subscribing. Unsubscribe: {unsubscribe_url}'
            subject = '📧 Welcome to RedCart Newsletter'

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

        logger.info(f"Newsletter confirmation email sent to {email}")
        print(f'NEWSLETTER EMAIL SENT: {email} via {settings.EMAIL_HOST}')
        return True
    except Exception as e:
        error_msg = f"Error sending newsletter confirmation email to {email}: {str(e)}"
        logger.error(error_msg)
        print(f'NEWSLETTER EMAIL ERROR: {error_msg}')  # Also print to console
        raise  # Re-raise so view can handle it


def send_order_confirmation_email(order):
    """Send order confirmation email"""
    context = {
        'order': order,
        'items': order.items.all(),
        'total': order.total,
    }
    return send_email(order.user, 'order_confirmation', context)


def send_order_shipped_email(order):
    """Send order shipped notification"""
    context = {
        'order': order,
        'tracking_number': order.tracking_number,
    }
    return send_email(order.user, 'order_shipped', context)


def send_order_delivered_email(order):
    """Send order delivered notification"""
    context = {'order': order}
    return send_email(order.user, 'order_delivered', context)


def send_welcome_email(user):
    """Send welcome email to new user"""
    context = {'username': user.username}
    return send_email(user, 'welcome', context)


def send_contact_reply_email(contact_submission, reply_message):
    """Send reply to contact form submission"""
    context = {
        'name': contact_submission.name,
        'subject': contact_submission.subject,
        'reply': reply_message,
    }
    return send_email(
        user=None,
        email_type='contact_reply',
        context=context,
        recipient_email=contact_submission.email
    )


# ============ INVENTORY UTILITIES ============

def update_stock(product, quantity, reason='adjustment'):
    """
    Update product stock with tracking

    Args:
        product: Product instance
        quantity: Amount to change (positive or negative)
        reason: Reason for change ('sale', 'return', 'restock', 'adjustment')
    """
    from .models import InventoryLog

    if product.stock_quantity is not None:
        product.stock_quantity += quantity
    else:
        product.stock += quantity

    product.save()

    InventoryLog.objects.create(
        product=product,
        quantity_changed=quantity,
        reason=reason
    )

    logger.info(f"Stock updated for {product.name}: {quantity} ({reason})")

    if product.available_stock < 5:
        logger.warning(f"Low stock alert for {product.name}: {product.available_stock} remaining")

    return product


def check_stock_availability(product, quantity, variant=None):
    """Check if sufficient stock is available"""
    if variant:
        return variant.stock >= quantity
    return product.stock >= quantity


# ============ ORDER UTILITIES ============

def generate_tracking_number(order_id):
    """Generate a tracking number for an order"""
    import uuid
    return f"RC-{order_id}-{str(uuid.uuid4())[:8].upper()}"


def calculate_tax(subtotal, tax_rate=0.075):
    """Calculate tax on order (7.5% for Nigeria)"""
    return round(subtotal * tax_rate, 2)


def apply_discount_code(code, subtotal):
    """
    Apply discount code and return discount amount

    Returns:
        (discount_amount, error_message) tuple
    """
    from .models import DiscountCode

    try:
        discount = DiscountCode.objects.get(code__iexact=code)

        if not discount.is_valid:
            return 0, "This discount code is no longer valid"

        if subtotal < discount.min_purchase:
            return 0, f"Minimum purchase of ₦{discount.min_purchase:,.2f} required"

        if discount.discount_type == 'percentage':
            discount_amount = subtotal * (discount.discount_value / 100)
        else:
            discount_amount = discount.discount_value

        discount_amount = min(discount_amount, subtotal)

        return discount_amount, None

    except DiscountCode.DoesNotExist:
        return 0, "Invalid discount code"


# ============ RECOMMENDATION UTILITIES ============

def get_product_recommendations(product, limit=4):
    """Get recommended products for a given product"""
    from .models import ProductRecommendation

    try:
        recommendation = ProductRecommendation.objects.get(product=product)
        return recommendation.frequently_bought_with.all()[:limit]
    except ProductRecommendation.DoesNotExist:
        return Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:limit]


# ============ AI UTILITIES (Groq) ============

def _get_cached_catalog():
    """Get all products with caching to reduce database queries."""
    global _CATALOG_CACHE, _CATALOG_CACHE_TIME
    current_time = time.time()

    if _CATALOG_CACHE is not None and (current_time - _CATALOG_CACHE_TIME) < CATALOG_CACHE_TTL:
        return _CATALOG_CACHE

    # Build lightweight product inventory (name, price, category)
    products = Product.objects.all().values('id', 'name', 'price', 'category', 'description').order_by('category', 'name')
    catalog = [
        f"{p['name']} (Category: {p['category']}) — ₦{p['price']:,.0f}"
        for p in products
    ]

    _CATALOG_CACHE = catalog
    _CATALOG_CACHE_TIME = current_time
    return catalog


def _get_groq_api_key():
    """Return the configured Groq API key from Django settings or environment."""
    api_key = (
        getattr(settings, 'GROQ_API_KEY', '')
        or os.environ.get('GROQ_API_KEY', '')
        or getattr(settings, 'GROK_API_KEY', '')
        or os.environ.get('GROK_API_KEY', '')
    )
    return (api_key or '').strip()


def _call_groq(prompt=None, messages=None, max_tokens=250, retries=2):
    """
    Send a prompt to the Groq OpenAI-compatible endpoint.

    Accepts either:
      - prompt: a single string (wrapped as one user message), or
      - messages: a full messages list (e.g. [{'role': 'system', ...}, {'role': 'user', ...}, ...])
    """
    api_key = _get_groq_api_key()

    if not api_key:
        logger.error('GROQ_API_KEY is not configured. Checked Django settings and os.environ.')
        raise RuntimeError('GROQ_API_KEY is not configured.')

    if messages is None:
        if prompt is None:
            raise ValueError('_call_groq requires either "prompt" or "messages".')
        messages = [{'role': 'user', 'content': prompt}]

    selected_model = getattr(settings, 'GROQ_MODEL', None) or 'llama-3.3-70b-versatile'

    for attempt in range(retries):
        try:
            payload = {
                'model': selected_model,
                'max_tokens': max_tokens,
                'messages': messages,
                'temperature': 0.65,
            }

            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key}',
                'User-Agent': 'Mozilla/5.0',
            }

            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                json=payload,
                headers=headers,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            content = data['choices'][0]['message']['content']
            if isinstance(content, list):
                content = ''.join(part.get('text', '') for part in content if isinstance(part, dict))
            return str(content).strip()
        except requests.exceptions.Timeout:
            if attempt < retries - 1:
                logger.warning('Groq API timeout (attempt %d/%d), retrying...', attempt + 1, retries)
                time.sleep(1)
                continue
            logger.exception('Groq API timeout after %d attempts', retries)
            return ''
        except requests.exceptions.HTTPError as exc:
            status = exc.response.status_code if exc.response is not None else 'unknown'
            body = exc.response.text if exc.response is not None else str(exc)
            if attempt < retries - 1 and isinstance(status, int) and status >= 500:
                logger.warning('Groq API HTTP error (attempt %d/%d): %s, retrying...', attempt + 1, retries, status)
                time.sleep(1)
                continue
            logger.error('Groq API HTTP error (%s): %s', status, body)
            return ''
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            logger.error('Unexpected Groq API response structure: %s', exc)
            return ''
        except Exception as exc:
            if attempt < retries - 1:
                logger.warning('Groq API request failed (attempt %d/%d): %s, retrying...', attempt + 1, retries, exc)
                time.sleep(1)
                continue
            logger.exception('Groq API request failed: %s', exc)
            return ''

    return ''


def _parse_ai_items(text, limit=4):
    """Parse a plain-text AI response into a list of product names."""
    if not text:
        return []

    candidates = []
    for part in re.split(r'[\r\n;]+', text):
        line = part.strip()
        if not line:
            continue
        line = re.sub(r'^[\d\s\-\.\)]+', '', line).strip()
        if line:
            candidates.append(line)
        if len(candidates) >= limit:
            break
    return candidates


def get_product_recommendations_ai(product, limit=4):
    """Ask Groq AI for smart product recommendations using catalog data."""
    try:
        candidates = list(Product.objects.filter(category=product.category).exclude(id=product.id)[:20])
        if not candidates:
            return get_product_recommendations(product, limit)

        candidate_lines = [
            f"{c.name} — ₦{c.price:,.2f} — {c.description[:80].strip()}"
            for c in candidates
        ]

        prompt = (
            f"You are a helpful shopping assistant for RedCart. The customer is viewing:\n"
            f"Name: {product.name}\n"
            f"Category: {product.category}\n"
            f"Price: ₦{product.price:,.2f}\n"
            f"Description: {product.description.strip()}\n\n"
            f"From the catalog below, recommend up to {limit} products the customer is most likely to like. "
            f"Return only the exact product names, one per line.\n\n"
            f"Catalog:\n" + '\n'.join(candidate_lines)
        )

        response_text = _call_groq(prompt=prompt, max_tokens=220)
        selected_names = _parse_ai_items(response_text, limit=limit)

        recommendations = []
        for name in selected_names:
            matched = Product.objects.filter(name__iexact=name).first()
            if matched and matched.id != product.id:
                recommendations.append(matched)
            if len(recommendations) >= limit:
                break

        if recommendations:
            return recommendations

    except RuntimeError:
        pass
    except Exception as exc:
        logger.error('Error fetching AI recommendations: %s', exc)

    return get_product_recommendations(product, limit)


# ---------- Intent detection ----------

_GREETING_PATTERNS = re.compile(
    r'^\s*(hi|hii+|hello|hey|yo|sup|good\s*(morning|afternoon|evening|day))\s*[!.?]*\s*$',
    re.IGNORECASE
)

_SMALLTALK_PATTERNS = re.compile(
    r'^\s*(thanks?|thank\s*you|thx|ty|ok(ay)?|cool|nice|great|lol|haha|bye|goodbye|see\s*ya|'
    r'how\s*are\s*you|what\'?s\s*up|good\s*(bot|job))\s*[!.?]*\s*$',
    re.IGNORECASE
)

_KNOWLEDGE_KEYWORDS = re.compile(
    r'\b(shipping|delivery|deliver|return|refund|exchange|policy|track|tracking|order\s*status|'
    r'payment|pay|checkout|warranty|faq|contact|support|how\s*long|when\s*will)\b',
    re.IGNORECASE
)

_PRODUCT_KEYWORDS = re.compile(
    r'\b(product|item|price|cost|buy|purchase|cheap|expensive|discount|deal|'
    r'have|show|find|search|looking\s*for|recommend|gift|compare|stock|available|'
    r'category|categories)\b',
    re.IGNORECASE
)


def _classify_message_intent(message):
    """Returns one of: 'greeting', 'smalltalk', 'knowledge', 'product', 'other'"""
    text = message.strip()
    if _GREETING_PATTERNS.match(text):
        return 'greeting'
    if _SMALLTALK_PATTERNS.match(text):
        return 'smalltalk'
    if _KNOWLEDGE_KEYWORDS.search(text):
        return 'knowledge'
    if _PRODUCT_KEYWORDS.search(text):
        return 'product'
    return 'other'


# ---------- Site knowledge base (shipping/returns/FAQ/etc.) ----------
# Move this to a DB model later if it grows past a handful of entries.

SITE_KNOWLEDGE = {
    'shipping': "Standard delivery within Nigeria takes 2-5 business days. Lagos same-city orders may arrive within 24-48 hours.",
    'returns': "Items can be returned within 7 days of delivery if unused and in original packaging. Refunds are processed within 5-10 business days.",
    'payment': "We accept card payments, bank transfer, and pay-on-delivery in select areas.",
    'tracking': "Once shipped, you'll receive a tracking number by email. You can also check order status in your account under 'My Orders'.",
    'warranty': "Electronics carry the manufacturer's standard warranty; check the product page for specific terms.",
    'support': "For anything not covered here, reach our support team via the Contact page.",
}

_KNOWLEDGE_KEYWORD_MAP = {
    'shipping': ['shipping', 'delivery', 'deliver', 'how long', 'when will'],
    'returns': ['return', 'refund', 'exchange'],
    'payment': ['payment', 'pay', 'checkout'],
    'tracking': ['track', 'tracking', 'order status'],
    'warranty': ['warranty'],
    'support': ['contact', 'support', 'faq'],
}


def _get_relevant_knowledge(message):
    """Keyword-match the message against the site knowledge base."""
    text = message.lower()
    matches = []
    for key, kws in _KNOWLEDGE_KEYWORD_MAP.items():
        if any(kw in text for kw in kws):
            matches.append(SITE_KNOWLEDGE[key])
    return matches


# ---------- Product retrieval (keyword-scored, no vector DB needed at this scale) ----------

_STOPWORDS = {
    'the', 'a', 'an', 'is', 'are', 'do', 'does', 'you', 'your', 'i', 'me', 'my',
    'have', 'has', 'want', 'need', 'for', 'of', 'to', 'in', 'on', 'with', 'and',
    'or', 'what', 'which', 'show', 'find', 'looking', 'please', 'can', 'could',
}


def _tokenize(text):
    return {w for w in re.findall(r'[a-z0-9]+', text.lower()) if w not in _STOPWORDS and len(w) > 1}


def _retrieve_relevant_products(message, limit=15):
    """Score cached catalog entries by keyword overlap; return top matches."""
    query_tokens = _tokenize(message)
    if not query_tokens:
        return []

    catalog_items = _get_cached_catalog()
    scored = []
    for item in catalog_items:
        item_tokens = _tokenize(item)
        overlap = len(query_tokens & item_tokens)
        if overlap > 0:
            scored.append((overlap, item))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in scored[:limit]]


# ---------- Conversation history (session-based, no new DB table needed) ----------

CHAT_HISTORY_SESSION_KEY = 'redcart_chat_history'
MAX_HISTORY_TURNS = 4  # keep last 4 exchanges (8 messages)


def get_chat_history(session):
    return session.get(CHAT_HISTORY_SESSION_KEY, [])


def append_chat_history(session, role, content):
    history = session.get(CHAT_HISTORY_SESSION_KEY, [])
    history.append({'role': role, 'content': content})
    history = history[-(MAX_HISTORY_TURNS * 2):]
    session[CHAT_HISTORY_SESSION_KEY] = history
    session.modified = True


def clear_chat_history(session):
    if CHAT_HISTORY_SESSION_KEY in session:
        del session[CHAT_HISTORY_SESSION_KEY]
        session.modified = True


# ---------- Main chat entry point ----------

def get_ai_chat_response(message, session=None, limit=4):
    """
    Build an AI chat response with intent-aware retrieval and conversation memory.

    Args:
        message: the customer's chat message
        session: Django request.session — pass this to enable multi-turn memory.
                 If omitted, the bot behaves statelessly (no memory).
        limit: max products to recommend in product-intent replies
    """
    intent = _classify_message_intent(message)
    history = get_chat_history(session) if session is not None else []
    response_text = ''

    try:
        if intent in ('greeting', 'smalltalk'):
            system_msg = (
                "You are RedCart's warm, polished in-store shopping concierge. "
                "Reply naturally in 1-2 short sentences. Do NOT recommend or list "
                "products unless the customer explicitly asks about items or shopping."
            )
            messages = [{'role': 'system', 'content': system_msg}] + history + [
                {'role': 'user', 'content': message}
            ]
            response_text = _call_groq(messages=messages, max_tokens=80)

        elif intent == 'knowledge':
            knowledge = _get_relevant_knowledge(message)
            knowledge_text = '\n'.join(knowledge) if knowledge else (
                "No specific policy on file for this — direct them to Contact support."
            )
            system_msg = (
                "You are RedCart's shopping concierge. Answer using only the policy info given below. "
                "Be concise, warm, and professional. If the info doesn't cover their question, "
                "say so and suggest contacting support.\n\n"
                f"Relevant policy info:\n{knowledge_text}"
            )
            messages = [{'role': 'system', 'content': system_msg}] + history + [
                {'role': 'user', 'content': message}
            ]
            response_text = _call_groq(messages=messages, max_tokens=150)

        elif intent == 'product':
            relevant_items = _retrieve_relevant_products(message, limit=15)
            if not relevant_items:
                # No keyword match — fall back to a small sample, not a fixed "featured" list
                all_items = _get_cached_catalog()
                if not all_items:
                    return 'Sorry, our product catalog is empty. Please check back later.'
                relevant_items = all_items[:15]

            catalog_text = '\n'.join(relevant_items)
            system_msg = (
                "You are RedCart's warm, polished in-store shopping concierge. "
                "Use only the products listed below as the source of truth.\n\n"
                f"RELEVANT PRODUCTS:\n{catalog_text}\n\n"
                "Instructions:\n"
                "1. Recommend only products relevant to what the customer actually asked.\n"
                "2. If nothing here truly matches, say so honestly instead of forcing a list.\n"
                "3. Format as a simple bullet list: product name, then price, one per line.\n"
                "4. No Markdown tables. Keep tone concise and premium.\n"
                "5. End with one short follow-up question."
            )
            messages = [{'role': 'system', 'content': system_msg}] + history + [
                {'role': 'user', 'content': message}
            ]
            response_text = _call_groq(messages=messages, max_tokens=320)

        else:  # intent == 'other'
            system_msg = (
                "You are RedCart's shopping concierge. If the message is about products, shopping, "
                "or orders, offer to help and ask what they need. If it's unrelated, politely say "
                "you're the RedCart assistant and redirect. Do not list products unless asked. "
                "Keep it to 1-2 sentences."
            )
            messages = [{'role': 'system', 'content': system_msg}] + history + [
                {'role': 'user', 'content': message}
            ]
            response_text = _call_groq(messages=messages, max_tokens=100)

        if response_text and session is not None:
            append_chat_history(session, 'user', message)
            append_chat_history(session, 'assistant', response_text)

        if response_text:
            return response_text

    except RuntimeError:
        pass
    except Exception as exc:
        logger.error('AI chat failed: %s', exc)

    return (
        'Sorry, the AI assistant is unavailable right now. '
        'Try browsing our categories or use the search bar to find items.'
    )


# ============ ANALYTICS UTILITIES ============

def track_product_view(product, user=None):
    """Track product views for analytics"""
    from .models import ProductView
    ProductView.objects.create(product=product, user=user)


def get_trending_products(days=30, limit=10):
    """Get trending products based on views"""
    from .models import ProductView
    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Count

    recent_date = timezone.now() - timedelta(days=days)

    return ProductView.objects.filter(
        viewed_at__gte=recent_date
    ).values('product').annotate(
        view_count=Count('id')
    ).order_by('-view_count')[:limit]


# ============ PAGINATION UTILITIES ============

def paginate_queryset(queryset, page, items_per_page=None):
    """
    Paginate a queryset

    Returns:
        (paginated_items, total_pages, current_page) tuple
    """
    if items_per_page is None:
        items_per_page = settings.ITEMS_PER_PAGE

    total_items = queryset.count()
    total_pages = (total_items + items_per_page - 1) // items_per_page

    start = (page - 1) * items_per_page
    end = start + items_per_page

    paginated = queryset[start:end]

    return paginated, total_pages, page