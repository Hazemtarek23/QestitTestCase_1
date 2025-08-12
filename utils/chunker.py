def split_text_into_chunks(text: str, max_tokens: int = 1500) -> list[str]:
    import tiktoken
    enc = tiktoken.encoding_for_model("gpt-4")  # or gpt-35-turbo
    words = text.split("\n")
    chunks = []
    current_chunk = []

    for paragraph in words:
        current_chunk.append(paragraph)
        tokenized = enc.encode("\n".join(current_chunk))
        if len(tokenized) > max_tokens:
            current_chunk.pop()
            chunks.append("\n".join(current_chunk))
            current_chunk = [paragraph]

    if current_chunk:
        chunks.append("\n".join(current_chunk))

    return chunks
