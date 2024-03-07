# resolve the path to the root of the project and lambda aws imports
import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from helpers import (
    basic_exceptions, 
    get_logger, 
    return_api
)

# initialize the logger outside of the handler function avoiding multiple initializations
logger = get_logger("lambda_receive_webhook")

@basic_exceptions
def handler(event, context):
    """
    This function is the main entry point for the lambda function
    @param event: The event data
    @param context: The context data
    """
    logger.info(f"Event Webhook received: {event}")

    response = {"message": "Webhook received"}
    status = 200
    return return_api(response, status)