"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movies or TV Shows that the user wants to watch.

"""

import uuid

from django.contrib.auth.models import User
from django.db import models

from .imdb import Title

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
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'title'], name='Unique watch')
        ]
