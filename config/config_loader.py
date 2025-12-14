import json
import os
from typing import Any, Dict


def load_config(path: str | None = None) -> Dict[str, Any]:
    """
    Loads a scenario JSON configuration.

    If path is None, it loads: config/default_scenario.json
    Paths can be absolute or relative to the project root.

    Returns
    -------
    dict
        Parsed JSON config
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if path is None:
        path = os.path.join(project_root, "config", "default_scenario.json")
    else:
        # If relative path, resolve relative to project root
        if not os.path.isabs(path):
            path = os.path.join(project_root, path)

    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
