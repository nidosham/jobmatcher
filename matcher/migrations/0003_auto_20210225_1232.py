# Generated by Django 3.0.8 on 2021-02-25 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0002_auto_20210224_2339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='experience',
            old_name='username',
            new_name='person',
        ),
    ]