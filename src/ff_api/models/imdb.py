"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movie and TV Show data from the IMDB datasets.

https://datasets.imdbws.com/
https://www.imdb.com/interfaces/

NOTICE: This data is obtained under a Non-Commercial Use License

"""

from django.db import models

from .title import Title
from .name import Name


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
