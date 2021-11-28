# Generated by Django 3.2.9 on 2021-11-26 13:06

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appCourses', '0033_auto_20211126_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 26, 13, 6, 45, 957615, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='date_submitted',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 26, 13, 6, 45, 958616, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='course',
            name='end_date',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='registercourse',
            name='date_of_registering',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 26, 13, 6, 45, 959614, tzinfo=utc)),
        ),
    ]