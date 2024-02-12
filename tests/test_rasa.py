"""Tests for Rasa engine."""
from typing import Dict

import pytest

from nl2ltl import translate
from nl2ltl.engines.rasa.core import RasaEngine
from nl2ltl.filters.simple_filters import BasicFilter, GreedyFilter

from .conftest import UtterancesFixtures


class TestRasa:
    """Rasa test class."""

    @classmethod
    def setup_class(cls):
        """Setup any state specific to the execution of the given class (which
        usually contains tests).
        """
        cls.rasa_engine = RasaEngine()
        cls.basic_filter = BasicFilter()
        cls.greedy_filter = GreedyFilter()

    @pytest.mark.parametrize("utterance", UtterancesFixtures.utterances)
    def test_rasa_engine_basic(self, utterance):
        """Test Rasa engine for utterances with basic filter."""
        output = translate(utterance, self.rasa_engine, self.basic_filter)
        assert isinstance(output, Dict)

    @pytest.mark.parametrize("utterance", UtterancesFixtures.utterances)
    def test_rasa_engine_greedy(self, utterance):
        """Test Rasa engine for utterances with greedy filter."""
        output = translate(utterance, self.rasa_engine, self.greedy_filter)
        assert isinstance(output, Dict)
