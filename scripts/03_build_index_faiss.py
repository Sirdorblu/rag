import os, glob, shutil
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

DOC_DIR = "knowledge_base/docs"
OUT_DIR = "data/faiss_index"
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

def load_docs():
    docs = []
    for path in sorted(glob.glob(os.path.join(DOC_DIR, "*.md"))):
        txt = open(path, "r", encoding="utf-8").read()
        docs.append(Document(page_content=txt, metadata={"source": path}))
    return docs

docs = load_docs()
splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=150)
chunks = splitter.split_documents(docs)

for i, d in enumerate(chunks):
    d.metadata["chunk_id"] = i

# nomic-embed-text: embeddings-only модель :contentReference[oaicite:8]{index=8}
emb = OllamaEmbeddings(model="nomic-embed-text", base_url=OLLAMA_BASE_URL)

if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)

vs = FAISS.from_documents(chunks, emb)
os.makedirs("data", exist_ok=True)
vs.save_local(OUT_DIR)

print("docs:", len(docs))
print("chunks:", len(chunks))
print("saved:", OUT_DIR)
