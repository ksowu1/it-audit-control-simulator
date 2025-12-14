
from typing import Dict, Any, List, Tuple


def orphan_account_test(users: Dict[str, Dict[str, Any]]) -> Tuple[str, List[str]]:
    """
    FAIL if any user has role None or missing.
    users example:
      {
        "john": {"role": "admin", ...},
        "lisa": {"role": None, ...}
      }
    """
    orphans = [u for u, d in users.items() if d.get("role") is None]
    return ("FAIL", orphans) if orphans else ("PASS", [])


def excessive_admin_test(users: Dict[str, Dict[str, Any]], threshold: float = 0.10) -> Tuple[str, float]:
    """
    FAIL if admin ratio exceeds threshold.
    """
    total = max(len(users), 1)
    admins = sum(1 for d in users.values() if d.get("role") == "admin")
    ratio = admins / total
    return ("FAIL", ratio) if ratio > threshold else ("PASS", ratio)


def terminated_but_active_test(users: Dict[str, Dict[str, Any]]) -> Tuple[str, List[str]]:
    """
    FAIL if status=terminated but active=True.
    """
    issues = [
        u for u, d in users.items()
        if d.get("status") == "terminated" and d.get("active", True) is True
    ]
    return ("FAIL", issues) if issues else ("PASS", [])
