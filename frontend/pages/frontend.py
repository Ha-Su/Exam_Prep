import streamlit as st
import re
import pathlib
import glob
import json
import time
from streamlit_js_eval import streamlit_js_eval
from streamlit.components.v1 import html
from streamlit_autorefresh import st_autorefresh
import google.generativeai as genai
from pages import page_config
from dotenv import load_dotenv
import os

# ──────────────────────────────────────────────────────────────────────────────
#  Configurations
# ──────────────────────────────────────────────────────────────────────────────
MODEL = os.getenv("MODEL", "gemini-2.5-flash-lite-preview-06-17")

MODULE = page_config.module_name

PAGES_DIR = pathlib.Path(__file__).resolve().parent               # …/Exam_Prep/frontend/pages
PROJECT_ROOT = PAGES_DIR.parent.parent                            # …/Exam_Prep
QUESTIONS_FOLDER = PROJECT_ROOT / "questions_md"

# Rate limit: max 15 calls per minute
SECONDS_BETWEEN_CALLS = 60.0 / 15.0
EXAM_TIME = 0.1 #in minutes

total_score = 0.0
total_max_score = 0.0
final_grade = 0.0

def check_key_validity() -> bool:
    if not st.session_state.api_key.strip():
        return False
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
def grade_with_llm(question: str, correct: str, student: str) -> str:
    global total_score, total_max_score

    prompt = f"""
        You are an {MODULE} professor grading a short-answer exam.  For each question:

        1. **Determine the maximum score** from the question text:
            - “Name N items” → 0.5 pt each → max = N × 0.5 (e.g., *Name 2 parts of…*)
            - “Define M items” → 1 pt each → max = M
            - “Give examples of X things” → 1 pt each → max = X
            - Mixed tasks (definition + example, etc.) → add the relevant point values.  
                • Example: *Define an item (1 pt) and give an example (1 pt)* → max = 2 pts.  
                • Example: *Name 4 laws and define 2* → naming = 4 × 0.5 = 2 pts; definitions = 2 pts → total = 4 pts.

        2. **Grade** the student’s answer out of the calculated maximum.  
            - Full credit may be given if the answer captures the concept in the model answer.  
            - If a student lists more than requested, cap their credit at the maximum.

        3.  **Explain** briefly what's missing or incorrect.

        4. **Format your output exactly like this** (omit lines that don’t apply to the question):
            ```
            Grade: <score>/<max>

            Your Answer:\n
            {student!r}

            Feedback:
            - Feedback <what is good or what is missing from the given answer> on one question point<naming, defining, example, etc> **Score/max**(refer to point 1)
            - Feedback <what is good or what is missing from the given answer> on another question point<naming, defining, example, etc>, !!IF APPLICABLE!!, **Score/max**(refer to point 1)
            - More feedbacks if necessary
            ```
            Only include the lines for parts the question actually asks.
            Output should be in text format!
            If the student leaves a part blank, award 0 for that part but keep the maximum.

        5. GRADING EXAMPLE :
            ```
            Question 1 :
            Name 4 parts of XYZ, give explanation for 2 of them

            Given/Student's answer :
            Parts of XYZ are X, Y, Z and A. X is x and Y is y

            Output :
            Grade: 3/4

            Feedback:
            - You named the parts correctly (2/2)
            - Definition for X is correct, but the definition of Y is missing something <explain what is missing> (1/2)

            Question 2 :
            Name 2 type of ABC, give explanation for 2 of them and lastly give an example of their implementations.

            Given/Student's answer :
            Parts of ABC are A and B. A is a and B is b. Example of A is X.

            Output :
            Grade: 4/5

            Your Answer:\n
            {student!r}

            Feedback:
            - You named the parts correctly (1/1)
            - Definition for A is correct, B is a little bit of the mark but still accepted <explain what is missing> (2/2)
            - Example of A is correct, but B is missing (1/2)            

            ```

        Here is the question, key, and given answer:

        Question:
        {question!r}

        Model Answer:
        {correct!r}

        Given's Answer:
        {student!r}
        """.strip()

    model = genai.GenerativeModel(MODEL)
    response = model.generate_content(prompt)
    text = response.text.strip()

    m = re.search(r"Grade:\s*([\d.]+)\s*/\s*([\d.]+)", text)
    if m:
        score = float(m.group(1))
        max_score = float(m.group(2))
        total_score += score
        total_max_score += max_score

    time.sleep(SECONDS_BETWEEN_CALLS)
    return text


# ──────────────────────────────────────────────────────────────────────────────
#  UI Shenanigans
# ──────────────────────────────────────────────────────────────────────────────
if "api_key" not in st.session_state:
    st.session_state.api_key = page_config.API_KEY
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "auto_submit" not in st.session_state:
    st.session_state.auto_submit = False
if "manual_submit" not in st.session_state:
    st.session_state.manual_submit = False
if "grading_done" not in st.session_state:
    st.session_state.grading_done = False

api_key_help = f"Use the default API key : {os.getenv("GOOGLE_API_KEY")}"

disabled = st.session_state.manual_submit

#--------------------- Back & Retake button -------------------------------------------------
exam_in_progress = st.session_state.start_time is not None 
study_disabled     = exam_in_progress and not st.session_state.grading_done

back_col, retake_col = st.columns(2)

with back_col:
    if st.button(label=f"Study: {page_config.module_name}", icon="◀️"):
        st.switch_page("pages/main_page.py")

with retake_col:
    if st.button("Retake Exam", type="primary", icon="🔁", use_container_width=True):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")

# Load questions
questions = load_qna(f"{QUESTIONS_FOLDER}/updated_QnA_pairs.json")

#--------------------- Exam Introduction -------------------------------------------------
if st.session_state.start_time is None :
    st.title("📝 MOCK EXAM 💯")
    st.divider()
    KEY_IS_INVALID = True
    #================================= API Key configuration =====================================================
    with st.form("api"):
        st.markdown("**Get your Gemini API key** [here](%s)." % page_config.API_KEY_URL) 
        USER_API_KEY = st.text_input("**Enter API Key :**", placeholder="API Key Please", key="api_key", help=api_key_help)
        col1,col2,col3 = st.columns(3)
        with col2:
            check_valid = st.form_submit_button("Set Key", use_container_width=True)
            page_config.API_KEY = st.session_state.api_key
            genai.configure(api_key=st.session_state.api_key)
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
    function startTimer(duration) {{
        let timer = duration;
        const timerElement = parent.document.getElementById('timer-display');
        
        function updateTimer() {{
            const minutes = Math.floor(timer / 60);
            const seconds = timer % 60;
            
            if (timerElement) {{
                timerElement.innerText = `⏱ Time Remaining: ${{minutes}}m ${{seconds}}s`;
            }}
            
            if (--timer < 0) {{
                clearInterval(interval);

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
        const interval = setInterval(updateTimer, 1000);
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

#--------------------------- Load questions -----------------------------------------------
if st.session_state.auto_submit :
    st.header("TIMES UP")

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
    st.session_state.manual_submit = True

if st.session_state.manual_submit:
    st.header("Grades")
    for idx, pair in enumerate(questions):
        student_ans = st.session_state[f"ans_{idx}"].strip()
        if not student_ans:
            st.warning(f"Q{idx+1}: No answer provided.")
            st.divider()
            continue

        with st.spinner(f"Grading Q{idx + 1}..."):
            result = grade_with_llm(
                question=pair["question_en"],
                correct=pair["answer"],
                student=student_ans,
            )
        st.markdown(f"**Q{idx + 1} Grade & Feedback:**  \n{result}")
        expander = st.expander("See actual answer")
        expander.write(f"**Q : {pair['question_en']}**")
        expander.divider()
        expander.write(f"A : {pair['answer']}")

        st.divider()
    
    #--------------------------- Grading Done -----------------------------------------------------
    st.session_state.grading_done = True
    if isinstance(total_score, float) and isinstance(total_max_score, float):
        if total_max_score == 0:
                final_grade = 5.0
        else:
            score_percentage = (total_score / total_max_score) * 100
            final_grade = note(score_percentage)
    
    #------------------------ Final Sidebar and Grades ------------------------------------------------
    st.sidebar.markdown(f"""
                        🏆 **Total Score: {total_score:.1f} / {total_max_score:.1f}** \n
                        💯 **Note : {final_grade}
                        """)
    st.success(f"🏆 **Total Score: {total_score:.1f} / {total_max_score:.1f}**")
    st.success(f"💯 **Note : {final_grade}**")

    if st.session_state.grading_done:
        page_config.EXAM_DONE = True
        page_config.LATEST_GRADE = final_grade
        page_config.LATEST_SCORE = f"Score: {total_score}/{total_max_score}"