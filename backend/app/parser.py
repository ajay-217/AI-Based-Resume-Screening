import pdfplumber

SKILLS_DB = [
    "python","java","sql","react",
    "machine learning","fastapi","django","html","css"
]

def extract_text(path):
    text=""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

def extract_skills(text):
    return [skill for skill in SKILLS_DB if skill in text]

def extract_experience(text):
    return text.count("year")

def extract_education(text):
    return 1 if ("b.tech" in text or "bachelor" in text or "mca" in text) else 0

def parse_resume(path):
    text = extract_text(path)

    return {
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text)
    }