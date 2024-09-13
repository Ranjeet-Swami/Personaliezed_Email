import streamlit as st
import os
from chains import Chain
from utils import clean_text

def create_streamlit_app(llm, clean_text):
    st.title("Resume Enhancement for ATS")
    
    resume_input = st.text_area("Paste your Resume here:")
    job_description_input = st.text_area("Paste the Job Description here:")
    submit_button = st.button("Submit")

    if submit_button:
        if resume_input and job_description_input:
            try:
                st.write("Processing your input...")

                cleaned_resume = clean_text(resume_input)
                cleaned_job_description = clean_text(job_description_input)

                
                suggestions = llm.suggest_resume_changes(cleaned_resume, cleaned_job_description)
                
                
                print("Suggestions:", suggestions)
                
                if isinstance(suggestions, list):
                    st.subheader("Suggested Bullet Points")
                    st.write("Here are the bullet points you should consider adding or revising in your resume to better match the job description:")
                    for suggestion in suggestions:
                        st.markdown(f"- {suggestion}")
                else:
                    st.error("Unexpected response format. Please try again.")

            except Exception as e:
                st.error(f"An Error Occurred: {e}")
        else:
            st.error("Please paste both your resume and job description.")



if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Resume Enhancer", page_icon="📝")
    create_streamlit_app(chain, clean_text)

