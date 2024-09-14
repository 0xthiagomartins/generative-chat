import streamlit as st
from utils.api_client import register_user


def show_register_form():
    st.header("Register")
    username = st.text_input("Username", key="register_username")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")
    confirm_password = st.text_input(
        "Confirm Password", type="password", key="register_confirm_password"
    )
    full_name = st.text_input("Full Name", key="register_full_name")

    if st.button("Register"):
        if password != confirm_password:
            st.error("Passwords do not match")
        else:
            if register_user(username, email, password, full_name):
                st.success("Registered successfully! Please log in.")
            else:
                st.error("Registration failed. Please try again.")
