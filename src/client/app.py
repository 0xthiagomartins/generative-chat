import streamlit as st
import requests
import json

BACKEND_URL = "http://localhost:8000"  # Adjust if your server runs on a different port


def main():
    st.set_page_config(page_title="Generative Chat", page_icon="💬")

    # Check if user is logged in
    if "access_token" not in st.session_state:
        show_auth_page()
    else:
        show_main_page()


def show_auth_page():
    st.title("Welcome to Generative Chat")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        show_login_form()

    with tab2:
        show_register_form()


def show_login_form():
    st.header("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        response = requests.post(
            f"{BACKEND_URL}/token",
            data={"username": username, "password": password},
        )
        if response.status_code == 200:
            token_data = response.json()
            st.session_state.access_token = token_data["access_token"]
            st.success("Logged in successfully!")
            st.rerun()
        else:
            st.error("Invalid username or password")


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
            response = requests.post(
                f"{BACKEND_URL}/register",
                json={
                    "username": username,
                    "email": email,
                    "password": password,
                    "full_name": full_name,
                },
            )
            if response.status_code == 200:
                st.success("Registered successfully! Please log in.")
            else:
                st.error(
                    f"Registration failed: {response.json().get('detail', 'Unknown error')}"
                )


def show_main_page():
    st.title("Generative Chat")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Chat", "How It Works"])

    if page == "Chat":
        show_chat_page()
    elif page == "How It Works":
        show_how_it_works()

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.pop("access_token", None)
        st.rerun()

    # Sidebar info
    st.sidebar.title("About")
    st.sidebar.info(
        "This is a generative chat application built with Streamlit and FastAPI."
    )


def show_chat_page():
    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("You:", key="user_input")

    if user_input:
        # Send request to server
        headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
        response = requests.post(
            f"{BACKEND_URL}/chat", json={"content": user_input}, headers=headers
        )

        if response.status_code == 200:
            ai_response = response.json()["response"]

            # Add user input and AI response to chat history
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_response}
            )
        else:
            st.error(f"Error: Server responded with status code {response.status_code}")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


def show_how_it_works():
    st.title("How It Works")

    st.write(
        """
    Welcome to the Generative Chat application! Here's how it works:

    1. **User Authentication**: Users need to register and log in to use the chat functionality.
    2. **User Interface**: The application uses Streamlit to create an interactive web interface where you can input your messages and see the chat history.
    3. **Backend Server**: When you send a message, it's transmitted to a FastAPI backend server.
    4. **Language Model**: The server uses a language model (powered by Langchain) to generate a response based on your input.
    5. **Response**: The generated response is sent back to the Streamlit frontend and displayed in the chat history.
    6. **Chat History**: Your conversation is stored in the session state and associated with your user account.

    To use the application:
    - Register for an account or log in if you already have one.
    - Navigate to the "Chat" page using the sidebar.
    - Type your message in the text input field and press Enter.
    - The AI-generated response will appear in the chat history.
    - You can continue the conversation by sending more messages.
    - Log out when you're done to protect your account.

    Enjoy your chat with our AI assistant!
    """
    )


if __name__ == "__main__":
    main()
