# Generated by Django 3.2.9 on 2021-11-19 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='actual_marks',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
