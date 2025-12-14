
import argparse
import os
from flask import Flask, render_template_string

from utils.scenario import load_scenario_from_file
from utils.runner import run_scenario

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>IT Audit Control Simulator</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 24px; background:#0d1117; color:#e6edf3; }
    .card { background:#161b22; border:1px solid #1f2937; border-radius:12px; padding:16px; margin-bottom:12px; }
    .pass { color:#22c55e; font-weight:700; }
    .fail { color:#ef4444; font-weight:700; }
    code { background:#0b1220; padding:2px 6px; border-radius:6px; }
  </style>
</head>
<body>
  <h1>IT Audit Control Simulator</h1>
  <p>Scenario: <code>{{ scenario_path }}</code></p>

  {% for name, result in results.items() %}
    {% set status = result[0] %}
    {% set details = result[1] %}
    <div class="card">
      <div>
        <span style="font-size:18px; font-weight:700;">{{ name.replace("_"," ").title() }}</span>
        —
        <span class="{{ 'pass' if status=='PASS' else 'fail' }}">{{ status }}</span>
      </div>
      {% if details %}
        <pre style="white-space:pre-wrap; margin-top:10px;">{{ details }}</pre>
      {% endif %}
    </div>
  {% endfor %}
</body>
</html>
"""

@app.route("/")
def home():
    return "Web app is running. Use /run to execute a scenario."

@app.route("/run")
def run_default():
    scenario_path = os.environ.get("SCENARIO_PATH", os.path.join("config", "default_scenario.json"))
    runtime = load_scenario_from_file(scenario_path)
    results = run_scenario(runtime)
    return render_template_string(HTML_TEMPLATE, results=results, scenario_path=scenario_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=os.path.join("config", "default_scenario.json"))
    parser.add_argument("--serve", action="store_true", help="Start the web server")
    args = parser.parse_args()

    # always set scenario path for web routes
    os.environ["SCENARIO_PATH"] = args.config

    if args.serve:
        app.run(host="127.0.0.1", port=5000, debug=True)
        return

    # CLI mode (prints results)
    runtime = load_scenario_from_file(args.config)
    results = run_scenario(runtime)
    print("\n=== Audit Results ===\n")
    for control_name, (status, details) in results.items():
        label = control_name.replace("_", " ").title()
        print(f"{label}: {status}")
        if details:
            print(f"  Details: {details}")
        print("-" * 50)

if __name__ == "__main__":
    main()
