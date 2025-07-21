import streamlit as st
from style import main_style
from pages import page_config

st.markdown(main_style.HOME_BUTTON, unsafe_allow_html=True)

if st.button(label="🏠", key="home-button", type="primary"):
    st.switch_page("app.py")

main_title = main_style.make_main_title(page_config.module_name)

st.markdown(main_title, unsafe_allow_html=True)

column1, column2 = st.columns(2, gap="large")

with column1:
    st.markdown(main_style.STUDY_BUTTON, unsafe_allow_html=True)
    if st.button(label="See the study materials", icon="📖", use_container_width=True, key="study-button", type="secondary"):
        st.switch_page("pages/study_page.py")
with column2:
    st.markdown(main_style.EXAM_BUTTON, unsafe_allow_html=True)
    if st.button(label="Mock Exams", icon="📣", use_container_width=True, key="exam-button", type="tertiary"):
        st.switch_page("pages/frontend.py")
    if page_config.EXAM_DONE:
        st.metric(page_config.LATEST_SCORE, page_config.LATEST_GRADE, border=True)
