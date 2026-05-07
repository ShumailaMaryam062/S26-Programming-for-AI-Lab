import os
import re
import pandas as pd
import numpy as np
import faiss
from flask import Flask, render_template, request, jsonify
from sentence_transformers import SentenceTransformer

app = Flask(__name__)

DATA_FILE = "qna_dataset.csv"
EMBEDDING_FILE = "findmate_embeddings.npy"
INDEX_FILE = "findmate_faiss.index"
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


qna_df = pd.read_csv(DATA_FILE)
qna_df["clean_question"] = qna_df["question"].apply(clean_text)
qna_df["clean_answer"] = qna_df["answer"].apply(clean_text)
qna_df["clean_text"] = qna_df["clean_question"] + " " + qna_df["clean_answer"]

model = SentenceTransformer(MODEL_NAME)


def make_embeddings_and_index():
    embeddings = model.encode(qna_df["clean_text"].values)
    embeddings = np.array(embeddings).astype("float32")

    np.save(EMBEDDING_FILE, embeddings)

    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    faiss.write_index(index, INDEX_FILE)
    return embeddings, index



if os.path.exists(EMBEDDING_FILE) and os.path.exists(INDEX_FILE):
    embeddings = np.load(EMBEDDING_FILE).astype("float32")
    faiss_index = faiss.read_index(INDEX_FILE)
else:
    embeddings, faiss_index = make_embeddings_and_index()


def search_findmate(query, count=3):
    query_clean = clean_text(query)
    query_embedding = model.encode([query_clean])
    query_embedding = np.array(query_embedding).astype("float32")

    distance, indices = faiss_index.search(query_embedding, count)

    results = []
    for i in range(count):
        row_no = indices[0][i]
        results.append({
            "question": qna_df["question"].iloc[row_no],
            "answer": qna_df["answer"].iloc[row_no],
            "category": qna_df["category"].iloc[row_no],
            "distance": float(distance[0][i])
        })

    return results


def get_best_answer(user_msg):
    if user_msg.strip() == "":
        return "Please enter your question about lost or found items."

    matched_results = search_findmate(user_msg, count=3)
    best = matched_results[0]

    reply = best["answer"]
    reply += f"\n\nMatched question: {best['question']}"
    return reply


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()

        if not data or "message" not in data:
            return jsonify({"error": "Invalid request format"}), 400

        user_text = data["message"]
        reply = get_best_answer(user_text)
        return jsonify({"reply": reply})

    except Exception as e:
        print("Some error occured:", e)
        return jsonify({"error": "An error occurred while processing your message"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=50009)
