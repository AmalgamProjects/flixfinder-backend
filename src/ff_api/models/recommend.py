"""
https://docs.djangoproject.com/en/2.2/topics/db/models/

Movies or TV Shows that the user wants to watch.

"""

import uuid
import pprint
import random

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from ..data import movies, tv_shows
from .title import Title
from .rapid import RapidTitle

from ..fields import DateTimeFieldWithoutMicroseconds


# noinspection PyShadowingBuiltins
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
    def _remove_excluded(suggestions, excluded):
        result = []
        for item in suggestions:
            if not item:
                continue
            tconst_string = item.tconst
            keep = True
            for excluded_tconst in excluded:
                if excluded_tconst == tconst_string:
                    keep = False
                    break
            if keep:
                result.append(item)
        return result

    # noinspection PyBroadException
    @staticmethod
    def update_recommendations_for_user(user_instance: User):

        pprint.pprint('user has %s suggestions' % user_instance.recommendation.get_queryset().count())

        maximum = 100

        suggestions = []

        excluded_tconsts = []
        for already_seen in user_instance.seen.all().prefetch_related('title'):
            if already_seen.title:
                excluded_tconsts.append(already_seen.title.tconst)

        pprint.pprint('making suggestions from favourites')
        for favourite in user_instance.favourites.all().prefetch_related('title'):
            suggestions += Recommendation._get_suggestions_from_list_item(favourite)
            if len(suggestions) > int(maximum * 1.5):
                break
        pprint.pprint('new suggestions count = %s' % len(suggestions))

        pprint.pprint('making suggestions from watch')
        for want_to_watch in user_instance.watch.all().prefetch_related('title'):
            suggestions += Recommendation._get_suggestions_from_list_item(want_to_watch)
            if len(suggestions) > int(maximum * 1.5):
                break
        pprint.pprint('new suggestions count = %s' % len(suggestions))

        if len(suggestions) < maximum:
            pprint.pprint('making suggestions from seen')
            for already_seen in user_instance.seen.all().prefetch_related('title'):
                if already_seen.liked and not already_seen.disliked:
                    suggestions += Recommendation._get_suggestions_from_list_item(already_seen)
                    if len(suggestions) > int(maximum * 1.5):
                        break
            pprint.pprint('new suggestions count = %s' % len(suggestions))

        if len(suggestions) < maximum:
            pprint.pprint('making suggestions from seen')
            for already_seen in user_instance.seen.all().prefetch_related('title'):
                if not already_seen.liked and not already_seen.disliked:
                    suggestions += Recommendation._get_suggestions_from_list_item(already_seen)
                    if len(suggestions) > int(maximum * 1.5):
                        break
            pprint.pprint('new suggestions count = %s' % len(suggestions))

        if len(suggestions) < maximum:
            pprint.pprint('making suggestions from old suggestions')
            for old_suggestion in user_instance.recommendation.get_queryset().prefetch_related('title'):
                suggestions += Recommendation._get_suggestions_from_list_item(old_suggestion)
                if len(suggestions) > int(maximum * 1.5):
                    break
            pprint.pprint('new suggestions count = %s' % len(suggestions))

        if len(suggestions) < maximum:
            pprint.pprint('making suggestions from new suggestions')
            for suggestion in suggestions:
                suggestions += Recommendation.get_suggestions_from_title_instance(suggestion)
                if len(suggestions) > int(maximum * 1.5):
                    break
            suggestions = Recommendation._remove_duplicate_suggestions(suggestions)
            pprint.pprint('new suggestions count = %s' % len(suggestions))

        # TODO use the data from user_instance.favourite_genres.all()

        if len(suggestions) > 0:
            suggestions = Recommendation._remove_duplicate_suggestions(suggestions)
            suggestions = Recommendation._remove_excluded(suggestions, excluded_tconsts)

        if len(suggestions) < maximum:
            pprint.pprint('making random suggestions')
            suggestions += Recommendation.random_good_movies(int(maximum / 2))
            suggestions += Recommendation.random_good_tvshow(int(maximum / 2))

            suggestions = Recommendation._remove_duplicate_suggestions(suggestions)
            suggestions = Recommendation._remove_excluded(suggestions, excluded_tconsts)
            pprint.pprint('new suggestions count = %s' % len(suggestions))

        suggested_movies = []
        suggested_tv = []

        # Ensure that we have a fix of Movies and TV shows
        for suggestion in suggestions:
            if suggestion.titleType[:2] == 'tv':
                suggested_tv.append(suggestion)
            elif suggestion.titleType == 'movie':
                suggested_movies.append(suggestion)
        count_movie = len(suggested_movies)
        count_tv = len(suggested_tv)
        pprint.pprint(
            'new suggestions count = move:%s tv:%s total:%s' % (
                count_movie, count_tv, len(suggestions)
            )
        )
        if len(suggested_movies) > maximum:
            suggested_movies = suggested_movies[:maximum]
        if len(suggested_movies) > maximum:
            suggested_tv = suggested_tv[:maximum]
        if count_movie < 50:
            pprint.pprint('adding more random movies')
            suggested_movies += Recommendation.random_good_movies(50)
            suggested_movies = Recommendation._remove_duplicate_suggestions(suggested_movies)
        if count_tv < 50:
            pprint.pprint('adding more random tv shows')
            suggested_tv += Recommendation.random_good_movies(50)
            suggested_tv = Recommendation._remove_duplicate_suggestions(suggested_tv)
        suggestions = suggested_movies + suggested_tv
        suggestions = Recommendation._remove_duplicate_suggestions(suggestions)

        pprint.pprint('deleting old suggestions')
        try:
            if user_instance.recommendation.get_queryset().count():
                user_instance.recommendation.get_queryset().all().delete()
        except Exception:
            pass

        pprint.pprint('saving %s new suggestions' % len(suggestions))

        priority = 0
        new_recommendations = []
        for suggestion in suggestions:
            if suggestion is None:
                continue
            try:
                r = Recommendation(
                    user=user_instance,
                    priority=priority,
                    title=suggestion,
                    primaryTitle=suggestion.primaryTitle,
                    backdrop_url=suggestion.get_backdrop_url(),
                    poster_url=suggestion.get_poster_url()
                )
                # r.save()
                new_recommendations.append(r)
                priority += 1
            except Exception:
                pass
        user_instance.recommendation.set(new_recommendations, bulk=False, clear=True)

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


@receiver(post_save, sender=User)
def user_saved_handler(sender, instance, created, **kwargs):
    if created:
        Recommendation.update_recommendations_for_user(instance)
