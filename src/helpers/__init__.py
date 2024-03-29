from exceptions import (BadRequest, ForbiddenException, NotFound)
import traceback
import json
from functools import wraps
import time
import sys
from os import environ
import logging
import uuid
import starkbank
import random


def get_logger(name: str):
    """
        Create a logger with the given name

    Args:
        name (str): The name of the logger

    Returns:
        Logger: The logger instance
    """
    logging.Formatter.converter = time.localtime
    formatter = logging.Formatter("%(levelname)s:%(funcName)s:%(lineno)s — %(message)s %(asctime)s")
    _logger = logging.getLogger(name)
    _logger.propagate = False
    if not _logger.hasHandlers():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        _logger.addHandler(console_handler)
        _logger.setLevel(logging.getLevelName(environ.get('LOG_LEVEL', 'INFO')))

    return _logger

def get_message(event: dict):
    """
        Get the first message from the event SQS messages
    Args:
        event (dict): The event data
    Returns:
        dict: The message payload
    """
    try:
        message = json.loads(event['Records'][0]['body'])
    except Exception as error:
        print(f"Error getting message: {error}")
        message = {}   
    finally:
        return message 

def return_api(payload, code: int, headers=None, additional=None):
    """
        This function formats the response header for the API Gateway, 
        usually used in lambda functions not using the proxy integration

    Args:
        payload (dict): The response payload
        code (int): The response status code
        headers (dict): header response.
        additional (dict): additional response.

    Returns:
        dict: The response payload and headers
    """
    headers = {} if headers is None else headers
    additional = {} if additional is None else additional

    return {
        "body": json.dumps(payload)
        if type(payload) is dict or type(payload) is list
        else payload,
        "statusCode": code,
        "headers": {
            **headers,
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True,
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Request-Method": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Request-Headers": "*",
        },
        **additional,
    }


def basic_exceptions(func):
    """
        This decorator catches the basic exceptions and returns the proper response
    Args:
        func: The function to be decorated
    Returns:
        func: The decorated function, otherwise the error response
    """
    @wraps(func)
    def wrapper(*args):
        try:
            return func(*args)

        except ForbiddenException as error:
            traceback.print_exc()
            return return_api(
                {"data": {
                    "code": 403,
                    "type": "/errors/internal-server-error",
                    "message": "deny access", 
                    "detail": str(error)}
                }, 403)
        except BadRequest as error:
            traceback.print_exc()
            return return_api({
                "data": {
                    "code": 400,
                    "type": "/errors/bad-request-exception",
                    "message": "Invalid parameters",
                    "detail": str(error)
                }
            }, 400)
        except NotFound as error:
            traceback.print_exc()
            return return_api({"data": {"code": 404, "detail": str(error)}}, 404)
        except Exception as error:

            traceback.print_exc()
            return return_api({
                "data": {
                    "code": 500,
                    "type": "/errors/internal-server-error",
                    "message": 'Internal server error',
                    "detail": str(error)
                }
            }, 500)

    return wrapper

def get_uuid():
    """
        Generate a UUID
    Returns:
        str: The UUID
    """
    return str(uuid.uuid4())

def get_random_persons():
    """
        Return persons to be processed
    Returns:
        List[dict]: The message payload
    """
    # random position list
    persons = [
        {
            "name": "John",
            "tax_id": "238.448.050-28",
            "tags": ["War supply", f"Invoice #{get_uuid()}"],
            "amount": random.randint(1, 100000),
        },        
        {
            "name": "Irene Solano Santiago Neto",
            "tax_id": "194.833.728-28",
            "tags": ["War supply", f"Invoice #{get_uuid()}"],
            "amount": random.randint(1, 100000),
        },
        {
            "name": "William R. Vasquez",
            "tax_id": "238.448.050-28",
            "tags": ["supply", f"Invoice #{get_uuid()}"],
            "amount": random.randint(1, 100000),
        },
        {
            "name": "Bianca Irene Salas Neto",
            "tax_id": "504.452.865-04",
            "tags": ["supply", f"Invoice #{get_uuid()}"],
            "amount": random.randint(1, 100000),
        },
        {
            "name": "Joana Lozano Serrano",
            "tax_id": "622.904.296-78",
            "tags": ["supply", f"Invoice #{get_uuid()}"],
            "amount": random.randint(1, 100000),
        },        
        {
            "name": "Ivan de Souza Filho",
            "tax_id": "336.458.331-53",
            "tags": ["supply", f"Invoice #{get_uuid()}"],
            "amount": random.randint(1, 100000),
        },
        {
            "name": "Emiliano Joaquin Soto",
            "tax_id": "680.104.959-30",
            "tags": ["supply", f"Invoice #{get_uuid()}"],
            "amount": random.randint(1, 100000),
        },
        {
            "name": "Sra. Samanta Salas Neto",
            "tax_id": "931.576.626-19",
            "tags": ["supply", f"Invoice #{get_uuid()}"],
            "amount": random.randint(1, 100000),
        },
        {
            "name": "Micaela Valência Jr.",
            "tax_id": "115.498.946-17",
            "tags": ["supply", f"Invoice #{get_uuid()}"],
            "amount": random.randint(1, 100000),
        },
        {
            "name": "Evandro Delatorre",
            "tax_id": "936.964.422-91",
            "tags": ["supply", f"Invoice #{get_uuid()}"],
            "amount": random.randint(1, 100000),
        },
        {
            "name": "Dr. Giovane Cordeiro Lutero",
            "tax_id": "619.728.043-40",
            "tags": ["supply", f"Invoice #{get_uuid()}"],
            "amount": random.randint(1, 100000),
        }            
    ]
    positions = [i for i in range(0, random.randint(8, len(persons) - 1))]
    random.shuffle(positions)
    return [persons[i] for i in positions]

def auth_startbank():
    """
        Start the bank authentication
    Returns:
        Object: The Starkbank object
    """
    # Get your private key from an environment variable or an encrypted database.
    # This is only an example of a private key content. You should use your own key.
    private_key_content = """some secret key here..."""

    project = starkbank.Project(
        environment=environ.get("ENV", "sandbox"),
        id=environ.get("STARK_ID", "6485521089953792"),
        private_key=private_key_content
    )
    starkbank.user = project
    return starkbank