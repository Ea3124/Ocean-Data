import streamlit as st
import time
import requests

def response_generator(assistant_response):
    for word in assistant_response.split():
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

        # Send prompt to the Flask server
        try:
            response = requests.post(
                "http://10.125.70.48:5000/ask",
                json={"question": prompt}  # 질문을 JSON 형식으로 전송
            )
            response.raise_for_status()  # 응답이 오류일 경우 예외 발생
            assistant_response = response.json().get("answer", "No answer provided.")  # 응답에서 "answer" 키를 가져옴
        except requests.exceptions.RequestException:
            assistant_response = "에러가 발생했습니다. 다시 질문해주세요."  # 에러 메시지 설정

        # Display assistant response in a streaming manner
        with st.chat_message("assistant"):
            response_container = st.empty()
            full_response = ""
            for word in response_generator(assistant_response):
                full_response += word  # 각 단어를 누적
                response_container.markdown(full_response)  # 현재 상태 업데이트

        # Update session state with completed assistant response
        st.session_state.messages.append({"role": "assistant", "content": assistant_response})

