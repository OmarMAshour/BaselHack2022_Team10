from blabel import LabelWriter
from data_fetcher.fetcher import Fetcher


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
    <link rel="stylesheet" href="label_template/style.css">
    <meta charset="UTF-8">
    <title>Label</title>
</head>
<body>
<table>
    <tr>
        <td bgcolor="#FFA400" colspan="3">{product['name']}</td>
    </tr>
    <tr>
        <td>{product["yearOfVintage"]}</td>
        <td>{product["wineMaker"]}</td>
        <td><img width="200" src="img.png" /></td>
        <!-- <td>{product["wineCharacter"]}</td> -->
    </tr>
    <tr>
        <td>Origin:</td>
        <td>{product["wineOrigin"]}</td>
        <td><img width="200" src="img.png" /></td>
    </tr>
    <tr>
        <td>Grape Type:</td>
        <td>{product["grapesText"]}</td>
    </tr>
    <tr>
        <td>Optimal Maturity:</td>
        <td>{product["enjoyFrom"] - product["enjoyUntil"]}</td>
    </tr>
    <tr>
        <td>Alcohol Percentage:</td>
        <td>{product["alcohol"]}</td>
        <!-- <td>{product["sellPrice"]}</td> -->
    </tr>
    </body>
</table>
</html>
    """

    f.write(message)
    f.close()


def create_label(prod):
    generate_html(prod)
    label_writer = LabelWriter("label_template/label_template.html",
                               default_stylesheets=("label_template/style.css",))
    records = [
        dict(sample_id="s01", sample_name="Sample 1")
    ]

    label_writer.write_labels(records, target='output/label.pdf')


if __name__ == "__main__":
    product = retrieve_wine_info()
    create_label(product)
