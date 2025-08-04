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
    import re
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    # Try to find a line with two words (likely a name) at the top
    for line in lines[:5]:
        if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+$', line):
            return line
    # Fallback: first non-empty line
    return lines[0] if lines else "John Doe"


def extract_about(text):
    import re
    # Look for 'Summary' or 'About' section
    match = re.search(r'(Summary|About)[\s\n:]+(.+?)(\n\w+:|\n\n|$)', text, re.IGNORECASE | re.DOTALL)
    if match:
        about = match.group(2).strip()
        # Remove trailing section header if present
        about = re.split(r'\n\w+:', about)[0].strip()
        return about
    # Fallback: first 3 lines after name
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    return ' '.join(lines[1:4]) if len(lines) > 3 else "About not found."


def extract_skills(text):
    import re
    # Look for 'Skills' section
    match = re.search(r'Skills[\s\n:]+(.+?)(\n\w+:|\n\n|$)', text, re.IGNORECASE | re.DOTALL)
    if match:
        skills_block = match.group(1)
        # Split by comma or newline
        skills = re.split(r',|\n', skills_block)
        return [s.strip() for s in skills if s.strip()]
    # Fallback: look for lines with many commas
    for line in text.split('\n'):
        if line.count(',') >= 2:
            return [s.strip() for s in line.split(',') if s.strip()]
    return []


def extract_experience(text):
    import re
    # Look for 'Experience' section
    match = re.search(r'Experience[\s\n:]+(.+?)(\n\w+:|\n\n|$)', text, re.IGNORECASE | re.DOTALL)
    experiences = []
    if match:
        exp_block = match.group(1)
        # Try to extract lines like 'Company - Role (Duration)'
        for line in exp_block.split('\n'):
            m = re.match(r'(.+?)\s+-\s+(.+?)\s+\((.+?)\)', line.strip())
            if m:
                experiences.append({
                    "company": m.group(1).strip(),
                    "role": m.group(2).strip(),
                    "duration": m.group(3).strip()
                })
        # Fallback: lines with at least 2 words
        if not experiences:
            for line in exp_block.split('\n'):
                parts = [p.strip() for p in re.split(r'-|\(|\)', line) if p.strip()]
                if len(parts) >= 2:
                    experiences.append({
                        "company": parts[0],
                        "role": parts[1],
                        "duration": parts[2] if len(parts) > 2 else ""
                    })
    return experiences if experiences else []


def extract_education(text):
    import re
    # Look for 'Education' section
    match = re.search(r'Education[\s\n:]+(.+?)(\n\w+:|\n\n|$)', text, re.IGNORECASE | re.DOTALL)
    educations = []
    if match:
        edu_block = match.group(1)
        # Try to extract lines like 'Degree, Year, Institution'
        for line in edu_block.split('\n'):
            parts = [p.strip() for p in line.split(',') if p.strip()]
            if len(parts) >= 3:
                educations.append({
                    "degree": parts[0],
                    "year": parts[1],
                    "institution": parts[2]
                })
    return educations if educations else []


def extract_email(text):
    import re
    match = re.search(r'[\w\.-]+@[\w\.-]+', text)
    return match.group(0) if match else "example@example.com"
