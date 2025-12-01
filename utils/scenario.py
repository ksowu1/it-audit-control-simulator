import json
import random
from datetime import datetime, timedelta
from typing import Dict, Any

from config.config_loader import load_config


def prepare_runtime_data(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts a raw config dict into runtime-ready structures.
    Handles date parsing, backup age conversion, etc.
    """
    users = config["access_control"]["users"]

    changes = [
        {
            "id": ch["id"],
            "approved": ch["approved"],
            "approval_date": datetime.fromisoformat(ch["approval_date"]),
            "deployment_date": datetime.fromisoformat(ch["deployment_date"]),
        }
        for ch in config["change_management"]["changes"]
    ]

    backups = [
        {
            "date": datetime.now() - timedelta(days=b["days_ago"]),
            "success": b["success"],
        }
        for b in config["backup_recovery"]["backups"]
    ]

    sod_rules = config["sod_rules"]["conflicts"]

    return {
        "users": users,
        "changes": changes,
        "backups": backups,
        "sod_rules": sod_rules,
    }


def load_scenario_from_file(path: str) -> Dict[str, Any]:
    """Load a JSON scenario file and prepare runtime data."""
    raw = load_config(path)
    return prepare_runtime_data(raw)


def build_interactive_scenario() -> Dict[str, Any]:
    """
    Interactive scenario builder.
    Creates a dynamic audit dataset from user inputs.
    """
    print("\n=== Interactive Scenario Builder ===")

    num_users = int(input("How many users? [default 10]: ") or 10)
    admin_ratio = float(input("Admin ratio (0–1) [default 0.10]: ") or 0.10)
    terminated_ratio = float(input("Terminated ratio (0–1) [default 0.10]: ") or 0.10)

    users = {}
    departments = ["IT", "Finance", "HR", "Ops"]

    for i in range(1, num_users + 1):
        role = "admin" if random.random() < admin_ratio else "user"
        status = "terminated" if random.random() < terminated_ratio else "active"
        users[f"user{i}"] = {
            "role": role,
            "status": status,
            "department": random.choice(departments),
            "privileged": True if role == "admin" else random.random() < 0.05,
        }

    changes = [
        {
            "id": 200 + i,
            "approved": random.choice([True, False]),
            "approval_date": datetime(2024, 7, 1),
            "deployment_date": datetime(2024, 7, 2),
        }
        for i in range(3)
    ]

    backups = [
        {"date": datetime.now() - timedelta(days=d), "success": s}
        for d, s in [(1, True), (3, True), (10, False)]
    ]

    sod_rules = [
        {"name": "developer & deployer", "role1": "developer", "role2": "deploy"},
        {"name": "requester & approver", "role1": "requester", "role2": "approve"},
    ]

    return {
        "users": users,
        "changes": changes,
        "backups": backups,
        "sod_rules": sod_rules,
    }
