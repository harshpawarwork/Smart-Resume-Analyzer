import PyPDF2
from pdf2image import convert_from_bytes
import pytesseract

from sentence_transformers import SentenceTransformer, util
from roles import ALL_SKILLS

model = SentenceTransformer('all-MiniLM-L6-v2')

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -------------------------------
# 📄 TEXT EXTRACTION
# -------------------------------
def extract_text(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        if text.strip():
            return text

        file.seek(0)
        images = convert_from_bytes(file.read())

        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img)

        return ocr_text if ocr_text else "NO_TEXT"

    except:
        return "ERROR"


def clean_text(text):
    return text.lower()


# -------------------------------
# 🔥 GUARANTEED SKILL EXTRACTION
# -------------------------------
def extract_skills(text):
    text = text.lower()
    found_skills = set()

    for skill in ALL_SKILLS:
        if skill in text:
            found_skills.add(skill)

    return list(found_skills)


# -------------------------------
# 🤖 SIMILARITY SCORE
# -------------------------------
def calculate_similarity(resume_text, job_desc):
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(job_desc, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2)
    return round(float(score) * 100, 2)


# -------------------------------
# ❗ JD MISSING SKILLS
# -------------------------------
def jd_missing_skills(resume_text, job_desc):
    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_desc)

    missing = []

    for skill in job_skills:
        if skill not in resume_skills:
            missing.append(skill)

    return missing


# -------------------------------
# 🎯 ROLE BASED
# -------------------------------
def role_missing_by_category(resume_text, role_data):
    resume_skills = extract_skills(resume_text)

    missing_by_category = {}

    for category, skills in role_data.items():
        missing = []

        for skill in skills:
            if skill not in resume_skills:
                missing.append(skill)

        missing_by_category[category] = missing

    return missing_by_category


# -------------------------------
# 💡 SUGGESTIONS
# -------------------------------
def generate_suggestions(missing_dict):
    suggestions = []

    for category, skills in missing_dict.items():
        for skill in skills:
            suggestions.append(
                f"Improve your {category} by adding projects in {skill}"
            )

    return suggestions