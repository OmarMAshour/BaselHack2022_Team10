from coop_challenge.fetcher import Fetcher
from coop_challenge.generator.label_generator import tryLabel
from coop_challenge.generator.info_generator import tryInfo
from django.shortcuts import render
from requests import request
from django.http import FileResponse


# Create your views here.
def viewIndex(request):
    # tryPDF()
    # return FileResponse(open(tryPDF(), 'rb'), content_type='application/pdf')

    return render(request, 'coop_challenge/scanner_1.html', {})


if __name__ == "__main__":
    id = "3760126362587"  # barcode

    fetcher = Fetcher()
    article_id = fetcher.find_article_id_by_barcode(id)

    # article_id = "1007906010"

    json = fetcher.find_by_article_ids([article_id])

    label_path = tryLabel(json[0].copy())
    info_path = tryInfo(json[0].copy())

    # return render(request, 'coop_challenge/base.html', {})
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
