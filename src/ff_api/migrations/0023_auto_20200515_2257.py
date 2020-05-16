# Generated by Django 2.2.12 on 2020-05-15 22:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ff_api', '0022_externalresponse'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='backdrop_url',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='title',
            name='image_url',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='title',
            name='poster_url',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='title',
            name='summary',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='title',
            name='vote_average',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='title',
            name='vote_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='title',
            name='wikipedia_url',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='title',
            name='youtube_url',
            field=models.URLField(default=None, null=True),
        ),
    ]