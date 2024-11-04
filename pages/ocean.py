# ocean.py
import streamlit as st
import requests

def show():
    st.title("Ocean Page")

    # 클라이언트의 IP 주소 가져오기
    # try:
    #     ip_response = requests.get('https://api.ipify.org?format=json')
    #     ip_address = ip_response.json().get('ip')
    #     st.write(f"클라이언트 IP 주소: {ip_address}")

    #     # Google Geolocation API를 사용하여 위치 정보 가져오기
    #     LOCATION_API_KEY = "localkey"  # Streamlit Secrets 사용 하거나 해야함
    #     geolocation_url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={LOCATION_API_KEY}'
    #     geolocation_data = {'considerIp': True}
    #     geo_response = requests.post(geolocation_url, json=geolocation_data)
    #     geo_result = geo_response.json()

    #     if 'location' in geo_result:
    #         latitude = geo_result['location']['lat']
    #         longitude = geo_result['location']['lng']
    #         st.write(f"추정 위치는 위도 {latitude}, 경도 {longitude}입니다.")
    #     else:
    #         st.write("위치 정보를 가져올 수 없습니다.")
    # except Exception as e:
    #     st.write("위치 정보를 가져오는 중 오류가 발생했습니다.")
    #     st.write(str(e))

    latitude = 35.241984
    longitude = 129.0797056
    st.write(f"추정 위치는 위도 {latitude}, 경도 {longitude}입니다.")
