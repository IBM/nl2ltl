"""This module implements the library exceptions."""


class Nl2ltlfException(Exception):
    """Base library exception."""


class NotImplementedEngineFunction(Nl2ltlfException):
    """Raise this exception when an engine does not support an operation."""


class BadUtteranceException(Nl2ltlfException):
    """Raise this exception when the utterance is malformed."""

    __ERROR_MSG = "wrong utterance for method {method_name}: expected '{expected}', found '{actual}'"

    def __init__(self, method_name: str, expected: str, actual: str, *args, **kwargs):
        """Initialize the exception."""
        format_args = dict(method_name=method_name, expected=expected, actual=actual)
        super().__init__(self.__ERROR_MSG.format(**format_args))
