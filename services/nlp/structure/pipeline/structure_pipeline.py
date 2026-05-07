from .regex_splitter import regex_split
from .gemini_extractor import extract_missing_sections
from .schema_merger import merge_sections
from .residual_builder import build_residual_text
from .schema_utils import get_missing_fields
from ..cleaning.noise_filter import clean_text


def run_structure_pipeline(text):

    cleaned = clean_text(text)

    # -----------------------------------------
    # 1. Regex extraction
    # -----------------------------------------
    regex_schema, regex_conf, unknown_headers = regex_split(cleaned)

    # -----------------------------------------
    # 2. Determine missing fields
    # -----------------------------------------
    missing_fields = get_missing_fields(regex_schema)

    # -----------------------------------------
    # 3. Build residual text
    # -----------------------------------------
    residual_text = build_residual_text(
        cleaned,
        regex_schema
    )

    # -----------------------------------------
    # 4. AI extraction
    # -----------------------------------------
    gemini_output = extract_missing_sections(
        residual_text,
        missing_fields
    )

    # -----------------------------------------
    # 5. Merge outputs
    # -----------------------------------------
    final_schema = merge_sections(
        regex_schema,
        gemini_output
    )

    return {
        "method": "hybrid",
        "sections": final_schema,
        "regex_conf": regex_conf
    }