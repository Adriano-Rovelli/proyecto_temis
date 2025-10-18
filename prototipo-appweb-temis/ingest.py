import os
import json
import pdfplumber
from sentence_transformers import SentenceTransformer

# Configuración
INPUT_DIR = "docs"
OUT_FILE = "vectors.json"
CHUNK_SIZE = 1000
OVERLAP = 200

# Cargar modelo local
model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    i = 0
    while i < len(text):
        chunk = text[i:i+chunk_size]
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def process_file(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    text = ""

    if ext == ".pdf":
        with pdfplumber.open(filepath) as pdf:
            text = "\n".join(page.extract_text() or "" for page in pdf.pages)
    elif ext == ".txt":
        with open(filepath, "r", encoding="utf8") as f:
            text = f.read()
    else:
        print(f"Formato no soportado: {filepath}")
        return []

    chunks = chunk_text(text)
    embeddings = []

    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue
        emb = model.encode(chunk).tolist()
        embeddings.append({
            "id": f"{os.path.basename(filepath)}_{i}",
            "text": chunk,
            "embedding": emb
        })
        print(f"✅ Procesado: {filepath} → chunk {i}")

    return embeddings

def main():
    all_vectors = []
    for filename in os.listdir(INPUT_DIR):
        if filename.endswith(".pdf") or filename.endswith(".txt"):
            filepath = os.path.join(INPUT_DIR, filename)
            all_vectors.extend(process_file(filepath))

    with open(OUT_FILE, "w", encoding="utf8") as f:
        json.dump(all_vectors, f, indent=2)
    print(f"\n🎉 Guardado {len(all_vectors)} vectores en {OUT_FILE}")

if __name__ == "__main__":
    main()
