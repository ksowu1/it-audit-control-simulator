
import os
import json
from datetime import datetime, timedelta

from config.config_loader import load_config
from tests.access_control import (
    orphan_account_test,
    excessive_admin_test,
    terminated_but_active_test,
)
from tests.sod import privileged_access_test, sod_violation_test
from tests.change_management import unapproved_change_test, approval_before_deployment_test
from tests.backup_recovery import backup_recency_test, backup_success_test
from export.csv_exporter import export_csv

# --- load config ---
base_path = os.path.dirname(os.path.abspath(__file__))
cfg = load_config()
users = cfg["users"]           # dict username -> details
changes = cfg["changes"]       # list of change dicts with datetimes
backups = cfg["backups"]       # list of backup dicts with 'date' and 'success'
sod_rules = cfg["sod_rules"]   # list of SoD rule dicts/lists

# --- run tests and collect failures ---
failed_controls = []

print("\n=== Access Control Tests ===")
r1 = orphan_account_test(users)
print("1.", r1)
if r1[0] == "FAIL":
    failed_controls.append(["Orphan Account Test", str(r1[1])])

r2 = excessive_admin_test(users)
print("2.", r2)
if r2[0] == "FAIL":
    failed_controls.append(["Admin Overuse Test", f"Admin ratio {r2[1]:.2f}"])

r3 = terminated_but_active_test(users)
print("3.", r3)
if r3[0] == "FAIL":
    failed_controls.append(["Terminated but Active Accounts", str(r3[1])])

print("\n=== Privileged Access & SoD ===")
r4 = privileged_access_test(users)
print("4.", r4)
if r4[0] == "FAIL":
    failed_controls.append(["Privileged Access Misuse", str(r4[1])])

r5 = sod_violation_test(users, sod_rules)
print("5.", r5)
if r5[0] == "FAIL":
    failed_controls.append(["SoD Violations", str(r5[1])])

print("\n=== Change Management Tests ===")
r6 = unapproved_change_test(changes)
print("6.", r6)
if r6[0] == "FAIL":
    failed_controls.append(["Unapproved Change Deployment", str(r6[1])])

r7 = approval_before_deployment_test(changes)
print("7.", r7)
if r7[0] == "FAIL":
    failed_controls.append(["Approval Before Deployment Error", str(r7[1])])

print("\n=== Backup & Recovery Tests ===")
r8 = backup_recency_test(backups)
print("8.", r8)
if r8[0] == "FAIL":
    failed_controls.append(["Old Backups", str(r8[1])])

r9 = backup_success_test(backups)
print("9.", r9)
if r9[0] == "FAIL":
    failed_controls.append(["Failed Backups", str(r9[1])])

# --- Ask user whether to export failures ---
if failed_controls:
    while True:
        choice = input("\nExport failing controls to CSV? (y/n): ").strip().lower()
        if choice in ("y", "n"):
            break
    if choice == "y":
        out_path = os.path.join(base_path, "failed_controls.csv")
        export_csv(out_path, failed_controls)
        print(f"\nCSV export complete → {out_path}")
    else:
        print("\nCSV export skipped by user.")
else:
    print("\nNo failing controls found — CSV export skipped.")
