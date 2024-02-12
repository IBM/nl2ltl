"""Base classes for filters."""

from abc import ABC, abstractmethod
from typing import Dict

from pylogics.syntax.base import Formula


class Filter(ABC):
    """Base class for all templates."""

    NAME: str

    @abstractmethod
    def enforce(self, output: Dict[Formula, float], entities: Dict[str, float], **kwargs) -> Dict[Formula, float]:
        """Enforce filters on output."""
        raise NotImplementedError("Filters must implement this method.")
