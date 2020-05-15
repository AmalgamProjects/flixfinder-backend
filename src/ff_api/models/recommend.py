"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movies or TV Shows that the user wants to watch.

"""

import uuid
import pprint

from django.contrib.auth.models import User
from django.db import models

from .imdb import Title

from ..fields import DateTimeFieldWithoutMicroseconds


class Recommendation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = DateTimeFieldWithoutMicroseconds(auto_now_add=True, editable=False)
    updated = DateTimeFieldWithoutMicroseconds(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recommendation',
    )
    priority = models.IntegerField(default=1)
    title = models.ForeignKey(Title, verbose_name="tconst", on_delete=models.CASCADE)

    @staticmethod
    def update_recommendations_for_user(user: User):
        # favourite_genres = user.favourite_genres.all()
        # favourites = user.favourites.all()
        # watch = user.watch.all()
        # seen = user.seen.all()
        # pprint.pprint(favourites)
        # pprint.pprint(favourite_genres)
        # pprint.pprint(watch)
        # pprint.pprint(seen)

        raise NotImplementedError('Not done this yet')
