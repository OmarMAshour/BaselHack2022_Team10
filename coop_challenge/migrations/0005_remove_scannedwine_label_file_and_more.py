# Generated by Django 4.1.2 on 2022-10-23 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coop_challenge', '0004_alter_scannedwine_alcohol_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scannedwine',
            name='label_file',
        ),
        migrations.RemoveField(
            model_name='scannedwine',
            name='pdf_file',
        ),
    ]
