"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ..models import Seen


class SeenSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seen
        fields = ['user', 'title']
