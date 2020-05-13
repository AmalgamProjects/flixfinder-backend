"""
https://docs.djangoproject.com/en/2.2/topics/http/views/

"""

from django.conf import settings
from django.http import Http404
from django.views.static import serve


def serve_spa(request, path):
    """
    This method will serve the files from the static root if they
     are specifically requested. However when a path is not found
     the index.html page is served instead.

    This will allow the SPA to use the JS browser.history API to
     implement JS client side path routing, and 404.

    :param request:
    :param path:
    :return:
    """
    try:
        return serve(request, path, settings.SPA_ROOT, False)
    except Http404:
        return serve(request, 'index.html', settings.SPA_ROOT)
