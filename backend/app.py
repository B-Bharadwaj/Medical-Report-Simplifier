from flask import Flask, request, jsonify
import pdfplumber
import google.generativeai as genai
import os

app = Flask(__name__)

# configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use one of your available models
model = genai.GenerativeModel("models/gemini-2.5-pro")

@app.route("/simplify", methods=["POST"])
def simplify():
    file = request.files["file"]
    text = extract_pdf_text(file)

    prompt = f"""
    Simplify the following medical report into clear, patient-friendly language.
    Explain all medical terms in easy words.

    Report:
    {text}
    """

    response = model.generate_content(prompt)
    simplified = response.text

    return jsonify({"simplified": simplified})

def extract_pdf_text(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"
    return text

if __name__ == "__main__":
    app.run(debug=True)
