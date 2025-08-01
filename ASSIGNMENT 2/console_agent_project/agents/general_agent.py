# agents/general_agent.py

from tools.general_tools import faq_response

def general_agent(context, user_input):
    print("📬 Routed to General Agent")
    return faq_response(context)
