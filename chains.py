import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
        temperature=0,
        model_kwargs={"Groq_api_key": os.getenv("Groq_api_key")},
        model_name="llama-3.1-70b-versatile"
        )


    def extract_bullet_points(self, job_description_text):
        prompt_bullet_points = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description_text}

            ### INSTRUCTION:
            Extract specific bullet points from the job description that are essential for matching the job requirements. 
            Provide these bullet points as a list. The output should be in a format that can be directly added to a resume to increase ATS score.
            ### OUTPUT FORMAT (NO PREAMBLE):
            """
        )
        chain_bullet_points = prompt_bullet_points | self.llm
        res = chain_bullet_points.invoke(input={"job_description_text": job_description_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
            print(res)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse bullet points.")
        return res if isinstance(res, list) else [res]

    def suggest_resume_changes(self, resume_text, job_description_text):
        prompt_suggestions = PromptTemplate.from_template(
            """
            ### RESUME:
            {resume_text}

            ### JOB DESCRIPTION:
            {job_description_text}

            ### INSTRUCTION:
            Analyze the resume text and compare it to the job description. 
            Suggest specific bullet points that should be added or revised in the resume to better match the job description.
            Provide these suggestions in a list format with clear instructions on what needs to be added or changed.
            ### OUTPUT FORMAT (NO PREAMBLE):
            """
        )
        chain_suggestions = prompt_suggestions | self.llm
        res = chain_suggestions.invoke(input={"resume_text": resume_text, "job_description_text": job_description_text})

        
        print("Raw LLM Response:", res.content)
        
        try:
            
            if isinstance(res.content, str):
                
                parsed_res = res.content.strip().split("\n")
                
                return [point.strip() for point in parsed_res if point.strip()]
            else:
                
                return [str(res.content)]
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse resume suggestions.")



if __name__ == "__main__":
    print(os.getenv("Groq_api_key"))

