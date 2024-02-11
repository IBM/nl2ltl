"""This module implements the library exceptions."""
import functools
import sys


def requires_optional(cls):
    @functools.wraps(cls)
    def wrapper_decor(*args, **kwargs):
        if "rasa" not in sys.modules:
            raise ModuleNotFoundError(f"Rasa is required to instantiate {cls.__name__}")
        return cls(*args, **kwargs)

    return wrapper_decor
