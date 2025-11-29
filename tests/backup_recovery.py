
from datetime import datetime

def backup_recency_test(backups, max_age=7):
    old = [b for b in backups if (datetime.now() - b["date"]).days > max_age]
    status = "FAIL" if old else "PASS"
    return status, old


def backup_success_test(backups):
    failed = [b for b in backups if not b.get("success", False)]
    status = "FAIL" if failed else "PASS"
    return status, failed
