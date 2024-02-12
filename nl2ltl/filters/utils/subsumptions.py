"""Subsumptions visitor."""
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
def subsumptions(formula: Formula) -> Set[Template]:
    """Compute subsumptions for a Formula."""
    raise NotImplementedError("subsumption handler not implemented for formula %s" % type(formula))


@subsumptions.register
def subsumptions_existence(_formula: Existence) -> Set[Template]:
    """Compute subsumptions for Existence."""
    return set()


@subsumptions.register
def subsumptions_existence_two(formula: ExistenceTwo) -> Set[Template]:
    """Compute subsumptions for ExistenceTwo."""
    return {Existence(formula.argument)}


@subsumptions.register
def subsumptions_absence(_formula: Absence) -> Set[Template]:
    """Compute subsumptions for Absence."""
    return set()


@subsumptions.register
def subsumptions_responded_existence(formula: RespondedExistence) -> Set[Template]:
    """Compute subsumptions for RespondedExistence."""
    return {Existence(formula.operands[0]), Existence(formula.operands[1])}


@subsumptions.register
def subsumptions_response(formula: Response) -> Set[Template]:
    """Compute subsumptions for Response."""
    return {
        Existence(formula.operands[0]),
        Existence(formula.operands[1]),
        RespondedExistence(*formula.operands),
        ChainResponse(*formula.operands),
    }


@subsumptions.register
def subsumptions_precedence(formula: Precedence) -> Set[Template]:
    """Compute subsumptions for Precedence."""
    return {Existence(formula.operands[0]), Existence(formula.operands[1])}


@subsumptions.register
def subsumptions_chain_response(formula: ChainResponse) -> Set[Template]:
    """Compute subsumptions for ChainResponse."""
    return {
        Existence(formula.operands[0]),
        Existence(formula.operands[1]),
        RespondedExistence(*formula.operands),
        ChainResponse(*formula.operands),
    }


@subsumptions.register
def subsumptions_not_co_existence(formula: NotCoExistence) -> Set[Template]:
    """Compute subsumptions for NotCoExistence."""
    return {Existence(formula.operands[0]), Existence(formula.operands[1])}
