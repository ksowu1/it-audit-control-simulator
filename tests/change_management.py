
def unapproved_change_test(changes):
    bad = [c for c in changes if not c.get("approved", False)]
    status = "FAIL" if bad else "PASS"
    return status, bad


def approval_before_deployment_test(changes):
    invalid = [c for c in changes if c["approval_date"] > c["deployment_date"]]
    status = "FAIL" if invalid else "PASS"
    return status, invalid
