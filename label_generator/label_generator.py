from data_fetcher.fetcher import Fetcher
import pdfkit


def retrieve_wine_info():
    fetcher = Fetcher()
    product_dict = fetcher.find_for_labels(article_ids=["1007906010"])[0]
    product_dict['sellPrice'] = product_dict["allPrices"][0]['sellPrice']
    del product_dict['allPrices']
    return product_dict


def generate_html(product):
    f = open("label_template/label_template.html", "w")

    message = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css">
    <meta charset="UTF-8">
    <title>Label</title>
</head>
<body>
<table bordercolor="FFA400">
    <tr>
        <td bgcolor="#FFA400" colspan="4">{product['name']}</td>
    </tr>
    <tr>
        <td ROWSPAN="7"><img src="bottle.png" height="100"></td>
    </tr>
    <tr>
        <td>{product["yearOfVintage"]}</td>
        <td>{product["wineCharacter"]}</td>
        <td ROWSPAN="5"><img src="qr.svg" width="100"></td>
    </tr>
    <tr>
        <td><em>Origin:</em></td>
        <td>{product["wineOrigin"]}</td>
    </tr>
    <tr>
        <td><em>Grape Type:</em></td>
        <td>{product["grapesText"]}</td>
    </tr>
    <tr>
        <td><em>Optimal Maturity:</em></td>
        <td>{product["enjoyFrom"]} - {product["enjoyUntil"]}</td>
    </tr>
    <tr>
        <td><em>Alcohol Percentage:</em></td>
        <td>{product["alcohol"]}</td>
    </tr>
    <tr>
        <td colspan ="2"><img src="logo.png" width="100"></td>
        <td>{product["sellPrice"]}</td>
      </tr>
    </table>
</body>
</html>"""

    f.write(message)
    f.close()


def create_label(prod):
    path = "label_template/label_template.html"
    pdfkit.from_file(path, "output/label1.pdf", css="label_template/style.css")


if __name__ == "__main__":
    product = retrieve_wine_info()
    generate_html(product)
    create_label(product)
