from django_filters import rest_framework as filters

from ff_api.models import Watch


class WatchEntryFilter(filters.FilterSet):

    username = filters.CharFilter(name='user__username', lookup_expr='exact')

    class Meta:
        model = Watch
        fields = ['title', 'user']