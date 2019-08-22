from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages

from products.models import ProductSKU

from .models import CartLog
from .helpers import get_products_from_cart, put_product_in_cart


def cart_overview(request):
    """ Overview of all products in cart and applied discount codes. """

    # Put attempted discount code in session for later use.
    if request.POST:
        request.session['discount_code'] = request.POST.get('discount_code', None)
    products = get_products_from_cart(request)
    context = {
        'products': products
    }
    return render(request, 'cart/cart.html', context)


def empty_cart(request):
    """ Remove all items from the cart. """
    # TODO: Rather have this in helpers as all session mutations happen there.
    request.session['in_cart'] = {}
    CartLog.objects.create(log_type='empty')
    messages.success(request, 'Emptied cart.')
    return redirect(reverse('cart'))


def add_quantity(request, product_id):
    """ Add 1 of a single SKU to the cart """
    productsku = get_object_or_404(ProductSKU, id=str(product_id))
    put_product_in_cart(request, productsku, 1)
    return redirect(reverse('cart'))


def remove_quantity(request, product_id):
    """ Remove 1 of a single SKU from the cart """
    productsku = get_object_or_404(ProductSKU, id=str(product_id))
    put_product_in_cart(request, productsku, -1)
    return redirect(reverse('cart'))

