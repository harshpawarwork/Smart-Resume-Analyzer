import PyPDF2
from pdf2image import convert_from_bytes
import pytesseract

from sentence_transformers import SentenceTransformer, util
import spacy

# Load models
model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load("en_core_web_sm")

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


# -------------------------------
# 📄 EXTRACT TEXT
# -------------------------------
def extract_text(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""

        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text()

        if text.strip() != "":
            return text

        file.seek(0)
        images = convert_from_bytes(file.read())

        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img)

        return ocr_text if ocr_text else "NO_TEXT"

    except:
        return "ERROR"


# -------------------------------
# 🧠 CLEAN TEXT
# -------------------------------
def clean_text(text):
    return text.lower()


# -------------------------------
# 🤖 SEMANTIC SIMILARITY
# -------------------------------
def calculate_similarity(resume_text, job_desc):
    emb1 = model.encode(resume_text, convert_to_tensor=True)
    emb2 = model.encode(job_desc, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2)

    return round(float(score) * 100, 2)


# -------------------------------
# 🔍 SMART KEYWORD EXTRACTION
# -------------------------------
def extract_keywords(text):
    doc = nlp(text.lower())

    keywords = []

    for token in doc:
        # keep only meaningful words
        if (
            token.is_stop == False and
            token.is_alpha and
            token.pos_ in ["NOUN", "PROPN"]
        ):
            keywords.append(token.lemma_)

    return list(set(keywords))


# -------------------------------
# ❗ MISSING SKILLS
# -------------------------------
def missing_skills(resume_text, job_desc):
    resume_words = set(extract_keywords(resume_text))
    job_words = set(extract_keywords(job_desc))

    return list(job_words - resume_words)