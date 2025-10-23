from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Adapter and base model paths
adapter_model = "./models/mistral_lora"
output_merged = "./models/mistral_merged"

# Load adapter config to get correct base model
config = PeftConfig.from_pretrained(adapter_model)
base_model = config.base_model_name_or_path  # mistralai/Mistral-7B-Instruct-v0.2

print(f"🔹 Loading base model: {base_model}")
base = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto", torch_dtype=torch.float16)

print("🔹 Loading adapter weights...")
model = PeftModel.from_pretrained(base, adapter_model)

print("🔹 Merging adapter into base model...")
model = model.merge_and_unload()

# Save merged model + tokenizer
print("🔹 Saving merged model...")
model.save_pretrained(output_merged)
tokenizer = AutoTokenizer.from_pretrained(base_model)
tokenizer.save_pretrained(output_merged)

print("✅ Merge complete! Merged model saved at:", output_merged)
