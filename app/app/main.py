import sys
import os

# ✅ IMPORTANT: Fix Python path so imports work with your current folder structure
CURRENT_DIR = os.path.dirname(__file__)              # app/app/
PARENT_DIR = os.path.dirname(CURRENT_DIR)            # app/
sys.path.append(CURRENT_DIR)                         # allows: import utils, chains, portfolio
sys.path.append(PARENT_DIR)                          # fallback for package resolution

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from utils import clean_text
from portfolio import Portfolio
from chains import Chain


def create_streamlit_app(llm, portfolio):

    st.title("📧 Cold Email Generator")

    url_input = st.text_input(
        "Enter Job URL:",
        "https://jobs.nike.com/job/R-33460"
    )

    if st.button("Submit"):
        try:
            st.write("🔄 Loading webpage...")
            loader = WebBaseLoader([url_input])
            doc = loader.load().pop()

            st.write("🧹 Cleaning text...")
            cleaned = clean_text(doc.page_content)

            st.write("🧠 Extracting job details...")
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(cleaned)

            for job in jobs:
                st.subheader(f"Job Role: {job.get('role', 'Unknown')}")

                skills = job.get("skills", [])
                links = portfolio.query_links(skills)

                st.write("✉️ Generating Cold Email...")
                email = llm.write_mail(job, links)

                st.subheader("Generated Email:")
                st.write(email)

        except Exception as e:
            st.error(f"❌ ERROR: {str(e)}")
            raise  # shows full traceback in terminal for debugging


if __name__ == "__main__":
    llm = Chain()
    portfolio = Portfolio()
    create_streamlit_app(llm, portfolio)

