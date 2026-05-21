from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import sys
from pathlib import Path
sys.path.append("inference")
from tools import (
    check_software_access, create_ticket, reset_password,
    get_ticket_status, check_vpn_status, get_user_info, get_all_tickets
)

app = FastAPI(title="IT Helpdesk LLM API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "model"
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH)
model.eval()

class ChatRequest(BaseModel):
    message: str
    user_name: str = None

class ToolCall(BaseModel):
    tool: str
    args: dict

def detect_intent(message: str) -> dict:
    msg_lower = message.lower()
    intent = {"tool": None, "args": {}}
    
    if any(kw in msg_lower for kw in ["software", "access", "permission"]):
        intent["tool"] = "check_software_access"
    elif "ticket" in msg_lower:
        if any(c.isdigit() for c in message) or "status" in msg_lower:
            intent["tool"] = "get_ticket_status"
        else:
            intent["tool"] = "create_ticket"
    elif any(kw in msg_lower for kw in ["vpn", "connect"]):
        intent["tool"] = "check_vpn_status"
    elif any(kw in msg_lower for kw in ["password", "reset", "forgot"]):
        intent["tool"] = "reset_password"
    elif any(kw in msg_lower for kw in ["user", "who is"]):
        intent["tool"] = "get_user_info"
    
    return intent

def execute_tool(tool_name: str, message: str, user_name: str = None) -> dict:
    try:
        if tool_name == "check_software_access" and user_name:
            return check_software_access(user_name)
        elif tool_name == "create_ticket" and user_name:
            return create_ticket(user_name, message)
        elif tool_name == "reset_password" and user_name:
            return reset_password(user_name)
        elif tool_name == "check_vpn_status" and user_name:
            return check_vpn_status(user_name)
        elif tool_name == "get_user_info" and user_name:
            return get_user_info(user_name)
        elif tool_name == "get_ticket_status":
            return get_ticket_status(message)  # ticket_id in message
    except Exception as e:
        return {"success": False, "error": str(e)}
    return {"success": False, "error": "Tool execution failed"}

def generate_response(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    input_length = inputs["input_ids"].shape[1]
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=input_length + 80,
            min_length=input_length + 10,
            do_sample=True,
            temperature=0.9,
            top_p=0.95,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id
        )
    
    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)
    if "Response:" in decoded:
        return decoded.split("Response:")[1].strip()
    return decoded.strip()

@app.get("/")
def root():
    return {"message": "IT Helpdesk LLM API", "endpoints": ["/chat", "/generate"]}

@app.get("/chat")
def serve_chat_page():
    return FileResponse(Path(__file__).parent.parent / "frontend" / "chat.html")

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    execution_trace = []
    tool_result = None
    
    intent = detect_intent(request.message)
    execution_trace.append(f"Detected intent: {intent}")
    
    if intent["tool"]:
        tool_result = execute_tool(intent["tool"], request.message, request.user_name)
        execution_trace.append(f"Executed {intent['tool']}: {tool_result}")
    
    system_info = f"Tool result: {tool_result}" if tool_result else ""
    prompt = f"""You are an IT helpdesk assistant.
{system_info}
Instruction: {request.message}
Response:"""
    
    llm_response = generate_response(prompt)
    execution_trace.append(f"Generated response via LLM")
    
    return {
        "message": request.message,
        "response": llm_response,
        "tool_used": intent["tool"],
        "tool_result": tool_result,
        "execution_trace": execution_trace
    }

@app.post("/generate")
def generate_helpdesk_response(request: ChatRequest):
    response = generate_response(f"Instruction: {request.message}\nResponse:")
    return {
        "message": request.message,
        "response": response
    }