from flask import Flask, request, jsonify
from flask_cors import CORS
import fitz  # PyMuPDF
from collections import Counter

app = Flask(__name__)
CORS(app)

@app.route("/extract-outline", methods=["POST"])
def extract_outline():
    if "pdf" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["pdf"]
    doc = fitz.open(stream=file.read(), filetype="pdf")

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
                    if (
                        text
                        and len(text) > 5
                        and text[0].isupper()
                        and not text.lower().startswith(("page", "sample", "document"))
                        and not text.endswith(":")
                    ):
                        font_counts[size] += 1
                        content.append({
                            "text": text,
                            "size": size,
                            "page": page_num
                        })

    # Sort and get up to 4 font sizes
    top_sizes = [size for size, _ in font_counts.most_common(4)]
    sorted_sizes = sorted(top_sizes, reverse=True)
    sizes_by_level = {
        i: sorted_sizes[i] if i < len(sorted_sizes) else sorted_sizes[-1]
        for i in range(4)
    }

    seen = set()
    headings = []

    for item in content:
        txt, sz, pg = item["text"], item["size"], item["page"]
        if txt in seen:
            continue

        level = None
        for lvl, s in sizes_by_level.items():
            if sz == s:
                level = f"H{lvl + 1}"
                break

        if level:
            headings.append({"level": level, "text": txt, "page": pg})
            seen.add(txt)

    return jsonify({
        "title": title,
        "outline": headings
    })

if __name__ == "__main__":
    app.run(debug=True)
