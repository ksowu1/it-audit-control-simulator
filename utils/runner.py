"""
Central scenario execution engine.

Takes a "scenario_runtime" dictionary built from:
- config file
- interactive builder
- uploads
- presets

Then runs each control test function and aggregates results.
"""

from typing import Dict, Any, Tuple

from tests.access_control import (
    orphan_account_test,
    excessive_admin_test,
    terminated_but_active_test,
)

from tests.sod import (
    privileged_access_test,
    sod_violation_test,
)

from tests.change_management import (
    unapproved_change_test,
    approval_before_deployment_test,
)

from tests.backup_recovery import (
    backup_recency_test,
    backup_success_test,
)


def run_scenario(runtime: Dict[str, Any]) -> Dict[str, Tuple[str, Any]]:
    """
    Executes all audit controls on the provided runtime dataset.

    runtime structure:
    {
        "users": {...},
        "changes": [...],
        "backups": [...],
        "sod_rules": [...]
    }
    """
    results: Dict[str, Tuple[str, Any]] = {}

    # =============================
    #        ACCESS CONTROL
    # =============================
    results["orphan_account_test"] = orphan_account_test(runtime["users"])
    results["excessive_admin_test"] = excessive_admin_test(runtime["users"])
    results["terminated_but_active_test"] = terminated_but_active_test(runtime["users"])

    # =============================
    #   PRIVILEGED ACCESS & SOD
    # =============================
    results["privileged_access_test"] = privileged_access_test(runtime["users"])
    results["sod_violation_test"] = sod_violation_test(runtime["users"], runtime["sod_rules"])

    # =============================
    #    CHANGE MANAGEMENT
    # =============================
    results["unapproved_change_test"] = unapproved_change_test(runtime["changes"])
    results["approval_before_deployment_test"] = approval_before_deployment_test(runtime["changes"])

    # =============================
    #   BACKUP & RECOVERY
    # =============================
    results["backup_recency_test"] = backup_recency_test(runtime["backups"])
    results["backup_success_test"] = backup_success_test(runtime["backups"])

    return results
