from flask import Flask, render_template_string, request
import random
from datetime import datetime

app = Flask(__name__)

# -----------------------------------
# LOGIN DETAILS
# -----------------------------------

USERNAME = "admin"
PASSWORD = "1234"

# -----------------------------------
# PATIENT HISTORY
# -----------------------------------

patient_history = []

# -----------------------------------
# DOCTORS DATABASE
# -----------------------------------

doctors = {
    "Cardiology": ["Dr. Sharma", "Dr. Reddy"],
    "Neurology": ["Dr. Mehta"],
    "Pulmonology": ["Dr. Khan"],
    "General": ["Dr. Kumar", "Dr. Rao"],
    "Emergency": ["Dr. Patel"],
    "Gastroenterology": [],
    "ENT": ["Dr. Priya"]
}

# -----------------------------------
# BED MANAGEMENT
# -----------------------------------

beds = {
    "ICU": 3,
    "General Ward": 10,
    "Emergency Ward": 2
}

# -----------------------------------
# HTML TEMPLATE
# -----------------------------------

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
input[type=password],
input[type=number],
select{
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

<h2>Patient Details</h2>

<form method="POST">

<input type="hidden" name="action" value="analyze">

<input type="text"
name="patient_name"
placeholder="Enter Patient Name"
required>

<input type="number"
name="age"
placeholder="Enter Age"
required>

<input type="text"
name="phone"
placeholder="Enter Phone Number"
required>

<select name="gender">

<option value="Male">Male</option>

<option value="Female">Female</option>

<option value="Other">Other</option>

</select>

<h2>Select Symptoms</h2>

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

<p><b>Patient Name:</b> {{ patient_name }}</p>

<p><b>Age:</b> {{ age }}</p>

<p><b>Gender:</b> {{ gender }}</p>

<p><b>Phone:</b> {{ phone }}</p>

<hr>

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
No beds or doctors are available currently.<br>
Please visit another hospital immediately.
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
<th>Name</th>
<th>Age</th>
<th>Gender</th>
<th>Phone</th>
<th>Disease</th>
<th>Severity</th>
<th>Doctor</th>

</tr>

{% for item in history %}

<tr>

<td>{{ item.time }}</td>
<td>{{ item.name }}</td>
<td>{{ item.age }}</td>
<td>{{ item.gender }}</td>
<td>{{ item.phone }}</td>
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

# -----------------------------------
# DISEASE PREDICTION
# -----------------------------------

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