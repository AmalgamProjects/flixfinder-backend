"""
https://docs.djangoproject.com/en/2.2/#the-view-layer
https://www.django-rest-framework.org/api-guide/views/

"""

from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from ..models import MovieDbTitle
from ..serializers import MovieDbTitleSerializer


class MovieDbTitleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MovieDbTitle.objects.all()
    serializer_class = MovieDbTitleSerializer
    permission_classes = (permissions.IsAuthenticated,)