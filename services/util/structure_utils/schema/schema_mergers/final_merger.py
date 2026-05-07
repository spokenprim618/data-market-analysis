from .job_merger import merge_job_sections
from .skill_merger import merge_skills


def merge_all(job_regex, job_gemini, skill_regex, skill_gemini):

    job = merge_job_sections(job_regex, job_gemini)
    skills = merge_skills(skill_regex, skill_gemini)

    return {
        "job": job,
        "skills": skills
    }