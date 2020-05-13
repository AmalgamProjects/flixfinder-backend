"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movie and TV Show data from the IMDB datasets.

https://datasets.imdbws.com/
https://www.imdb.com/interfaces/

NOTICE: This data is obtained under a Non-Commercial Use License

"""

from django.db import models

from ..fields import SeparatedValuesField


class Title(models.Model):
    tconst = models.CharField(primary_key=True, max_length=255)
    titleType = models.CharField(max_length=255)
    primaryTitle = models.CharField(max_length=255)
    originalTitle = models.CharField(max_length=255)
    isAdult = models.CharField(max_length=1)
    startYear = models.CharField(max_length=4)
    endYear = models.CharField(null=True, max_length=4)
    runtimeMinutes = models.CharField(max_length=10)
    genres = SeparatedValuesField()


class Name(models.Model):
    nconst = models.CharField(primary_key=True, max_length=255)
    primaryName = models.CharField(max_length=255)
    birthYear = models.IntegerField()
    deathYear = models.IntegerField(null=True)
    primaryProfession = SeparatedValuesField()
    knownForTitles = SeparatedValuesField()


class Crew(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE)
    directors = SeparatedValuesField()
    writers = SeparatedValuesField()


class Episode(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE)
    parentTconst = models.CharField(max_length=255)
    seasonNumber = models.IntegerField(null=True)
    episodeNumber = models.IntegerField(null=True)


class Principal(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE)
    ordering = models.IntegerField()
    nconst = models.ForeignKey(Name, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    job = models.CharField(max_length=255, null=True)
    characters = models.TextField(null=True)


class Rating(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE)
    averageRating = models.DecimalField(decimal_places=2, max_digits=10)
    numVotes = models.IntegerField()
