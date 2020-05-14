from ff_api.models import Seen
from rest_framework import viewsets
from rest_framework import permissions

from ..serializers import SeenSerializer


class SeenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Seen.objects.all()
    serializer_class = SeenSerializer
    permission_classes = [permissions.IsAuthenticated]
    

