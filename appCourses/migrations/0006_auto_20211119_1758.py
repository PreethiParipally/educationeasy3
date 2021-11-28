# Generated by Django 3.2.9 on 2021-11-19 12:28

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appCourses', '0005_auto_20211119_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 12, 28, 35, 697677, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='assignmentsubmission',
            name='date_submitted',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 12, 28, 35, 697677, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='registercourse',
            name='date_of_registering',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 19, 12, 28, 35, 697677, tzinfo=utc)),
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('file', models.FileField(blank=True, null=True, upload_to='')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appCourses.course')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]