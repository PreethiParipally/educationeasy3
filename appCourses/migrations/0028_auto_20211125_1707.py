# Generated by Django 3.2.9 on 2021-11-25 11:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appCourses', '0027_auto_20211125_1255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='duration',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 25, 11, 37, 44, 466868, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='date_submitted',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 25, 11, 37, 44, 468124, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='registercourse',
            name='date_of_registering',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 25, 11, 37, 44, 470166, tzinfo=utc)),
        ),
    ]
