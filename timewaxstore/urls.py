"""timewaxstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cart.views import cart_overview
from products.views import product_list, product_detail
from cart.views import add_quantity, remove_quantity, empty_cart

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', product_list, name='product_list'),
    path('<int:product_id>/', product_detail, name='product_detail'),

    path('cart/', cart_overview, name='cart'),
    path('cart/empty/', empty_cart, name='empty-cart'),
    path('cart/add/<int:product_id>/', add_quantity, name='add-cart'),
    path('cart/remove/<int:product_id>/', remove_quantity, name='remove-cart'),
]
