# utils/guardrail.py

def apply_guardrails(response: str) -> str:
    forbidden = ["sorry", "apologize", "can't help", "no solution"]
    for word in forbidden:
        if word in response.lower():
            return "⚠️ M.H.Z Agent processed your query but found no clean answer. Please rephrase or contact premium support."
    return response
