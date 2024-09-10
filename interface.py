__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from streamlit_chat import message as st_message
from chatbot import pak_law_gpt



# Introduction
st.markdown("""## PakConBot
This is a chat bot that has information about the entire constitution of Pakistan. This can help people who want to know about a specific Law.
- Developed by Muhammad Afaq Khan
- Supervised by Hamas Ur Rehman
""")


# Initialize messages in session state if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages above the input section
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input section
if question := st.chat_input("Say Something"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)
    
    response = pak_law_gpt(question)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("ai"):
        st.markdown(response)
