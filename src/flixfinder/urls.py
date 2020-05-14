"""flixfinder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/

"""

from django.contrib import admin
from django.contrib.staticfiles.views import serve
from django.urls import include, path, re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ff_api.urls')),
    path('api/', include('ff_api.urls')),
    re_path(r'^(?!admin|api|static)', include('ff_spa.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'insecure': True}),
]
