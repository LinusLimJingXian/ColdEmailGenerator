import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import pdfplumber
import streamlit.components.v1 as components
import shutil
import os

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def extract_resume_text(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")

    # Initialise email history in session
    if "email_history" not in st.session_state:
        st.session_state.email_history = []

    # --- SIDEBAR ---
    with st.sidebar:
        st.subheader("📋 Email History")
        if not st.session_state.email_history:
            st.caption("No emails generated yet. Your last 5 emails will appear here.")
        else:
            for i, item in enumerate(reversed(st.session_state.email_history)):
                with st.expander(f"{i+1}. {item['role']} — {item['tone']}"):
                    st.code(item['email'], language='markdown')

        st.divider()

        st.subheader("⚙️ Settings")
        if st.button("🗑️ Clear Portfolio Cache"):
            if os.path.exists("vectorstore"):
                shutil.rmtree("vectorstore")
                st.success("✅ Portfolio cache cleared! It will rebuild on next email generation.")
            else:
                st.info("No cache found — nothing to clear.")

    # --- MAIN INPUTS ---
    uploaded_resume = st.file_uploader("Upload your resume (PDF):", type="pdf")
    resume_text = ""
    if uploaded_resume:
        resume_text = extract_resume_text(uploaded_resume)
        st.success("✅ Resume uploaded successfully!")

    url_input = st.text_input("Enter a URL:", placeholder="e.g. https://careers.google.com/jobs")
    st.caption("⚠️ Please use a direct company careers page URL (e.g. careers.google.com). Job boards like LinkedIn or Ashby may not work.")

    tone = st.selectbox("Select Email Tone:", ["Professional", "Friendly", "Confident", "Concise"])

    submit_button = st.button("Generate Email")

    if submit_button:
        # Validate resume
        if not uploaded_resume:
            st.warning("⚠️ Please upload your resume before submitting.")
            return
        if len(resume_text.strip()) < 100:
            st.warning("⚠️ We could not extract enough information from your uploaded file. Please make sure you are uploading a valid resume in PDF format.")
            return
        # Validate URL
        if not url_input.strip():
            st.warning("⚠️ Please enter a URL before submitting.")
            return
        if not url_input.startswith("http"):
            st.warning("⚠️ Please enter a valid URL starting with http:// or https://")
            return

        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)

            if not jobs:
                st.warning("⚠️ AI could not detect any job listings. Please use a direct company careers page URL instead of a job board.")
                return

            for job in jobs:
                skills = job.get('skills', [])
                role = job.get('role', 'this role')

                if not skills:
                    st.warning("⚠️ AI could not detect any skills from this page. Please use a direct company careers page URL instead of a job board.")
                    continue

                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links, tone, resume_text)

                st.subheader(f"Generated Email — {role}")

                # Display copyable email
                st.code(email, language='markdown')
                st.caption("👆 Click the copy icon in the top right of the box to copy your email")

                # Auto save to history with cap of 5
                if len(st.session_state.email_history) >= 5:
                    st.session_state.email_history.pop(0)
                st.session_state.email_history.append({
                    "role": role,
                    "tone": tone,
                    "email": email
                })

        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)