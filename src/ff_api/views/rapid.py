"""
https://docs.djangoproject.com/en/2.2/#the-view-layer
https://www.django-rest-framework.org/api-guide/views/

"""

from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from ..models import RapidTitle
from ..serializers import RapidTitleSerializer


class RapidTitleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = RapidTitle.objects.all()
    serializer_class = RapidTitleSerializer
    permission_classes = (permissions.IsAuthenticated,)
