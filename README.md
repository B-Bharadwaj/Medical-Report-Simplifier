# ⭐ LLM-Based Medical Report Simplifier with Safety & Quality Assurance

This system converts complex medical reports into clear, patient-friendly explanations using **Gemini 2.5 Flash**, enhanced with a **Safety & Quality Evaluation Pipeline** that ensures medical accuracy, meaning preservation, and improved readability.

Designed for **academic research**, **final-year projects**, and **healthcare explainability** use cases.

---

## 🚀 Features

### 🩺 1. Medical Report Simplification
The system rewrites medical reports in multiple formats:

- **Summary Only**  
- **Summary + Key Findings**  
- **Full Detailed Explanation**

Users can choose conciseness levels:
- **Short**
- **Medium**
- **Detailed**

All outputs ensure:
- No extra medical information is added  
- Patient-friendly explanations  
- Clear, structured, readable formatting  

---

### 🔐 2. Safety & Quality Evaluation  
**(Key Novel Contribution of the Project)**  

- Every simplified report undergoes a strict evaluation pipeline:

#### ✔ Semantic Content Retention (SCR)
- Measures whether the simplified text preserves the meaning of the original using sentence embeddings.

#### ✔ Negation Safety
Detects changes to crucial negations such as:  
- “no fracture”  
- “not malignant”  
- “no evidence of …”

#### ✔ Critical Medical Term Retention
- Ensures essential clinical terms (e.g., *lesion, embolism, fracture, carcinoma*) are not lost.

#### ✔ Readability Score
- Uses **Flesch–Kincaid Grade Level** to compare complexity **before vs. after** simplification.

#### ✔ Safe Rewrite Module
- If any important term or negation is missing, the system **automatically corrects and rewrites** the output in simpler, safe language.

---

### 🤖 3. Patient Follow-Up Chat Assistant
Users can ask questions **based  on the simplified report**.

Assistant capabilities:
- Answers using information strictly from the report  
- Avoids medical diagnosis or treatment advice  
- Responds clearly and supportively  

---

## 🧠 System Architecture
```
User Upload (PDF)
│
▼
PDF Text Extraction
│
▼
Gemini 2.5 Flash (LLM Simplification)
│
▼
Generate Simplified Explanation
│
▼
Safety Evaluation Layer
• SCR Score
• Negation Check
• Critical Terms
• Readability
│
▼
Safe Rewrite Module
│
▼
Final Evaluation
│
▼
Final Simplified Report + Safety Metrics
```

---

## 🛠️ Tech Stack

| Component  | Technology |
|------------|------------|
| Backend    | Flask |
| Frontend   | Streamlit |
| LLM        | Gemini 2.5 Flash |
| Embeddings | SentenceTransformers |
| Readability | textstat |
| PDF Parsing | pdfplumber |

---
### 📊 Quantitative Evaluation (Academic Scoring)
- Readability grade improved from 14–16 → 7–9
- SCR scores show high meaning preservation
- Negation safety: 100% maintained
- Essential medical terms retained or safely reinserted

These results demonstrate that the system significantly improves patient understanding without compromising medical accuracy.

---

## 📦 Installation
```bash
1. Clone the Repository
  -git clone https://github.com/yourusername/Medical-Report-Simplifier.git
  -cd Medical-Report-Simplifier

2. Create Virtual Environment
  -python -m venv venv
  -venv\Scripts\activate       # Windows
  -source venv/bin/activate    # Mac/Linux

3. Install Dependencies
  -pip install -r requirements.txt

4. Add Your Gemini API Key
  -Create a .env file inside backend/:
  -GOOGLE_API_KEY=YOUR_KEY_HERE

5.Running the Project
  -Start Backend
  -python backend/app.py
  -Start Frontend
  -streamlit run frontend/app.py
```
