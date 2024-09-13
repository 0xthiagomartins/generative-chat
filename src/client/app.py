import streamlit as st
from pages.auth_page import show_auth_page
from pages.chat_page import show_chat_page
from pages.how_it_works_page import show_how_it_works_page
from pages.pricing_page import show_pricing_page
from pages.settings_page import show_settings_page
from configuration import APP_TITLE, APP_ICON


def main():
    st.set_page_config(page_title=APP_TITLE, page_icon=APP_ICON, layout="wide")

    if "access_token" not in st.session_state:
        show_auth_page()
    else:
        show_main_page()


def show_main_page():
    st.title(APP_TITLE)

    page = st.sidebar.radio(
        "Navigation", ["Chat", "How It Works", "Pricing", "Settings"]
    )

    if page == "Chat":
        show_chat_page()
    elif page == "How It Works":
        show_how_it_works_page()
    elif page == "Pricing":
        show_pricing_page()
    elif page == "Settings":
        show_settings_page()

    if st.sidebar.button("Logout"):
        st.session_state.pop("access_token", None)
        st.rerun()

    st.sidebar.title("About")
    st.sidebar.info(
        "This is a generative chat application built with Streamlit and FastAPI."
    )


if __name__ == "__main__":
    main()
