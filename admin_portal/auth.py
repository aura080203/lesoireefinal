import streamlit as st
import requests

# from auth import pg_conf


# Page config
# def pg_conf(width="centered"):
#     st.set_page_config(
#         page_title="Lesoiree Admin Dashboard",
#         page_icon=":dog:",  # Set your desired icon
#         layout=width,  # Choose the layout style: "centered", "wide", "wide+sidebar"
#         initial_sidebar_state="auto",  # Set the initial state of the sidebar: "auto", "expanded", "collapsed"
# )


def login_form():
    # Login form
    login_form = st.form(key="login_form")
    login_form.title("Admin Login")
    username = login_form.text_input("Username")
    password = login_form.text_input("Password", type="password")
    submit_button = login_form.form_submit_button("Login")

    if submit_button:
        # Make request to FastAPI for authentication
        hostname = ("localhost",)
        db_name = ("hostname",)
        response = authenticate_user(username, password, "localhost", "lesoiree")
        if response.status_code == 200:
            st.session_state.logged_in = True
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")

        # st.session_state.logged_in = True  # debug mode
        # st.success("Login successful")  # debug mode
        # st.rerun()  # debug mode


def authenticate_user(username, password, hostname, db_name):
    # Endpoint URL of the FastAPI authentication route
    authentication_endpoint = "http://localhost:8000/auth/"

    # Payload containing username and password
    payload = {
        "username": username,
        "password": password,
        "hostname": hostname,
        "db_name": db_name,
    }

    # Make a POST request to FastAPI
    response = requests.post(authentication_endpoint, json=payload)

    return response
