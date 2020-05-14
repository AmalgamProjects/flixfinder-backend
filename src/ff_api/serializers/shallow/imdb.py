"""
http://www.django-rest-framework.org/api-guide/serializers/

"""

from rest_framework import serializers

from ...models import Title, Name


class ShallowTitleSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='title-detail',
        lookup_field='tconst'
    )

    id = serializers.SlugField(source='tconst')

    class Meta:
        model = Title
        fields = ['id', 'titleType', 'primaryTitle']
        

class ShallowNameSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.SlugField(source='nconts')
    
    class Meta:
        model = Name
        fields = ['id', 'primaryName']