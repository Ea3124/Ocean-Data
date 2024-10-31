import streamlit as st
import pandas as pd
from PIL import Image
import os

def show():
    # 데이터 로드
    data = pd.read_csv("data/wiki_data.csv")

    st.title("해양 생물 Wiki")

    # 데이터에서 각 종의 버튼 생성
    num_cols = 4
    for i in range(0, len(data), num_cols):
        cols = st.columns(num_cols)

        for j, row in enumerate(data.iloc[i:i + num_cols].itertuples()):
            species_name = getattr(row, "OC_BIOSPC_NM")
            species_image_path = f"data/images/{species_name}.jpg"

            with cols[j]:
                # 이미지 로드
                if os.path.exists(species_image_path):
                    image = Image.open(species_image_path)
                else:
                    image = Image.open("data/images/placeholder.jpg")

                # 이미지 표시
                st.image(image, use_column_width=True)

                # 클릭 시 상세 페이지로 이동
                if st.button(f"{species_name}", key=species_name, use_container_width=True):
                    st.session_state["selected_species"] = species_name
                    st.session_state["show_detail"] = True  # 상세 페이지 표시 상태 설정
                    st.rerun()  # 페이지 리프레시하여 상태 반영

    # CSS 스타일 추가
    st.markdown("""
    <style>
    /* 이미지 컨테이너에 테두리 추가 */
    [data-testid="stColumn"] {
        border: 2px solid #F0F2F6; 
        border-radius: 10px; /* 모서리 둥글게 */
        padding: 5px; /* 테두리와 이미지 간격 */
    }
    </style>
    """, unsafe_allow_html=True)

