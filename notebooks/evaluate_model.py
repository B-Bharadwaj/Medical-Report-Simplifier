import pandas as pd
import textstat
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# Load model and tokenizer
model_path = "./models/mistral_lora"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", load_in_4bit=True)

# Load test data
df = pd.read_csv("data/processed/paired_dataset.csv")

def simplify(text):
    prompt = f"Explain in simple, patient-friendly language:\n{text}\nExplanation:"
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda" if torch.cuda.is_available() else "cpu")
    outputs = model.generate(**inputs, max_new_tokens=120)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

results = []
for text in df["input_text"][:10]:  # test first 10
    simplified = simplify(text)
    results.append({
        "original": text,
        "simplified": simplified,
        "original_grade": textstat.flesch_kincaid_grade(text),
        "simplified_grade": textstat.flesch_kincaid_grade(simplified)
    })

out_df = pd.DataFrame(results)
print(out_df[["original", "simplified", "original_grade", "simplified_grade"]])
print("\nAverage Original Grade:", out_df["original_grade"].mean())
print("Average Simplified Grade:", out_df["simplified_grade"].mean())

out_df.to_csv("data/processed/evaluation_results.csv", index=False)
print("\n✅ Results saved to data/processed/evaluation_results.csv")
