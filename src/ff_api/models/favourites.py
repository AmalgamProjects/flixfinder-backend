"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movies or TV Shows that the user has said they love.

"""

import uuid

from django.contrib.auth.models import User
from django.db import models

from .imdb import Title, Genre

from ..fields import DateTimeFieldWithoutMicroseconds


class Favourite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = DateTimeFieldWithoutMicroseconds(auto_now_add=True, editable=False)
    updated = DateTimeFieldWithoutMicroseconds(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourites',
    )
    title = models.ForeignKey(Title, verbose_name="tconst", on_delete=models.CASCADE)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='Unique favourite')
        ]


class FavouriteGenre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = DateTimeFieldWithoutMicroseconds(auto_now_add=True, editable=False)
    updated = DateTimeFieldWithoutMicroseconds(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favourite_genres',
    )
    genre = models.ForeignKey(Genre, verbose_name="name", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'genre'], name='Unique favourite genre')
        ]