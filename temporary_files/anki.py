import genanki
import os
import re
from glob import glob
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import google.generativeai as genai

genai.configure(api_key="AIzaSyD_zK_-MrOgNAtML2MuiRZW4ibbXt83G1I")
gemini_model = genai.GenerativeModel("gemini-2.5-flash-lite-preview-06-17")

# Paths
PDF_FOLDER = "./slides_pdfs"
SLIDES_MD_FOLDER = "./slides_md"
QUESTIONS_MD_FOLDER = "./questions_md"

# Step 1: Read all converted markdown slide passages (one chunk per blank-line paragraph)
def load_passages(md_folder):
    passages = []
    for md_path in glob(os.path.join(md_folder, "*.md")):
        topic = os.path.splitext(os.path.basename(md_path))[0]
        with open(md_path, encoding='utf-8') as f:
            text = f.read()
        # chunk by blank lines
        for chunk in filter(bool, re.split(r"\n{2,}", text)):
            passages.append((topic, chunk.replace("\n", " ").strip()))
    return passages

# Step 2: Build FAISS index for retrieval
def build_index(passages, model_name="all-MiniLM-L6-v2"):
    texts = [p for _, p in passages]
    metas = [t for t, _ in passages]
    embedder = SentenceTransformer(model_name)
    embeddings = embedder.encode(texts, convert_to_numpy=True)
    faiss.normalize_L2(embeddings)
    dim = embeddings.shape[1]
    idx = faiss.IndexFlatIP(dim)
    idx.add(embeddings)
    return idx, texts, metas, embedder

# Step 3: Load exam questions
def load_questions(q_folder):
    questions = []
    for md_path in glob(os.path.join(q_folder, "*.md")):
        with open(md_path, encoding='utf-8') as f:
            content = f.read()
        for q in filter(lambda x: len(x.strip())>0, re.split(r"\n\*+ ?", content)):
            questions.append(q.strip())
    return questions

# Step 4: Retrieve top contexts
def retrieve(question, idx, texts, metas, embedder, k=3):
    q_emb = embedder.encode([question], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = idx.search(q_emb, k)
    return [texts[i] for i in I[0]]

# Step 5: Generate answer via Gemini
def generate_answer(question, contexts):
    prompt = "You are an HCI teaching assistant. Use the following contexts to answer:\n\n"
    prompt += "\n---\n".join(contexts)
    prompt += f"\n\nQuestion: {question}\nAnswer:"
    resp = gemini_model.generate_content(prompt)
    return resp.generations[0].text if hasattr(resp, 'generations') else str(resp)

# Step 6: Create Anki deck
MY_MODEL = genanki.Model(
    1607392319,
    'Simple HCI Model',
    fields=[{'name': 'Question'}, {'name': 'Answer'}],
    templates=[{
        'name': 'Card 1',
        'qfmt': '{{Question}}',
        'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    }]
)

deck = genanki.Deck(2059400110, 'HCI Review Deck')

# Prepare passages and index
passages = load_passages(SLIDES_MD_FOLDER)
idx, texts, metas, embedder = build_index(passages)
questions = load_questions(QUESTIONS_MD_FOLDER)

# Create cards
for q in questions:
    contexts = retrieve(q, idx, texts, metas, embedder)
    answer = generate_answer(q, contexts)
    note = genanki.Note(
        model=MY_MODEL,
        fields=[q, answer]
    )
    deck.add_note(note)

# Write to .apkg file
output_path = 'hci_review_deck.apkg'
genanki.Package(deck).write_to_file(output_path)

print(f"Anki deck generated: {output_path}")
