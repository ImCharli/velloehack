from typing import List
import logfire


def chunk_text(
    text: str,
    chunk_size: int = 1500,
    chunk_overlap: int = 200,
) -> List[str]:
    """
    Paragraph-aware chunking with 200-character overlap.
    Keeps chunks reasonably small while preserving context between chunks.
    """

    with logfire.span("✂️ Text Chunking", text_length=len(text)):

        if not text.strip():
            return []

        paragraphs = [
            p.strip()
            for p in text.split("\n\n")
            if p.strip()
        ]

        chunks = []
        current = ""

        for paragraph in paragraphs:

            # Normal case: paragraph fits into current chunk
            if len(current) + len(paragraph) + 2 <= chunk_size:
                current = (
                    current + "\n\n" + paragraph
                    if current
                    else paragraph
                )
                continue

            # Save current chunk
            if current:
                chunks.append(current.strip())

            # Preserve overlap from previous chunk
            overlap_text = (
                current[-chunk_overlap:]
                if current and chunk_overlap > 0
                else ""
            )

            current = (
                overlap_text + "\n\n" + paragraph
                if overlap_text
                else paragraph
            )

            # Handle unusually large paragraphs
            while len(current) > chunk_size:
                chunks.append(current[:chunk_size].strip())
                current = current[
                    max(0, chunk_size - chunk_overlap):
                :]

        if current.strip():
            chunks.append(current.strip())

        chunks = [c for c in chunks if c.strip()]

        logfire.info(
            f"✅ Generated {len(chunks)} chunks "
            f"(size={chunk_size}, overlap={chunk_overlap})"
        )

        return chunks