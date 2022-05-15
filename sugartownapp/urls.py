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
    # path("facecapture", views.registerfacecapture, name="facecapture"),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
