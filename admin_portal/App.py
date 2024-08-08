import streamlit as st
import requests
from auth import login_form
from sidebar import side_bar

st.set_page_config(
    page_title="Lesoiree Admin Dashboard",
    page_icon=":dog:",  # Set your desired icon
    layout="wide",  # Choose the layout style: "centered", "wide", "wide+sidebar"
    initial_sidebar_state="expanded",  # Set the initial state of the sidebar: "auto", "expanded", "collapsed"
)


# Streamlit app
def main():

    # Check if user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        st.title("Lesoiree RSVP Dashboard")
        # Sidebar
        side_bar()
        show_rsvps()
    else:
        login_form()
        # st.rerun()


# Function to retrieve and display RSVPs
def show_rsvps():
    # Retrieve all RSVPs from backend
    rsvps = get_all_rsvps()
    if not rsvps:
        st.write("No RSVPs found.")
        return

    # Prepare table data as list of dictionaries
    table_data = rsvps  # Assuming rsvps is already in the correct format

    # Display the table
    st.table(table_data)


def display_rsvps(rsvps):
    if not rsvps:
        return []

    # Extract column headers from the first RSVP
    columns = list(rsvps[0].keys())

    # Create a list of dictionaries for each RSVP
    table_data = [
        {column: rsvp.get(column, "") for column in columns} for rsvp in rsvps
    ]

    return table_data


# Search functionality to get row
def filter_rsvps(rsvps, search_term):
    if search_term:
        return [
            rsvp
            for rsvp in rsvps
            if any(search_term.lower() in str(value).lower() for value in rsvp.values())
        ]
    else:
        return rsvps


# Function to retrieve all RSVPs from the backend
def get_all_rsvps():
    # Endpoint URL of the FastAPI route to retrieve all RSVPs
    rsvps_endpoint = "http://127.0.0.1:8000/rsvp/"
    # Make a GET request to FastAPI
    response = requests.get(rsvps_endpoint)
    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch RSVPs")
        raise Exception("Failed to fetch RSVPs")


if __name__ == "__main__":
    main()
