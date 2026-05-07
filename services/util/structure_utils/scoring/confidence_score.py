import re


def score_sentence(sentence, schema):
    """
    Confidence = how much of this sentence is already covered by schema.
    """

    if not sentence:
        return 0.0

    sentence_l = sentence.lower()

    matched = 0
    total = 0

    for value in schema.values():

        if value is None:
            continue

        if isinstance(value, list):
            for item in value:
                if not item:
                    continue

                total += 1
                if str(item).lower() in sentence_l:
                    matched += 1

        elif isinstance(value, str):
            total += 1
            if value.lower() in sentence_l:
                matched += 1

    if total == 0:
        return 0.0

    # normalize + soften (IMPORTANT)
    return matched / max(total, 1)