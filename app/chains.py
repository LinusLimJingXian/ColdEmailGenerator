import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.3-70b-versatile")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, links, tone="Professional", resume_text=""):
        tone_instructions = {
            "Professional": "Write in a formal and professional tone.",
            "Friendly": "Write in a warm and friendly tone, as if writing to someone you know.",
            "Confident": "Write in a bold and confident tone that strongly highlights your capabilities.",
            "Concise": "Write in a brief and concise tone. Keep the email short and to the point."
        }

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### MY RESUME:
            {resume_text}

            ### INSTRUCTION:
            You are a job seeker named Linus reaching out to a hiring manager about the job described above.
            Use the resume provided to personalise the email with actual skills, experience, and achievements.
            Your goal is to write a compelling cold email that:
            - Introduces yourself briefly based on your resume
            - Shows genuine interest in the role
            - Highlights how your actual skills and experience from your resume are relevant to their needs
            - Includes the most relevant portfolio links to showcase your work: {link_list}
            - Ends with a clear call to action (e.g. requesting a call or interview)
            
            Tone instruction: {tone_instruction}
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "resume_text": resume_text,
            "link_list": links,
            "tone_instruction": tone_instructions[tone]
        })
        return res.content


if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))