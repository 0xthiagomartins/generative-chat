import streamlit as st
import pandas as pd


def show_pricing_page():
    st.title("Pricing")

    st.markdown(
        """
    #### Pricing example

    The message cost depends on the number of words you send and the number of words the AI returns. One word roughly equals one token.

    The example below has 57 input tokens and 153 output tokens. Asking a model the example prompt and getting the example response would result in the example cost listed in the table.

    Chat models by default use the chat history as input for additional context. As conversations go longer your input and therefore the cost increases. We recommend opening new chats liberally.

    The cost to generate an image is listed per image model and can differ based on resolution.

    There is a fixed base fee of Ӿ0.001 Nano per request which is already reflected in the example cost.
    """
    )

    st.subheader("Input (57 tokens)")
    st.text(
        "Explain the concept of artificial intelligence in simple terms. Pretend that I'm a 5-year old that doesn't have a very long attention span, so keep it limited to roughly 150 words."
    )

    st.subheader("Output (153 tokens)")
    st.text(
        """Okay! Imagine you have a really smart robot friend. This robot can learn things just like you do. It can understand what you say, help you find your toys, or even play games with you! Artificial intelligence, or AI for short, is like the robot's brain. It helps the robot think, learn, and make decisions. So, if you teach the robot how to play a game, it can remember and get better over time! Just like when you use your brain to solve puzzles or tell stories, AI uses its brain to do cool things like answering questions, recognizing faces, or even driving cars. It's all about making machines smart so they can help us in our everyday lives! Isn't that fun?"""
    )

    st.subheader("Model Pricing")
    st.markdown("Prices are shown in Nano (Ӿ). Current Nano price: $0.95 USD")

    # Create a DataFrame for the pricing table
    data = {
        "Model Name": [
            "ChatGPT 4o",
            "Claude 3 Opus",
            "Claude 3.5 Sonnet",
            "GPT 3.5 Turbo (API only)",
            "GPT 4 Turbo (API only)",
            "GPT 4o",
            "GPT 4o (API only)",
            "GPT 4o mini",
            "Gemini 1.5 Flash",
            "Gemini 1.5 Flash (API only)",
            "Gemini 1.5 Pro",
            "Gemini 1.5 Pro (API only)",
            "Gemini 1.5 Pro Exp (API only)",
            "Hermes 3 Large",
            "Hermes 3 Large (API only)",
            "L3 Euryale 70B (API only)",
            "Llama 3.1 Large",
            "Llama 3.1 Large (API only)",
            "Llama 3.1 Medium",
            "Llama 3.1 Medium (API only)",
            "MythoMax 13B (API only)",
            "OpenAI o1",
            "OpenAI o1-mini",
            "Reflection 70B",
            "Sonar Online (API only)",
            "Sonar Online Huge",
            "WizardLM-2 8x22B (API only)",
        ],
        "Example Cost": [
            "Ӿ0.00563",
            "Ӿ0.02312",
            "Ӿ0.00542",
            "Ӿ0.00146",
            "Ӿ0.01026",
            "Ӿ0.00400",
            "Ӿ0.00563",
            "Ӿ0.00118",
            "Ӿ0.00112",
            "Ӿ0.00118",
            "Ӿ0.00553",
            "Ӿ0.00748",
            "Ӿ0.00460",
            "Ӿ0.00118",
            "Ӿ0.00118",
            "Ӿ0.00113",
            "Ӿ0.00230",
            "Ӿ0.00323",
            "Ӿ0.00134",
            "Ӿ0.00138",
            "Ӿ0.00104",
            "Ӿ0.01901",
            "Ӿ0.00460",
            "Ӿ0.00138",
            "Ӿ0.00138",
            "Ӿ0.00288",
            "Ӿ0.00119",
        ],
        "Example prompts per $1": [
            187,
            45,
            194,
            721,
            102,
            263,
            187,
            894,
            942,
            894,
            190,
            141,
            229,
            894,
            894,
            936,
            458,
            326,
            788,
            766,
            1017,
            55,
            229,
            766,
            766,
            365,
            888,
        ],
        "Input Rate (per 1k tokens)": [
            "Ӿ0.00897",
            "Ӿ0.02691",
            "Ӿ0.00538",
            "Ӿ0.00090",
            "Ӿ0.01794",
            "Ӿ0.00449",
            "Ӿ0.00897",
            "Ӿ0.00027",
            "Ӿ0.00018",
            "Ӿ0.00027",
            "Ӿ0.00718",
            "Ӿ0.01256",
            "Ӿ0.00538",
            "Ӿ0.00027",
            "Ӿ0.00027",
            "Ӿ0.00054",
            "Ӿ0.00359",
            "Ӿ0.00538",
            "Ӿ0.00161",
            "Ӿ0.00179",
            "Ӿ0.00018",
            "Ӿ0.02691",
            "Ӿ0.00538",
            "Ӿ0.00179",
            "Ӿ0.00179",
            "Ӿ0.00897",
            "Ӿ0.00090",
        ],
        "Output Rate (per 1k tokens)": [
            "Ӿ0.02691",
            "Ӿ0.13457",
            "Ӿ0.02691",
            "Ӿ0.00269",
            "Ӿ0.05383",
            "Ӿ0.01794",
            "Ӿ0.02691",
            "Ӿ0.00108",
            "Ӿ0.00072",
            "Ӿ0.00108",
            "Ӿ0.02691",
            "Ӿ0.03768",
            "Ӿ0.02153",
            "Ӿ0.00108",
            "Ӿ0.00108",
            "Ӿ0.00063",
            "Ӿ0.00718",
            "Ӿ0.01256",
            "Ӿ0.00161",
            "Ӿ0.00179",
            "Ӿ0.00018",
            "Ӿ0.10765",
            "Ӿ0.02153",
            "Ӿ0.00179",
            "Ӿ0.00179",
            "Ӿ0.00897",
            "Ӿ0.00090",
        ],
        "API Name": [
            "chatgpt-4o-latest",
            "claude-3-opus-20240229",
            "claude-3-5-sonnet-20240620",
            "gpt-3.5-turbo",
            "gpt-4-turbo-preview",
            "gpt-4o-2024-08-06",
            "gpt-4o",
            "gpt-4o-mini",
            "google/gemini-flash-1.5",
            "gemini-1.5-flash-001",
            "google/gemini-pro-1.5",
            "gemini-1.5-pro-001",
            "google/gemini-pro-1.5-exp",
            "nousresearch/hermes-3-llama-3.1-405b",
            "nousresearch/hermes-3-llama-3.1-405b:extended",
            "sao10k/l3-euryale-70b",
            "meta-llama/llama-3.1-405b-instruct",
            "accounts/fireworks/models/llama-v3p1-405b-instruct",
            "accounts/fireworks/models/llama-v3p1-70b-instruct",
            "llama-3.1-70b-instruct",
            "gryphe/mythomax-l2-13b",
            "o1-preview",
            "o1-mini",
            "mattshumer/reflection-70b",
            "llama-3.1-sonar-large-128k-online",
            "llama-3.1-sonar-huge-128k-online",
            "microsoft/wizardlm-2-8x22b",
        ],
    }

    df = pd.DataFrame(data)

    # Display the table
    st.dataframe(df, hide_index=True)
