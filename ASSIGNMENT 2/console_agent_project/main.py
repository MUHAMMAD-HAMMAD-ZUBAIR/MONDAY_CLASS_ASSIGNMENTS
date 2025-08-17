# 🌍 Smart Country Info Agent using Gemini API via OpenAI Adapter
# 👨‍💻 Author: Muhammad Hammad Zubair

from context_model import UserContext
from agents.triage_agent import triage_agent
from utils.guardrail import apply_guardrails
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

console = Console()

def main():
    console.print(Panel("🔥 [bold cyan]M.H.Z Intelligent Support Console[/]", subtitle="Made by M.H.Z", style="bright_blue"))
    
    name = prompt("👤 Name: ", history=InMemoryHistory())
    is_premium = prompt("💎 Premium user (yes/no): ", history=InMemoryHistory()).strip().lower() == "yes"
    issue_type = prompt("❓ Issue type (billing/technical/general): ", history=InMemoryHistory()).strip().lower()

    context = UserContext(name=name, is_premium_user=is_premium, issue_type=issue_type)

    console.print("\n[bold green]Type your support query below. ('exit' to quit)[/]")
    while True:
        console.print("\n" + "-"*60, style="grey37")
        user_input = prompt("⚡ Query>>> ", history=InMemoryHistory())

        if user_input.strip().lower() == "exit":
            console.print(Panel("[bold magenta]✅ Thank you for using M.H.Z Agents. Goodbye![/]", style="magenta"))
            break

        console.print(Text("🧠 Processing query through M.H.Z Intelligence...", style="bold yellow"))
        
        raw_result = triage_agent(context, user_input)
        safe_result = apply_guardrails(raw_result)

        console.print(Panel(f"[bold white]{safe_result}[/]", title="🤖 M.H.Z Agent Reply", style="green"))

    console.print("\n")

if __name__ == "__main__":
    main()
