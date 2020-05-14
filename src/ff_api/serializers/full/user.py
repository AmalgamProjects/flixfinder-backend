"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ..shallow import ShallowFavouriteSerializer, ShallowSeenSerializer, ShallowWatchSerializer
from ...models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail',
        lookup_field='username'
    )
    favourites = ShallowFavouriteSerializer(many=True, read_only=True)
    seen = ShallowSeenSerializer(many=True, read_only=True)
    watch = ShallowWatchSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'url',
            'username',
            'email',
            'favourites',
            'seen',
            'watch',
        ]
