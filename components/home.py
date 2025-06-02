import streamlit as st
import requests
from requests.exceptions import RequestException

def get_data_from_backend():
    try:
        response = requests.get(f"{st.secrets['BACKEND_IP']}/data")
        response.raise_for_status()
        data = response.json()
        return data
    except RequestException as e:
        st.warning("⚠️ Server not reachable, using mock data.")
        return {
            "message": "Hello from Mocked Backend!",
            "value": 99
        }

def show():
    st.title("Home Page - Data Fetch")
    if st.button("Fetch Data from Backend"):
        data = get_data_from_backend()
        if data:
            st.write("Message from Backend:", data['message'])
            st.write("Value from Backend:", data['value'])
