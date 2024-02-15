"""Greedy filter class."""
from typing import Dict

from pylogics.syntax.base import Formula

from nl2ltl.declare.base import Template
from nl2ltl.filters.base import Filter
from nl2ltl.filters.utils.conflicts import conflicts
from nl2ltl.filters.utils.subsumptions import subsumptions


class BasicFilter(Filter):
    """Basic filter class."""

    NAME = "basic"

    @staticmethod
    def enforce(output: Dict[Formula, float], entities: Dict[str, float], **kwargs) -> Dict[Formula, float]:
        """Enforce conflicts and subsumptions to output formulas.

        Algorithm:
        - scan the output
        - pick the best match formulas based on number of matching entities
        """
        return output


class GreedyFilter(Filter):
    """Greedy filter class."""

    NAME = "greedy"

    @staticmethod
    def enforce(output: Dict[Formula, float], entities: Dict[str, float], **kwargs) -> Dict[Formula, float]:
        """Enforce conflicts and subsumptions to output formulas.

        Algorithm:
        - empty set of formulas
        - add the highest scoring formula to the result set
        - scan the output one formula at a time
        - compare the highest scoring formula with other formulas
        - if the current formulas has conflicts with the highest scoring formula, discard it
        - if the current formula subsumes the highest scoring formula, discard it and keep the highest scoring formula
        - else add the current formula to the result set
        """
        result_set = set()

        highest_scoring_formula = max(output, key=output.get, default=Template)
        formula_conflicts = conflicts(highest_scoring_formula)
        formula_subsumptions = subsumptions(highest_scoring_formula)

        result_set.add(highest_scoring_formula)
        for formula in output:
            if formula in formula_subsumptions:
                continue
            if formula in formula_conflicts:
                continue
            result_set.add(formula)
        return {formula: output[formula] for formula in result_set}
