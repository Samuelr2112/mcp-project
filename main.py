from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from datetime import datetime
import os

# -----------------------------
# Database Configuration
# -----------------------------
# DATABASE_URL will come from environment variables (set in docker-compose.yml)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://samuel:mypassword@db:5432/appointments_db"
)

# Create the database engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -----------------------------
# Database Model (Appointment table)
# -----------------------------
class AppointmentDB(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    date = Column(String, nullable=False)

# Create the table in the database (if it doesn't exist)
Base.metadata.create_all(bind=engine)

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(
    title="MCP Server with Postgres",
    version="1.0.0",
    description="Simple API to create and list appointments using FastAPI + PostgreSQL",
    servers=[
        {"url": "http://localhost:8000", "description": "Local development server"}
    ]
)

# -----------------------------
# Pydantic Schemas
# -----------------------------
class Appointment(BaseModel):
    customer_name: str
    date: str  # Puede venir en ISO o ya formateada

class AppointmentUpdate(BaseModel):
    customer_name: str | None = None
    date: str | None = None

# Dependency: Get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Routes (Endpoints)
# -----------------------------

# Root endpoint (health check)
@app.get("/")
def root():
    return {"message": "MCP server with Postgres is running 🚀"}

# Create a new appointment
@app.post("/create_appointment")
def create_appointment(appointment: Appointment, db: Session = Depends(get_db)):
    # Parse ISO date (ej: 2025-09-25T14:30:00) y convertir a formato humano
    try:
        parsed_date = datetime.fromisoformat(appointment.date)
        formatted_date = parsed_date.strftime("%-d/%-m/%Y - %-I:%M%p").lower()
    except Exception:
        # Si ya viene formateada, guardamos directo
        formatted_date = appointment.date

    db_appointment = AppointmentDB(
        customer_name=appointment.customer_name,
        date=formatted_date
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return {
        "status": "success",
        "message": f"Appointment created for {appointment.customer_name} on {formatted_date}",
        "id": db_appointment.id
    }

# List all appointments
@app.get("/list_appointments")
def list_appointments(db: Session = Depends(get_db)):
    appointments = db.query(AppointmentDB).all()
    return appointments

# Delete an appointment by ID
@app.delete("/delete_appointment/{appointment_id}")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(AppointmentDB).filter(AppointmentDB.id == appointment_id).first()
    if not appointment:
        return {
            "status": "error",
            "message": f"No appointment found with id {appointment_id}"
        }

    db.delete(appointment)
    db.commit()
    return {
        "status": "success",
        "message": f"Appointment with id {appointment_id} has been deleted"
    }

# Update an appointment by ID
@app.put("/update_appointment/{appointment_id}")
def update_appointment(appointment_id: int, appointment_update: AppointmentUpdate, db: Session = Depends(get_db)):
    appointment = db.query(AppointmentDB).filter(AppointmentDB.id == appointment_id).first()
    if not appointment:
        return {
            "status": "error",
            "message": f"No appointment found with id {appointment_id}"
        }

    update_data = {}
    if appointment_update.customer_name is not None:
        update_data["customer_name"] = appointment_update.customer_name

    if appointment_update.date is not None:
        try:
            parsed_date = datetime.fromisoformat(appointment_update.date)
            update_data["date"] = parsed_date.strftime("%-d/%-m/%Y - %-I:%M%p").lower()
        except Exception:
            update_data["date"] = appointment_update.date

    if update_data:
        db.query(AppointmentDB).filter(AppointmentDB.id == appointment_id).update(update_data)
        db.commit()
        db.refresh(appointment)

    return {
        "status": "success",
        "message": f"Appointment {appointment_id} updated successfully",
        "appointment": {
            "id": appointment.id,
            "customer_name": appointment.customer_name,
            "date": appointment.date
        }
    }
