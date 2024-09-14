import streamlit as st
from utils.api_client import login_user


def show_login_form():
    st.header("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        if login_user(username, password):
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")
