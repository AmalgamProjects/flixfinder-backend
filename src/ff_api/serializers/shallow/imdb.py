"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import Title, Name, Rating


class VeryShallowTitleSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SlugField(source='tconst')

    class Meta:
        model = Title
        fields = ['id', 'titleType', 'primaryTitle']


class ShallowTitleSerializer(serializers.HyperlinkedModelSerializer):
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='title-detail',
    #     lookup_field='tconst'
    # )

    id = serializers.SlugField(source='tconst')
    backdrop_url = serializers.URLField(source="get_backdrop_url")
    poster_url = serializers.URLField(source="get_poster_url")

    class Meta:
        model = Title
        fields = ['id', 'titleType', 'primaryTitle', 'backdrop_url', 'poster_url']


class ShallowNameSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SlugField(source='nconts')

    class Meta:
        model = Name
        fields = ['id', 'primaryName']


class ShallowRatingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rating
        fields = ['averageRating', 'numVotes']
