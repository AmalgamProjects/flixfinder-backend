# Generated by Django 2.2.12 on 2020-05-15 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ff_api', '0019_auto_20200515_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moviedbtitle',
            name='backdrop_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='moviedbtitle',
            name='overview',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='moviedbtitle',
            name='poster_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='rapidtitle',
            name='image_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
