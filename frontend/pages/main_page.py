import streamlit as st
from pages import page_config

MODULE_MAP = {
    "Human Computer Interaction": "HCI",
    "Serious Games": "SG",
}

def get_module(module: str) -> str | None:
    if module in MODULE_MAP:
        return MODULE_MAP[module]
    if module in MODULE_MAP.values():
        return module
    return None

if st.button(label="Go Back To Landing Page", icon="◀️"):
    st.switch_page("app.py")

module_name = page_config.module_name
st.title(module_name)

if st.button(label="See the study materials", icon="📖"):
    st.switch_page("pages/study_page.py")

if st.button(label="Mock Exams", icon="📣"):
    st.switch_page("pages/frontend.py")

page_config.module_name = get_module(module_name)
