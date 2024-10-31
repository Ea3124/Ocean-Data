import streamlit as st
import random
import time

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def show():
    st.title("Simple Chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("무엇이 궁금하신가요?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Initialize assistant response and start streaming
        assistant_response = ""
        with st.chat_message("assistant"):
            response_container = st.empty()
            for word in response_generator():
                assistant_response += word
                response_container.markdown(assistant_response)
                time.sleep(0.05)

        # Update session state with completed assistant response
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})
