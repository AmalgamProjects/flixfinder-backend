"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

"""

import uuid
import requests
import pprint

from django.conf import settings
from django.db import models
from urllib.parse import quote_plus

from .imdb import Title
from ..fields import DateTimeFieldWithoutMicroseconds


class TasteTitle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = DateTimeFieldWithoutMicroseconds(auto_now_add=True, editable=False)
    updated = DateTimeFieldWithoutMicroseconds(auto_now=True)
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='tastedb', null=True)
    name = models.CharField(max_length=255, db_index=True)
    type = models.CharField(max_length=255)
    teaser = models.TextField()
    wikipedia = models.URLField()
    youtube = models.URLField()

    def __str__(self):
        return 'TasteDive: %s - %s' % (self.type, self.name)

    @staticmethod
    def populate_from_api(query):
        """
        https://tastedive.com/read/api
        """
        response = requests.get(
            '%s/similar?k=%s&q=%s&info=1' % (
                settings.TD_API_HOST,
                settings.TD_API_KEY,
                quote_plus(query)
            ))
        response.raise_for_status()
        data = response.json()
        for result_type in ['Info', 'Results']:
            for result in data['Similar'][result_type]:
                name = result['Name']  # 'Primal Fear'
                pprint.pprint(name)
                instance, created = TasteTitle.objects.get_or_create(
                    name=name,
                    defaults={
                        'name': name,  # 'Primal Fear'
                        'type': result['Type'],  # 'movie'
                        'teaser': result['wTeaser'],  # 'Primal Fear is a 1996 American legal ....'
                        'wikipedia': result['wUrl'],  # 'http://en.wikipedia.org/wiki/Primal_Fear_(film)'
                        'youtube': result['yUrl'],  # 'https://www.youtube-nocookie.com/embed/PnmTi7hSjrA'
                    },
                )
                if created:
                    title = Title.objects.filter(primaryTitle=name).first()
                    instance.tconst = title
                    instance.save()
