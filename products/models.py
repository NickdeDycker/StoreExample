from django.db import models
from django.core.validators import MaxValueValidator

from django_extensions.db.models import TimeStampedModel

MAX_ITEMS = 1000


class Product(TimeStampedModel):
    """
    A single product, with no specific properties such as size.
    """

    name = models.CharField(max_length=32)
    sku_code = models.CharField(max_length=6, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_stock(self):
        raise NotImplemented

    def __str__(self):
        return self.name


class ProductSKU(TimeStampedModel):
    """
    A product with properties such as size and color. The combination of properties should make it unique.
    """

    # TODO: Uniqueness of properties
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MaxValueValidator(MAX_ITEMS)])
    properties = models.ManyToManyField('ProductPropertyValues')

    def __str__(self):
        base = str(self.product)
        properties_string = ', '.join(["{}: {}".format(x.product_property, x.value) for x in self.properties.all()])
        return "{} ({})".format(base, properties_string)

    @classmethod
    def get_product_from_sku_code(cls, sku_code):
        """ Get an object from a sku_code string. """
        codes = sku_code.split("-")

        # Get main product
        try:
            product = Product.objects.get(sku_code=codes[0])
        except Product.DoesNotExist:
            return None

        # Filter by individual properties
        possible_product_skus = cls.objects.filter(product=product)
        for code in codes[1:]:
            possible_product_skus = possible_product_skus.filter(properties__sku_code=code)

        if possible_product_skus.count() != 1:
            return None
        return possible_product_skus.first()

    def get_full_sku_code(self):
        """ Get a sku_code string from an object. """
        properties_sku_code = "-".join([prop.sku_code for prop in self.properties.all()])
        return "{}-{}".format(self.product.sku_code, properties_sku_code)


class ProductProperty(TimeStampedModel):
    """
    A possible property of a product (e.g. size or color)
    This is in a separate table so we can group them easily.
    """

    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class ProductPropertyValues(TimeStampedModel):
    """
    A possible value for a property (e.g.: size 42 or blue)
    """
    product_property = models.ForeignKey(ProductProperty, on_delete=models.CASCADE)
    value = models.CharField(max_length=16)
    sku_code = models.CharField(max_length=3, unique=True)

    def __str__(self):
        return "{}: {}".format(self.product_property.name, self.value)
