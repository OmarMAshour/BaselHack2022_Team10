from django.contrib import admin
from .models import ScannedWine
# Register your models here.
admin.site.register(ScannedWine)
admin.site.site_header = 'Coop Wine Manager Administration'