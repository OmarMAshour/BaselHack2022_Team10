from unicodedata import name
from coop_challenge.fetcher import Fetcher
from coop_challenge.generator.label_generator import tryLabel
from coop_challenge.generator.info_generator import tryInfo
from django.shortcuts import render
from requests import request
from django.http import FileResponse
from .models import ScannedWine
import json
# Create your views here.
def viewIndex(request):
    # tryPDF()
    # return FileResponse(open(tryPDF(), 'rb'), content_type='application/pdf')

    return render(request, 'coop_challenge/scanner_1.html', {})


# if __name__ == "__main__":
    # id = "3760126362587"  # barcode

    # fetcher = Fetcher()
    # article_id = fetcher.find_article_id_by_barcode(id)

    # # article_id = "1007906010"

    # json = fetcher.find_by_article_ids([article_id])

    # label_path = tryLabel(json[0].copy())
    # info_path = tryInfo(json[0].copy())

    # return render(request, 'coop_challenge/base.html', {})
def printLabel(request, article):
    # tryPDF()
    # return FileResponse(open(tryPDF(), 'rb'), content_type='application/pdf')
    json_obj = fetchandsave(article)
    label_path = tryLabel(json.loads(json_obj))
    return FileResponse(open(label_path, 'rb'), content_type='application/pdf')


def viewRecommend(request):
    return render(request, 'coop_challenge/recommend.html', {})





def viewRecommResult(request, query):
    query = query.replace('&&&', ' ')
    filtered = ScannedWine.objects.distinct().filter(goesWithText_de__icontains=query).all()
    results = []
    for f in filtered:
        entry = {'name': f.name, 'wineOrigin': f.wineOrigin, 'maturity': f.maturity, 'goesWith' : f.goesWithText_de, 'article_id': f.article_id}
        results.append(entry)


    return render(request,'coop_challenge/recommend.html', {'results':filtered})

def viewSearch(request, query):
    query = query.replace('&&&', ' ')
    filtered = ScannedWine.objects.distinct().filter(name__icontains=query).all()
    


    return render(request,'coop_challenge/search.html', {'results':filtered})


def viewAbout(request):
    return render(request, 'coop_challenge/about_us.html', {})

def printPdf(request, article):
    # tryPDF()
    # return FileResponse(open(tryPDF(), 'rb'), content_type='application/pdf')

    json_obj = fetchandsave(article)
    label_path = tryInfo(json.loads(json_obj))
    return FileResponse(open(label_path, 'rb'), content_type='application/pdf')

def fetchandsave(article):
    fetcher = Fetcher()
    if len(str(article)) == 13:
        article = fetcher.find_article_id_by_barcode(article)
    old_scanned = ScannedWine.objects.filter(article_id= article)
    if len(old_scanned) == 1:
        # return json.loads(old_scanned[0].json)
        return old_scanned[0].json
    json_str = fetcher.find_by_article_ids([article])
    json_str = json_str[0]
    new_scan = ScannedWine(name=json_str['name'], article_id = json_str['code'], alcohol=json_str['alcohol'], sellPrice=json_str['allPrices'][0]['sellPrice'], maturity=str(json_str['enjoyFrom'])+' - ' +str(json_str['enjoyUntil']), goesWithText=json_str['goesWithText'], goesWithText_de=json_str['goesWithText_de'],  goesWithText_fr=json_str['goesWithText_fr'], goesWithText_it=json_str['goesWithText_it'], servingTemperature=json_str['servingTemperature'], wineCharacter=json_str['wineCharacter'], wineMaker=json_str['wineMaker'], wineOrigin=json_str['wineOrigin'], yearOfVintage=json_str['yearOfVintage'], json=json.dumps(json_str))
    new_scan.save()
    return json.dumps(json_str)