from pathlib import Path
import streamlit as st
from streamlit_pdf_viewer import pdf_viewer
from pages import page_config
import random
import json

# Config
MODULE = page_config.module_name_ab

@st.cache_data
def load_markdown(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")

if st.button(label=f"Study: {page_config.module_name}", icon="◀️"):
    st.switch_page("pages/main_page.py")

st.title('View The Documents')

# __file__ = .../frontend/pages/study_page.py
PAGES_DIR = Path(__file__).resolve().parent  # …/Exam_Prep/frontend/pages
PROJECT_ROOT = PAGES_DIR.parent.parent  # …/Exam_Prep
DATA_DIR = f"{PROJECT_ROOT}/study_material/{MODULE}"

docs = []
DATA_DIR_PDFs = Path(f"{DATA_DIR}/slides_pdfs")

for doc in DATA_DIR_PDFs.iterdir():
    if doc.suffix == ".pdf":
        docs.append(doc.name.removesuffix(".pdf"))

if len(docs) == 0:
    st.warning("There are no contents for this module!")
else:
    chapter = st.selectbox(label="Please select the module chapter", options=docs)
    viewer, summary, quiz = st.tabs(tabs=["PDF Viewer", "Summary", "Quiz"])

    pdf_opts = dict(width=700, height=1000, viewer_align="center", show_page_separator=True)

    with viewer:
        st.header(chapter)
        docName = chapter + ".pdf"
        pdf_file = DATA_DIR_PDFs / docName
        pdf_viewer(str(pdf_file), **pdf_opts)

    with summary:
        chapter_md = chapter + ".md"
        sum = load_markdown(f"{DATA_DIR}/summary/{chapter_md}")
        st.header("Summary of " + chapter)
        st.divider()
        st.markdown(sum)

    with quiz:
        st.header("Quiz: " + chapter)
        st.divider()

        # Constants
        chapter_json = chapter + ".json"
        DECK_FILE = f"{DATA_DIR}/quiz/{chapter_json}"

        # Track last loaded chapter to detect changes
        if "last_chapter" not in st.session_state:
            st.session_state.last_chapter = None

        if st.session_state.last_chapter != chapter:
            # Load and shuffle new deck
            with open(DECK_FILE, "r", encoding="utf-8") as f:
                st.session_state.cards = json.load(f)
            random.shuffle(st.session_state.cards)
            st.session_state.index = 0
            st.session_state.show_answer = False
            st.session_state.last_chapter = chapter

        # Current card
        card = st.session_state.cards[st.session_state.index]

        # Page layout
        st.title("🧠 Anki-Style Quiz")
        st.subheader(f"Card {st.session_state.index + 1} of {len(st.session_state.cards)}")
        st.write(card["question"])

        # Show answer or Next using callbacks
        if not st.session_state.show_answer:
            st.button(
                "Show Answer",
                key="show-answer",
                on_click=lambda: st.session_state.__setitem__('show_answer', True)
            )
        else:
            st.write(f"**Answer:** {card['answer']}")
            st.button(
                "Next",
                key="next-card",
                on_click=lambda: [
                    st.session_state.__setitem__('show_answer', False),
                    st.session_state.__setitem__('index', (st.session_state.index + 1) % len(st.session_state.cards))
                ]
            )



