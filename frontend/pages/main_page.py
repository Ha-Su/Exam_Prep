import streamlit as st
from style import main_style
from pages import page_config

st.markdown(main_style.HOME_BUTTON, unsafe_allow_html=True)

if st.button(label="🏠", key="home-button", type="primary"):
    st.switch_page("app.py")

main_title = main_style.make_main_title(page_config.module_name)

st.markdown(main_title, unsafe_allow_html=True)

column1, column2 = st.columns(2, gap="large", vertical_alignment="center")

with column1:
    st.markdown(main_style.STUDY_BUTTON, unsafe_allow_html=True)
    if st.button(label="See the study materials", icon="📖", use_container_width=True, key="study-button",
                 type="secondary"):
        st.switch_page("pages/study_page.py")
with column2:
    st.markdown(main_style.EXAM_BUTTON, unsafe_allow_html=True)
    if st.button(label="Mock Exams", icon="📣", use_container_width=True, key="exam-button", type="tertiary"):
        st.switch_page("pages/frontend.py")

column3, column4, column5 = st.columns(3, gap=None, vertical_alignment="center")

with column4:
    if page_config.EXAM_DONE:
        st.markdown(main_style.METRIC_CSS, unsafe_allow_html=True)
        value = page_config.LATEST_GRADE
        delta = page_config.LATEST_SCORE
        html = f"""
                <div class="custom-metric-wrapper">
                  <div class="metric-container">
                    <div class="metric-label">Latest Grade</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-delta">{delta}</div>
                  </div>
                </div>
                """
        st.markdown(html, unsafe_allow_html=True)
        if 1 <= float(value) <= 2:
            gif = "frontend/gifs/bear_success.gif"
        elif 2.3 <= float(value) <= 3.7:
            gif = "frontend/gifs/nice.gif"
        else:
            gif = "frontend/gifs/trash.gif"
        st.image(gif)
    else:
        st.markdown(main_style.TEXT_NO_EXAM, unsafe_allow_html=True)
        st.image(image="frontend/gifs/bear_nosucc.gif")
