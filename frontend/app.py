import streamlit as st
from pages import page_config


st.title("Welcome!")

st.markdown("Please choose the module you want to study and click the button\n")

choice = st.selectbox(label="Module Selection", options=["Human Computer Interaction", "Serious Games"])

if st.button(label="Let's Go!", icon="🚀"):
    if choice is not None:
        page_config.module_name = choice
        st.switch_page("pages/main_page.py")
    else:
        st.markdown(label="Please choose the module you want to study before clicking the button\n")
