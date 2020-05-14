"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

import hashlib

from django.contrib.auth.models import User, Group
from rest_framework import serializers


class ShallowUserSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field='username'
    )

    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'email',
        )
        read_only_fields = (
            'url',
            'username',
            'email',
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field='username'
    )

    class Meta:
        model = User
        fields = [
            'url',
            'username',
            'email',
        ]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    url = serializers.HyperlinkedIdentityField(
        view_name='group-detail',
        lookup_field='name'
    )
    users = ShallowUserSerializer(source='user_set', many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            'url',
            'name',
            'users'
        ]
