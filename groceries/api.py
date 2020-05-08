import logging
import os
import sys
import requests

grocy_config = {}


class GrocyAPIClient(object):

    base_url = None
    api_key = None

    def __init__(self, **kwds):

        if "GROCY_API_KEY" in os.environ:
            self.api_key = os.environ["GROCY_API_KEY"]

        if "GROCY_BASE_URL" in os.environ:
            self.base_url = os.environ["GROCY_BASE_URL"]

        for key in kwds:
            self.__dict__[key] = kwds[key]

        if self.base_url is None or self.api_key is None:
            # TODO: Logging
            logging.debug("Environmental variables not set correctly")
            pass
        else:
            self.headers = {
                "GROCY-API-KEY": self.api_key,
                "User-Agent": "Grocy-Handler",
            }

    def consume_barcode(self, barcode_string):
        path = f"/api/stock/products/by-barcode/{barcode_string}/consume"
        url = self.base_url + path
        json = {
            "amount": 1,
            "transaction_type": "consume",
            "spoiled": False,
        }
        response = requests.post(url, headers=self.headers, json=json)
        if response.status_code == 200:
            return response
        elif response.status_code == 400:
            logging.debug(f"Status Code is {response.status_code}")
            logging.debug(response.json())
