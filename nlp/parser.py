from regex_splitter import regex_split
from nlp_splitter import nlp_split
from schema import PARSER_VERSION
from logger import log_event

def parse_job(text, row_id, logs):
    
    # Step 1 — regex attempt
    regex_result, regex_conf = regex_split(text)

    if regex_result and regex_conf > 0:
        log_event(logs, row_id, "regex", "regex_success", regex_conf)
        return {
            "parser_version": PARSER_VERSION,
            "method": "regex",
            "confidence": regex_conf,
            "sections": regex_result
        }

    # Step 2 — fallback NLP
    nlp_result, nlp_conf = nlp_split(text)

    log_event(logs, row_id, "nlp", "fallback_used", nlp_conf)

    return {
        "parser_version": PARSER_VERSION,
        "method": "nlp",
        "confidence": nlp_conf,
        "sections": nlp_result
    }