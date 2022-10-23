import os
import pdfkit

from coop_challenge.fetcher import Fetcher

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html_link = f"{ROOT_DIR}/generator/label_template/label_template.html"
css_link = f"{ROOT_DIR}/generator/label_template/style.css"
label_output_filename = "label.pdf"
label_output_folder_path = f"{ROOT_DIR}/output/"
label_output_file_path = f"{ROOT_DIR}/output/{label_output_filename}"

if not os.path.exists(label_output_folder_path):
    os.makedirs(label_output_folder_path)


def tryLabel(product_dict):
    generate_html(product_dict)
    label_name = create_label()

    return label_name


def generate_html(product):
    f = open(html_link, "w")

    bottle_url = "https://svgsilh.com/png-512/150955.png"
    logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Coop.svg/2000px-Coop.svg.png"
    qr_url = generate_qr_link(product['code'])

    name = product.get('name', 'NotProvided').strip()
    yearOfVintage = product.get('yearOfVintage', 'NotProvided')
    wineCharacter = product.get('wineCharacter', 'NotProvided')
    wineOrigin = product.get('wineOrigin', 'NotProvided')
    grapesText = product.get('grapesText', 'NotProvided')
    enjoyFrom = product.get('enjoyFrom', 'NotProvided')
    enjoyUntil = product.get('enjoyUntil', 'NotProvided')
    alcohol = product.get('alcohol', 'NotProvided')
    allPrices = product.get('allPrices', 'NotProvided')
    if allPrices == 'NotProvided':
        sellPrice = 'NotProvided'
    else:
        sellPrice = allPrices[0]['sellPrice']

    message = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="{css_link}">
    <meta charset="UTF-8">
    <title>Label</title>
</head>
<body>
<table id="table" style="font-family: sans-serif; border: 2px solid #FFA400">
    <tr>
        <td colspan = "4" id="name"><b> &nbsp; {name}</b></td>
    </tr>
    <tr>
        <td ROWSPAN="7" id="bottle"><img src="{bottle_url}" height="150"></td>
    </tr>
    <tr>
        <td width="100" id="year">{yearOfVintage}</td>
        <td width="300">{wineCharacter}</td>
        <td ROWSPAN="5"><img src={qr_url} id="qr"></td>
    </tr>
    <tr>
        <td id="origin"><em>Origin:</em></td>
        <td>{wineOrigin}</td>
    </tr>
    <tr>
        <td id="grape"><em>Grape:</em></td>
        <td>{grapesText}</td>
    </tr>
    <tr>
        <td id="maturity"><em>Maturity:</em></td>
        <td>{enjoyFrom} - {enjoyUntil}</td>
    </tr>
    <tr>
        <td id="alcohol"><em>Alcohol:</em></td>
        <td>{alcohol}%</td>
    </tr>
    <tr>
        <td colspan ="2" id="logo"><img src="{logo_url}" width="100"></td>
        <td id="price""><b>{sellPrice} CHF</b></td>
      </tr>
    </table>
</body>
</html>"""

    f.write(message)
    f.close()


def create_label():
    pdfkit.from_file(html_link, label_output_file_path, css=css_link, options={"enable-local-file-access": ""})

    return label_output_file_path


def generate_qr_link(productId):
    link_to_wine = "https://www.coop.ch/p/" + productId
    QR_API = f'https://api.qrserver.com/v1/create-qr-code/?size=210x210&data={link_to_wine}'
    return QR_API


def retrieve_wine_info():
    fetcher = Fetcher()
    product_dict = fetcher.find_for_labels(article_ids=["1000372018"])[0]
    product_dict['sellPrice'] = product_dict["allPrices"][0]['sellPrice']
    product_dict['wineCharacter'] = product_dict["wineCharacter"].split(",")[0]
    del product_dict['allPrices']
    return product_dict


if __name__ == "__main__":
    product = retrieve_wine_info()
    generate_html(product)
    create_label()
