"""
https://docs.djangoproject.com/en/2.2/#the-view-layer
https://www.django-rest-framework.org/api-guide/views/

"""

from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets

from ..models import TasteTitle
from ..serializers import TasteTitleSerializer


class TasteTitleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TasteTitle.objects.all()
    serializer_class = TasteTitleSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, ]
