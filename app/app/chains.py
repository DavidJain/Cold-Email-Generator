import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException


load_dotenv("app/app/resource/.env")



class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            
            model="llama-3.3-70b-versatile" 
        )

      


    def extract_jobs(self, cleaned_text):
        prompt = PromptTemplate.from_template("""
        ### SCRAPED TEXT FROM WEBSITE:
        {page_data}

        ### INSTRUCTION:
        Extract job details and return ONLY valid JSON with:
        - role
        - experience
        - skills
        - description

        NO PREAMBLE, ONLY VALID JSON.
        """)

        chain = prompt | self.llm
        res = chain.invoke({"page_data": cleaned_text})

        try:
            parser = JsonOutputParser()
            data = parser.parse(res.content)
        except:
            raise OutputParserException("❌ Could not parse job JSON.")

        return data if isinstance(data, list) else [data]

    def write_mail(self, job, links):
        prompt = PromptTemplate.from_template("""
        ### JOB INFO:
        {job_description}

        ### TASK:
        You are Mohan, BDE at AtliQ (AI & Software Consulting).
        Write a cold email to this client showing:
        - how AtliQ can fulfill their needs
        - reference portfolio links: {link_list}

        NO PREAMBLE. DIRECT EMAIL ONLY.
        """)

        chain = prompt | self.llm
        res = chain.invoke({
            "job_description": str(job),
            "link_list": links
        })
        return res.content
