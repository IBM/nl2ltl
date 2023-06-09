# -*- coding: utf-8 -*-

"""Parse GPT output to produce Dict[Formula, Float] result."""
import re
from dataclasses import dataclass
from typing import Dict, Match, Set, Tuple, cast

from pylogics.syntax.base import Formula

from nl2ltl.engines.utils import _get_formulas
from nl2ltl.filters.base import Filter


@dataclass
class GPTOutput:
    """Dataclass to represent the GPT output."""

    pattern: str
    entities: Tuple[str]

    def __post_init__(self):
        """Do consistency checks after initialization."""
        assert self.pattern is not None
        assert self.entities is not None


@dataclass
class _GPTOutputWrapper:
    """A wrapper to the textual output of GPT."""

    output: dict

    @property
    def pattern(self) -> str:
        """Get the predicted pattern."""
        return str(
            cast(
                Match, re.search("PATTERN: (.*)\n", self.output["choices"][0]["text"])
            ).group(1)
        )

    @property
    def entities(self) -> Tuple[str]:
        """Get the predicted entities."""
        return tuple(
            cast(
                Match,
                re.search("SYMBOLS: (.*)", self.output["choices"][0]["text"]),
            )
            .group(1)
            .split(", ")
        )


def parse_gpt_output(gpt_output: dict) -> GPTOutput:
    """
    Parse the GPT output.

    :param gpt_output: the json description of the GPT prediction.
    :return: a GPTOutput instance.
    """
    wrapper = _GPTOutputWrapper(gpt_output)
    pattern: str = wrapper.pattern
    entities: Tuple[str] = wrapper.entities
    gpt_result = GPTOutput(pattern, entities)
    return gpt_result


def parse_gpt_result(
    output: GPTOutput, filtering: Filter = None
) -> Dict[Formula, float]:
    """
    Build a dict of formulas, given the GPT3Output object.

    :param output: a GPT3Output instance.
    :param filtering: a custom filtering function
    :return: the dictionary of formulas.
    """
    result: Dict[Formula, float] = {}
    symbols: Dict[str, float] = {e: 1 for e in output.entities}
    formulas: Set[Formula] = _get_formulas(output.pattern, symbols)
    if all(isinstance(f, Formula) for f in formulas):
        for f in formulas:
            result[f] = 1
    else:
        raise Exception("The output is not a valid formula.")

    if filtering:
        return filtering.enforce(result, symbols)
    else:
        return result