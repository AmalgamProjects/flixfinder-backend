from django_filters import rest_framework as filters

from ff_api.models import Seen


class SeenEntryFilter(filters.FilterSet):

    username = filters.CharFilter(name='user__username', lookup_expr='exact')

    class Meta:
        model = Seen
        fields = ['title', 'user']