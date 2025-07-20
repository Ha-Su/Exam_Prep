import streamlit as st
from pages import page_config
from style import landing_style
import streamlit as st

MODULE_MAP = {
    "Human Computer Interaction": "HCI",
    "Serious Games": "SG",
}


def get_module(module: str) -> str | None:
    if module in MODULE_MAP:
        return MODULE_MAP[module]
    return None


st.markdown(landing_style.TITLE_LANDING, unsafe_allow_html=True)

st.markdown(landing_style.MARKDOWN_LANDING, unsafe_allow_html=True)

choice = st.selectbox(label=" ", options=["Human Computer Interaction", "Serious Games"])

st.markdown(landing_style.BUTTON_LANDING, unsafe_allow_html=True)

if st.button("Let's Go!", icon="🚀"):
    if choice is not None:
        page_config.module_name = choice
        page_config.module_name_ab = get_module(choice)
        st.switch_page("pages/main_page.py")
    else:
        st.warning("Please choose the module you want to study before clicking the button")
