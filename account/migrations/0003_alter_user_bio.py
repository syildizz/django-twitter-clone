# Generated by Django 4.2.3 on 2023-08-27 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_user_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(max_length=150),
        ),
    ]
