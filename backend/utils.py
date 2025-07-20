import fitz  # PyMuPDF

def extract_outline(file_stream):
    doc = fitz.open(stream=file_stream.read(), filetype="pdf")

    # Try to get built-in PDF outline (bookmarks)
    toc = doc.get_toc(simple=True)  # Returns list of [level, title, page]
    
    outline = []
    for entry in toc:
        level, title, page = entry
        outline.append({
            "level": f"H{level}",
            "text": title,
            "page": page
        })

    # If no outline found, add fallback message
    if not outline:
        outline.append({
            "level": "H1",
            "text": "No outline/bookmarks found in PDF.",
            "page": 1
        })

    return {
        "title": doc.metadata.get("title", "Untitled Document"),
        "outline": outline
    }
