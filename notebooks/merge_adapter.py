from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer

base_model = "mistralai/Mistral-7B-Instruct-v0.2"
adapter_model = "./models/mistral_lora"
output_merged = "./models/mistral_merged"

base = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto")
model = PeftModel.from_pretrained(base, adapter_model)
model = model.merge_and_unload()       # permanently merges adapter weights
model.save_pretrained(output_merged)

tokenizer = AutoTokenizer.from_pretrained(base_model)
tokenizer.save_pretrained(output_merged)

print("✅ Merged model saved at", output_merged)
