"""sugartown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from sugartownapp import views
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('sugartownapp.urls', 'sugartown'), namespace='sugartown')),
    # path('cartload/',
    #      views.cart_add, name='cartload'),
    path('shop/cart',
         views.shop_cart, name="shop-cart"),
    path('cartload/product_name=<str:product_name>&product_price=<int:product_price>',
         views.cart_add, name='cartload'),
    path('deleteitem/product_name=<str:product_name>',
         views.delete_cart_item, name='deleteitem'),
    path('altercart/product_name=<str:product_name>',
         views.alter_cart, name='altercart'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Sugar Town"
admin.site.site_title = "Sugar Town"
admin.site.index_title = "Welcome to Sugar Town"
