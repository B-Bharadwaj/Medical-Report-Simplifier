import streamlit as st
import requests

st.title("🩺 Medical Report Simplifier")

uploaded_file = st.file_uploader("Upload your medical report (PDF)", type="pdf")

if uploaded_file:
    with st.spinner("Extracting and simplifying..."):
        response = requests.post(
            "http://localhost:5000/simplify",
            files={"file": uploaded_file}
        )

        if response.status_code == 200:
            simplified_text = response.json()["simplified"]
            st.subheader("Simplified Explanation:")
            st.write(simplified_text)
        else:
            st.error("Error processing file.")
