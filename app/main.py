from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import delete, and_
from datetime import date, datetime, timedelta
from typing import List
import json

from . import models, auth, database, schemas

app = FastAPI(title="Appointment Booking System")

# --- WebSocket Manager ---
class ConnectionManager:
    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            await connection.send_text(json.dumps(message))

manager = ConnectionManager()

# --- Startup: Create Tables ---
@app.on_event("startup")
async def startup():
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

# --- USER MANAGEMENT ---

@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    new_user = models.User(email=user.email, role=user.role)
    db.add(new_user)
    try:
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except Exception:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email already registered")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(database.get_db), api_key: str = Depends(auth.get_api_key)):
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"detail": f"User {user_id} deleted"}

# --- APPOINTMENT MANAGEMENT ---

@app.post("/appointments/", response_model=schemas.AppointmentResponse)
async def create_appointment(
    appt: schemas.AppointmentCreate, 
    db: AsyncSession = Depends(database.get_db),
    api_key: str = Depends(auth.get_api_key)
):
    new_appt = models.Appointment(title=appt.title, slot_time=appt.slot_time, user_id=appt.user_id)
    db.add(new_appt)
    await db.commit()
    await db.refresh(new_appt)
    
    await manager.broadcast({"event": "BOOKED", "id": new_appt.id, "title": appt.title})
    return new_appt

@app.get("/appointments/{appt_id}", response_model=schemas.AppointmentResponse)
async def get_appointment_by_id(appt_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Appointment).filter(models.Appointment.id == appt_id))
    appt = result.scalars().first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appt

@app.get("/appointments/filter/date", response_model=List[schemas.AppointmentResponse])
async def get_appointments_by_date(target_date: date, db: AsyncSession = Depends(database.get_db)):
    # Calculate start and end of the chosen day
    start_time = datetime.combine(target_date, datetime.min.time())
    end_time = datetime.combine(target_date, datetime.max.time())
    
    result = await db.execute(
        select(models.Appointment).filter(
            and_(models.Appointment.slot_time >= start_time, models.Appointment.slot_time <= end_time)
        )
    )
    return result.scalars().all()

@app.patch("/appointments/{appt_id}/cancel")
async def cancel_appointment(
    appt_id: int, 
    db: AsyncSession = Depends(database.get_db),
    api_key: str = Depends(auth.get_api_key)
):
    result = await db.execute(select(models.Appointment).filter(models.Appointment.id == appt_id))
    appt = result.scalars().first()
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    
    appt.status = "cancelled"
    await db.commit()
    
    await manager.broadcast({"event": "CANCELLED", "id": appt_id})
    return {"status": "Appointment cancelled"}

# --- WebSockets ---
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)