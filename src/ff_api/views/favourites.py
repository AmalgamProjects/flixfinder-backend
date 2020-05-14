from ff_api.models import Favourite
from rest_framework import viewsets
from rest_framework import permissions

from ..serializers import FavouriteSerializer


class FavouriteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer
    permission_classes = [permissions.IsAuthenticated]
    

