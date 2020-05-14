from django_filters import rest_framework as filters

from ff_api.models import Favourite


class FavouriteEntryFilter(filters.FilterSet):

    username = filters.CharFilter(name='user__username', lookup_expr='exact')

    class Meta:
        model = Favourite
        fields = ['title', 'user']