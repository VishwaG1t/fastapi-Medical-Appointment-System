# 🏥  MediCal Appointment System API

A **FastAPI backend application** designed for managing doctors and appointments in a clinic. This project demonstrates practical backend concepts such as CRUD operations, filtering, searching, sorting, pagination, and appointment workflow management.

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# 🚀 Features

## 👨‍⚕️ Doctor Management

- Add, update, and delete doctors
  
- Retrieve all doctors

- Filter doctors by:
  - Specialization
  - Fee
  - Experience
  - Availability
  
- Search doctors by name or specialization
  
- Sort doctors by fee, name, or experience
  
- Pagination support for doctor listings
  
## 📅 Appointment Management
- Create appointments with automated fee calculations:

- Video appointments → 20% discount

- Emergency appointments → 50% extra charge

- Senior citizens → 15% discount

- Appointment lifecycle management:

  - Scheduled → Confirmed → Completed / Cancelled
  
  - Cancelling an appointment frees up the doctor’s availability
  
## 🔍 Advanced APIs

- Search and sort appointments by date or fee

- Pagination for appointment listings

- Filter only active appointments

- Retrieve appointments for a specific doctor

## 🛠 Tech Stack

- FastAPI – Web framework

- Python – Core language

- Pydantic – Data validation and serialization

- Uvicorn – ASGI server

## 📦 Installation

## 1. Clone the repository

```bash
git clone https://github.com/Vi1t/fastapi-Medical-Appointment-System.git
cd fastapi-project
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

## 3. Activate the virtual environment
**Windows:**
```bash
venv\Scripts\activate
```
**Mac/Linux:**
```bash
source venv/bin/activate
```
## 4. Install dependencies
```bash
pip install -r requirements.txt
```
## Run the server
```bash
uvicorn main:app --reload
```
The server will run at:👉 http://127.0.0.1:8000

## 📘 API Documentation

FastAPI provides interactive API documentation:

  - Swagger UI: http://127.0.0.1:8000/docs
  - ReDoc: http://127.0.0.1:8000/redoc
    
## 📂 Project Structure
```bash
project/
│── main.py
│── requirements.txt
│── README.md
│── Screenshots
```
## 🧠 Key Concepts Covered
- REST API Design
  
- CRUD Operations

- Query Parameters and Filters

- Data Validation with Pydantic

- Business Logic Implementation

- Pagination, Filtering, Sorting

- Workflow & State Management
  
## 🚊 Example Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET    | /doctors | Retrieve all doctors |
| POST   | /doctors | Add a new doctor |
| GET    | /doctors/filter | Filter doctors |
| GET    | /appointments | Retrieve appointments |
| POST   | /appointments | Create an appointment |
| POST   | /appointments/{id}/confirm | Confirm an appointment |


## 😎 Author
### Vishwajit Suryawanshi
