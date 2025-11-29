
import json
import os
from datetime import datetime, timedelta

def load_config():
    """
    Loads config/config.json and converts change dates and backup days to usable structures.
    Returns dict: { users, changes, backups, sod_rules }
    """
    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, "config.json")

    with open(path, "r") as f:
        raw = json.load(f)

    # Users (dict of username -> dict) - we return raw["access_control"]["users"]
    users = raw["access_control"]["users"]

    # Convert change dates to datetime
    changes = [
        {
            "id": c["id"],
            "approved": c["approved"],
            "approval_date": datetime.fromisoformat(c["approval_date"]),
            "deployment_date": datetime.fromisoformat(c["deployment_date"]),
        }
        for c in raw.get("change_management", {}).get("changes", [])
    ]

    # Convert backups: days_ago -> real datetime
    backups = [
        {
            "date": datetime.now() - timedelta(days=b["days_ago"]),
            "success": b["success"]
        }
        for b in raw.get("backup_recovery", {}).get("backups", [])
    ]

    sod_rules = raw.get("sod_rules", {}).get("conflicts", [])

    return {
        "users": users,
        "changes": changes,
        "backups": backups,
        "sod_rules": sod_rules
    }
