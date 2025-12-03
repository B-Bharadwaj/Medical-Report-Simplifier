import streamlit as st
import requests

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Medical Report Simplifier",
    page_icon="🩺",
    layout="wide"
)

st.title("🩺 Medical Report Simplifier")
st.write("Convert complex medical reports into simple, patient-friendly explanations.")

# -------------------- SIDEBAR --------------------
st.sidebar.header("⚙️ Options")

level = "patient"   # Always patient-friendly

conciseness = st.sidebar.radio(
    "Conciseness",
    ["Short", "Medium", "Detailed"],
    index=1
)

output_format = st.sidebar.radio(
    "Output Format",
    ["Summary Only", "Summary + Key Findings", "Full Explanation"],
    index=2
)

st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ About")
st.sidebar.caption("Medical Report Simplifier")
st.sidebar.caption("Built for patient-friendly explanations.")
st.sidebar.caption("Powered by Gemini 2.5 Flash")

backend_url = "http://127.0.0.1:5000/simplify"

# -------------------- FILE UPLOAD --------------------
uploaded_file = st.file_uploader("Upload a medical report (PDF)", type=["pdf"])

# -------------------- MAIN LOGIC --------------------
if uploaded_file is not None:
    st.success("PDF uploaded successfully!")

    if st.button("Simplify Report"):
        with st.spinner("Processing your medical report..."):

            try:
                # Send request to backend
                files = {"file": uploaded_file}
                payload = {
                    "level": level,
                    "conciseness": conciseness,
                    "format": output_format
                }

                response = requests.post(backend_url, data=payload, files=files)

                try:
                    data = response.json()
                except:
                    st.error("Backend sent invalid JSON!")
                    st.code(response.text)
                    st.stop()

                if "error" in data:
                    st.error("Backend Error: " + data["error"])
                    if "trace" in data:
                        st.code(data["trace"])
                    st.stop()

                if "simplified_text" not in data:
                    st.error("Unexpected backend response.")
                    st.write(data)
                    st.stop()

                # Store simplified text in session state
                st.session_state["simplified_report"] = data["simplified_text"]

                # ---------------------------------------------
                # 📝 Simplified Output
                # ---------------------------------------------
                st.subheader("📝 Simplified Explanation")
                st.write(data["simplified_text"])

                # Download buttons
                st.download_button(
                    "📄 Download Text Version",
                    data["simplified_text"],
                    file_name="simplified_report.txt"
                )

                # ---------------------------------------------
                # ⭐ NEW BLOCK — Evaluation Metrics
                # ---------------------------------------------
                st.subheader("📊 Safety & Quality Evaluation")

                # SCR Score
                st.markdown(
                    f"**Meaning Preservation (SCR):** `{data['scr_score']}` "
                    f"— **{data['scr_label'].upper()}**"
                )

                # Negation Check
                if data["negation_safe"]:
                    st.success("🟢 Negation Check: No negation meaning lost.")
                else:
                    st.error("🔴 WARNING: Negation may be incorrectly changed!")

                # Critical Medical Terms
                if len(data["critical_terms_missing"]) == 0:
                    st.success("🟢 No critical medical terms were lost.")
                else:
                    missing = ", ".join(data["critical_terms_missing"])
                    st.error(f"🔴 Missing important medical terms: **{missing}**")

                # Readability
                st.info(f"📘 Readability Grade: **{data['readability_grade']:.2f}**")

            except Exception as e:
                st.error("Frontend Error: " + str(e))

# -------------------- CHATBOT SECTION --------------------
if "simplified_report" in st.session_state:

    st.markdown("## 🤖 Chat with Your Medical Assistant")

    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []

    # Display chat history
    for msg in st.session_state["chat_history"]:
        if msg["role"] == "user":
            st.markdown(f"**🧑 You:** {msg['content']}")
        else:
            st.markdown(f"**🤖 AI:** {msg['content']}")

    user_input = st.text_input("Ask a follow-up question:")

    if st.button("Send"):
        if user_input.strip():
            st.session_state["chat_history"].append(
                {"role": "user", "content": user_input}
            )

            payload = {
                "question": user_input,
                "simplified_report": st.session_state["simplified_report"],
                "chat_history": "\n".join(
                    [f"{m['role']}: {m['content']}" for m in st.session_state["chat_history"]]
                )
            }

            chat_response = requests.post(
                "http://127.0.0.1:5000/chat_followup",
                data=payload
            )

            answer = chat_response.json().get("answer", "Error")

            st.session_state["chat_history"].append(
                {"role": "ai", "content": answer}
            )

            st.rerun()

# -------------------- DEBUG SECTION --------------------
st.markdown("---")
with st.expander("🔍 Debug Information"):
    st.write(st.session_state)
