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

        return product_dict


def generate_html(product):
    pass


def create_label(product):
    generate_html(product)
    label_writer = LabelWriter("item_template.html",
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
