"""
https://docs.djangoproject.com/en/2.2/#the-view-layer
https://www.django-rest-framework.org/api-guide/views/

"""

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions

from ..permissions import IsOwner
from ..serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = 'username'
    filter_fields = ('username', 'email',)
    ordering_fields = ('username', 'email',)
    ordering = ('email',)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, ]
    lookup_field = 'name'
    filter_fields = ('name',)
    ordering_fields = ('name',)
    ordering = ('name',)
