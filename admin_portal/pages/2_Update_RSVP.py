import streamlit as st
import requests
from auth import login_form
from sidebar import side_bar
from datetime import datetime

st.set_page_config(
    page_title="Lesoiree Admin Dashboard",
    page_icon=":dog:",  # Set your desired icon
    layout="centered",  # Choose the layout style: "centered", "wide", "wide+sidebar"
    initial_sidebar_state="expanded",  # Set the initial state of the sidebar: "auto", "expanded", "collapsed"
)
is_number = lambda x: isinstance(x, int) or (isinstance(x, str) and x.isdigit())


def main():
    # Check if user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        # Sidebar
        enter_id_form()

    else:
        login_form()


def enter_id_form():
    # Form to enter ID to find data to edit
    c1, c2 = st.columns([10, 2])

    id_form = st.form(key="enter_id_form", border=False)
    id_form.subheader("Search RSVP ID to update")
    with c1:
        id = id_form.text_input(
            "Search RSVP ID", placeholder="Input RSVP ID and press Enter"
        )
    with c2:
        submit_button = id_form.form_submit_button("Find RSVP")
    if submit_button:
        response = get_rsvp_id(id)
        if response == None:
            st.error("No entries exist")
        else:
            with st.expander("Update RSVP Data", expanded=True):
                update_rsvp_form(
                    response["id"],
                    response["first_name"],
                    response["last_name"],
                    response["email"],
                    response["date_of_birth"],
                    response["phone"],
                    response["gender"],
                    response["guests"],
                    response["rsvp_date"],
                    response["rsvp_time"],
                    response["message"],
                    response["payment"],
                )


# Function to retrieve RSVP from the backend by calling ID
def get_rsvp_id(id):
    if is_number(id):
        # Endpoint URL of the FastAPI route to retrieve all RSVPs
        rsvps_endpoint = f"http://127.0.0.1:8000/rsvp/{id}"

        # Make a GET request to FastAPI
        response = requests.get(rsvps_endpoint)

        # Check if the request was successful
        if response.status_code != 200:
            st.error("No entries exist")
        else:
            rsvps = response.json()
            return rsvps
    else:
        st.error("Invalid ID format, please input integer numbers")


def update_rsvp_form(
    id_value,
    first_name_value,
    last_name_value,
    email_value,
    date_of_birth_value,
    phone_value,
    gender_value,
    guests_value,
    rsvp_date_value,
    rsvp_time_value,
    message_value,
    payment_value,
):
    with st.form(key="update_rsvp_form", border=False):
        st.subheader("Update RSVP Data")

        date_of_birth = (
            datetime.strptime(date_of_birth_value, "%Y-%m-%d")
            if date_of_birth_value
            else None
        )
        rsvp_date = (
            datetime.strptime(rsvp_date_value, "%Y-%m-%d") if rsvp_date_value else None
        )

        first_name = st.text_input("First Name", value=first_name_value)
        last_name = st.text_input("Last Name", value=last_name_value)
        email = st.text_input("Email Address", value=email_value)
        date_of_birth = st.date_input("Date of Birth", value=date_of_birth)
        phone = st.text_input("Phone Number", value=phone_value)
        gender_options = ["Male", "Female", "Other"]
        gender_index = (
            gender_options.index(gender_value) if gender_value in gender_options else 0
        )
        gender = st.selectbox("Gender", gender_options, index=gender_index)
        guests = st.text_input(
            "Number of Guests",
            value=guests_value,
        )

        rsvp_date = st.date_input("RSVP Date", value=rsvp_date)
        rsvp_time_options = ["12:00 AM - 04:00 AM", "09:00 PM - 12:00 AM"]
        rsvp_time_index = (
            rsvp_time_options.index(rsvp_time_value)
            if rsvp_time_value in rsvp_time_options
            else 0
        )
        rsvp_time = st.selectbox("RSVP Time", rsvp_time_options, index=rsvp_time_index)
        payment = st.checkbox("Payment Made?", value=payment_value)

        message = st.text_input("Message", value=message_value)
        update_button = st.form_submit_button("Submit")
        if update_button:
            update_rsvp_to_backend(
                id_value,
                first_name,
                last_name,
                email,
                date_of_birth.strftime("%Y-%m-%d") if date_of_birth else None,
                phone,
                gender,
                guests,
                rsvp_date.strftime("%Y-%m-%d") if rsvp_date else None,
                rsvp_time,
                message,
                payment,
            )
            print("RSVP submitted successfully")


def update_rsvp_to_backend(
    id,
    first_name,
    last_name,
    email,
    date_of_birth,
    phone,
    gender,
    guests,
    rsvp_date,
    rsvp_time,
    message,
    payment,
):
    # Convert date value to string
    date_of_birth_str = date_of_birth.strftime("%Y-%m-%d") if date_of_birth else None
    rsvp_date_str = rsvp_date.strftime("%Y-%m-%d") if rsvp_date else None

    # Endpoint URL of the FastAPI route to add new RSVP
    rsvps_endpoint = f"http://127.0.0.1:8000/rsvp/update/{id}"
    # # Payload containing RSVP data
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "date_of_birth": date_of_birth_str,
        "scanned_dob": date_of_birth_str,  # Assuming scanned_dob is already a string
        "phone": phone,
        "gender": gender,
        "guests": guests,
        "rsvp_date": rsvp_date_str,
        "rsvp_time": rsvp_time,
        "message": message,
        "payment": payment,
    }
    try:
        # Make a POST request to FastAPI
        response = requests.put(rsvps_endpoint, json=payload)

        # Check if the request was successful
        if response.status_code != 200:
            st.error(f"Failed to update RSVP. Error: {response.text}")
        else:
            st.success("RSVP updated successfully")
    except Exception as e:
        st.error(f"An error occurred while sending the request to FastAPI: {str(e)}")


if __name__ == "__main__":
    main()
