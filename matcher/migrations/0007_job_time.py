# Generated by Django 3.1.4 on 2021-04-15 23:43

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0006_auto_20210416_0017'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='time',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, max_length=200),
        ),
    ]
