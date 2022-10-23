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
    product_dict['sellPrice'] = product_dict["allPrices"][0]['sellPrice']
    product_dict['wineCharacter'] = product_dict["wineCharacter"].split(",")[0]
    del product_dict['allPrices']
    generate_html(product_dict)
    label_name = create_label()

    return label_name


def retrieve_wine_info():
    fetcher = Fetcher()
    product_dict = fetcher.find_for_labels(article_ids=["1000372018"])[0]
    product_dict['sellPrice'] = product_dict["allPrices"][0]['sellPrice']
    product_dict['wineCharacter'] = product_dict["wineCharacter"].split(",")[0]
    del product_dict['allPrices']
    return product_dict


def generate_html(product):
    f = open(html_link, "w")

    bottle_url = "https://svgsilh.com/png-512/150955.png"
    logo_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Coop.svg/2000px-Coop.svg.png"
    qr_url = generate_qr_link(product['code'])

    message = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="{css_link}">
    <meta charset="UTF-8">
    <title>Label</title>
</head>
<body>
<table style="font-family: sans-serif; border: 2px solid #FFA400">
    <tr>
        <td style=font-size:20px bgcolor="#FFA400" colspan = "4"><b> &nbsp; {product['name']}</b></td>
    </tr>
    <tr>
        <td width=80 ROWSPAN="7"><img src="{bottle_url}" height="150"></td>
    </tr>
    <tr>
        <td width="80">{product["yearOfVintage"]}</td>
        <td width="190">{product["wineCharacter"]}</td>
        <td ROWSPAN="5"><img src={qr_url} width="100" align="center"></td>
    </tr>
    <tr>
        <td><em>Origin:</em></td>
        <td>{product["wineOrigin"]}</td>
    </tr>
    <tr>
        <td><em>Grape:</em></td>
        <td>{product["grapesText"]}</td>
    </tr>
    <tr>
        <td><em>Maturity:</em></td>
        <td>{product["enjoyFrom"]} - {product["enjoyUntil"]}</td>
    </tr>
    <tr>
        <td><em>Alcohol:</em></td>
        <td>{product["alcohol"]}%</td>
    </tr>
    <tr>
        <td colspan ="2"><img src="{logo_url}" width="100"></td>
        <td style=font-size:20px><b>{product["sellPrice"]} CHF</b></td>
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


if __name__ == "__main__":
    product = retrieve_wine_info()
    generate_html(product)
    create_label()
