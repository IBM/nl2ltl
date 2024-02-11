"""Helper functions."""
from typing import Sequence, Type

from pylogics.syntax.base import Formula
from pylogics.syntax.ltl import Atomic


def _enforce(condition: bool, message: str = "", exception_cls: Type[Exception] = AssertionError):
    """User-defined assert."""
    if not condition:
        raise exception_cls(message)
    else:
        return True


def enforce_unary(argument: Formula):
    """Enforce a unary formula."""
    return _enforce(
        isinstance(argument, Atomic),
        "argument is not an instance of 'Atomic'",
        exception_cls=ValueError,
    )


def enforce_binary(operands: Sequence[Formula]):
    """Enforce DECLARE binary condition."""
    return _enforce(
        len(operands) == 2,
        f"expected exactly 2 operands, found {len(operands)} operands",
    ) and _enforce(
        all(map(lambda x: isinstance(x, Atomic), operands)),
        "some argument is not an instance of 'Atomic'",
        exception_cls=ValueError,
    )
