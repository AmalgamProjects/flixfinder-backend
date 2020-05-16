"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movies or TV Shows that the user wants to watch.

"""

import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .title import Title
from .recommend import Recommendation

from ..fields import DateTimeFieldWithoutMicroseconds


class Watch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = DateTimeFieldWithoutMicroseconds(auto_now_add=True, editable=False)
    updated = DateTimeFieldWithoutMicroseconds(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='watch',
    )
    title = models.ForeignKey(Title, verbose_name="tconst", on_delete=models.CASCADE)

    primaryTitle = models.CharField(max_length=255, null=True, default=None)
    backdrop_url = models.URLField(null=True, default=None)
    poster_url = models.URLField(null=True, default=None)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='Unique watch')
        ]

    def get_primary_title(self):
        if self.primaryTitle is None or self.primaryTitle == "":
            if self.title is not None:
                self.primaryTitle = self.title.primaryTitle
        return self.primaryTitle

    def get_backdrop_url(self):
        if self.backdrop_url is None or self.backdrop_url == "":
            if self.title is not None:
                self.backdrop_url = self.title.get_backdrop_url()
        return self.backdrop_url

    def get_poster_url(self):
        if self.poster_url is None or self.poster_url == "":
            if self.title is not None:
                self.poster_url = self.title.get_poster_url()
        return self.poster_url


@receiver(post_save, sender=Watch)
def watch_saved_handler(sender, instance, **kwargs):
    Recommendation.update_recommendations_for_user(instance.user)
