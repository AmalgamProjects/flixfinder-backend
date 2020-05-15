"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

"""

import datetime
import uuid
import requests
import pprint

from django.conf import settings
from django.db import models

from .title import Title
from ..fields import DateTimeFieldWithoutMicroseconds


class MovieDbTitle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = DateTimeFieldWithoutMicroseconds(auto_now_add=True, editable=False)
    updated = DateTimeFieldWithoutMicroseconds(auto_now=True)
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='moviedb', null=True)
    title = models.CharField(max_length=255, db_index=True)
    overview = models.TextField(blank=True, null=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField()
    backdrop_url = models.URLField(blank=True, null=True)
    poster_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return 'MovieDB: %s' % self.title

    @staticmethod
    def call_api(method, params=None):
        """
        https://developers.themoviedb.org/3/getting-started/introduction
        """
        if params is None:
            params = {}
        params['api_key'] = settings.MDB_API_KEY
        response = requests.get(
            'https://%s/%s' % (settings.MDB_API_HOST, method),
            params=params
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def populate_from_api(tconst_string, create_missing_title=True):
        if tconst_string[:2] != 'tt':
            return
        pprint.pprint('MovieDbTitle tconst = %s' % tconst_string)
        image_base = 'http://image.tmdb.org/t/p/w500'
        data = MovieDbTitle.call_api('3/find/%s' % tconst_string, {'external_source': 'imdb_id'})
        for result_type in ['movie_results', 'tv_results']:
            if result_type == 'movie_results':
                titleType = 'movie'
            else:
                titleType = 'tvSeries'
            for result in data[result_type]:
                # pprint.pprint(result)
                try:
                    title = result['title']  # "Ocean's Twelve"
                    backdrop_url = ''
                    if isinstance(result['backdrop_path'], str):
                        backdrop_url = ''.join(
                            (image_base, result['backdrop_path']))  # '/3guCfwRt3MrmO6q56I4F5xN1LYB.jpg'
                    poster_url = ''
                    if isinstance(result['backdrop_path'], str):
                        poster_url = ''.join((image_base, result['poster_path']))  # '/3guCfwRt3MrmO6q56I4F5xN1LYB.jpg'

                    instance, created = MovieDbTitle.objects.update_or_create(
                        title=title,
                        defaults={
                            'title': title,  # "Ocean's Twelve"
                            'overview': result['overview'],  # 'Danny Ocean reunites with ....
                            'vote_average': result['vote_average'],  # 6.5
                            'vote_count': result['vote_count'],  # 4750
                            'backdrop_url': backdrop_url,
                            'poster_url': poster_url
                        },
                    )
                    if create_missing_title:
                        release_date = datetime.datetime.strptime(result['release_date'], '%Y-%m-%d')
                        title_instance, created = Title.objects.update_or_create(
                            tconst=tconst_string,
                            defaults={
                                'tconst': tconst_string,
                                'titleType': titleType,
                                'primaryTitle': result['title'],
                                'originalTitle': result['title'],
                                'startYear': str(release_date.year),
                            }
                        )
                    else:
                        title_instance = Title.objects.filter(tconst=tconst_string).first()
                    instance.tconst = title_instance
                    instance.save()
                    pprint.pprint('MovieDbTitle %s ... %s' % (title, instance.tconst))
                except Exception as e:
                    pprint.pprint(e)
                    pass
