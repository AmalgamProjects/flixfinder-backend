"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

"""

import uuid
import requests
import pprint

from django.conf import settings
from django.db import models
from urllib.parse import quote_plus

from .title import Title
from ..fields import DateTimeFieldWithoutMicroseconds


class RapidTitle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = DateTimeFieldWithoutMicroseconds(auto_now_add=True, editable=False)
    updated = DateTimeFieldWithoutMicroseconds(auto_now=True)
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE, related_name='rapid', null=True)
    title = models.CharField(max_length=255, db_index=True)
    titleType = models.CharField(max_length=255)
    image_url = models.URLField(blank=True, null=True)
    remote_id = models.CharField(max_length=255, db_index=True)

    similar = models.ManyToManyField(Title, related_name='rapid_similar')

    def __str__(self):
        return 'Rapid: %s' % self.title

    @staticmethod
    def call_api(method, params=None):
        response = requests.get(
            'https://%s/%s' % (settings.RAPID_API_HOST, method),
            headers={
                'x-rapidapi-host': settings.RAPID_API_HOST,
                'x-rapidapi-key': settings.RAPID_API_KEY

            },
            params=params
        )
        response.raise_for_status()
        return response.json()

    @staticmethod
    def populate_from_api(tconst_string):
        """
        https://rapidapi.com/apidojo/api/imdb8/endpoints
        """
        instance = RapidTitle.populate_one_from_api(tconst_string)
        RapidTitle.populate_related_from_api(tconst_string)
        return instance

    @staticmethod
    def populate_one_from_api(tconst_string, create_missing_title=True):
        instance = None
        try:
            data = RapidTitle.call_api('title/get-base', {'tconst': tconst_string})
            # pprint.pprint(data)
            instance, created = RapidTitle.objects.get_or_create(
                remote_id=tconst_string,
                defaults={
                    'title': data['title'],
                    'titleType': data['titleType'],
                    'image_url': data['image']['url'],
                    'remote_id': tconst_string,
                },
            )
            if create_missing_title:
                title_instance, created = Title.objects.update_or_create(
                    tconst=tconst_string,
                    defaults={
                        'tconst': tconst_string,
                        'titleType': data['titleType'],
                        'primaryTitle': data['title'],
                        'originalTitle': data['title'],
                        'startYear': data['year'],
                    }
                )
            else:
                title_instance = Title.objects.filter(tconst=tconst_string).first()
            instance.tconst = title_instance
            instance.save()
            pprint.pprint('RapidTitle %s ... %s' % (data['title'], instance.tconst))
        except Exception as e:
            pprint.pprint(e)
        return instance

    @staticmethod
    def populate_related_from_api(tconst_string):
        instance = RapidTitle.objects.filter(remote_id=tconst_string).first()
        if not instance:
            RapidTitle.populate_one_from_api(tconst_string, create_missing_title=False)
            instance = RapidTitle.objects.filter(remote_id=tconst_string).first()
            if not instance:
                return
        if instance.tconst is not None:
            data = RapidTitle.call_api('title/get-more-like-this', {'tconst': tconst_string})
            # pprint.pprint(data)
            for ref in data:
                related_tconst = ref.split('/')[2]
                RapidTitle.populate_one_from_api(related_tconst, create_missing_title=False)
                related_title = Title.objects.filter(tconst=related_tconst).first()
                if related_title:
                    instance.similar.add(related_title)

    @staticmethod
    def populate_top_rated_movies():
        data = RapidTitle.call_api('title/get-top-rated-movies', None)
        # pprint.pprint(data)
        for item in data:
            tconst_string = item['id'].split('/')[2]
            RapidTitle.populate_from_api(tconst_string)

    @staticmethod
    def create_title_from_rapid(tconst_string):
        instance_rapid = RapidTitle.objects.filter(tconst=tconst_string).first()
        instance_title = Title.objects.filter(tconst=tconst_string).first()
        if instance_rapid is None or instance_title is None:
            pprint.pprint('Generating missing Title for %s' % tconst_string)
            RapidTitle.populate_one_from_api(tconst_string, create_missing_title=True)
