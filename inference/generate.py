from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_PATH = "model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)

model.eval()

def generate_response(issue):
    prompt = f"Instruction: {issue}\nResponse:"

    inputs = tokenizer(prompt, return_tensors="pt")

    input_length = inputs["input_ids"].shape[1]

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=input_length + 80,   #  force generation AFTER prompt
            min_length=input_length + 10,   #  prevent early EOS
            do_sample=True,
            temperature=0.9,
            top_p=0.95,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Extract only what comes after "Response:"
    if "Response:" in decoded:
        response = decoded.split("Response:")[1].strip()
    else:
        response = decoded.strip()
    
    return response

if __name__ == "__main__":
    while True:
        issue = input("\nDescribe your IT issue (or type 'exit'): ")
        if issue.lower() == "exit":
            break

        reply = generate_response(issue)
        print(f"\nAI Response:\n", reply)