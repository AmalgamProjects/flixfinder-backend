"""
https://docs.djangoproject.com/en/2.2/#the-view-layer
https://www.django-rest-framework.org/api-guide/views/

"""

import pprint

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import permissions
from rest_framework import viewsets

from ..models import MovieDbTitle
from ..serializers import MovieDbTitleSerializer


class MovieDbTitleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = MovieDbTitle.objects.all()
    serializer_class = MovieDbTitleSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser, ]


def get_mdb_id_from_tconst(tconst):
    data = MovieDbTitle.call_api('3/find/%s' % tconst, {'external_source': 'imdb_id'})
    movie_id = None
    tv_id = None
    if 'movie_results' in data:
        for movie_data in data['movie_results']:
            if 'id' in movie_data:
                movie_id = movie_data['id']
                pprint.pprint('tconst %s is external movie id %s' % (tconst, movie_id))
                break
    if 'tv_results' in data:
        for tv_data in data['tv_results']:
            if 'id' in tv_data:
                tv_id = tv_data['id']
                pprint.pprint('tconst %s is external tv id %s' % (tconst, tv_id))
                break
    return movie_id, tv_id


@api_view(['GET'])
def title_reviews(request, tconst):
    result = {
        "count": 0,
        "next": None,
        "previous": None,
        "results": []
    }
    # noinspection PyBroadException
    try:
        if tconst[:2] == 'tt':
            data = None
            movie_id, tv_id = get_mdb_id_from_tconst(tconst)
            if movie_id:
                data = MovieDbTitle.call_api('3/movie/%s/reviews' % movie_id)
            if tv_id:
                data = MovieDbTitle.call_api('3/tv/%s/reviews' % tv_id)
            if data:
                if 'results' in data:
                    for review in data['results']:
                        result['results'].append({
                            'author': review['author'],
                            'content': review['content'],
                        })
    except Exception as e:
        pprint.pprint(str(e))
    result['count'] = len(result['results'])
    return Response(result)
