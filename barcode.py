import logging
import groceries.api as groceries
import barcodescanner.scan as barcode


def main():
    grocy = groceries.GrocyAPIClient()
    while True:
        scanner = barcode.Scan()
        line = scanner.PollScanner()
        if line != None:
            response = grocy.consume_barcode(line)
            logging.debug(response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
