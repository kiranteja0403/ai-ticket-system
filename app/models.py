from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    issue = Column(Text, nullable=False)
    category = Column(String(100), nullable=True)
    troubleshooting = Column(Text, nullable=True)
    status = Column(String(50), default="Open")
    created_at = Column(DateTime, default=datetime.utcnow)
