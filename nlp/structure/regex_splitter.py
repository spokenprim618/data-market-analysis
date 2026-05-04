import re
from ..util.schema import empty_schema

SECTION_PATTERNS = {
    "responsibilities": r"(responsibilities|duties|what you will do|primary responsibilities)",
    "requirements": r"(requirements|qualifications|what you bring|skills required|what we're looking for)",
    "experience": r"(experience|minimum experience|preferred experience)",
    "benefits": r"(benefits|what we offer|compensation)",
    "about": r"(about us|about the company|about the role)",

    # NEW: skill-focused structure
    "skills": r"(skills|technical skills|core skills|preferred skills)",
    "additional_qualifications": r"(additional qualifications|preferred qualifications|nice to have|bonus qualifications)"
}

def regex_split(text):
    sections = empty_schema()

    # normalize whitespace
    text = re.sub(r"\s+", " ", text)

    matches = []
    unknown_headers = []

    # ---------------------------
    # 1. Known section detection
    # ---------------------------
    for label, pattern in SECTION_PATTERNS.items():
        for m in re.finditer(pattern, text, re.IGNORECASE):
            matches.append((m.start(), label))

    # ---------------------------
    # 2. Unknown header detection
    # ---------------------------
    UNKNOWN_HEADER_PATTERN = r"(?m)^\s*[A-Z][A-Za-z\s&/\-]{3,50}\s*:?\s*$"

    for m in re.finditer(UNKNOWN_HEADER_PATTERN, text):
        header = m.group().strip()

        # ensure it's not already a known section
        is_known = any(
            re.search(pattern, header, re.IGNORECASE)
            for pattern in SECTION_PATTERNS.values()
        )

        if not is_known:
            unknown_headers.append(header)

    # if nothing found at all
    if not matches and not unknown_headers:
        return None, 0.0, []

    matches.sort()

    used_labels = set()

    # ---------------------------
    # 3. Extract known sections
    # ---------------------------
    for i, (start, label) in enumerate(matches):
        end = matches[i + 1][0] if i + 1 < len(matches) else len(text)
        chunk = text[start:end].strip()

        if sections[label] is None:
            sections[label] = chunk
        else:
            sections[label] += " " + chunk

        used_labels.add(label)

    # ---------------------------
    # 4. Confidence calculation
    # ---------------------------
    confidence = len(used_labels) / max(len(SECTION_PATTERNS), 1)

    # ---------------------------
    # 5. Return unknown headers
    # ---------------------------
    return sections, confidence, unknown_headers