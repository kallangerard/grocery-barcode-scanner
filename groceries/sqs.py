import concurrent.futures
import random
from uuid import uuid1

import boto3

sqs = boto3.client("sqs")

# TODO: Environ for QueueNames 
consume_url = sqs.get_queue_url(QueueName="groceryConsume.fifo")
purchase_url = sqs.get_queue_url(QueueName="groceryPurchase.fifo")


def consume_product(barccode_string):
    uuidOne = str(uuid1())
    response = sqs.send_message(
        QueueUrl=consume_url["QueueUrl"],
        MessageBody=barcode_string,
        MessageGroupId="grocy",
        MessageDeduplicationId=uuidOne,
    )
    return response


def purchase_product(barcode_string):
    uuidOne = str(uuid1())
    response = sqs.send_message(
        QueueUrl=purchase_url["QueueUrl"],
        MessageBody=barcode_string,
        MessageGroupId="grocy",
        MessageDeduplicationId=uuidOne,
    )
    return response

def threaded_send(barcode_string)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        submitted = executor.submit(purchase_product, str(barcode_string))
    
