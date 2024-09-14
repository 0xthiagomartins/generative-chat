import streamlit as st


def show_how_it_works_page():
    st.title("How It Works")
    st.write(
        """
    Welcome to the Generative Chat application! Here's how it works:

    1. User Authentication: Register or log in to use the chat.
    2. User Interface: Interactive web interface for messaging.
    3. Backend Server: Messages are sent to a FastAPI backend.
    4. Language Model: The server uses an AI model to generate responses.
    5. Response: AI-generated responses are displayed in the chat history.
    6. Chat History: Conversations are stored and associated with your account.

    Enjoy chatting with our AI assistant!
    """
    )
