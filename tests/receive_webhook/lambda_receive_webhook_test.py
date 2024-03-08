from src.lambda_receive_webhook import handler
from unittest.mock import patch, MagicMock


@patch(f'src.lambda_receive_webhook.sqs.get_queue_by_name', return_value=MagicMock())
def test_lambda_handler(moock_sqs_get_queue_by_name):
    result = handler({"teste_message": 123}, {})
    assert result['statusCode'] == 200