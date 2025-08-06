from pages import page_config
from pages.session_manager import initialize_session, set_user_module
from style import landing_style
import streamlit as st

# Initialize session state for this user
initialize_session()


st.markdown(landing_style.TITLE_LANDING, unsafe_allow_html=True)

st.markdown(landing_style.MARKDOWN_LANDING, unsafe_allow_html=True)

choice = st.selectbox(label=" ", options=["Human Computer Interaction", "Serious Games"])

st.markdown(landing_style.BUTTON_LANDING, unsafe_allow_html=True)

if st.button("Let's Go!", icon="🚀"):
    if choice is not None:
        # Store user's module choice in their session
        module_ab = page_config.get_module_abbreviation(choice)
        set_user_module(choice, module_ab)
        st.switch_page("pages/main_page.py")
    else:
        st.warning("Please choose the module you want to study before clicking the button")
