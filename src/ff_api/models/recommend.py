"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movies or TV Shows that the user wants to watch.

"""

import uuid
import pprint

from django.contrib.auth.models import User
from django.db import models

from .title import Title

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

        top_movies = [
            'tt0111161',
            'tt0068646',
            'tt0071562',
            'tt0468569',
            'tt0050083',
            'tt0108052',
            'tt0167260',
            'tt0110912',
            'tt0060196',
            'tt0120737',
            'tt0137523',
            'tt0109830',
            'tt1375666',
            'tt0080684',
            'tt0167261',
            'tt0133093',
            'tt0099685',
            'tt0073486',
            'tt0047478',
            'tt0114369',
            'tt0118799',
            'tt0317248',
            'tt0102926',
            'tt0038650',
            'tt0076759',
            'tt0120815',
            'tt6751668',
            'tt0245429',
            'tt0120689',
            'tt0816692',
            'tt0110413',
            'tt0114814',
            'tt0056058',
            'tt0110357',
            'tt0120586',
            'tt0253474',
            'tt0088763',
            'tt0103064',
            'tt0027977',
            'tt0054215',
            'tt0172495',
            'tt0021749',
            'tt0407887',
            'tt1675434',
            'tt2582802',
            'tt0482571',
            'tt0064116',
            'tt0095327',
            'tt0034583',
            'tt0047396',
            'tt0095765',
            'tt7286456',
            'tt0078748',
            'tt0078788',
            'tt0209144',
            'tt0082971',
            'tt0032553',
            'tt0405094',
            'tt1853728',
            'tt0050825',
            'tt0081505',
            'tt4154756',
            'tt0910970',
            'tt0043014',
            'tt4633694',
            'tt0119698',
            'tt0057012',
            'tt0364569',
            'tt0051201',
            'tt4154796',
            'tt1345836',
            'tt0066763',
            'tt0087843',
            'tt0090605',
            'tt5311514',
            'tt2380307',
            'tt0169547',
            'tt0112573',
            'tt0082096',
            'tt1187043',
            'tt0114709',
            'tt0057565',
            'tt0986264',
            'tt8579674',
            'tt0086190',
            'tt0086879',
            'tt0105236',
            'tt0361748',
            'tt0119217',
            'tt0062622',
            'tt0052357',
            'tt0180093',
            'tt0022100',
            'tt5074352',
            'tt0338013',
            'tt8267604',
            'tt0033467',
            'tt2106476',
            'tt0093058',
            'tt0053125',
        ]

        for movie in top_movies:
            pass

        raise NotImplementedError('Not done this yet')
