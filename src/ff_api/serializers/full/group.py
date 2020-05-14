"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ..shallow import ShallowUserSerializer
from ...models import Group


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='group-detail',
    #     lookup_field='name'
    # )
    users = ShallowUserSerializer(source='user_set', many=True, read_only=True)

    class Meta:
        model = Group
        fields = [
            'name',
            'users'
        ]
