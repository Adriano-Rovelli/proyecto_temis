from flask import Flask, render_template, request
import json
import os
import numpy as np
import requests
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq

load_dotenv()
app = Flask(__name__)

# Configuración Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "gemma2-9b-it")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Cargar vectores
with open("vectors.json", "r", encoding="utf8") as f:
    vectors = json.load(f)

# Cargar modelo local de embeddings
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    return embed_model.encode(text).tolist()

def cosine_sim(a, b):
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

def buscar_contexto(pregunta):
    emb = get_embedding(pregunta)
    similares = sorted([
        { "text": v["text"], "score": cosine_sim(emb, v["embedding"]) }
        for v in vectors
    ], key=lambda x: x["score"], reverse=True)
    top = [s["text"] for s in similares[:3] if s["score"] > 0.65]
    return "\n\n---\n\n".join(top)

def responder(pregunta, contexto):
    messages = [
    { "role": "system", "content": "Sos un asistente útil, conciso y claro. Respondé en base al contexto." },
    { "role": "user", "content": f"{pregunta}\n\n(Usá el contexto interno para responder, pero no lo muestres ni lo expliques)." }
    ]
    chat_completion = groq_client.chat.completions.create(
        model=os.getenv("GROQ_MODEL", "gemma2-9b-it"),
        messages=messages,
        temperature=0.7,
        max_tokens=512
    )
    return chat_completion.choices[0].message.content

@app.route("/", methods=["GET", "POST"])
def index():
    answer = None
    if request.method == "POST":
        pregunta = request.form["question"]
        contexto = buscar_contexto(pregunta)
        answer = responder(pregunta, contexto)
    return render_template("index.html", answer=answer)

if __name__ == "__main__":
    app.run(debug=True)
