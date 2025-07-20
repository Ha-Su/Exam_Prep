import streamlit as st
from pages import page_config

if st.button(label="Go Back To Landing Page", icon="◀️"):
    st.switch_page("app.py")

st.title(page_config.module_name)

if st.button(label="See the study materials", icon="📖"):
    st.switch_page("pages/study_page.py")

if st.button(label="Exams Prep", icon="📣"):
    st.switch_page("pages/frontend.py")