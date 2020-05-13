from django.db import models


class SeparatedValuesField(models.TextField):

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ',')
        super(SeparatedValuesField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value: return
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not value: return
        assert (isinstance(value, list) or isinstance(value, tuple))
        return self.token.join([unicode(s) for s in value])

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def from_db_value(self, value, expression, connection, context):
        value = self.to_python(value)
        return value if value is not None else ''


# Create your models here.
class Title(models.Model):
    tconst = models.CharField(primary_key=True, max_length=255)
    titleType = models.CharField(max_length=255)
    primaryTitle = models.CharField(max_length=255)
    originalTitle = models.CharField(max_length=255)
    isAdult = models.CharField(max_length=1)
    startYear = models.CharField(max_length=4)
    endYear = models.CharField(null=True, max_length=4)
    runtimeMinutes = models.CharField(max_length=10)
    genres = SeparatedValuesField()


class Name(models.Model):
    nconst = models.CharField(primary_key=True, max_length=255)
    primaryName = models.CharField(max_length=255)
    birthYear = models.IntegerField()
    deathYear = models.IntegerField(null=True)
    primaryProfession = SeparatedValuesField()
    knownForTitles = SeparatedValuesField()


class Crew(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE)
    directors = SeparatedValuesField()
    writers = SeparatedValuesField()


class Episode(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE)
    parentTconst = models.CharField(max_length=255)
    seasonNumber = models.IntegerField(null=True)
    episodeNumber = models.IntegerField(null=True)


class Principal(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE)
    ordering = models.IntegerField()
    nconst = models.ForeignKey(Name, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    job = models.CharField(max_length=255, null=True)
    characters = models.TextField(null=True)


class Rating(models.Model):
    tconst = models.ForeignKey(Title, on_delete=models.CASCADE)
    averageRating = models.DecimalField(decimal_places=2, max_digits=10)
    numVotes = models.IntegerField()
