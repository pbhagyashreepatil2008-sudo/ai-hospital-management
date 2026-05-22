from flask import Flask, render_template_string, request
import random
from datetime import datetime

app = Flask(__name__)

# ------------------------------------
# LOGIN DETAILS
# ------------------------------------

USERNAME = "admin"
PASSWORD = "1234"

# ------------------------------------
# PATIENT HISTORY
# ------------------------------------

patient_history = []

# ------------------------------------
# DOCTOR DATABASE
# ------------------------------------

doctors = {
    "Cardiology": ["Dr. Sharma", "Dr. Reddy"],
    "Neurology": ["Dr. Mehta"],
    "Pulmonology": ["Dr. Khan"],
    "General": ["Dr. Kumar", "Dr. Rao"],
    "Emergency": ["Dr. Patel"],
    "Gastroenterology": [],
    "ENT": ["Dr. Priya"]
}

# ------------------------------------
# BED MANAGEMENT
# ------------------------------------

beds = {
    "ICU": 3,
    "General Ward": 10,
    "Emergency Ward": 2
}

# ------------------------------------
# HTML PAGE
# ------------------------------------

HTML = """

<!DOCTYPE html>
<html>

<head>

<title>AI Hospital Resource Management</title>

<style>

body{
    font-family: Arial;
    background: #eef3ff;
    margin: 0;
    padding: 0;
}

.header{
    background: darkblue;
    color: white;
    padding: 20px;
    text-align: center;
}

.login-box{
    width: 350px;
    margin: auto;
    margin-top: 100px;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0px 0px 10px gray;
}

.container{
    width: 90%;
    margin: auto;
    margin-top: 20px;
}

.card{
    background: white;
    padding: 20px;
    margin-top: 20px;
    border-radius: 12px;
    box-shadow: 0px 0px 8px lightgray;
}

input[type=text],
input[type=password]{
    width: 100%;
    padding: 12px;
    margin-top: 10px;
}

button{
    width: 100%;
    padding: 12px;
    background: darkblue;
    color: white;
    border: none;
    margin-top: 20px;
    cursor: pointer;
    border-radius: 6px;
}

.symptoms{
    display: grid;
    grid-template-columns: repeat(3,1fr);
    gap: 10px;
    margin-top: 20px;
}

.green{
    color: green;
    font-weight: bold;
}

.red{
    color: red;
    font-weight: bold;
}

.history-table{
    width: 100%;
    border-collapse: collapse;
}

.history-table th,
.history-table td{
    border: 1px solid gray;
    padding: 10px;
    text-align: center;
}

.history-table th{
    background: darkblue;
    color: white;
}

</style>

</head>

<body>

<div class="header">
<h1>AI BASED HOSPITAL RESOURCE MANAGEMENT</h1>
</div>

{% if not logged_in %}

<div class="login-box">

<h2 align="center">Login</h2>

<form method="POST">

<input type="hidden" name="action" value="login">

<input type="text"
name="username"
placeholder="Enter Username"
required>

<input type="password"
name="password"
placeholder="Enter Password"
required>

<button type="submit">Login</button>

</form>

{% if error %}
<p class="red">{{ error }}</p>
{% endif %}

</div>

{% else %}

<div class="container">

<div class="card">

<h2>Select Symptoms</h2>

<form method="POST">

<input type="hidden" name="action" value="analyze">

<div class="symptoms">

<label><input type="checkbox" name="symptoms" value="fever"> Fever</label>

<label><input type="checkbox" name="symptoms" value="cough"> Cough</label>

<label><input type="checkbox" name="symptoms" value="headache"> Headache</label>

<label><input type="checkbox" name="symptoms" value="vomiting"> Vomiting</label>

<label><input type="checkbox" name="symptoms" value="stomach pain"> Stomach Pain</label>

<label><input type="checkbox" name="symptoms" value="abdomen pain"> Abdomen Pain</label>

<label><input type="checkbox" name="symptoms" value="breathing issue"> Breathing Issue</label>

<label><input type="checkbox" name="symptoms" value="chest pain"> Chest Pain</label>

<label><input type="checkbox" name="symptoms" value="body pain"> Body Pain</label>

<label><input type="checkbox" name="symptoms" value="nose bleeding"> Nose Bleeding</label>

<label><input type="checkbox" name="symptoms" value="mouth bleeding"> Mouth Bleeding</label>

<label><input type="checkbox" name="symptoms" value="heart pain"> Heart Pain</label>

</div>

<button type="submit">
Analyze Patient
</button>

</form>

</div>

{% if result %}

<div class="card">

<h2>Patient Report</h2>

<p><b>Disease:</b> {{ result.disease }}</p>

<p><b>Severity:</b> {{ result.severity }}</p>

<p><b>Department:</b> {{ result.department }}</p>

<p><b>Recommended Ward:</b> {{ result.ward }}</p>

<h3>Doctor Allocation</h3>

{% if doctor_available %}

<p class="green">
Doctor Assigned:
<b>{{ doctor }}</b>
</p>

{% else %}

<p class="red">
Doctors are not available currently.<br>
Please go to another hospital. Sorry.
</p>

{% endif %}

<h3>Bed Availability</h3>

<p>ICU Beds: {{ beds['ICU'] }}</p>
<p>General Ward Beds: {{ beds['General Ward'] }}</p>
<p>Emergency Ward Beds: {{ beds['Emergency Ward'] }}</p>

</div>

{% endif %}

<div class="card">

<h2>Patient History</h2>

<table class="history-table">

<tr>
<th>Time</th>
<th>Symptoms</th>
<th>Disease</th>
<th>Severity</th>
<th>Doctor</th>
</tr>

{% for item in history %}

<tr>

<td>{{ item.time }}</td>

<td>{{ item.symptoms }}</td>

<td>{{ item.disease }}</td>

<td>{{ item.severity }}</td>

<td>{{ item.doctor }}</td>

</tr>

{% endfor %}

</table>

</div>

</div>

{% endif %}

</body>
</html>

"""

# ------------------------------------
# DISEASE PREDICTION
# ------------------------------------

def predict_disease(symptoms):

    symptoms = [s.lower() for s in symptoms]

    if "fever" in symptoms and "body pain" in symptoms:
        return {
            "disease": "Dengue",
            "severity": "High",
            "department": "General",
            "ward": "ICU"
        }

    elif "chest pain" in symptoms or "heart pain" in symptoms:
        return {
            "disease": "Heart Disease",
            "severity": "Critical",
            "department": "Cardiology",
            "ward": "ICU"
        }

    elif "breathing issue" in symptoms or "cough" in symptoms:
        return {
            "disease": "Asthma",
            "severity": "Medium",
            "department": "Pulmonology",
            "ward": "Emergency Ward"
        }

    elif "headache" in symptoms:
        return {
            "disease": "Migraine",
            "severity": "Low",
            "department": "Neurology",
            "ward": "General Ward"
        }

    elif "vomiting" in symptoms or "stomach pain" in symptoms:
        return {
            "disease": "Food Poisoning",
            "severity": "Medium",
            "department": "Gastroenterology",
            "ward": "General Ward"
        }

    elif "abdomen pain" in symptoms:
        return {
            "disease": "Appendicitis",
            "severity": "High",
            "department": "Emergency",
            "ward": "Emergency Ward"
        }

    elif "nose bleeding" in symptoms or "mouth bleeding" in symptoms:
        return {
            "disease": "ENT Infection",
            "severity": "Medium",
            "department": "ENT",
            "ward": "General Ward"
        }

    else:
        return {
            "disease": "Normal Fever",
            "severity": "Low",
            "department": "General",
            "ward": "General Ward"
        }

# ------------------------------------
# MAIN ROUTE
# ------------------------------------

@app.route("/", methods=["GET", "POST"])

def home():

    logged_in = False
    result = None
    doctor = None
    doctor_available = False
    error = None

    if request.method == "POST":

        action = request.form.get("action")

        # LOGIN

        if action == "login":

            username = request.form.get("username")
            password = request.form.get("password")

            if username == USERNAME and password == PASSWORD:
                logged_in = True

            else:
                error = "Invalid Username or Password"

        # ANALYZE

        elif action == "analyze":

            logged_in = True

            symptoms = request.form.getlist("symptoms")

            result = predict_disease(symptoms)

            department = result["department"]

            available_doctors = doctors.get(department, [])

            if len(available_doctors) > 0:

                doctor_available = True

                doctor = random.choice(available_doctors)

            else:

                doctor = "Not Available"

            # SAVE HISTORY

            patient_history.append({
                "time": datetime.now().strftime("%H:%M:%S"),
                "symptoms": ", ".join(symptoms),
                "disease": result["disease"],
                "severity": result["severity"],
                "doctor": doctor
            })

    return render_template_string(
        HTML,
        logged_in=logged_in,
        result=result,
        doctor=doctor,
        doctor_available=doctor_available,
        beds=beds,
        history=patient_history,
        error=error
    )

# ------------------------------------
# RUN APP
# ------------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)