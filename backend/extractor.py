import os
import json
import fitz  # PyMuPDF
from collections import Counter

input_dir = os.environ.get("INPUT_DIR", "input")
output_dir = os.environ.get("OUTPUT_DIR", "output")


# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

def process_pdf(file_path):
    with open(file_path, "rb") as f:
        doc = fitz.open(stream=f.read(), filetype="pdf")

    title = doc.metadata.get("title") or "Untitled Document"

    font_counts = Counter()
    content = []

    for page_num, page in enumerate(doc, start=1):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    size = round(span.get("size", 0), 1)
                    if text and len(text) > 5 and text[0].isupper():
                        font_counts[size] += 1
                        content.append({
                            "text": text,
                            "size": size,
                            "page": page_num
                        })

    top_sizes = [size for size, _ in font_counts.most_common(3)]
    sorted_sizes = sorted(top_sizes, reverse=True)
    h1_size = sorted_sizes[0] if len(sorted_sizes) > 0 else 0
    h2_size = sorted_sizes[1] if len(sorted_sizes) > 1 else h1_size
    h3_size = sorted_sizes[2] if len(sorted_sizes) > 2 else h2_size

    seen = set()
    outline = []

    for item in content:
        txt, sz, pg = item["text"], item["size"], item["page"]
        if txt in seen:
            continue
        if sz == h1_size:
            level = "H1"
        elif sz == h2_size:
            level = "H2"
        elif sz == h3_size:
            level = "H3"
        else:
            continue
        outline.append({"level": level, "text": txt, "page": pg})
        seen.add(txt)

    return {
        "title": title,
        "outline": outline
    }

def main():
    if not os.path.exists(input_dir):
        print(f"[ERROR] Input folder not found: {input_dir}")
        exit(1)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(".pdf"):
            print(f"Processing {filename}")
            full_path = os.path.join(input_dir, filename)
            data = process_pdf(full_path)

            output_path = os.path.join(output_dir, filename.replace(".pdf", ".json"))
            with open(output_path, "w", encoding="utf-8") as out:
                json.dump(data, out, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
