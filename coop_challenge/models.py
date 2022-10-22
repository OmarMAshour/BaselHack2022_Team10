from django.db import models

# Create your models here.
class ScannedWine(models.Model):
    name = models.TextField()
    article_id = models.TextField()
    alcohol = models.TextField()
    sellPrice = models.TextField()
    averageRating = models.TextField()
    maturity = models.TextField()
    goesWithText = models.TextField()
    goesWithText_de = models.TextField()
    goesWithText_en = models.TextField()
    goesWithText_fr = models.TextField()
    goesWithText_it = models.TextField()
    servingTemperature = models.TextField()
    wineCharacter = models.TextField()
    wineMaker = models.TextField()
    wineOrigin = models.TextField()
    yearOfVintage = models.TextField()
    json = models.TextField()

    def __str__(self) -> str:
        return self.name