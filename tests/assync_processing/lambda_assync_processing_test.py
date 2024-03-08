from src.lambda_assync_processing import handler
from pytest import fixture

@fixture
def mock_event_payload():
    import json
    """
        This function mocks the expected event payload

    Yields:
        dict: mock_payload event
    """
    mock_payload = {
        "Records": [
            {
                "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": json.dumps({"body": json.dumps(
                        {
                            "event":{
                                "created":"2024-03-07T22:05:48.857797+00:00",
                                "id":"6507058002132992",
                                "log":{
                                    "id":"5728520546287616",
                                    "invoice":{
                                        "amount":34093,
                                        "name":"Sra. Samanta Salas Neto",
                                        "nominalAmount":34093,
                                        "status":"created",
                                        "tags":[
                                        "supply",
                                        "invoice #9bdfb85c-b0e8-46a5-9dcb-7f36efe34082"
                                        ],
                                        "taxId":"931.576.626-19",
                                    },
                                    "type":"created"
                                },
                                "subscription":"invoice",
                                "workspaceId":"6276476441722880"
                            }
                    }
                )}),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1545082649183",
                    "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                    "ApproximateFirstReceiveTimestamp": "1545082649185"
                },
                "messageAttributes": {},
                "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:111122223333:my-queue",
                "awsRegion": "us-east-1"
            }
        ]
    }
    yield mock_payload
    del mock_payload


@fixture
def mock_event_payload_credit():
    import json
    """
        This function mocks the expected event payload

    Yields:
        dict: mock_payload event
    """
    mock_payload = {
        "Records": [
            {
                "messageId": "059f36b4-87a3-44ab-83d2-661975830a7d",
                "receiptHandle": "AQEBwJnKyrHigUMZj6rYigCgxlaS3SLy0a...",
                "body": json.dumps({"body": json.dumps(
                        {
                            "event":{
                                "created":"2024-03-07T22:05:48.857797+00:00",
                                "id":"6507058002132992",
                                "log":{
                                    "id":"5728520546287616",
                                    "invoice":{
                                        "amount":34093,
                                        "name":"Sra. Samanta Salas Neto",
                                        "nominalAmount":34093,
                                        "status":"paid",
                                        "tags":[
                                        "supply",
                                        "invoice #9bdfb85c-b0e8-46a5-9dcb-7f36efe34082"
                                        ],
                                        "taxId":"931.576.626-19",
                                    },
                                    "type":"credited"
                                },
                                "subscription":"invoice",
                                "workspaceId":"6276476441722880"
                            }
                    }
                )}),
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1545082649183",
                    "SenderId": "AIDAIENQZJOLO23YVJ4VO",
                    "ApproximateFirstReceiveTimestamp": "1545082649185"
                },
                "messageAttributes": {},
                "md5OfBody": "098f6bcd4621d373cade4e832627b4f6",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:111122223333:my-queue",
                "awsRegion": "us-east-1"
            }
        ]
    }
    yield mock_payload
    del mock_payload    

def test_lambda_handler(mock_event_payload, mock_event_payload_credit):
    result = handler(mock_event_payload, {})
    result_credited = handler(mock_event_payload_credit, {})
    assert result['statusCode'] == 200
    assert result_credited['statusCode'] == 200