import logging
import groceries.api

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    consume = groceries.api.GrocyAPIClient()
    response = consume.consume_barcode("12345")
