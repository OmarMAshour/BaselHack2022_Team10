from distutils.command.upload import upload
from pyexpat import model
from django.db import models

# Create your models here.
class ScannedWine(models.Model):
    name = models.TextField(blank = True)
    article_id = models.TextField(blank = True)
    alcohol = models.TextField(blank = True)
    sellPrice = models.TextField(blank = True)
    averageRating = models.TextField(blank = True)
    maturity = models.TextField(blank = True)
    goesWithText = models.TextField(blank = True)
    goesWithText_de = models.TextField(blank = True)
    # goesWithText_en = models.TextField(blank = True)
    goesWithText_fr = models.TextField(blank = True)
    goesWithText_it = models.TextField(blank = True)
    servingTemperature = models.TextField(blank = True)
    wineCharacter = models.TextField(blank = True)
    wineMaker = models.TextField(blank = True)
    wineOrigin = models.TextField(blank = True)
    yearOfVintage = models.TextField(blank = True)
    json = models.TextField(blank = True)
    # pdf_file = models.FileField(upload_to='media/pdfs', blank = True)
    # label_file = models.FileField(upload_to='media/label', blank=True)
    def __str__(self) -> str:
        return self.name