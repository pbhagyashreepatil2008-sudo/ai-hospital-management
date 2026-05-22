from flask import Flask, render_template_string, request, redirect, url_for, session
import random
from datetime import datetime

app = Flask(__name__)

app.secret_key = "hospital_secret"

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
    "Gastroenterology": ["Dr. Arjun"],
    "ENT": ["Dr. Priya"]
}

# -----------------------------------
# BED MANAGEMENT
# -----------------------------------

beds = {
    "ICU": 5,
    "General Ward": 15,
    "Emergency Ward": 3
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
    background:#eef3ff;
    margin:0;
    padding:0;
}

.header{
    background:darkblue;
    color:white;
    padding:20px;
    text-align:center;
}

.top-bar{
    text-align:right;
    padding:10px 30px;
}

.logout-btn{
    background:red;
    color:white;
    padding:10px 20px;
    text-decoration:none;
    border-radius:6px;
}

.login-box{
    width:350px;
    margin:auto;
    margin-top:100px;
    background:white;
    padding:30px;
    border-radius:12px;
    box-shadow:0px 0px 10px gray;
}

.container{
    width:90%;
    margin:auto;
    margin-top:20px;
}

.card{
    background:white;
    padding:20px;
    margin-top:20px;
    border-radius:12px;
    box-shadow:0px 0px 8px lightgray;
}

input[type=text],
input[type=password],
input[type=number],
select{
    width:100%;
    padding:12px;
    margin-top:10px;
}

button{
    width:100%;
    padding:12px;
    background:darkblue;
    color:white;
    border:none;
    margin-top:20px;
    border-radius:6px;
    cursor:pointer;
}

.symptoms{
    display:grid;
    grid-template-columns:repeat(3,1fr);
    gap:10px;
    margin-top:20px;
}

.green{
    color:green;
    font-weight:bold;
}

.red{
    color:red;
    font-weight:bold;
}

.history-table{
    width:100%;
    border-collapse:collapse;
}

.history-table th,
.history-table td{
    border:1px solid gray;
    padding:10px;
    text-align:center;
}

.history-table th{
    background:darkblue;
    color:white;
}

.dashboard{
    display:grid;
    grid-template-columns:repeat(4,1fr);
    gap:20px;
}

.dashboard-card{
    background:white;
    padding:20px;
    border-radius:12px;
    text-align:center;
    box-shadow:0px 0px 8px lightgray;
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

<div class="top-bar">
<a href="/logout" class="logout-btn">Logout</a>
</div>

<div class="container">

<!-- DASHBOARD -->

<div class="dashboard">

<div class="dashboard-card">
<h2>{{ history|length }}</h2>
<p>Total Patients</p>
</div>

<div class="dashboard-card">
<h2>{{ beds['ICU'] }}</h2>
<p>ICU Beds Left</p>
</div>

<div class="dashboard-card">
<h2>{{ beds['General Ward'] }}</h2>
<p>General Beds Left</p>
</div>

<div class="dashboard-card">
<h2>{{ beds['Emergency Ward'] }}</h2>
<p>Emergency Beds Left</p>
</div>

</div>

<!-- PATIENT FORM -->

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

<!-- REPORT -->

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
<p><b>Ward:</b> {{ result.ward }}</p>

{% if doctor_available %}

<p class="green">
Doctor Assigned:
<b>{{ doctor }}</b>
</p>

{% else %}

<p class="red">
No beds or doctors available.
</p>

{% endif %}

<h3>Bed Availability</h3>

<p>ICU Beds: {{ beds['ICU'] }}</p>
<p>General Ward Beds: {{ beds['General Ward'] }}</p>
<p>Emergency Ward Beds: {{ beds['Emergency Ward'] }}</p>

</div>

{% endif %}

<!-- SEARCH -->

<div class="card">

<h2>Search Patient</h2>

<form method="GET">

<input type="text"
name="search"
placeholder="Enter Patient Name">

<button type="submit">
Search
</button>

</form>

</div>

<!-- HISTORY -->

<div class="card">

<h2>Patient History</h2>

<table class="history-table">

<tr>

<th>Date</th>
<th>Time</th>
<th>Name</th>
<th>Age</th>
<th>Gender</th>
<th>Phone</th>
<th>Disease</th>
<th>Severity</th>
<th>Doctor</th>

</tr>

{% for item in filtered_history %}

<tr>

<td>{{ item.date }}</td>
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
            "disease":"Dengue",
            "severity":"High",
            "department":"General",
            "ward":"ICU"
        }

    elif "chest pain" in symptoms or "heart pain" in symptoms:
        return {
            "disease":"Heart Disease",
            "severity":"Critical",
            "department":"Cardiology",
            "ward":"ICU"
        }

    elif "breathing issue" in symptoms or "cough" in symptoms:
        return {
            "disease":"Asthma",
            "severity":"Medium",
            "department":"Pulmonology",
            "ward":"Emergency Ward"
        }

    elif "headache" in symptoms:
        return {
            "disease":"Migraine",
            "severity":"Low",
            "department":"Neurology",
            "ward":"General Ward"
        }

    elif "vomiting" in symptoms or "stomach pain" in symptoms:
        return {
            "disease":"Food Poisoning",
            "severity":"Medium",
            "department":"Gastroenterology",
            "ward":"General Ward"
        }

    elif "abdomen pain" in symptoms:
        return {
            "disease":"Appendicitis",
            "severity":"High",
            "department":"Emergency",
            "ward":"Emergency Ward"
        }

    else:
        return {
            "disease":"Normal Fever",
            "severity":"Low",
            "department":"General",
            "ward":"General Ward"
        }

# -----------------------------------
# HOME ROUTE
# -----------------------------------

@app.route("/", methods=["GET", "POST"])

def home():

    logged_in = session.get("logged_in", False)

    result = None
    doctor = None
    doctor_available = False
    error = None

    patient_name = ""
    age = ""
    gender = ""
    phone = ""

    search_query = request.args.get("search", "")

    filtered_history = patient_history

    if search_query:

        filtered_history = [

            item for item in patient_history

            if search_query.lower() in item["name"].lower()

        ]

    if request.method == "POST":

        action = request.form.get("action")

        # LOGIN

        if action == "login":

            username = request.form.get("username")
            password = request.form.get("password")

            if username == USERNAME and password == PASSWORD:

                session["logged_in"] = True

                return redirect(url_for("home"))

            else:

                error = "Invalid Username or Password"

        # ANALYZE

        elif action == "analyze":

            patient_name = request.form.get("patient_name")
            age = request.form.get("age")
            gender = request.form.get("gender")
            phone = request.form.get("phone")

            symptoms = request.form.getlist("symptoms")

            result = predict_disease(symptoms)

            department = result["department"]
            ward = result["ward"]

            available_doctors = doctors.get(department, [])

            if ward in beds and beds[ward] > 0:

                beds[ward] -= 1

                if len(available_doctors) > 0:

                    doctor_available = True
                    doctor = random.choice(available_doctors)

                else:

                    doctor = "Not Available"

            else:

                result["ward"] = "No Beds Available"
                doctor = "Not Available"

            patient_history.append({

                "date": datetime.now().strftime("%d-%m-%Y"),

                "time": datetime.now().strftime("%H:%M:%S"),

                "name": patient_name,

                "age": age,

                "gender": gender,

                "phone": phone,

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
        filtered_history=filtered_history,
        error=error,
        patient_name=patient_name,
        age=age,
        gender=gender,
        phone=phone

    )

# -----------------------------------
# LOGOUT
# -----------------------------------

@app.route("/logout")

def logout():

    session.clear()

    return redirect(url_for("home"))

# -----------------------------------
# RUN APP
# -----------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)