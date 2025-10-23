from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

adapter_model = "./models/mistral_lora"
output_merged = "./models/mistral_merged"

# Step 1: Read adapter config (auto-detect base)
config = PeftConfig.from_pretrained(adapter_model)
base_model = config.base_model_name_or_path
print(f"🔹 Loading base model: {base_model}")

# Step 2: Load base model cleanly without 4-bit/8-bit or offloading
base = AutoModelForCausalLM.from_pretrained(
    base_model,
    torch_dtype=torch.float16,
    device_map=None  # load fully in memory (prevents meta-device issues)
)

# Step 3: Attach LoRA adapter
print("🔹 Loading LoRA adapter weights...")
model = PeftModel.from_pretrained(base, adapter_model, is_trainable=False)

# Step 4: Force weights copy into base model to avoid meta issues
for name, param in model.named_parameters():
    if "lora" in name and hasattr(param, "data"):
        param.data = param.data.to(torch.float16)

print("🔹 Merging adapter weights into base model...")
model = model.merge_and_unload()

# Step 5: Save final merged model + tokenizer
print("🔹 Saving merged model...")
model.save_pretrained(output_merged)
tokenizer = AutoTokenizer.from_pretrained(base_model)
tokenizer.save_pretrained(output_merged)

print("✅ Merge complete! Merged model saved at", output_merged)
