import os
import json
from flask import Flask, render_template, request, redirect, send_file
from werkzeug.utils import secure_filename

from config.config_loader import load_config
from utils.scenario import (
    prepare_runtime_data,
    load_scenario_from_file
)
from utils.runner import run_scenario
from reporting.report_generator import export_pdf, export_csv

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "web/uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    """
    Accepts a JSON scenario file uploaded by the user.
    """
    if "file" not in request.files:
        return redirect("/error")

    file = request.files["file"]

    if file.filename == "":
        return redirect("/error")

    filename = secure_filename(file.filename)
    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(path)

    # Load and run scenario
    scenario_runtime = load_scenario_from_file(path)
    results = run_scenario(scenario_runtime)

    # Store results temporarily
    results_path = os.path.join(app.config["UPLOAD_FOLDER"], "latest_results.json")
    with open(results_path, "w") as f:
        json.dump(results, f)

    return render_template("results.html", results=results)


@app.route("/run_default")
def run_default():
    raw = load_config()
    runtime = prepare_runtime_data(raw)
    results = run_scenario(runtime)

    # Save temporary results
    results_path = os.path.join(app.config["UPLOAD_FOLDER"], "latest_results.json")
    with open(results_path, "w") as f:
        json.dump(results, f)

    return render_template("results.html", results=results)


@app.route("/download_pdf")
def download_pdf():
    # Use the latest results
    path = os.path.join(app.config["UPLOAD_FOLDER"], "latest_results.json")
    if not os.path.exists(path):
        return "No results to export."

    with open(path, "r") as f:
        results = json.load(f)

    filename = export_pdf(results, scenario_name="Web Scenario")
    return send_file(filename, as_attachment=True)


@app.route("/download_csv")
def download_csv():
    path = os.path.join(app.config["UPLOAD_FOLDER"], "latest_results.json")
    if not os.path.exists(path):
        return "No results to export."

    with open(path, "r") as f:
        results = json.load(f)

    filename = export_csv(results)
    return send_file(filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
