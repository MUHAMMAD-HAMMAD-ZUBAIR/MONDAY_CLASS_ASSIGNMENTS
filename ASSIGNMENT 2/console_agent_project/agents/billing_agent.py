from tools.billing_tools import pay_status, refund

def billing_agent(context, intent):
    print("💼 [M.H.Z Billing Agent] Handling your issue...")
    if intent == "refund":
        return refund(context)
    return pay_status(context)
