# Generated by Django 3.2.9 on 2021-11-25 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0006_alter_result_time_taken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='time_taken',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
