from django import forms

from .models import ProductProperty, ProductPropertyValues, ProductSKU


class ProductSelectForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=1000)

    def __init__(self, product, *args, **kwargs):
        """ Get all product properties of a specific product. """
        self.product = product
        super().__init__(*args, **kwargs)

        # Get all combinations of sku's
        productsku_set = product.productsku_set.all()

        # Get all distinct property of this product.
        properties = ProductProperty.objects.filter(productpropertyvalues__productsku__product=product).distinct()

        # Create a field for each property
        for product_property in properties:

            # Get all possible values for this property and product
            values = ProductPropertyValues.objects.filter(productsku__in=productsku_set,
                                                          product_property=product_property).distinct()

            # Create field
            choices = ((x.sku_code, x.value) for x in values)
            self.fields[product_property.name] = forms.ChoiceField(
                choices=choices, widget=forms.Select,
            )

    def clean(self):
        """ Make sure quantity selected isn't more than in stock currently. """
        data = super().clean()

        # Pop so we can loop over data
        quantity = data.pop('quantity')

        productsku = ProductSKU.objects.filter(product=self.product)
        for key in data.keys():
            property_value = ProductPropertyValues.objects.get(product_property__name=key, sku_code=data[key])
            productsku = productsku.filter(properties=property_value)

        # return quantity since looped
        data['quantity'] = quantity

        if productsku.count() != 1:
            raise forms.ValidationError('This combination is not possible.')
        self.productsku = productsku.first()

        if int(quantity) > self.productsku.quantity:
            raise forms.ValidationError("We don't have this many in stock :(")
        return data
