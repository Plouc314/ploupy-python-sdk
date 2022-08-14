class PloupyException(Exception):
    """
    Base exception for all ploupy-defined exceptions
    """


class InvalidStateException(PloupyException):
    """
    Exception raised when a state is invalid
    """


class InvalidGameIdException(PloupyException):
    pass


class InvalidServerDataFormatException(PloupyException):
    """
    Exception raised when data received from the server isn't
    in the excepted format
    """
