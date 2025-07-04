import streamlit as st
import matplotlib.pyplot as plt
from utils.parser import extract_text_from_pdf
from utils.nlp_utils import compute_similarity, get_missing_keywords, clean_text

st.set_page_config(page_title="AI Resume Screener", layout="centered")

st.title("🧠 AI Resume Screener")
st.markdown("Upload one or more resumes and a job description to get similarity scores and keyword feedback.")

# Upload one or more resumes
uploaded_resumes = st.file_uploader(
    "📄 Upload Resume(s) (PDF only)", 
    type=["pdf"], 
    accept_multiple_files=True
)

# Job description input
job_description = st.text_area("📝 Paste Job Description Here", height=200)

# Analyze button
if st.button("🔍 Analyze Resumes") and uploaded_resumes and job_description:
    with st.spinner("Analyzing resumes..."):
        results = []

        for file in uploaded_resumes:
            resume_text = extract_text_from_pdf(file)
            score = compute_similarity(resume_text, job_description)
            missing_keywords = get_missing_keywords(resume_text, job_description)

            # Count match stats for chart
            total_keywords = len(set(clean_text(job_description).split()))
            matched_keywords = total_keywords - len(missing_keywords)
            missing_count = len(missing_keywords)

            # Prepare feedback
            if score >= 80:
                feedback = "🎯 Excellent match!"
            elif score >= 60:
                feedback = "👍 Good match. Tailor a bit more."
            else:
                feedback = "⚠️ Low match. Improve resume."

            results.append({
                "Resume": file.name,
                "Score (%)": round(score, 2),
                "Matched Keywords": matched_keywords,
                "Missing Keywords": missing_count,
                "Feedback": feedback,
                "Missing List": ", ".join(missing_keywords)
            })

        # Sort results
        sorted_results = sorted(results, key=lambda x: x["Score (%)"], reverse=True)

        # Show table
        st.subheader("📊 Resume Ranking by Match Score")
        st.dataframe(sorted_results, use_container_width=True)

        # Optional: Show visual chart for top resume
        top = sorted_results[0]
        st.subheader(f"🔍 Keyword Breakdown for Best Match: {top['Resume']}")

        fig, ax = plt.subplots()
        ax.bar(["Matched", "Missing"], [top["Matched Keywords"], top["Missing Keywords"]], color=["green", "red"])
        ax.set_ylabel("Count")
        ax.set_title("Top Resume Keyword Match Overview")
        for bar in ax.patches:
            ax.text(bar.get_x() + 0.1, bar.get_height() + 0.2, int(bar.get_height()))
        st.pyplot(fig)

        # Generate report for top resume
        report_text = f"""AI Resume Screening Report
-------------------------------
Resume: {top['Resume']}
Score: {top['Score (%)']}%
Matched Keywords: {top['Matched Keywords']}
Missing Keywords: {top['Missing Keywords']}

Feedback: {top['Feedback']}

Missing Terms: {top['Missing List']}
"""
        st.download_button(
            label="📄 Download Top Resume Report",
            data=report_text,
            file_name="top_resume_feedback.txt",
            mime="text/plain"
        )
