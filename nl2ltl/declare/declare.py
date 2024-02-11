"""Classes for declare templates."""
from pylogics.syntax.base import And, Formula, Implies, Not, Or, _BinaryOp, _UnaryOp
from pylogics.syntax.ltl import Always, Eventually, Next, Until
from pylogics.syntax.pltl import Before, Historically, Once, Since

from nl2ltl.declare.base import Template, TemplateEnum
from nl2ltl.declare.misc import enforce_binary, enforce_unary


class Existence(Template, _UnaryOp):
    """The existence template."""

    SYMBOL = TemplateEnum.EXISTENCE.value

    def __init__(self, argument):
        """Existence initialization."""
        super().__init__(arg=argument)
        enforce_unary(self.argument)

    def to_ltlf(self) -> Formula:
        """Translate Existence to LTLf."""
        return Eventually(self.argument)

    def to_english(self) -> str:
        """English meaning."""
        return f"Eventually, {self.argument} will happen."

    def to_ppltl(self) -> Formula:
        """Translate Existence to PPLTL."""
        return Once(self.argument)


class ExistenceTwo(Template, _UnaryOp):
    """The existenceTwo template."""

    SYMBOL = TemplateEnum.EXISTENCE_TWO.value

    def __init__(self, argument):
        """Existence Two initialization."""
        super().__init__(arg=argument)
        enforce_unary(self.argument)

    def to_ltlf(self) -> Formula:
        """Translate ExistenceTwo to LTLf."""
        return Eventually(And(self.argument, Next(Eventually(self.argument))))

    def to_english(self) -> str:
        """English meaning."""
        return f"{self.argument} will happen at least twice."

    def to_ppltl(self) -> Formula:
        """Translate ExistenceTwo to PPLTL."""
        return Once(And(self.argument, Before(Once(self.argument))))


class Absence(Template, _UnaryOp):
    """The existenceTwo template."""

    SYMBOL = TemplateEnum.ABSENCE.value

    def __init__(self, argument):
        """Absence initialization."""
        super().__init__(arg=argument)
        enforce_unary(self.argument)

    def to_ltlf(self) -> Formula:
        """Translate Absence to LTLf."""
        return Not(Eventually(self.argument))

    def to_english(self) -> str:
        """English meaning."""
        return f"{self.argument} will never happen."

    def to_ppltl(self) -> Formula:
        """Translate Absence to PPLTL."""
        return Not(Once(self.argument))


class RespondedExistence(Template, _BinaryOp):
    """The RespondedExistence template."""

    SYMBOL = TemplateEnum.RESPONDED_EXISTENCE.value

    def __init__(self, proposition1, proposition2):
        """Responded Existence initialization."""
        super().__init__(proposition1, proposition2)
        enforce_binary(self.operands)

    def to_ltlf(self) -> Formula:
        """Translate RespondedExistence to LTLf."""
        return Implies(Eventually(self.operands[0]), Eventually(self.operands[1]))

    def to_english(self) -> str:
        """English meaning."""
        return (
            f"If {self.operands[0]} happens at least once then {self.operands[1]} has to happen or happened "
            f"before {self.operands[0]}."
        )

    def to_ppltl(self) -> Formula:
        """Translate RespondedExistence to PPLTL."""
        return Implies(Once(self.operands[0]), Once(self.operands[1]))


class Response(Template, _BinaryOp):
    """The Response template."""

    SYMBOL = TemplateEnum.RESPONSE.value

    def __init__(self, proposition1, proposition2):
        """Response initialization."""
        super().__init__(proposition1, proposition2)
        enforce_binary(self.operands)

    def to_ltlf(self) -> Formula:
        """Translate Response to LTLf."""
        return Always(Implies(self.operands[0], Eventually(self.operands[1])))

    def to_english(self) -> str:
        """English meaning."""
        return f"Whenever  {self.operands[0]} happens,  {self.operands[1]} has to happen " f"eventually afterward."

    def to_ppltl(self) -> Formula:
        """Translate Response to PPLTL."""
        return Not(Since(Not(self.operands[1]), And(self.operands[0], Not(self.operands[1]))))


class Precedence(Template, _BinaryOp):
    """The Precedence template."""

    SYMBOL = TemplateEnum.PRECEDENCE.value

    def __init__(self, proposition1, proposition2):
        """Precedence initialization."""
        super().__init__(proposition1, proposition2)
        enforce_binary(self.operands)

    def to_ltlf(self) -> Formula:
        """Translate Precedence to LTLf."""
        return Or(
            Until(Not(self.operands[1]), self.operands[0]),
            Always(Not(self.operands[1])),
        )

    def to_english(self) -> str:
        """English meaning."""
        return f"Whenever  {self.operands[1]} happens,  {self.operands[0]} has to have happened " f"before it."

    def to_ppltl(self) -> Formula:
        """Translate Precedence to PPLTL."""
        return Or(
            Once(
                And(
                    self.operands[0],
                    Historically(Or(self.operands[0], Not(self.operands[1]))),
                )
            ),
            Historically(Not(self.operands[1])),
        )


class ChainResponse(Template, _BinaryOp):
    """The ChainResponse template."""

    SYMBOL = TemplateEnum.CHAIN_RESPONSE.value

    def __init__(self, proposition1, proposition2):
        """Chain Response initialization."""
        super().__init__(proposition1, proposition2)
        enforce_binary(self.operands)

    def to_ltlf(self) -> Formula:
        """Translate ChainResponse to LTLf."""
        return Always(Implies(self.operands[0], Next(self.operands[1])))

    def to_english(self) -> str:
        """English meaning."""
        return (
            f"Every time  {self.operands[0]} happens, it must be directly followed by  "
            f"{self.operands[1]} ( {self.operands[1]} can also follow other activities)."
        )

    def to_ppltl(self) -> Formula:
        """Translate ChainResponse to PPLTL."""
        return And(
            Historically(Implies(Before(self.operands[0]), self.operands[1])),
            Not(self.operands[0]),
        )


class NotCoExistence(Template, _BinaryOp):
    """The NotCoExistence template."""

    SYMBOL = TemplateEnum.NOT_CO_EXISTENCE.value

    def __init__(self, proposition1, proposition2):
        """Not Co Existence initialization."""
        super().__init__(proposition1, proposition2)
        enforce_binary(self.operands)

    def to_ltlf(self) -> Formula:
        """Translate NotCoExistence to LTLf."""
        return Implies(Eventually(self.operands[0]), Not(Eventually(self.operands[1])))

    def to_english(self) -> str:
        """English meaning."""
        return f"Either  {self.operands[0]} or {self.operands[1]} can happen, but not both."

    def to_ppltl(self) -> Formula:
        """Translate NotCoExistence to PPLTL."""
        return Implies(Once(self.operands[0]), Not(Once(self.operands[1])))
