"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movies or TV Shows that the user wants to watch.

"""

import uuid
import pprint
import random

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

    class Meta:
        ordering = ['user', 'priority']

    def get_backdrop_url(self):
        if self.title is not None:
            return self.title.get_backdrop_url()
        return None

    def get_poster_url(self):
        if self.title is not None:
            return self.title.get_poster_url()
        return None

    @staticmethod
    def _get_suggestions_from_list_item(item_instance):
        suggestions = []
        rapid_title = item_instance.title.get_rapid()
        if rapid_title is not None:
            for title_instance in rapid_title.similar.all():
                suggestions.append(title_instance)
        random.shuffle(suggestions)
        return suggestions

    @staticmethod
    def update_recommendations_for_user(user_instance: User):

        suggestions = []

        if len(suggestions) < 100:
            for favourite in user_instance.favourites.all():
                suggestions += Recommendation._get_suggestions_from_list_item(favourite)

        if len(suggestions) < 100:
            for want_to_watch in user_instance.watch.all():
                suggestions += Recommendation._get_suggestions_from_list_item(want_to_watch)

        if len(suggestions) < 100:
            for already_seen in user_instance.seen.all():
                if already_seen.liked and not already_seen.disliked:
                    suggestions += Recommendation._get_suggestions_from_list_item(already_seen)

        if len(suggestions) < 100:
            for already_seen in user_instance.seen.all():
                if not already_seen.liked and not already_seen.disliked:
                    suggestions += Recommendation._get_suggestions_from_list_item(already_seen)

        # TODO use the data from user_instance.favourite_genres.all()

        while len(suggestions) < 100:
            suggestions.append(Recommendation.random_good_movie())

        if len(suggestions) > 100:
            suggestions = suggestions[:100]

        user_instance.recommendation.set([], clear=True)

        priority = 0
        for suggestion in suggestions:
            r = Recommendation(user=user_instance, priority=priority, title=suggestion)
            r.save()
            priority += 1

    @staticmethod
    def random_good_movie():
        return Title.objects.filter(tconst=Recommendation.random_good_movie_tconst()).first()

    @staticmethod
    def random_good_movie_tconst():
        random.choice([
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
        ])
