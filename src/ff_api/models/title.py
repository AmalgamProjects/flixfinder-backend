import uuid

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

    class Meta:
        ordering = ['primaryTitle', 'startYear', 'endYear']

    def is_fully_populated(self):
        return self.rapid.exists() and self.moviedb.exists() and self.tastedb.exists()

    def get_rapid(self):
        if not hasattr(self, '_cached_rapid'):
            instance = self.rapid.first()
            if instance is None:
                from .rapid import RapidTitle
                instance = RapidTitle.populate_one_from_api(self.tconst)
            self._cached_rapid = instance
        return self._cached_rapid

    def get_moviedb(self):
        if not hasattr(self, '_cached_moviedb'):
            instance = self.moviedb.first()
            if instance is None:
                from .mdb import MovieDbTitle
                instance = MovieDbTitle.populate_from_api(self.tconst)
            self._cached_moviedb = instance
        return self._cached_moviedb

    def get_tastedb(self):
        if not hasattr(self, '_cached_tastedb'):
            instance = self.tastedb.first()
            if instance is None:
                from .tastedive import TasteTitle
                instance = TasteTitle.populate_from_api(self.primaryTitle)
                self._cached_tastedb = instance
        return self._cached_tastedb

    def get_image_url(self):
        instance = self.get_rapid()
        if instance is not None and instance.image_url != "":
            return instance.image_url
        return None

    def get_backdrop_url(self):
        instance = self.get_moviedb()
        if instance is not None and instance.backdrop_url != "":
            return instance.backdrop_url
        return None

    def get_poster_url(self):
        instance = self.get_moviedb()
        if instance is not None and instance.backdrop_url != "":
            return instance.poster_url
        return self.get_image_url()

    def get_wikipedia_url(self):
        instance = self.get_tastedb()
        if instance is not None and instance.wikipedia != "":
            return instance.wikipedia
        return None

    def get_youtube_url(self):
        instance = self.get_tastedb()
        if instance is not None and instance.youtube != "":
            return instance.youtube
        return None

    def get_youtube_url(self):
        instance = self.get_tastedb()
        if instance is not None and instance.youtube != "":
            return instance.youtube
        return None

    def get_summary(self):
        mdb = self.get_moviedb()
        if mdb is not None and mdb.overview != "":
            return mdb.overview
        tdb = self.get_tastedb()
        if tdb is not None and tdb.teaser != "":
            return tdb.teaser
        return None

    def get_vote_average(self):
        try:
            return self.rating.first().averageRating
        except Exception:
            instance = self.get_moviedb()
            if instance is not None and instance.vote_average != "":
                return instance.vote_average
            return 0.0

    def get_vote_count(self):
        try:
            return self.rating.first().numVotes
        except Exception:
            instance = self.get_moviedb()
            if instance is not None and instance.vote_average != "":
                return instance.vote_count
            return 0.0

    def __str__(self):
        return '%s - %s - %s' % (self.tconst, self.titleType, self.primaryTitle)
