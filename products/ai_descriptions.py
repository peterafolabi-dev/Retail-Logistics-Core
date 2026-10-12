import logging
import re

logger = logging.getLogger(__name__)


def generate_description(product):
    """Generate a cautious, plain-text description for a product listing."""
    try:
        from products.utils import _call_groq

        name = str(getattr(product, 'name', '') or '').strip()
        category = str(getattr(product, 'category', '') or '').strip()
        brand = str(getattr(product, 'brand', '') or '').strip()
        price = getattr(product, 'price', '')
        if not name:
            logger.warning('Cannot generate a product description without a product name.')
            return None

        prompt = (
            'Write exactly 2 or 3 short plain-text sentences for an online store product listing. '
            'Use a neutral, helpful, store-friendly tone and no markdown, headings, bullets, or quotes. '
            'Only describe what can reasonably be known from the product name and category. '
            'Never invent or infer specifications, dimensions, warranty, certifications, quantities, '
            'performance claims, or other numbers. Do not include the price in the description. '
            'If details are limited, use cautious general wording rather than making claims.\n\n'
            f'Product name: {name}\n'
            f'Category: {category or "Not specified"}\n'
            f'Brand: {brand or "Not specified"}\n'
            f'Listed price for context only: {price}'
        )
        result = _call_groq(prompt=prompt, max_tokens=180, retries=2, timeout=15)
        if not isinstance(result, str) or not result.strip():
            logger.warning('Groq returned no description for product %s.', getattr(product, 'pk', None))
            return None

        description = re.sub(r'\s+', ' ', result).strip().strip('"\'')
        description = re.sub(r'^(?:[-*#]\s+|\d+[.)]\s+)', '', description)
        description = description.replace('**', '').replace('__', '').replace('`', '')
        sentences = re.findall(r'[^.!?]+(?:[.!?]+|$)', description)
        if not 2 <= len(sentences) <= 3 or re.search(r'\[[^\]]+\]\([^)]+\)', description):
            logger.warning('Groq returned an invalid description for product %s.', getattr(product, 'pk', None))
            return None

        return description
    except Exception:
        logger.exception('Description generation failed for product %s.', getattr(product, 'pk', None))
        return None
