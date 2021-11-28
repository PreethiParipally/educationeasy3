# Generated by Django 3.2.9 on 2021-11-26 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0007_alter_result_time_taken'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='correct',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='percent',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='result',
            name='wrong',
            field=models.PositiveIntegerField(default=0),
        ),
    ]