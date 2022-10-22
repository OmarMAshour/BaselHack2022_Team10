from django.urls import path

from . import views

app_name = 'coop_challenge'

urlpatterns = [
    path('', views.viewIndex, name='index'),
]