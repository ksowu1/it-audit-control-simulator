
import csv
import os

def export_csv(output_path, failed_controls):
    """
    Write failed_controls (list of [name, details]) to CSV at output_path.
    Returns the path written.
    """
    base = os.path.dirname(os.path.abspath(output_path))
    # ensure directory exists
    if base and not os.path.exists(base):
        os.makedirs(base, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Control Name", "Details"])
        writer.writerows(failed_controls)
    return output_path
