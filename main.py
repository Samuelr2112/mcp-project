from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session, Mapped, mapped_column
from datetime import datetime
from dateutil import parser
import os

# -----------------------------
# Database Configuration
# -----------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://samuel:mypassword@db:5432/appointments_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# -----------------------------
# Database Model
# -----------------------------
class AppointmentDB(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    customer_name: Mapped[str] = mapped_column(String, nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)

Base.metadata.create_all(bind=engine)

# -----------------------------
# FastAPI App
# -----------------------------
app = FastAPI(
    title="Business Assistant API",
    version="1.0.0",
    description="API to manage appointments with FastAPI and PostgreSQL",
)

# -----------------------------
# Schemas
# -----------------------------
class CreateAppointment(BaseModel):
    customer_name: str
    date: str

class UpdateAppointment(BaseModel):
    appointment_id: int
    customer_name: str | None = None
    date: str | None = None

class DeleteAppointment(BaseModel):
    appointment_id: int

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# Utility function: safe date formatting
# -----------------------------
def safe_format_date(value):
    """Ensure consistent date formatting for datetime or string values."""
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    try:
        parsed = parser.parse(str(value))
        return parsed.strftime("%Y-%m-%d %H:%M:%S")
    except Exception:
        return str(value)

# -----------------------------
# Routes
# -----------------------------
@app.post("/create_appointment")
def create_appointment(appointment: CreateAppointment, db: Session = Depends(get_db)):
    try:
        parsed_date = parser.parse(str(appointment.date))
    except Exception:
        return {"status": "error", "message": "Invalid date. Use ISO 8601 like '2025-09-26T10:55:00'"}

    db_appointment = AppointmentDB(
        customer_name=appointment.customer_name,
        date=parsed_date
    )

    try:
        db.add(db_appointment)
        db.commit()
        return {
            "status": "success",
            "message": f"Appointment created for {appointment.customer_name} on {safe_format_date(parsed_date)}",
            "id": db_appointment.id
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"Database error: {str(e)}"}

@app.put("/update_appointment")
def update_appointment(appointment: UpdateAppointment, db: Session = Depends(get_db)):
    appt = db.query(AppointmentDB).filter(AppointmentDB.id == appointment.appointment_id).first()
    if not appt:
        return {"status": "error", "message": f"No appointment found with id {appointment.appointment_id}"}

    if appointment.customer_name:
        appt.customer_name = appointment.customer_name
    if appointment.date:
        try:
            parsed_date = parser.parse(str(appointment.date))
            appt.date = parsed_date
        except Exception:
            return {"status": "error", "message": "Invalid date format. Use ISO 8601."}

    try:
        db.commit()
        return {
            "status": "success",
            "message": f"Appointment {appointment.appointment_id} updated successfully",
            "appointment": {
                "id": appt.id,
                "customer_name": appt.customer_name,
                "date": safe_format_date(appt.date)
            }
        }
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"Database error: {str(e)}"}

@app.get("/list_appointments")
def list_appointments(db: Session = Depends(get_db)):
    appointments = db.query(AppointmentDB).all()
    results = []
    for a in appointments:
        results.append({
            "id": a.id,
            "customer_name": a.customer_name,
            "date": safe_format_date(a.date)
        })
    return results

@app.delete("/delete_appointment")
def delete_appointment(payload: DeleteAppointment, db: Session = Depends(get_db)):
    appointment_id = payload.appointment_id
    appt = db.query(AppointmentDB).filter(AppointmentDB.id == appointment_id).first()
    if not appt:
        return {"status": "error", "message": f"No appointment found with id {appointment_id}"}

    try:
        db.delete(appt)
        db.commit()
        return {"status": "success", "message": f"Appointment with id {appointment_id} has been deleted"}
    except Exception as e:
        db.rollback()
        return {"status": "error", "message": f"Database error: {str(e)}"}
