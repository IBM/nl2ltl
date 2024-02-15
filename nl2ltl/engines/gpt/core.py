"""Implementation of the GPT engine.

Website:

    https://openai.com

"""
import json
from enum import Enum
from pathlib import Path
from typing import Dict, Set

from openai import OpenAI
from pylogics.syntax.base import Formula

from nl2ltl.engines.base import Engine
from nl2ltl.engines.gpt import ENGINE_ROOT
from nl2ltl.engines.gpt.output import GPTOutput, parse_gpt_output, parse_gpt_result
from nl2ltl.filters.base import Filter

try:
    client = OpenAI()
except Exception:
    client = None

engine_root = ENGINE_ROOT
DATA_DIR = engine_root / "data"
PROMPT_PATH = engine_root / DATA_DIR / "prompt.json"


class Models(Enum):
    """The set of available GPT language models."""

    GPT35_INSTRUCT = "gpt-3.5-turbo-instruct"
    GPT35_TURBO = "gpt-3.5-turbo"
    GPT4 = "gpt-4"


SUPPORTED_MODELS: Set[str] = {v.value for v in Models}


class OperationModes(Enum):
    """The set of available GPT modes."""

    CHAT = "chatCompletion"
    COMPLETION = "Completion"


SUPPORTED_MODES: Set[str] = {v.value for v in OperationModes}


class GPTEngine(Engine):
    """The GPT engine."""

    def __init__(
        self,
        model: str = Models.GPT35_TURBO.value,
        prompt: Path = PROMPT_PATH,
        operation_mode: str = OperationModes.CHAT.value,
        temperature: float = 0.5,
    ):
        """GPT LLM Engine initialization."""
        self._model = model
        self._prompt = self._load_prompt(prompt)
        self._operation_mode = operation_mode
        self._temperature = temperature

        self._check_consistency()

    def _load_prompt(self, prompt):
        return json.load(open(prompt))["prompt"]

    def _check_consistency(self) -> None:
        """Run consistency checks."""
        self.__check_openai_version()
        self.__check_model_support()
        self.__check_operation_mode()

    def __check_openai_version(self):
        """Check that the GPT tool is at the right version."""
        is_right_version = client._version == "1.12.0"
        if not is_right_version:
            raise Exception(
                "OpenAI needs to be at version 1.12.0. "
                "Please install it manually using:"
                "\n"
                "pip install openai==1.12.0"
            )

    def __check_model_support(self):
        """Check if the model is a supported model."""
        is_supported = self.model in SUPPORTED_MODELS
        if not is_supported:
            raise Exception(f"The LLM model {self.model} is not currently supported by nl2ltl.")

    def __check_operation_mode(self):
        """Check if the operation mode is a supported mode."""
        is_supported = self.operation_mode in SUPPORTED_MODES
        if not is_supported:
            raise Exception(f"The operation mode {self.operation_mode} is not currently supported by nl2ltl.")

    @property
    def model(self) -> str:
        """Get the GPT model."""
        return self._model

    @property
    def prompt(self) -> str:
        """Get the GPT prompt."""
        return self._prompt

    @property
    def operation_mode(self) -> str:
        """Get the GPT operation mode."""
        return self._operation_mode

    @property
    def temperature(self) -> float:
        """Get the GPT temperature."""
        return self._temperature

    def translate(self, utterance: str, filtering: Filter = None) -> Dict[Formula, float]:
        """From NL to best matching LTL formulas with confidence."""
        return _process_utterance(
            utterance,
            self.model,
            self.prompt,
            self.operation_mode,
            self.temperature,
            filtering,
        )


def _process_utterance(
    utterance: str,
    model: str,
    prompt: str,
    operation_mode: str,
    temperature: float,
    filtering: Filter,
) -> Dict[Formula, float]:
    """Process NL utterance.

    :param utterance: the natural language utterance
    :param model: the GPT model
    :param prompt: the prompt
    :param operation_mode: the operation mode
    :param temperature: the temperature
    :param filtering: the filter used to remove formulas
    :return: a dict matching formulas to their confidence
    """
    query = f"NL: {utterance}\n"
    messages = [{"role": "user", "content": prompt + query}]
    if operation_mode == OperationModes.CHAT.value:
        prediction = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n\n"],
        )
    else:
        prediction = client.completions.create(
            model=model,
            prompt=messages[0]["content"],
            temperature=temperature,
            max_tokens=200,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n\n"],
        )

    gpt_result: GPTOutput = parse_gpt_output(prediction, operation_mode)
    matching_formulas: Dict[Formula, float] = parse_gpt_result(gpt_result, filtering)
    return matching_formulas
