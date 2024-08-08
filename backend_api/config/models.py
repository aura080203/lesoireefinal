from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Declare Base class for models
Base = declarative_base()


# Define RSVP model
class RSVP(Base):
    __tablename__ = "rsvp"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    date_of_birth = Column(Date)
    phone = Column(Integer)
    age = Column(Integer)
    gender = Column(String(255))
    guests = Column(Integer)
    rsvp_date = Column(String(255))
    rsvp_time = Column(Date)
    message = Column(String(255))
    payment = Column(Boolean, default=False)
