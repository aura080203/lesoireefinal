import os
from shutil import copyfileobj
from datetime import datetime
from fastapi import HTTPException


# Function to save the uploaded file
def save_file(file, path):
    # Defined image directory
    images_dir = str("src/images/" + path)

    # Ensure the directory exists
    os.makedirs(images_dir, exist_ok=True)

    # Define the file path to save the image
    file_path = os.path.join(images_dir, file.filename)

    # Save the uploaded image
    with open(file_path, "wb") as buffer:
        copyfileobj(file.file, buffer)

    return file_path


# Function to delete all uploaded image files in directory
def delete_images(directory):
    files_in_directory = os.listdir(directory)
    for file in files_in_directory:
        # Check if the file is a JPEG file (.jpg or .jpeg)
        if file.lower().endswith((".jpg", ".jpeg")):
            # Delete the JPEG file
            os.remove(os.path.join(directory, file))


# Format Date
def format_date(textual_date):
    date_formats = [
        "%d %b %Y",
        "%d %B %Y",
    ]  # Supports both abbreviated and full month names

    for date_format in date_formats:
        try:
            date_time_obj = datetime.strptime(textual_date, date_format)
            return date_time_obj.strftime("%Y-%m-%d")
        except ValueError:
            pass  # Continue to the next format if parsing fails
    # return "Invalid date format."
    raise HTTPException(status_code=404, detail="Invalid date format.")


# Calculate age based on DoB
def calculate_age(date_of_birth):
    # Convert date_of_birth string to datetime object
    dob = datetime.strptime(date_of_birth, "%Y-%m-%d")

    # Get current date
    current_date = datetime.now()

    # Calculate age
    age = (
        current_date.year
        - dob.year
        - ((current_date.month, current_date.day) < (dob.month, dob.day))
    )

    return age
