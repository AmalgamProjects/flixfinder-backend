"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import RapidTitle


class RapidTitleSerializer(serializers.HyperlinkedModelSerializer):
    tconst = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='title-detail',
        lookup_field='tconst'
    )

    class Meta:
        model = RapidTitle
        fields = [
            'id',
            'created',
            'updated',
            'tconst',
            'title',
            'titleType',
            'image_url',
            'remote_id',
        ]
