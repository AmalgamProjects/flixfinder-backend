"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movie and TV Show data from the IMDB datasets.

https://datasets.imdbws.com/
https://www.imdb.com/interfaces/

NOTICE: This data is obtained under a Non-Commercial Use License

"""

import uuid

from django.db import models

from ..fields import SeparatedValuesField


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

    def get_image_url(self):
        instance = self.rapid.first()
        if instance is not None:
            if instance.image_url != "":
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


class Name(models.Model):
    nconst = models.CharField(primary_key=True, max_length=255)
    primaryName = models.CharField(max_length=255, db_index=True)
    birthYear = models.IntegerField(null=True)
    deathYear = models.IntegerField(null=True)
    primaryProfession = SeparatedValuesField(default="", blank=True, null=True)
    knownForTitles = models.ManyToManyField(Title, blank=True)


class Crew(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='crew')
    directors = models.ManyToManyField(Name, related_name='directors')
    writers = models.ManyToManyField(Name, related_name='writers')


class Episode(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE)
    parentTconst = models.CharField(max_length=255, db_index=True)
    seasonNumber = models.IntegerField(null=True)
    episodeNumber = models.IntegerField(null=True)


class Principal(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='principals')
    ordering = models.IntegerField()
    nconst = models.ForeignKey(Name, on_delete=models.CASCADE, related_name='principals')
    category = models.CharField(max_length=255, db_index=True)
    job = models.CharField(max_length=255, null=True)
    characters = models.TextField(null=True)


class Rating(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='rating')
    averageRating = models.DecimalField(decimal_places=2, max_digits=10)
    numVotes = models.IntegerField()
