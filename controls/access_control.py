
def orphan_account_test(users):
    orphans = [u for u, d in users.items() if d.get("role") is None]
    status = "FAIL" if orphans else "PASS"
    return status, orphans


def excessive_admin_test(users, threshold=0.10):
    total = len(users)
    admins = sum(1 for d in users.values() if d.get("role") == "admin")
    ratio = admins / total if total > 0 else 0
    status = "FAIL" if ratio > threshold else "PASS"
    return status, ratio


def terminated_but_active_test(users):
    issues = [
        u for u, d in users.items()
        if d.get("status") == "terminated" and d.get("active", True)
    ]
    status = "FAIL" if issues else "PASS"
    return status, issues
