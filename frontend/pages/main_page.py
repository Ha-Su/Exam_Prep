import streamlit as st
from style import main_style
from pages import page_config
from pages.session_manager import initialize_session, get_user_module
from pathlib import Path
from PIL import Image
import sys
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from leaderboard.leaderboard import load_leaderboard

initialize_session()

ROOT = Path(__file__).parent.parent 

def generate_leaderboard_html() -> str:
    leaderboard = load_leaderboard()

    html = f"""
                <div class="custom-metric-wrapper">
                <div class="metric-container">
                    <div class="metric-label">{leaderboard[0]["name"]}</div>
                    <div class="metric-value">{leaderboard[0]["grade"]}</div>
                    <div class="metric-delta">Score : {leaderboard[0]["total_score"]}/{leaderboard[0]["total_max_score"]}</div>
                    <div class="metric-label">-------------------</div>
                    <div class="metric-label">{leaderboard[1]["name"]}</div>
                    <div class="metric-value">{leaderboard[1]["grade"]}</div>
                    <div class="metric-delta">Score : {leaderboard[1]["total_score"]}/{leaderboard[1]["total_max_score"]}</div>
                    <div class="metric-label">-------------------</div>
                    <div class="metric-label">{leaderboard[2]["name"]}</div>
                    <div class="metric-value">{leaderboard[2]["grade"]}</div>
                    <div class="metric-delta">Score : {leaderboard[2]["total_score"]}/{leaderboard[2]["total_max_score"]}</div>
                </div>
                </div>
                """
    return html

st.markdown(main_style.HOME_BUTTON, unsafe_allow_html=True)

if st.button(label="🏠", key="home-button", type="primary"):
    st.switch_page("app.py")

# Get user's module from their session
user_module_name, user_module_ab = get_user_module()
main_title = main_style.make_main_title(user_module_name)

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

latest_private_score, leaderboard_top3 = st.columns(2, gap='large', vertical_alignment="center")

with latest_private_score:
    if st.session_state.get("exam_done", False):
        st.markdown(main_style.METRIC_CSS, unsafe_allow_html=True)
        value = st.session_state.get("latest_grade", "No score")
        delta = st.session_state.get("latest_score", "No score")
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
        if value != "N/A" and 1 <= float(value) <= 2:
            gif = ROOT / "gifs" / "bear_success.gif"
        elif value != "N/A" and 2.3 <= float(value) <= 3.7:
            gif = ROOT / "gifs" / "nice.gif"
        else:
            gif = ROOT / "gifs" / "trash.gif"
        st.image(gif)
    else:
        st.markdown(main_style.TEXT_NO_EXAM, unsafe_allow_html=True)
        no_exam_gif = ROOT / "gifs" / "bear_nosucc.gif"
        st.image(no_exam_gif)

with leaderboard_top3:

    st.markdown(main_style.METRIC_CSS, unsafe_allow_html=True)
    html = generate_leaderboard_html()
    st.markdown(html, unsafe_allow_html=True)
