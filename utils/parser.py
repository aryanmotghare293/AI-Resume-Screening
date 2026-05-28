"""
Resume Parser Module
Extracts text from PDF/DOCX files and parses structured sections
(name, contact, skills, education, experience, projects, certifications).
"""

import re
import pdfplumber
import docx2txt


# ---------------------------------------------------------------------------
# Text Extraction
# ---------------------------------------------------------------------------

def extract_text_from_pdf(uploaded_file) -> str:
    """Extract text from an uploaded PDF using pdfplumber."""
    text = ""
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")
    return text.strip()


def extract_text_from_docx(uploaded_file) -> str:
    """Extract text from an uploaded DOCX file."""
    try:
        text = docx2txt.process(uploaded_file)
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from DOCX: {e}")
    return text.strip() if text else ""


def extract_text(uploaded_file) -> str:
    """
    Detect file type and dispatch to the correct extractor.
    Accepts a Streamlit UploadedFile object.
    """
    filename = uploaded_file.name.lower()
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX file.")


# ---------------------------------------------------------------------------
# Section Header Patterns
# ---------------------------------------------------------------------------

SECTION_PATTERNS = {
    "education": [
        r"\b(education|academic|qualification|degree|university|college)\b"
    ],
    "experience": [
        r"\b(experience|employment|work\s*history|professional\s*experience|career)\b"
    ],
    "skills": [
        r"\b(skills|technical\s*skills|core\s*competencies|technologies|proficiencies)\b"
    ],
    "projects": [
        r"\b(projects|personal\s*projects|academic\s*projects|key\s*projects)\b"
    ],
    "certifications": [
        r"\b(certifications?|certificates?|licenses?|accreditations?)\b"
    ],
    "summary": [
        r"\b(summary|objective|profile|about\s*me|professional\s*summary|career\s*objective)\b"
    ],
}


def _find_section(lines: list[str], patterns: list[str]) -> list[str]:
    """Find lines belonging to a section based on header patterns."""
    section_lines = []
    capturing = False
    all_section_re = re.compile(
        "|".join(p for pats in SECTION_PATTERNS.values() for p in pats),
        re.IGNORECASE,
    )

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if capturing:
                section_lines.append("")
            continue

        # Check if this line is a section header
        is_header = bool(all_section_re.search(stripped)) and len(stripped.split()) <= 6

        if any(re.search(p, stripped, re.IGNORECASE) for p in patterns) and len(stripped.split()) <= 6:
            capturing = True
            continue
        elif is_header and capturing:
            # Hit a different section header — stop capturing
            break
        elif capturing:
            section_lines.append(stripped)

    return section_lines


# ---------------------------------------------------------------------------
# Contact Info Extraction
# ---------------------------------------------------------------------------

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
PHONE_RE = re.compile(r"[\+]?[\d\s\-\(\)]{7,15}")
LINKEDIN_RE = re.compile(r"(?:https?://)?(?:www\.)?linkedin\.com/in/[\w\-]+", re.I)


def _extract_contact(text: str) -> dict:
    """Extract email, phone, and LinkedIn from resume text."""
    emails = EMAIL_RE.findall(text)
    phones = PHONE_RE.findall(text)
    linkedin = LINKEDIN_RE.findall(text)
    return {
        "email": emails[0] if emails else None,
        "phone": phones[0].strip() if phones else None,
        "linkedin": linkedin[0] if linkedin else None,
    }


def _extract_name(lines: list[str]) -> str:
    """
    Heuristic: the first non-empty, non-contact, short line is likely the name.
    """
    for line in lines[:5]:
        stripped = line.strip()
        if not stripped:
            continue
        if EMAIL_RE.search(stripped) or PHONE_RE.search(stripped):
            continue
        if len(stripped.split()) <= 5 and not any(
            c.isdigit() for c in stripped
        ):
            return stripped
    return "Unknown"


# ---------------------------------------------------------------------------
# Main Parser
# ---------------------------------------------------------------------------

def parse_resume_sections(text: str) -> dict:
    """
    Parse resume text into structured sections.
    Returns a dict with keys: name, contact, summary, skills, education,
    experience, projects, certifications, raw_text.
    """
    lines = text.split("\n")

    name = _extract_name(lines)
    contact = _extract_contact(text)

    sections = {}
    for key, patterns in SECTION_PATTERNS.items():
        section_lines = _find_section(lines, patterns)
        sections[key] = "\n".join(section_lines).strip()

    return {
        "name": name,
        "contact": contact,
        "summary": sections.get("summary", ""),
        "skills": sections.get("skills", ""),
        "education": sections.get("education", ""),
        "experience": sections.get("experience", ""),
        "projects": sections.get("projects", ""),
        "certifications": sections.get("certifications", ""),
        "raw_text": text,
    }
