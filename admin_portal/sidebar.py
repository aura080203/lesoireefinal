import streamlit as st
import os, re


# Sidebar
def side_bar():
    st.sidebar.title("Navigation")
    logout_button = st.sidebar.button("Logout")
    if logout_button:
        st.session_state.logged_in = False
        st.rerun()

    # refresh_page = st.sidebar.button("Refresh Page")
    # if refresh_page:
    #     st.rerun()


def save_uploadedfile(uploadedfile, email, phone):
    # Extract the file extension from the original filename
    _, extension = os.path.splitext(uploadedfile.name)
    # Remove invalid characters from email and phone
    email_cleaned = re.sub(r"\W+", "", email)
    phone_cleaned = re.sub(r"\W+", "", phone)
    # Combine email and phone to form a unique filename
    filename = f"{email_cleaned}_{phone_cleaned}"
    # Append the file extension to the custom name
    # file_path = os.path.join(".", f"{filename}{extension}")
    file_path = os.path.join("", f"{filename}{extension}")
    # Write the uploaded file to disk with the custom name
    with open(file_path, "wb") as f:
        f.write(uploadedfile.getbuffer())
    return file_path
