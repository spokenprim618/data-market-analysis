from .regex_splitter import regex_split
from .gemini_extractor import extract_missing_sections
from .schema_merger import merge_sections
from .residual_builder import build_residual_text
from .schema_utils import get_missing_fields
from ..cleaning.noise_filter import clean_text
from .confidence_score import score_sentence


def compute_residual_confidence(text, schema):
    """
    Measures how much of the remaining text is already explained.
    Lower = better residual (more useful to Gemini)
    """

    if not text:
        return 0.0

    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)

    scores = []

    for s in sentences:
        s = s.strip()
        if len(s) < 10:
            continue

        scores.append(score_sentence(s, schema))

    if not scores:
        return 0.0

    return sum(scores) / len(scores)


def run_structure_pipeline(text):

    cleaned = clean_text(text)

    # -----------------------------------------
    # 1. Regex extraction
    # -----------------------------------------
    regex_schema, regex_conf, unknown_headers = regex_split(cleaned)

    # -----------------------------------------
    # 2. Missing fields (CRITICAL TRACKING)
    # -----------------------------------------
    missing_fields = get_missing_fields(regex_schema)

    # -----------------------------------------
    # 3. Residual text (now implicitly filtered)
    # -----------------------------------------
    residual_text = build_residual_text(
        cleaned,
        regex_schema
    )

    residual_conf = compute_residual_confidence(
        residual_text,
        regex_schema
    )

    # -----------------------------------------
    # 4. Gemini extraction (only if needed)
    # -----------------------------------------
    gemini_output, gemini_conf = extract_missing_sections(
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

    # -----------------------------------------
    # 6. FINAL confidence model
    # -----------------------------------------

    missing_weight = len(missing_fields)

    final_conf = (
        regex_conf * 0.6 +
        gemini_conf * 0.3 +
        (1 - residual_conf) * 0.1
    )

    # -----------------------------------------
    # 7. Return full diagnostics
    # -----------------------------------------
    return {
        "method": "hybrid",

        "sections": final_schema,

        # -------------------------------------
        # Core confidence tracking
        # -------------------------------------
        "confidence": {
            "regex_conf": regex_conf,
            "gemini_conf": gemini_conf,
            "residual_conf": residual_conf,
            "final_conf": final_conf
        },

        # -------------------------------------
        # Field tracking
        # -------------------------------------
        "missing_fields": missing_fields,
        "missing_count": len(missing_fields),

        # -------------------------------------
        # Debugging
        # -------------------------------------
        "unknown_headers": unknown_headers,
        "gemini_used": len(missing_fields) > 0
    }