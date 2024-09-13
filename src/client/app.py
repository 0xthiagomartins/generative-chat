import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"  # Adjust if your server runs on a different port


def main():
    st.set_page_config(page_title="Generative Chat", page_icon="💬")
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

    # Sidebar
    st.sidebar.title("About")
    st.sidebar.info(
        "This is a generative chat application built with Streamlit and FastAPI."
    )


if __name__ == "__main__":
    main()
