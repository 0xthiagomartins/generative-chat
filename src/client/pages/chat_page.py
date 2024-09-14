import streamlit as st
from utils.api_client import (
    send_chat_message,
    get_conversations,
    start_new_conversation,
    generate_image,
    get_chat_history,
)


def show_chat_page():
    st.header("Chat")

    # Sidebar for conversation management
    st.sidebar.title("Conversations")
    if st.sidebar.button("Start New Conversation"):
        new_conversation = start_new_conversation()
        if new_conversation:
            st.session_state.current_conversation_id = new_conversation["id"]
            st.session_state.messages = []
            st.rerun()

    # Load conversations
    conversations = get_conversations()

    # Display conversations in the sidebar
    for conv in conversations:
        if st.sidebar.button(
            f"{conv['title']} - {conv['created_at'][:10]}", key=f"conv_{conv['id']}"
        ):
            st.session_state.current_conversation_id = conv["id"]
            st.session_state.messages = get_chat_history(conv["id"])
            st.rerun()

    # Model selection
    model = st.sidebar.selectbox(
        "Select Model", ["gpt-3.5-turbo", "gpt-4", "text-davinci-002"]
    )

    # Initialize session state for messages and current conversation
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = None

    # Chat history
    chat_container = st.container()

    # Input container
    input_container = st.container()

    # Display chat messages
    with chat_container:
        for message in st.session_state.messages:
            if message["is_from_user"]:
                st.chat_message("user").write(message["content"])
            else:
                st.chat_message("assistant").write(message["content"])

    # Input and send button
    with input_container:
        user_input = st.chat_input("Type your message here...")

    # Send message logic
    if user_input:
        if not st.session_state.current_conversation_id:
            new_conversation = start_new_conversation()
            st.session_state.current_conversation_id = new_conversation["id"]

        with st.spinner("AI is thinking..."):
            response = send_chat_message(
                user_input, model, st.session_state.current_conversation_id
            )

        if response:
            if isinstance(response, dict) and "error" in response:
                st.error(response["error"])
            else:
                st.session_state.messages.append(
                    {"is_from_user": True, "content": user_input}
                )
                st.session_state.messages.append(
                    {"is_from_user": False, "content": response}
                )
                st.rerun()
        else:
            st.error("Failed to get a response from the AI. Please try again.")

    # Image upload
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
        if uploaded_file is not None:
            if st.button("Process Image"):
                response = generate_image()
                st.success(response["message"])
