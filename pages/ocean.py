# ocean.py
import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import pages.model_temp.model_temp as model_temp
from pyngrok import ngrok

if __name__ == '__main__':
    # ngrok 터널 연결
    port = 8501
    public_url = ngrok.connect(port).public_url
    print(f" * ngrok 터널 URL: {public_url}")


def haversine(lon1, lat1, lon2, lat2):
    from math import radians, sin, cos, sqrt, asin
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2.0)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 지구의 반지름(km)
    return c * r

def process_temperature_data(json_data):
    data = json_data['result']['data']
    df = pd.DataFrame(data)
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    df['datetime'] = pd.to_datetime(df['date'], format='%Y%m%d') + pd.to_timedelta(df['hour'].astype(int), unit='h')
    df.set_index('datetime', inplace=True)
    df.sort_index(inplace=True)
    df = df[['temperature']].dropna()
    return df

def show_temperature_forecast_plotly(json_data):
    """
    72시간 수온 예측 데이터를 Plotly 라인 차트로 시각화
    """
    st.subheader("일주일 수온 예측 Line Graph")
    
    # 데이터 처리
    df = process_temperature_data(json_data)
    
    # 리샘플링 (3시간 간격)
    try:
        df_resampled = df.resample('3H').mean()
    except Exception as e:
        st.error(f"데이터 리샘플링 중 오류가 발생했습니다: {e}")
        return
    
    # Plotly 라인 그래프 생성
    fig = px.line(df_resampled, x=df_resampled.index, y='temperature', markers=True, title="72시간 수온 예측")
    
    # y축 범위 설정 (예: 14도에서 데이터 최대값 + 2도)
    y_min = 14
    y_max = df_resampled['temperature'].max() + 2
    fig.update_layout(
        title={
            'text': "일주일 수온 예측",
            'y':0.9,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'},
        xaxis_title="시간",
        yaxis_title="수온 (°C)",
        yaxis=dict(range=[y_min, y_max]),
        font=dict(
            family="AppleGothic",  # macOS의 경우
            size=12,
            color="Black"
        )
    )
    
    # Plotly 그래프 Streamlit에 표시
    st.plotly_chart(fig, use_container_width=True)

def show():
    st.title("Ocean Page")

    # st.columns()로 열 생성
    col1, col2, col3 = st.columns([0.7, 0.15, 0.15])

    # # 클라이언트의 IP 주소 가져오기
    # try:
    #     ip_response = requests.get('https://api.ipify.org?format=json')
    #     ip_address = ip_response.json().get('ip')
        
    #     # Google Geolocation API를 사용하여 위치 정보 가져오기
    #     LOCATION_API_KEY = st.secrets["LOCATION_API_KEY"]  # Streamlit Secrets 사용 하거나 해야함
    #     geolocation_url = f'https://www.googleapis.com/geolocation/v1/geolocate?key={LOCATION_API_KEY}'
    #     geolocation_data = {'considerIp': True}
    #     geo_response = requests.post(geolocation_url, json=geolocation_data)
    #     geo_result = geo_response.json()

    #     if 'location' in geo_result:
    #         latitude = geo_result['location']['lat']
    #         longitude = geo_result['location']['lng']
    #     else:
    #         st.write("위치 정보를 가져올 수 없습니다.")
    # except Exception as e:
    #     st.write("위치 정보를 가져오는 중 오류가 발생했습니다.")
    #     st.write(str(e))

    latitude = 35.241984
    longitude = 129.0797056

    # 2. 관측소 정보가 담긴 CSV 파일 불러오기
    try:
        df_stations = pd.read_csv('observation_stations.csv')
    except FileNotFoundError:
        st.error("관측소 정보 CSV 파일을 찾을 수 없습니다.")
        return

    # 3. 거리 계산 및 가장 가까운 관측소 찾기
    df_stations['distance'] = df_stations.apply(
        lambda row: haversine(longitude, latitude, row['경도'], row['위도']), axis=1
    )

    closest_station = df_stations.loc[df_stations['distance'].idxmin()]

    station_code = closest_station['관측소 번호']
    station_name = closest_station['관측 지역']

    with col1:
        st.write(f"추정 위치는 **위도 {latitude}**, **경도 {longitude}**입니다.")
        st.write(f"가장 가까운 관측소는 **{station_name}** 입니다.")

    # 4. 관측소 번호에 따라 DataType 결정
    if station_code.startswith('DT') or station_code.startswith('IE'):
        data_type = 'tideObsRecent'
    else:
        data_type = 'buObsRecent'

    # 5. API 호출을 위한 URL 생성
    try:
        ServiceKey = st.secrets["ServiceKey"]
    except KeyError:
        st.error("ServiceKey가 설정되어 있지 않습니다. secrets.toml 파일을 확인하세요.")
        return

    api_url1 = f"http://www.khoa.go.kr/api/oceangrid/{data_type}/search.do"
    params1 = {
        'ServiceKey': ServiceKey,
        'ObsCode': station_code,
        'ResultType': 'json'
    }

    api_url2 = f"http://www.khoa.go.kr/api/oceangrid/romsTemp/search.do"
    params2 = {
        'ServiceKey': ServiceKey,
        'ObsLon': longitude,  # ObsLon은 longitude이어야 합니다.
        'ObsLat': latitude,   # ObsLat은 latitude이어야 합니다.
        'ResultType': 'json'
    }

    model_value = model_temp.predict_tomorrow(station_code, data_type)

    with col2:
        st.write("익일 수온 예상:")
        st.markdown(f"""
            <div style="text-align: center; font-size: 24px;">
                <strong>{model_value:.2f}°C</strong>
            </div>
            """, unsafe_allow_html=True)

    # 6. API 호출 및 데이터 가져오기
    with st.spinner('API 요청 중...'):
        # 첫 번째 API 호출
        response1 = requests.get(api_url1, params=params1)
        if response1.status_code == 200:
            data1 = response1.json()
            # 데이터 추출
            try:
                obs_data = data1['result']['data']
                obs_meta = data1['result']['meta']
            except KeyError:
                st.error("첫 번째 API 응답 형식이 예상과 다릅니다.")
                return

            # 7. 주요 관측 지표 표시
            st.subheader("주요 관측 지표")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("염분 (ppt)", obs_data.get("Salinity", "N/A"))
                st.metric("기온 (°C)", obs_data.get("air_temp", "N/A"))
            with col2:
                st.metric("수온 (°C)", obs_data.get("water_temp", "N/A"))
                st.metric("풍향 (m/s)", obs_data.get("wind_speed", "N/A"))
            with col3:
                st.metric("파고 (m)", obs_data.get("wave_height", "N/A"))
                st.metric("풍속 (cm/s)", obs_data.get("current_speed", "N/A"))

        else:
            st.error("첫 번째 API 요청에 실패했습니다.")
            st.write(f"HTTP 상태 코드: {response1.status_code}")
            return

        # 두 번째 API 호출 (72시간 수온 예측)
        response2 = requests.get(api_url2, params=params2)
        if response2.status_code == 200:
            data2 = response2.json()
            # st.subheader("일주일 수온 예측 데이터")
            # st.json(data2)
            # Temperature Forecast 라인 그래프 표시 (Plotly 사용)
            show_temperature_forecast_plotly(data2)
        else:
            st.error("두 번째 API 요청에 실패했습니다.")
            st.write(f"HTTP 상태 코드: {response2.status_code}")
            return


if __name__ == "__main__":
    show()