from fastapi import FastAPI, HTTPException, Request

from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create SQLAlchemy engine
SQLALCHEMY_DATABASE_URL = "mysql://root:1234@localhost/lesoiree"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declare Base class for SQLAlchemy models
Base = declarative_base()


# Define SQLAlchemy model
class RSVP(Base):
    __tablename__ = "rsvp"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    gender = Column(String(255))
    phone = Column(Integer)
    guests = Column(Integer)
    card = Column(String(255))
    message = Column(String(255))


# Create FastAPI app instance
app = FastAPI()


# Pydantic model for request body validation
class RSVPCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    gender: str
    phone: int
    guests: int
    card: str
    message: str


# Routes for CRUD operations
@app.get("/rsvp/")
def read_all_rsvp():
    db = SessionLocal()
    rsvp_list = db.query(RSVP).all()
    db.close()
    return rsvp_list


@app.get("/rsvp/{rsvp_id}")
def read_rsvp(rsvp_id: int):
    db = SessionLocal()
    rsvp = db.query(RSVP).filter(RSVP.id == rsvp_id).first()
    db.close()
    if rsvp is None:
        raise HTTPException(status_code=404, detail="RSVP not found")
    return rsvp


@app.post("/rsvp/")
# def create_rsvp(rsvp_data: RSVPCreate):
def create_rsvp(rsvp_data: RSVPCreate, request: Request):
    # print(request.body())
    db = SessionLocal()
    db_rsvp = RSVP(**rsvp_data.dict())
    db.add(db_rsvp)
    db.commit()
    db.refresh(db_rsvp)
    db.close()
    return {"message": "RSVP created successfully"}


@app.put("/rsvp/{rsvp_id}")
def update_rsvp(rsvp_id: int, rsvp_data: RSVPCreate):
    db = SessionLocal()
    db_rsvp = db.query(RSVP).filter(RSVP.id == rsvp_id).first()
    if db_rsvp is None:
        db.close()
        raise HTTPException(status_code=404, detail="RSVP not found")
    for key, value in rsvp_data.dict().items():
        setattr(db_rsvp, key, value)
    db.commit()
    db.refresh(db_rsvp)
    db.close()
    return {"message": "RSVP updated successfully"}


@app.delete("/rsvp/{rsvp_id}")
def delete_rsvp(rsvp_id: int):
    db = SessionLocal()
    db_rsvp = db.query(RSVP).filter(RSVP.id == rsvp_id).first()
    if db_rsvp is None:
        db.close()
        raise HTTPException(status_code=404, detail="RSVP not found")
    db.delete(db_rsvp)
    db.commit()
    db.close()
    return {"message": "RSVP deleted successfully"}
