from sentence_transformers import SentenceTransformer, util
import re
from .schema import empty_schema

# load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

SECTION_PROTOTYPES = {
    "responsibilities": "tasks, duties, what you will do in the job",
    "requirements": "skills, qualifications, what is required for the job",
    "experience": "years of experience, prior work background",
    "benefits": "salary, compensation, benefits, perks",
    "about": "company description, mission, organization overview"
}

# precompute embeddings
prototype_embeddings = {
    k: model.encode(v, convert_to_tensor=True)
    for k, v in SECTION_PROTOTYPES.items()
}


def classify_chunk(chunk):
    chunk_embedding = model.encode(chunk, convert_to_tensor=True)

    scores = {}

    for section, proto_emb in prototype_embeddings.items():
        score = util.cos_sim(chunk_embedding, proto_emb).item()
        scores[section] = score

    best_section = max(scores, key=scores.get)
    best_score = scores[best_section]

    # threshold (tune this later)
    if best_score < 0.4:
        return "unknown", best_score

    return best_section, best_score


def semantic_split(text):
    sections = empty_schema()

    chunks = re.split(r"\n+|(?<=[.!?])\s+", text)

    suggestions = []
    confidences = []

    for chunk in chunks:
        chunk = chunk.strip()
        if not chunk:
            continue

        section, score = classify_chunk(chunk)

        if section == "unknown":
            sections["unknown"].append(chunk)
        else:
            if sections[section] is None:
                sections[section] = chunk
            else:
                sections[section] += " " + chunk

        confidences.append(score)

        suggestions.append({
            "chunk": chunk[:100],
            "predicted_section": section,
            "confidence": round(score, 3)
        })

    sections["suggestions"] = suggestions

    avg_conf = sum(confidences) / len(confidences) if confidences else 0.3

    return sections, avg_conf