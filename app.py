from flask import Flask, render_template_string, request
import random

app = Flask(__name__)

# -----------------------------------
# DOCTORS DATABASE
# -----------------------------------

doctors = {
    "Cardiology": ["Dr. Sharma", "Dr. Reddy"],
    "Neurology": ["Dr. Mehta"],
    "Pulmonology": ["Dr. Khan"],
    "General": ["Dr. Kumar", "Dr. Rao"],
    "Emergency": ["Dr. Patel"],
    "Gastroenterology": []
}

# -----------------------------------
# BED AVAILABILITY
# -----------------------------------

beds = {
    "ICU": 3,
    "General Ward": 10,
    "Emergency Ward": 2
}

# -----------------------------------
# LOGIN DETAILS
# -----------------------------------

USERNAME = "admin"
PASSWORD = "1234"

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

.container{
    width: 80%;
    margin: auto;
    margin-top: 40px;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0px 0px 10px gray;
}

h1{
    text-align: center;
    color: darkblue;
}

.login-box{
    width: 400px;
    margin: auto;
    margin-top: 100px;
    background: white;
    padding: 30px;
    border-radius: 12px;
    box-shadow: 0px 0px 10px gray;
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
    grid-template-columns: repeat(2,1fr);
    margin-top: 20px;
}

.card{
    background: #f2f6ff;
    padding: 20px;
    border-radius: 10px;
    margin-top: 20px;
}

.red{
    color: red;
    font-weight: bold;
}

.green{
    color: green;
    font-weight: bold;
}

</style>

</head>

<body>

{% if not logged_in %}

<div class="login-box">

<h1>Hospital Login</h1>

<form method="POST">

<input type="hidden" name="action" value="login">

<input type="text" name="username"
placeholder="Enter Username" required>

<input type="password" name="password"
placeholder="Enter Password" required>

<button type="submit">Login</button>

</form>

{% if error %}
<p class="red">{{ error }}</p>
{% endif %}

</div>

{% else %}

<div class="container">

<h1>AI Based Hospital Resource Management</h1>

<form method="POST">

<input type="hidden" name="action" value="analyze">

<h3>Select Symptoms</h3>

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

<button type="submit">Analyze Patient</button>

</form>

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

</div>

{% endif %}

</body>
</html>

"""

# -----------------------------------
# DISEASE PREDICTION FUNCTION
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

    else:
        return {
            "disease": "Normal Fever",
            "severity": "Low",
            "department": "General",
            "ward": "General Ward"
        }

# -----------------------------------
# MAIN ROUTE
# -----------------------------------

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

        # ANALYZE PATIENT

        elif action == "analyze":

            logged_in = True

            symptoms = request.form.getlist("symptoms")

            result = predict_disease(symptoms)

            department = result["department"]

            available_doctors = doctors.get(department, [])

            if len(available_doctors) > 0:

                doctor_available = True

                doctor = random.choice(available_doctors)

    return render_template_string(
        HTML,
        logged_in=logged_in,
        result=result,
        doctor=doctor,
        doctor_available=doctor_available,
        beds=beds,
        error=error
    )

# -----------------------------------
# RUN APP
# -----------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)