# -*- coding: utf-8 -*-

"""Implementation of the GPT-3 engine."""

import inspect
from pathlib import Path

ENGINE_ROOT = Path(inspect.getframeinfo(inspect.currentframe()).filename).parent  # type: ignore
