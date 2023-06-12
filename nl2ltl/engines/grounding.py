# -*- coding: utf-8 -*-

"""Grounding visitor."""
import logging
from typing import Dict, Set

from pylogics.syntax.ltl import Atomic

from nl2ltl.declare.base import Template
from nl2ltl.declare.declare import (
    Absence,
    ChainResponse,
    Existence,
    ExistenceTwo,
    NotCoExistence,
    Precedence,
    RespondedExistence,
    Response,
)


def ground_existence(connectors: Dict[str, float]) -> Set[Template]:
    """Compute ground for Existence."""
    if len(list(connectors)) > 0:
        return {Existence(Atomic(list(connectors)[0].lower()))}
    else:
        logging.warning(
            "No valid matching, cannot instantiate Existence with < 1 connectors."
        )
        return set()


def ground_existencetwo(connectors: Dict[str, float]) -> Set[Template]:
    """Compute ground for ExistenceTwo."""
    if len(list(connectors)) > 0:
        return {ExistenceTwo(Atomic(list(connectors)[0].lower()))}
    else:
        logging.warning(
            "No valid matching, cannot instantiate ExistenceTwo with < 1 connectors."
        )
        return set()


def ground_absence(connectors: Dict[str, float]) -> Set[Template]:
    """Compute ground for Absence."""
    if len(list(connectors)) > 0:
        return {Absence(Atomic(list(connectors)[0].lower()))}
    else:
        logging.warning(
            "No valid matching, cannot instantiate Absence with < 1 connectors."
        )
        return set()


def ground_respondedexistence(connectors: Dict[str, float]) -> Set[Template]:
    """Compute ground for RespondedExistence."""
    if len(list(connectors)) >= 2:
        return {
            RespondedExistence(
                Atomic(list(connectors)[0].lower()), Atomic(list(connectors)[1].lower())
            )
        }
    else:
        logging.warning(
            "No valid matching, cannot instantiate RespondedExistence with < 2 connectors."
        )
        return set()


def ground_response(connectors: Dict[str, float]) -> Set[Template]:
    """Compute ground for Response."""
    if len(list(connectors)) >= 2:
        return {
            Response(
                Atomic(list(connectors)[0].lower()), Atomic(list(connectors)[1].lower())
            )
        }
    else:
        logging.warning(
            "No valid matching, cannot instantiate Response with < 2 connectors."
        )
        return set()


def ground_precedence(connectors: Dict[str, float]) -> Set[Template]:
    """Compute ground for Precedence."""
    if len(list(connectors)) >= 2:
        return {
            Precedence(
                Atomic(list(connectors)[0].lower()), Atomic(list(connectors)[1].lower())
            )
        }
    else:
        logging.warning(
            "No valid matching, cannot instantiate Precedence with < 2 connectors."
        )
        return set()


def ground_chainresponse(connectors: Dict[str, float]) -> Set[Template]:
    """Compute ground for ChainResponse."""
    if len(list(connectors)) >= 2:
        return {
            ChainResponse(
                Atomic(list(connectors)[0].lower()), Atomic(list(connectors)[1].lower())
            )
        }
    else:
        logging.warning(
            "No valid matching, cannot instantiate ChainResponse with < 2 connectors."
        )
        return set()


def ground_notcoexistence(connectors: Dict[str, float]) -> Set[Template]:
    """Compute ground for NotCoExistence."""
    if len(list(connectors)) >= 2:
        return {
            NotCoExistence(
                Atomic(list(connectors)[0].lower()), Atomic(list(connectors)[1].lower())
            )
        }
    else:
        logging.warning(
            "No valid matching, cannot instantiate NotCoExistence with < 2 connectors."
        )
        return set()
