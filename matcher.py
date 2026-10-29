
import re

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from resume_parser import clean_text


GENERIC_TERMS = {
    "experience", "requirements", "requirement",
    "responsibilities", "responsibility", "ability",
    "knowledge", "skills", "skill", "work", "working",
    "team", "teams", "role", "job", "years", "year",
    "strong", "good", "excellent", "preferred",
    "required", "including", "candidate", "candidates",
    "position", "company", "support", "ability to",
    "responsible", "must", "should", "will", "using",
    "related", "relevant", "plus", "provide",
}


def extract_keywords(job_text, max_keywords=30):
    """Extract job-specific terms without assuming a profession."""

    text = clean_text(job_text)

    if not text:
        return []

    vectorizer = CountVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        token_pattern=r"(?u)\b[a-zA-Z][a-zA-Z+#.-]*\b",
        binary=True,
    )

    try:
        vectorizer.fit([text])
    except ValueError:
        return []

    terms = vectorizer.get_feature_names_out().tolist()

    candidates = [
        term for term in terms
        if term not in GENERIC_TERMS
        and not all(part in GENERIC_TERMS
                    for part in term.split())
        and len(term) > 1
    ]

    # Prefer meaningful phrases, then individual terms.
    candidates.sort(
        key=lambda term: (
            -len(term.split()),
            -len(term),
            term,
        )
    )

    return candidates[:max_keywords]


def find_matching_keywords(resume_text, keywords):
    """Find job terms explicitly mentioned in the resume."""

    resume = clean_text(resume_text)
    found = []
    missing = []

    for keyword in keywords:
        pattern = (
            r"(?<!\w)"
            + re.escape(clean_text(keyword))
            + r"(?!\w)"
        )

        if re.search(pattern, resume):
            found.append(keyword)
        else:
            missing.append(keyword)

    return found, missing


def calculate_similarity(resume_text, job_text):
    """Calculate text similarity using TF-IDF and cosine similarity."""

    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    if not resume_text or not job_text:
        return 0.0

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
    )

    try:
        vectors = vectorizer.fit_transform(
            [resume_text, job_text]
        )
    except ValueError:
        return 0.0

    score = cosine_similarity(
        vectors[0:1], vectors[1:2]
    )[0][0]

    return round(float(score) * 100, 2)


def analyze_resume(resume_text, job_text):
    """Analyze a resume against any profession's job description."""

    keywords = extract_keywords(job_text)

    matching, missing = find_matching_keywords(
        resume_text, keywords
    )

    return {
        "similarity_score": calculate_similarity(
            resume_text, job_text
        ),
        # Retain these keys so the existing app continues to work.
        "resume_skills": [],
        "job_skills": keywords,
        "matching_skills": matching,
        "missing_skills": missing,
    }
