import json, re

MD_FILE = "gemini-code-1784297640531.md"
OUTPUT = "data/chunks.json"

with open(MD_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# Split by the chunk separator: ---\nmetadata: {...}\n---
# Each chunk (except first) starts with "---\nmetadata: {...}\n---"
# We use a regex that matches the metadata block as a delimiter
parts = re.split(r'\n---\nmetadata:\s*(\{[^}]+\})\n---\n', text)

chunks = []
# First part is content before any metadata (the cover/intro)
# Then each pair is: metadata_json, content

i = 0
if parts[0].strip():
    # First chunk has no metadata block
    chunks.append({
        "id": "chunk_000",
        "section": "general",
        "article_title": "Cover and Index",
        "text": parts[0].strip(),
        "metadata": {"section": "general", "article_title": "Cover and Index"}
    })
    i = 1
else:
    i = 1

chunk_counter = len(chunks)

while i < len(parts) - 1:
    meta_str = parts[i]
    content = parts[i + 1].strip()
    i += 2

    try:
        meta = json.loads(meta_str)
    except json.JSONDecodeError:
        meta = {}

    # Clean content: remove <page_number> tags
    content_clean = re.sub(r'<page_number>\d+</page_number>', '', content).strip()
    content_clean = re.sub(r'\[cite: \d+\]', '', content_clean).strip()

    if not content_clean:
        continue

    chunk_id = f"chunk_{chunk_counter:03d}"
    chunk_counter += 1

    entry = {
        "id": chunk_id,
        "section": meta.get("section", "unknown"),
        "article_title": meta.get("article_title") or meta.get("course_code") or meta.get("level", "unknown"),
        "text": content_clean,
        "metadata": meta
    }
    chunks.append(entry)

# Save
with open(OUTPUT, "w", encoding="utf-8") as f:
    json.dump({"chunks": chunks, "total_chunks": len(chunks)}, f, ensure_ascii=False, indent=2)

print(f"✅ Done! {len(chunks)} chunks saved to {OUTPUT}")
for c in chunks:
    print(f"   {c['id']}: [{c['section']}] {c['article_title']} ({len(c['text'])} chars)")
