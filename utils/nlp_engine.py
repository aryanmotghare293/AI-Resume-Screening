"""
NLP Preprocessing Engine
Provides text cleaning, tokenization, lemmatization, stopword removal,
and TF-IDF keyword extraction using spaCy and NLTK.
"""

import re
import string

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# ---------------------------------------------------------------------------
# Load spaCy model (fall back gracefully)
# ---------------------------------------------------------------------------
try:
    _nlp = spacy.load("en_core_web_sm")
except OSError:
    # Auto-download if missing
    from spacy.cli import download as _spacy_dl
    _spacy_dl("en_core_web_sm")
    _nlp = spacy.load("en_core_web_sm")

_LEMMATIZER = WordNetLemmatizer()

# Additional domain stopwords to filter out
_DOMAIN_STOP = {
    "resume", "experience", "education", "skills", "projects",
    "name", "email", "phone", "address", "objective", "summary",
    "references", "available", "upon", "request", "page",
}


def _load_stopwords() -> set[str]:
    """Load NLTK stopwords if installed; fall back to project stopwords offline."""
    try:
        return set(stopwords.words("english")) | _DOMAIN_STOP
    except LookupError:
        print("[NLP] NLTK stopwords not found; using fallback stopword set.")
        return set(_DOMAIN_STOP)


_STOP_WORDS = _load_stopwords()


# ---------------------------------------------------------------------------
# Core Functions
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    """Remove special characters, extra whitespace, and normalise case."""
    # Remove URLs
    text = re.sub(r"https?://\S+|www\.\S+", " ", text)
    # Remove email addresses
    text = re.sub(r"\S+@\S+\.\S+", " ", text)
    # Remove phone-like number sequences
    text = re.sub(r"[\+\(]?\d[\d\s\-\(\)]{6,}\d", " ", text)
    # Remove non-alphanumeric (keep spaces, hyphens, periods for abbreviations)
    text = re.sub(r"[^a-zA-Z0-9\s\-\.]", " ", text)
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()


def tokenize_text(text: str) -> list[str]:
    """Tokenize text into words using NLTK."""
    try:
        return word_tokenize(text)
    except LookupError:
        return re.findall(r"[a-zA-Z0-9][a-zA-Z0-9\-.]*", text)


def lemmatize_tokens(tokens: list[str]) -> list[str]:
    """Lemmatize tokens with NLTK WordNet lemmatizer and spaCy fallback."""
    try:
        return [_LEMMATIZER.lemmatize(token) for token in tokens]
    except LookupError:
        return tokens


def lemmatize_text_spacy(text: str) -> list[str]:
    """Lemmatize full text with spaCy (better for contextual lemmatization)."""
    doc = _nlp(text)
    return [token.lemma_ for token in doc if not token.is_punct and not token.is_space]


def remove_stopwords(tokens: list[str]) -> list[str]:
    """Remove stopwords and very short tokens."""
    return [
        t for t in tokens
        if t not in _STOP_WORDS
        and len(t) > 1
        and t not in string.punctuation
    ]


def extract_keywords(text: str, top_n: int = 30) -> list[str]:
    """Extract top keywords using TF-IDF on pseudo-documents (sentences)."""
    sentences = re.split(r"[.\n]", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]

    if not sentences:
        return []

    try:
        vectorizer = TfidfVectorizer(
            max_features=200,
            stop_words="english",
            ngram_range=(1, 2),
            min_df=1,
        )
        tfidf_matrix = vectorizer.fit_transform(sentences)
        feature_names = vectorizer.get_feature_names_out()

        # Aggregate scores across sentences
        scores = tfidf_matrix.sum(axis=0).A1
        ranked = sorted(zip(feature_names, scores), key=lambda x: x[1], reverse=True)
        return [word for word, _ in ranked[:top_n]]
    except ValueError:
        return []


def preprocess_pipeline(text: str) -> dict:
    """
    Full preprocessing pipeline.
    Returns dict with: cleaned_text, tokens, keywords
    """
    cleaned = clean_text(text)
    tokens = tokenize_text(cleaned)
    tokens = lemmatize_tokens(tokens)
    tokens = remove_stopwords(tokens)
    keywords = extract_keywords(cleaned)

    return {
        "cleaned_text": cleaned,
        "tokens": tokens,
        "keywords": keywords,
    }
