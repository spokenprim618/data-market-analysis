import json
from google import genai
from prompts.extraction_prompts import EXTRACTION_PROMPT

client = genai.Client(api_key="YOUR_API_KEY")


def extract_missing_sections(text, missing_fields):

    prompt = EXTRACTION_PROMPT.format(
        requested_fields=", ".join(missing_fields),
        description=text
    )

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    raw = response.text.strip()

    try:
        return json.loads(raw)
    except:
        return {}