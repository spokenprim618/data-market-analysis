def merge_job_sections(regex_schema, gemini_schema):
    if regex_schema is None:
        regex_schema = {}

    if gemini_schema is None:
        gemini_schema = {}

    merged = dict(regex_schema)

    for key, value in gemini_schema.items():

        if value in (None, "", []):
            continue

        existing = merged.get(key)

        if existing is None:
            merged[key] = value
            continue

        # list merge only
        if isinstance(existing, list) and isinstance(value, list):
            seen = set()
            combined = []

            for item in existing + value:
                if not item:
                    continue

                norm = str(item).lower().strip()

                if norm in seen:
                    continue

                seen.add(norm)
                combined.append(item)

            merged[key] = combined

    merged.setdefault("unknown", [])
    merged.setdefault("suggestions", [])

    return merged