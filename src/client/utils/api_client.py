import streamlit as st
from configuration import BACKEND_URL
import requests


def login_user(username: str, password: str) -> bool:
    response = requests.post(
        f"{BACKEND_URL}/token", data={"username": username, "password": password}
    )
    if response.status_code == 200:
        token_data = response.json()
        st.session_state.access_token = token_data["access_token"]
        return True
    return False


def register_user(username: str, email: str, password: str, full_name: str) -> bool:
    response = requests.post(
        f"{BACKEND_URL}/register",
        json={
            "username": username,
            "email": email,
            "password": password,
            "full_name": full_name,
        },
    )
    return response.status_code == 200


def send_chat_message(message: str, model: str) -> str:
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.post(
        f"{BACKEND_URL}/chat/text",
        json={"content": message, "model": model},
        headers=headers,
    )
    if response.status_code == 200:
        return response.json()["response"]
    elif response.status_code in [500, 503]:
        return {"error": response.json()["detail"]}
    else:
        return {"error": "An unexpected error occurred. Please try again."}


def get_chat_history():
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(f"{BACKEND_URL}/chat/history", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []


def generate_image(file):
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.post(f"{BACKEND_URL}/chat/image", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def get_user_settings():
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(f"{BACKEND_URL}/user/settings", headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def update_user_settings(settings):
    headers = {
        "Authorization": f"Bearer {st.session_state.access_token}",
        "Content-Type": "application/json",
    }
    response = requests.put(
        f"{BACKEND_URL}/user/settings",
        json=settings,  # Send the entire settings dictionary
        headers=headers,
    )
    return response.status_code == 200


def start_new_conversation(model: str = "gpt-3.5-turbo"):
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.post(
        f"{BACKEND_URL}/conversations", json={"model": model}, headers=headers
    )
    if response.status_code == 200:
        json = response.json()
        print(json)
        return json
    return None


def get_conversations():
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(f"{BACKEND_URL}/conversations", headers=headers)
    if response.status_code == 200:
        return response.json()
    return []
