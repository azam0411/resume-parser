import pdfplumber
from docx import Document
import os


def extract_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        return "\n".join([page.extract_text() or "" for page in pdf.pages])


def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])


def parse_resume(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.pdf':
        text = extract_text_from_pdf(file_path)
    elif ext == '.docx':
        text = extract_text_from_docx(file_path)
    else:
        return {'error': 'Unsupported format'}

    # Basic dummy parsing (mock logic)
    return {
        "hero": {"name": extract_name(text), "title": "Aspiring Developer"},
        "about": {"bio": extract_about(text)},
        "skills": extract_skills(text),
        "experience": extract_experience(text),
        "education": extract_education(text),
        "contact": {"email": extract_email(text)}
    }


def extract_name(text):
    lines = text.split('\n')
    return lines[0].strip() if lines else "John Doe"


def extract_about(text):
    return "An enthusiastic software developer looking for challenging opportunities."


def extract_skills(text):
    return ["Python", "Flask", "JavaScript", "MongoDB"]


def extract_experience(text):
    return [{"company": "XYZ Corp", "role": "Intern", "duration": "6 months"}]


def extract_education(text):
    return [{"degree": "B.Tech in AIML", "year": "2024", "institution": "ADGIPS"}]


def extract_email(text):
    import re
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "example@example.com"
