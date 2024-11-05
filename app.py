import streamlit as st
from pages import home, chat, ocean
from pages.wiki import wiki
from pages.wiki import wiki_detail

# 사이드바에 Navigation 섹션만 표시
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a Page", ["Home", "Wiki", "Chat", "Ocean"])

# 선택한 페이지에 따라 해당 페이지의 콘텐츠 보여주기
if page == "Home":
    home.show()
elif page == "Wiki":
    # Wiki 페이지 선택 시 selected_species 여부에 따라 다른 페이지 렌더링
    if "selected_species" in st.session_state:
        wiki_detail.show()
    else:
        wiki.show()
elif page == "Chat":
    chat.show()
elif page == "Ocean":
    ocean.show()
