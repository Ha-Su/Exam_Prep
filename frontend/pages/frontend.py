import streamlit as st
import re
import pathlib
import glob
import json
import time
import sys
from streamlit_js_eval import streamlit_js_eval
from streamlit.components.v1 import html
from streamlit_autorefresh import st_autorefresh
import google.generativeai as genai

PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from pages import page_config
from pages.session_manager import (
    initialize_session, get_user_api_key, set_user_api_key, get_user_module, reset_exam_state,
    store_grading_result, get_grading_result, has_grading_result,
    add_to_total_score, get_total_scores, reset_total_scores,
    store_student_answer, get_student_answer, get_user_name, set_user_name
)
from leaderboard.leaderboard import add_new_entry
from dotenv import load_dotenv
import os

# Initialize session state for this user
initialize_session()

# ──────────────────────────────────────────────────────────────────────────────
#  Configurations
# ──────────────────────────────────────────────────────────────────────────────
MODEL = page_config.DEFAULT_MODEL

# Get user's module from their session
user_module_name, user_module_ab = get_user_module()
MODULE = user_module_name

PAGES_DIR = pathlib.Path(__file__).resolve().parent               # …/Exam_Prep/frontend/pages
PROJECT_ROOT = PAGES_DIR.parent.parent                            # …/Exam_Prep
QUESTIONS_FOLDER = PROJECT_ROOT / "questions_md"

# Get constants from config
SECONDS_BETWEEN_CALLS = page_config.SECONDS_BETWEEN_CALLS
EXAM_TIME = page_config.EXAM_TIME

# Scores are now managed in session state - no global variables needed

def check_key_validity() -> bool:
    user_key = get_user_api_key()
    if not user_key.strip():
        return False
    
    # Configure genai with user's specific key
    genai.configure(api_key=user_key)
    model = genai.GenerativeModel(MODEL)
    try:
        response = model.generate_content("Hello")
        return True
    except Exception as e:
        return False

def note(final_score):
    grade_map = [
        (95, "1.0"),
        (90, "1.3"),
        (85, "1.7"),
        (80, "2.0"),
        (75, "2.3"),
        (70, "2.7"),
        (65, "3.0"),
        (60, "3.3"),
        (55, "3.7"),
        (50, "4.0"),
    ]
    for score, grade in grade_map:
        if final_score >= score:
            return grade
    return "5.0"


# Load QnA
def load_qna(folder_path):
    p = pathlib.Path(folder_path)
    if not p.is_file:
        raise FileNotFoundError(f"{folder_path} not found")
    return json.loads(p.read_text(encoding="utf-8"))


# Call the LLM for grading given specific prompt for grading
def grade_with_llm(question: str, correct: str, student: str, scoring: dict) -> str:
    
    # Build scoring components description
    components_str = "\n".join(
        f"- {comp['description']} ({comp.get('score', 1)} point(s))" 
        for comp in scoring.get("components", [])
    )
    
    max_score = scoring.get("max_score", 1)
    
    prompt = f"""
        You are an {MODULE} professor grading a short-answer exam. For this question:

        1. **Scoring Rubric** (Total: {max_score} points):
        {components_str}

        2. **Grading Rules**:
           - Award FULL credit for a component if the concept is correctly explained
           - Award PARTIAL credit (50-100%) if partially correct but missing key aspects
           - Be LENIENT - accept equivalent phrasings and alternative valid examples
           - Focus on conceptual understanding rather than exact wording

        3. **Output Format**:
            ```
            Grade: <score>/{max_score}

            Given Answer: 
            {student!r}

            Feedback:
            - [Component 1]: <feedback> (Score: <component_score>/<max_component_score>)
            - [Component 2]: <feedback> (Score: <component_score>/<max_component_score>)
            ...
            ```

        4. **Examples**:
           Good: 
             - "Correctly explained memory limit (1/1)"
             - "Good menu example but missed CLI application (0.5/1)"
           Bad:
             - "Wrong answer" (too vague)
             - "Missing key point" (not helpful)

        ---
        **Question**: {question!r}
        **Model Answer**: {correct!r}
        **Student's Answer**: {student!r}
        """.strip()

    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)
    text = response.text.strip()

    # Extract score and add to session totals
    m = re.search(r"Grade:\s*([\d.]+)\s*/\s*([\d.]+)", text)
    if m:
        score = float(m.group(1))
        add_to_total_score(score, max_score)

    time.sleep(SECONDS_BETWEEN_CALLS)
    return text

# ──────────────────────────────────────────────────────────────────────────────
#  UI Shenanigans
# ──────────────────────────────────────────────────────────────────────────────
# if "api_key" not in st.session_state:
#     st.session_state.api_key = page_config.API_KEY
# if "start_time" not in st.session_state:
#     st.session_state.start_time = None
# if "auto_submit" not in st.session_state:
#     st.session_state.auto_submit = False
# if "manual_submit" not in st.session_state:
#     st.session_state.manual_submit = False
# if "grading_done" not in st.session_state:
#     st.session_state.grading_done = False

api_key_help = f"Use the default API key : {os.getenv('GOOGLE_API_KEY')}"

disabled = st.session_state.manual_submit

#--------------------- Back & Retake button -------------------------------------------------
exam_in_progress = st.session_state.start_time is not None 

back_col, retake_col = st.columns(2)

with back_col:
    if st.button(label=f"Study: {user_module_name}", icon="◀️"):
        # Stop the timer when navigating away
        stop_timer_js = """
        <script>
        if (window.stopExamTimer) {
            window.stopExamTimer();
        }
        </script>
        """
        html(stop_timer_js, height=0)
        st.session_state.new_score = False
        st.switch_page("pages/main_page.py")

with retake_col:
    if st.button("Retake Exam", type="primary", icon="🔁", use_container_width=True):
        # Stop the timer before resetting
        stop_timer_js = """
        <script>
        if (window.stopExamTimer) {
            window.stopExamTimer();
        }
        </script>
        """
        html(stop_timer_js, height=0)
        reset_exam_state()
        st.rerun()

# Load questions
questions = load_qna(f"{QUESTIONS_FOLDER}/updated_QnA_pairs.json")

#--------------------- Exam Introduction -------------------------------------------------
if st.session_state.start_time is None :
    st.title("📝 MOCK EXAM 💯")
    st.divider()
    KEY_IS_INVALID = True
    #================================= API Key configuration =====================================================
    with st.form("api"):
        form_user_name = st.text_input("**Enter your name :**", value=get_user_name())
        st.divider()
        st.markdown("**Get your Gemini API key** [here](%s)." % page_config.API_KEY_URL) 
        USER_API_KEY = st.text_input(
            "**Enter API Key :**", 
            placeholder="API Key Please", 
            value=get_user_api_key(),
            help=api_key_help
        )
        col1,col2,col3 = st.columns(3)
        with col2:
            check_valid = st.form_submit_button("Set Key", use_container_width=True)
            if check_valid:
                set_user_api_key(USER_API_KEY)
                set_user_name(form_user_name) 
                genai.configure(api_key=USER_API_KEY)
    if check_valid:
        with st.spinner("Checking validity…"):
            if check_key_validity():
                st.success(f"✅ Key is valid!")
                KEY_IS_INVALID = False
            else:
                st.warning("⚠️ Key is invalid!")
                KEY_IS_INVALID = True

    #================================= Exam Intro ==================================================
    st.markdown(f"""
                **Exam Instructions :**

                - Duration: **90 minutes**
                - Questions will appear once you press **Start Exam**.
                - The timer will begin immediately and cannot be paused.
                - **DO NOT** Refresh / Reload the page.
                """)  
    def start_exam():
        st.session_state.start_time = time.time()

    if st.button("Start Exam", type="primary", use_container_width=True, disabled=KEY_IS_INVALID, on_click=start_exam):
        st.session_state.start_time = time.time()
    st.stop()

elapsed = time.time() - st.session_state.start_time
remaining_seconds = max(0, EXAM_TIME*60 - int(elapsed))
remaining_minutes = remaining_seconds // 60
if remaining_seconds == 0:
    st.session_state.auto_submit = True

#------------------------------------------- Timer -------------------------------------------------
def start_js_timer(duration_seconds):
    js = f"""
    <script>
    // Global variables
    window.examTimerInterval = null;
    window.timerShouldStop = false;
    
    function startTimer(duration) {{
        let timer = duration;
        const timerElement = parent.document.getElementById('timer-display');
        
        function updateTimer() {{
            // Check if timer should be stopped (via session state changes)
            if (window.timerShouldStop) {{
                clearInterval(window.examTimerInterval);
                window.examTimerInterval = null;
                
                if (timerElement) {{
                    timerElement.innerText = `⏱ Timer Stopped - Exam Submitted`;
                    timerElement.style.color = '#28a745'; // Green color
                }}
                return;
            }}
            
            const minutes = Math.floor(timer / 60);
            const seconds = timer % 60;
            
            if (timerElement) {{
                timerElement.innerText = `⏱ Time Remaining: ${{minutes}}m ${{seconds}}s`;
            }}
            
            if (--timer < 0) {{
                clearInterval(window.examTimerInterval);
                window.examTimerInterval = null;
                
                const rEvent = new KeyboardEvent('keydown', {{
                    key: 'r',
                    code: 'KeyR',
                    keyCode: 82,
                    which: 82,
                    bubbles: true,
                    cancelable: true
                }});

                parent.document.dispatchEvent(rEvent);
            }}
        }}
        
        // Initial update
        updateTimer();
        
        // Store interval ID globally
        window.examTimerInterval = setInterval(updateTimer, 1000);
    }}
    
    // Global function to stop the timer
    window.stopExamTimer = function() {{
        window.timerShouldStop = true;
    }}
    
    // Start the timer with the specified duration
    startTimer({duration_seconds});
    </script>
    """
    return js

timer_slot = st.empty
if not disabled and st.session_state.start_time:
    # Create a container for the timer display
    st.sidebar.markdown('<div id="timer-display"></div>', unsafe_allow_html=True)
    
    # Start the JavaScript timer
    html(start_js_timer(remaining_seconds), height=0)

#--------------------------- Load questions -------------------------------------------
for idx, qna_pair in enumerate(questions):
    st.markdown(f"**{idx + 1} )**")
    st.markdown(f"**🇩🇪 : {qna_pair['question_de']}**")  # German questions
    st.markdown(f"**🇬🇧 : {qna_pair['question_en']}**")  # English questions

    st.text_area("Answer : ", key=f"ans_{idx}", height=100, disabled=disabled)
    st.divider()

#--------------------------- Time is up / Submit Button -------------------------------------------------
if st.session_state.auto_submit or st.button("Submit", type="primary", disabled=st.session_state.manual_submit):
    if st.session_state.auto_submit:
        st.warning("⏳ Time is up! Your answers have been submitted automatically.")
    else:
        # Manual submission - stop the timer using HTML injection
        stop_timer_js = """
        <script>
        if (window.stopExamTimer) {
            window.stopExamTimer();
        }
        </script>
        """
        html(stop_timer_js, height=0)
        
    st.session_state.manual_submit = True
    st.session_state.new_score = True

if st.session_state.manual_submit:
    st.header("Grades")
    
    # Only reset and grade if not already done
    if not st.session_state.grading_done:
        # Reset totals before grading
        reset_total_scores()
        
        # Store all answers first
        for idx, pair in enumerate(questions):
            student_ans = st.session_state[f"ans_{idx}"].strip()
            store_student_answer(idx, student_ans)
        
        # Grade all questions
        for idx, pair in enumerate(questions):
            student_ans = get_student_answer(idx)
            if not student_ans:
                # Store empty result for empty answers
                store_grading_result(idx, f"❌ **Q{idx+1}: No answer provided.**")
                add_to_total_score(0, pair.get("scoring", {"max_score": 1})["max_score"])
                continue
            
            with st.spinner(f"Grading Q{idx + 1}..."):
                genai.configure(api_key=get_user_api_key())
                result = grade_with_llm(
                    question=pair["question_en"],
                    correct=pair["answer"],
                    student=student_ans,
                    scoring=pair.get("scoring", {"max_score": 1, "components": []})
                )
                # Store the grading result
                store_grading_result(idx, result)
        
        # Mark grading as complete
        st.session_state.grading_done = True
    
    # Display all stored results (whether just graded or from previous session)
    for idx, pair in enumerate(questions):
        if has_grading_result(idx):
            result = get_grading_result(idx)
            st.markdown(f"**Q{idx + 1} Grade & Feedback:**  \n{result}")
            
            expander = st.expander("See actual answer")
            expander.write(f"**Q : {pair['question_en']}**")
            expander.divider()
            expander.write(f"A : {pair['answer']}")
            
            # Show student's answer too
            student_ans = get_student_answer(idx)
            if student_ans:
                expander.write(f"**Your Answer:** {student_ans}")
            
            st.divider()
    
    #--------------------------- Grading Done -----------------------------------------------------
    # Calculate final grade using session state scores
    total_score, total_max_score = get_total_scores()
    
    if total_max_score == 0:
        final_grade = 5.0
    else:
        score_percentage = (total_score / total_max_score) * 100
        final_grade = note(score_percentage)
    
    # Store results in user's session
    st.session_state.latest_grade = final_grade
    st.session_state.latest_score = f"Score: {total_score}/{total_max_score}"
    
    #------------------------ Final Sidebar and Grades ------------------------------------------------
    st.success(f"🏆 **Total Score: {total_score:.1f} / {total_max_score:.1f}**")
    st.success(f"💯 **Note :** {final_grade}")
    new_entry = {
        "name": get_user_name(),
        "grade": final_grade,
        "total_score": total_score,
        "total_max_score": total_max_score
        }
    add_new_entry(new_entry)

    if st.session_state.grading_done:
        st.session_state.exam_done = True
