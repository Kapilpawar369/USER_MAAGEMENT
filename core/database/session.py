from sqlalchemy.ext.declarative import declarative_base
from core.connections.database import SessionLocal, engine

Base = declarative_base()

# Dependency for FastAPI endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()