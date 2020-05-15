# Generated by Django 2.2.12 on 2020-05-15 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ff_api', '0017_auto_20200515_0037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='parentTconst',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='name',
            name='primaryName',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='principal',
            name='category',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='title',
            name='endYear',
            field=models.CharField(db_index=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='title',
            name='isAdult',
            field=models.CharField(db_index=True, max_length=1),
        ),
        migrations.AlterField(
            model_name='title',
            name='originalTitle',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='title',
            name='primaryTitle',
            field=models.CharField(db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='title',
            name='runtimeMinutes',
            field=models.CharField(db_index=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='title',
            name='startYear',
            field=models.CharField(db_index=True, max_length=4),
        ),
        migrations.AlterField(
            model_name='title',
            name='titleType',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
