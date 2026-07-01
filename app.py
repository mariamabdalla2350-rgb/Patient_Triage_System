# app.py
# Flask server — connects the webpage to the triage logic

from flask import Flask, render_template, request
from patient import Patient
from triage_rules import assign_triage

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        # Get data from the form
        name         = request.form.get("name")
        age          = int(request.form.get("age"))
        symptoms_raw = request.form.get("symptoms")
        symptoms     = [s.strip() for s in symptoms_raw.split(",")]
        pain_level   = int(request.form.get("pain_level"))
        fever        = float(request.form.get("fever"))
        pulse        = int(request.form.get("pulse"))
        sob          = request.form.get("shortness_of_breath") == "yes"

        # Run triage logic
        patient = Patient(name, age, symptoms, pain_level, fever, pulse, sob)
        assign_triage(patient)

        # Package result to send to the webpage
        result = {
            "name":     patient.name,
            "category": patient.triage_category,
            "reasons":  patient.triage_reason,
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)
    