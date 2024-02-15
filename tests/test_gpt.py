"""Tests for GPT engine."""
from typing import Dict

import pytest

from nl2ltl import translate
from nl2ltl.engines.gpt.core import GPTEngine
from nl2ltl.filters.simple_filters import BasicFilter, GreedyFilter

from .conftest import UtterancesFixtures


class TestGPT:
    """GPT test class."""

    @classmethod
    def setup_class(cls):
        """Setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.gpt_engine = GPTEngine()
        cls.basic_filter = BasicFilter()
        cls.greedy_filter = GreedyFilter()

    @pytest.mark.parametrize("utterance", UtterancesFixtures.utterances)
    def test_gpt_engine_basic(self, utterance):
        """Test GPT engine for utterances with basic filter."""
        output = translate(utterance, self.gpt_engine, self.basic_filter)
        assert isinstance(output, Dict)

    @pytest.mark.parametrize("utterance", UtterancesFixtures.utterances)
    def test_gpt_engine_greedy(self, utterance):
        """Test GPT engine for utterances with greedy filter."""
        output = translate(utterance, self.gpt_engine, self.greedy_filter)
        assert isinstance(output, Dict)
