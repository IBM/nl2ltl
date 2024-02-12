"""Conflicts visitor."""
from functools import singledispatch
from typing import Set

from pylogics.syntax.base import Formula

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


@singledispatch
def conflicts(formula: Formula) -> Set[Template]:
    """Compute conflicts for a Formula."""
    raise NotImplementedError("handler not implemented for formula %s" % type(formula))


@conflicts.register
def conflicts_existence(formula: Existence) -> Set[Template]:
    """Compute conflicts for Existence."""
    return {Absence(formula.argument)}


@conflicts.register
def conflicts_existence_two(formula: ExistenceTwo) -> Set[Template]:
    """Compute conflicts for ExistenceTwo."""
    return {Absence(formula.argument)}


@conflicts.register
def conflicts_absence(formula: Absence) -> Set[Template]:
    """Compute conflicts for Absence."""
    return {Existence(formula.argument)}


@conflicts.register
def conflicts_responded_existence(formula: RespondedExistence) -> Set[Template]:
    """Compute conflicts for RespondedExistence."""
    return {
        Absence(formula.operands[0]),
        Absence(formula.operands[1]),
        Precedence(*reversed(formula.operands)),
    }


@conflicts.register
def conflicts_response(formula: Response) -> Set[Template]:
    """Compute conflicts for Response."""
    return {
        Absence(formula.operands[0]),
        Absence(formula.operands[1]),
        Precedence(*reversed(formula.operands)),
    }


@conflicts.register
def conflicts_precedence(formula: Precedence) -> Set[Template]:
    """Compute conflicts for Precedence."""
    return {
        RespondedExistence(*reversed(formula.operands)),
        Response(*reversed(formula.operands)),
        ChainResponse(*reversed(formula.operands)),
    }


@conflicts.register
def conflicts_chain_response(formula: ChainResponse) -> Set[Template]:
    """Compute conflicts for ChainResponse."""
    return {
        Precedence(*reversed(formula.operands)),
        Absence(formula.operands[0]),
        Absence(formula.operands[1]),
    }


@conflicts.register
def conflicts_not_co_existence(_formula: NotCoExistence) -> Set[Template]:
    """Compute conflicts for NotCoExistence."""
    return set()
