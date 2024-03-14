# Generated by Django 4.2.3 on 2023-08-21 15:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_alter_message_edit_date_alter_message_pub_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='edit_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='message',
            name='pub_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 8, 21, 18, 23, 7, 537819)),
        ),
    ]
