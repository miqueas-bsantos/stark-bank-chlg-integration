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
import json
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
    event_payload = json.loads(get_message(event=event).get('body', "{}"))
    log = event_payload.get('event', {}).get('log', {})
    subscription = event_payload.get('event', {}).get('subscription', None)
    if subscription == 'invoice' and log.get('type', None) == 'credited':
        invoice = log.get('invoice')
        logger.info(f"Event Webhook received processing: {invoice}")
        transfer_amount = invoice.get('amount', 0)
        transfers = starkbank.transfer.create([
            starkbank.Transfer(
                amount=transfer_amount,
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
    else:
        response = {"message": "Webhook ignored"}
    status = 200
    return return_api(response, status)