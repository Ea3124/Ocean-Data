# app.py
import streamlit as st
import requests

# Streamlit 앱 제목
st.title("Streamlit - Flask Integration")

# API 요청을 보내 데이터를 가져오는 함수
def get_data_from_backend():
    try:
        # Flask 서버에서 데이터 가져오기
        response = requests.get("http://10.125.70.48:5000/data")
        response.raise_for_status()  # HTTP 에러가 발생할 경우 예외 발생
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# 버튼 클릭 시 데이터 요청
if st.button("Fetch Data from Backend"):
    data = get_data_from_backend()
    if data:
        # 데이터 출력
        st.write("Message from Backend:", data['message'])
        st.write("Value from Backend:", data['value'])
