def detect_intent(user_input: str) -> str:
    text = user_input.lower()
    if "refund" in text or "money" in text:
        return "refund"
    elif "payment" in text or "status" in text:
        return "pay_status"
    elif "restart" in text:
        return "restart_service"
    elif "log" in text or "crash" in text:
        return "check_logs"
    elif "faq" in text or "question" in text:
        return "faq"
    else:
        return "general"
