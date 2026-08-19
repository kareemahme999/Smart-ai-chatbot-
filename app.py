import os

import streamlit as st
from dotenv import load_dotenv

from core.chatbot_engine import ChatbotError, SmartChatbot

load_dotenv()

st.set_page_config(page_title="Smart AI Chatbot", page_icon="🤖", layout="centered")

st.title("🤖 Smart AI Chatbot")
st.caption("TechMaster Academy · Phase 04 / Project 04")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chatbot" not in st.session_state:
    st.session_state.chatbot = None
    st.session_state.error = None
    default_key = os.getenv("COHERE_API_KEY")
    if default_key:
        try:
            st.session_state.chatbot = SmartChatbot(api_key=default_key)
        except ChatbotError as e:
            st.session_state.error = str(e)

with st.sidebar:
    st.header("⚙️ Settings")
    key_input = st.text_input(
        "Cohere API Key",
        type="password",
        value=os.getenv("COHERE_API_KEY", ""),
        help="Get a free key from dashboard.cohere.com",
    )

    if st.button("🔌 Save key & connect", use_container_width=True):
        try:
            st.session_state.chatbot = SmartChatbot(api_key=key_input)
            st.session_state.error = None
            st.success("Connected to the API successfully!")
        except ChatbotError as e:
            st.session_state.chatbot = None
            st.session_state.error = str(e)

    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        if st.session_state.chatbot:
            st.session_state.chatbot.reset_conversation()
        st.rerun()

    st.divider()
    st.caption(
        "This project uses the Cohere Chat API to get real AI responses, "
        "while keeping conversation context and handling errors."
    )

if st.session_state.error:
    st.warning(st.session_state.error)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Type your message here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        if st.session_state.chatbot is None:
            st.error("Please enter a valid Cohere API key in the sidebar first.")
        else:
            with st.spinner("Thinking..."):
                try:
                    reply = st.session_state.chatbot.send_message(user_input)
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except ChatbotError as e:
                    st.error(str(e))
