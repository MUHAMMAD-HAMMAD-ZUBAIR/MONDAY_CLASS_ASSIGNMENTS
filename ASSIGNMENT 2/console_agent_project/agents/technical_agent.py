# agents/technical_agent.py

from tools.technical_tools import check_logs, restart_service

def technical_agent(context, user_input):
    print("🛠️ Routed to Technical Agent")
    if "restart" in user_input.lower():
        return restart_service(context)
    return check_logs(context)
