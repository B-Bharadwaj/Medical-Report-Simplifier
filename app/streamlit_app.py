import streamlit as st
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel

# --- Load model once, cache for faster startup ---
@st.cache_resource
def load_model():
    model_name = "mistralai/Mistral-7B-Instruct-v0.2"
    adapter_path = "./models/mistral_lora"   # fine-tuned LoRA adapter (optional)

    # Configure quantization (4-bit GPU mode)
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.float16
    )

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # Load base model in quantized mode on GPU
    base = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="cuda"
    )

    # Load adapter (fine-tuned weights), or just use base if not fine-tuned
    model = base
    print("✅ Base Mistral-7B-Instruct model running in 4-bit mode on GPU (LoRA skipped).")


    model.config.pad_token_id = tokenizer.pad_token_id
    model.eval()
    return tokenizer, model


tokenizer, model = load_model()

# --- Streamlit page setup ---
st.set_page_config(
    page_title="🧠 Medical Report Simplifier",
    page_icon="💊",
    layout="wide",
)

st.title("🧠 Medical Report Simplifier")
st.write("Convert complex medical language into easy-to-understand explanations for patients.")

# --- Text input box ---
text = st.text_area("🩺 Paste or type the medical report here:", height=200)

# --- Simplify button ---
# --- Simplify button ---
# --- Simplify button ---
if st.button("Simplify"):
    if text.strip():
        with st.spinner("Simplifying... please wait ⏳"):
            device = "cuda" if torch.cuda.is_available() else "cpu"

            # ✅ Chat-style format for Mistral-Instruct
            prompt = (
                "[INST] You are a medical professional. "
                "Read the following report and explain it clearly and simply for a patient. "
                "Avoid medical jargon. [/INST]\n"
                f"{text}\n"
            )

            inputs = tokenizer(prompt, return_tensors="pt").to(device)

            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=350,
                    temperature=0.8,
                    top_p=0.95,
                    do_sample=True,
                    repetition_penalty=1.1,
                    pad_token_id=tokenizer.eos_token_id,
                    eos_token_id=tokenizer.eos_token_id,
                    min_length=100,  # ensure continuation
                )

            output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            print("\nRAW OUTPUT:\n", output_text)

            # ✅ Extract meaningful response (after [/INST])
            if "[/INST]" in output_text:
                simplified = output_text.split("[/INST]")[-1].strip()
            else:
                simplified = output_text.replace(prompt, "").strip()

            if not simplified or simplified.lower().startswith("you are"):
                simplified = "⚠️ Model produced no valid output — try a shorter or simpler report."

        st.success("✅ Simplified Explanation:")
        st.write(simplified)
    else:
        st.warning("⚠️ Please enter a medical report to simplify.")



# --- Footer ---
st.markdown(
    """
    ---
    💡 *Powered by Mistral-7B-Instruct (4-bit Quantized) — Runs on GPU ⚡*
    """
)
