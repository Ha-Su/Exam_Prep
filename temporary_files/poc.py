import os
import re
import time
import json
import pathlib
from glob import glob

from sentence_transformers import SentenceTransformer, CrossEncoder
import faiss
import google.generativeai as genai

# ──────────────────────────────────────────────────────────────────────────────
#  CONFIGURATION
# ──────────────────────────────────────────────────────────────────────────────
genai.configure(api_key="AIzaSyD_zK_-MrOgNAtML2MuiRZW4ibbXt83G1I")
gemini_model = genai.GenerativeModel("gemini-2.5-flash-lite-preview-06-17")

MD_FOLDER        = "./slides_md"
QUESTIONS_FOLDER = "./questions_md"
OUTPUT_PATH      = "./answers_generated"
OUTPUT_JSON      = f"{OUTPUT_PATH}/answers.json"           #Change name to save into different file

# Rate limit: max 15 calls per minute
SECONDS_BETWEEN_CALLS = 60.0 / 15.0

cross_encoder = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2",
    device="mps"                    #Change to gpu or cpu if not on macbook
)

# ──────────────────────────────────────────────────────────────────────────────
#  Load lecture text from Markdown
# ──────────────────────────────────────────────────────────────────────────────
def extract_slides_from_md(md_folder):
    slides = []
    for md_path in pathlib.Path(md_folder).rglob("*.md"):
        topic = md_path.stem
        text  = md_path.read_text(encoding="utf-8")
        paras = [p.replace("\n", " ").strip()
                 for p in text.split("\n\n")
                 if p.strip()]
        for idx, para in enumerate(paras):
            slides.append((topic, idx, para))
    return slides

# ──────────────────────────────────────────────────────────────────────────────
#  Break long text into size‐bounded chunks
# ──────────────────────────────────────────────────────────────────────────────
def chunkify(text, max_len=500):
    words  = text.split()
    chunks, chunk, length = [], [], 0
    for w in words:
        chunk.append(w)
        length += len(w) + 1
        if length > max_len:
            chunks.append(" ".join(chunk))
            chunk, length = [], 0
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks

# ──────────────────────────────────────────────────────────────────────────────
#   Build a FAISS index over all chunks
# ──────────────────────────────────────────────────────────────────────────────
def build_index(slide_tuples, model_name="paraphrase-multilingual-MiniLM-L12-v2"): #for multi language problem, use : "all-MiniLM-L6-v2" for broader problems
    embedder = SentenceTransformer(model_name)
    passages, metadata = [], []
    for topic, idx, text in slide_tuples:
        for chunk in chunkify(text):
            passages.append(chunk)
            metadata.append((topic, idx))
    embeddings = embedder.encode(passages, convert_to_numpy=True)
    faiss.normalize_L2(embeddings)
    dim   = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index, passages, metadata, embedder

# ──────────────────────────────────────────────────────────────────────────────
#   Load exam questions (bullets or numbered items), parsed using markdown symbols
# ──────────────────────────────────────────────────────────────────────────────
def load_questions(q_folder):
    qs = []
    bullet_re = re.compile(r'^\s*(?:[\*\-]|\d+\.)\s+(.*\S.*)$')
    for md_path in pathlib.Path(q_folder).glob("*.md"):
        for line in md_path.read_text(encoding="utf-8").splitlines():
            m = bullet_re.match(line)
            if m:
                text = m.group(1).strip()
                # skip very short lines
                if len(text) > 5:
                    qs.append(text)
    return qs

# ──────────────────────────────────────────────────────────────────────────────
#   Retrieve top-k relevant chunks for a question
# ──────────────────────────────────────────────────────────────────────────────
def retrieve_and_rerank(
    question,
    faiss_index,
    passages,       # list of all chunk texts
    metadata,       # list of (topic, slide) for each chunk
    embedder,       # your SentenceTransformer for dense retrieval
    cross_encoder,
    initial_k=20,   # how many to pull from FAISS
    final_k=10       # how many to return after rerank
):
    # --- Stage 1: dense retrieval ---
    q_emb = embedder.encode([question], convert_to_numpy=True)
    faiss.normalize_L2(q_emb)
    D, I = faiss_index.search(q_emb, initial_k)

    # build a list of hits
    hits = []
    for score, idx in zip(D[0], I[0]):
        hits.append({
            "score": float(score),
            "topic": metadata[idx][0],
            "slide": metadata[idx][1],
            "text": passages[idx]
        })

    # --- Stage 2: cross-encoder reranking ---
    # Prepare (question, passage) pairs
    pairs = [[question, h["text"]] for h in hits]

    # Predict relevance scores
    rerank_scores = cross_encoder.predict(pairs, batch_size=16)

    # Attach and sort
    for h, r in zip(hits, rerank_scores):
        h["rerank_score"] = float(r)

    hits = sorted(hits, key=lambda x: x["rerank_score"], reverse=True)

    # Return top final_k
    return hits[:final_k]


# ──────────────────────────────────────────────────────────────────────────────
#  Generate an answer via Gemini
# ──────────────────────────────────────────────────────────────────────────────
def generate_answer(question, contexts):
    prompt = (
        "You are an HCI teaching assistant. Use ONLY the following contexts to answer the question."
        "IF the context does not give a proper answer to the question or if the information of the context is limited, answer it using your knowledge outside of the given context."
        "\n\n"
        + "\n---\n".join(contexts)
        + f"\n\nQuestion: {question}\nAnswer:"
    )
    resp = gemini_model.generate_content(prompt)
    
    time.sleep(SECONDS_BETWEEN_CALLS)   
    return resp.text.strip()

# ──────────────────────────────────────────────────────────────────────────────
#  MAIN PIPELINE
# ──────────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # 1) Read & index slides
    slides  = extract_slides_from_md(MD_FOLDER)
    index, passages, metadata, embedder = build_index(slides)

    # 2) Load questions
    questions = load_questions(QUESTIONS_FOLDER)
    if not questions:
        print(f"No questions found in {QUESTIONS_FOLDER}")
        exit(1)

    # 3) Retrieve + answer each
    qa_pairs = []
    for q in questions:
        hits = retrieve_and_rerank(
                q,
                index,
                passages,
                metadata,
                embedder,
                cross_encoder,
                initial_k=20,   # bump this up so your relevant slide is in the pool
                final_k=5       # Gemini still only sees top 5
        )
        contexts = [h["text"] for h in hits]
        ans      = generate_answer(q, contexts)
        qa_pairs.append({
            "question": q,
            "answer": ans,
            "sources": [
                {"topic": h["topic"], "slide": h["slide"], "score": h["score"]}
                for h in hits
            ]
        })
        print("✓", q)


    # 4) Write to JSON
    with open(OUTPUT_JSON, "w", encoding="utf-8") as fp:
        json.dump(qa_pairs, fp, ensure_ascii=False, indent=2)

    print(f"\n Wrote {len(qa_pairs)} Q&A pairs to '{OUTPUT_JSON}'")
