from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

# ---- Load model in 4-bit mode ----
model_name = "mistralai/Mistral-7B-Instruct-v0.2"

# Configure quantization
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",          # normal float 4-bit
    bnb_4bit_use_double_quant=True,     # adds extra compression
    bnb_4bit_compute_dtype=torch.float16
)

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Load model to GPU with quantization
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="cuda"   # 🔥 force all layers to GPU
)

print("✅ Model loaded in 4-bit mode on GPU!")

def simplify(text):
    # Simple, clear prompt
    prompt = f"Simplify this medical report for a patient:\n{text}\nSimplified:"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")

    # Generation settings for coherent, short explanations
    outputs = model.generate(
        **inputs,
        max_new_tokens=150,
        temperature=0.7,
        top_p=0.9,
        do_sample=True
    )

    # Decode
    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    simplified = output_text.split("Simplified:")[-1].strip()
    return simplified


# Example test
example = "CT scan shows a small lesion in the liver with fatty infiltration."
print("Input:", example)
print("Output:", simplify(example))
