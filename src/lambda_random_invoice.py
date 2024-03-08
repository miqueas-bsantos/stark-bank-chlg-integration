# resolve the path to the root of the project and lambda aws imports
import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from helpers import (
    get_logger, 
    return_api,
    get_random_persons,
    auth_startbank
)
# initialize the logger outside of the handler function avoiding multiple initializations
logger = get_logger("lambda_receive_webhook")
starkbank = auth_startbank()

def handler(event, context):
    """
    This function is the main entry point for the lambda function
    @param event: The event data
    @param context: The context data
    """
    logger.info(f"Event starting: {event}")
    response = {"message": "Webhook processed successfully"}
    status = 200
    # Create invoices
    invoices = starkbank.invoice.create([starkbank.Invoice(**person) for person in get_random_persons()])
    for invoice in invoices:
        logger.info(f"Created invoice: {invoice.id}")
    logger.info(f"Event ended: {response}")
    return return_api(response, status)