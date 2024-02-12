"""Implementation of the RASA engine.

Repository:

    https://github.com/RasaHQ/rasa

"""
import asyncio
import shutil
from pathlib import Path
from typing import Dict

from pylogics.syntax.base import Formula

from nl2ltl.helpers import requires_optional

try:
    import rasa
    from rasa.core.agent import Agent
except ImportError:
    rasa = Agent = None

from nl2ltl.engines.base import Engine
from nl2ltl.engines.rasa import ENGINE_ROOT
from nl2ltl.engines.rasa.helpers import _get_latest_model
from nl2ltl.engines.rasa.output import RasaOutput, parse_rasa_output, parse_rasa_result
from nl2ltl.filters.base import Filter

engine_root = ENGINE_ROOT
DATA_DIR = engine_root / "data"
DOMAIN_PATH = engine_root / DATA_DIR / "domain.yml"
CONFIG_PATH = engine_root / DATA_DIR / "config.yml"
TRAINING_PATH = engine_root / DATA_DIR / "nlu_training.yml"
MODEL_OUTPUT_PATH = engine_root / "models"


@requires_optional
class RasaEngine(Engine):
    """The RASA engine."""

    def __init__(
        self,
        model: Path = None,
    ):
        """Rasa NLU Engine initialization."""
        self._load_model(model)

        self._check_consistency()

    def _load_model(self, model: Path = None):
        if model:
            self.agent = Agent.load(model)
        else:
            self.agent = Agent.load(_get_latest_model(path=MODEL_OUTPUT_PATH))

    def _check_consistency(self) -> None:
        """Run consistency checks."""
        self.__check_rasa_available()
        self.__check_rasa_version()

    def __check_rasa_available(self):
        """Check that the Rasa tool is available."""
        is_rasa_present = shutil.which("rasa") is not None
        if is_rasa_present is None:
            raise Exception(
                "Rasa is not installed. Please follow"
                "the installation instructions at https://rasa.com/docs/rasa/installation.\n"
            )

    def __check_rasa_version(self):
        """Check that the Rasa tool is at the right version."""
        is_right_version = rasa.__version__ == "3.6.16"
        if not is_right_version:
            raise Exception(
                "Rasa needs to be at version 3.6.16. "
                "Please install it manually using:"
                "\n"
                "pip install rasa==3.6.16"
            )

    @staticmethod
    def train(
        domain: Path = DOMAIN_PATH,
        config: Path = CONFIG_PATH,
        training: Path = TRAINING_PATH,
    ) -> Path:
        """Train a Rasa model."""
        result = rasa.train(
            domain=str(domain),
            config=str(config),
            training_files=[str(training)],
            output=str(MODEL_OUTPUT_PATH),
            force_training=True,
        )
        return Path(result.model)

    def translate(self, utterance: str, filtering: Filter = None) -> Dict[Formula, float]:
        """From NL to best matching LTL formulas with confidence."""
        return _process_utterance(utterance, self.agent, filtering)


def _process_utterance(utterance: str, rasa_agent: Agent, filtering: Filter) -> Dict[Formula, float]:
    """Process NL utterance.

    :param utterance: the natural language utterance
    :return: a dict with matching formulas and confidence
    """
    prediction = asyncio.run(rasa_agent.parse_message(utterance.strip()))
    rasa_result: RasaOutput = parse_rasa_output(prediction)
    matching_formulas: Dict[Formula, float] = parse_rasa_result(rasa_result, filtering)
    return matching_formulas
