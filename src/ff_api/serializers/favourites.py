"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

import hashlib

from ff_api.models import Favourite
from rest_framework import serializers


class FavouriteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Favourite
        fields = ['user', 'title']