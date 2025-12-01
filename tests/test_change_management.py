from controls.change_management import (
    unapproved_change_test,
    approval_before_deployment_test,
)


def test_unapproved_change(sample_changes):
    status, bad = unapproved_change_test(sample_changes)
    assert status == "FAIL"
    assert any(not c["approved"] for c in bad)


def test_approval_before_deployment(sample_changes):
    status, invalid = approval_before_deployment_test(sample_changes)
    assert status == "PASS"   # all approval_date < deployment_date
