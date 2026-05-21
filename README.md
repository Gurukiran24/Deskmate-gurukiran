# IT Helpdesk LLM Assistant (Generative AI)

An end-to-end **Generative AI application** that fine-tunes a GPT-style language model for **IT helpdesk issue resolution** and exposes it as a **REST API** using FastAPI.

This project demonstrates the complete lifecycle of a GenAI system — from data preparation and model fine-tuning to inference optimization and API deployment — under realistic **CPU-only constraints**.

---

## Problem Statement

IT helpdesk teams frequently handle repetitive troubleshooting queries such as:

* VPN not connecting
* Outlook emails not syncing
* Hardware peripherals not responding

The objective of this project is to build a **domain-adapted language model** that can generate **contextual, helpdesk-style responses** to such issues and serve them programmatically through an API.

---

## System Architecture

```
Data (JSONL)
   ↓
Fine-tuning (Hugging Face + PyTorch)
   ↓
Trained Language Model
   ↓
Inference Logic with Controlled Decoding
   ↓
FastAPI REST Service
```

---

## Dataset

* **Format:** Instruction–Response pairs (`.jsonl`)
* **Domain:** IT helpdesk troubleshooting
* **Example:**

  ```json
  {
    "instruction": "VPN is not connecting",
    "response": "Ensure the user has an active internet connection, correct credentials, and restart the VPN client."
  }
  ```

### Dataset Design Notes

* Synthetic but domain-specific
* No personal or sensitive data
* Designed to teach **response structure and tone**, not memorization

---

## Model and Training

* **Base model:** `distilgpt2`
* **Architecture:** Causal Language Model (GPT-style)
* **Frameworks:** Hugging Face Transformers, PyTorch
* **Training setup:**

  * CPU-only execution
  * Small batch size
  * Multiple epochs for stability

### Model Artifacts and Version Control

Trained model artifacts are intentionally excluded from version control due to GitHub file size limits and standard machine learning repository practices. The model is generated locally by running the training script, and the repository focuses on providing a reproducible training, inference, and deployment pipeline.

### Model Choice Rationale

`distilgpt2` was selected due to hardware constraints. The training pipeline is **model-agnostic** and can be scaled to larger instruction-tuned models (such as LLaMA or Mistral) using LoRA or QLoRA on GPU-backed systems.

---

## Engineering Challenges and Solutions

### Loss Not Computed During Training

* **Issue:** Model did not return training loss
* **Solution:** Explicitly set `labels = input_ids` for causal language model training

### Empty or Truncated Responses During Inference

* **Issue:** Model terminated generation early due to EOS prediction
* **Solution:**

  * Enforced minimum generation length
  * Applied controlled decoding parameters (`min_length`, `temperature`, `top_p`, `repetition_penalty`)

### Prompt Consistency

* Ensured inference prompts matched the training format:

  ```
  Instruction: <issue>
  Response:
  ```

---

## Inference and Decoding

Inference uses controlled text generation to improve response completeness and prevent premature termination.

Key decoding parameters:

* `max_length` relative to input prompt length
* `min_length` to avoid early EOS
* Sampling-based decoding (`temperature`, `top_p`)
* Repetition control

---

## API Deployment

The trained model is deployed as a REST API using **FastAPI**.

### Endpoint

```
POST /generate
```

### Request Body

```json
{
  "issue": "VPN not connecting"
}
```

### Response

```json
{
  "issue": "VPN not connecting",
  "response": "Not Connect, but disconnect the connection to any other network or router using a device and connect"
}
```

Response quality reflects the limitations of a small model and a constrained dataset. The primary focus of this project is **pipeline correctness, deployment readiness, and engineering design**, not conversational fluency.

---

## Project Structure

```
IT-Helpdesk-LLM/
│── api/            # FastAPI application
│── training/       # Fine-tuning scripts
│── inference/      # Local inference logic
│── data/           # Dataset (JSONL)
│── model/          # Trained model artifacts
│── requirements.txt
│── README.md
```

---

## Running the Project Locally

### Install dependencies

```bash
pip install -r requirements.txt
```

### Train the model

```bash
python training/finetune.py
```

### Start the API server

```bash
uvicorn api.app:app --reload
```

### Test using Swagger UI

Open the following URL in a browser:

```
http://127.0.0.1:8000/docs
```

---

## Scalability and Future Enhancements

* Fine-tune larger instruction-tuned models using LoRA or QLoRA
* Deploy on GPU-backed cloud infrastructure
* Integrate Retrieval-Augmented Generation (RAG)
* Expand dataset size and diversity
* Add monitoring and logging for production inference

---

## Key Takeaways

This project demonstrates:

* Practical understanding of Generative AI pipelines
* Hands-on experience with LLM fine-tuning
* Debugging real-world training and inference issues
* Serving machine learning models as production-style APIs
* Engineering trade-offs under hardware constraints

---
