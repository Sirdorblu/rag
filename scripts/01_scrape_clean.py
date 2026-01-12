import os, re, time, requests
from bs4 import BeautifulSoup

IN_FILE = "raw_sources/urls.txt"
OUT_DIR = "raw_sources/pages"
os.makedirs(OUT_DIR, exist_ok=True)

def clean_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    text = soup.get_text("\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

with open(IN_FILE, "r", encoding="utf-8") as f:
    urls = [u.strip() for u in f if u.strip()]

for i, url in enumerate(urls, 1):
    r = requests.get(url, timeout=40, headers={"User-Agent": "rag-bot/1.0"})
    r.raise_for_status()
    txt = clean_html(r.text)
    out = os.path.join(OUT_DIR, f"doc_{i:02d}.txt")
    with open(out, "w", encoding="utf-8") as f2:
        f2.write(txt)
    print("saved:", out)
    time.sleep(1.0)
