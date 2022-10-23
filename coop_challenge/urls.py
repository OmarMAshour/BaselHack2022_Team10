from django.urls import path

from . import views

app_name = 'coop_challenge'

urlpatterns = [
    path('', views.viewIndex, name='index'),
    path('printlabell/', views.printLabell, name='printlabell'),
    path('printlabel/<int:article>/', views.printLabel, name='printlabel'),
    path('printpdf/<int:article>/', views.printPdf, name='printpdf'),
]