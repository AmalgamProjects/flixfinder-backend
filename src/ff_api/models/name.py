"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Name data from the IMDB datasets.

https://datasets.imdbws.com/
https://www.imdb.com/interfaces/

NOTICE: This data is obtained under a Non-Commercial Use License

"""

import pprint

from django.db import models

from .mdb import MovieDbTitle
from .title import Title
from ..fields import SeparatedValuesField


class Name(models.Model):
    nconst = models.CharField(primary_key=True, max_length=255)
    primaryName = models.CharField(max_length=255, db_index=True)
    birthYear = models.IntegerField(null=True)
    deathYear = models.IntegerField(null=True)
    primaryProfession = SeparatedValuesField(default="", blank=True, null=True)
    knownForTitles = models.ManyToManyField(Title, blank=True)

    moviedbid = models.CharField(max_length=255, null=True, blank=True, default=None, db_index=True)
    image_url = models.URLField(null=True, default=None)

    def get_image_url(self):
        if self.image_url is None or self.image_url == '':
            self.get_data_from_moviedb_api()
        return self.image_url

    def get_data_from_moviedb_api(self):
        if self.moviedbid == 0:
            return None, None
        self.moviedbid = 0
        self.image_url = None
        save = False
        data = MovieDbTitle.call_api('3/find/%s' % self.nconst, {'external_source': 'imdb_id'})
        if 'person_results' in data:
            for person_data in data['person_results']:
                if 'id' in person_data:
                    self.moviedbid = person_data['id']
                    pprint.pprint('nconst %s is external person id %s' % (self.nconst, self.moviedbid))
                    save = True
                if 'profile_path' in person_data and person_data['profile_path'] is not None:
                    self.image_url = 'https://image.tmdb.org/t/p/w185' + person_data['profile_path']
                    save = True
                # TODO we could/should use the known_for to populate more principal relationships
        if save:
            self.save()
        return self.moviedbid, self.image_url
