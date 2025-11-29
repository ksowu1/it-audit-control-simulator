
def privileged_access_test(users):
    """
    Find users who are marked privileged but are not admins (possible misuse).
    """
    bad = [u for u, d in users.items() if d.get("privileged") and d.get("role") != "admin"]
    status = "FAIL" if bad else "PASS"
    return status, bad


def sod_violation_test(users, rules):
    """
    rules: list of dicts {role1, role2} meaning holding both duties is a conflict.
    We assume each user has 'duties' list (strings).
    """
    violations = []

    for uname, data in users.items():
        duties = set(data.get("duties", []))
        for r in rules:
            # support both dict or list formats for rules
            if isinstance(r, dict):
                a = r.get("role1")
                b = r.get("role2")
            elif isinstance(r, list) and len(r) >= 2:
                a, b = r[0], r[1]
            else:
                continue

            if a in duties and b in duties:
                violations.append({"user": uname, "conflict": f"{a} & {b}"})

    status = "FAIL" if violations else "PASS"
    return status, violations
