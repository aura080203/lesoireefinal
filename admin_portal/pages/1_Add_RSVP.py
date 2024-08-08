import streamlit as st
from datetime import datetime
import requests, os
from auth import login_form
from sidebar import side_bar, save_uploadedfile

st.set_page_config(
    page_title="Lesoiree Admin Dashboard",
    page_icon=":dog:",  # Set your desired icon
    layout="centered",  # Choose the layout style: "centered", "wide", "wide+sidebar"
    initial_sidebar_state="auto",  # Set the initial state of the sidebar: "auto", "expanded", "collapsed"
)


def main():
    # Check if user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        # Sidebar
        side_bar()
        add_rsvp_form()
    else:
        login_form()


# Function to add new RSVP entry
def add_rsvp_form():
    # Form for adding new RSVP entry
    with st.form(key="add_rsvp_form", border=False):
        st.header("Add New RSVP")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        date_of_birth = st.date_input(
            "Date of Birth", max_value=datetime.now(), min_value=datetime(1900, 1, 1)
        )
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        uploaded_file = st.file_uploader(
            "Upload your paspport image",
            type=["jpg", "png"],
            accept_multiple_files=False,
        )
        passport_img = None  # Initialize passport_img outside the if block
        if uploaded_file is not None:
            passport_img = uploaded_file
            # scanned_dob = uploaded_file.getvalue()

        guests = st.number_input("Number of Guests", min_value=1, value=1)
        rsvp_date = st.date_input("RSVP Date")
        rsvp_time = st.selectbox(
            "RSVP Time", ["12:00 AM - 04:00 AM", "09:00 PM - 12:00 AM"]
        )
        payment = st.checkbox("Payment Made?")
        message = st.text_area("Message")
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            if passport_img is None:
                st.error("Please upload a passport image.")
            else:
                # Handle form submission
                file_path = save_uploadedfile(passport_img, email, phone)

                passport_to_scan = open(file_path, "rb")

                # st.write({scanned_dob.name, scanned_dob})
                passport_dob = extract_dob(passport_to_scan)
                # st.write(passport_dob)
                add_rsvp_to_backend(
                    first_name,
                    last_name,
                    email,
                    date_of_birth,
                    passport_dob,
                    phone,
                    gender,
                    guests,
                    rsvp_date,
                    rsvp_time,
                    message,
                    payment,
                )
                os.remove(file_path)
                print("RSVP submitted successfully")


# Function to add new RSVP entry to the backend
def add_rsvp_to_backend(
    first_name,
    last_name,
    email,
    date_of_birth,
    scanned_dob,
    phone,
    gender,
    guests,
    rsvp_date,
    rsvp_time,
    message,
    payment,
):
    # Convert date value to string
    date_of_birth_str = str(date_of_birth.strftime("%Y-%m-%d"))
    rsvp_date_str = str(rsvp_date.strftime("%Y-%m-%d"))
    # date_of_birth_str = (
    #     datetime.strptime(str(date_of_birth), "%Y-%m-%d") if date_of_birth else None
    # )

    # rsvp_date_str = datetime.strptime(str(rsvp_date), "%Y-%m-%d") if rsvp_date else None

    # Endpoint URL of the FastAPI route to add new RSVP
    add_rsvp_endpoint = "http://127.0.0.1:8000/rsvp/create/"

    # Payload containing RSVP data
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "date_of_birth": date_of_birth_str,
        "scanned_dob": scanned_dob,  # Assuming scanned_dob is already a string
        "phone": phone,
        "gender": gender,
        "guests": guests,
        "rsvp_date": rsvp_date_str,
        "rsvp_time": rsvp_time,
        "message": message,
        "payment": payment,
    }
    st.toast(payload)
    try:
        # Make a POST request to FastAPI
        response = requests.post(add_rsvp_endpoint, json=payload)

        # Check if the request was successful
        if response.status_code == 200:
            st.success("RSVP added successfully")
        else:
            st.error(f"Failed to add RSVP. Error: {response.text}")
    except Exception as e:
        st.error(f"An error occurred while sending the request to FastAPI: {str(e)}")


# Function to extract Date of Birth from passport image
def extract_dob(image_to_scan):
    # Endpoint URL of the FastAPI route to extract DoB
    extract_dob_endpoint = "http://localhost:8000/rsvp/scan_passport/"
    try:
        # Construct files parameter
        file_data = image_to_scan.read()
        print("file name:", image_to_scan.name)
        files = {"file": (image_to_scan.name, file_data, "image/jpeg")}

        # Make a POST request to FastAPI
        response = requests.post(extract_dob_endpoint, files=files)

        # Check if the request was successful
        if response.status_code == 200:
            st.toast("Date of Birth extracted successfully from passport")
            return response.json()["date of birth"]

        else:
            st.error("Failed to extract Date of Birth from your passport")
            st.write("Error:", response.text)
    except Exception as e:
        st.error("An error occurred while sending the request to FastAPI:")
        st.write(e)


if __name__ == "__main__":
    main()
