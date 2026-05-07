# schema_utils.py


def get_missing_fields(schema):
    """
    Returns fields still needing extraction.

    Ignores:
    - unknown
    - suggestions

    Returns:
        [
            "skills",
            "experience"
        ]
    """

    ignored = {
        "unknown",
        "suggestions"
    }

    missing = []

    for key, value in schema.items():

        if key in ignored:
            continue

        if value is None:
            missing.append(key)

    return missing