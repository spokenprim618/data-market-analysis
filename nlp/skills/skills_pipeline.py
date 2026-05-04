from .skill_extractor import extract_skills

def run_skills_pipeline(structure_output):
    """
    Takes structured sections and extracts skills
    """

    sections = structure_output.get("sections", {})

    skills_output = extract_skills(sections)

    return {
        "skills": skills_output["skills"],
        "raw_matches": skills_output["raw_matches"]
    }