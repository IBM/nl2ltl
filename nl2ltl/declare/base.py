"""Base classes for declare templates."""

from abc import abstractmethod
from enum import Enum, unique

from pylogics.syntax.base import Formula, Logic


@unique
class TemplateEnum(Enum):
    """Template enumeratin class."""

    EXISTENCE = "Existence"
    EXISTENCE_TWO = "ExistenceTwo"
    ABSENCE = "Absence"
    RESPONDED_EXISTENCE = "RespondedExistence"
    RESPONSE = "Response"
    PRECEDENCE = "Precedence"
    CHAIN_RESPONSE = "ChainResponse"
    NOT_CO_EXISTENCE = "NotCoExistence"


class Template(Formula):
    """Base class for all templates."""

    SYMBOL: str

    def logic(self) -> Logic:
        """Get the logic."""
        return Logic.LTL

    @abstractmethod
    def to_ltlf(self) -> "Formula":
        """Get the template translation to LTLf."""
        raise NotImplementedError("Template's subclasses must implement this method.")

    @abstractmethod
    def to_english(self) -> str:
        """Get the English semantics."""
        raise NotImplementedError("Template's subclasses must implement this method.")

    @abstractmethod
    def to_ppltl(self) -> "Formula":
        """Get the template translation to PPLTL."""

    def __hash__(self):
        """Delegate the computation of the hash to the superclass."""
        return super(Formula, self).__hash__()
