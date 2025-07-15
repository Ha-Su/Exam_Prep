from pathlib import Path
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer

st.title('View The Documents')

# __file__ = .../frontend/pages/page1.py
PAGES_DIR = Path(__file__).resolve().parent               # …/Exam_Prep/frontend/pages
PROJECT_ROOT = PAGES_DIR.parent.parent                    # …/Exam_Prep
DATA_DIR = PROJECT_ROOT / "slides_pdfs"

docs = []

for doc in DATA_DIR.iterdir():
    if doc.suffix == ".pdf":
        docs.append(doc.name.removesuffix(".pdf"))

tabs = st.tabs(docs)

pdf_opts = dict(width=700, height=1000, viewer_align="center", show_page_separator=True)

counter = 0

for tab in tabs:
    with tab:
        st.header(docs[counter])
        docName = docs[counter] + ".pdf"
        pdf_file = DATA_DIR / docName
        counter += 1
        pdf_viewer(str(pdf_file), **pdf_opts, key="tab" + str(counter))
