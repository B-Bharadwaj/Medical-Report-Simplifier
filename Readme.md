# 🧠Medical Report Simplifier 💊


<p align="center"> <img src="C:\Users\bhara\OneDrive\Documents\Medical_Report_Simplifier\UI_preview.png" alt="Medical Report Simplifier Demo" width="750"/> </p>

**Medical Report Simplifier** is a Streamlit-based AI application that converts complex medical jargon into **easy-to-understand, patient-friendly explanations**.  
The app uses **Mistral-7B-Instruct**, fine-tuned using **LoRA adapters** on a custom dataset of medical reports and their simplified counterparts.

---

## 🚀 Features
- 🏥 Converts dense clinical reports into plain English  
- 🤖 Powered by **Mistral-7B-Instruct (LoRA fine-tuned)**  
- ⚡ Runs on GPU with **4-bit quantization** for faster inference  
- 🧾 Interactive **Streamlit UI**  
- 🧠 Automatically detects missing padding tokens and handles EOS properly   

---

##📊 Dataset

-The fine-tuning dataset was built using 111 paired samples of:
-Original clinical statements
-Simplified patient explanations
stored in:
data/processed/paired_dataset.csv

---

## 🧩 Project Structure
```
Medical_Report_Simplifier/
│
├── data/
│ ├── raw/ # Original dataset
│ ├── processed/ # Paired simplified dataset
│
├── models/
│ ├── mistral_lora/ # Fine-tuned adapter weights
│ └── mistral_merged/ # Fully merged model (optional)
│
├── notebooks/
│ ├── fine_tune_mistral.py # Fine-tuning script
│ ├── merge_adapter_fixed.py # Adapter merging script
│ └── test_mistral_model.py # Local inference test
│
├── app/
│ └── streamlit_app.py # Streamlit interface
│
├── requirements.txt
└── README.md
```
---

##⚙️ Tech Stack
-🧠 Model: Mistral-7B-Instruct-v0.2
-🧩 Fine-tuning: PEFT + LoRA
-⚙️ Quantization: BitsAndBytes (4-bit)
-🖥️ Frontend: Streamlit
-🔥 Backend: PyTorch

---