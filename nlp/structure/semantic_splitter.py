from sentence_transformers import SentenceTransformer, util
import re

model = SentenceTransformer("all-MiniLM-L6-v2")

SECTION_PROTOTYPES = {
    "responsibilities": "tasks and duties of the job",
    "benefits": "salary perks compensation what we offer",
    "about": "company overview mission description"
}

proto_emb = {
    k: model.encode(v, convert_to_tensor=True)
    for k, v in SECTION_PROTOTYPES.items()
}


def fill_missing_sections(text, sections):
    """
    Only fills empty fields in existing regex output.
    Returns:
        updated_sections, confidence_score
    """

    if sections is None:
        return None, 0.0

    # -----------------------------
    # 1. Only target missing fields
    # -----------------------------
    missing_sections = {
        k: v for k, v in sections.items() if v is None and k in proto_emb
    }

    if not missing_sections:
        return sections, 1.0

    # -----------------------------
    # 2. Better sentence splitting
    # -----------------------------
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 15]

    confidences = []
    used_scores = []

    # -----------------------------
    # 3. Backfill only missing keys
    # -----------------------------
    for sent in sentences:
        emb = model.encode(sent, convert_to_tensor=True)

        # only compare against missing sections
        scores = {
            k: util.cos_sim(emb, proto_emb[k]).item()
            for k in missing_sections.keys()
        }

        best = max(scores, key=scores.get)
        best_score = scores[best]

        confidences.append(best_score)

        # ignore weak matches
        if best_score < 0.35:
            continue

        # fill ONLY if still missing
        if sections.get(best) is None:
            sections[best] = sent
            used_scores.append(best_score)

    # -----------------------------
    # 4. Confidence (more accurate now)
    # -----------------------------
    if used_scores:
        confidence = sum(used_scores) / len(used_scores)
    else:
        confidence = 0.0

    return sections, confidence