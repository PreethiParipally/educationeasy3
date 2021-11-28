# Generated by Django 3.2.9 on 2021-11-20 14:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appCourses', '0008_auto_20211120_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 20, 14, 57, 32, 252127, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='date_submitted',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 20, 14, 57, 32, 254177, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='registercourse',
            name='date_of_registering',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 20, 14, 57, 32, 256183, tzinfo=utc)),
        ),
    ]