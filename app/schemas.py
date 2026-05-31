from pydantic import BaseModel, EmailStr

class TicketCreate(BaseModel):
    name: str
    email: EmailStr
    issue: str
