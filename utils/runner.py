from controls.access_control import (
    orphan_account_test,
    excessive_admin_test,
    terminated_but_active_test,
)

from controls.change_management import (
    unapproved_change_test,
    approval_before_deployment_test,
)

from controls.backup_recovery import (
    backup_recency_test,
    backup_success_test,
)

from controls.sod import (
    privileged_access_test,
    sod_violation_test,
)


def run_scenario(runtime_data: dict) -> dict:
    """
    Executes all audit controls on the provided scenario.
    Returns a structured dict of results.
    """
    users = runtime_data["users"]
    changes = runtime_data["changes"]
    backups = runtime_data["backups"]
    sod_rules = runtime_data["sod_rules"]

    return {
        "orphan_accounts": orphan_account_test(users),
        "admin_ratio": excessive_admin_test(users),
        "terminated_accounts": terminated_but_active_test(users),
        "privileged_misuse": privileged_access_test(users),
        "sod_violations": sod_violation_test(users, sod_rules),
        "unapproved_changes": unapproved_change_test(changes),
        "approval_order_errors": approval_before_deployment_test(changes),
        "old_backups": backup_recency_test(backups),
        "failed_backups": backup_success_test(backups),
    }
