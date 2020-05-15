"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movies or TV Shows that the user has already seen

"""

import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .title import Title
from .recommend import Recommendation

from ..fields import DateTimeFieldWithoutMicroseconds


class Seen(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = DateTimeFieldWithoutMicroseconds(auto_now_add=True, editable=False)
    updated = DateTimeFieldWithoutMicroseconds(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='seen',
    )
    title = models.ForeignKey(Title, verbose_name="tconst", on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)
    disliked = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='Unique seen')
        ]

    def get_primary_title(self):
        if self.title is not None:
            return self.title.primaryTitle
        return None

    def get_backdrop_url(self):
        if self.title is not None:
            return self.title.get_backdrop_url()
        return None

    def get_poster_url(self):
        if self.title is not None:
            return self.title.get_poster_url()
        return None


@receiver(post_save, sender=Seen)
def seen_saved_handler(sender, instance, **kwargs):
    Recommendation.update_recommendations_for_user(instance.user)
