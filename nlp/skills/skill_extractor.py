# nlp/skills/skill_extractor.py

import spacy
from spacy.matcher import PhraseMatcher

from skillNer.skill_extractor_class import SkillExtractor
from skillNer.general_params import SKILL_DB


import re
# -----------------------------
# 1. Load spaCy model
# -----------------------------
nlp = spacy.load("en_core_web_sm")


# -----------------------------
# 2. Build PhraseMatcher
# -----------------------------
phrase_matcher = PhraseMatcher(nlp.vocab)

skill_patterns = [nlp.make_doc(skill) for skill in SKILL_DB.keys()]
phrase_matcher.add("SKILLS", skill_patterns)


# -----------------------------
# 3. Initialize SkillExtractor
# -----------------------------
skill_extractor = SkillExtractor(
    nlp,
    SKILL_DB,
    phrase_matcher
)


# Only these sections are allowed to generate skills
SKILL_SOURCE_SECTIONS = {
    "responsibilities",
    "requirements",
    "experience"
}


def clean_skill_text(text: str) -> str:
    """
    Lightweight cleanup for skill extraction only
    """
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[*•\-]", " ", text)
    return text.lower().strip()


def extract_skills(sections: dict):
    """
    Extract skills ONLY from structured sections.

    Returns:
        {
            "skills": [
                {"skill": "...", "confidence": float, "source": section}
            ],
            "raw_matches": [...]
        }
    """

    if not sections:
        return {"skills": [], "raw_matches": []}

    collected = {}
    raw_debug = []

    for section_name, text in sections.items():

        if section_name not in SKILL_SOURCE_SECTIONS:
            continue

        if not text:
            continue

        cleaned = clean_skill_text(text)

        annotated = skill_extractor.annotate(cleaned)
        results = annotated.get("results", {})

        full_matches = results.get("full_matches", [])
        ngram_matches = results.get("ngram_scored", [])

        match_count = 0

        # -----------------------------
        # 1. Full matches (high confidence)
        # -----------------------------
        for entity in full_matches:
            skill_name = entity.get("doc_node_value", "").lower()
            score = float(entity.get("score", 1.0))

            if not skill_name:
                continue

            match_count += 1

            # keep best confidence per skill
            if skill_name not in collected or score > collected[skill_name]["confidence"]:
                collected[skill_name] = {
                    "skill": skill_name,
                    "confidence": round(score, 3),
                    "source": section_name
                }

        # -----------------------------
        # 2. N-gram matches (lower confidence)
        # -----------------------------
        for entity in ngram_matches:
            skill_name = entity.get("doc_node_value", "").lower()
            score = float(entity.get("score", 0.5))

            if not skill_name:
                continue

            # ignore weak matches
            if score < 0.3:
                continue

            match_count += 1

            if skill_name not in collected or score > collected[skill_name]["confidence"]:
                collected[skill_name] = {
                    "skill": skill_name,
                    "confidence": round(score, 3),
                    "source": section_name
                }

        # debug info
        raw_debug.append({
            "section": section_name,
            "text": cleaned[:200],
            "matches": match_count
        })

    # -----------------------------
    # 3. Optional filtering (VERY important)
    # -----------------------------
    STOP_SKILLS = {
        "analysis", "system", "data", "process", "operations",
        "communication", "team", "business", "support"
    }

    filtered = [
        v for k, v in collected.items()
        if k not in STOP_SKILLS and len(k) > 2
    ]

    return {
        "skills": filtered,
        "raw_matches": raw_debug
    }