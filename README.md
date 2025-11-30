# 🩺 Medical Report Simplifier  
### Convert complex medical reports into clear, patient-friendly explanations.

This project takes any uploaded **medical report (PDF)** and automatically:

- Extracts medical text from the PDF  
- Simplifies the content using **Gemini 2.5 Flash**
- Allows follow-up questions through an integrated **medical chatbot**
- Generates a downloadable simplified summary  
- Organizes information in a clean Streamlit UI  

Ideal for patients, students, and clinicians who want instant, easy-to-understand explanations.

---

## 🚀 Features

### 1. PDF Text Extraction  
Uses `pdfplumber` to accurately extract text from medical PDFs.

### 2. Medical Text Simplification  
Powered by **Google Gemini 2.5 Flash**, providing:
- Patient-friendly explanations  
- Student-level summaries  
- Clinical bullet points  

### 3. Adjustable Output Controls  
Through the sidebar, users can choose:
- **Conciseness**: Short / Medium / Detailed  
- **Output Format**: Summary Only / Key Findings / Full Explanation  

### 4. Integrated Medical Chatbot 🤖  
After generating the report, the user can ask follow-up questions like:
- “What does lymphovascular invasion mean?”  
- “Is this type of cancer serious?”  
- “What are the next treatment steps?”  

The chatbot uses:
- The simplified report  
- Chat history  
to generate context-aware answers.

### 5. Downloadable Summary  
Users can download:
- **TXT file**
- (Optional) PDF output (backend-ready)

---

## 🧠 System Architecture
```
📁 Medical-Report-Simplifier
│
├── backend/
│ ├── app.py # Flask backend
│ ├── utils.py # PDF extraction & helpers
│ ├── requirements.txt
│ └── .env # API key (ignored by Git)
│
├── frontend/
│ └── app.py # Streamlit UI
│
├── .gitignore
├── README.md
└── files/
└── sample_reports/
```


---

## 🛠️ Tech Stack

### **Frontend**
- Streamlit

### **Backend**
- Flask  
- Google Gemini 2.5 Flash (API)
- pdfplumber
- python-dotenv
- fpdf (optional PDF generation)

### **Tools**
- Git & GitHub  
- Virtual environments  
- `.env` secrets handling

---

## 📡 API Endpoints

### **POST /simplify**
Simplifies uploaded medical PDF.

**Request:**
- `file` → PDF    
- `conciseness` → Short / Medium / Detailed  
- `format` → Summary Only / Key Findings / Full Explanation  

**Response:**
```json
{
  "simplified_text": "Final simplified output…"
}
```
---
# 🧪 How to Run Locally
```bash
1. Clone the repository
git clone https://github.com/B-Bharadwaj/Medical-Report-Simplifier.git
cd Medical-Report-Simplifier

2. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install -r backend/requirements.txt

4. Set up your .env

Create the .env file:

backend/.env

Add your Google API key inside it:

GOOGLE_API_KEY=your_api_key_here

5. Run backend
cd backend
python app.py

6.Run frontend
cd ../frontend
streamlit run app.py
```