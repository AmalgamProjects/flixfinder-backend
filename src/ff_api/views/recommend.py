"""
https://docs.djangoproject.com/en/2.2/#the-view-layer
https://www.django-rest-framework.org/api-guide/views/

"""

import pprint

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import viewsets
from rest_framework import permissions

from ..models import Recommendation
from ..permissions import IsOwner
from ..serializers import RecommendationSerializer, ShallowTitleSerializer


class RecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """

    """
    queryset = Recommendation.objects.order_by('priority')
    serializer_class = RecommendationSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            return queryset.none()
        return queryset.filter(user=self.request.user)


@api_view(['GET'])
def titles_like_this(request, tconst):
    result = {
        "count": 0,
        "next": None,
        "previous": None,
        "results": []
    }
    # noinspection PyBroadException
    try:
        for title_instance in Recommendation.get_suggestions_from_tconst(tconst):
            if title_instance:
                result['results'].append(
                    ShallowTitleSerializer(title_instance, context={'request': request}).data
                )
    except Exception as e:
        pprint.pprint(str(e))
        raise
    result['count'] = len(result['results'])
    return Response(result)
