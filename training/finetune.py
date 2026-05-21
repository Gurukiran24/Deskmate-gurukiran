from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer
)
import torch
MODEL_NAME = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
tokenizer.pad_token = tokenizer.eos_token
dataset = load_dataset(
    "json",
    data_files="data/raw/helpdesk.jsonl"
)
def format_example(example):
    text = f"Instruction: {example['instruction']}\nResponse: {example['response']}"
    return {"text": text}
dataset = dataset.map(format_example)
def tokenize(example):
    tokens = tokenizer(
        example["text"],
        truncation=True,
        padding="max_length",
        max_length=256
    )
    tokens["labels"] = tokens["input_ids"].copy()
    return tokens
tokenized_dataset = dataset.map(tokenize, batched=True)
training_args = TrainingArguments(
    output_dir="./results",
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=2,
    save_steps=50,
    save_total_limit=2,
    logging_steps=10,
    learning_rate=5e-5,
    fp16=False
)
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"]
)
trainer.train()
model.save_pretrained("model")
tokenizer.save_pretrained("model")
