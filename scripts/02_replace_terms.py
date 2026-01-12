import os, json, re, glob

MAP_FILE = "knowledge_base/terms_map.json"
IN_DIR = "raw_sources/pages"
OUT_DIR = "knowledge_base/docs"
os.makedirs(OUT_DIR, exist_ok=True)

with open(MAP_FILE, "r", encoding="utf-8") as f:
    terms = json.load(f)

pairs = sorted(terms.items(), key=lambda x: len(x[0]), reverse=True)

def replace_all(text: str) -> str:
    for src, dst in pairs:
        text = re.sub(re.escape(src), dst, text, flags=re.IGNORECASE)
    return text

count = 0
for p in sorted(glob.glob(os.path.join(IN_DIR, "*.txt"))):
    raw = open(p, "r", encoding="utf-8").read()
    out = replace_all(raw)
    out_path = os.path.join(OUT_DIR, os.path.basename(p).replace(".txt", ".md"))
    open(out_path, "w", encoding="utf-8").write(out)
    print("written:", out_path)
    count += 1

print("total docs:", count)
print("note: 00_fewshot.md and malicious.md are already in knowledge_base/docs/")
