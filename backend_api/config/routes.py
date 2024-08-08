from fastapi import APIRouter, HTTPException, Request, File, UploadFile
from sqlalchemy.orm import Session
from .models import RSVP
from .schemas import RSVPCreate, RSVPUpdate
from .database import SessionLocal
from gcp_document_ai.doc_ai import process_document_sample
from shutil import copyfileobj
from .utilities import save_file, format_date, calculate_age
import os
from fastapi.responses import JSONResponse
import mysql.connector

# Initializing routes for CRUD operations
router_function = APIRouter()


# Get all RSVPs
@router_function.get("/rsvp/")
def read_all_rsvp():
    db = SessionLocal()
    rsvp_list = db.query(RSVP).all()
    db.close()
    return rsvp_list


# Get a single RSVP by ID
@router_function.get("/rsvp/{rsvp_id}")
def read_rsvp(rsvp_id: int):
    db = SessionLocal()
    rsvp = db.query(RSVP).filter(RSVP.id == rsvp_id).first()
    db.close()
    if rsvp is None:
        raise HTTPException(status_code=404, detail="RSVP not found")
    return rsvp


# Create a new RSVP
@router_function.post("/rsvp/create/")
def create_rsvp(rsvp_data: RSVPCreate, request: Request):
    #  Get date of birth
    dob = rsvp_data.date_of_birth
    #  Get date of birth from passport scan
    scanned_dob = rsvp_data.scanned_dob
    # Check inputted and scanned DoB is same
    if dob != scanned_dob:
        raise HTTPException(
            status_code=404,
            detail="RSVP creation failed. User inputted data and passport scanned data doen't match.",
        )
    #  Calculate age
    age = calculate_age(scanned_dob)
    #  Age logic:
    #  Age not legal -> return error statement
    if age <= 18:
        raise HTTPException(
            status_code=404,
            detail=f"RSVP creation failed. User is {age}, under 18 years old.",
        )

    #  Age legal -> Continue
    # Convert json values to a dictionary
    rsvp_data_dict = rsvp_data.dict()
    # Get rid of "scanned_dob" input before send it DB
    rsvp_data_dict.pop("scanned_dob", None)
    # Add age to dict
    rsvp_data_dict["age"] = age
    db = SessionLocal()
    db_rsvp = RSVP(**rsvp_data_dict)
    db.add(db_rsvp)
    db.commit()
    db.refresh(db_rsvp)

    # Trying to retrieve the generated User ID from DB
    db_rsvp_id = (
        db.query(RSVP.id)
        .filter(
            RSVP.email == rsvp_data_dict["email"],
            RSVP.date_of_birth == rsvp_data_dict["date_of_birth"],
            RSVP.phone == rsvp_data_dict["phone"],
        )
        .first()
    )
    # Check if db_rsvp_id is not None before accessing its value
    if db_rsvp_id:
        # Extract the ID from the tuple
        db_rsvp_id = db_rsvp_id[0]
    db.close()
    return {
        "code": 200,
        "message": "RSVP created successfully",
        "user": rsvp_data_dict,
        "user_id": db_rsvp_id,
    }


# Update a RSVP by ID
@router_function.put("/rsvp/update/{rsvp_id}")
def update_rsvp(rsvp_id: int, rsvp_data: RSVPUpdate):
    db = SessionLocal()
    # get rsvp by id
    db_rsvp = db.query(RSVP).filter(RSVP.id == rsvp_id).first()
    if db_rsvp is None:
        db.close()
        raise HTTPException(status_code=404, detail="RSVP not found")
    # update database
    for key, value in rsvp_data.dict().items():
        setattr(db_rsvp, key, value)
    db.commit()
    db.refresh(db_rsvp)
    db_rsvp_new = db.query(RSVP).filter(RSVP.id == rsvp_id).first()
    db.close()
    return {
        "code": 200,
        "message": "RSVP updated successfully",
        "updated_user_data": db_rsvp_new,
    }


# Delete a RSVP by ID
@router_function.delete("/rsvp/{rsvp_id}")
def delete_rsvp(rsvp_id: int):
    db = SessionLocal()
    db_rsvp = db.query(RSVP).filter(RSVP.id == rsvp_id).first()
    if db_rsvp is None:
        db.close()
        # return {
        #     "code": 404,
        #     "message": "RSVP not found",
        # }
        raise HTTPException(status_code=404, detail="RSVP not found")
    db.delete(db_rsvp)
    db.commit()
    db.close()
    return {
        "code": 200,
        "message": "RSVP deleted successfully",
        "deleted_user": db_rsvp,
    }


# Upload profile picture
@router_function.post("/rsvp/upload_pro_pic/")
def upload_profile_pic(file: UploadFile = File(...)):
    print("file:", "file uploaded")
    print("file Type:", type(file))

    # Save the uploaded file and get file path
    file_path = save_file(file, "user")
    print("file path:", file_path)
    # print("filetype:", type(file))
    try:
        return {
            "code": 200,
            "message": "Profile picture uploaded successfully",
            "filename": file_path,
        }
    except:
        os.remove(file_path)
        raise HTTPException(
            status_code=404,
            detail="Failed to upload profile picture.",
        )


# Scan Passport to extract DoB and get age
@router_function.post("/rsvp/scan_passport/")
def upload_passport(file: UploadFile = File(...)):
    print("file:", "file uploaded")
    print("file Type:", type(file))
    # Save the uploaded file and get file path
    file_path = save_file(file, "passport")
    print("file path:", file_path)
    # print("filetype:", type(file))
    try:
        # Extract date of birth from image
        file_output = process_document_sample(
            project_id="900576536122",
            location="us",
            processor_id="2a231379c45dffc5",
            file_path=file_path,
            field_mask="entities",
            mime_type="image/jpeg",
        )
        print("extract:", file_output)

        # Format the extracted data
        dob_formatted = format_date(file_output)
        # os.remove(file_path)  # debuginng
        # Calculate age using the extracted DoB
        # age = calculate_age(dob_formatted)
        # delete_images("./users/images")
        return {
            "code": 200,
            "message": "Date of Birth extracted successfully",
            "filename": file_path,
            "date of birth": dob_formatted,
            # "age": age,
        }
    except:
        os.remove(file_path)
        raise HTTPException(
            status_code=404,
            detail="Failed to extract Date of Birth. Image is not readable or isn't in the right format",
        )


# Authenticat, for admin login
@router_function.post("/auth/")
def authenticate_user(credentials: dict):
    username = credentials.get("username")
    password = credentials.get("password")
    hostname = credentials.get("hostname")
    db_name = credentials.get("db_name")

    # Establish connection to the phpMyAdmin database
    db_connection = mysql.connector.connect(
        host=hostname, user=username, password=password, database=db_name
    )

    # Check if connection was successful
    if db_connection.is_connected():
        db_connection.close()
        return JSONResponse(content={"message": "Login successful"}, status_code=200)
    else:
        return JSONResponse(content={"message": "Invalid credentials"}, status_code=401)
