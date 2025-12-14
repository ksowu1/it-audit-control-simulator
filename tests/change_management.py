
from typing import List, Dict, Any, Tuple


def unapproved_change_test(changes: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
    bad = [c for c in changes if not c.get("approved", False)]
    return ("FAIL", bad) if bad else ("PASS", [])


def approval_before_deployment_test(changes: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
    invalid = [c for c in changes if c["approval_date"] > c["deployment_date"]]
    return ("FAIL", invalid) if invalid else ("PASS", [])
