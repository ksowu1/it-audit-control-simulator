from controls.sod import (
    privileged_access_test,
    sod_violation_test
)


def test_privileged_access(sample_users):
    status, violations = privileged_access_test(sample_users)
    # john is privileged AND admin → OK
    # no violations expected
    assert status == "PASS"
    assert violations == []


def test_sod_violations(sample_users, sample_sod_rules):
    status, conflicts = sod_violation_test(sample_users, sample_sod_rules)
    assert status == "FAIL"
    assert len(conflicts) > 0
