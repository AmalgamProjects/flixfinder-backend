# Generated by Django 2.2.12 on 2020-05-15 00:03

from django.db import migrations, models
import django.db.models.deletion
import ff_api.fields.db
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('ff_api', '0012_auto_20200514_2136'),
    ]

    operations = [
        migrations.CreateModel(
            name='RapidTitle',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', ff_api.fields.db.DateTimeFieldWithoutMicroseconds(auto_now_add=True)),
                ('updated', ff_api.fields.db.DateTimeFieldWithoutMicroseconds(auto_now=True)),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('titleType', models.CharField(max_length=255)),
                ('image_url', models.URLField()),
                ('remote_id', models.CharField(db_index=True, max_length=255)),
                ('similar', models.ManyToManyField(related_name='rapid_similar', to='ff_api.Title')),
                ('tconst', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rapid', to='ff_api.Title')),
            ],
        ),
    ]