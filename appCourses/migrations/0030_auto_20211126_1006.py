# Generated by Django 3.2.9 on 2021-11-26 04:36

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appCourses', '0029_auto_20211125_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 26, 4, 36, 31, 581612, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='date_submitted',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 26, 4, 36, 31, 582612, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='registercourse',
            name='date_of_registering',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 26, 4, 36, 31, 582612, tzinfo=utc)),
        ),
    ]