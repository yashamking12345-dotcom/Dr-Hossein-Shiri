from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta

app = FastAPI(title="Dr.Shiri Clinic System")

templates = Jinja2Templates(directory="templates")

appointments = []

# -------------------------
# UI PAGE (REAL WEBSITE)
# -------------------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "doctor_name": "Dr.Shiri"
    })

# -------------------------
# API: CREATE APPOINTMENT
# -------------------------
@app.post("/appointment")
def create_appointment(data: dict):

    data["status"] = "scheduled"
    data["created_at"] = datetime.now().isoformat()

    appointments.append(data)

    return {
        "message": "appointment created",
        "data": data
    }

# -------------------------
# API: GET APPOINTMENTS
# -------------------------
@app.get("/appointments")
def get_appointments():
    return appointments

# -------------------------
# 15 MIN RULE CHECK
# -------------------------
@app.post("/check")
def check(data: dict):

    t = datetime.fromisoformat(data["time"])
    now = datetime.now()

    if now > t + timedelta(minutes=15):
        return {"status": "cancelled"}

    return {"status": "valid"}
