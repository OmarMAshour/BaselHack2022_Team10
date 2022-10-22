from django.shortcuts import render
from requests import request

# Create your views here.
def viewIndex(request):
    return render(request, 'coop_challenge/index2.html', {})