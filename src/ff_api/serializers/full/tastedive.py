"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import TasteTitle

class TasteTitleSerializer(serializers.HyperlinkedModelSerializer):
    tconst = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='tastetitle-detail'
    )

    class Meta:
        model = TasteTitle
        fields = [
            'id', 
            'created', 
            'updated', 
            'tconst', 
            'name',
            'type',
            'teaser',
            'wikipedia',
            'youtube'
        ]