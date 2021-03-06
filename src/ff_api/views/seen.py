"""
https://docs.djangoproject.com/en/2.2/#the-view-layer
https://www.django-rest-framework.org/api-guide/views/

"""

from rest_framework import viewsets
from rest_framework import permissions

from ..models import Seen
from ..permissions import IsOwner
from ..serializers import SeenSerializer


class SeenViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Seen.objects.all()
    serializer_class = SeenSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        return queryset.filter(user=self.request.user)
    

