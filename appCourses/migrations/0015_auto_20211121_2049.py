# Generated by Django 3.2.9 on 2021-11-21 15:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appCourses', '0014_auto_20211121_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 21, 15, 19, 20, 332210, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='date_submitted',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 21, 15, 19, 20, 333210, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='registercourse',
            name='date_of_registering',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 21, 15, 19, 20, 335273, tzinfo=utc)),
        ),
    ]
