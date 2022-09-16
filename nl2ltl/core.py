# -*- coding: utf-8 -*-

"""NL2LTLf core module."""
from typing import Dict

from pylogics.syntax.base import Formula

from nl2ltl.engines import Engine
from nl2ltl.filters.base import Filter


def _call_translation_method(
    utterance: str, engine: Engine, filtering: Filter, method_name: str
) -> Dict[Formula, float]:
    """Call the translation method."""
    method = getattr(engine, method_name)
    return method(utterance, filtering)


def translate(
    utterance: str, engine: Engine, filtering: Filter = None
) -> Dict[Formula, float]:
    """
    From NL to LTLf.

    :param utterance: the natural language utterance to translate.
    :param engine: the engine to use.
    :param filtering: the filtering function to use.
    :return: the best matching LTL formulas with their confidence.
    """
    return _call_translation_method(utterance, engine, filtering, translate.__name__)
