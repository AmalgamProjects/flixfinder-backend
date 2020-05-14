# Generated by Django 2.2.12 on 2020-05-14 17:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ff_api.fields.db
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ff_api', '0009_auto_20200514_1001'),
    ]

    operations = [
        migrations.CreateModel(
            name='FavouriteGenre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', ff_api.fields.db.DateTimeFieldWithoutMicroseconds(auto_now_add=True)),
                ('updated', ff_api.fields.db.DateTimeFieldWithoutMicroseconds(auto_now=True)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ff_api.Genre', verbose_name='name')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourite_genres', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
