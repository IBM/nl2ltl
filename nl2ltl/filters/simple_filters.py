# -*- coding: utf-8 -*-

"""Greedy filter class."""
from typing import Dict

from pylogics.syntax.base import Formula

from nl2ltl.filters.base import Filter


class BasicFilter(Filter):
    """Basic filter class."""

    NAME = "basic"

    @staticmethod
    def enforce(
        output: Dict[Formula, float], entities: Dict[str, float], **kwargs
    ) -> Dict[Formula, float]:
        """
        Enforce conflicts and subsumptions to output formulas.

        Algorithm:
        - scan the output
        - pick the best match formulas based on number of matching entities
        """
        return output


class GreedyFilter(Filter):
    """Greedy filter class."""

    NAME = "greedy"

    @staticmethod
    def enforce(
        output: Dict[Formula, float], entities: Dict[str, float], **kwargs
    ) -> Dict[Formula, float]:
        """
        Enforce conflicts and subsumptions to output formulas.

        Algorithm:
        - scan the output
        - ...
        """
        return output
