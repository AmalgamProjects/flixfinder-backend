"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movies or TV Shows that the user wants to watch.

"""

import uuid
import pprint

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

    cached_title_data = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='Unique watch')
        ]

    def _cache_title_data(self):
        if not self.cached_title_data and self.title is not None:
            if self.primaryTitle is None or self.primaryTitle == "":
                self.primaryTitle = self.title.primaryTitle
            if self.backdrop_url is None or self.backdrop_url == "":
                self.backdrop_url = self.title.get_backdrop_url()
            if self.poster_url is None or self.poster_url == "":
                self.poster_url = self.title.get_poster_url()
            self.cached_title_data = True
            self.save()

    def _ensure_url_is_secure(self, url):
        if url is not None:
            if url[:5] == 'http:':
                return 'https:' + url[5:]
        return url

    def get_primary_title(self):
        if self.primaryTitle is None or self.primaryTitle == "":
            self._cache_title_data()
        return self.primaryTitle

    def get_backdrop_url(self):
        if self.backdrop_url is None or self.backdrop_url == "":
            self._cache_title_data()
        return self._ensure_url_is_secure(self.backdrop_url)

    def get_poster_url(self):
        if self.poster_url is None or self.poster_url == "":
            self._cache_title_data()
        return self._ensure_url_is_secure(self.poster_url)


@receiver(post_save, sender=Watch)
def watch_saved_handler(sender, instance, created, **kwargs):
    # TODO remove from other lists if added to this list
    if created:
        Recommendation.update_recommendations_for_user(instance.user)
