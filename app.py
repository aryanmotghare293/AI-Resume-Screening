"""
FastAPI backend for the AI Resume Screener.

This replaces the old Streamlit UI layer. The React frontend talks to the
endpoints under /api, and a built React app in frontend/dist can also be
served directly by this FastAPI process.
"""

import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from utils.ats_score import calculate_ats_score
from utils.genai_helper import (
    generate_career_roadmap,
    generate_interview_questions,
    generate_resume_summary,
    improve_resume_bullets,
    init_gemini,
    optimize_ats_keywords,
)
from utils.parser import extract_text_from_docx, extract_text_from_pdf, parse_resume_sections
from utils.skill_extractor import categorize_skills, extract_skills, extract_skills_from_jd
from utils.skill_gap import (
    analyze_skill_gap,
    get_learning_priority,
    suggest_certifications,
    suggest_projects,
    suggest_tools,
)

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"
API_VERSION = "2.0.0"


app = FastAPI(
    title="AI Resume Screener API",
    description="Backend API for Resume Screening and ATS Optimization",
    version=API_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
    ],
    allow_origin_regex=r"https?://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if (FRONTEND_DIST / "assets").exists():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIST / "assets"),
        name="frontend-assets",
    )


class AISuggestionsRequest(BaseModel):
    resume_text: str
    jd_text: str


class InterviewQuestionsRequest(BaseModel):
    skills: list[str]
    projects: str = ""
    target_role: str
    missing_skills: list[str] = []


class CareerRoadmapRequest(BaseModel):
    resume_data: dict
    target_role: str


def _extract_resume_text(file_path: str, filename: str) -> str:
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(file_path)
    if filename.endswith(".docx"):
        return extract_text_from_docx(file_path)
    raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")


def _build_recommendations(missing_skills: list[str], jd_text: str) -> dict:
    return {
        "certifications": suggest_certifications(missing_skills),
        "projects": suggest_projects(missing_skills),
        "tools": suggest_tools(missing_skills),
        "priorities": get_learning_priority(missing_skills, jd_text),
    }


@app.get("/api/health")
def health_check() -> dict:
    return {
        "status": "healthy",
        "gemini_connected": init_gemini() is not None,
        "version": API_VERSION,
    }


@app.post("/api/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    jd_text: str = Form(...),
    target_role: str = Form("Data Scientist"),
) -> dict:
    filename = (resume.filename or "").lower()
    if not filename.endswith((".pdf", ".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")

    if not jd_text.strip():
        raise HTTPException(status_code=400, detail="Job description is required.")

    tmp_path: str | None = None

    try:
        suffix = ".pdf" if filename.endswith(".pdf") else ".docx"
        content = await resume.read()
        if not content:
            raise HTTPException(status_code=400, detail="Uploaded resume file is empty.")

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        resume_text = _extract_resume_text(tmp_path, filename)
        if not resume_text or len(resume_text.strip()) < 50:
            raise HTTPException(
                status_code=422,
                detail="Could not extract sufficient text from the resume.",
            )

        resume_data = parse_resume_sections(resume_text)
        resume_skills = extract_skills(resume_text)
        jd_skills = extract_skills_from_jd(jd_text)
        ats_result = calculate_ats_score(resume_data, jd_text)
        gap_result = analyze_skill_gap(resume_text, jd_text)

        return {
            "resume_text": resume_text,
            "resume_data": resume_data,
            "resume_skills": resume_skills,
            "resume_skills_categorized": categorize_skills(resume_skills),
            "jd_skills": jd_skills,
            "ats_result": ats_result,
            "gap_result": gap_result,
            "recommendations": _build_recommendations(gap_result["missing"], jd_text),
            "target_role": target_role,
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}") from exc
    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass


@app.post("/api/ai-suggestions")
def ai_suggestions(req: AISuggestionsRequest) -> dict:
    if not init_gemini():
        raise HTTPException(
            status_code=503,
            detail="Gemini API key not configured. Add GEMINI_API_KEY to .env.",
        )

    return {
        "bullets": improve_resume_bullets(req.resume_text, req.jd_text),
        "keywords": optimize_ats_keywords(req.resume_text, req.jd_text),
        "summary": generate_resume_summary(req.resume_text, req.jd_text),
    }


@app.post("/api/interview-questions")
def interview_questions(req: InterviewQuestionsRequest) -> dict:
    if not init_gemini():
        raise HTTPException(
            status_code=503,
            detail="Gemini API key not configured. Add GEMINI_API_KEY to .env.",
        )

    questions = generate_interview_questions(
        skills=req.skills,
        projects=req.projects,
        target_role=req.target_role,
        missing_skills=req.missing_skills,
    )
    return {"questions": questions}


@app.post("/api/career-roadmap")
def career_roadmap(req: CareerRoadmapRequest) -> dict:
    if not init_gemini():
        raise HTTPException(
            status_code=503,
            detail="Gemini API key not configured. Add GEMINI_API_KEY to .env.",
        )

    roadmap = generate_career_roadmap(
        resume_data=req.resume_data,
        target_role=req.target_role,
    )
    return {"roadmap": roadmap}


@app.get("/{full_path:path}", include_in_schema=False)
def serve_react_app(full_path: str):
    if full_path.startswith("api"):
        raise HTTPException(status_code=404, detail="API route not found.")

    index_file = FRONTEND_DIST / "index.html"
    if not FRONTEND_DIST.exists() or not index_file.exists():
        return {
            "message": (
                "React build not found. Run `npm run build` inside frontend, "
                "or run the Vite dev server and use http://localhost:5173."
            )
        }

    requested_file = (FRONTEND_DIST / full_path).resolve()
    frontend_root = FRONTEND_DIST.resolve()

    try:
        requested_file.relative_to(frontend_root)
    except ValueError:
        raise HTTPException(status_code=404, detail="File not found.") from None

    if requested_file.is_file():
        return FileResponse(requested_file)

    return FileResponse(index_file)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
