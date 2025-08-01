# tools/billing_tools.py

def pay_status(context):
    return f"📄 Payment status for {context.name}: PAID ✅"

def refund(context):
    if not context.is_premium_user:
        return "❌ Refund not allowed for non-premium users."
    return f"💸 Refund initiated for {context.name}"
