# Generated by Django 2.2.12 on 2020-05-13 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ff_api', '0002_auto_20200513_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='name',
            name='knownForTitles',
            field=models.ManyToManyField(blank=True, to='ff_api.Title'),
        ),
    ]