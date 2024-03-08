from collections import namedtuple
from unittest.mock import MagicMock
from src.lambda_random_invoice import handler


def test_lambda_handler():
    result = handler({}, {})
    assert result['statusCode'] == 200