from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app import models
from app.schemas import TicketCreate, TicketStatusUpdate
from app.services.dify_service import analyze_issue
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

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
    ai_result = analyze_issue(ticket.issue)

    new_ticket = models.Ticket(
        name=ticket.name,
        email=ticket.email,
        issue=ticket.issue,
        category=ai_result["category"],
        troubleshooting=ai_result["troubleshooting"]
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
        "category": new_ticket.category,
        "troubleshooting": new_ticket.troubleshooting,
        "status": new_ticket.status
    }

@app.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    tickets = db.query(models.Ticket).all()
    return tickets

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    return ticket

@app.put("/tickets/{ticket_id}/status")
def update_ticket_status(ticket_id: int, ticket_update: TicketStatusUpdate, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = ticket_update.status
    db.commit()
    db.refresh(ticket)

    return {
        "message": "Ticket status updated successfully",
        "ticket_id": ticket.id,
        "new_status": ticket.status
    }

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()

    return {"message": "Ticket deleted successfully"}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    tickets = db.query(models.Ticket).all()
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={"tickets": tickets}
    )
@app.post("/tickets/{ticket_id}/status-form")
def update_ticket_status_form(ticket_id: int, status: str = Form(...), db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    ticket.status = status
    db.commit()

    return RedirectResponse(url="/dashboard", status_code=303)
@app.post("/tickets/create-form")
def create_ticket_form(
    name: str = Form(...),
    email: str = Form(...),
    issue: str = Form(...),
    db: Session = Depends(get_db)
):
    ai_result = analyze_issue(issue)

    new_ticket = models.Ticket(
        name=name,
        email=email,
        issue=issue,
        category=ai_result["category"],
        troubleshooting=ai_result["troubleshooting"]
    )
    db.add(new_ticket)
    db.commit()

    return RedirectResponse(url="/dashboard", status_code=303)
@app.post("/tickets/{ticket_id}/delete-form")
def delete_ticket_form(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()

    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    db.delete(ticket)
    db.commit()

    return RedirectResponse(url="/dashboard", status_code=303)


