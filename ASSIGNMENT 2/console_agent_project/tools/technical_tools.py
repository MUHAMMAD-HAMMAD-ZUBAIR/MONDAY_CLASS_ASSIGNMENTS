# tools/technical_tools.py

def check_logs(context):
    return "📝 System logs checked. No major issues found."

def restart_service(context):
    if context.issue_type != "technical":
        return "❌ Restart service is only for technical issues."
    return "🔁 Service restarted successfully!"
