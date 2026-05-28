"""
Skill Gap Analysis Module
Compares JD skills vs resume skills and provides:
- matched / missing skills
- certification recommendations
- project suggestions
- tools & resources to learn
- learning priority ranking
"""

from utils.skill_extractor import extract_skills, extract_skills_from_jd, categorize_skills

# ---------------------------------------------------------------------------
# Certification Recommendations (curated mapping)
# ---------------------------------------------------------------------------

CERTIFICATION_MAP: dict[str, list[str]] = {
    "python": ["Google IT Automation with Python (Coursera)", "PCEP – Certified Entry-Level Python Programmer"],
    "java": ["Oracle Certified Professional Java SE Developer"],
    "javascript": ["Meta Front-End Developer (Coursera)", "freeCodeCamp JavaScript Certification"],
    "sql": ["Oracle Database SQL Certified Associate", "Google Data Analytics Certificate"],
    "machine learning": ["Stanford ML Specialization (Coursera)", "AWS Machine Learning Specialty"],
    "deep learning": ["Deep Learning Specialization (Coursera, Andrew Ng)", "TensorFlow Developer Certificate"],
    "nlp": ["NLP Specialization (Coursera, deeplearning.ai)", "Hugging Face NLP Course"],
    "natural language processing": ["NLP Specialization (Coursera, deeplearning.ai)"],
    "computer vision": ["OpenCV University Courses", "Convolutional Neural Networks (Coursera)"],
    "aws": ["AWS Solutions Architect Associate", "AWS Cloud Practitioner"],
    "azure": ["Microsoft Azure Fundamentals (AZ-900)", "Azure Data Scientist Associate (DP-100)"],
    "gcp": ["Google Cloud Professional Data Engineer", "Google Cloud Associate Cloud Engineer"],
    "google cloud": ["Google Cloud Professional Data Engineer"],
    "docker": ["Docker Certified Associate"],
    "kubernetes": ["Certified Kubernetes Administrator (CKA)"],
    "data science": ["IBM Data Science Professional Certificate", "Google Data Analytics Certificate"],
    "power bi": ["Microsoft PL-300: Power BI Data Analyst"],
    "tableau": ["Tableau Desktop Specialist Certification"],
    "tensorflow": ["TensorFlow Developer Certificate (Google)"],
    "pytorch": ["PyTorch Scholarship (Udacity)"],
    "git": ["Git & GitHub for Beginners (freeCodeCamp)"],
    "ci/cd": ["GitHub Actions Certification", "Jenkins Certified Engineer"],
    "mlops": ["MLOps Specialization (Coursera, deeplearning.ai)"],
    "generative ai": ["Google Cloud Generative AI Learning Path"],
    "genai": ["Google Cloud Generative AI Learning Path"],
    "llm": ["LangChain for LLM Application Development (DeepLearning.AI)"],
    "prompt engineering": ["ChatGPT Prompt Engineering for Developers (DeepLearning.AI)"],
    "react": ["Meta React Developer Certificate (Coursera)"],
    "node.js": ["Node.js Application Developer (OpenJS)"],
    "agile": ["Professional Scrum Master I (PSM I)"],
    "scrum": ["Professional Scrum Master I (PSM I)"],
}

# ---------------------------------------------------------------------------
# Project Suggestions
# ---------------------------------------------------------------------------

PROJECT_MAP: dict[str, list[str]] = {
    "python": ["Build a CLI task manager with SQLite", "Create a web scraper with BeautifulSoup & Requests"],
    "sql": ["Design a normalized database for an e-commerce platform", "Write complex analytical queries on Kaggle datasets"],
    "machine learning": ["Customer churn prediction with XGBoost", "House price prediction with feature engineering"],
    "deep learning": ["Image classification with CNN on CIFAR-10", "Sentiment analysis with LSTM/BERT"],
    "nlp": ["Resume parser with spaCy NER", "Text summarisation with Hugging Face Transformers"],
    "natural language processing": ["Build a chatbot with Rasa", "Named Entity Recognition system"],
    "computer vision": ["Object detection with YOLO", "Face recognition attendance system"],
    "aws": ["Deploy a serverless API with Lambda + API Gateway", "Build a data pipeline with S3, Glue, and Athena"],
    "docker": ["Containerise a full-stack web app", "Build a multi-service app with Docker Compose"],
    "power bi": ["Create an interactive sales dashboard", "Build HR analytics report with DAX measures"],
    "tableau": ["Build a COVID-19 analytics dashboard", "Financial performance tracking dashboard"],
    "react": ["Build a real-time chat application", "Create a project management Kanban board"],
    "data science": ["Exploratory Data Analysis on a Kaggle dataset", "End-to-end ML pipeline with model deployment"],
    "generative ai": ["Build a RAG-based Q&A system", "Create an AI-powered content generator"],
    "genai": ["Build a RAG-based Q&A system using LangChain"],
    "llm": ["Fine-tune an LLM on custom data", "Build a multi-agent AI system"],
    "git": ["Contribute to an open-source project on GitHub"],
    "mlops": ["Build an ML model monitoring dashboard", "Implement CI/CD for ML with GitHub Actions + MLflow"],
    "tensorflow": ["Build a neural style transfer app", "Create a real-time object detection system"],
    "pytorch": ["Implement GANs for image generation", "Build a text generation model with GPT-2"],
}

# ---------------------------------------------------------------------------
# Tools / Resources Mapping
# ---------------------------------------------------------------------------

TOOLS_MAP: dict[str, list[str]] = {
    "python": ["Jupyter Notebook", "Google Colab", "PyCharm", "VS Code"],
    "sql": ["DBeaver", "PostgreSQL", "MySQL Workbench", "Mode Analytics"],
    "machine learning": ["Scikit-learn", "Google Colab", "Kaggle Notebooks", "MLflow"],
    "deep learning": ["TensorFlow", "PyTorch", "Google Colab (GPU)", "Weights & Biases"],
    "nlp": ["spaCy", "Hugging Face", "NLTK", "Gensim"],
    "natural language processing": ["spaCy", "Hugging Face Transformers"],
    "aws": ["AWS Free Tier", "AWS CloudFormation", "AWS CLI", "LocalStack"],
    "docker": ["Docker Desktop", "Docker Hub", "Portainer"],
    "kubernetes": ["Minikube", "Kind", "Lens IDE"],
    "power bi": ["Power BI Desktop (free)", "DAX Studio"],
    "tableau": ["Tableau Public (free)", "Tableau Prep"],
    "git": ["GitHub Desktop", "GitKraken", "Git CLI"],
    "data science": ["Pandas", "NumPy", "Plotly", "Streamlit"],
    "generative ai": ["Google AI Studio", "LangChain", "Ollama", "Hugging Face"],
    "genai": ["Google AI Studio", "LangChain", "Ollama"],
    "llm": ["Ollama", "LM Studio", "vLLM", "Hugging Face"],
    "mlops": ["MLflow", "DVC", "Kubeflow", "BentoML"],
    "react": ["Create React App / Vite", "React DevTools", "Storybook"],
    "ci/cd": ["GitHub Actions", "Jenkins", "CircleCI"],
    "computer vision": ["OpenCV", "Roboflow", "Label Studio"],
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def analyze_skill_gap(resume_text: str, jd_text: str) -> dict:
    """
    Compare resume skills against JD skills.
    Returns {matched, missing, matched_categorized, missing_categorized,
             match_percentage, gap_percentage}.
    """
    resume_skills = set(s.lower() for s in extract_skills(resume_text))
    jd_skills_raw = extract_skills_from_jd(jd_text)
    jd_skills = set(s.lower() for s in jd_skills_raw)

    matched = sorted(resume_skills & jd_skills)
    missing = sorted(jd_skills - resume_skills)

    # Canonical names
    skill_map = {s.lower(): s for s in jd_skills_raw}
    matched_canonical = [skill_map.get(s, s.title()) for s in matched]
    missing_canonical = [skill_map.get(s, s.title()) for s in missing]

    match_pct = (len(matched) / len(jd_skills) * 100) if jd_skills else 0
    gap_pct = 100 - match_pct

    return {
        "matched": matched_canonical,
        "missing": missing_canonical,
        "matched_categorized": categorize_skills(matched_canonical),
        "missing_categorized": categorize_skills(missing_canonical),
        "match_percentage": round(match_pct, 1),
        "gap_percentage": round(gap_pct, 1),
        "total_jd_skills": len(jd_skills),
        "total_matched": len(matched),
        "total_missing": len(missing),
    }


def suggest_certifications(missing_skills: list[str]) -> list[dict]:
    """
    Return certification recommendations for missing skills.
    Returns [{skill, certifications: [str]}].
    """
    suggestions = []
    for skill in missing_skills:
        key = skill.lower()
        certs = CERTIFICATION_MAP.get(key, [])
        if certs:
            suggestions.append({"skill": skill, "certifications": certs})
    return suggestions


def suggest_projects(missing_skills: list[str]) -> list[dict]:
    """
    Return project ideas to demonstrate missing skills.
    Returns [{skill, projects: [str]}].
    """
    suggestions = []
    for skill in missing_skills:
        key = skill.lower()
        projects = PROJECT_MAP.get(key, [])
        if projects:
            suggestions.append({"skill": skill, "projects": projects})
    return suggestions


def suggest_tools(missing_skills: list[str]) -> list[dict]:
    """
    Return tools and platforms to learn missing skills.
    Returns [{skill, tools: [str]}].
    """
    suggestions = []
    for skill in missing_skills:
        key = skill.lower()
        tools = TOOLS_MAP.get(key, [])
        if tools:
            suggestions.append({"skill": skill, "tools": tools})
    return suggestions


def get_learning_priority(missing_skills: list[str], jd_text: str) -> list[dict]:
    """
    Rank missing skills by their frequency / importance in the JD.
    Returns [{skill, priority_score, rank}] sorted by priority.
    """
    jd_lower = jd_text.lower()
    scored = []
    for skill in missing_skills:
        # Count occurrences in JD (more mentions = higher priority)
        count = jd_lower.count(skill.lower())
        # Bonus if it appears in first 500 chars (likely a key requirement)
        is_early = 1.5 if skill.lower() in jd_lower[:500] else 1.0
        priority = count * is_early
        scored.append({"skill": skill, "priority_score": round(priority, 2)})

    scored.sort(key=lambda x: x["priority_score"], reverse=True)
    for i, item in enumerate(scored, 1):
        item["rank"] = i

    return scored
