# -*- coding: utf-8 -*-

"""Tests for GPT-3 engine."""
from typing import Dict

import pytest

from nl2ltl import translate
from nl2ltl.engines.gpt3.core import GPT3Engine
from nl2ltl.filters.simple_filters import BasicFilter, GreedyFilter

from .conftest import UtterancesFixtures


class TestGPT3:
    """GPT-3 test class."""

    @classmethod
    def setup_class(cls):
        """setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.gpt3_engine = GPT3Engine()
        cls.basic_filter = BasicFilter()
        cls.greedy_filter = GreedyFilter()

    @pytest.mark.parametrize("utterance", UtterancesFixtures.utterances)
    def test_gpt3_engine_basic(self, utterance):
        """Test GPT-3 engine for utterances with basic filter."""
        output = translate(utterance, self.gpt3_engine, self.basic_filter)
        assert isinstance(output, Dict)

    @pytest.mark.parametrize("utterance", UtterancesFixtures.utterances)
    def test_gpt3_engine_greedy(self, utterance):
        """Test GPT-3 engine for utterances with greedy filter."""
        output = translate(utterance, self.gpt3_engine, self.greedy_filter)
        assert isinstance(output, Dict)
