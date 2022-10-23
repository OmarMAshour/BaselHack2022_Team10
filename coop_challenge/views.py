import imp
from django.shortcuts import render
from requests import request
from coop_challenge.pdf_generator import tryPDF
from django.http import FileResponse
# Create your views here.
def viewIndex(request):
    # tryPDF()
    # return FileResponse(open(tryPDF(), 'rb'), content_type='application/pdf')

    return render(request, 'coop_challenge/scanner_1.html', {})

def printLabel(request, article):
    # tryPDF()
    # return FileResponse(open(tryPDF(), 'rb'), content_type='application/pdf')
    print(article)
    print(article)
    print(article)
    print(article)
    print(article)
    print(article)
    print(article)
    print(article)
    return render(request, 'coop_challenge/scanner_1.html', {})

def printLabell(request):
    # tryPDF()
    # return FileResponse(open(tryPDF(), 'rb'), content_type='application/pdf')

    return render(request, 'coop_challenge/scanner_1.html', {})

def printPdf(request, article):
    # tryPDF()
    # return FileResponse(open(tryPDF(), 'rb'), content_type='application/pdf')

    return render(request, 'coop_challenge/scanner_1.html', {})