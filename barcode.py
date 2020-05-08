import logging
import groceries.api
import barcodescanner.scan

consume = groceries.api.GrocyAPIClient()


def main():
    scanner = barcodescanner.scan.Scan()
    line = scanner.PollScanner()
    if line != None:
        response = consume.consume_barcode(line)
        logging.debug(response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    while True:
        main()
