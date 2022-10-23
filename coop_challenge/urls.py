from django.urls import path

from . import views

app_name = 'coop_challenge'

urlpatterns = [
    path('', views.viewIndex, name='index'),
    path('printlabel/<int:article>/', views.printLabel, name='printlabel'),
    path('printpdf/<int:article>/', views.printPdf, name='printpdf'),
    path('about/', views.viewAbout, name='about'),
    path('recommend/', views.viewRecommend, name='viewRecommend'),
    path('recommend/<str:query>', views.viewRecommResult, name='viewRecommResult'),
    path('search/<str:query>', views.viewSearch, name='viewSearch'),
]