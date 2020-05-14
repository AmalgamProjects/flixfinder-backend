"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ..models import Watch


class WatchSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Watch
        fields = ['user', 'title']
