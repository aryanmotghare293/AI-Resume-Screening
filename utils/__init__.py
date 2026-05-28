"""
Utils Package — AI Resume Screening & ATS Optimization
Provides modules for resume parsing, NLP processing, skill extraction,
ATS scoring, skill gap analysis, and Generative AI integration.
"""

from utils.parser import extract_text, parse_resume_sections
from utils.nlp_engine import preprocess_pipeline, extract_keywords, clean_text
from utils.skill_extractor import extract_skills, categorize_skills, extract_skills_from_jd
from utils.ats_score import calculate_ats_score, get_score_verdict
from utils.skill_gap import analyze_skill_gap, suggest_certifications, suggest_projects, suggest_tools
from utils.genai_helper import (
    init_gemini,
    improve_resume_bullets,
    optimize_ats_keywords,
    generate_interview_questions,
    generate_career_roadmap,
    generate_resume_summary,
)
