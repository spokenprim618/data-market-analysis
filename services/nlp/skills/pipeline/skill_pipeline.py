from services.nlp.skills.extractors.skill_extractor import extract_skills


def _truncate_at_line_or_period(text):
    """
    Keep only the first segment of text up to a newline or period.
    """
    if not isinstance(text, str):
        return text

    stripped = text.strip()
    if not stripped:
        return stripped

    newline_idx = stripped.find("\n")
    period_idx = stripped.find(".")

    cut_points = [i for i in (newline_idx, period_idx) if i != -1]
    if not cut_points:
        return stripped

    cut_idx = min(cut_points)
    segment = stripped[:cut_idx + (1 if cut_idx == period_idx else 0)].strip()
    return segment or stripped


def run_skills_pipeline(structure_output):
    """
    Takes structured sections and extracts skills
    """

    sections = structure_output.get("sections", {})
    job_title = structure_output.get("job_title")
    company_title = structure_output.get("company")

    section_snippets = {}
    for section_name, section_text in sections.items():
        if isinstance(section_text, str):
            section_snippets[section_name] = _truncate_at_line_or_period(section_text)
        else:
            section_snippets[section_name] = section_text

    skills_output = extract_skills(section_snippets)

    for item in skills_output.get("skills", []):
        item["job_title"] = job_title
        item["company"] = company_title
        source_section = item.get("source")
        item["section_text"] = section_snippets.get(source_section)

    for item in skills_output.get("raw_matches", []):
        item["job_title"] = job_title

    return {
        "job_title": job_title,
        "company": company_title,
        "sections_for_skills": section_snippets,
        "skills": skills_output["skills"],
        "raw_matches": skills_output["raw_matches"]
    }