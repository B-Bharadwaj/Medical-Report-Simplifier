# 🧠Medical Report Simplifier

**AI-powered tool to convert complex medical reports into simple, patient-friendly language**

This application helps users understand medical reports by transforming complex PDF content into simple, easy-to-read explanations using an AI-powered simplification engine.

---

## 🚀 Features
```bash
-PDF Upload Support (via Streamlit)
-Automatic Text Extraction using pdfplumber
-Medical Report Simplification powered by Gemini 2.5 Flash
-Explains complex medical terms in clear language
-Produces structured, easy-to-read output
-Fast, reliable, and demo-ready
-Lightweight Flask backend + Streamlit frontend   

```

## ⚙️ Tech Stack

| Component   | Technology                      |
| ----------- | ------------------------------- |
| Frontend    | Streamlit                       |
| Backend     | Flask                           |
| AI Model    | Google Gemini 2.5 Flash         |
| PDF Parsing | pdfplumber                      |
| Language    | Python                          |
| Deployment  | Local (ideal for presentations) |


## 📦 Project Structure
```
Medical_Report_Simplifier/
│
├── backend/
│   ├── app.py          # Flask API for PDF → Text → LLM pipeline
│
├── frontend/
│   ├── app.py          # Streamlit UI for PDF upload and display
│
├── venv/               # Virtual environment
│
└── README.md           # Project documentation
```
---

## 🛠️ How It Works
```bash
-User uploads a PDF medical report via Streamlit
-Streamlit sends the file to the Flask backend
-Backend extracts text using pdfplumber
-Extracted text is sent to Gemini 2.5 Flash
-The model returns a simplified, patient-friendly explanation
-Streamlit displays the explanation in clean format
```

--- 