# -*- coding: utf-8 -*-

"""
Implementation of the GPT-3 engine.

Website:

    https://openai.com

"""
import json
import os
from pathlib import Path
from typing import Dict

import openai
from pylogics.syntax.base import Formula

from nl2ltl.engines.base import Engine
from nl2ltl.engines.gpt3 import ENGINE_ROOT
from nl2ltl.engines.gpt3.output import GPT3Output, parse_gpt3_output, parse_gpt3_result
from nl2ltl.filters.base import Filter

openai.api_key = os.getenv("OPENAI_API_KEY")
engine_root = ENGINE_ROOT
DATA_DIR = engine_root / "data"
PROMPT_PATH = engine_root / DATA_DIR / "prompt.json"


class GPT3Engine(Engine):
    """The GPT-3 engine."""

    def __init__(
        self,
        prompt: Path = PROMPT_PATH,
        temperature: float = 0.5,
    ):
        """GPT-3 LLM Engine initialization."""
        self.prompt = self._load_prompt(prompt)
        self.temperature = temperature

    def _load_prompt(self, prompt):
        return json.load(open(prompt, "r"))["prompt"]

    @classmethod
    def __check_openai_version(cls):
        """Check that the GPT-3 tool is at the right version."""
        is_right_version = openai.__version__ == "0.23.0"
        if not is_right_version:
            raise Exception(
                "OpenAI needs to be at version 0.23.0. "
                "Please install it manually using:"
                "\n"
                "pip install openai==0.23.0"
            )

    def __post_init__(self):
        """Do post-initialization checks."""
        self.__check_openai_version()

    def translate(
        self, utterance: str, filtering: Filter = None
    ) -> Dict[Formula, float]:
        """From NL to best matching LTL formulas with confidence."""
        return _process_utterance(utterance, self.prompt, self.temperature, filtering)


def _process_utterance(
    utterance: str, prompt: str, temperature: float, filtering: Filter
) -> Dict[Formula, float]:
    """
    Process NL utterance.

    :param utterance: the natural language utterance
    :return: a dict with matching formulas and confidence
    """
    query = "NL: " + utterance + "\n"
    prediction = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt + query,
        temperature=temperature,
        max_tokens=200,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\n\n"],
    )
    gpt3_result: GPT3Output = parse_gpt3_output(prediction)
    matching_formulas: Dict[Formula, float] = parse_gpt3_result(gpt3_result, filtering)
    return matching_formulas
