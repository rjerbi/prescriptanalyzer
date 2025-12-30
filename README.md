# Medical Prescription Analyzer

An AI-powered application to extract and classify medicines from handwritten or printed medical prescriptions using **Google Gemini AI**.

## Screenshots
<div style="text-align: center;">
  <img src="./img/per analyzer & classif.png" alt="Image 1" width="700" style="margin-bottom: 10px;">
  <br>
  <br>
  <img src="./img/per analyzer & classif 2.png" alt="Image 2" width="700" style="margin-bottom: 10px;">
</div>

## Features
- Upload prescription images (handwritten or printed)
- Extract patient info, doctor name, date, medicines, dosage, frequency, duration, and instructions
- Classify medicines into categories and suggest possible illnesses
- Outputs structured JSON data for further processing

## Technologies Used
- Python
- Gradio (for web interface)
- Google Gemini AI (Generative AI model)
- Pandas
- dotenv (for environment variable management)

## Installation
- python -m venv venv
- venv\Scripts\activate
- pip install -r requirements.txt
- python pipeline_ordonnance.py
