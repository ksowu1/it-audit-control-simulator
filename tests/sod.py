
from typing import Dict, Any, List, Tuple


def privileged_access_test(users: Dict[str, Dict[str, Any]]) -> Tuple[str, List[str]]:
    """
    FAIL if privileged=True but role != admin
    """
    bad = [u for u, d in users.items() if d.get("privileged") and d.get("role") != "admin"]
    return ("FAIL", bad) if bad else ("PASS", [])


def sod_violation_test(users: Dict[str, Dict[str, Any]], conflicts: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, str]]]:
    """
    conflicts example:
      [{"conflict": "developer & deployer", "requires_separation": ["developer","deployer"]}, ...]
    Each user has duties: ["developer","deployer"]
    """
    violations = []
    for u, d in users.items():
        duties = set(d.get("duties", []))
        for rule in conflicts:
            required = set(rule.get("requires_separation", []))
            if required and required.issubset(duties):
                violations.append({"user": u, "conflict": rule.get("conflict", "SoD conflict")})
    return ("FAIL", violations) if violations else ("PASS", [])
