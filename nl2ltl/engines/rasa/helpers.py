"""This module contains utilities to call the Lydia tool from Python."""
import glob
import os
from pathlib import Path


def _get_latest_model(path: Path):
    """Get the Rasa latest model."""
    if not path:
        return None
    list_of_files = glob.glob(os.path.join(path, "*.tar.gz"))
    if len(list_of_files) == 0:
        return None
    return max(list_of_files, key=os.path.getctime)
