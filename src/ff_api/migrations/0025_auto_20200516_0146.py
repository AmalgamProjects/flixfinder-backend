# Generated by Django 2.2.12 on 2020-05-16 01:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ff_api', '0024_auto_20200516_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='title',
            name='api_cached_moviedb',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='title',
            name='api_cached_rapid',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='title',
            name='api_cached_tastedb',
            field=models.BooleanField(default=False),
        ),
    ]
