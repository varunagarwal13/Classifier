from sqlalchemy import create_engine, Column, String, Float, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Local = SQLite, Production = PostgreSQL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./threat_log.db")

# Render.com provides postgres:// but SQLAlchemy needs postgresql://
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ThreatLog(Base):
    __tablename__ = "threat_log"

    id          = Column(Integer, primary_key=True, index=True)
    url         = Column(String(2048), nullable=False)
    score       = Column(Float, nullable=False)
    verdict     = Column(String(10), nullable=False)
    signals     = Column(Text, nullable=True)
    rf_score    = Column(Float, nullable=True)
    xgb_score   = Column(Float, nullable=True)
    vt_malicious= Column(Integer, nullable=True)
    vt_total    = Column(Integer, nullable=True)
    cached      = Column(Integer, default=0)
    timestamp   = Column(DateTime, default=datetime.utcnow)
    user_feedback = Column(String(20), nullable=True)  # "correct", "false_positive", "false_negative"

class FeedbackLog(Base):
    __tablename__ = "feedback_log"

    id        = Column(Integer, primary_key=True, index=True)
    url       = Column(String(2048), nullable=False)
    verdict   = Column(String(10), nullable=False)
    feedback  = Column(String(20), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    print(f"Database initialized: {DATABASE_URL}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()