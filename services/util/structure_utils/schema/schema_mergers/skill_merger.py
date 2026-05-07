def merge_skills(base, extracted):
    if base is None:
        base = {}
    if extracted is None:
        extracted = {}

    merged = dict(base)

    for category, items in extracted.items():

        if not isinstance(items, list):
            continue

        existing = merged.get(category, [])

        if not isinstance(existing, list):
            existing = []

        seen = set()
        combined = []

        for item in existing + items:
            if not item:
                continue

            norm = str(item).lower().strip()

            if norm in seen:
                continue

            seen.add(norm)
            combined.append(item)

        merged[category] = combined

    return merged