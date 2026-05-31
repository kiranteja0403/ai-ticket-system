from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app import models
from app.schemas import TicketCreate

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "AI Ticket System is running"}

@app.post("/tickets")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):
    new_ticket = models.Ticket(
        name=ticket.name,
        email=ticket.email,
        issue=ticket.issue
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "message": "Ticket created successfully",
        "ticket_id": new_ticket.id,
        "name": new_ticket.name,
        "email": new_ticket.email,
        "issue": new_ticket.issue,
        "status": new_ticket.status
    }
