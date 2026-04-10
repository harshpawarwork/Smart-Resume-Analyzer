import PyPDF2
from pdf2image import convert_from_bytes
import pytesseract
import spacy
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load("en_core_web_sm")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


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


def extract_keywords(text):
    doc = nlp(text)
    keywords = []

    for token in doc:
        if (
            not token.is_stop and
            token.is_alpha and
            token.pos_ in ["NOUN", "PROPN"]
        ):
            keywords.append(token.lemma_)

    return list(set(keywords))


def calculate_similarity(resume_text, job_desc):
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(job_desc, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2)
    return round(float(score) * 100, 2)


def is_matched(skill, resume_skills):
    for r in resume_skills:
        sim = util.cos_sim(
            model.encode(skill, convert_to_tensor=True),
            model.encode(r, convert_to_tensor=True)
        )
        if float(sim) > 0.6:
            return True
    return False


# JD-based missing skills
def jd_missing_skills(resume_text, job_desc):
    resume_skills = extract_keywords(resume_text)
    job_skills = extract_keywords(job_desc)

    missing = []
    for skill in job_skills:
        if not is_matched(skill, resume_skills):
            missing.append(skill)

    return missing


# 🔥 CATEGORY-BASED ROLE ANALYSIS
def role_missing_by_category(resume_text, role_data):
    resume_skills = extract_keywords(resume_text)

    missing_by_category = {}

    for category, skills in role_data.items():
        missing = []

        for skill in skills:
            if not is_matched(skill, resume_skills):
                missing.append(skill)

        missing_by_category[category] = missing

    return missing_by_category


def generate_suggestions(missing_dict):
    suggestions = []

    for category, skills in missing_dict.items():
        for skill in skills:
            suggestions.append(
                f"Improve your {category} by learning or adding projects in {skill}"
            )

    return suggestions