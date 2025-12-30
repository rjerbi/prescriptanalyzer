import os
import json
import gradio as gr
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv
from io import BytesIO

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Please set your GOOGLE_API_KEY in a .env file")

# Configure the Gemini model
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-flash")

# Load medicine classification dataset
med_df = pd.read_excel("dataset.xlsx") 
med_lookup = {
    str(name).strip().lower(): {
        "category": category,
        "possible_illness": illness
    }
    for name, category, illness in zip(
        med_df["medicine_name"], med_df["category"], med_df["possible_illness"]
    )
}

# Convert PIL image to bytes
def image_to_bytes(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return buffered.getvalue()

# Main prescription analysis function
def analyze_prescription(image):
    if image is None:
        return "Please upload an image.", ""

    image_bytes = image_to_bytes(image)

    system_prompt = (
        "You are a medical expert specialized in understanding prescriptions. "
        "Given this image of a handwritten or printed prescription, extract "
        "patient name, doctor name, date, medicines (name, dosage, frequency, duration), and instructions."
    )
    user_prompt = "Provide the extracted prescription info as a JSON."

    input_prompt = [
        system_prompt,
        {
            "mime_type": "image/png",
            "data": image_bytes
        },
        user_prompt,
    ]

    # Get response from Gemini model
    response = model.generate_content(input_prompt)

    # Clean up Gemini response (remove markdown-style formatting)
    raw_text = response.text.strip()
    if raw_text.startswith("```json"):
        raw_text = raw_text.replace("```json", "").strip()
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3].strip()

    # Parse the cleaned text into JSON
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        return "Failed to parse response as JSON.", response.text

    # Enrich each medicine with category and possible illness
    for med in data.get("medicines", []):
        name = med.get("name", "").strip().lower()
        info = med_lookup.get(name)
        if info:
            med["category"] = info["category"]
            med["possible_illness"] = info["possible_illness"]
        else:
            med["category"] = "Unknown"
            med["possible_illness"] = "Unknown"

    # Return the enriched JSON
    enriched_json = json.dumps(data, ensure_ascii=False, indent=2)
    return "Prescription JSON Data with Classification:", enriched_json

# Gradio user interface
interface = gr.Interface(
    fn=analyze_prescription,
    inputs=gr.Image(type="pil", label="Upload Prescription Image"),
    outputs=[
        gr.Textbox(label="Result"),
        gr.Textbox(label="Output (JSON)")
    ],
    title="Medical Prescription Analyzer",
    description="Upload a handwritten or printed prescription image to extract and classify medicines."
)

# Launch the app
if __name__ == "__main__":
    interface.launch()
