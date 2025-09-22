import streamlit as st
from googletrans import Translator, LANGUAGES

# Initialize translator
translator = Translator()

# Streamlit UI
st.title("💬 Language Translator Chatbot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Language selection
target_lang = st.sidebar.selectbox("🌍 Select target language", list(LANGUAGES.keys()), index=21)  # Default to French

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type a message...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Translate message
    translated_text = translator.translate(user_input, dest=target_lang).text

    # Display bot response
    bot_response = f"**Translated:** {translated_text}"
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)