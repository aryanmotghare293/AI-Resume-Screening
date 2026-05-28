"""
Generative AI Helper Module — Google Gemini Integration
Uses the modern `google-genai` SDK (Gemini 2.5 Flash) for:
- Resume bullet point improvement
- ATS keyword optimisation
- Interview question generation
- Career roadmap generation
- Professional summary generation
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()

# ---------------------------------------------------------------------------
# Gemini Client (lazy initialisation)
# ---------------------------------------------------------------------------
_CLIENT = None
_MODEL = "gemini-2.5-flash"


def init_gemini():
    """
    Initialise and return the Gemini client.
    Returns None if the API key is not configured.
    """
    global _CLIENT
    if _CLIENT is not None:
        return _CLIENT

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key or api_key == "your_gemini_api_key_here":
        return None

    try:
        from google import genai
        _CLIENT = genai.Client(api_key=api_key)
        return _CLIENT
    except Exception as e:
        print(f"[GenAI] Failed to initialise Gemini client: {e}")
        return None


def _generate(prompt: str, max_tokens: int = 4096) -> str | None:
    """Internal helper to call Gemini's generate_content API."""
    client = init_gemini()
    if client is None:
        return None
    try:
        from google.genai import types
        response = client.models.generate_content(
            model=_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=max_tokens,
                temperature=0.7,
            ),
        )
        return response.text
    except Exception as e:
        print(f"[GenAI] Generation error: {e}")
        return None


# ---------------------------------------------------------------------------
# Resume Bullet Improvement
# ---------------------------------------------------------------------------

def improve_resume_bullets(resume_text: str, jd_text: str) -> str | None:
    """
    Use Gemini to rewrite weak resume bullet points into powerful,
    quantified, action-based statements optimised for ATS.
    """
    prompt = f"""You are an expert resume writer and ATS optimisation specialist.

TASK: Rewrite the resume bullet points below to make them:
1. Start with strong action verbs
2. Include quantified impact (%, $, numbers)
3. Be ATS-friendly with relevant keywords from the job description
4. Be concise (one line each, max 20 words)
5. Sound achievement-oriented, not task-oriented

JOB DESCRIPTION:
{jd_text[:1500]}

RESUME CONTENT:
{resume_text[:2000]}

FORMAT YOUR RESPONSE AS:
For each improved bullet, show:
**Original:** [original text]
**Improved:** [improved text]

Provide at least 6 improved bullet points. Focus on the weakest bullets first.
If a bullet is already strong, note it as "Already Strong" and suggest only minor tweaks.
"""
    return _generate(prompt)


# ---------------------------------------------------------------------------
# ATS Keyword Optimisation
# ---------------------------------------------------------------------------

def optimize_ats_keywords(resume_text: str, jd_text: str) -> str | None:
    """
    Suggest specific keywords and phrases from the JD that should
    be incorporated into the resume for higher ATS matching.
    """
    prompt = f"""You are an ATS (Applicant Tracking System) optimisation expert.

TASK: Analyse the job description and resume below. Identify keywords and phrases
from the JD that are MISSING from the resume and suggest WHERE to add them.

JOB DESCRIPTION:
{jd_text[:1500]}

RESUME CONTENT:
{resume_text[:2000]}

FORMAT YOUR RESPONSE AS:
### Missing Keywords
List the top 10-15 keywords/phrases missing from the resume.

### Where to Add Them
For each keyword, suggest which resume section to add it to and provide an example sentence.

### Quick Wins
List 5 easy changes that will immediately boost the ATS score.
"""
    return _generate(prompt)


# ---------------------------------------------------------------------------
# Interview Questions Generator
# ---------------------------------------------------------------------------

def generate_interview_questions(
    skills: list[str],
    projects: str,
    target_role: str,
    missing_skills: list[str],
) -> str | None:
    """
    Generate role-specific interview questions organised by category:
    HR, Technical, SQL, ML/NLP, and Project-based.
    """
    skills_str = ", ".join(skills[:20]) if skills else "Not specified"
    missing_str = ", ".join(missing_skills[:10]) if missing_skills else "None"

    prompt = f"""You are a senior technical interviewer.

Generate interview questions for a **{target_role}** candidate with the following profile:

**Skills:** {skills_str}
**Projects:** {projects[:800] if projects else 'Not specified'}
**Skills to assess (gaps):** {missing_str}

Generate questions in these exact categories:

### 🤝 HR & Behavioral Questions (5 questions)
Include questions about teamwork, challenges, career goals.

### 💻 Technical Questions (5 questions)
Core technical questions relevant to {target_role}. Include difficulty level [Easy/Medium/Hard].

### 🗄️ SQL Questions (3 questions)
Practical SQL problems. Include difficulty level.

### 🤖 ML / NLP / AI Questions (4 questions)
Based on the candidate's skills. Include difficulty level.

### 📋 Project-Based Viva Questions (4 questions)
Questions specifically about their projects listed above.

For each question, provide:
- The question
- Difficulty: [Easy/Medium/Hard]
- Brief hint on what a good answer should cover (1-2 lines)
"""
    return _generate(prompt, max_tokens=4096)


# ---------------------------------------------------------------------------
# Career Roadmap
# ---------------------------------------------------------------------------

def generate_career_roadmap(resume_data: dict, target_role: str) -> str | None:
    """
    Generate a personalised career roadmap based on the candidate's
    current profile and target role.
    """
    skills = resume_data.get("skills", "Not specified")
    experience = resume_data.get("experience", "Not specified")
    education = resume_data.get("education", "Not specified")

    prompt = f"""You are a career coach and tech industry expert.

Create a detailed, personalised career roadmap for a candidate with this profile:

**Current Skills:** {skills[:500]}
**Experience:** {experience[:500]}
**Education:** {education[:300]}
**Target Role:** {target_role}

Provide the roadmap in this format:

### 🎯 Career Goal Analysis
Brief analysis of current position vs target role.

### 📅 30-Day Plan
Immediate action items — quick wins, certifications to start, skills to practice.

### 📅 60-Day Plan
Intermediate goals — projects to build, technologies to learn, networking.

### 📅 90-Day Plan
Advanced preparation — portfolio polish, interview prep, job applications.

### 🛤️ Long-term Growth Path
Career progression from the target role (Year 1, Year 3, Year 5).

### 🔧 Tools & Resources
Specific platforms, courses, and communities for each phase.

Make it practical, specific, and actionable. Use emojis for visual appeal.
"""
    return _generate(prompt, max_tokens=4096)


# ---------------------------------------------------------------------------
# Professional Summary Generator
# ---------------------------------------------------------------------------

def generate_resume_summary(resume_text: str, jd_text: str) -> str | None:
    """
    Generate an optimised professional summary/objective that aligns
    the candidate's experience with the target job description.
    """
    prompt = f"""You are an expert resume writer.

TASK: Write a compelling professional summary (3-4 sentences) for a resume that:
1. Highlights the candidate's strongest qualifications
2. Aligns with the job description keywords
3. Includes quantified achievements if possible
4. Starts with the candidate's professional identity

JOB DESCRIPTION:
{jd_text[:1000]}

RESUME CONTENT:
{resume_text[:1500]}

Write 2 versions:
### Version 1 (For Experienced Candidates)
[3-4 sentence professional summary]

### Version 2 (For Entry-Level / Fresh Graduates)
[3-4 sentence career objective]
"""
    return _generate(prompt, max_tokens=1024)
