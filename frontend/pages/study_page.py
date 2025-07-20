from pathlib import Path
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from pages import page_config

if st.button(label=f"Study: {page_config.module_name}", icon="◀️"):
    st.switch_page("pages/main_page.py")

st.title('View The Documents')

# __file__ = .../frontend/pages/study_page.py
PAGES_DIR = Path(__file__).resolve().parent  # …/Exam_Prep/frontend/pages
PROJECT_ROOT = PAGES_DIR.parent.parent  # …/Exam_Prep
DATA_DIR = PROJECT_ROOT / "slides_pdfs"

docs = []

for doc in DATA_DIR.iterdir():
    if doc.suffix == ".pdf":
        docs.append(doc.name.removesuffix(".pdf"))

if len(docs) == 0:
    st.markdown("There are no contents for this module!")
else:
    chapter = st.selectbox(label="Please select the module chapter", options=docs)
    viewer, summary, quiz = st.tabs(tabs=["PDF Viewer", "Summary", "Quiz"])

    pdf_opts = dict(width=700, height=1000, viewer_align="center", show_page_separator=True)

    with viewer:
        st.header(chapter)
        docName = chapter + ".pdf"
        pdf_file = DATA_DIR / docName
        pdf_viewer(str(pdf_file), **pdf_opts)

    with summary:
        st.header("Summary of " + chapter)

    with quiz:
        st.header("Quiz: " + chapter)

