"""Text reflow — cleans up extracted text and wraps to terminal width."""

import re


def clean_text(raw: str) -> str:
    if not raw:
        return ""

    text = raw.replace("\r\n", "\n").replace("\r", "\n")

    # Remove standalone page numbers
    text = re.sub(r"^\s*\d{1,4}\s*$", "", text, flags=re.MULTILINE)

    # Fix hyphenated line breaks: "jum-\nped" → "jumped"
    text = re.sub(r"-\n([a-z])", r"\1", text)

    # Fix broken sentences: line not ending with punctuation + next starts lowercase
    text = re.sub(r"([a-zA-Z,;])\n([a-z])", r"\1 \2", text)

    # Collapse 3+ newlines into 2
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Collapse multiple spaces
    text = re.sub(r"[ \t]{2,}", " ", text)

    # Trim each line
    text = "\n".join(line.strip() for line in text.split("\n"))

    return text.strip()


def word_wrap(text: str, width: int) -> str:
    if not text or width <= 0:
        return text or ""

    result = []
    for line in text.split("\n"):
        # Preserve short/special lines
        if line.startswith(("- ", "* ", "> ", "#")) or len(line) <= width:
            result.append(line)
            continue

        remaining = line
        while len(remaining) > width:
            break_point = remaining.rfind(" ", 0, width)
            if break_point <= 0:
                break_point = width - 1
                result.append(remaining[:break_point] + "-")
                remaining = remaining[break_point:]
            else:
                result.append(remaining[:break_point])
                remaining = remaining[break_point + 1:]
        if remaining:
            result.append(remaining)

    return "\n".join(result)


def reflow(raw: str, width: int = 80) -> str:
    cleaned = clean_text(raw)
    paragraphs = [p for p in cleaned.split("\n\n") if p.strip()]
    wrapped = [word_wrap(p, width) for p in paragraphs]
    return "\n\n".join(wrapped)
