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

    return {
        'cart_item_count': total_quantity,
    }
