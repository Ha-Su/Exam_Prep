import streamlit as st
import json
import random

# Constants
DECK_FILE = "anki.json"

# Initialize session state
if "cards" not in st.session_state:
    with open(DECK_FILE, "r") as f:
        st.session_state.cards = json.load(f)
    random.shuffle(st.session_state.cards)
    st.session_state.index = 0
    st.session_state.show_answer = False

# Current card
card = st.session_state.cards[st.session_state.index]

# Page layout
st.title("🧠 Anki-Style Quiz App")
st.subheader(f"Card {st.session_state.index + 1} of {len(st.session_state.cards)}")
st.write(card["question"])

# Show answer or Next using callbacks for immediate effect
if not st.session_state.show_answer:
    st.button(
        "Show Answer",
        key="show-answer",
        on_click=lambda: st.session_state.__setitem__('show_answer', True)
    )
else:
    st.markdown("---")
    st.write(f"**Answer:** {card['answer']}")
    st.button(
        "Next",
        key="next-card",
        on_click=lambda: [
            st.session_state.__setitem__('show_answer', False),
            st.session_state.__setitem__('index', (st.session_state.index + 1) % len(st.session_state.cards))
        ]
    )
