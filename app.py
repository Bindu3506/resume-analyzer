import streamlit as st
import re
from utils import extract_text

st.title("📄 Resume Analyzer & Improver AI")

file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

# -----------------------------
# FREE ANALYZER FUNCTION
# -----------------------------
def analyze(text):
    score = 0
    strengths = []
    weaknesses = []
    suggestions = []
    improved_bullets = []

    text_lower = text.lower()

    # 1. Length check
    if len(text) > 800:
        score += 20
        strengths.append("Good resume length")
    else:
        weaknesses.append("Resume is too short")
        suggestions.append("Add more details about your experience")

    # 2. Keywords check
    keywords = ["python", "java", "sql", "machine learning", "project", "experience"]
    found = [k for k in keywords if k in text_lower]

    score += len(found) * 10

    if len(found) >= 3:
        strengths.append("Good use of technical keywords")
    else:
        weaknesses.append("Not enough technical keywords")
        suggestions.append("Add relevant skills like Python, SQL, Projects")

    # 3. Achievements (numbers)
    numbers = re.findall(r'\d+', text)

    if numbers:
        score += 20
        strengths.append("Includes measurable achievements")
    else:
        weaknesses.append("No measurable achievements")
        suggestions.append("Add numbers (e.g., improved performance by 30%)")

    # 4. Formatting
    if "\n" in text:
        score += 10
        strengths.append("Proper formatting detected")
    else:
        weaknesses.append("Poor formatting")
        suggestions.append("Use bullet points and sections")

    # 5. Sections check
    sections = ["education", "skills", "experience", "projects"]
    found_sections = [s for s in sections if s in text_lower]

    if len(found_sections) >= 3:
        score += 20
        strengths.append("Good section structure")
    else:
        weaknesses.append("Missing important sections")
        suggestions.append("Include Education, Skills, Projects sections")

    # Final score
    score = min(score, 100)

    # Improved bullets (sample)
    improved_bullets = [
        "Developed and deployed projects using modern technologies",
        "Improved system performance by optimizing code efficiency",
        "Collaborated with teams to deliver high-quality solutions",
        "Applied problem-solving skills to real-world challenges"
    ]

    return {
        "score": score,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
        "improved_bullets": improved_bullets
    }

# -----------------------------
# UI
# -----------------------------
if file:
    text = extract_text(file)

    st.subheader("📄 Resume Text")
    st.text_area("", text, height=200)

    if st.button("Analyze"):
        result = analyze(text)

        # Score
        st.subheader("📊 Score")
        st.progress(result["score"])
        st.write(f"{result['score']} / 100")

        # Strengths
        st.subheader("✅ Strengths")
        for s in result["strengths"]:
            st.write("-", s)

        # Weaknesses
        st.subheader("⚠️ Weaknesses")
        for w in result["weaknesses"]:
            st.write("-", w)

        # Suggestions
        st.subheader("💡 Suggestions")
        for s in result["suggestions"]:
            st.write("-", s)

        # Improved bullets
        st.subheader("✍️ Improved Bullet Points")
        for b in result["improved_bullets"]:
            st.write("-", b)