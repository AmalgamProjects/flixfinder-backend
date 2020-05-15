"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import Recommendation


class ShallowRecommendationSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username',
    )
    title = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='tconst',
    )

    class Meta:
        model = Recommendation
        fields = ['id', 'user', 'priority', 'title']
        read_only_fields = ['id', 'user', 'priority', 'title']
