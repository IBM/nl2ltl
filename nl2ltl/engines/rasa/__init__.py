"""Implementation of the RASA engine."""

import inspect
from pathlib import Path

ENGINE_ROOT = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent  # type: ignore
