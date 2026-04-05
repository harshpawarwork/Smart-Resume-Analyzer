from flask import Flask, render_template, request
from analyzer import extract_text, clean_text, calculate_similarity, missing_skills

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["resume"]
        job_desc = request.form["job_desc"]

        resume_text = extract_text(file)

        if resume_text == "ERROR":
            return "Invalid PDF."

        if resume_text == "NO_TEXT":
            return "No readable text."

        resume_clean = clean_text(resume_text)
        job_clean = clean_text(job_desc)

        score = calculate_similarity(resume_clean, job_clean)
        gaps = missing_skills(resume_clean, job_clean)

        return render_template("index.html", score=score, gaps=gaps)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)