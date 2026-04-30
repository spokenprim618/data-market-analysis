import re
from .schema import empty_schema

SECTION_PATTERNS = {
    "responsibilities": r"(responsibilities|duties|what you will do|primary responsibilities)",
    "requirements": r"(requirements|qualifications|what you bring|skills required|what we're looking for)",
    "experience": r"(experience|minimum experience|preferred experience)",
    "benefits": r"(benefits|what we offer|compensation)",
    "about": r"(about us|about the company|about the role)"
}

def regex_split(text):
    sections = empty_schema()

    # normalize
    text = re.sub(r"\s+", " ", text)

    matches = []

    for label, pattern in SECTION_PATTERNS.items():
        for m in re.finditer(pattern, text, re.IGNORECASE):
            matches.append((m.start(), label))

    if not matches:
        return None, 0.0  # no structure detected

    matches.sort()

    for i, (start, label) in enumerate(matches):
        end = matches[i+1][0] if i+1 < len(matches) else len(text)
        chunk = text[start:end].strip()

        if sections[label] is None:
            sections[label] = chunk
        else:
            # handle duplicates
            sections[label] += " " + chunk

    confidence = len(matches) / len(SECTION_PATTERNS)

    return sections, confidence