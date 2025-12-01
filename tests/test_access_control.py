from controls.access_control import (
    orphan_account_test,
    excessive_admin_test,
    terminated_but_active_test,
)


def test_orphan_account(sample_users):
    status, orphans = orphan_account_test(sample_users)
    assert status == "FAIL"
    assert "lisa" in orphans


def test_excessive_admin(sample_users):
    status, ratio = excessive_admin_test(sample_users, threshold=0.10)
    assert status == "FAIL"
    assert ratio > 0.10


def test_terminated_but_active(sample_users):
    status, issues = terminated_but_active_test(sample_users)
    assert status == "FAIL"
    assert "paul" in issues
