"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

import hashlib

from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field='username'
    )
    gravatar = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'url',
            'username',
            'email',
            # 'groups',
            'gravatar'
        ]

    def get_gravatar(self, instance):
        email = str(instance.email).strip().lower()
        bytes = email.encode()
        hash = hashlib.md5(bytes).hexdigest()
        return 'https://www.gravatar.com/avatar/%s?d=retro&r=g' % hash


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
