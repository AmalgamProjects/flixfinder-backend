"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movies or TV Shows that the user has already seen

"""

import uuid

from django.contrib.auth.models import User
from django.db import models

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

    # TODO = foreign key to a movie or tv show
