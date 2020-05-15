"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

"""

import uuid
import requests
import pprint

from django.conf import settings
from django.db import models
from urllib.parse import quote_plus

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
    def populate_from_api(query):
        """
        https://developers.themoviedb.org/3/getting-started/introduction
        """
        pprint.pprint('MovieDbTitle query = %s' % query)
        image_base = 'http://image.tmdb.org/t/p/w500'
        response = requests.get(
            '%s3/search/movie?api_key=%s&query=%s' % (
                settings.MDB_API_HOST,
                settings.MDB_API_KEY,
                quote_plus(query)
            ))
        response.raise_for_status()
        data = response.json()
        for result in data['results']:
            try:
                title = result['title']  # "Ocean's Twelve"

                backdrop_url = ''
                if isinstance(result['backdrop_path'], str):
                    backdrop_url = image_base + result['backdrop_path'],  # '/3guCfwRt3MrmO6q56I4F5xN1LYB.jpg'
                poster_url = ''
                if isinstance(result['backdrop_path'], str):
                    poster_url = image_base + result['poster_path'],  # '/3guCfwRt3MrmO6q56I4F5xN1LYB.jpg'

                instance, created = MovieDbTitle.objects.get_or_create(
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
                instance.tconst = Title.objects.filter(primaryTitle=title).first()
                instance.save()
                pprint.pprint('MovieDbTitle %s ... %s' % (title, instance.tconst))
            except Exception as e:
                pprint.pprint(e)
                pass
