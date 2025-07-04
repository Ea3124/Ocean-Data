import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.express as px
import components.model.model as model
from pyngrok import ngrok

def haversine(lon1, lat1, lon2, lat2):
    from math import radians, sin, cos, sqrt, asin
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2.0)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2.0)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 지구의 반지름(km)
    return c * r

def load_species_constants(csv_path):
    """
    종별 수온 상수를 저장한 CSV 파일을 읽어와 딕셔너리로 반환
    """
    # CSV 파일 읽기
    df_constants = pd.read_csv(csv_path, header=None)
    
    # 첫 번째 블록 (종 이름, const1, const2, legend)
    species = df_constants.iloc[0].dropna().astype(str).tolist()
    const1 = df_constants.iloc[1].dropna().tolist()
    const2 = df_constants.iloc[2].tolist()
    legend = df_constants.iloc[3].dropna().tolist()
    
    # 종별 수온 상수 딕셔너리 생성
    species_constants = {}
    for i, specie in enumerate(species):
        species_constants[specie] = {
            'const1': pd.to_numeric(const1[i], errors='coerce') if i < len(const1) else None,
            'const2': pd.to_numeric(const2[i], errors='coerce') if i < len(const2) else None,
            'legend': legend[i] if i < len(legend) else ''
        }
    return species_constants

def process_temperature_data(json_data):
    data = json_data['result']['data']
    df = pd.DataFrame(data)
    df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
    df['datetime'] = pd.to_datetime(df['date'], format='%Y%m%d') + pd.to_timedelta(df['hour'].astype(int), unit='h')
    df.set_index('datetime', inplace=True)
    df.sort_index(inplace=True)
    df = df[['temperature']].dropna()
    return df

def show_temperature_forecast_plotly(json_data, species_constants):
    """
    72시간 수온 예측 데이터를 Plotly 라인 차트로 시각화
    """
    st.subheader("수온 변화 추이와 적정 수온 Line Graph")
    
    # 데이터 처리
    df = process_temperature_data(json_data)
    
    # 리샘플링 (3시간 간격)
    try:
        df_resampled = df.resample('3h').mean()
    except Exception as e:
        st.error(f"데이터 리샘플링 중 오류가 발생했습니다: {e}")
        return
    
    # 연간 수온 데이터 처리
    df = pd.read_csv('data/yearly_temperature.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df.set_index('Date', inplace=True)
    df_resampled = df
    
    # Streamlit 레이아웃: 선택 상자와 그래프를 나란히 배치
    col1, col2 = st.columns([1, 3])  # 선택 상자에 비해 그래프에 더 많은 공간 할당
    
    with col1:
        # 어종 카테고리와 종 데이터
        categories = {
            "어류": "fish",
            "패류": "shellfish",
            "해조류": "seaweed",
            "기타": "etc"
        }
        
        # Category selection
        category = st.selectbox("어종을 선택하세요:", list(categories.keys()))
        st.session_state.category = categories[category]
        
        # Species selection based on the chosen category
        if st.session_state.category == "fish":
            species_list = ["넙치", "조피볼락", "뱀장어", "무지개송어", "강도다리", "숭어", "향어", "돔류", "메기", "황복", "비단잉어"]
        elif st.session_state.category == "shellfish":
            species_list = ["참굴", "전복", "가리비"]
        elif st.session_state.category == "seaweed":
            species_list = ["곰피", "모자반", "청각", "넓미역", "미역", "김"]
        else:
            species_list = ["해삼양식", "큰징거미새우", "멍게", "흰다리새우"]
        
        # Species selection
        species = st.selectbox("종을 선택하세요:", species_list)
    
    with col2:
        # Plotly 라인 그래프 생성
        fig = px.line(df_resampled, x=df_resampled.index, y='temperature', markers=True)
        
        # 선택된 종에 대한 상수 값 가져오기
        constants = species_constants.get(species, {})
        const1 = constants.get('const1', None)
        const2 = constants.get('const2', None)
        legend = constants.get('legend', '')
        
        if const2 is None:
            y_min = min(df_resampled['temperature'].min() - 2, const1 - 2) # 적정 상수 수온이 안그려지는 것 수정
        else:
            y_min = min(df_resampled['temperature'].min() - 2, const1 - 2, const2 - 2)
        if const2 is None:
            y_max = max(df_resampled['temperature'].max() + 2, const1 + 2) # 적정 상수 수온이 안그려지는 것 수정
        else:
            y_max = max(df_resampled['temperature'].max() + 2, const1 + 2, const2 + 2)
        
        fig.update_layout(
            title={
                'text': "2024년 수온 변화 추이",
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

        # 상수 값이 존재하면 Plotly에 수평선 추가
        if const1 is not None:
            fig.add_hline(
                y=const1,
                line_dash="dash",
                line_color="red",
                annotation_text=f"{legend}: {const1}°C",
                annotation_position="bottom right"
            )
        
        if const2 is not None:
            fig.add_hline(
                y=const2,
                line_dash="dash",
                line_color="red",
                annotation_text=f"{legend}: {const2}°C",
                annotation_position="bottom right"
            )
        
        # Plotly 그래프 Streamlit에 표시
        st.plotly_chart(fig, use_container_width=True)

def show():
    st.title("Ocean Page")

    # st.columns()로 열 생성
    col1, col2, col3 = st.columns([0.7, 0.18, 0.12])

    # # 클라이언트의 IP 주소 가져오기 (현재 API 토큰 보존을 위해 위도 경도는 임의의 부산 내 위치로 지정)
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

    constants_csv_path = 'data/optimal_rearing_temperature.csv'
    species_constants = load_species_constants(constants_csv_path)

    # 2. 관측소 정보가 담긴 CSV 파일 불러오기
    try:
        df_stations = pd.read_csv('data/observation_stations.csv')
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

    model_value = model.predict_tomorrow(station_code, data_type)

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
            show_temperature_forecast_plotly(data2, species_constants)
        else:
            st.error("두 번째 API 요청에 실패했습니다.")
            st.write(f"HTTP 상태 코드: {response2.status_code}")
            return

if __name__ == "__main__":
    show()
    # ngrok 터널 연결 (개발 중단)
    # port = 8501
    # public_url = ngrok.connect(port).public_url
    # print(f" * ngrok 터널 URL: {public_url}")