import streamlit as st
import requests
from auth import login_form
from sidebar import side_bar

st.set_page_config(
    page_title="RSVP Admin Dashboard",
    page_icon=":dog:",  # Set your desired icon
    layout="centered",  # Choose the layout style: "centered", "wide", "wide+sidebar"
    initial_sidebar_state="expanded",  # Set the initial state of the sidebar: "auto", "expanded", "collapsed"
)


def main():
    # Check if user is logged in
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        # Sidebar
        side_bar()
        delete_form()
    else:
        login_form()


def delete_form():
    # Form to enter ID to find data to edit
    c1, c2 = st.columns([10, 2])

    id_form = st.form(key="delete-form", border=False)
    id_form.subheader("Enter ID to Delete RSVP")
    with c1:
        id = id_form.text_input(
            "Delete ID", placeholder="Input RSVP ID and press Enter"
        )
    with c2:
        submit_button = id_form.form_submit_button("Find RSVP")
    if submit_button:
        response = delete_id(id)
        if response == None:
            st.error("No entries exist")
        else:
            st.write(response)


is_number = lambda x: isinstance(x, int) or (isinstance(x, str) and x.isdigit())


def delete_id(id):
    if is_number(id):
        # Endpoint URL of the FastAPI route to retrieve all RSVPs
        rsvps_endpoint = f"http://127.0.0.1:8000/rsvp/{id}"

        # Make a GET request to FastAPI
        response = requests.delete(rsvps_endpoint)

        # Check if the request was successful
        if response.status_code != 200:
            st.error("No entries exist")
        else:
            rsvps = response.json()
            return rsvps
    else:
        st.error("Invalid ID format, please input integer numbers")


if __name__ == "__main__":
    main()
