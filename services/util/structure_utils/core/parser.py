from ..structure.regex_splitter import regex_split
from ..structure.semantic_splitter import fill_missing_sections
from ..skills.skill_extractor import extract_skills
from ..cleaning.noise_filter import clean_text
from .schema import PARSER_VERSION
from .logger import log_event


def parse_job(text, row_id, logs):

    # -------------------
    # 0. CLEANING LAYER
    # -------------------
    text = clean_text(text)

    # -----------------------------
    # 1. REGEX STRUCTURE LAYER
    # -----------------------------
    regex_result, regex_conf = regex_split(text)

    if regex_result:
        log_event(logs, row_id, "regex", "regex_success", regex_conf)
    else:
        log_event(logs, row_id, "regex", "regex_failed", 0.0)

    # -----------------------------
    # 2. SEMANTIC BACKFILL
    # -----------------------------
    if regex_result:
        sections, sem_conf = fill_missing_sections(text, regex_result)
        method = "hybrid"
    else:
        sections, sem_conf = fill_missing_sections(text, None)
        method = "semantic_only"

    log_event(logs, row_id, "semantic", "fill_complete", sem_conf)

    # -----------------------------
    # 🔒 2.5 GUARANTEE DICTIONARY
    # -----------------------------
    if not isinstance(sections, dict):
        sections = {
            "responsibilities": None,
            "requirements": None,
            "experience": None,
            "benefits": None,
            "about": None,
            "unknown": [],
            "suggestions": [],
            "sections_confidence": {}
        }

    # -----------------------------
    # 3. SKILL EXTRACTION
    # -----------------------------
    skills_output = extract_skills(sections)

    log_event(
        logs,
        row_id,
        "skills",
        "skill_extraction_complete",
        len(skills_output["skills"])
    )

    # -----------------------------
    # 4. FINAL CONFIDENCE
    # -----------------------------
    final_confidence = (
        (regex_conf * 0.5) +
        (sem_conf * 0.3) +
        (min(len(skills_output["skills"]), 10) / 10 * 0.2)
    )

    # -----------------------------
    # 5. OUTPUT STRUCTURE
    # -----------------------------
    return {
        "parser_version": PARSER_VERSION,
        "method": method,
        "confidence": round(final_confidence, 4),
        "sections": sections,
        "skills": skills_output["skills"]
    }