"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import RapidTitle

class RapidTitleSerializer(serializers.HyperlinkedModelSerializer):
    tconst = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rapidtitle-detail'
    )

    class Meta:
        model = RapidTitle
        fields = [
            'id', 
            'created', 
            'updated', 
            'tconst', 
            'title',
            'title_type',
            'image_url',
            'remote_id',
        ]