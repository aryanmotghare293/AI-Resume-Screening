"""
Skill Extraction Engine
Comprehensive skill dictionary with NLP-based extractor
that matches technical and soft skills from text.
Returns structured, categorized JSON output.
"""

import re

# ---------------------------------------------------------------------------
# Skill Dictionary — organised by category
# ---------------------------------------------------------------------------

SKILL_DATABASE: dict[str, list[str]] = {
    "Programming Languages": [
        "Python", "Java", "C++", "C#", "C", "JavaScript", "TypeScript",
        "R", "Go", "Rust", "Kotlin", "Swift", "Scala", "Ruby", "PHP",
        "MATLAB", "Perl", "Shell", "Bash", "Dart", "Lua",
    ],
    "Data Science & ML": [
        "Machine Learning", "Deep Learning", "Natural Language Processing",
        "NLP", "Computer Vision", "Reinforcement Learning",
        "Time Series Analysis", "Recommendation Systems",
        "Feature Engineering", "Model Deployment", "MLOps",
        "Statistical Modeling", "A/B Testing", "Data Mining",
        "Predictive Modeling", "Artificial Intelligence", "AI",
        "Generative AI", "GenAI", "LLM", "Large Language Models",
        "Prompt Engineering", "RAG", "Fine-tuning",
    ],
    "ML Frameworks": [
        "TensorFlow", "PyTorch", "Scikit-learn", "Keras", "XGBoost",
        "LightGBM", "CatBoost", "Hugging Face", "OpenCV", "YOLO",
        "LangChain", "LlamaIndex", "Transformers", "JAX", "FastAI",
        "Stable Diffusion", "Sentence Transformers",
    ],
    "Data & Analytics": [
        "SQL", "MySQL", "PostgreSQL", "MongoDB", "Cassandra", "Redis",
        "Elasticsearch", "Neo4j", "DynamoDB", "SQLite",
        "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn",
        "Plotly", "Power BI", "Tableau", "Excel", "Google Sheets",
        "Apache Spark", "PySpark", "Hadoop", "Hive", "Kafka",
        "Airflow", "dbt", "Snowflake", "BigQuery", "Redshift",
        "Data Warehousing", "ETL", "Data Pipeline",
    ],
    "Web & Software Development": [
        "HTML", "CSS", "React", "Angular", "Vue.js", "Next.js",
        "Node.js", "Express.js", "Django", "Flask", "FastAPI",
        "Spring Boot", "REST API", "GraphQL", "Microservices",
        "Streamlit", "Gradio",
    ],
    "Cloud & DevOps": [
        "AWS", "Azure", "GCP", "Google Cloud",
        "Docker", "Kubernetes", "Jenkins", "GitHub Actions",
        "CI/CD", "Terraform", "Ansible",
        "AWS Lambda", "AWS S3", "AWS EC2", "AWS SageMaker",
        "Azure ML", "Google Vertex AI",
        "Linux", "Nginx",
    ],
    "Tools & Platforms": [
        "Git", "GitHub", "GitLab", "Bitbucket",
        "Jira", "Confluence", "Notion", "Slack",
        "Jupyter", "VS Code", "PyCharm",
        "Postman", "Swagger", "Figma",
        "MLflow", "Weights & Biases", "DVC",
    ],
    "Data Structures & Algorithms": [
        "DSA", "Data Structures", "Algorithms",
        "Dynamic Programming", "Graph Algorithms",
        "Sorting Algorithms", "Binary Search", "Recursion",
        "Linked List", "Trees", "Heaps", "Hashing",
    ],
    "Soft Skills": [
        "Communication", "Leadership", "Teamwork", "Problem Solving",
        "Critical Thinking", "Time Management", "Adaptability",
        "Project Management", "Agile", "Scrum", "Kanban",
        "Public Speaking", "Presentation", "Technical Writing",
        "Collaboration", "Mentoring",
    ],
}

# Flattened set for quick lookup
_ALL_SKILLS_FLAT: set[str] = set()
for _skills in SKILL_DATABASE.values():
    for _s in _skills:
        _ALL_SKILLS_FLAT.add(_s.lower())


# ---------------------------------------------------------------------------
# Multi-word & abbreviation handling
# ---------------------------------------------------------------------------

def _build_skill_pattern(skill: str) -> re.Pattern:
    """
    Build a regex pattern for a skill that handles:
    - word boundaries
    - case-insensitive matching
    - optional hyphens/dots/spaces in multi-word skills
    """
    escaped = re.escape(skill)
    # Allow flexible whitespace / hyphens / dots between words
    pattern = escaped.replace(r"\ ", r"[\s\-\.]*")
    return re.compile(rf"\b{pattern}\b", re.IGNORECASE)


# Pre-compile patterns (longest first for greedy matching)
_SKILL_PATTERNS: list[tuple[str, str, re.Pattern]] = []
for _cat, _skills in SKILL_DATABASE.items():
    for _s in sorted(_skills, key=len, reverse=True):
        _SKILL_PATTERNS.append((_cat, _s, _build_skill_pattern(_s)))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_skills(text: str) -> list[str]:
    """
    Extract skills from arbitrary text.
    Returns a deduplicated list of matched skill names.
    """
    found: dict[str, str] = {}  # lowercase -> canonical name
    for _, canonical, pattern in _SKILL_PATTERNS:
        if canonical.lower() not in found and pattern.search(text):
            found[canonical.lower()] = canonical
    return list(found.values())


def categorize_skills(skills: list[str]) -> dict[str, list[str]]:
    """
    Group a flat list of skills into their categories.
    Returns {category: [skills]}.
    """
    result: dict[str, list[str]] = {}
    skill_lower_map = {s.lower(): s for s in skills}

    for category, db_skills in SKILL_DATABASE.items():
        matched = [
            skill_lower_map[s.lower()]
            for s in db_skills
            if s.lower() in skill_lower_map
        ]
        if matched:
            result[category] = matched
    return result


def extract_skills_from_jd(jd_text: str) -> list[str]:
    """Extract skills specifically from a job description."""
    return extract_skills(jd_text)


def get_skill_summary(text: str) -> dict:
    """
    Convenience function: extract and categorize skills from text.
    Returns {skills: [...], categorized: {category: [...]}, count: int}.
    """
    skills = extract_skills(text)
    categorized = categorize_skills(skills)
    return {
        "skills": skills,
        "categorized": categorized,
        "count": len(skills),
    }
