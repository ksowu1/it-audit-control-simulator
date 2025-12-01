import os
import csv
from datetime import datetime
from fpdf import FPDF


# ----------------------------
# RISK SCORING SYSTEM
# ----------------------------

def calculate_risk_score(results: dict) -> dict:
    """
    Calculates risk rating based on failed controls.
    """
    total_controls = len(results)
    failed_controls = sum(1 for _, (status, _) in results.items() if status == "FAIL")

    if failed_controls == 0:
        rating = "LOW"
    elif failed_controls <= max(1, int(total_controls * 0.33)):
        rating = "MEDIUM"
    else:
        rating = "HIGH"

    return {
        "total": total_controls,
        "failed": failed_controls,
        "passed": total_controls - failed_controls,
        "rating": rating,
    }


# ----------------------------
# "AI" RECOMMENDATION ENGINE
# ----------------------------

def generate_recommendations(results: dict, risk_info: dict) -> list:
    """
    Generates human-readable recommendations based on failed controls.
    This is a rule-based engine that acts like an AI advisor.
    """
    recs = []

    # Overall risk-level recommendation
    if risk_info["rating"] == "HIGH":
        recs.append(
            "Overall risk is HIGH. Escalate to IT leadership and Internal Audit, and "
            "prioritize remediation of the most critical control failures within 30 days."
        )
    elif risk_info["rating"] == "MEDIUM":
        recs.append(
            "Overall risk is MEDIUM. Plan remediation activities and track them with "
            "owners and target dates over the next 60–90 days."
        )
    else:
        recs.append(
            "Overall risk is LOW. Maintain current controls, continue monitoring, and "
            "schedule periodic re-tests at least annually."
        )

    # Control-specific recommendations
    for control, (status, details) in results.items():
        if status != "FAIL":
            continue

        name = control.lower()

        if "orphan" in name:
            recs.append(
                "Review all orphan accounts (e.g., users with no valid owner) and either "
                "disable, remove, or reassign them according to the user lifecycle policy."
            )

        if "excessive_admin" in name or "admin_overuse" in name or "excessive" in name:
            recs.append(
                "Reduce the number of admin accounts by enforcing least privilege, using "
                "role-based access control (RBAC), and requiring approvals for admin role assignments."
            )

        if "terminated" in name:
            recs.append(
                "Align HR offboarding with IT deprovisioning. Ensure terminated users are "
                "disabled on or before their termination date, and perform periodic reviews for exceptions."
            )

        if "privileged_access" in name:
            recs.append(
                "Implement a formal privileged access management (PAM) process, including "
                "just-in-time elevation, session logging, and periodic recertification of privileged accounts."
            )

        if "sod" in name or "segregation" in name:
            recs.append(
                "Review Segregation of Duties (SoD) conflicts and redesign roles so that no single "
                "user can both request and approve, or develop and deploy, sensitive changes."
            )

        if "unapproved_change" in name:
            recs.append(
                "Require documented change approvals prior to deployment. Enforce this via change "
                "management tooling or deployment gates that block unapproved changes."
            )

        if "approval_before_deployment" in name:
            recs.append(
                "Ensure approval timestamps precede deployment timestamps. Investigate any changes "
                "deployed before approval and strengthen the change workflow controls."
            )

        if "backup_recency" in name or "backup_age" in name:
            recs.append(
                "Increase backup frequency, especially for critical systems. Validate that at least one "
                "recent backup (≤ 7 days old) exists for each in-scope system."
            )

        if "backup_success" in name or "backup_failure" in name:
            recs.append(
                "Investigate failed backup jobs, correct root causes (e.g., capacity, permissions, schedule), "
                "and implement alerting so failures are reviewed daily."
            )

    # Fallback if nothing specific was generated
    if not recs:
        recs.append(
            "No critical issues detected. Continue monitoring and maintain your current control environment."
        )

    # Deduplicate while preserving order
    deduped = []
    seen = set()
    for r in recs:
        if r not in seen:
            deduped.append(r)
            seen.add(r)

    return deduped


# ----------------------------
# CSV EXPORT
# ----------------------------

def export_csv(results: dict, output_dir: str = "export") -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(output_dir, f"audit_results_{timestamp}.csv")

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Control Name", "Status", "Details"])

        for control, (status, details) in results.items():
            writer.writerow([control, status, details])

    return filename


# ----------------------------
# PDF EXPORT (WITH EXEC SUMMARY + RECS)
# ----------------------------

def export_pdf(results: dict, scenario_name="Audit Scenario", output_dir="export") -> str:
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.join(output_dir, f"audit_report_{timestamp}.pdf")

    risk = calculate_risk_score(results)
    recommendations = generate_recommendations(results, risk)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Title Area
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, f"IT Audit Report – {scenario_name}", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)

    # Executive Summary
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Executive Summary", ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", size=12)
    pdf.multi_cell(
        0,
        7,
        f"Overall Risk Rating: {risk['rating']}\n"
        f"Total Controls Tested: {risk['total']}\n"
        f"Passed: {risk['passed']}\n"
        f"Failed: {risk['failed']}\n",
    )

    pdf.ln(5)

    # Control Results
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Control-by-Control Results", ln=True)
    pdf.ln(4)

    for control, (status, details) in results.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, control.replace("_", " ").title(), ln=True)

        pdf.set_font("Arial", size=11)
        pdf.cell(0, 6, f"Status: {status}", ln=True)

        if details:
            pdf.multi_cell(0, 6, f"Details: {details}")

        pdf.ln(3)

    # Recommendations Section
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Recommendations", ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", size=12)
    for idx, rec in enumerate(recommendations, start=1):
        pdf.multi_cell(0, 7, f"{idx}. {rec}")
        pdf.ln(2)

    pdf.output(filename)
    return filename
