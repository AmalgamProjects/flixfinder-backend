"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Main representation of Movies and TV Shows.

"""

import uuid
import pprint

from django.db import models


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)


# noinspection PyBroadException
class Title(models.Model):
    tconst = models.CharField(primary_key=True, max_length=255)
    titleType = models.CharField(max_length=255, db_index=True)
    primaryTitle = models.CharField(max_length=255, db_index=True)
    originalTitle = models.CharField(max_length=255, db_index=True)
    isAdult = models.CharField(max_length=1, db_index=True, default='')
    startYear = models.CharField(max_length=4, db_index=True, default='')
    endYear = models.CharField(null=True, max_length=4, db_index=True, default='')
    runtimeMinutes = models.CharField(max_length=10, db_index=True, default='')
    genres = models.ManyToManyField(Genre)

    image_url = models.URLField(null=True, default=None)
    backdrop_url = models.URLField(null=True, default=None)
    poster_url = models.URLField(null=True, default=None)
    wikipedia_url = models.URLField(null=True, default=None)
    youtube_url = models.URLField(null=True, default=None)
    summary = models.TextField(null=True, default=None)
    vote_average = models.FloatField(default=0.0)
    vote_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['primaryTitle', 'startYear', 'endYear']

    def is_fully_populated(self):
        return self.rapid.exists() and self.moviedb.exists() and self.tastedb.exists()

    def get_rapid(self):
        if not hasattr(self, '_cached_rapid'):
            self._cached_rapid = None
            instance = self.rapid.first()
            if instance is None:
                from .rapid import RapidTitle
                instance = RapidTitle.populate_one_from_api(self.tconst)
            self._cached_rapid = instance
        return self._cached_rapid

    def get_moviedb(self):
        if not hasattr(self, '_cached_moviedb'):
            self._cached_moviedb = None
            instance = self.moviedb.first()
            if instance is None:
                from .mdb import MovieDbTitle
                instance = MovieDbTitle.populate_from_api(self.tconst)
            self._cached_moviedb = instance
        return self._cached_moviedb

    def get_tastedb(self):
        if not hasattr(self, '_cached_tastedb'):
            self._cached_tastedb = None
            instance = self.tastedb.first()
            if instance is None:
                from .tastedive import TasteTitle
                instance = TasteTitle.populate_from_api(self.primaryTitle)
            self._cached_tastedb = instance
        return self._cached_tastedb

    def get_image_url(self):
        if self.image_url is None or self.image_url == "":
            instance = self.get_rapid()
            if instance is not None and instance.image_url != "":
                self.image_url = instance.image_url
                self.save()
        return self.image_url

    def get_backdrop_url(self):
        if self.backdrop_url is None or self.backdrop_url == "":
            instance = self.get_moviedb()
            if instance is not None and instance.backdrop_url != "":
                self.backdrop_url = instance.backdrop_url
                self.save()
        return self.backdrop_url

    def get_poster_url(self):
        if self.poster_url is None or self.poster_url == "":
            instance = self.get_moviedb()
            if instance is not None and instance.poster_url != "":
                self.poster_url = instance.poster_url
            if self.poster_url is None or self.poster_url == "":
                self.poster_url = self.get_image_url()
            if self.poster_url is not None or self.poster_url != "":
                self.save()
        return self.poster_url

    def get_wikipedia_url(self):
        if self.wikipedia_url is None or self.wikipedia_url == "":
            instance = self.get_tastedb()
            if instance is not None and instance.wikipedia != "":
                self.wikipedia_url = instance.wikipedia
                self.save()
        return self.wikipedia_url

    def get_youtube_url(self):
        if self.youtube_url is None or self.youtube_url == "":
            instance = self.get_tastedb()
            if instance is not None and instance.youtube != "":
                self.youtube_url = instance.youtube
                self.save()
        return self.youtube_url

    def get_summary(self):
        if self.summary is None or self.summary == "":
            mdb = self.get_moviedb()
            if mdb is not None and mdb.overview != "":
                self.summary = mdb.overview
            if self.summary is None or self.summary == "":
                tdb = self.get_tastedb()
                if tdb is not None and tdb.teaser != "":
                    self.summary = tdb.teaser
            if self.summary is not None and self.summary != "":
                self.save()
        return self.summary

    def get_vote_average(self):
        if self.vote_average <= 0.0:
            try:
                self.vote_average = self.rating.first().averageRating
                self.save()
            except Exception:
                instance = self.get_moviedb()
                if instance is not None and instance.vote_average != "":
                    self.vote_average = instance.vote_average
                    self.save()
        return self.vote_average

    def get_vote_count(self):
        if self.vote_count <= 0:
            try:
                self.vote_count = self.rating.first().numVotes
                self.save()
            except Exception:
                instance = self.get_moviedb()
                if instance is not None and instance.vote_average != "":
                    self.vote_count = instance.vote_count
                    self.save()
        return self.vote_count

    def __str__(self):
        return '%s - %s - %s' % (self.tconst, self.titleType, self.primaryTitle)
