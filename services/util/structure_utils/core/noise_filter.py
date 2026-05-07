import re

JUNK_PATTERNS = [
    r"\bEEO\b",
    r"\bEOE\b",
    r"equal opportunity employer",
    r"privacy statement",
    r"background check",
    r"drug test",
    r"ADA disclaimer",
    r"FIS is committed",
    r"all qualified applicants",
    r"sourcing model",
]


def is_junk_block(block: str) -> bool:
    block_lower = block.lower()

    return any(
        re.search(pattern, block_lower, re.IGNORECASE)
        for pattern in JUNK_PATTERNS
    )


def clean_text(text: str) -> str:
    # split into paragraph-like blocks first (better than word-level)
    blocks = re.split(r"\n{2,}|\r\n{2,}", text)

    cleaned_blocks = []

    for block in blocks:
        block = block.strip()

        if not block:
            continue

        # remove entire block if junk
        if is_junk_block(block):
            continue

        cleaned_blocks.append(block)

    return "\n\n".join(cleaned_blocks).strip()