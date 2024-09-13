import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"  # Adjust if your server runs on a different port


def main():
    st.set_page_config(page_title="Generative Chat", page_icon="💬")

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Chat", "How It Works"])

    if page == "Chat":
        show_chat_page()
    elif page == "How It Works":
        show_how_it_works()

    # Sidebar info
    st.sidebar.title("About")
    st.sidebar.info(
        "This is a generative chat application built with Streamlit and FastAPI."
    )


def show_chat_page():
    st.title("Generative Chat")

    # Check server health
    try:
        health_response = requests.get(f"{BACKEND_URL}/health")
        if health_response.status_code == 200:
            st.success("Server is running")
        else:
            st.error("Server is not responding correctly")
    except requests.ConnectionError:
        st.error("Cannot connect to the server. Make sure it's running.")
        return

    # Chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []

    user_input = st.text_input("You:", key="user_input")

    if user_input:
        # Send request to server
        response = requests.post(f"{BACKEND_URL}/chat", json={"content": user_input})

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

    1. **User Interface**: The application uses Streamlit to create an interactive web interface where you can input your messages and see the chat history.

    2. **Backend Server**: When you send a message, it's transmitted to a FastAPI backend server.

    3. **Language Model**: The server uses a language model (powered by Langchain) to generate a response based on your input.

    4. **Response**: The generated response is sent back to the Streamlit frontend and displayed in the chat history.

    5. **Chat History**: Your conversation is stored in the session state, allowing you to see the full context of your interaction.

    6. **Server Health**: The application checks if the server is running and accessible before allowing you to chat.

    To use the application:
    - Navigate to the "Chat" page using the sidebar.
    - Type your message in the text input field and press Enter.
    - The AI-generated response will appear in the chat history.
    - You can continue the conversation by sending more messages.

    Enjoy your chat with our AI assistant!
    """
    )


if __name__ == "__main__":
    main()
