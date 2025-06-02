import streamlit as st
import pandas as pd

def show():
    # 데이터 로드
    data = pd.read_csv("data/wiki_data.csv")

    # 선택된 종 데이터 가져오기
    species_name = st.session_state.get("selected_species", "")
    species_row = data[data["OC_BIOSPC_NM"] == species_name].iloc[0]

    # 페이지 상단에 뒤로 가기 버튼 추가
    if st.button("← 뒤로 가기"):
        st.session_state.pop("selected_species")
        st.rerun()
        return  # 함수 종료하여 페이지 새로고침

    # 종 정보 보여주기
    st.header(f"{species_name} 상세 정보")
    
    for col, display_name in column_mappings.items():
        value = species_row[col]
        if pd.notna(value):
            st.write(f"**{display_name}:** {value}")


# Column mappings
column_mappings = {
    "OC_BIOSPC_NM": "해양 생물 종명",
    "OC_BLY_NM": "해양 생물 학명",
    "LVB_INFO": "생물 정보",
    "STLE_INFO": "형태 정보",
    "ECGY_INFO": "생태 정보",
    "BRD_PLACE_RQSTE_CN": "사육 장소 요건 내용",
    "SPAWN_ERA_CN": "산란 시기 내용",
    "SPAWN_WTEM": "산란 수온",
    "HTGHG_WTEM": "부화 수온",
    "BUDD_GRWH_WTEM": "발아 성장 수온",
    "DRMNCY_WTEM": "휴면 수온",
    "RELS_ERA_CN": "방출 시기 내용",
    "RELS_WTEM": "방출 수온",
    "SEEDCOL_ERA_CN": "채묘 시기 내용",
    "SEEDCOL_WTEM": "채묘 수온",
    "TRNPLT_ERA_CN": "이식 시기 내용",
    "TRNPLT_WTEM": "이식 수온",
    "BRD_WTEM": "사육 수온",
    "PSTV_WTEM": "양성 수온",
    "HIGHWTPR_LIMIT_CN": "고수온 한계 내용",
    "LWWTPR_LIMIT_CN": "저수온 한계 내용",
    "LWSLN_LIMIT_CN": "저염분 한계 내용",
    "SLNTY_VARTION_CN": "염분 변화 내용",
    "MIM_DOXN": "최소 용존 산소량",
    "HIGHWTPR_TKACT_MTH_CN": "고수온 조치 방법 내용",
    "LWWTPR_TKACT_MTH_CN": "저수온 조치 방법 내용",
    "CP_TKACT_MTH_CN": "냉수대 조치 방법 내용",
    "LWSLN_TKACT_MTH_CN": "저염분 조치 방법 내용",
    "PARAST_DISS_NM": "기생충 질병 명",
    "BCLS_DISS_NM": "세균 질병 명",
    "CPTVR_DISS_NM": "바이러스 질병 명",
    "ETC_DISS_NM": "기타 질병 명",
    "MAIN_DISS_NM": "주요 질병 명",
    "RDTD_AP_TKACT_MTH_CN": "적조 출현 조치 방법 내용",
    "RDTD_ATENT_TKACT_MTH_CN": "적조 주의 조치 방법 내용",
    "RDTD_ALRT_TKACT_MTH_CN": "적조 경보 조치 방법 내용",
    "RDTD_SRS_TKACT_MTH_CN": "적조 심각 조치 방법 내용",
    "RDTD_RELIS_TKACT_MTH_CN": "적조 해제 조치 방법 내용"
}
