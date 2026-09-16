import streamlit as st
import fitz
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write("Analyze your resume and compare it with a job description.")

st.divider()

# Resume upload
resume = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx"]
)

# Job description
job_description = st.text_area(
    "Paste the Job Description",
    height=250,
    placeholder="Paste the job description here..."
)

if st.button("🔍 Analyze Resume"):
    if resume.name.lower().endswith(".pdf"):
            pdf = fitz.open(stream=resume.read(), filetype="pdf")
            resume_text = ""

            for page in pdf:
                resume_text += page.get_text()

            st.subheader("Extracted Resume Text")
            st.text_area("Resume content", resume_text, height=300)

    if resume is None:
        st.warning("Please upload your resume.")

    elif not job_description.strip():
        st.warning("Please paste the job description.")

    else:
        st.success("Resume and job description received!")

        st.subheader("Resume Details")
        st.write("File:", resume.name)

        st.subheader("Job Description")
        st.write(job_description)

        prompt = f"""
Analyze this resume against the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Give:
1. ATS match score out of 100
2. Matching skills
3. Missing skills
4. Resume improvement suggestions
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        st.subheader("🤖 AI Resume Analysis")
        st.write(response.text)