SECTION_DEFINITIONS = {
    "responsibilities":
        "job duties, tasks, operational work",

    "requirements":
        "required qualifications, required skills, must-have abilities",

    "experience":
        "years of experience, prior background expectations",

    "benefits":
        "salary, perks, insurance, PTO, compensation",

    "about":
        "company mission, company overview, culture"
}

def build_missing_section_prompt(
    missing_sections,
    text
):
    section_descriptions = []

    for section in missing_sections:

        desc = SECTION_DEFINITIONS.get(
            section,
            "unknown"
        )

        section_descriptions.append(
            f"- {section}: {desc}"
        )

    section_text = "\n".join(section_descriptions)

    return f"""
You are extracting missing information
from a job posting.

ONLY extract information relevant
to the requested sections.

Requested sections:
{section_text}

Rules:
- Return ALL matching text
- Do NOT summarize aggressively
- Do NOT invent information
- Multiple matches per section are allowed
- Use empty arrays if nothing is found

Return ONLY valid JSON.

Example:
{{
  "benefits": [
    "401k matching",
    "Health insurance"
  ],

  "requirements": [
    "Python experience",
    "SQL knowledge"
  ]
}}

Job Posting:
{text}
"""