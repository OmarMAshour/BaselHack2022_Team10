from django.db import models

# Create your models here.
class Scanned_Wine(models.Model):
    
    json = models.TextField()