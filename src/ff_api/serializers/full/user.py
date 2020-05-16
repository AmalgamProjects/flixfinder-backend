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

    recommended_movies = serializers.SerializerMethodField()
    recommended_tv = serializers.SerializerMethodField()

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
            'recommended_movies',
            'recommended_tv',
        ]

    def get_recommended_movies(self, instance):
        result = []
        for recommendation in instance.recommendation.get_queryset().filter(title__titleType='movie'):
            if recommendation.title.titleType == 'movie':
                serializer = ShallowRecommendationSerializer(recommendation, context=self.context)
                result.append(serializer.data)
        return result

    def get_recommended_tv(self, instance):
        result = []
        for recommendation in instance.recommendation.get_queryset().exclude(title__titleType='movie'):
            if recommendation.title.titleType[:2] == 'tv':
                serializer = ShallowRecommendationSerializer(recommendation, context=self.context)
                result.append(serializer.data)
        return result
