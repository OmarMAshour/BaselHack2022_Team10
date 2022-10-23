# Generated by Django 4.1.2 on 2022-10-22 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coop_challenge', '0002_rename_scanned_wine_scannedwine'),
    ]

    operations = [
        migrations.AddField(
            model_name='scannedwine',
            name='label_file',
            field=models.FileField(blank=True, upload_to='media/label'),
        ),
        migrations.AddField(
            model_name='scannedwine',
            name='pdf_file',
            field=models.FileField(blank=True, upload_to='media/pdfs'),
        ),
    ]