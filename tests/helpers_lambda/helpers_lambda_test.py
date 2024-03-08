from src.helpers import (
    get_logger,
    return_api,
    basic_exceptions,
    get_uuid,
    auth_startbank,
    get_random_persons,
    get_message
)
from exceptions import (ForbiddenException, NotFound, BadRequest)

# def test_get_logger():
#     assert isinstance(get_logger("test"), LoggerAdapter) == True

def test_get_message():
    assert get_message(None) == {}

def test_basic_exceptions():
    @basic_exceptions
    def test():
        1/0
    assert test()['statusCode'] == 500

def test_forbidden_exception():
    @basic_exceptions
    def test():
        raise ForbiddenException("test")
    assert test()['statusCode'] == 403

def test_not_found_exception():
    @basic_exceptions
    def test():
        raise NotFound("test")
    assert test()['statusCode'] == 404

def test_bad_request_exception():
    @basic_exceptions
    def test():
        raise BadRequest({"payload_response": "test"})
    assert test()['statusCode'] == 400
