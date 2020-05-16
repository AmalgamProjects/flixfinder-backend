"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movies or TV Shows that the user wants to watch.

"""

import uuid
import pprint
import random

from django.contrib.auth.models import User
from django.db import models

from ..data import movies, tv_shows
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
    def get_suggestions_from_title_instance(title_instance):
        suggestions = []
        rapid_instance = title_instance.get_rapid()
        if rapid_instance is not None:
            if rapid_instance.similar.all().count() <= 0:
                rapid_instance = RapidTitle.populate_related_from_api(title_instance.tconst, rapid_instance)
            for title_instance in rapid_instance.similar.all():
                suggestions.append(title_instance)
        random.shuffle(suggestions)
        return suggestions

    @staticmethod
    def get_suggestions_from_tconst(tconst):
        title_instance = Title.objects.filter(tconst=tconst).first()
        if title_instance:
            return Recommendation.get_suggestions_from_title_instance(title_instance)
        return []

    @staticmethod
    def _get_suggestions_from_list_item(item_instance):
        return Recommendation.get_suggestions_from_title_instance(item_instance.title)

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

        pprint.pprint('making random movie suggestions')
        suggestions += Recommendation.random_good_movies(50 - len(suggestions))
        suggestions = Recommendation._remove_duplicate_suggestions(suggestions)

        pprint.pprint('making random tvshow suggestions')
        suggestions += Recommendation.random_good_tvshow(50 - len(suggestions))

        suggestions += Recommendation.random_good_movies(10)
        suggestions += Recommendation.random_good_tvshow(10)
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
    def random_good_tvshow(number=1):
        result = []
        for tconst in Recommendation.random_good_tvshow_tconsts(number):
            result.append(Title.objects.filter(tconst=tconst).first())
        return result

    @staticmethod
    def random_good_movie_tconsts(number=1):
        if number < 1:
            number = 1
        if number >= len(movies):
            number = len(movies) - 1
        result = random.sample(movies, number)
        random.shuffle(result)
        return result

    @staticmethod
    def random_good_tvshow_tconsts(number=1):
        if number < 1:
            number = 1
        if number >= len(tv_shows):
            number = len(tv_shows) - 1
        result = random.sample(tv_shows, number)
        random.shuffle(result)
        return result
