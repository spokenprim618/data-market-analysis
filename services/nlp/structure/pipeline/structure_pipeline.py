from services.nlp.structure.preprocessing.regex_splitter import regex_split

from services.nlp.structure.extractors.structure_extractor import (
    extract_missing_sections
)

from services.util.structure_utils.schema.schema_mergers.final_merger import (
    merge_sections
)

from services.util.structure_utils.schema.schema_missing.missing_schema import (
    get_missing_fields
)

from services.util.structure_utils.core.noise_filter import clean_text

from services.util.structure_utils.core.residual_builder import (
    build_residual_text
)

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