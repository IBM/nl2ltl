"""Abstract definition of a engine."""
from abc import ABC, ABCMeta
from typing import Dict

from pylogics.syntax.base import Formula

from nl2ltl.exceptions import NotImplementedEngineFunction
from nl2ltl.filters.base import Filter


class _MetaEngine(ABCMeta):
    """Metaclass for rasa."""

    def __new__(mcs, *args, **kwargs):
        """Instantiate a new class."""
        return super().__new__(mcs, *args, **kwargs)


class Engine(ABC, metaclass=_MetaEngine):
    """Nl2ltlf engine interface."""

    @classmethod
    def __not_supported_error(cls, operation: str) -> Exception:
        """Raise a not supported error."""
        return NotImplementedEngineFunction(f"operation '{operation}' is not supported by the '{cls.__name__}' engine")

    def translate(self, utterance: str, filtering: Filter = None) -> Dict[Formula, float]:
        """Transform a Natural Language utterance into an LTLf formula.

        :param utterance: a Natural Language utterance
        :param filtering: a custom filtering algorithm
        :return: the corresponding LTLf formula template
        """
        raise self.__not_supported_error(self.translate.__name__)
