import os
from typing import Dict, Any, Optional

from config.config_loader import load_config
from utils.scenario import prepare_runtime_data, load_scenario_from_file, build_interactive_scenario
from utils.runner import run_scenario


# Predefined scenarios you ship with the tool
PREDEFINED_SCENARIOS = {
    "1": ("Default Scenario", os.path.join("config", "default_scenario.json")),
    "2": ("High-Risk Scenario", os.path.join("config", "scenario_high_risk.json")),
    "3": ("Best-Practice Scenario", os.path.join("config", "scenario_best_practice.json")),
    "4": ("Change Management Failure Scenario", os.path.join("config", "scenario_change_failure.json")),
}


def _print_banner() -> None:
    print("\n" + "=" * 40)
    print("   IT AUDIT CONTROL SIMULATOR - MENU")
    print("=" * 40)


def _print_results(results: Dict[str, Any]) -> None:
    print("\n=== Audit Results ===\n")
    for control_name, (status, details) in results.items():
        label = control_name.replace("_", " ").title()
        print(f"{label}: {status}")
        if details:
            print(f"  Details: {details}")
        print("-" * 50)


def _basic_validate_config(raw: Dict[str, Any]) -> list:
    """
    Very simple structural validation to catch missing top-level keys.
    This keeps things user-friendly in the menu.
    """
    required_keys = ["access_control", "change_management", "backup_recovery", "sod_rules"]
    issues = []

    for k in required_keys:
        if k not in raw:
            issues.append(f"Missing top-level key: {k}")

    if "access_control" in raw and "users" not in raw["access_control"]:
        issues.append("access_control.users is missing")

    if "change_management" in raw and "changes" not in raw["change_management"]:
        issues.append("change_management.changes is missing")

    if "backup_recovery" in raw and "backups" not in raw["backup_recovery"]:
        issues.append("backup_recovery.backups is missing")

    if "sod_rules" in raw and "conflicts" not in raw["sod_rules"]:
        issues.append("sod_rules.conflicts is missing")

    return issues


def _load_and_prepare(path: str) -> Optional[Dict[str, Any]]:
    """
    Load a JSON config file, validate, and convert to runtime data.
    Returns None if validation fails.
    """
    if not os.path.exists(path):
        print(f"\n[ERROR] File not found: {path}")
        return None

    try:
        raw = load_config(path)
    except Exception as e:
        print(f"\n[ERROR] Failed to load JSON: {e}")
        return None

    issues = _basic_validate_config(raw)
    if issues:
        print("\n[ERROR] Dataset validation failed:")
        for issue in issues:
            print(f"  - {issue}")
        return None

    return prepare_runtime_data(raw)


def _choose_predefined_scenario() -> Optional[Dict[str, Any]]:
    print("\nAvailable predefined scenarios:")
    for key, (name, _) in PREDEFINED_SCENARIOS.items():
        print(f"  {key}. {name}")

    choice = input("Select a scenario number (or press Enter to cancel): ").strip()
    if not choice:
        return None

    if choice not in PREDEFINED_SCENARIOS:
        print("[ERROR] Invalid selection.")
        return None

    name, path = PREDEFINED_SCENARIOS[choice]
    print(f"\nLoading {name} from: {path}")
    return _load_and_prepare(path)


def _run_custom_config() -> None:
    path = input("\nEnter the path to your JSON dataset (e.g., config/my_scenario.json): ").strip()
    if not path:
        print("No path entered, returning to menu.")
        return

    scenario = _load_and_prepare(path)
    if scenario is None:
        print("Dataset invalid or could not be loaded.")
        return

    results = run_scenario(scenario)
    _print_results(results)


def _run_predefined() -> None:
    scenario = _choose_predefined_scenario()
    if scenario is None:
        print("No scenario selected or dataset invalid.")
        return

    results = run_scenario(scenario)
    _print_results(results)


def _run_interactive_quick() -> None:
    scenario = build_interactive_scenario()
    results = run_scenario(scenario)
    _print_results(results)


def run_interactive_menu() -> None:
    """
    Entry point for the interactive menu.
    Called from main.py when --menu is used.
    """
    while True:
        _print_banner()
        print("1. Run with custom JSON dataset")
        print("2. Run a predefined scenario")
        print("3. Quick interactive scenario builder")
        print("4. Validate a dataset (no execution)")
        print("5. Exit")

        choice = input("\nChoose an option [1-5]: ").strip()

        if choice == "1":
            _run_custom_config()
        elif choice == "2":
            _run_predefined()
        elif choice == "3":
            _run_interactive_quick()
        elif choice == "4":
            path = input("\nEnter path to JSON dataset to validate: ").strip()
            if not path:
                print("No path entered.")
                continue
            if not os.path.exists(path):
                print(f"[ERROR] File not found: {path}")
                continue
            try:
                raw = load_config(path)
            except Exception as e:
                print(f"[ERROR] Failed to load JSON: {e}")
                continue
            issues = _basic_validate_config(raw)
            if not issues:
                print("\n✅ Dataset structure looks valid.")
            else:
                print("\n❌ Dataset issues:")
                for issue in issues:
                    print(f"  - {issue}")
        elif choice == "5":
            print("\nExiting interactive menu.")
            break
        else:
            print("\n[ERROR] Invalid choice. Please select 1–5.")
