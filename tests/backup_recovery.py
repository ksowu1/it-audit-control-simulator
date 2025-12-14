
from datetime import datetime
from typing import List, Dict, Any, Tuple


def backup_recency_test(backups: List[Dict[str, Any]], max_age_days: int = 7) -> Tuple[str, List[Dict[str, Any]]]:
    old = [b for b in backups if (datetime.now() - b["date"]).days > max_age_days]
    return ("FAIL", old) if old else ("PASS", [])


def backup_success_test(backups: List[Dict[str, Any]]) -> Tuple[str, List[Dict[str, Any]]]:
    failed = [b for b in backups if not b.get("success", False)]
    return ("FAIL", failed) if failed else ("PASS", [])
