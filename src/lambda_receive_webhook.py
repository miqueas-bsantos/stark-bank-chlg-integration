# resolve the path to the root of the project and lambda aws imports
import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from helpers import (
    basic_exceptions, 
    get_logger, 
    return_api
)
import boto3
# initialize the logger outside of the handler function avoiding multiple initializations
logger = get_logger("lambda_receive_webhook")
sqs = boto3.resource('sqs')


@basic_exceptions
def handler(event, context):
    """
    This function is the main entry point for the lambda function
    @param event: The event data
    @param context: The context data
    """
    logger.info(f"Event Webhook received: {event}")
    # Get the queue
    queue_name = f'starkbank-sqs-{os.environ.get("REGION")}-{os.environ.get("ACCOUNT")}-WebHookQueue'
    logger.info(f"Queue Name: {queue_name}")
    queue = sqs.get_queue_by_name(QueueName=queue_name)
    queue.send_message(MessageBody=str(event))

    response = {"message": "Webhook received"}
    status = 200
    return return_api(response, status)