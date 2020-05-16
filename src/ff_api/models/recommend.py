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
from .rapid import RapidTitle

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

    primaryTitle = models.CharField(max_length=255, null=True, default=None)
    backdrop_url = models.URLField(null=True, default=None)
    poster_url = models.URLField(null=True, default=None)

    cached_title_data = models.BooleanField(default=False)

    class Meta:
        ordering = ['user', 'priority']

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

    def get_primary_title(self):
        if self.primaryTitle is None or self.primaryTitle == "":
            self._cache_title_data()
        return self.primaryTitle

    def get_backdrop_url(self):
        if self.backdrop_url is None or self.backdrop_url == "":
            self._cache_title_data()
        return self.backdrop_url

    def get_poster_url(self):
        if self.poster_url is None or self.poster_url == "":
            self._cache_title_data()
        return self.poster_url

    @staticmethod
    def _get_suggestions_from_list_item(item_instance):
        suggestions = []
        rapid_instance = item_instance.title.get_rapid()
        if rapid_instance is not None:
            if rapid_instance.similar.all().count() <= 0:
                rapid_instance = RapidTitle.populate_related_from_api(item_instance.title.tconst, rapid_instance)
            for title_instance in rapid_instance.similar.all():
                suggestions.append(title_instance)
        random.shuffle(suggestions)
        return suggestions

    @staticmethod
    def _remove_duplicate_suggestions(suggestions):
        result = []
        for item in suggestions:
            if not item:
                continue
            tconst_string = item.tconst
            duplicate = False
            for kept in result:
                if kept.tconst == tconst_string:
                    duplicate = True
                    break
            if not duplicate:
                result.append(item)
        return result

    @staticmethod
    def update_recommendations_for_user(user_instance: User):

        pprint.pprint('user has %s suggestions' % user_instance.recommendation.get_queryset().count())

        suggestions = []

        if len(suggestions) < 100:
            pprint.pprint('making suggestions from favourites')
            for favourite in user_instance.favourites.all():
                suggestions += Recommendation._get_suggestions_from_list_item(favourite)

        suggestions = Recommendation._remove_duplicate_suggestions(suggestions)
        if len(suggestions) < 100:
            pprint.pprint('making suggestions from watch')
            for want_to_watch in user_instance.watch.all():
                suggestions += Recommendation._get_suggestions_from_list_item(want_to_watch)

        suggestions = Recommendation._remove_duplicate_suggestions(suggestions)
        if len(suggestions) < 100:
            pprint.pprint('making suggestions from seen')
            for already_seen in user_instance.seen.all():
                if already_seen.liked and not already_seen.disliked:
                    suggestions += Recommendation._get_suggestions_from_list_item(already_seen)

        suggestions = Recommendation._remove_duplicate_suggestions(suggestions)
        if len(suggestions) < 100:
            pprint.pprint('making suggestions from seen')
            for already_seen in user_instance.seen.all():
                if not already_seen.liked and not already_seen.disliked:
                    suggestions += Recommendation._get_suggestions_from_list_item(already_seen)

        # TODO use the data from user_instance.favourite_genres.all()

        pprint.pprint('making random suggestions')
        suggestions += Recommendation.random_good_movies(100 - len(suggestions))
        suggestions = Recommendation._remove_duplicate_suggestions(suggestions)

        if len(suggestions) > 100:
            suggestions = suggestions[:100]

        pprint.pprint('deleting old suggestions')
        user_instance.recommendation.get_queryset().all().delete()

        pprint.pprint('saving new suggestions')

        priority = 0
        for suggestion in suggestions:
            if suggestion is None:
                continue
            # noinspection PyBroadException
            try:
                r = Recommendation(
                    user=user_instance,
                    priority=priority,
                    title=suggestion,
                    primaryTitle=suggestion.primaryTitle,
                    backdrop_url=suggestion.get_backdrop_url(),
                    poster_url=suggestion.get_poster_url()
                )
                r.save()
                priority += 1
            except Exception:
                pass

    @staticmethod
    def random_good_movies(number=1):
        result = []
        for tconst in Recommendation.random_good_movie_tconsts(number):
            result.append(Title.objects.filter(tconst=tconst).first())
        return result

    @staticmethod
    def random_good_movie_tconsts(number=1):
        return random.sample([
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
        ], number)
