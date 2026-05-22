print("UPDATED VERSION LOADED")
from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

# -------------------------------
# Doctors Database
# -------------------------------

doctors = {
    "Cardiology": ["Dr. Sharma", "Dr. Reddy"],
    "Neurology": ["Dr. Mehta"],
    "Pulmonology": ["Dr. Khan", "Dr. Priya"],
    "General": ["Dr. Kumar", "Dr. Rao"],
    "Gastroenterology": [],
    "Emergency": ["Dr. Patel"]
}

# -------------------------------
# Bed Availability
# -------------------------------

beds = {
    "ICU": 3,
    "General Ward": 10,
    "Emergency Ward": 2
}

# -------------------------------
# Disease Prediction Function
# -------------------------------

def predict_disease(symptoms):

    symptoms = [s.lower() for s in symptoms]

    # Dengue
    if "fever" in symptoms and "body pain" in symptoms:
        return {
            "disease": "Dengue",
            "severity": "High",
            "department": "General",
            "ward": "ICU"
        }

    # Heart Attack
    elif "heart pain" in symptoms or "chest pain" in symptoms:
        return {
            "disease": "Heart Disease",
            "severity": "Critical",
            "department": "Cardiology",
            "ward": "ICU"
        }

    # Asthma
    elif "breathing issue" in symptoms or "cough" in symptoms:
        return {
            "disease": "Asthma",
            "severity": "Medium",
            "department": "Pulmonology",
            "ward": "Emergency Ward"
        }

    # Migraine
    elif "headache" in symptoms:
        return {
            "disease": "Migraine",
            "severity": "Low",
            "department": "Neurology",
            "ward": "General Ward"
        }

    # Food Poisoning
    elif "vomiting" in symptoms or "stomach pain" in symptoms:
        return {
            "disease": "Food Poisoning",
            "severity": "Medium",
            "department": "Gastroenterology",
            "ward": "General Ward"
        }

    # Appendix
    elif "abdomen pain" in symptoms:
        return {
            "disease": "Appendicitis",
            "severity": "High",
            "department": "Emergency",
            "ward": "Emergency Ward"
        }

    # Default
    else:
        return {
            "disease": "Normal Fever",
            "severity": "Low",
            "department": "General",
            "ward": "General Ward"
        }


# -------------------------------
# HTML PAGE
# -------------------------------

HTML = """

<!DOCTYPE html>
<html>
<head>
    <title>AI Hospital Resource Management</title>

    <style>

        body{
            font-family: Arial;
            background: #f4f7fc;
            padding: 20px;
        }

        .container{
            max-width: 800px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px gray;
        }

        h1{
            text-align: center;
            color: darkblue;
        }

        input{
            width: 100%;
            padding: 12px;
            margin-top: 10px;
        }

        button{
            background: darkblue;
            color: white;
            padding: 12px;
            width: 100%;
            border: none;
            margin-top: 20px;
            cursor: pointer;
        }

        .result{
            margin-top: 20px;
            background: #eef;
            padding: 20px;
            border-radius: 10px;
        }

        .danger{
            color: red;
            font-weight: bold;
        }

        .success{
            color: green;
            font-weight: bold;
        }

    </style>

</head>

<body>

<div class="container">

<h1>AI Based Hospital Resource Management</h1>

<form method="POST">

<label>Enter Symptoms (comma separated)</label>

<input type="text" name="symptoms"
placeholder="fever, cough, headache, vomiting">

<button type="submit">Analyze Patient</button>

</form>

{% if result %}

<div class="result">

<h2>Patient Report</h2>

<p><b>Disease:</b> {{ result.disease }}</p>

<p><b>Severity:</b> {{ result.severity }}</p>

<p><b>Recommended Ward:</b> {{ result.ward }}</p>

<p><b>Department:</b> {{ result.department }}</p>

<h3>Doctor Status</h3>

{% if doctor_available %}

<p class="success">
Doctor Assigned:
<b>{{ doctor }}</b>
</p>

{% else %}

<p class="danger">
Doctors are not available currently.<br>
Please visit another hospital. Sorry.
</p>

{% endif %}

<h3>Bed Availability</h3>

<p>ICU Beds: {{ beds['ICU'] }}</p>
<p>General Ward Beds: {{ beds['General Ward'] }}</p>
<p>Emergency Ward Beds: {{ beds['Emergency Ward'] }}</p>

</div>

{% endif %}

</div>

</body>
</html>

"""

# -------------------------------
# Main Route
# -------------------------------

@app.route("/", methods=["GET", "POST"])

def home():

    result = None
    doctor = None
    doctor_available = False

    if request.method == "POST":

        symptoms = request.form["symptoms"].split(",")

        result = predict_disease(symptoms)

        dept = result["department"]

        available_doctors = doctors.get(dept, [])

        if len(available_doctors) > 0:

            doctor_available = True
            doctor = random.choice(available_doctors)

        else:

            doctor_available = False

    return render_template_string(
        HTML,
        result=result,
        doctor=doctor,
        doctor_available=doctor_available,
        beds=beds
    )

# -------------------------------
# Run App
# -------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)