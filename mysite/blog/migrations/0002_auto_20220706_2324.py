# Generated by Django 3.2.5 on 2022-07-07 03:24

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='create_date',
        ),
        migrations.AddField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 7, 3, 24, 36, 41775, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 7, 7, 3, 24, 36, 42772, tzinfo=utc)),
        ),
    ]
