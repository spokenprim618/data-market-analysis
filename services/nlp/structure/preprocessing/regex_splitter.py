import re
from ..util.schema import empty_schema

SECTION_PATTERNS = {
    "responsibilities": r"\b(responsibilities|duties|what you will do|primary responsibilities)\b",

    "requirements": r"\b(requirements|qualifications|what you bring|what we're looking for|you should have)\b",

    "experience": r"\b(experience|minimum experience|preferred experience|years of experience)\b",

    "benefits": r"\b(benefits|what we offer|compensation|perks|salary)\b",

    "about": r"\b(about us|about the company|about the role|company overview)\b",

    "education": r"\b(education|degree|bachelor|master|phd)\b",

    "certifications": r"\b(certifications|certified|license|accreditation)\b",

    "additional_qualifications": r"\b(additional qualifications|nice to have|bonus qualifications|preferred qualifications)\b"
}

def regex_split(text):

    sections = empty_schema()

    text = re.sub(r"\s+", " ", text)

    matches = []
    unknown_headers = []

    field_hits = {k: 0 for k in SECTION_PATTERNS.keys()}

    # -----------------------------------
    # 1. Detect known sections
    # -----------------------------------
    for label, pattern in SECTION_PATTERNS.items():

        for m in re.finditer(pattern, text, re.IGNORECASE):

            matches.append((m.start(), label))
            field_hits[label] += 1

    # -----------------------------------
    # 2. Detect unknown headers
    # -----------------------------------
    UNKNOWN_HEADER_PATTERN = r"(?m)^\s*[A-Z][A-Za-z\s&/\-]{3,50}\s*:?\s*$"

    for m in re.finditer(UNKNOWN_HEADER_PATTERN, text):

        header = m.group().strip()

        is_known = any(
            re.search(pattern, header, re.IGNORECASE)
            for pattern in SECTION_PATTERNS.values()
        )

        if not is_known:
            unknown_headers.append(header)

    # -----------------------------------
    # 3. Empty case
    # -----------------------------------
    if not matches and not unknown_headers:
        return None, 0.0, [], {}

    matches.sort()

    # -----------------------------------
    # 4. Extract structured sections
    # -----------------------------------
    for i, (start, label) in enumerate(matches):

        end = matches[i + 1][0] if i + 1 < len(matches) else len(text)

        chunk = text[start:end].strip()

        if sections[label] is None:
            sections[label] = chunk
        else:
            sections[label] += " " + chunk

    # -----------------------------------
    # 5. FIELD-LEVEL confidence (IMPORTANT)
    # -----------------------------------
    total_fields = len(SECTION_PATTERNS)

    field_confidence = {
        k: (1.0 if field_hits[k] > 0 else 0.0)
        for k in SECTION_PATTERNS.keys()
    }

    overall_conf = sum(field_confidence.values()) / max(total_fields, 1)

    # -----------------------------------
    # 6. Return enriched output
    # -----------------------------------
    return (
        sections,
        overall_conf,
        unknown_headers,
        field_confidence
    )