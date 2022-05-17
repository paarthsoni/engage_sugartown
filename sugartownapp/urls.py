from django import views
from django.contrib import admin
from django.urls import path, include
from sugartown.settings import STATICFILES_DIRS
from sugartown import settings
from sugartownapp import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [

    path("", views.index, name="index"),
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('img/favicon.ico'))),
    path("login/", views.loginuser, name="loginuser"),
    path("register", views.registeruser, name="registeruser"),
    path("logout", views.logoutUser, name="logoutuser"),
    path("requirements/", views.userrequirements_data, name="requirementsuser"),
    path("latestoffers/", views.latestoffers_user_email_data,
         name="latestoffersuser"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact/submit/", views.contact, name="contactsubmit"),
    path("blog/", views.blog, name="blog"),
    path("blog/newsletter/", views.blog, name="blognewsletter"),
    path("account/", views.account, name="account"),
    path("shop/", views.shop, name="shop"),
    path("shop/products/", views.shop_products, name="shop-products"),
    path("shop/products/Cakes", views.shop_products_cakes, name="shop-products"),
    path("shop/products/Chocolates",
         views.shop_products_chocolates, name="shop-products"),
    path("shop/products/Cookies",
         views.shop_products_cookies, name="shop-products"),
    path("shop/products/Donuts",
         views.shop_products_donuts, name="shop-products"),
    path("shop/products/icecreams",
         views.shop_products_icecreams, name="shop-products"),




]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
