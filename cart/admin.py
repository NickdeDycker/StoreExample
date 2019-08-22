from django.contrib import admin

from .models import CartLog, DiscountCode


admin.site.register(DiscountCode)
admin.site.register(CartLog)
