from .regex_splitter import regex_split
from .semantic_splitter import fill_missing_sections
from ..cleaning.noise_filter import clean_text

def run_structure_pipeline(text):
    cleaned = clean_text(text)

    regex_result, regex_conf, _unknown_headers = regex_split(cleaned)

    if regex_result:
        sections, sem_conf = fill_missing_sections(cleaned, regex_result)
        method = "hybrid"
    else:
        sections, sem_conf = fill_missing_sections(cleaned, None)
        method = "semantic_only"

    return {
        "method": method,
        "sections": sections,
        "regex_conf": regex_conf,
        "semantic_conf": sem_conf
    }