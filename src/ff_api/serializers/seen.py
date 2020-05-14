"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

import hashlib

from ff_api.models import Seen
from rest_framework import serializers


class SeenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seen
        fields = ['user', 'title']