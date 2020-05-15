import uuid

from django.db import models


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)


class Title(models.Model):
    tconst = models.CharField(primary_key=True, max_length=255)
    titleType = models.CharField(max_length=255, db_index=True)
    primaryTitle = models.CharField(max_length=255, db_index=True)
    originalTitle = models.CharField(max_length=255, db_index=True)
    isAdult = models.CharField(max_length=1, db_index=True)
    startYear = models.CharField(max_length=4, db_index=True)
    endYear = models.CharField(null=True, max_length=4, db_index=True)
    runtimeMinutes = models.CharField(max_length=10, db_index=True)
    genres = models.ManyToManyField(Genre)

    def get_rapid(self):
        instance = self.rapid.first()
        if instance is None:
            from .rapid import RapidTitle
            instance = RapidTitle.populate_one_from_api(self.tconst)
        return instance

    def get_image_url(self):
        instance = self.get_rapid()
        if instance is not None and instance.image_url != "":
            return instance.image_url
        return None

    def get_backdrop_url(self):
        instance = self.moviedb.first()
        if instance is not None:
            if instance.backdrop_url != "":
                return instance.backdrop_url
        return None

    def get_poster_url(self):
        instance = self.moviedb.first()
        if instance is not None:
            if instance.backdrop_url != "":
                return instance.poster_url
        return None

    def get_wikipedia_url(self):
        instance = self.tastedb.first()
        if instance is not None:
            if instance.wikipedia != "":
                return instance.wikipedia
        return None

    def get_youtube_url(self):
        instance = self.tastedb.first()
        if instance is not None:
            if instance.youtube != "":
                return instance.youtube
        return None

    def __str__(self):
        return '%s - %s - %s' % (self.tconst, self.titleType, self.primaryTitle)