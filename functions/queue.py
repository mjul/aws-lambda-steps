import boto3
import json
import os


def send_message(event, context):
    """Send a message to the application's queue"""
    message = json.dumps({"data": event['data']})
    queue = get_application_queue()
    response = queue.send_message(MessageBody=message)
    return {
        "statusCode": 200,
        "body": json.dumps("OK")
    }


def get_application_queue():
    sqs = boto3.resource('sqs')
    return sqs.get_queue_by_name(QueueName=os.environ['SQS_APPLICATION_QUEUE'])
