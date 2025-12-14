import json
import os
from datetime import datetime, timedelta
from typing import Any, Dict, List


def prepare_runtime_data(raw: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts raw JSON config into runtime objects used by control tests.
    - change dates -> datetime objects
    - backups days_ago -> datetime objects

    Expected raw structure:
    {
      "access_control": {"users": {...}},
      "change_management": {"changes": [...]},
      "backup_recovery": {"backups": [...]},
      "sod_rules": {"conflicts": [...]}
    }
    """
    users = raw["access_control"]["users"]

    changes = [
        {
            "id": c["id"],
            "approved": c["approved"],
            "approval_date": datetime.fromisoformat(c["approval_date"]),
            "deployment_date": datetime.fromisoformat(c["deployment_date"]),
        }
        for c in raw["change_management"]["changes"]
    ]

    backups = [
        {
            "date": datetime.now() - timedelta(days=b["days_ago"]),
            "success": b["success"],
        }
        for b in raw["backup_recovery"]["backups"]
    ]

    sod_rules = raw["sod_rules"]["conflicts"]

    return {
        "users": users,
        "changes": changes,
        "backups": backups,
        "sod_rules": sod_rules,
    }


def load_scenario_from_file(path: str) -> Dict[str, Any]:
    """
    Loads a scenario JSON file (absolute or relative to project root)
    then converts it to runtime data.
    """
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isabs(path):
        path = os.path.join(project_root, path)

    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return prepare_runtime_data(raw)


def build_interactive_scenario() -> Dict[str, Any]:
    """
    Quick interactive builder (minimal). You can expand this later.
    Returns runtime data dict directly.
    """
    print("\nInteractive Scenario Builder (quick)")
    print("Using default scenario values as a base...\n")

    # Minimal quick builder: just load default scenario
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    default_path = os.path.join(project_root, "config", "default_scenario.json")
    return load_scenario_from_file(default_path)
