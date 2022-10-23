import imp
from django.shortcuts import render
from requests import request
from coop_challenge.pdf_generator import tryPDF
from django.http import FileResponse
# Create your views here.
def viewIndex(request):
    tryPDF()
    # return FileResponse(open(tryPDF(), 'rb'), content_type='application/pdf')

    return render(request, 'coop_challenge/base.html', {})