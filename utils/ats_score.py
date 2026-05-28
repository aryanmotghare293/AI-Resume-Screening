"""
ATS Score Calculation Module
Computes an ATS compatibility score using a weighted combination of:
  40%  — skill match
  25%  — experience relevance
  15%  — project relevance
  10%  — education fit
  10%  — formatting quality
Also provides semantic similarity via sentence-transformers.
"""

import re
import math

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.skill_extractor import extract_skills, extract_skills_from_jd

# ---------------------------------------------------------------------------
# Optional: sentence-transformers for semantic score
# ---------------------------------------------------------------------------
_SEMANTIC_MODEL = None


def _load_semantic_model():
    """Lazy-load the sentence-transformer model."""
    global _SEMANTIC_MODEL
    if _SEMANTIC_MODEL is None:
        try:
            from sentence_transformers import SentenceTransformer
            _SEMANTIC_MODEL = SentenceTransformer(
                "all-MiniLM-L6-v2",
                local_files_only=True,
            )
        except Exception:
            _SEMANTIC_MODEL = False  # Mark as unavailable
    return _SEMANTIC_MODEL


# ---------------------------------------------------------------------------
# Sub-score calculators
# ---------------------------------------------------------------------------

def calculate_skill_match(resume_text: str, jd_text: str) -> dict:
    """
    Calculate skill overlap between resume and JD.
    Returns {score (0-100), matched, missing, total_jd}.
    """
    resume_skills = set(s.lower() for s in extract_skills(resume_text))
    jd_skills = set(s.lower() for s in extract_skills_from_jd(jd_text))

    if not jd_skills:
        return {"score": 50.0, "matched": [], "missing": [], "total_jd": 0}

    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills

    score = (len(matched) / len(jd_skills)) * 100

    return {
        "score": round(min(score, 100), 1),
        "matched": sorted(matched),
        "missing": sorted(missing),
        "total_jd": len(jd_skills),
    }


def calculate_experience_match(resume_text: str, jd_text: str) -> float:
    """
    TF-IDF cosine similarity on experience-related content (0-100).
    """
    return _tfidf_similarity(resume_text, jd_text)


def calculate_project_relevance(resume_text: str, jd_text: str) -> float:
    """
    TF-IDF cosine similarity focused on project descriptions (0-100).
    """
    return _tfidf_similarity(resume_text, jd_text)


def calculate_education_fit(resume_text: str, jd_text: str) -> float:
    """
    Check for education keyword overlap.
    """
    edu_keywords = {
        "bachelor", "master", "phd", "doctorate", "b.tech", "m.tech",
        "b.e.", "m.e.", "bsc", "msc", "mba", "bca", "mca",
        "computer science", "data science", "information technology",
        "statistics", "mathematics", "engineering", "artificial intelligence",
    }

    resume_lower = resume_text.lower()
    jd_lower = jd_text.lower()

    jd_edu = {kw for kw in edu_keywords if kw in jd_lower}
    if not jd_edu:
        return 70.0  # Neutral if JD doesn't specify

    resume_edu = {kw for kw in edu_keywords if kw in resume_lower}
    matched = resume_edu & jd_edu
    score = (len(matched) / len(jd_edu)) * 100 if jd_edu else 70.0
    return round(min(score, 100), 1)


def assess_formatting_quality(resume_text: str) -> float:
    """
    Heuristic formatting quality check (0-100):
    - Has email, phone
    - Has section headings
    - Reasonable length
    - Uses bullet points
    - Not overly cluttered
    """
    score = 0
    checks = 0
    total_checks = 6

    # Has email?
    if re.search(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}", resume_text):
        score += 1
    checks += 1

    # Has phone?
    if re.search(r"[\+]?\d[\d\s\-\(\)]{6,}\d", resume_text):
        score += 1
    checks += 1

    # Has section headings?
    headings = ["education", "experience", "skills", "projects"]
    heading_count = sum(
        1 for h in headings if re.search(rf"(?i)\b{h}\b", resume_text)
    )
    if heading_count >= 3:
        score += 1
    elif heading_count >= 2:
        score += 0.5
    checks += 1

    # Reasonable length (300-5000 words)
    word_count = len(resume_text.split())
    if 300 <= word_count <= 5000:
        score += 1
    elif 150 <= word_count < 300:
        score += 0.5
    checks += 1

    # Uses bullet-like patterns
    bullet_patterns = resume_text.count("•") + resume_text.count("-") + resume_text.count("●")
    if bullet_patterns >= 5:
        score += 1
    elif bullet_patterns >= 2:
        score += 0.5
    checks += 1

    # Has quantifiable achievements (numbers)
    numbers = re.findall(r"\d+%|\d+\+|\d+x|\$\d+", resume_text)
    if len(numbers) >= 3:
        score += 1
    elif len(numbers) >= 1:
        score += 0.5
    checks += 1

    return round((score / total_checks) * 100, 1)


def calculate_semantic_similarity(resume_text: str, jd_text: str) -> float:
    """
    Compute semantic similarity using sentence-transformers (0-100).
    Falls back to TF-IDF if model unavailable.
    """
    model = _load_semantic_model()
    if model and model is not False:
        try:
            # Truncate texts to avoid memory issues
            r = resume_text[:2000]
            j = jd_text[:2000]
            embeddings = model.encode([r, j])
            sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
            return float(round(max(0, min(float(sim) * 100, 100)), 1))
        except Exception:
            pass

    # Fallback to TF-IDF
    return _tfidf_similarity(resume_text, jd_text)


# ---------------------------------------------------------------------------
# Main ATS Score
# ---------------------------------------------------------------------------

def calculate_ats_score(resume_data: dict, jd_text: str) -> dict:
    """
    Calculate the composite ATS score.
    
    Weights:
        40% — skill match
        25% — experience relevance
        15% — project relevance
        10% — education fit
        10% — formatting quality
    
    Returns {
        total_score, breakdown, semantic_score, skill_details, verdict
    }
    """
    raw_text = resume_data.get("raw_text", "")
    experience_text = resume_data.get("experience", "") or raw_text
    project_text = resume_data.get("projects", "") or raw_text
    education_text = resume_data.get("education", "") or raw_text

    # Sub-scores
    skill_result = calculate_skill_match(raw_text, jd_text)
    skill_score = skill_result["score"]
    experience_score = calculate_experience_match(experience_text, jd_text)
    project_score = calculate_project_relevance(project_text, jd_text)
    education_score = calculate_education_fit(education_text, jd_text)
    formatting_score = assess_formatting_quality(raw_text)
    semantic_score = calculate_semantic_similarity(raw_text, jd_text)

    # Weighted total
    total = (
        skill_score * 0.40
        + experience_score * 0.25
        + project_score * 0.15
        + education_score * 0.10
        + formatting_score * 0.10
    )
    total = round(min(total, 100), 1)

    # Verdict
    verdict = get_score_verdict(total)

    return {
        "total_score": total,
        "breakdown": {
            "Skill Match (40%)": round(skill_score, 1),
            "Experience (25%)": round(experience_score, 1),
            "Projects (15%)": round(project_score, 1),
            "Education (10%)": round(education_score, 1),
            "Formatting (10%)": round(formatting_score, 1),
        },
        "semantic_score": semantic_score,
        "skill_details": skill_result,
        "verdict": verdict,
    }


def get_score_verdict(score: float) -> dict:
    """Return verdict label, colour, and recommendation."""
    if score >= 75:
        return {
            "label": "✅ Strong Match",
            "css_class": "verdict-pass",
            "recommendation": (
                "Your resume is well-aligned with this job description. "
                "Focus on fine-tuning keywords and quantifying achievements."
            ),
        }
    elif score >= 50:
        return {
            "label": "⚠️ Moderate Match",
            "css_class": "verdict-moderate",
            "recommendation": (
                "Your resume has partial alignment. Add missing skills, "
                "tailor your experience bullets, and include relevant projects."
            ),
        }
    else:
        return {
            "label": "❌ Weak Match",
            "css_class": "verdict-fail",
            "recommendation": (
                "Significant gaps detected. Rewrite your resume to target this role: "
                "add required skills, relevant projects, and role-specific keywords."
            ),
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _tfidf_similarity(text_a: str, text_b: str) -> float:
    """Compute TF-IDF cosine similarity between two texts (0-100)."""
    if not text_a.strip() or not text_b.strip():
        return 0.0
    try:
        vectorizer = TfidfVectorizer(stop_words="english", max_features=500)
        matrix = vectorizer.fit_transform([text_a, text_b])
        sim = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        return float(round(max(0, min(float(sim) * 100, 100)), 1))
    except ValueError:
        return 0.0
