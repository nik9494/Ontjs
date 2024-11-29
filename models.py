from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, func
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    name = Column(String)
    role = Column(String)  # admin, female, male, team_lead
    balance = Column(Float, default=0)
    gift_balance = Column(Float, default=0)
    last_gift_request = Column(DateTime)
    created_at = Column(DateTime, default=func.now())

class Female(Base):
    __tablename__ = "females"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(String, unique=True, index=True)
    name = Column(String)
    unique_code = Column(String, unique=True)
    earnings_today = Column(Float, default=0)
    total_earnings = Column(Float, default=0)
    created_at = Column(DateTime, default=func.now())

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    female_id = Column(Integer, ForeignKey("females.id"))
    messages_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())

class Action(Base):
    __tablename__ = "actions"
    id = Column(Integer, primary_key=True, index=True)
    female_id = Column(Integer, ForeignKey("females.id"))
    action_type = Column(String)
    created_at = Column(DateTime, default=func.now())
