"""The conftest.py module for pytest."""
import inspect
from pathlib import Path

import nl2ltl

_current_filepath = inspect.getframeinfo(inspect.currentframe()).filename  # type: ignore
TEST_DIRECTORY = Path(_current_filepath).absolute().parent
ROOT_DIRECTORY = TEST_DIRECTORY.parent
LIBRARY_DIRECTORY = ROOT_DIRECTORY / nl2ltl.__name__
DOCS_DIRECTORY = ROOT_DIRECTORY / "docs"


class UtterancesFixtures:
    utterances = [
        "whenever I get a Slack, send a Gmail.",
        "Invite Sales employees.",
        "If a new Eventbrite is created, alert me through Slack.",
        "send me a Slack whenever I get a Gmail.",
    ]
