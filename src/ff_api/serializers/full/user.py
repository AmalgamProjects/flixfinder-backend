"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ..shallow import \
    ShallowFavouriteSerializer, \
    ShallowFavouriteGenreSerializer, \
    ShallowSeenSerializer, \
    ShallowWatchSerializer, \
    ShallowRecommendationSerializer
from ...models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    favourites = ShallowFavouriteSerializer(many=True, read_only=True)
    favouriteGenres = ShallowFavouriteGenreSerializer(many=True, read_only=True, source='favourite_genres')
    seen = ShallowSeenSerializer(many=True, read_only=True)
    watch = ShallowWatchSerializer(many=True, read_only=True)
    recommended = ShallowRecommendationSerializer(many=True, read_only=True, source='recommendation')

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'favourites',
            'favouriteGenres',
            'seen',
            'watch',
            'recommended',
        ]
