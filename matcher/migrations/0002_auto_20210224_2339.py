# Generated by Django 3.0.8 on 2021-02-24 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matcher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='field_of_study',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='education',
            name='educationLevel',
            field=models.CharField(max_length=50),
        ),
    ]
