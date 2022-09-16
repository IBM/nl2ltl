# -*- coding: utf-8 -*-

"""This module contains utilities to call the Lydia tool from Python."""
import glob
import os
from pathlib import Path
from typing import Dict

from pylogics.syntax.base import Formula


def _get_latest_model(path: Path):
    """Get the Rasa latest model."""
    if not path:
        return None
    list_of_files = glob.glob(os.path.join(path, "*.tar.gz"))
    if len(list_of_files) == 0:
        return None
    return max(list_of_files, key=os.path.getctime)


def pretty(result: Dict[Formula, float]):
    """Pretty print Rasa output."""
    print("=" * 150)
    for k, v in result.items():
        print(f"Declare Template: {str(k)}", end="\n")
        print(f"English meaning:  {k.to_english()}", end="\n")
        print(f"Confidence:       {str(v)}", end="\n\n")
