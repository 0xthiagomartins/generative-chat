import streamlit as st
from components.login_form import show_login_form
from components.register_form import show_register_form


def show_auth_page():
    st.title("Welcome to Generative Chat")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        show_login_form()
    with tab2:
        show_register_form()
