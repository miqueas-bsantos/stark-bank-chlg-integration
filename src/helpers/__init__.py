from exceptions import (BadRequest, ClientException, ConflictException,
                        ForbiddenException, NotFound)
import traceback
import json
from functools import wraps
import time
import sys
from os import environ
import logging
from ast import literal_eval


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
        message = None   
    finally:
        return message 

def return_api(payload, code: int, headers=None, additional=None, lambda_integration=True):
    """
        This function formats the response header for the API Gateway, 
        usually used in lambda functions not using the proxy integration

    Args:
        payload (dict): The response payload
        code (int): The response status code
        headers (dict): header response.
        additional (dict): additional response.
        lambda_integration (bool, optional): If the response is for a lambda integration. Defaults to True.

    Returns:
        dict: The response payload and headers
    """
    headers = {} if headers is None else headers
    additional = {} if additional is None else additional

    if lambda_integration:
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
    else:
        return payload


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
        except ClientException as error:
            traceback.print_exc()
            return return_api({"data": {
                "code": 400,
                "type": "/errors/internal-bad-request-error",
                "message": "bad request", 
                "detail": str(error)}
            }, 400)
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
        except ConflictException as error:
            traceback.print_exc()
            return return_api({"data": {"code": 409, "detail": str(error)}}, 409)

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