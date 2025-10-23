# fine_tune_mistral.py
import torch
import pandas as pd
from transformers import BitsAndBytesConfig
from torch.utils.data import Dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer
from peft import LoraConfig, get_peft_model

# ---------------------
# 1. Load dataset
# ---------------------
df = pd.read_csv("data/processed/paired_dataset.csv")

class SimplifyDataset(Dataset):
    def __init__(self, tokenizer, data, max_len=512):
        self.tokenizer = tokenizer
        self.data = data
        self.max_len = max_len

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        row = self.data.iloc[idx]
        text = f"Simplify the medical report: {row['input_text']}\nSimplified:"
        tokenized = self.tokenizer(
            text, truncation=True, padding="max_length", max_length=self.max_len, return_tensors="pt"
        )
        labels = self.tokenizer(
            row['output_text'], truncation=True, padding="max_length", max_length=self.max_len, return_tensors="pt"
        )
        tokenized["labels"] = labels["input_ids"]
        return {k: v.squeeze() for k, v in tokenized.items()}


# ---------------------
# 2. Load model & tokenizer
# ---------------------
model_name = "mistralai/Mistral-7B-Instruct-v0.2"

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 🩹 Fix: assign a padding token if missing
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# Quantization config (replaces deprecated load_in_4bit argument)
bnb_config = BitsAndBytesConfig(load_in_4bit=True)

# Load model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    quantization_config=bnb_config,
)

# Ensure model knows what pad token to use
model.config.pad_token_id = tokenizer.pad_token_id
# ---------------------
# 3. Apply LoRA (parameter-efficient fine-tuning)
# ---------------------
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)
model = get_peft_model(model, lora_config)

# ---------------------
# 4. Prepare data
# ---------------------
dataset = SimplifyDataset(tokenizer, df)
train_size = int(0.9 * len(dataset))
train_dataset, eval_dataset = torch.utils.data.random_split(dataset, [train_size, len(dataset) - train_size])

# ---------------------
# 5. Training setup
# ---------------------
training_args = TrainingArguments(
    output_dir="./models/mistral_lora",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    warmup_steps=20,
    num_train_epochs=1,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_steps=500,
    eval_steps=500,
    report_to="none",  # disables WandB / HF logging
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
model.save_pretrained("./models/mistral_lora")
tokenizer.save_pretrained("./models/mistral_lora")

print("✅ Fine-tuning completed and model saved in ./models/mistral_lora")
