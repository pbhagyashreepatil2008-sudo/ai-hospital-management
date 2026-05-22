from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ---------------------------------
# LOGIN DETAILS
# ---------------------------------

USERNAME = "admin"
PASSWORD = "1234"

# ---------------------------------
# HOSPITAL DATA
# ---------------------------------

TOTAL_BEDS = 100
occupied_beds = 35

# ---------------------------------
# PATIENT HISTORY
# ---------------------------------

patient_history = []

# ---------------------------------
# DOCTORS DATABASE
# ---------------------------------

doctors = [

    {
        "name": "Dr. Rajesh",
        "specialization": "Cardiologist",
        "available": True
    },

    {
        "name": "Dr. Priya",
        "specialization": "General Physician",
        "available": True
    },

    {
        "name": "Dr. Ahmed",
        "specialization": "Pulmonologist",
        "available": True
    },

    {
        "name": "Dr. Kavya",
        "specialization": "Neurologist",
        "available": True
    }
]

# ---------------------------------
# DISEASE DETECTION
# ---------------------------------

def detect_disease(symptoms):

    symptoms = [s.lower() for s in symptoms]

    if "fever" in symptoms and "cough" in symptoms and "breathing issue" in symptoms:
        return "COVID-19"

    elif "fever" in symptoms and "breathing issue" in symptoms:
        return "Pneumonia"

    elif "heart problem" in symptoms:
        return "Heart Disease"

    elif "body pain" in symptoms and "fever" in symptoms:
        return "Dengue"

    elif "headache" in symptoms and "fever" in symptoms:
        return "Migraine"

    elif "cough" in symptoms and "breathing issue" in symptoms:
        return "Asthma"

    elif "nose bleeding" in symptoms:
        return "Nasal Infection"

    elif "mouth bleeding" in symptoms:
        return "Gum Disease"

    else:
        return "General Checkup Required"

# ---------------------------------
# SEVERITY DETECTION
# ---------------------------------

def detect_severity(symptoms, disease):

    symptoms = [s.lower() for s in symptoms]

    if disease in ["COVID-19", "Pneumonia", "Heart Disease"]:

        return "HIGH"

    elif disease in ["Dengue", "Asthma", "Migraine"]:

        return "MEDIUM"

    else:

        return "LOW"

# ---------------------------------
# DOCTOR RECOMMENDATION
# ---------------------------------

def recommend_doctor(disease):

    if disease == "Heart Disease":
        specialization = "Cardiologist"

    elif disease in ["COVID-19", "Pneumonia", "Asthma"]:
        specialization = "Pulmonologist"

    elif disease == "Migraine":
        specialization = "Neurologist"

    else:
        specialization = "General Physician"

    for doctor in doctors:

        if doctor["specialization"] == specialization and doctor["available"]:

            return {
                "doctor_name": doctor["name"],
                "specialization": specialization
            }

    return {
        "doctor_name": "No Doctor Available",
        "specialization": specialization
    }

# ---------------------------------
# LOGIN PAGE
# ---------------------------------

@app.route("/", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == USERNAME and password == PASSWORD:

            return redirect(url_for("home"))

        else:

            error = "Invalid Username or Password"

    return render_template("login.html", error=error)

# ---------------------------------
# HOME PAGE
# ---------------------------------

@app.route("/home", methods=["GET", "POST"])
def home():

    global occupied_beds

    result = None

    if request.method == "POST":

        patient_name = request.form["patient_name"]
        age = request.form["age"]
        gender = request.form["gender"]

        symptoms = request.form.getlist("symptoms")

        disease = detect_disease(symptoms)

        severity = detect_severity(symptoms, disease)

        doctor = recommend_doctor(disease)

        available_beds = TOTAL_BEDS - occupied_beds

        if available_beds > 0:

            occupied_beds += 1
            status = "Bed Allocated"

        else:

            status = "⚠ No Beds Available - Transfer Patient"

        result = {

            "patient_name": patient_name,

            "age": age,

            "gender": gender,

            "symptoms": symptoms,

            "disease": disease,

            "severity": severity,

            "doctor_name": doctor["doctor_name"],

            "specialization": doctor["specialization"],

            "available_beds": TOTAL_BEDS - occupied_beds,

            "status": status
        }

        # SAVE HISTORY

        patient_history.append(result)

    return render_template(
        "index.html",
        result=result,
        history=patient_history
    )

# ---------------------------------
# RUN APP
# ---------------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=10000)