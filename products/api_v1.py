"""Read-only JSON API for the Next.js storefront (app/).

The Django site stays the source of truth for cart, checkout, payments and
accounts; the storefront only reads the catalog from these endpoints and hands
off to Django for anything that changes state.
"""
from math import ceil

from django.conf import settings
from django.db.models import Avg, Count, Q
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_GET

from .models import Product

MAX_PAGE_SIZE = 48
DEFAULT_PAGE_SIZE = 24
SORTS = {
    'newest': '-id',
    'price_asc': 'price',
    'price_desc': '-price',
    'name': 'name',
}


def _with_cors(request, response):
    origin = request.headers.get('Origin', '')
    allowed = getattr(settings, 'STOREFRONT_ORIGINS', [])
    if origin and origin in allowed:
        response['Access-Control-Allow-Origin'] = origin
        response['Vary'] = 'Origin'
    response['Cache-Control'] = 'public, max-age=60'
    return response


def _serialize(product, rating=None, reviews=None):
    on_sale = product.has_active_sale
    return {
        'id': product.id,
        'name': product.name,
        'category': product.category,
        'category_label': product.get_category_display(),
        'price': product.price,
        'sale_price': product.sale_price if on_sale else None,
        'sale_ends_at': product.sale_ends_at.isoformat() if on_sale else None,
        'discount_percentage': product.discount_percentage if on_sale else 0,
        'image': product.image_src,
        'in_stock': not product.is_out_of_stock,
        'low_stock': product.is_low_stock,
        'rating': round(rating or 0, 1),
        'review_count': reviews or 0,
    }


def _published_reviews():
    return Q(reviews__moderation_status='published')


def _annotated(queryset):
    return queryset.annotate(
        avg_rating=Avg('reviews__rating', filter=_published_reviews()),
        num_reviews=Count('reviews', filter=_published_reviews()),
    )


def _int_param(request, name, default, low, high):
    try:
        value = int(request.GET.get(name, default))
    except (TypeError, ValueError):
        return default
    return max(low, min(high, value))


@require_GET
def product_list(request):
    queryset = Product.objects.all()

    query = request.GET.get('q', '').strip()[:100]
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | Q(description__icontains=query) | Q(category__icontains=query)
        )

    category = request.GET.get('category', '').strip()
    valid_categories = dict(Product.CATEGORY_CHOICES)
    if category in valid_categories:
        queryset = queryset.filter(category=category)

    if request.GET.get('on_sale') == '1':
        queryset = queryset.filter(
            sale_price__isnull=False, sale_ends_at__gt=timezone.now(),
        )

    sort = request.GET.get('sort', 'newest')
    queryset = _annotated(queryset).order_by(SORTS.get(sort, '-id'), 'id')

    page_size = _int_param(request, 'page_size', DEFAULT_PAGE_SIZE, 1, MAX_PAGE_SIZE)
    count = queryset.count()
    pages = max(1, ceil(count / page_size))
    page = _int_param(request, 'page', 1, 1, pages)
    start = (page - 1) * page_size
    products = queryset[start:start + page_size]

    category_counts = dict(
        Product.objects.values_list('category').annotate(n=Count('id')).values_list('category', 'n')
    )
    categories = [
        {'value': value, 'label': label, 'count': category_counts[value]}
        for value, label in Product.CATEGORY_CHOICES if category_counts.get(value)
    ]

    return _with_cors(request, JsonResponse({
        'results': [_serialize(p, p.avg_rating, p.num_reviews) for p in products],
        'count': count,
        'page': page,
        'pages': pages,
        'categories': categories,
    }))


@require_GET
def product_detail(request, product_id):
    product = _annotated(Product.objects.filter(pk=product_id)).first()
    if product is None:
        return _with_cors(request, JsonResponse({'error': 'Product not found.'}, status=404))

    data = _serialize(product, product.avg_rating, product.num_reviews)
    data['description'] = product.description or product.ai_description or ''
    data['images'] = [product.image_src, *product.additional_images]
    data['stock'] = max(product.available_stock, 0)

    reviews = product.reviews.filter(moderation_status='published').select_related('user').order_by('-created_at')[:5]
    data['reviews'] = [
        {
            'rating': review.rating,
            'text': review.review_text,
            'author': review.user.first_name or review.user.username,
            'verified_purchase': review.verified_purchase,
            'created_at': review.created_at.isoformat(),
        }
        for review in reviews
    ]

    related = _annotated(
        Product.objects.filter(category=product.category).exclude(pk=product.pk)
    ).order_by('-id')[:4]
    data['related'] = [_serialize(p, p.avg_rating, p.num_reviews) for p in related]

    return _with_cors(request, JsonResponse(data))
