"""Parse Rasa output to produce Dict[Formula, Float] result."""
from dataclasses import dataclass
from typing import Any, Dict

from pylogics.syntax.base import Formula

from nl2ltl.engines.utils import _get_formulas
from nl2ltl.filters.base import Filter


@dataclass
class RasaOutput:
    """Dataclass to represent the Rasa output."""

    text: str
    intent: Dict[str, float]
    entities: Dict[str, float]
    intent_ranking: Dict[str, Any]

    def __post_init__(self):
        """Do consistency checks after initialization."""
        assert self.intent is not None
        assert self.entities is not None


@dataclass
class _RasaOutputWrapper:
    """A wrapper to the textual output of Rasa."""

    output: dict

    @property
    def text(self) -> str:
        """Get the matched text."""
        return str(self.output["text"])

    @property
    def intent(self) -> Dict[str, float]:
        """Get the predicted intent."""
        return {self.output["intent"]["name"]: self.output["intent"]["confidence"]}

    @property
    def entities(self) -> Dict[str, float]:
        """Get the predicted entities."""
        entities: Dict[str, float] = {}
        for item in self.output["entities"]:
            entities[item["value"]] = item["confidence_entity"]
        return entities

    @property
    def intent_ranking(self) -> Dict[str, float]:
        """Get the intent ranking."""
        ranking: Dict[str, float] = {}
        for item in self.output["intent_ranking"]:
            ranking[item["name"]] = item["confidence"]
        return ranking


def parse_rasa_output(rasa_output: dict) -> RasaOutput:
    """Parse the Rasa output.

    :param rasa_output: the json description of the RASA prediction.
    :return: a RasaOutput instance.
    """
    wrapper = _RasaOutputWrapper(rasa_output)
    text: str = wrapper.text
    intent: Dict[str, float] = wrapper.intent
    entities: Dict[str, float] = wrapper.entities
    intent_ranking: Dict[str, float] = wrapper.intent_ranking
    rasa_result = RasaOutput(text, intent, entities, intent_ranking)
    return rasa_result


def parse_rasa_result(output: RasaOutput, filtering: Filter = None) -> Dict[Formula, float]:
    """Build a dict of formulas, given the RasaOutput object.

    :param output: a RasaOutput instance.
    :param filtering: a custom filtering function
    :return: the dictionary of formulas.
    """
    result: Dict[Formula, float] = {}
    for intent_name, confidence in output.intent_ranking.items():
        formulas = _get_formulas(intent_name, output.entities)
        if all(isinstance(f, Formula) for f in formulas):
            for f in formulas:
                result[f] = confidence
    if filtering:
        return filtering.enforce(result, output.entities)
    else:
        return result
