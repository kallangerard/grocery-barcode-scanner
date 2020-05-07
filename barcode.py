import groceries.api

consume = groceries.api.GrocyAPIClient()
response = consume.consume_barcode("12345")
print(response.status_code)
