"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

External API response caching

"""

import json
import requests
import uuid

from django.conf import settings
from django.db import models

from ..fields import DateTimeFieldWithoutMicroseconds


class ExternalResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = DateTimeFieldWithoutMicroseconds(auto_now_add=True, editable=False)
    updated = DateTimeFieldWithoutMicroseconds(auto_now=True)
    query = models.CharField(max_length=255, db_index=True)
    response = models.TextField(default='')

    @staticmethod
    def call_api_url(url, headers=None, params=None):
        if params is None:
            params = {}
        params['api_key'] = settings.MDB_API_KEY
        prepared = requests.Request('GET', url, headers=headers, params=params).prepare()
        instance = ExternalResponse.objects.filter(query=prepared.url).first()
        if instance is None:
            with requests.Session() as session:
                response = session.send(prepared)
                response.raise_for_status()
                instance = ExternalResponse(
                    query=prepared.url,
                    response=json.dumps(response.json())
                )
                instance.save()
        return json.loads(instance.response)
