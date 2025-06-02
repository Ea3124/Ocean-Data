# 🐟 양식등대
> **2024 부산 해양데이터 해커톤** <br/> **개발기간: 2024.10 ~ 2024.11**

<br>

## 🛳 프로젝트 소개
* 양식등대는 2024년 부산 해양데이터 해커톤 본선 진출 및 장려상 수상 작품으로, 해양과 빅데이터의 융합을 기반으로 해양의 디지털 전환과 기후 변화에 대응하는 서비스를 개발하였습니다.
* 저희 등대지기 팀의 출품작은 '**내 손 안에 들어오는 양식업 도우미**' 로, 양식업을 배우고자 하는 청년 어민들을 대상으로 한 **RAG 기반 챗봇 서비스 및 다양한 해양 데이터를 제공하는 웹 서비스**입니다. 

<br>

## 🎯 기술 스택
* **Backend**: <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" />
* **Frontend**: <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
* **ETC**: <img src="https://img.shields.io/badge/FAISS-007ACC?style=for-the-badge&logoColor=white" /> <img src="https://img.shields.io/badge/LangChain-5B21B6?style=for-the-badge&logoColor=white" />

<br>

## 🚣 등대지기 팀원 소개

|      김명석       |          정지윤         |      이승재       |          김민경         |
| :------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------: |
|   <img width="160px" src="https://avatars.githubusercontent.com/mangsgi" />    |                      <img width="160px" src="https://avatars.githubusercontent.com/enchantee00" />    |   <img width="160px" src="https://avatars.githubusercontent.com/Ea3124" />    |                      <img width="160px" src="https://avatars.githubusercontent.com/kim-minkyoung" />    |
|   UI/Design 개발   |  ML/DL 개발  |   UI/Design 개발   |  ML/DL 개발  |
|   [@mangsgi](https://github.com/mangsgi)   |    [@enchantee00](https://github.com/enchantee00)  |   [@Ea3124](https://github.com/Ea3124)   |    [@kim-minkyoung](https://github.com/kim-minkyoung)  |
| 부산대학교 정보컴퓨터공학부 3학년 | 부산대학교 정보컴퓨터공학부 3학년 | 부산대학교 정보컴퓨터공학부 3학년 | 부산대학교 정보컴퓨터공학부 3학년 |

---
<!-- ![0](https://github.com/user-attachments/assets/c38caf7c-2388-4a6d-9b9b-49991a2d1705) -->

<br>

## ⭐️ 탄생 배경

<div align="center">
  <img src="https://github.com/user-attachments/assets/bd86e101-993e-44ba-971d-26f0a9048a9a" alt="3" width=70%>
  <img src="https://github.com/user-attachments/assets/2bab15a6-dea8-41c9-b761-72808238bca4" alt="4" width=70%>
</div>
  
<!-- ![5](https://github.com/user-attachments/assets/cf823eff-978a-4249-8f92-e41cc1b524fe) -->

## ⭐️ 기능 1
<div align="center">
  <img src="https://github.com/user-attachments/assets/32cf576c-c83b-4c05-b315-255bfdf9e440" alt="7" width=70%>
</div>

## ⭐️ 기능 2
<div align="center">
  <img src="https://github.com/user-attachments/assets/3f966889-d7a9-4e05-a6f0-83a76270f1c0" alt="8" width=70%>
  <img src="https://github.com/user-attachments/assets/75e95064-1b58-4049-bb3d-4586b979dca9" alt="9" width=70%>
  <img src="https://github.com/user-attachments/assets/7201c98e-3340-45c2-9007-0805995a4c83" alt="10" width=70%>
</div>

## ⭐️ 기능 3
<div align="center">
  <img src="https://github.com/user-attachments/assets/d286b390-f0a4-4f91-8d41-1bdfbef36f8e" alt="12" width=70%>
  <img src="https://github.com/user-attachments/assets/3d257509-8c22-4720-8c91-ee6455c791ea" alt="13" width=70%>
</div>

<!--
## ⭐️ 사업화 방향
![19](https://github.com/user-attachments/assets/4d6a4027-1a83-48ca-bd98-e78df9b6f77d)
![20](https://github.com/user-attachments/assets/b7894583-0d1a-48b5-966c-026c1604c146)
-->

## ⭐️ 사회적 의의
<div align="center">
  <img src="https://github.com/user-attachments/assets/7bdd1c40-36dc-475d-a2ad-04b3e9dbc720" alt="22" width=70%>
</div>

---

<br>

## 📁 프로젝트 주요 구조

```bash
C:.
│  app.py                              # Streamlit 메인 앱 파일 (사이드 바 네비게이션 포함)
│  llm.py                              # LLM 관련 유틸리티 및 처리 함수
│  requirements.txt                    # 필요한 Python 패키지 목록
│  server.py                           # 백엔드 서버 실행 스크립트 (Flask API)
│
├─.streamlit
│      config.toml                     # Streamlit 설정
│      secrets.toml                    # API 키 및 IP 저장 (e.g., ServiceKey)
│
├─components # page 구성 파일
│  │  home.py                          # 홈 페이지 (Streamlit 랜딩 페이지)
│  │  chat.py                          # Chat 페이지 구성 (LLM 응답 등)
│  │  ocean.py                         # 실시간 수온 데이터 및 예측 시각화
│  │
│  ├─model
│  │      lstm_model_2012_2024.h5      # 학습된 수온 예측 LSTM 모델
│  │      model.py                     # 수온 예측 모델 로직
│  │
│  └─wiki
│      │  wiki.py                      # 위키 메인 페이지 (생물 목록 표시)
│      └─ wiki_detail.py               # 생물 상세 페이지 (종별 특성 표시)
|
├─data
│  │  daily_average_water_bui.csv     # 관측소 별 일평균 부이 수온 데이터 2024.10.06 ~ 2024.11.4
│  │  daily_average_water_temp.csv    # 관측소 별 일평균 수온 평균 데이터 2024.10.06 ~ 2024.11.4
│  │  observation_stations.csv        # 수온 관측소 정보
│  │  optimal_rearing_temperature.csv # 종별 적정 사육 수온
│  │  question.csv                    # 챗봇 모델 파인튜닝을 위한 사용자 질문 데이터
│  │  wiki_data.csv                   # 해양 생물 종 정보 데이터
│  │  yearly_temperature.csv          # 2024년 특정 일별 수온 데이터
│  │
│  └─images                           # Wiki 페이지에 사용되는 이미지 모음
│
└─faiss # FAISS DB
    ├─etc                              # 기타 생물 종에 대한 벡터 인덱스
    │      *.pkl, *.index              
    │
    ├─fish                             # 어류 관련 벡터 인덱스
    │      *.pkl, *.index
    │
    ├─seaweed                          # 해조류 관련 벡터 인덱스
    │      *.pkl, *.index
    │
    └─shellfish                        # 패류 관련 벡터 인덱스
           *.pkl, *.index

```

<br>

## 🛠️ 설치 및 실행 가이드
### 1. 리포지토리 클론
```bash
git clone https://github.com/enchantee00/Ocean-Data.git
```

### 2. 의존성 설치 (가상환경 사용 추천)
* 파이썬 버전 3.9.21
* CUDA 버전 11.8
```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정
* `.streamlit` 폴더 내 `secrets.toml` 파일을 생성한 후 아래와 같이 설정합니다:
```bash
# 반드시 KEY는 문자열로 지정 
BACKEND_IP="<your-backend-ip>"
ServiceKey="<your-service-key>" # 해양수산부 바다누리 해양정보서비스 API
LOCATION_API_KEY="<your-api-key>" # Google Geolocation API
```

### 4. 페이지 실행
```bash
# Flask 서버 실행
python server.py
# 웹 페이지 실행
streamlit run app.py
```

<br>

## 📈 향후 계획
* **RAG 모델 경량화 및 성능 향상**을 통해 언제 어디서나 사용가능하도록 로컬에 설치가능한 챗봇 구현
* **API 제한이 없는 GPS**를 통한 제한없는 정보 불러오기
  * _현재 Geolocation API 제한으로 인해 위도와 경도를 고정하고 API 사용은 주석 처리한 상태_
* **깃허브 Action**를 통한 관측소 수온 정보 실시간 업데이트 및 **CI/CD 구현**
  * _현재는 프로젝트 당시를 기준으로 관측소별 데이터가 존재_
