# Generated by Django 4.2.3 on 2023-08-23 14:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0004_alter_message_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='dislikes',
            field=models.ManyToManyField(blank=True, null=True, related_name='disliking', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='likes',
            field=models.ManyToManyField(blank=True, null=True, related_name='liking', to=settings.AUTH_USER_MODEL),
        ),
    ]
