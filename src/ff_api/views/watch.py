from ff_api.models import Watch
from rest_framework import viewsets
from rest_framework import permissions

from ..serializers import WatchSerializer


class WatchViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Watch.objects.all()
    serializer_class = WatchSerializer
    permission_classes = [permissions.IsAuthenticated]
    

