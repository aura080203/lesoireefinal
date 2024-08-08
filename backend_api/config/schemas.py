from pydantic import BaseModel, Field


# Schema for request body validation
class RSVPBase(BaseModel):
    first_name: str
    last_name: str
    email: str
    date_of_birth: str
    scanned_dob: str
    phone: int
    gender: str
    guests: int
    rsvp_date: str
    rsvp_time: str
    message: str
    payment: bool


class RSVPCreate(RSVPBase):
    date_of_birth: str = Field(default="2000-10-10")
    scanned_dob: str = Field(default="2000-10-10")
    rsvp_date: str = Field(default="2000-10-10")
    payment: bool = Field(default=False)
    # pass


class RSVPUpdate(BaseModel):
    first_name: str
    last_name: str
    email: str
    date_of_birth: str
    scanned_dob: str
    phone: int
    gender: str
    guests: int
    rsvp_date: str
    rsvp_time: str
    message: str
    payment: bool = Field(default=False)
