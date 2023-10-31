from django.shortcuts import render
from .models import StudyMaterial
import openai
import PyPDF2
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.pagesizes import letter
from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph

summarized_text = ""

def home(request):
    return render(request, 'studyguideai/home.html')  

def upload_material(request):
    global summarized_text
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        extracted_text = extract_text(uploaded_file)
        summarized_text = summarize_text(extracted_text)
        return render(request, 'studyguideai/upload_form.html', {'summary': summarized_text})

    return render(request, 'studyguideai/upload_form.html')

def extract_text(uploaded_file):
    # Function to extract text from PDF files (You may need to adapt this for other file types)
    pdf_reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

def summarize_text(text):
    #apikey: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
    openai.api_key = ''
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Provide key points of this text in bullet points and 10 multiple choice questions with answers (add <br /> as string after each keypoint,question,answer choice, and answer. add <br /> as string before each question add <br /> as string before the first keypoint. add <br /> <br /> as string after the last keypoint <): '{text}'",
        max_tokens=1000  
    )
    return response.choices[0].text

def string_to_pdf(pdf_content):
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []


    # Define a paragraph style for the content
    styles = getSampleStyleSheet()
    content_style = ParagraphStyle(
        name='ContentStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
    )

    # Create a Paragraph with the provided text and style
    content = Paragraph(pdf_content, content_style)
    elements.append(content)

    # Build the PDF document
    doc.build(elements)

    return response
    # Serve the PDF as an attachment with the appropriate headers
   

def download_pdf(request):
    global summarized_text
    response = string_to_pdf(summarized_text)
    return response


def string_to_pdf2(pdf_content):
   
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="output.pdf"'
    response['X-Frame-Options'] = 'ALLOWALL'

    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []


    # Define a paragraph style for the content
    styles = getSampleStyleSheet()
    content_style = ParagraphStyle(
        name='ContentStyle',
        parent=styles['Normal'],
        fontSize=12,
        leading=14,
    )

    # Create a Paragraph with the provided text and style
    content = Paragraph(pdf_content, content_style)
    elements.append(content)

    # Build the PDF document
    doc.build(elements)

    return response
    # Serve the PDF as an attachment with the appropriate headers
   

def download_pdf2(request):
    global summarized_text
    response = string_to_pdf2(summarized_text)
    return response


