from django.contrib import admin
from .models import Product, ProductSKU, ProductProperty, ProductPropertyValues


class ProductPropertyValuesAdmin(admin.StackedInline):
    model = ProductPropertyValues


class ProductPropertyAdmin(admin.ModelAdmin):
    model = ProductProperty
    inlines = [ProductPropertyValuesAdmin]


class ProductSKUAdmin(admin.StackedInline):
    model = ProductSKU


class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name', 'sku_code']
    inlines = [ProductSKUAdmin]


admin.site.register(ProductProperty, ProductPropertyAdmin)
admin.site.register(Product, ProductAdmin)
