def chunk_text(pages, chunk_size=500, overlap=100):
    chunks = []  # Final list of chunks

    for page in pages:
        text = page["text"]
        page_num = page["page"]

        start = 0
        while start < len(text):
            chunk = text[start:start + chunk_size]

            chunks.append({
                "content": chunk,
                "page": page_num
            })

            start += chunk_size - overlap

    return chunks