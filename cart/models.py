from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from django_extensions.db.models import TimeStampedModel

from products.models import ProductSKU


class CartLog(TimeStampedModel):
    """
    Object to store all mutations to a cart.
    """
    product_sku = models.ForeignKey(ProductSKU, on_delete=models.CASCADE, null=True, blank=True)
    quantity_change = models.IntegerField(default=0)
    log_type = models.CharField(max_length=10, choices=(('change', 'change'), ('empty', 'empty')), default='change')

    def __str__(self):
        if self.log_type == 'empty':
            return "Cart is emptied"

        operation = 'added'
        quantity_change = self.quantity_change
        if self.quantity_change < 0:
            quantity_change = quantity_change * -1
            operation = 'removed'
        return '{} "{}" have been {} from the cart'.format(quantity_change, self.product_sku, operation)


class DiscountCode(TimeStampedModel):
    """
    Discount code for a discount between 1 and 100 percent.
    """
    code = models.CharField(max_length=16, unique=True)
    percentage = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])

    def __str__(self):
        return "{} ({}%)".format(self.code, self.percentage)
