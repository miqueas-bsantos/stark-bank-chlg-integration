class BadRequest(Exception):
    dict = None

    def __init__(self, *args: object) -> None:
        if len(args) and type(args[0]) == dict:
            self.dict = args[0]
        super().__init__(*args)


class NotFound(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ForbiddenException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ClientException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class ConflictException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class CallOrderException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class MalConfiguredException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class RetryException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
