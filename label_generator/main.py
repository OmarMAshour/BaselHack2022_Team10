from blabel import LabelWriter
import json


def retrieve_wine_info(json_file):
    # Read the json data
    with open('data.json') as f:
        data = json.load(f)
        product_data = data['products'][0]

        product_dict = dict()

        product_dict['name'] = product_data['name_en']
        product_dict['yearOfVintage'] = product_data['yearOfVintage']
        product_dict['wineMaker'] = product_data['wineMaker']
        product_dict['wineCharacter'] = product_data['wineCharacter']
        product_dict['wineOrigin'] = product_data['wineOrigin']
        product_dict['grapesText'] = product_data['grapesText']
        product_dict['enjoyFrom'] = product_data['enjoyFrom']
        product_dict['enjoyUntil'] = product_data['enjoyUntil']
        product_dict['alcohol'] = product_data['alcohol']
        product_dict['sellPrice'] = product_data["allPrices"][0]['sellPrice']

        return product_dict


def generate_html(product):
    f = open("label_template.html", "w")

    message = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <link rel="stylesheet" href="style.css">
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
    # f.write("<img src=\"{{ label_tools.qr_code(sample_id)}}\"/>\n")
    # f.write(f"<span class='label'>\n")
    # f.write(f"\t{product['name']} <br/>\n")
    # f.write(f"\tCoop challenge <br/>\n")
    # f.write(f"</span>\n")

    f.write(message)
    f.close()


def create_label(product):
    generate_html(product)
    label_writer = LabelWriter("label_template.html",
                               default_stylesheets=("style.css",))
    records = [
        dict(sample_id="s01", sample_name="Sample 1")
    ]

    label_writer.write_labels(records, target='label.pdf')


def main():
    product = retrieve_wine_info('data.json')
    create_label(product)


if __name__ == "__main__":
    main()
