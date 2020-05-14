"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

import hashlib

from ff_api.models import Watch
from rest_framework import serializers


class WatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Watch
        fields = ['user', 'title']