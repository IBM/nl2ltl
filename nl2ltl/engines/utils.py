# -*- coding: utf-8 -*-

"""Engines utils."""
import difflib
from typing import Callable, Dict, Set

from pylogics.syntax.base import Formula

from nl2ltl.declare.base import TemplateEnum


def _get_formulas(name: str, args: Dict[str, float]) -> Set[Formula]:
    """Instantiate matching formulas based on intent name and entities."""
    import nl2ltl.declare.declare
    import nl2ltl.engines.grounding

    class_name_match = difflib.get_close_matches(
        name, [x.value for x in TemplateEnum], n=1
    )
    grounding_map: Dict[str, Callable] = {}
    for c_name in TemplateEnum:
        grounding_map[c_name.value] = getattr(
            nl2ltl.engines.grounding, f"ground_{c_name.value.lower()}"
        )

    grounding_func: Callable = grounding_map[str(class_name_match[0])]
    grounded_formulas: Set[Formula] = grounding_func(args)
    return grounded_formulas


def pretty(result: Dict[Formula, float]):
    """Pretty print Rasa output."""
    print("=" * 150)
    for k, v in result.items():
        print(f"Declare Template: {str(k)}", end="\n")
        print(f"English meaning:  {k.to_english()}", end="\n")
        print(f"Confidence:       {str(v)}", end="\n\n")
