from django.contrib import messages

from products.models import ProductSKU

from .models import CartLog, DiscountCode


def put_product_in_cart(request, productsku, quantity):
    """ Adds `quantity` of `productsku` to the cart. Handles all changes to the cart.  """
    in_cart = request.session.get('in_cart', {})

    # Makes sure the quantity doesn't exceed the one in stock.
    sku_code = productsku.get_full_sku_code()
    if sku_code not in in_cart and productsku.quantity > quantity:
        in_cart[sku_code] = quantity
    elif productsku.quantity > in_cart[sku_code] + quantity:
        if in_cart[sku_code] + quantity <= 0:
            del in_cart[sku_code]
        else:
            in_cart[sku_code] += quantity
    else:
        messages.warning(request, 'Not enough of {} in stock'.format(productsku))
        return

    request.session['in_cart'] = in_cart
    CartLog.objects.create(product_sku=productsku, quantity_change=quantity)
    messages.success(request, 'Added {} of {} to cart.'.format(quantity, productsku))


def get_products_from_cart(request):
    """ Convert all products from session to python objects and add total prices to session. """
    products = []
    if 'in_cart' not in request.session:
        return []

    # Get all products from session and calculate price.
    total_price = 0
    for sku_code in request.session['in_cart']:
        product = ProductSKU.get_product_from_sku_code(sku_code)
        product.in_cart = request.session['in_cart'][sku_code]
        product.total_price = product.in_cart * product.product.price
        products.append(product)

        total_price += product.total_price

    # Check for valid discount code and calculate discount price
    discount_code = request.session.get('discount_code', None)
    if discount_code:
        try:
            discount_code = DiscountCode.objects.get(code=discount_code)
            request.session['discount_price'] = round(float(total_price) * ((100 - discount_code.percentage) / 100.), 2)
        except DiscountCode.DoesNotExist:
            messages.warning(request, 'Discount code "{}" does not exist'.format(discount_code))
            del request.session['discount_code']

    request.session['total_price'] = round(float(total_price), 2)
    return products
