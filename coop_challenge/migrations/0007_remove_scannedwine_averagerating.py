# Generated by Django 4.1.2 on 2022-10-23 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coop_challenge', '0006_remove_scannedwine_goeswithtext_en'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scannedwine',
            name='averageRating',
        ),
    ]