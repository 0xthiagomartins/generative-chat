import streamlit as st
from utils.api_client import get_user_settings, update_user_settings
import plotly.graph_objects as go


def show_settings_page():
    st.title("Settings")
    st.header("Preferences")

    # Get current user settings
    current_settings = get_user_settings()

    if current_settings:
        # Theme toggle
        st.subheader("Theme")
        current_theme = current_settings["theme"]
        is_dark_theme = current_theme == "dark"

        # Use st.toggle for theme selection
        dark_mode = st.toggle("Dark Mode", value=is_dark_theme)
        new_theme = "dark" if dark_mode else "light"

        # New Storage section
        st.header("Storage")
        col1, col2 = st.columns([3, 2])

        with col1:
            st.write(
                "The estimated amount of storage used to store your conversations and images. "
                "You can free up space by deleting conversations."
            )

        with col2:
            # Calculate storage usage
            storage_used = current_settings.get("storage_used", 0)
            storage_limit = current_settings.get(
                "storage_limit", 1000000000
            )  # 1 GB default
            storage_used_gb = storage_used / 1e9
            storage_limit_gb = storage_limit / 1e9
            usage_percentage = (storage_used / storage_limit) * 100

            # Create pie chart
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=["Used", "Available"],
                        values=[usage_percentage, 100 - usage_percentage],
                        hole=0.7,
                        marker_colors=["#1f77b4", "#d3d3d3"],
                    )
                ]
            )
            fig.update_layout(
                annotations=[
                    dict(
                        text=f"{storage_limit_gb:.1f} GB",
                        x=0.5,
                        y=0.5,
                        font_size=20,
                        showarrow=False,
                    )
                ],
                showlegend=False,
                width=100,
                height=100,
                margin=dict(l=0, r=0, t=0, b=0),
            )
            st.plotly_chart(fig)
            st.write(f"Used: {storage_used_gb:.2f} GB ({usage_percentage:.1f}%)")

        default_text_model = st.selectbox(
            "Default Text Model",
            ["gpt-3.5-turbo", "gpt-4", "claude"],
            index=["gpt-3.5-turbo", "gpt-4", "claude"].index(
                current_settings["default_text_model"]
            ),
        )
        default_image_model = st.selectbox(
            "Default Image Model",
            ["dall-e-2", "dall-e-3"],
            index=["dall-e-2", "dall-e-3"].index(
                current_settings["default_image_model"]
            ),
        )

        language = st.selectbox(
            "Language",
            ["en", "es", "fr", "de", "zh", "ja"],
            index=["en", "es", "fr", "de", "zh", "ja"].index(
                current_settings["language"]
            ),
        )

        # New Conversation section
        st.subheader("Conversation")
        show_options_menu = st.checkbox(
            "Show options menu when clicking a message",
            value=current_settings.get(
                "show_options_menu_when_clicking_a_message", False
            ),
        )
        show_explicit_content = st.checkbox(
            "Show explicit content",
            value=current_settings.get("show_explicit_content", False),
        )

        # Save preferences button
        if st.button("Save Preferences"):
            new_settings = {
                "default_text_model": default_text_model,
                "default_image_model": default_image_model,
                "theme": new_theme,  # Use the current theme
                "language": language,
                "show_options_menu_when_clicking_a_message": show_options_menu,
                "show_explicit_content": show_explicit_content,
            }
            if update_user_settings(new_settings):
                st.success("Preferences saved successfully!")
            else:
                st.error("Failed to save preferences. Please try again.")
    else:
        st.error("Failed to load user settings. Please try again later.")
    st.header("Your AI-Powered Partner")
    st.write(
        "NanoGPT answers questions, generates images, and assists with various tasks. From creative writing to coding help, NanoGPT is your all-in-one AI companion."
    )

    st.header("Cutting-Edge Models")
    st.write(
        "Access a wide range of top-tier text and image models. We continuously update our selection, ensuring you always have the most advanced AI technology at your fingertips."
    )

    st.header("Pay-As-You-Go Simplicity")
    st.write(
        "Start by adding as little as $0.10 to your wallet. Pay per use with no subscriptions or hidden fees. Easily withdraw your funds via Nano cryptocurrency at any time, completely free."
    )

    st.header("Uncompromising Privacy")
    st.write(
        "No data is stored on our servers. All conversations and generated content remain solely on your device. NanoGPT is committed to protecting your privacy and data sovereignty."
    )
    # Terms of Service link
    st.markdown("[Terms of Service](/legal/terms-of-service)")

    # Let's go button
    if st.button("Let's go"):
        st.write("Redirecting to main application...")
        # Here you would implement the logic to redirect to the main application
