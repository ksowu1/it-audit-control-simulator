from controls.backup_recovery import (
    backup_recency_test,
    backup_success_test,
)
from datetime import datetime, timedelta


def test_backup_recency(sample_backups):
    status, old = backup_recency_test(sample_backups, max_age=7)
    assert status == "FAIL"
    assert any((datetime.now() - b["date"]).days > 7 for b in old)


def test_backup_success(sample_backups):
    status, failed = backup_success_test(sample_backups)
    assert status == "FAIL"
    assert any(not b["success"] for b in failed)
