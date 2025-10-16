from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from django.conf import settings
import stripe

stripe.api_key = getattr(settings, "STRIPE_SECRET_KEY", "")


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = cart.total_price()
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
def cart_add(request, product_id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart:cart_detail')


@login_required
def cart_remove(request, item_id):
    """Remove a specific item from the user's cart."""
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart:cart_detail')


@login_required
def checkout(request):
    """Simulated checkout (test mode only)."""
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.items.all()

        if not cart_items.exists():
            return render(request, 'cart/checkout.html', {
                'error': 'Your cart is empty!'
            })

        testing_message = "⚠️ System is currently in testing mode. Your order will not be charged."
        final_message = "✅ Cart cleared! Thank you for testing. You can now go back home."

        # Clear the cart
        cart_items.delete()

        return render(request, 'cart/checkout.html', {
            'message': f"{testing_message}\n{final_message}"
        })

    except Cart.DoesNotExist:
        return render(request, 'cart/checkout.html', {
            'error': 'You do not have a cart yet!'
        })
