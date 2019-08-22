from django.shortcuts import render, get_object_or_404, redirect, reverse

from cart.helpers import put_product_in_cart

from .models import Product
from .forms import ProductSelectForm


def product_list(request):
    """ ListView of all store items. """
    products = Product.objects.all()
    context = {
        'products': products,
    }
    return render(request, 'products/list.html', context)


def product_detail(request, product_id):
    """ Detailed view of product with the ability to add to cart. """
    product = get_object_or_404(Product, id=str(product_id))

    if request.POST:
        form = ProductSelectForm(product, request.POST)
        if form.is_valid():

            # Put product in session
            productsku = form.productsku
            put_product_in_cart(request, productsku, form.cleaned_data['quantity'])
            return redirect(reverse('cart'))
    else:
        form = ProductSelectForm(product)

    context = {
        'product': product,
        'form': form
    }
    return render(request, 'products/detail.html', context)
