import streamlit as st
from pages.auth_page import show_auth_page
from pages.chat_page import show_chat_page
from pages.how_it_works_page import show_how_it_works_page
from pages.pricing_page import show_pricing_page
from pages.settings_page import show_settings_page
from configuration import APP_TITLE, APP_ICON
from utils.api_client import get_user_settings


def main():
    # Get user settings
    if "access_token" in st.session_state:
        user_settings = get_user_settings()
        theme = user_settings.get("theme", "light") if user_settings else "light"
    else:
        theme = "light"

    # Set page config
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon=APP_ICON,
        initial_sidebar_state="expanded",
    )

    # Apply theme using custom CSS
    if theme == "dark":
        st.markdown(
            """
        <style>
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        .stSidebar {
            background-color: #262730;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
        <style>
        .stApp {
            background-color: #FFFFFF;
            color: #000000;
        }
        .stSidebar {
            background-color: #F0F2F6;
        }
        </style>
        """,
            unsafe_allow_html=True,
        )

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
