import base64
import io
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("GOOGLE_API_KEY not found in environment variables!")
    st.stop()

def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    # reading only 1st page of pdf for fast testing purpose not for production (pdf_content[0])
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        first_page = images[0]

        # convert into bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {"mime_type": "image/jpeg", "data": base64.b64encode(img_byte_arr).decode()}
        ]
        return pdf_parts
    else:

        raise FileNotFoundError("No file uploaded")


### Streamlit App

st.set_page_config(page_title="ATS Resume Expert")
st.header("Application Tracking System")
input_text = st.text_area("Job Description: ", key="input")
uploaded_files = st.file_uploader("Uploaded you resume(PDF)...", type=["PDF"])

if uploaded_files is not None:
    st.write("PDF uploaded successfully")


submit1 = st.button("Tell Me About the resume")

# submit2 = st.button("How Can I Improve my Skill")

submit3 = st.button("Percentage Match")

# submit4 = st.button("What are the Keywords That are Missing")

input_prompt1 = """
You are an experienced Human resource with Tech experience in the field of any one job role from Data Science, Web development, AI/ML, Fullstack, Devops, Data Analyst.
Your task is to review the resume against the provided job description with its respective domain. 
please share your professional evaluation on whether the candidate profile aligns with the role.
Highlight the strength and weakness of the applicant in relation to specified job requirements. 
"""

input_prompt3 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of any one job role Data Science, Web development, AI/ML, Fullstack, Devops, Data Analyst and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. 
First the output should come as percentage and then keywords missing and last final thoughts.
"""

if submit1:
    if uploaded_files is not None:
        pdf_content = input_pdf_setup(uploaded_files)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)

    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_files is not None:
        pdf_content = input_pdf_setup(uploaded_files)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)

    else:
        st.write("Please upload the resume")
