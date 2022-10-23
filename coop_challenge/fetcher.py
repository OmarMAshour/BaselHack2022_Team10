"""
Fetcher module, this is where all the data fetch from Wine API happens
"""
import os

import requests
import configparser
from typing import List, Dict
import ast


class Fetcher:

    def __init__(self) -> None:
        # read api configuration (secret)
        self.api_conf = configparser.RawConfigParser()
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.api_conf.read(f"{ROOT_DIR}/conf/api.conf")
        api_details = dict(self.api_conf.items("Wine Info"))
        self.info_url = api_details['info_url']
        self.barcode_url = api_details["barcode_url"]
        self.api_key = api_details['api_key']

        # read keys configuration for label and info sheet
        self.keys_conf = configparser.RawConfigParser()
        self.keys_conf.read(f"{ROOT_DIR}/conf/keys.conf")
        self.label_keys = ast.literal_eval(self.keys_conf.get("Keys", "label"))

    def find_article_id_by_barcode(self, barcode: str) -> str:
        return self.find_by_barcode(barcode=barcode)["code"]

    def find_by_barcode(self, barcode: str) -> Dict:
        """
        Fetch wine brief by a barcode
        """

        params = {"lang": "de", "gtin": barcode}
        headers = {"APIKey": self.api_key}

        response = requests.get(
            self.barcode_url,
            params=params,
            headers=headers
        )

        return response.json()

    def find_for_labels(self, article_ids: List[str]) -> List[Dict]:
        return self.find_by_article_ids(article_ids, self.label_keys)

    def find_by_article_ids(self, article_ids: List[str], keys: List[str] = None) -> List[Dict]:
        """
        Fetch a list of wine info by a list of article_ids
        """

        params = {"codes": article_ids}
        headers = {"APIKey": self.api_key}

        response = requests.get(
            self.info_url,
            params=params,
            headers=headers
        )

        products = response.json()["products"]

        if keys is None:
            return products

        return [{key: product[key] for key in keys} for product in products]


if __name__ == "__main__":
    fetcher = Fetcher()
    print(fetcher.find_article_id_by_barcode("3760126362587"))
    items = fetcher.find_for_labels(article_ids=["1007906010"])

    print(items)

# def fetchData(article_id):
#     fetcher = Fetcher()
#     items = fetcher.find_for_labels(article_ids=[article_id])
#     return items[0]
