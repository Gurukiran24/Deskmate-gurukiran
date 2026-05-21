import json
from typing import Dict, List, Optional

DB_PATH = "mock_db.json"

def _load_db() -> Dict:
    with open(DB_PATH, "r") as f:
        return json.load(f)

def _save_db(db: Dict) -> None:
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)

def check_software_access(user_name: str) -> Dict:
    db = _load_db()
    for user in db["users"]:
        if user["name"].lower() == user_name.lower():
            return {
                "success": True,
                "user": user["name"],
                "software_access": user["software_access"]
            }
    return {"success": False, "error": f"User '{user_name}' not found"}

def create_ticket(user_name: str, issue: str) -> Dict:
    db = _load_db()
    existing_ids = [int(t["ticket_id"][1:]) for t in db["tickets"]]
    new_id = f"T{max(existing_ids) + 1:04d}" if existing_ids else "T1001"
    
    ticket = {
        "ticket_id": new_id,
        "user": user_name,
        "issue": issue,
        "status": "Open"
    }
    db["tickets"].append(ticket)
    _save_db(db)
    return {"success": True, "ticket": ticket}

def reset_password(user_name: str) -> Dict:
    db = _load_db()
    for user in db["users"]:
        if user["name"].lower() == user_name.lower():
            return {
                "success": True,
                "message": f"Password reset for {user['name']} completed",
                "new_password": "TempPass123!"
            }
    return {"success": False, "error": f"User '{user_name}' not found"}

def get_ticket_status(ticket_id: str) -> Dict:
    db = _load_db()
    for ticket in db["tickets"]:
        if ticket["ticket_id"].upper() == ticket_id.upper():
            return {"success": True, "ticket": ticket}
    return {"success": False, "error": f"Ticket '{ticket_id}' not found"}

def check_vpn_status(user_name: str) -> Dict:
    db = _load_db()
    for user in db["users"]:
        if user["name"].lower() == user_name.lower():
            return {
                "success": True,
                "user": user["name"],
                "vpn_enabled": user["vpn_enabled"],
                "status": "Connected" if user["vpn_enabled"] else "Disconnected"
            }
    return {"success": False, "error": f"User '{user_name}' not found"}

def get_all_tickets() -> Dict:
    db = _load_db()
    return {"success": True, "tickets": db["tickets"]}

def get_user_info(user_name: str) -> Dict:
    db = _load_db()
    for user in db["users"]:
        if user["name"].lower() == user_name.lower():
            return {"success": True, "user": user}
    return {"success": False, "error": f"User '{user_name}' not found"}