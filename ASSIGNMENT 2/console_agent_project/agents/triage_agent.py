from agents.billing_agent import billing_agent
from agents.technical_agent import technical_agent
from agents.general_agent import general_agent
from utils.intent_classifier import detect_intent

def triage_agent(context, user_input):
    intent = detect_intent(user_input)
    print(f"🧠 [M.H.Z Triage AI] Detected intent: {intent}")
    
    if intent in ["refund", "pay_status"]:
        return billing_agent(context, intent)
    elif intent in ["restart_service", "check_logs"]:
        return technical_agent(context, intent)
    elif intent == "faq":
        return general_agent(context, intent)
    else:
        return general_agent(context, "general")
