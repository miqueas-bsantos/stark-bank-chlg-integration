# resolve the path to the root of the project and lambda aws imports
import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from helpers import (
    get_logger, 
    return_api,
    get_persons
)
import starkbank
# initialize the logger outside of the handler function avoiding multiple initializations
logger = get_logger("lambda_receive_webhook")



# Get your private key from an environment variable or an encrypted database.
# This is only an example of a private key content. You should use your own key.
private_key_content = """secret-key-content"""

project = starkbank.Project(
    environment=os.environ.get("ENV"),
    id=os.environ.get("STARK_ID"),
    private_key=private_key_content
)
starkbank.user = project

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
    invoices = starkbank.invoice.create([starkbank.Invoice(**person) for person in get_persons()])
    for invoice in invoices:
        logger.info(f"Created invoice: {invoice.id}")
    logger.info(f"Event ended: {response}")
    return return_api(response, status)