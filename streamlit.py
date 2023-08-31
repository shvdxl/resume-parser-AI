import streamlit as st
import re
import PyPDF2
from pdfminer.high_level import extract_text



def extract_text_from_pdf(pdf_path):
    return extract_text(pdf_path)


def extract_contact_number_from_resume(text):
    contact_number = None

    # Use regex pattern to find a potential contact number
    pattern = r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    match = re.search(pattern, text)
    if match:
        contact_number = match.group()

    return contact_number


def extract_email_from_resume(text):
    email = None

    # Use regex pattern to find a potential email address
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    match = re.search(pattern, text)
    if match:
        email = match.group()

    return email


def extract_skills_from_resume(text, skills_list):
    skills = []

    for skill in skills_list:
        pattern = r"\b{}\b".format(re.escape(skill))
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            skills.append(skill)

    return skills


def extract_education_from_resume(text):
    education = []

    # Use regex pattern to find education information
    pattern = r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
    matches = re.findall(pattern, text)
    for match in matches:
        education.append(match.strip())

    return education


def extract_name(resume_text):
    name_pattern = r"(?i)\b([A-Z][a-z]+)\s+([A-Z][a-z]+)\b"
    match = re.search(name_pattern, resume_text)
    if match:
        first_name = match.group(1)
        last_name = match.group(2)
        full_name = f"{first_name} {last_name}"
        return full_name
    else:
        return None


def read_pdf(file_path):
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        num_pages = len(pdf_reader.pages)

        print(f"Number of pages in the PDF: {num_pages}")

        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            print(f"Page {page_num + 1}:\n{text}\n")




if __name__ == "__main__":
    st.markdown("<h1 style='color: #6683D3;'>resume parser AI 📄</h1>", unsafe_allow_html=True)
    st.write("<hr style='border: none; height: 2px; background-color: white;'>", unsafe_allow_html=True)
    text = 'A resume parser AI project involves developing a system that can automatically extract and analyze information from resumes or CVs (curriculum vitae). This technology is particularly useful for recruitment and HR processes as it can save a significant amount of time and effort by efficiently processing large volumes of resumes.'
    st.markdown(f"<p style='text-align: justify;'>{text}</p>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload your file:")
    with st.form("Upload Form"):
        submit_button = st.form_submit_button("Submit")
        
        
        if submit_button and uploaded_file is not None:
            resume_text = extract_text_from_pdf(uploaded_file)
            name = extract_name(resume_text)
            contact_number = extract_contact_number_from_resume(resume_text)            
            email = extract_email_from_resume(resume_text)
            skills_list = ['Python', 'Data Analysis', 'Machine Learning', 'Communication']
            extracted_skills = extract_skills_from_resume(resume_text, skills_list)
            extracted_education = extract_education_from_resume(resume_text)

            
            if name:
               st.success("Name : " + str(name))
            else:
               st.success("Name not found")


            if contact_number:
                st.success("Contact Number : " + str(contact_number))
            else:
                st.success("Contact Number not found")


            if email:
                st.success("Email : " + str(email))
            else:
                st.success("Email not found")
    
           
            if extracted_skills:
                st.success("Extracted Skills : " + str(extracted_skills))
            else:
                st.success("No skills found")
        
            
            if extracted_education:
                st.success("Extracted Education : " + str(extracted_education))
            else:
                st.success("No education information found")
                
    image_path = "logoCV.png"
    st.image(image_path, use_column_width=True, width=200)
