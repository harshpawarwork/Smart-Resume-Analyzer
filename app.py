from flask import Flask, render_template, request
from analyzer import (
    extract_text,
    clean_text,
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
            # 🔥 Get inputs
            file = request.files.get("resume")
            job_desc = request.form.get("job_desc")
            role = request.form.get("role")

            # ❌ Validate
            if not file or file.filename == "":
                return render_template("index.html", score=None, error="No file uploaded")

            if not job_desc:
                return render_template("index.html", score=None, error="Job description required")

            # 📄 Extract text
            resume_text = extract_text(file)

            if resume_text in ["ERROR", "NO_TEXT"]:
                return render_template("index.html", score=None, error="Resume could not be read")

            # 🧹 Clean
            resume_clean = clean_text(resume_text)
            job_clean = clean_text(job_desc)

            # 📊 Score
            score = calculate_similarity(resume_clean, job_clean)

            # ❗ Missing skills (JD)
            jd_missing = jd_missing_skills(resume_clean, job_clean)

            # 🎯 Role-based analysis
            role_data = ROLES.get(role, {})
            role_missing = role_missing_by_category(resume_clean, role_data)

            # 💡 Suggestions
            suggestions = generate_suggestions(role_missing)

            # 🔥 SEND EVERYTHING TO UI
            return render_template(
                "index.html",
                score=score,
                jd_missing=jd_missing,
                role_missing=role_missing,
                suggestions=suggestions
            )

        except Exception as e:
            # 🔥 Show error clearly
            return render_template(
                "index.html",
                score=None,
                error=f"Error: {str(e)}"
            )

    # GET request
    return render_template("index.html", score=None)


if __name__ == "__main__":
    app.run(debug=True)