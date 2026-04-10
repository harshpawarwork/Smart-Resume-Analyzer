from flask import Flask, render_template, request
from analyzer import (
    extract_text, clean_text,
    calculate_similarity,
    jd_missing_skills,
    role_missing_by_category,
    generate_suggestions
)
from roles import ROLES

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            file = request.files["resume"]
            job_desc = request.form["job_desc"]
            role = request.form["role"]

            # 🔥 Check file
            if not file:
                return "No file uploaded"

            resume_text = extract_text(file)

            if resume_text in ["ERROR", "NO_TEXT"]:
                return "Error reading resume"

            resume_clean = clean_text(resume_text)
            job_clean = clean_text(job_desc)

            score = calculate_similarity(resume_clean, job_clean)

            jd_missing = jd_missing_skills(resume_clean, job_clean)

            role_missing = role_missing_by_category(
                resume_clean,
                ROLES[role]
            )

            suggestions = generate_suggestions(role_missing)

            # 🔥 IMPORTANT: send everything
            return render_template(
                "index.html",
                score=score,
                jd_missing=jd_missing,
                role_missing=role_missing,
                suggestions=suggestions
            )

        except Exception as e:
            return f"Error: {str(e)}"

    return render_template("index.html", score=None)


if __name__ == "__main__":
    app.run(debug=True)