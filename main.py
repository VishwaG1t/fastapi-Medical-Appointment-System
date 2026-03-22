# Import required libraries

from fastapi import FastAPI, status
from pydantic import BaseModel, Field
from typing import Optional
import math

#Initialize FastAPI app
app = FastAPI()

# --------------------------
# DATA (In-memory storage)
# --------------------------

# Sample doctors data
# Note : Using List of dictionaries instead of database (as per project requirement)

doctors = [
    {"id": 1,
    "name": "Dr. Vishwajit",
    "specialization": "Cardiologist",
    "fee": 500,
    "experience_years":10,
    "is_available": True
    },
    
    {
    "id": 2,
    "name": "Dr. Mangesh",
    "specialization": "Dermatologist",
    "fee": 300,
    "experience_years":7,
    "is_available": True
    },
    {
    "id": 3,
    "name": "Dr. Pradyum",
    "specialization": "Pediatrician",
    "fee": 400,
    "experience_years":12,
    "is_available": False
    },
    {
    "id": 4,
    "name": "Dr. Vaibhav",
    "specialization": "General",
    "fee": 200,
    "experience_years":5,
    "is_available": True
    },
    {
    "id": 5,
    "name": "Dr. Sagar",
    "specialization": "Cardiologist",
    "fee": 600,
    "experience_years":15,
    "is_available": True
    },
    {
    "id": 6,
    "name": "Dr. Durgesh",
    "specialization": "Dermatologist",
    "fee": 350,
    "experience_years":8,
    "is_available": False
    }
]

# Appointments storage (dynamic)
appointments = []
appt_counter = 1

# --------------------------
# MODELS (Pydantic)
# --------------------------

# Request model for creating appointment
class AppointmentRequest(BaseModel):
    patient_name : str = Field(min_length=2)
    doctor_id : int = Field(gt=0)
    date : str = Field(min_length=8)
    reason : str = Field(min_length=5)
    appointment_type: str = "in-person"
    senior_citizen: bool = False

# Model for adding new doctor    
class NewDoctor(BaseModel):
    name: str = Field(min_length=2)
    specialization: str = Field(min_length=2)
    fee: int = Field(gt=0)
    experience_years: int = Field(gt=0)
    is_available: bool = True
    
           
# --------------------------
# HELPER FUNCTIONS
# --------------------------

# Find doctor by ID
def find_doctor(doctor_id):
    for doctor in doctors:
        if doctor["id"] == doctor_id:
            return doctor
    return None

# Calculate consultation fee based on type and senior citizen discount
def calculate_fee(base_fee, appointment_type, senior):
    fee = base_fee

    if appointment_type == "video":
        fee *= 0.8
    elif appointment_type == "emergency":
        fee *= 1.5
    
    # Apply additional 15% discount for senior citizens
    if senior:
        fee *= 0.85  # 15% discount

    return round(fee)

# Home route   
@app.get("/")
def home():
    return {"message": "Welcome to MediFriend clinic"}

# Get all doctors
@app.get("/doctors")
def get_doctors():
    return {
        "total_doctors" : len(doctors),
        "available_doctors" :len([d for d in doctors if d["is_available"]]),
        "data" : doctors
    }


# Summary doctor
@app.get("/doctors/summary")
def get_summary():
    return {
        "total_doctors" : len(doctors),
        "available_doctors" : len([d for d in doctors if d["is_available"]]),
        "most_experienced_doctor" : max(doctors, key = lambda x:x["experience_years"])["name"],
        "cheapest_fee" :min(doctors, key = lambda x:x["fee"])["fee"]
    }   




# --------------------------
# FILTER, SEARCH, SORT, PAGINATION (Day 3 & Day 6)
# --------------------------

# Filter doctors using query parameters
@app.get("/doctors/filter")
def filter_doctors(
    specialization: Optional[str] = None,
    max_fee: Optional[int] = None,
    min_experience: Optional[int] = None,
    is_available: Optional[bool] = None
):
    result = doctors

    if specialization is not None:
        result = [d for d in result if d["specialization"].lower() == specialization.lower()]

    if max_fee is not None:
        result = [d for d in result if d["fee"] <= max_fee]

    if min_experience is not None:
        result = [d for d in result if d["experience_years"] >= min_experience]

    if is_available is not None:
        result = [d for d in result if d["is_available"] == is_available]

    return {
        "count": len(result),
        "data": result
    }


# Search doctors
@app.get("/doctors/search")
def search_doctors(keyword: str):
    keyword = keyword.lower()

    result = [
        d for d in doctors
        if keyword in d["name"].lower() or keyword in d["specialization"].lower()
    ]

    if not result:
        return {"message": "No doctors found"}

    return {
        "total_found": len(result),
        "data": result
    }

# Sort doctors
@app.get("/doctors/sort")
def sort_doctors(
    sort_by: str = "fee",
    order: str = "asc"
):
    valid_fields = ["fee", "name", "experience_years"]

    if sort_by not in valid_fields:
        return {"error": "Invalid sort field"}

    reverse = True if order == "desc" else False

    sorted_data = sorted(doctors, key=lambda x: x[sort_by], reverse=reverse)

    return {
        "sort_by": sort_by,
        "order": order,
        "data": sorted_data
    }


# Pagination  
@app.get("/doctors/page")
def paginate_doctors(
    page: int = 1,
    limit: int = 3
):
    total = len(doctors)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    data = doctors[start:end]

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "data": data
    }

# Combined API : Search + Sort + Pagination
@app.get("/doctors/browse")
def browse_doctors(
    keyword: Optional[str] = None,
    sort_by: str = "fee",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = doctors

    # 🔍 Search (Filter)
    if keyword is not None:
        keyword = keyword.lower()
        result = [
            d for d in result
            if keyword in d["name"].lower() or keyword in d["specialization"].lower()
        ]

    # 🔽 Sort
    valid_fields = ["fee", "name", "experience_years"]

    if sort_by not in valid_fields:
        return {"error": "Invalid sort field"}

    reverse = True if order == "desc" else False
    result = sorted(result, key=lambda x: x[sort_by], reverse=reverse)

    # 📄 Pagination
    total = len(result)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    paginated = result[start:end]

    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "limit": limit,
        "data": paginated
    }


# Get doctor by ID   
@app.get("/doctors/{doctor_id}")
def get_doctor_by_id(doctor_id: int):
    for doctor in doctors:
        if doctor["id"] == doctor_id:
            return doctor
        
    return {"error": "Doctor not found"}



# --------------------------
# APPOINTMENTS (CRUD + Workflow)
# --------------------------


# Get all appointments
@app.get("/appointments")
def get_appointments():
    return {
        "total_appointments" : len(appointments),
        "data" : appointments
    }

# Temporary endpoint to test pydantic validation
# Helps verify request body constraints like min_length, gt, etc,..    
@app.post("/test-appointment")
def test_appointment(data: AppointmentRequest):
    return data

# Temperory endpoint to test helper function
# Used to verify find_doctor() and calculate_fee() logic independently
@app.get("/test-helper/{doctor_id}")
def test_helper(doctor_id: int):
    doctor = find_doctor(doctor_id)

    if not doctor:
        return {"error": "Doctor not found"}
    
    # Example: calculating video consulting fee
    fee = calculate_fee(doctor["fee"], "video", 'senior')

    return {
        "doctor": doctor["name"],
        "calculated_fee": fee
    }
    
 
# Create a new appointment
# Includes validation, availability check, fee calculation, and status assignment   
@app.post("/appointments")
def create_appointment(req: AppointmentRequest):
    global appt_counter

    # Check if doctor exists
    doctor = find_doctor(req.doctor_id)
    if not doctor:
        return {"error": "Doctor not found"}

    # Ensure doctor is available before booking
    if not doctor["is_available"]:
        return {"error": "Doctor not available"}

    # Calculate final consultation fee
    fee = calculate_fee(doctor["fee"], req.appointment_type, req.senior_citizen)

    # Create appointment record
    appointment = {
        "appointment_id": appt_counter,
        "patient": req.patient_name,
        "doctor": doctor["name"],
        "doctor_id": doctor["id"],
        "date": req.date,
        "reason": req.reason,
        "type": req.appointment_type,
        "original_fee": doctor["fee"],
        "final_fee" : fee,
        "senior_citizen" : req.senior_citizen,
        "status": "scheduled"
    }

    # Save appointment and update doctor availability
    appointments.append(appointment)
    doctor["is_available"] = False
    appt_counter += 1

    return appointment

# --------------------------
# DOCTOR CRUD OPERATIONS (Day 4)
# --------------------------

# Add a new doctor
# Includes duplicate name check
@app.post("/doctors", status_code = status.HTTP_201_CREATED)
def add_doctor(doc: NewDoctor):
    
    # Duplicate check
    for d in doctors:
        if d["name"].lower() == doc.name.lower():
            return {"error" : "Doctor already exists"}  

    # Create new doctor object
    new_doctor = {
        "id": len(doctors) + 1,
        "name": doc.name,
        "specialization": doc.specialization,
        "fee": doc.fee,
        "experience_years": doc.experience_years,
        "is_available": doc.is_available
    }
    
    doctors.append(new_doctor)
    return new_doctor

# Update doctor details
# Only updates fields if provided 
@app.put("/doctors/{doctor_id}")
def update_doctor(
    doctor_id: int,
    fee: Optional[int] = None,
    is_available: Optional[bool] = None
):
    doctor = find_doctor(doctor_id)

    if not doctor:
        return {"error": "Doctor not found"}

    # Apply updates only if values are provided
    if fee is not None:
        doctor["fee"] = fee

    if is_available is not None:
        doctor["is_available"] = is_available

    return doctor

# Delete doctor
# Restriction: cannot delete if doctor have active appointments
@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)

    if not doctor:
        return {"error": "Doctor not found"}

    # Check active appointments
    for appt in appointments:
        if appt["doctor_id"] == doctor_id and appt["status"] == "scheduled":
            return {"error": "Doctor has active appointments"}

    doctors.remove(doctor)

    return {"message": "Doctor deleted successfully"}

# --------------------------
# APPOINTMENT SEARCH, SORT, PAGINATION (Day 6)
# --------------------------

# Search appointments by patient name
@app.get("/appointments/search")
def search_appointments(keyword: str):
    keyword = keyword.lower()

    result = [
        a for a in appointments
        if keyword in a["patient"].lower()
    ]

    if not result:
        return {"message": "No appointments found"}

    return {
        "count": len(result),
        "data": result
    }
 
# Sort appointments based on date or final_fee   
@app.get("/appointments/sort")
def sort_appointments(sort_by: str = "date"):
    valid_fields = ["date", "final_fee"]

    if sort_by not in valid_fields:
        return {"error": "Invalid sort field"}

    sorted_data = sorted(appointments, key=lambda x: x[sort_by])

    return {
        "sort_by": sort_by,
        "data": sorted_data
    }

# Paginate appointments list
@app.get("/appointments/page")
def paginate_appointments(page: int = 1, limit: int = 2):
    total = len(appointments)
    total_pages = math.ceil(total / limit)

    start = (page - 1) * limit
    end = start + limit

    data = appointments[start:end]

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "total_pages": total_pages,
        "data": data
    }   

# --------------------------
# APPOINTMENT WORKFLOW (Day 5)
# --------------------------


# Confirm appointment
# Changes status from scheduled -> confirmed
@app.post("/appointments/{appointment_id}/confirm")
def confirm_appointment(appointment_id: int):
    for appt in appointments:
        if appt["appointment_id"] == appointment_id:
            appt["status"] = "confirmed"
            return {"message": "Appointment confirmed", "data": appt}

    return {"error": "Appointment not found"}


# Cancel appointment
# Updates status and frees doctor availability
@app.post("/appointments/{appointment_id}/cancel")
def cancel_appointment(appointment_id: int):
    for appt in appointments:
        if appt["appointment_id"] == appointment_id:
            appt["status"] = "cancelled"

            doctor = find_doctor(appt["doctor_id"])
            if doctor:
                doctor["is_available"] = True

            return {"message": "Appointment cancelled", "data": appt}

    return {"error": "Appointment not found"}


# Complete appointment
# Marks appointment as completed 
@app.post("/appointments/{appointment_id}/complete")
def complete_appointment(appointment_id: int):
    for appt in appointments:
        if appt["appointment_id"] == appointment_id:
            appt["status"] = "completed"
            return {"message": "Appointment completed", "data": appt}

    return {"error": "Appointment not found"}

# Get active appointments
# Includes only scheduled and confirmed (not cancelled/completed)
@app.get("/appointments/active")
def get_active_appointments():
    active = [
        appt for appt in appointments 
        if appt["status"] in ["scheduled", "confirmed"]
    ]

    return {
        "count": len(active),
        "data": active
    }
    
# Get appointments for a specifice
@app.get("/appointments/by-doctor/{doctor_id}")
def get_appointments_by_doctor(doctor_id: int):
    result = [
        appt for appt in appointments
        if appt["doctor_id"] == doctor_id
    ]

    return {
        "count": len(result),
        "data": result
    }


    
