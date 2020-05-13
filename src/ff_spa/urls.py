"""
https://docs.djangoproject.com/en/2.2/topics/http/urls/

The `urlpatterns` list routes URLs to views.

"""

from django.urls import re_path

from .views import serve_spa

urlpatterns = [
    re_path(r'^(?P<path>.*)$', serve_spa),
]
