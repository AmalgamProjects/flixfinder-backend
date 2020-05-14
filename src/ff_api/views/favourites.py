"""
https://docs.djangoproject.com/en/2.2/#the-view-layer
https://www.django-rest-framework.org/api-guide/views/

"""

from rest_framework import viewsets
from rest_framework import permissions

from ..filters import FavouriteEntryFilter
from ..models import Favourite
from ..permissions import IsOwner
from ..serializers import FavouriteSerializer


class FavouriteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    filter_class = FavouriteEntryFilter
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        return queryset.filter(user=self.request.user)
