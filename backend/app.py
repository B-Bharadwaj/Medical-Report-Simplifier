from flask import Flask, request, jsonify
import pdfplumber
import google.generativeai as genai
import os
import traceback

app = Flask(__name__)

# Load API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Use a valid model
model = genai.GenerativeModel("models/gemini-2.5-flash")

# ------------------- PDF Extraction -------------------
def extract_text_from_pdf(path):
    try:
        with pdfplumber.open(path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text
    except:
        return ""

# ------------------- ROUTE: Simplify -------------------
@app.route("/simplify", methods=["POST"])
def simplify():
    try:
        # 1. File check
        if "file" not in request.files:
            return jsonify({"error": "No PDF uploaded"}), 400

        uploaded_file = request.files["file"]
        pdf_path = "uploaded.pdf"
        uploaded_file.save(pdf_path)

        # 2. Extract PDF text
        extracted_text = extract_text_from_pdf(pdf_path)
        if not extracted_text.strip():
            return jsonify({"error": "Could not extract text from PDF"}), 400

        # 3. Prompt using 'level'
        level = request.form.get("level", "patient")
        conciseness = request.form.get("conciseness", "Medium")
        output_format = request.form.get("format", "Full Explanation")

        # Define instruction based on simplification level
        if level == "patient":
            base_instruction = "Explain this in simple, compassionate, patient-friendly language."
        elif level == "student":
            base_instruction = "Summarize this like a medical lecturer explaining key findings to a medical student."
        else:
            base_instruction = "Summarize this as tight, structured clinical bullet points for a clinician."

        # Prompt template
        prompt = f"""
You are an expert medical explanation assistant. Simplify the following medical report EXACTLY according to the user's preferences.

=== USER SETTINGS ===
Simplification Level: {level}
Conciseness: {conciseness}
Format: {output_format}

=== HARD RULES (MUST FOLLOW) ===
1. If Conciseness = "Detailed":
   - Your output MUST be at least 8–12 paragraphs.
   - Include: what the diagnosis means, how it happens, symptoms, test interpretations, staging meaning, treatment plan, why that treatment is chosen, risks, prognosis, and emotional reassurance.
   - Use headers and subheaders.
   - NO summarizing. FULL explanation.

2. If Format = "Full Explanation":
   - Include: 
        • “Summary of Findings”
        • “What This Diagnosis Means”
        • “How Doctors Interpret the Tests”
        • “Does it Mean Cancer Spread?”
        • “Treatment Options & Why They Are Chosen”
        • “Prognosis”
        • “Supportive Guidance”
   - Write in a warm, empathetic tone.
   - Expand each section into multiple sentences and paragraphs.

3. If Format = "Summary Only":
   - MAXIMUM 5 sentences.

4. If Format = "Summary + Key Findings":
   - 1 short paragraph + 6–10 bullet points.

5. Do NOT add new medical information not found in the report.
6. Be strictly medically accurate.
7. Do NOT compress the explanation if conciseness = Detailed.

=== MEDICAL REPORT TO EXPLAIN ===
{extracted_text}

Now produce the explanation.
"""


        # 4. Call Gemini
        response = model.generate_content(prompt)
        simplified = response.text

        return jsonify({"simplified_text": simplified})

    except Exception as e:
        return jsonify({
            "error": str(e),
            "trace": traceback.format_exc()
        }), 500

@app.route("/chat_followup", methods=["POST"])
def chat_followup():
    try:
        user_question = request.form.get("question")
        simplified_report = request.form.get("simplified_report")
        chat_history = request.form.get("chat_history", "")

        if not user_question:
            return jsonify({"error": "No question provided"}), 400

        # Full context for the LLM
        prompt = f"""
You are a medical assistant chatbot helping a patient understand THEIR OWN medical report.

Below is the simplified report of THEIR condition:
------------------------------------
{simplified_report}
------------------------------------

Conversation so far:
{chat_history}

User's new question:
{user_question}

Rules:
- Answer ONLY using information from their report.
- If user asks something not in the report, say:
  "Your report does not contain this information. Please consult your doctor."
- Be supportive and patient-friendly.
- Do NOT give medical advice, diagnoses, or treatment decisions.
- Focus on explanations, meaning, clarity, and reassurance.
- Keep answers short, clear, and easy to understand.

Now respond to the user's question.
"""

        response = model.generate_content(prompt)
        answer = response.text

        return jsonify({"answer": answer})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------- RUN SERVER -------------------
if __name__ == "__main__":
    print("🚀 Backend running at: http://127.0.0.1:5000")
    app.run(debug=True)
