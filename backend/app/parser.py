import pdfplumber
import re

SKILLS_DB = [
    "python", "java", "sql", "react",
    "machine learning", "fastapi",
    "django", "html", "css"
]


def extract_text(path: str) -> str:
    text = ""

    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + " "
    except Exception:
        return ""

    return text.lower()


def extract_skills(text: str) -> list:
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill.title())

    return found_skills


def extract_experience(text: str) -> int:
    matches = re.findall(r'(\d+)\+?\s*(?:years|year|yrs|yr)', text)

    if matches:
        return max(int(match) for match in matches)

    return 0


def extract_education(text: str) -> int:
    education_keywords = [
        "b.tech", "btech", "bachelor",
        "mca", "m.tech", "msc", "bsc"
    ]

    for keyword in education_keywords:
        if keyword in text:
            return 1

    return 0


def parse_resume(path: str) -> dict:
    text = extract_text(path)

    return {
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text)
    }