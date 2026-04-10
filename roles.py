ROLES = {
    "Software Engineer": {
        "Programming": [
            "python", "java", "c++"
        ],
        "Core Concepts": [
            "data structures", "algorithms", "system design"
        ],
        "Tools": [
            "git", "docker", "api"
        ]
    },

    "Data Analyst": {
        "Programming": [
            "python", "sql"
        ],
        "Tools": [
            "excel", "tableau", "power bi"
        ],
        "Concepts": [
            "statistics", "data visualization"
        ]
    },

    "ML Engineer": {
        "Programming": [
            "python"
        ],
        "Frameworks": [
            "tensorflow", "pytorch"
        ],
        "Concepts": [
            "machine learning", "deep learning", "nlp"
        ]
    }
}


# 🔥 GLOBAL SKILL LIST (VERY IMPORTANT)
ALL_SKILLS = set()

for role in ROLES.values():
    for category in role.values():
        for skill in category:
            ALL_SKILLS.add(skill)