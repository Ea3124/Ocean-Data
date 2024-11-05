import streamlit as st
from pages import home, wiki, chat, ocean

# 사이드바에 Navigation 섹션만 표시
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a Page", ["Home", "Wiki", "Chat", "Ocean"])

# 선택한 페이지에 따라 해당 페이지의 콘텐츠 보여주기
if page == "Home":
    home.show()
elif page == "Wiki":
    wiki.show()
elif page == "Chat":
    chat.show()
elif page == "Ocean":
    ocean.show()