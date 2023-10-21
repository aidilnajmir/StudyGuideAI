from django.shortcuts import render
from .models import StudyMaterial
import openai
import PyPDF2

def home(request):
    return render(request, 'studyguideai/home.html')  # You can create a 'home.html' template

def upload_material(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        extracted_text = extract_text(uploaded_file)
        summarized_text = summarize_text(extracted_text)
        return render(request, 'studyguideai/upload_form.html',{'extract': extracted_text,'summary': summarized_text})

    return render(request, 'studyguideai/upload_form.html')

def extract_text(uploaded_file):
    # Function to extract text from PDF files (You may need to adapt this for other file types)
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def summarize_text(text):
    openai.api_key = 'API_KEY'
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Provide key points of this text in bullet points and generate 10 multiple choice questions and their answers as a study guide: '{text}'",
        max_tokens=1000  # Adjust as needed
    )
    return response.choices[0].text

def save_summary_to_database(title, extracted_text, summarized_text):
    study_material = StudyMaterial(title=title, original_text=extracted_text, summary=summarized_text)
    study_material.save()
