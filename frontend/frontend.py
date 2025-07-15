import streamlit as st
import re
import pathlib
import glob
import json
import time
import google.generativeai as genai
from dotenv import load_dotenv
import os

# ──────────────────────────────────────────────────────────────────────────────
#  Configurations
# ──────────────────────────────────────────────────────────────────────────────
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("Missing GOOGLE_API_KEY in environment")
genai.configure(api_key=api_key)

MODEL = os.getenv("MODEL", "gemini-2.5-flash-lite-preview-06-17")
QUESTIONS_FOLDER = os.getenv("QUESTIONS_GP")

# Rate limit: max 15 calls per minute
SECONDS_BETWEEN_CALLS = 60.0 / 15.0


# Load QnA
def load_qna(folder_path):
    p = pathlib.Path(folder_path)
    if not p.is_file:
        raise FileNotFoundError(f"{folder_path} not found")
    return json.loads(p.read_text(encoding="utf-8"))

# Load questions in MD format (questions only, no answer)
# def load_questions_GP(q_folder):
#     qs = []
#     bullet_re = re.compile(r'^\s*(?:[\*\-]|\d+\.)\s+(.*\S.*)$')
#     for md_path in pathlib.Path(q_folder).glob("*.md"):
#         for line in md_path.read_text(encoding="utf-8").splitlines():
#             m = bullet_re.match(line)
#             if m:
#                 text = m.group(1).strip()
#                 # skip very short lines
#                 if len(text) > 5:
#                     qs.append(text)
#     return qs

# Call the LLM for grading given specific prompt for grading
def grade_with_llm(question: str, correct: str, student: str) -> str:
    prompt = f"""
        You are an HCI professor grading a short-answer exam.  For each question:

        1.  **Determine the maximum score** by reading the question:
            - Naming N items → 0.5 pts each → max = N*0.5.  
            - Defining M items → 1 pts each → max = M.  
            - Definition + Example → 1 pt for definition, 1 pt for example → max = 2.  
            - Mix and match as needed (e.g. “Name 4 Laws and define 2” → naming max = 4*0.5=2; definitions max = 2*0.5=1; total max = 3).

        2.  **Grade** the student's answer out of that inferred maximum. Be fair. If the given answer somehow includes / summarizes the main idea of the model answer / key, full score may be given.

        3.  **Explain** briefly what's missing or incorrect.

        4.  **Format your output** like this:
            ```
            Grade: <score>/<max>

            Feedback:
            - Feedback <what is good or what is missing from the given answer> on one question point<naming, defining, example, etc> **Score/max**(refer to point 1)
            - Feedback <what is good or what is missing from the given answer> on another question point<naming, defining, example, etc>, !!IF APPLICABLE!!, **Score/max**(refer to point 1)
            - More feedbacks if necessary
            ```
            Only include the lines for parts the question actually asks.
            Output should be in text format!

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
    time.sleep(SECONDS_BETWEEN_CALLS)
    return response.text.strip()

# print(load_questions(QUESTIONS_FOLDER))


# ──────────────────────────────────────────────────────────────────────────────
#  UI Shenanigans
# ──────────────────────────────────────────────────────────────────────────────

# Load questions
# questions_de = load_questions_GP(QUESTIONS_FOLDER)
questions = load_qna(f"{QUESTIONS_FOLDER}/updated_QnA_pairs.json")

for idx, qna_pair in enumerate(questions) :
    st.markdown(f"**{idx+1} )**")
    st.markdown(f"**🇩🇪 : {qna_pair['question_de']}**") #German questions
    st.markdown(f"**🇬🇧 : {qna_pair['question_en']}**") #English questions

    st.text_area("Answer : ", key=f"ans_{idx}", height=100)
    st.divider()

if st.button("Submit", type="primary"):
    st.header("Grades")
    for idx, pair in enumerate(questions):
        student_ans = st.session_state[f"ans_{idx}"].strip()
        if not student_ans:
            st.warning(f"Q{idx+1}: No answer provided.")
            continue

        with st.spinner(f"Grading Q{idx+1}..."):
            result = grade_with_llm(
                question=pair["question_en"],
                correct=pair["answer"],
                student=student_ans,
            )
        st.markdown(f"**Q{idx+1} Grade & Feedback:**  \n{result}")
        expander = st.expander("See actual answer")
        expander.write(f"**{pair['question_en']}**")
        expander.divider()
        expander.write(f"{pair['answer']}")
        
        st.divider()