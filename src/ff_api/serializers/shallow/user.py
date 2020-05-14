"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import User


class ShallowUserSerializer(serializers.HyperlinkedModelSerializer):
    """

    """
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='user-detail',
    #     lookup_field='username'
    # )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )
        read_only_fields = (
            'username',
            'email',
        )
