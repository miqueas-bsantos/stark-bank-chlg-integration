# resolve the path to the root of the project and lambda aws imports
import sys, os
dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)
from helpers import (
    basic_exceptions, 
    get_logger, 
    return_api,
    get_message,
    auth_startbank
)
import boto3
# initialize the logger outside of the handler function avoiding multiple initializations
logger = get_logger("lambda_receive_webhook")
starkbank = auth_startbank()

@basic_exceptions
def handler(event, context):
    """
    This function is the main entry point for the lambda function
    @param event: The event data
    @param context: The context data
    """
    logger.info(f"Event Webhook received: {event}")
    # Get the queue
    transfer_amount = get_message(event=event)
    logger.info(f"Event Webhook received processing: {transfer_amount}")
    transfers = starkbank.transfer.create([
        starkbank.Transfer(
            amount=transfer_amount.get('event').get('log').get('amount', 0),
            tax_id='20.018.183/0001-80',
            name='Stark Bank S.A.',
            bank_code="20018183",
            branch_code="0001",
            account_number="6341320293482496",
            account_type="payment",
        )
    ])

    for transfer in transfers:
        logger.info(f"Created transfer: {transfer.id}")
    response = {"message": "Webhook processed successfully"}
    status = 200
    return return_api(response, status)